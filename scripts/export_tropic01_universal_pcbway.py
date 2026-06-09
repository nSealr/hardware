#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOARD_NAME = "tropic01-universal-secure-device"
SOURCE_BOM = ROOT / "bom" / f"{BOARD_NAME}.csv"
PRODUCTION_ROOT = ROOT / "pcb" / BOARD_NAME / "production"
KICAD_BOARD = ROOT / "pcb" / BOARD_NAME / "kicad" / f"{BOARD_NAME}.kicad_pcb"
ERC_REPORT = PRODUCTION_ROOT / "erc" / "erc.json"
DRC_REPORT = PRODUCTION_ROOT / "drc" / "drc.json"

PCBWAY_BOM_HEADERS = (
    "Designator",
    "Qty",
    "Manufacturer",
    "Manufacturer Part Number",
    "Description",
    "Package",
    "Footprint",
    "Notes",
)

NON_PCBA_FREEZE_STATUSES = {
    "footprint_only",
    "tuning_required",
}


def load_bom(path: Path = SOURCE_BOM) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [{key: value or "" for key, value in row.items()} for row in csv.DictReader(handle)]


def split_designators(designator: str) -> list[str]:
    return [item.strip() for item in designator.replace(",", " ").split() if item.strip()]


def is_pcba_row(row: dict[str, str]) -> bool:
    if row.get("required", "").strip().lower() != "true":
        return False
    designator = row.get("designator", "").strip()
    if designator.startswith("TP_"):
        return False
    if row.get("freeze_status", "").strip().lower() in NON_PCBA_FREEZE_STATUSES:
        return False
    if row.get("footprint", "").strip().startswith("Mechanical:"):
        return False
    return True


def pcbway_bom_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    exported: list[dict[str, str]] = []
    for row in rows:
        if not is_pcba_row(row):
            continue
        refs = split_designators(row["designator"])
        exported.append(
            {
                "Designator": ",".join(refs),
                "Qty": str(len(refs)),
                "Manufacturer": row.get("manufacturer", ""),
                "Manufacturer Part Number": row.get("mpn", ""),
                "Description": row.get("description", ""),
                "Package": row.get("package", ""),
                "Footprint": row.get("footprint", ""),
                "Notes": row.get("notes", ""),
            }
        )
    return exported


def write_pcbway_bom(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=PCBWAY_BOM_HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def count_kicad_report_violations(report: object) -> int:
    if not isinstance(report, dict):
        return 1

    count = 0
    violations = report.get("violations", [])
    if isinstance(violations, list):
        count += len(violations)

    sheets = report.get("sheets", [])
    if isinstance(sheets, list):
        for sheet in sheets:
            if isinstance(sheet, dict) and isinstance(sheet.get("violations", []), list):
                count += len(sheet["violations"])

    return count


def require_clean_kicad_report(path: Path, label: str) -> None:
    if not path.exists():
        raise ValueError(f"PCBWay export blocked: {label} report missing")

    try:
        report = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"PCBWay export blocked: {label} report is not valid JSON") from exc

    violation_count = count_kicad_report_violations(report)
    if violation_count:
        raise ValueError(f"PCBWay export blocked: {label} violations present ({violation_count})")


def validate_board_ready_for_export(board_path: Path = KICAD_BOARD, production_root: Path = PRODUCTION_ROOT) -> None:
    if not board_path.exists():
        raise ValueError("PCBWay export blocked: no routed KiCad PCB exists")

    text = board_path.read_text(encoding="utf-8", errors="replace")
    real_nets = {net for net in re.findall(r"\(net\s+(\d+)\s+", text) if net != "0"}
    segment_count = len(re.findall(r"\(segment\s+", text))
    via_count = len(re.findall(r"\(via\s+", text))
    routed_item_count = segment_count + via_count

    if routed_item_count == 0 or len(real_nets) <= 1:
        raise ValueError("PCBWay export blocked: no routed KiCad PCB copper exists; board is not routed")

    require_clean_kicad_report(production_root / "erc" / "erc.json", "ERC")
    require_clean_kicad_report(production_root / "drc" / "drc.json", "DRC")


def _mpn_by_designator(rows: list[dict[str, str]]) -> dict[str, str]:
    return {row.get("designator", ""): row.get("mpn", "") for row in rows}


def _required_non_pcba_designators(rows: list[dict[str, str]]) -> list[str]:
    return sorted(row["designator"] for row in rows if row.get("required", "").lower() == "true" and not is_pcba_row(row))


def blocked_manifest(rows: list[dict[str, str]], blocked_reasons: list[str]) -> dict[str, object]:
    mpns = _mpn_by_designator(rows)
    return {
        "board": BOARD_NAME,
        "release_outputs_valid": False,
        "status": "blocked",
        "blocked_reasons": blocked_reasons,
        "usb_connector": mpns.get("J1", ""),
        "second_secure_element": mpns.get("U11", ""),
        "microsd": "excluded",
        "erc": "blocked",
        "drc": "blocked",
        "required_non_pcba_rows": _required_non_pcba_designators(rows),
    }


def release_manifest(rows: list[dict[str, str]]) -> dict[str, object]:
    mpns = _mpn_by_designator(rows)
    return {
        "board": BOARD_NAME,
        "release_outputs_valid": True,
        "status": "ready_for_fabrication_review",
        "usb_connector": mpns.get("J1", ""),
        "second_secure_element": mpns.get("U11", ""),
        "microsd": "excluded",
        "erc": "pass",
        "drc": "pass",
    }


def write_manifest(path: Path, manifest: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def export_blocked_status(reason: str) -> None:
    rows = load_bom()
    write_pcbway_bom(PRODUCTION_ROOT / "bom" / "pcbway-bom.csv", pcbway_bom_rows(rows))
    write_manifest(
        PRODUCTION_ROOT / "pcbway-manifest.json",
        blocked_manifest(rows, [reason]),
    )


def main() -> int:
    rows = load_bom()
    write_pcbway_bom(PRODUCTION_ROOT / "bom" / "pcbway-bom.csv", pcbway_bom_rows(rows))
    try:
        validate_board_ready_for_export(KICAD_BOARD)
    except ValueError as exc:
        write_manifest(PRODUCTION_ROOT / "pcbway-manifest.json", blocked_manifest(rows, [str(exc)]))
        print(str(exc), file=sys.stderr)
        return 1

    write_manifest(PRODUCTION_ROOT / "pcbway-manifest.json", release_manifest(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
