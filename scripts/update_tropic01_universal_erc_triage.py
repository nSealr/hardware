#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOARD_NAME = "tropic01-universal-secure-device"
PRODUCTION_ROOT = ROOT / "pcb" / BOARD_NAME / "production"
ERC_REPORT = PRODUCTION_ROOT / "erc" / "erc.json"
TRIAGE_JSON = PRODUCTION_ROOT / "erc" / "triage.json"
TRIAGE_MD = PRODUCTION_ROOT / "erc" / "triage.md"


ACTION_BY_TYPE = {
    "pin_not_connected": (
        "Complete the generated schematic binding for each real pin, or add explicit no-connect markers "
        "only where the component datasheet confirms the pin is unused in this design."
    ),
    "isolated_pin_label": (
        "Connect the matching endpoint on another generated sheet or replace the label-only scaffold with "
        "real circuit elements. Do not treat a one-pin global label as a production connection."
    ),
    "unconnected_wire_endpoint": (
        "Fix the schematic generator pin/label geometry so generated wires land on KiCad electrical "
        "connection points and grid coordinates."
    ),
    "power_pin_not_driven": (
        "Add the real power tree, regulator/load-switch symbols, PWR_FLAGs where appropriate, and KiCad "
        "power symbols for driven rails."
    ),
    "pin_not_driven": (
        "Connect the required driver/source for input pins, or correct the symbol electrical type only "
        "after source-backed symbol review."
    ),
    "label_dangling": (
        "Remove stale labels or connect them to real sheet pins/components. A dangling label must not be "
        "waived in the fabrication package."
    ),
    "footprint_link_issues": (
        "Replace generic connector symbols or footprint fields with source-backed library references that "
        "match the selected manufacturing footprints."
    ),
    "ground_pin_not_ground": (
        "Use the KiCad GND power symbol/net consistently for ground pins and verify the generated labels "
        "resolve to the canonical GND net."
    ),
}


def load_erc(path: Path = ERC_REPORT) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def item_description(violation: dict[str, object]) -> str:
    items = violation.get("items", [])
    if isinstance(items, list) and items and isinstance(items[0], dict):
        return str(items[0].get("description", ""))
    return str(violation.get("description", ""))


def build_triage(report: dict[str, object]) -> dict[str, object]:
    by_type: Counter[str] = Counter()
    by_sheet: dict[str, Counter[str]] = defaultdict(Counter)
    examples: dict[str, list[str]] = defaultdict(list)

    for sheet in report.get("sheets", []):
        if not isinstance(sheet, dict):
            continue
        sheet_path = str(sheet.get("path", "/"))
        for violation in sheet.get("violations", []):
            if not isinstance(violation, dict):
                continue
            violation_type = str(violation.get("type", "unknown"))
            by_type[violation_type] += 1
            by_sheet[sheet_path][violation_type] += 1
            description = item_description(violation)
            if description and description not in examples[violation_type] and len(examples[violation_type]) < 5:
                examples[violation_type].append(description)

    return {
        "board": BOARD_NAME,
        "source_report": "erc/erc.json",
        "total_violations": sum(by_type.values()),
        "by_type": {
            violation_type: {
                "count": count,
                "recommended_action": ACTION_BY_TYPE.get(
                    violation_type,
                    "Review this ERC class manually and document the source-backed fix before routing.",
                ),
                "examples": examples.get(violation_type, []),
            }
            for violation_type, count in by_type.most_common()
        },
        "by_sheet": {
            sheet: dict(counter.most_common())
            for sheet, counter in sorted(by_sheet.items(), key=lambda item: item[0])
        },
        "release_policy": [
            "Do not upload the PCBWay package while ERC triage total_violations is non-zero.",
            "Do not add ERC waivers to make the report green unless the waiver is tied to a reviewed datasheet decision.",
            "Prefer improving the schematic generator and source-backed bindings over editing generated sheets by hand.",
        ],
    }


def render_markdown(triage: dict[str, object]) -> str:
    lines = [
        "# ERC Triage",
        "",
        f"Board: `{triage['board']}`",
        f"Source report: `{triage['source_report']}`",
        f"Total violations: `{triage['total_violations']}`",
        "",
        "This is a blocking fabrication artifact. It explains what must be fixed before the PCBWay package can be treated as a release candidate.",
        "",
        "## By Type",
        "",
        "| Type | Count | Required action |",
        "| --- | ---: | --- |",
    ]
    for violation_type, value in triage["by_type"].items():
        lines.append(
            f"| `{violation_type}` | {value['count']} | {value['recommended_action']} |"
        )

    lines.extend(["", "## By Sheet", ""])
    for sheet, counts in triage["by_sheet"].items():
        rendered_counts = ", ".join(f"`{key}`: {value}" for key, value in counts.items())
        lines.append(f"- `{sheet}`: {rendered_counts}")

    lines.extend(["", "## Release Policy", ""])
    for item in triage["release_policy"]:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def write_triage() -> None:
    triage = build_triage(load_erc())
    TRIAGE_JSON.write_text(json.dumps(triage, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    TRIAGE_MD.write_text(render_markdown(triage), encoding="utf-8")


def main() -> int:
    write_triage()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
