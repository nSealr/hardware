#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOARD_NAME = "tropic01-universal-secure-device"
BOARD_ROOT = ROOT / "pcb" / BOARD_NAME
PRODUCTION_ROOT = BOARD_ROOT / "production"
BOM_CSV = ROOT / "bom" / f"{BOARD_NAME}.csv"
KICAD_BOARD = BOARD_ROOT / "kicad" / f"{BOARD_NAME}.kicad_pcb"
SCHEMATIC_BINDING = PRODUCTION_ROOT / "schematic-binding.json"
COVERAGE_JSON = PRODUCTION_ROOT / "schematic-coverage.json"

BOARD_ONLY_FREEZE_STATUSES = {"footprint_only", "tuning_required"}
BOARD_ONLY_REFS = {"DISP1", "ANT1", "BAT1", "MH1", "MH2"}


def split_designators(value: str) -> list[str]:
    return [item.strip() for item in value.replace(",", " ").split() if item.strip()]


def load_bom_rows(path: Path = BOM_CSV) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [{key: value or "" for key, value in row.items()} for row in csv.DictReader(handle)]


def board_refs(path: Path = KICAD_BOARD) -> set[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    return set(re.findall(r'\(property "Reference" "([^"]+)"', text))


def binding_refs(path: Path = SCHEMATIC_BINDING) -> set[str]:
    value = json.loads(path.read_text(encoding="utf-8"))
    return set(value["components"])


def required_bom_refs(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    refs: dict[str, dict[str, str]] = {}
    for row in rows:
        if row.get("required", "").strip().lower() != "true":
            continue
        for ref in split_designators(row.get("designator", "")):
            if ref.endswith("_ALT"):
                continue
            refs[ref] = row
    return refs


def is_board_only_ref(ref: str, row: dict[str, str] | None) -> bool:
    if ref in BOARD_ONLY_REFS or ref.startswith("TP_"):
        return True
    if row and row.get("freeze_status", "").strip().lower() in BOARD_ONLY_FREEZE_STATUSES:
        return True
    if row and row.get("footprint", "").strip().startswith("Mechanical:"):
        return True
    return False


def build_coverage() -> dict[str, object]:
    rows = load_bom_rows()
    required_refs = required_bom_refs(rows)
    current_board_refs = board_refs()
    current_binding_refs = binding_refs()

    required_missing = []
    for ref, row in sorted(required_refs.items()):
        if ref in current_binding_refs or is_board_only_ref(ref, row):
            continue
        required_missing.append(
            {
                "ref": ref,
                "description": row.get("description", ""),
                "mpn": row.get("mpn", ""),
                "datasheet": row.get("datasheet", ""),
                "reason": "required BOM/PCB component has no schematic-binding component yet",
            }
        )

    board_missing = []
    for ref in sorted(current_board_refs - current_binding_refs):
        row = required_refs.get(ref)
        if is_board_only_ref(ref, row):
            continue
        board_missing.append(ref)

    if required_missing:
        status = "blocked_until_required_refs_are_bound"
    elif board_missing:
        status = "blocked_until_all_pcba_refs_are_bound"
    else:
        status = "required_refs_bound"

    return {
        "board": BOARD_NAME,
        "status": status,
        "board_ref_count": len(current_board_refs),
        "binding_ref_count": len(current_binding_refs),
        "required_missing_binding": required_missing,
        "board_refs_missing_binding": board_missing,
        "allowed_board_only_refs": sorted(ref for ref in current_board_refs if is_board_only_ref(ref, required_refs.get(ref))),
        "release_gates": [
            "all_required_pcba_refs_in_schematic_binding",
            "no_physical_pcba_component_without_symbol_or_documented_board_only_policy",
            "component_pin_bindings_must_be_datasheet_backed_before_routing",
        ],
    }


def write_coverage(path: Path = COVERAGE_JSON) -> None:
    path.write_text(json.dumps(build_coverage(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    write_coverage()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
