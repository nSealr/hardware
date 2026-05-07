#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_INTERFACES = {
    "usb_c_native",
    "display",
    "physical_buttons",
    "secure_boot_capable",
    "flash_encryption_capable",
    "debug_lock_capable",
}

REQUIRED_BOM_HEADERS = {
    "designator",
    "category",
    "description",
    "required",
    "notes",
}

REQUIRED_BOM_CATEGORIES = {
    "mcu",
    "usb",
    "power",
    "display",
    "input",
    "programming",
}

REQUIRED_REVIEW_KEYWORDS = {
    "request id",
    "approval_digest",
}


def validate_requirements(path: Path) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("schema_version") != 1:
        raise ValueError(f"{path}: schema_version must be 1")
    if value.get("device_class") != "esp32_s3_usb_signer":
        raise ValueError(f"{path}: device_class must be esp32_s3_usb_signer")
    mandatory = set(value.get("mandatory_interfaces", []))
    missing = sorted(REQUIRED_INTERFACES - mandatory)
    if missing:
        raise ValueError(f"{path}: missing mandatory interfaces: {', '.join(missing)}")
    for field in ("security_requirements", "review_requirements"):
        items = value.get(field)
        if not isinstance(items, list) or not items:
            raise ValueError(f"{path}: {field} must be a non-empty list")
        if not all(isinstance(item, str) and item for item in items):
            raise ValueError(f"{path}: {field} must contain non-empty strings")
    review_text = "\n".join(value["review_requirements"]).lower()
    missing_review_keywords = sorted(keyword for keyword in REQUIRED_REVIEW_KEYWORDS if keyword not in review_text)
    if missing_review_keywords:
        raise ValueError(f"{path}: review_requirements must mention {', '.join(missing_review_keywords)}")


def validate_bom(path: Path) -> None:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = set(reader.fieldnames or [])
        missing_headers = sorted(REQUIRED_BOM_HEADERS - headers)
        if missing_headers:
            raise ValueError(f"{path}: missing BOM headers: {', '.join(missing_headers)}")
        designators: set[str] = set()
        categories: set[str] = set()
        for row_number, row in enumerate(reader, start=2):
            designator = (row.get("designator") or "").strip()
            category = (row.get("category") or "").strip()
            required = (row.get("required") or "").strip().lower()
            description = (row.get("description") or "").strip()
            if not designator:
                raise ValueError(f"{path}:{row_number}: designator is required")
            if designator in designators:
                raise ValueError(f"{path}:{row_number}: duplicate designator {designator}")
            if required not in {"true", "false"}:
                raise ValueError(f"{path}:{row_number}: required must be true or false")
            if not category or not description:
                raise ValueError(f"{path}:{row_number}: category and description are required")
            designators.add(designator)
            if required == "true":
                categories.add(category)
        missing_categories = sorted(REQUIRED_BOM_CATEGORIES - categories)
        if missing_categories:
            raise ValueError(f"{path}: missing required BOM categories: {', '.join(missing_categories)}")


def main() -> int:
    validate_requirements(ROOT / "pcb/reference-esp32-s3-signer/requirements.json")
    validate_bom(ROOT / "bom/reference-esp32-s3-signer.csv")
    print("NostrSeal hardware validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
