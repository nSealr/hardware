#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from datetime import date
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

REQUIRED_QR_INTERFACES = REQUIRED_INTERFACES | {
    "camera",
    "battery_power",
    "wireless_disable_capable",
}

VALID_DEVICE_CLASSES = {
    "esp32_s3_qr_signer",
    "esp32_s3_usb_signer",
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

VALID_MANUAL_REPORT_TYPES = {
    "board_detection",
    "firmware_build",
    "protocol_smoke",
    "display_smoke",
    "camera_smoke",
    "qr_flow_smoke",
    "pcsc_card_smoke",
}

VALID_TARGET_FAMILIES = {
    "esp32_usb_nip46_signer",
    "esp32_stateless_qr_vault",
    "raspberry_stateless_qr_vault",
    "smartcard_signer",
    "custom_persistent_secret_wallet",
}

STATELESS_TARGET_FAMILIES = {
    "esp32_stateless_qr_vault",
    "raspberry_stateless_qr_vault",
}

VALID_MANUAL_RESULTS = {
    "pass",
    "fail",
    "blocked",
}

REQUIRED_MANUAL_REPORT_FIELDS = {
    "schema_version",
    "report_type",
    "date",
    "target_family",
    "hardware",
    "source_repo",
    "firmware_commit",
    "procedure",
    "expected_result",
    "observed_result",
    "result",
    "production_signing_enabled",
    "persistent_secret_present",
    "tropic01_used",
    "limitations",
}


def validate_requirements(path: Path) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("schema_version") != 1:
        raise ValueError(f"{path}: schema_version must be 1")
    device_class = value.get("device_class")
    if device_class not in VALID_DEVICE_CLASSES:
        raise ValueError(f"{path}: device_class must be one of {', '.join(sorted(VALID_DEVICE_CLASSES))}")
    mandatory = set(value.get("mandatory_interfaces", []))
    required_interfaces = REQUIRED_QR_INTERFACES if device_class == "esp32_s3_qr_signer" else REQUIRED_INTERFACES
    missing = sorted(required_interfaces - mandatory)
    if missing:
        raise ValueError(f"{path}: missing mandatory interfaces: {', '.join(missing)}")
    optional = set(value.get("optional_interfaces", []))
    if device_class == "esp32_s3_qr_signer":
        interface_text = " ".join(sorted(mandatory | optional)).lower()
        if "tropic01" in interface_text:
            raise ValueError(f"{path}: TROPIC01 interfaces are not allowed on stateless QR vault requirements")
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
    if device_class == "esp32_s3_qr_signer":
        security_text = "\n".join(value["security_requirements"])
        if "Wireless must be disabled" not in security_text:
            raise ValueError(f"{path}: security_requirements must mention Wireless must be disabled")
        review_text_original = "\n".join(value["review_requirements"])
        if "Touch must not be accepted as approve/reject consent" not in review_text_original:
            raise ValueError(
                f"{path}: review_requirements must mention Touch must not be accepted as approve/reject consent"
            )


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


def _require_non_empty_string(value: object, path: Path, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{path}: {field} must be a non-empty string")


def _require_non_empty_string_list(value: object, path: Path, field: str) -> None:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{path}: {field} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise ValueError(f"{path}: {field} must contain non-empty strings")


def _report_text(value: dict) -> str:
    fields = [
        str(value.get("expected_result", "")),
        str(value.get("observed_result", "")),
        " ".join(str(item) for item in value.get("limitations", [])),
    ]
    return " ".join(fields).lower()


def _mentions_signing_disabled(value: dict) -> bool:
    text = _report_text(value)
    return "signing_disabled" in text or "signing disabled" in text


def validate_manual_report(path: Path) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    missing = sorted(REQUIRED_MANUAL_REPORT_FIELDS - set(value))
    if missing:
        raise ValueError(f"{path}: missing manual report fields: {', '.join(missing)}")
    if value.get("schema_version") != 1:
        raise ValueError(f"{path}: schema_version must be 1")
    if value.get("report_type") not in VALID_MANUAL_REPORT_TYPES:
        raise ValueError(f"{path}: report_type must be one of {', '.join(sorted(VALID_MANUAL_REPORT_TYPES))}")
    if value.get("target_family") not in VALID_TARGET_FAMILIES:
        raise ValueError(f"{path}: target_family must be one of {', '.join(sorted(VALID_TARGET_FAMILIES))}")
    try:
        date.fromisoformat(value["date"])
    except ValueError as error:
        raise ValueError(f"{path}: date must use YYYY-MM-DD") from error
    if not isinstance(value.get("hardware"), dict) or not value["hardware"]:
        raise ValueError(f"{path}: hardware must be a non-empty object")
    for field in ("source_repo", "firmware_commit", "expected_result", "observed_result"):
        _require_non_empty_string(value.get(field), path, field)
    _require_non_empty_string_list(value.get("procedure"), path, "procedure")
    _require_non_empty_string_list(value.get("limitations"), path, "limitations")
    if value.get("result") not in VALID_MANUAL_RESULTS:
        raise ValueError(f"{path}: result must be one of {', '.join(sorted(VALID_MANUAL_RESULTS))}")
    if value.get("production_signing_enabled") is not False:
        raise ValueError(f"{path}: production_signing_enabled must be false for hardware validation reports")
    if not isinstance(value.get("persistent_secret_present"), bool):
        raise ValueError(f"{path}: persistent_secret_present must be boolean")
    if not isinstance(value.get("tropic01_used"), bool):
        raise ValueError(f"{path}: tropic01_used must be boolean")
    if value["target_family"] in STATELESS_TARGET_FAMILIES and value["persistent_secret_present"]:
        raise ValueError(f"{path}: stateless targets must not report persistent secrets")
    if value["target_family"] in STATELESS_TARGET_FAMILIES and value["tropic01_used"]:
        raise ValueError(f"{path}: stateless targets must not report TROPIC01 usage")
    if (
        value["report_type"] == "protocol_smoke"
        and value["target_family"] == "esp32_usb_nip46_signer"
        and not _mentions_signing_disabled(value)
    ):
        raise ValueError(f"{path}: ESP32 USB protocol_smoke reports must mention signing_disabled evidence")


def main() -> int:
    validate_requirements(ROOT / "pcb/reference-esp32-s3-signer/requirements.json")
    validate_requirements(ROOT / "pcb/reference-esp32-s3-qr-signer/requirements.json")
    validate_bom(ROOT / "bom/reference-esp32-s3-signer.csv")
    for report_path in sorted((ROOT / "reports").glob("*.json")):
        validate_manual_report(report_path)
    print("NostrSeal hardware validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
