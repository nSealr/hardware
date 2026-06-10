#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.export_tropic01_universal_pcbway import collect_preflight_blockers

BOARD_NAME = "tropic01-universal-secure-device"
BOARD_ROOT = ROOT / "pcb" / BOARD_NAME
PRODUCTION_ROOT = BOARD_ROOT / "production"
KICAD_BOARD = BOARD_ROOT / "kicad" / f"{BOARD_NAME}.kicad_pcb"
PREFLIGHT_SUMMARY = PRODUCTION_ROOT / "preflight-summary.json"
ERC_REPORT = PRODUCTION_ROOT / "erc" / "erc.json"
DRC_REPORT = PRODUCTION_ROOT / "drc" / "drc.json"
SCHEMATIC_COVERAGE = PRODUCTION_ROOT / "schematic-coverage.json"
GLB_RENDER = PRODUCTION_ROOT / "step" / f"{BOARD_NAME}.glb"
VRML_RENDER = PRODUCTION_ROOT / "step" / f"{BOARD_NAME}.wrl"
STEP_RENDER = PRODUCTION_ROOT / "step" / f"{BOARD_NAME}.step"
KICAD_CLI_CANDIDATES = (
    "kicad-cli",
    "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli",
)


def kicad_cli_version() -> str:
    for executable in KICAD_CLI_CANDIDATES:
        try:
            completed = subprocess.run(
                [executable, "version"],
                check=True,
                capture_output=True,
                text=True,
            )
        except (OSError, subprocess.CalledProcessError):
            continue
        return completed.stdout.strip()
    return "unavailable"


def load_json(path: Path) -> dict[str, object] | None:
    if not path.exists():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def footprint_blocks(board_text: str) -> list[str]:
    return re.findall(r'\n\t\(footprint "[^"]+"[\s\S]*?(?=\n\t\(footprint |\n\))', board_text)


def ref_for_footprint(block: str) -> str | None:
    match = re.search(r'\(property "Reference" "([^"]+)"', block)
    return match.group(1) if match else None


def layer_for_footprint(block: str) -> str | None:
    match = re.search(r'\n\t\t\(layer "([^"]+)"\)', block)
    return match.group(1) if match else None


def board_statistics(board_path: Path = KICAD_BOARD) -> dict[str, object]:
    text = board_path.read_text(encoding="utf-8", errors="replace")
    front_refs: list[str] = []
    back_refs: list[str] = []
    for block in footprint_blocks(text):
        ref = ref_for_footprint(block)
        layer = layer_for_footprint(block)
        if not ref:
            continue
        if layer == "F.Cu":
            front_refs.append(ref)
        elif layer == "B.Cu":
            back_refs.append(ref)

    outline_match = re.search(
        r'\(gr_rect\s+\(start\s+([-0-9.]+)\s+([-0-9.]+)\)\s+\(end\s+([-0-9.]+)\s+([-0-9.]+)\)[\s\S]*?\(layer "Edge.Cuts"\)',
        text,
    )
    width_mm = None
    height_mm = None
    if outline_match:
        start_x, start_y, end_x, end_y = (float(value) for value in outline_match.groups())
        width_mm = round(abs(end_x - start_x), 3)
        height_mm = round(abs(end_y - start_y), 3)

    tracks = len(re.findall(r"\(segment\s+", text))
    vias = len(re.findall(r"\(via\s+", text))
    zones = len(re.findall(r"\(zone\s+", text))
    return {
        "width_mm": width_mm,
        "height_mm": height_mm,
        "area_mm2": round(width_mm * height_mm, 3) if width_mm is not None and height_mm is not None else None,
        "front_footprints": sorted(front_refs),
        "back_footprints": len(back_refs),
        "tracks": tracks,
        "vias": vias,
        "zones": zones,
    }


def collect_erc_summary(path: Path = ERC_REPORT) -> dict[str, object]:
    report = load_json(path)
    if report is None:
        return {
            "report": "erc/erc.json",
            "violations": None,
            "top_violation_types": {},
        }

    counter: Counter[str] = Counter()
    for sheet in report.get("sheets", []):
        if not isinstance(sheet, dict):
            continue
        for violation in sheet.get("violations", []):
            if isinstance(violation, dict):
                counter[str(violation.get("type", "unknown"))] += 1

    return {
        "report": "erc/erc.json",
        "violations": sum(counter.values()),
        "top_violation_types": dict(counter.most_common(8)),
    }


def collect_drc_summary(board_path: Path = KICAD_BOARD, path: Path = DRC_REPORT) -> dict[str, object]:
    report = load_json(path)
    fresh = bool(report is not None and path.exists() and path.stat().st_mtime >= board_path.stat().st_mtime)
    return {
        "report": "drc/drc.json",
        "fresh_report_available": fresh,
        "last_cli_exit": -1 if not fresh else 0,
        "note": (
            "KiCad CLI DRC aborts before writing a fresh report in this environment; "
            "the existing drc.json is stale and must not be used as release evidence."
        )
        if not fresh
        else "Fresh KiCad CLI DRC report is available.",
    }


def render_outputs() -> dict[str, str]:
    return {
        "glb": str(GLB_RENDER.relative_to(PRODUCTION_ROOT)),
        "vrml": str(VRML_RENDER.relative_to(PRODUCTION_ROOT)),
        "step": str(STEP_RENDER.relative_to(PRODUCTION_ROOT)),
        "step_note": "STEP was emitted, but KiCad reports that local VRML mesh envelope models cannot be used for non-mesh CAD export.",
    }


def pcbway_summary() -> dict[str, object]:
    blockers = collect_preflight_blockers(KICAD_BOARD, PRODUCTION_ROOT)
    return {
        "manifest": "pcbway-manifest.json",
        "release_outputs_valid": not blockers,
        "blocked_reasons": blockers,
    }


def schematic_coverage_summary(path: Path = SCHEMATIC_COVERAGE) -> dict[str, object]:
    value = load_json(path)
    if value is None:
        return {
            "report": "schematic-coverage.json",
            "status": "missing",
            "required_missing_binding_count": None,
        }
    missing = value.get("required_missing_binding", [])
    board_missing = value.get("board_refs_missing_binding", [])
    return {
        "report": "schematic-coverage.json",
        "status": value.get("status", "unknown"),
        "required_missing_binding_count": len(missing) if isinstance(missing, list) else None,
        "required_missing_refs": [item.get("ref") for item in missing if isinstance(item, dict)],
        "board_refs_missing_binding_count": len(board_missing) if isinstance(board_missing, list) else None,
        "board_refs_missing_binding": board_missing if isinstance(board_missing, list) else [],
    }


def build_preflight_summary() -> dict[str, object]:
    return {
        "board": BOARD_NAME,
        "date": date.today().isoformat(),
        "status": "ready_for_fabrication_review"
        if not collect_preflight_blockers(KICAD_BOARD, PRODUCTION_ROOT)
        else "blocked_preflight",
        "kicad_cli_version": kicad_cli_version(),
        "mechanical_render_outputs": render_outputs(),
        "board_statistics": board_statistics(),
        "schematic_coverage": schematic_coverage_summary(),
        "erc": collect_erc_summary(),
        "drc": collect_drc_summary(),
        "pcbway": pcbway_summary(),
    }


def write_preflight_summary(path: Path = PREFLIGHT_SUMMARY) -> None:
    path.write_text(json.dumps(build_preflight_summary(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    write_preflight_summary()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
