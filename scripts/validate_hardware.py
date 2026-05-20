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

REQUIRED_RASPBERRY_QR_INTERFACES = {
    "camera",
    "display",
    "physical_buttons",
    "response_qr_display",
    "wireless_disable_capable",
    "removable_boot_media",
}

REQUIRED_CUSTOM_WALLET_INTERFACES = REQUIRED_INTERFACES | {
    "usb_c_bus_powered",
    "wireless_disable_capable",
    "tropic01_spi",
    "tropic01_gpo_irq",
    "tropic01_power_cycle_control",
    "tropic01_pairing_lifecycle",
}

VALID_DEVICE_CLASSES = {
    "esp32_s3_qr_signer",
    "esp32_s3_usb_signer",
    "custom_persistent_secret_wallet",
    "raspberry_qr_vault",
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

REQUIRED_CUSTOM_WALLET_BOM_CATEGORIES = REQUIRED_BOM_CATEGORIES | {
    "protection",
    "secure_element",
}

REQUIRED_CUSTOM_WALLET_LIFECYCLE_FIELDS = {
    "secret_at_rest",
    "unlock_location",
    "plaintext_persistence",
    "wipe_events",
    "pin_attempt_policy",
    "backup_export_policy",
}

REQUIRED_CUSTOM_WALLET_WIPE_EVENTS = {
    "manual_lock",
    "power_loss",
    "pin_attempt_exhausted",
    "session_timeout",
    "firmware_error",
    "debug_policy_violation",
}

FORBIDDEN_TROPIC01_RESET_INTERFACE_TERMS = {
    "reset",
}

REQUIRED_REVIEW_KEYWORDS = {
    "request id",
    "approval_digest",
}

REQUIRED_QR_KEYWORDS = {
    "nsealr1",
    "physical approval",
    "trusted review",
}

REQUIRED_IDENTITY_POLICY_KEYWORDS_BY_CLASS = {
    "esp32_s3_usb_signer": (
        "nsealr-account-descriptor-v0",
        "esp32_usb_nip46",
        "policy-manual-only-persistent-device",
        "policy-scoped-automation-daily-use",
        "grant-esp32-usb-kind-1-session",
    ),
    "esp32_s3_qr_signer": (
        "nsealr-account-descriptor-v0",
        "esp32_qr_vault",
        "policy-manual-only-qr-vault",
        "persistent_grants: false",
    ),
    "raspberry_qr_vault": (
        "nsealr-account-descriptor-v0",
        "raspberry_qr_vault",
        "policy-manual-only-qr-vault",
        "persistent_grants: false",
    ),
    "custom_persistent_secret_wallet": (
        "nsealr-account-descriptor-v0",
        "custom_hardware_wallet",
        "custom_hardware_persistent",
        "policy-manual-only-persistent-device",
        "custom-hardware-wallet-enable-kind-1-automation",
        "policy-scoped-automation-daily-use",
        "grant-custom-hardware-wallet-kind-1-session",
    ),
}

STATELESS_QR_DEVICE_CLASSES = {
    "esp32_s3_qr_signer",
    "raspberry_qr_vault",
}

VALID_MANUAL_REPORT_TYPES = {
    "board_detection",
    "firmware_build",
    "os_profile_smoke",
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

REQUIRED_RASPBERRY_OS_DISABLED_SERVICES = {
    "ssh",
    "bluetooth",
    "wifi_client",
    "wifi_access_point",
}

REQUIRED_RASPBERRY_OS_EVIDENCE_KEYWORDS = {
    "wireless": ("wi-fi", "wifi", "bluetooth", "wireless"),
    "swap": ("swap",),
    "remote_access": ("ssh", "remote"),
    "persistent_secret_storage": ("persistent signing secret", "persistent secret"),
    "seed_entry": ("seed entry", "session-secret input", "session secret input"),
    "power_cycle": ("power-cycle", "power cycle"),
}

REQUIRED_RASPBERRY_OS_REPORT_KEYWORDS = {
    "boot_media": ("microsd", "boot media", "removable"),
    "wireless": ("wi-fi", "wifi", "bluetooth", "wireless"),
    "swap": ("swap",),
    "remote_access": ("ssh", "remote"),
    "ram_only": ("ram-only", "ram only"),
    "persistent_secret_storage": ("persistent signing secret", "persistent secret"),
    "seed_entry": ("seed entry", "session-secret input", "session secret input"),
    "power_cycle": ("power-cycle", "power cycle"),
}

REQUIRED_RASPBERRY_QR_FLOW_REPORT_KEYWORDS = {
    "board": ("pi zero",),
    "camera_scan": ("camera", "nsealr1", "qr"),
    "trusted_display_review": ("display", "review"),
    "physical_controls": ("gpio", "button", "approve", "reject", "next", "scroll"),
    "response_qr": ("response qr", "signed-event qr"),
    "companion_verification": ("companion", "verify-response"),
    "approval_binding": ("request id", "approval_digest"),
    "ram_only": ("ram-only",),
    "no_usb_data_transport": ("no usb data",),
}

REQUIRED_RASPBERRY_SEEDSIGNER_PROFILE_FIELDS = {
    "supported_board_targets",
    "display_targets",
    "camera_targets",
    "control_targets",
    "os_targets",
    "acceptance_targets",
}

REQUIRED_RASPBERRY_SEEDSIGNER_PROFILE_KEYWORDS = {
    "primary_physical_target": ("pi zero",),
    "supported_board_targets": ("pi zero",),
    "display_targets": ("waveshare", "st7789", "240x240"),
    "camera_targets": ("ov5647", "camera"),
    "control_targets": ("gpio", "button"),
    "os_targets": ("seedsigner", "buildroot"),
    "acceptance_targets": ("pi zero", "qr", "review"),
}

REQUIRED_RASPBERRY_GPIO_ACTIONS = {
    "next",
    "scroll",
    "approve",
    "reject",
}

REQUIRED_ESP32_QR_SECONDARY_TARGET = {
    "sku": "ESP32-S3-Touch-LCD-3.5B-C",
    "display_driver": "AXS15231B",
    "display_bus": "QSPI",
    "camera_module": "OV5640",
}


def validate_requirements(path: Path) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("schema_version") != 1:
        raise ValueError(f"{path}: schema_version must be 1")
    device_class = value.get("device_class")
    if device_class not in VALID_DEVICE_CLASSES:
        raise ValueError(f"{path}: device_class must be one of {', '.join(sorted(VALID_DEVICE_CLASSES))}")
    mandatory = set(value.get("mandatory_interfaces", []))
    if device_class == "esp32_s3_qr_signer":
        required_interfaces = REQUIRED_QR_INTERFACES
    elif device_class == "raspberry_qr_vault":
        required_interfaces = REQUIRED_RASPBERRY_QR_INTERFACES
    elif device_class == "custom_persistent_secret_wallet":
        required_interfaces = REQUIRED_CUSTOM_WALLET_INTERFACES
    else:
        required_interfaces = REQUIRED_INTERFACES
    missing = sorted(required_interfaces - mandatory)
    if missing:
        raise ValueError(f"{path}: missing mandatory interfaces: {', '.join(missing)}")
    if device_class == "esp32_s3_qr_signer":
        validate_esp32_qr_secondary_target(value, path)
    optional = set(value.get("optional_interfaces", []))
    if device_class in STATELESS_QR_DEVICE_CLASSES:
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
    validate_identity_policy_requirements(value, path, device_class)
    if device_class in STATELESS_QR_DEVICE_CLASSES:
        security_text = "\n".join(value["security_requirements"])
        if "Wireless must be disabled" not in security_text:
            raise ValueError(f"{path}: security_requirements must mention Wireless must be disabled")
        review_text_original = "\n".join(value["review_requirements"])
        if "Touch must not be accepted as approve/reject consent" not in review_text_original:
            raise ValueError(
                f"{path}: review_requirements must mention Touch must not be accepted as approve/reject consent"
            )
        qr_items = value.get("qr_requirements")
        if not isinstance(qr_items, list) or not qr_items:
            raise ValueError(f"{path}: qr_requirements must be a non-empty list")
        if not all(isinstance(item, str) and item for item in qr_items):
            raise ValueError(f"{path}: qr_requirements must contain non-empty strings")
        qr_text = "\n".join(qr_items).lower()
        missing_qr_keywords = sorted(keyword for keyword in REQUIRED_QR_KEYWORDS if keyword not in qr_text)
        if missing_qr_keywords:
            raise ValueError(f"{path}: qr_requirements must mention {', '.join(missing_qr_keywords)}")
    if device_class == "raspberry_qr_vault":
        validate_seed_signer_compatibility_profile(value, path)
    if device_class == "custom_persistent_secret_wallet":
        validate_custom_persistent_secret_wallet(value, path, mandatory, optional)


def validate_esp32_qr_secondary_target(value: dict, path: Path) -> None:
    target = value.get("secondary_devkit_candidate")
    if not isinstance(target, dict):
        raise ValueError(f"{path}: secondary_devkit_candidate must be an object")
    for field, expected in REQUIRED_ESP32_QR_SECONDARY_TARGET.items():
        if target.get(field) != expected:
            raise ValueError(f"{path}: secondary_devkit_candidate.{field} must be {expected}")


def validate_identity_policy_requirements(value: dict, path: Path, device_class: str) -> None:
    items = value.get("identity_policy_requirements")
    if not isinstance(items, list) or not items:
        raise ValueError(f"{path}: identity_policy_requirements must be a non-empty list")
    if not all(isinstance(item, str) and item for item in items):
        raise ValueError(f"{path}: identity_policy_requirements must contain non-empty strings")

    text = "\n".join(items).lower()
    for keyword in REQUIRED_IDENTITY_POLICY_KEYWORDS_BY_CLASS[device_class]:
        if keyword not in text:
            raise ValueError(f"{path}: identity_policy_requirements must mention {keyword}")
    if device_class in STATELESS_QR_DEVICE_CLASSES and "persistent_grants: true" in text:
        raise ValueError(f"{path}: stateless QR vault identity_policy_requirements must require persistent_grants: false")


def validate_seed_signer_compatibility_profile(value: dict, path: Path) -> None:
    profile = value.get("seed_signer_compatibility")
    if not isinstance(profile, dict) or not profile:
        raise ValueError(f"{path}: seed_signer_compatibility must be a non-empty object")
    _require_non_empty_string(profile.get("primary_physical_target"), path, "seed_signer_compatibility.primary_physical_target")
    for field in sorted(REQUIRED_RASPBERRY_SEEDSIGNER_PROFILE_FIELDS):
        _require_non_empty_string_list(profile.get(field), path, f"seed_signer_compatibility.{field}")

    profile_text_by_field = {
        "primary_physical_target": str(profile.get("primary_physical_target", "")).lower(),
        **{field: _list_text(profile.get(field)) for field in REQUIRED_RASPBERRY_SEEDSIGNER_PROFILE_FIELDS},
    }
    for field, keywords in REQUIRED_RASPBERRY_SEEDSIGNER_PROFILE_KEYWORDS.items():
        field_text = profile_text_by_field[field]
        missing_keywords = sorted(keyword for keyword in keywords if keyword not in field_text)
        if missing_keywords:
            raise ValueError(
                f"{path}: seed_signer_compatibility.{field} must mention {', '.join(missing_keywords)}"
            )
    validate_seed_signer_gpio_button_profile(profile, path)


def validate_seed_signer_gpio_button_profile(profile: dict, path: Path) -> None:
    button_profile = profile.get("gpio_button_profile")
    if not isinstance(button_profile, dict) or not button_profile:
        raise ValueError(f"{path}: seed_signer_compatibility.gpio_button_profile must be a non-empty object")
    if button_profile.get("numbering") != "BOARD":
        raise ValueError(f"{path}: seed_signer_compatibility.gpio_button_profile.numbering must be BOARD")
    actions = button_profile.get("actions")
    if not isinstance(actions, dict):
        raise ValueError(f"{path}: seed_signer_compatibility.gpio_button_profile.actions must be an object")
    for action in sorted(REQUIRED_RASPBERRY_GPIO_ACTIONS):
        pins = actions.get(action)
        field = f"seed_signer_compatibility.gpio_button_profile.actions.{action}"
        if not isinstance(pins, list) or not pins:
            raise ValueError(f"{path}: {field} must be a non-empty list")
        if not all(isinstance(pin, int) and pin > 0 for pin in pins):
            raise ValueError(f"{path}: {field} must contain positive integer BOARD pins")
    approve_pins = set(actions["approve"])
    reject_pins = set(actions["reject"])
    if approve_pins & reject_pins:
        raise ValueError(f"{path}: approve and reject pins must be distinct")
    safety_text = _list_text(button_profile.get("safety", []))
    if "reject" not in safety_text or "precedence" not in safety_text:
        raise ValueError(
            f"{path}: seed_signer_compatibility.gpio_button_profile.safety must document reject precedence"
        )


def validate_custom_persistent_secret_wallet(
    value: dict,
    path: Path,
    mandatory: set[str],
    optional: set[str],
) -> None:
    if value.get("product_mode") != "usb_c_bus_powered_connected_wallet_rev_a":
        raise ValueError(f"{path}: product_mode must be usb_c_bus_powered_connected_wallet_rev_a")

    interface_text = " ".join(sorted(mandatory | optional)).lower()
    if "battery_power" in interface_text:
        raise ValueError(f"{path}: battery_power is not allowed in custom wallet Rev A interfaces")
    forbidden_reset_interfaces = sorted(
        interface
        for interface in mandatory | optional
        if "tropic01" in interface.lower()
        and any(term in interface.lower() for term in FORBIDDEN_TROPIC01_RESET_INTERFACE_TERMS)
        and "power_cycle" not in interface.lower()
    )
    if forbidden_reset_interfaces:
        raise ValueError(
            f"{path}: TROPIC01 reset must be modeled as power-cycle control, not dedicated reset interfaces: "
            + ", ".join(forbidden_reset_interfaces)
        )

    text = "\n".join(
        _flatten_text(value.get(field))
        for field in (
            "security_requirements",
            "review_requirements",
            "identity_policy_requirements",
            "notes",
        )
    ).lower()
    if "air-gapped" in text or "airgapped" in text:
        raise ValueError(f"{path}: USB connected custom wallet Rev A must not claim air-gapped operation")

    for phrase in (
        "currently performs bip-340",
        "currently supports bip-340",
        "available bip-340",
        "public api supports bip-340",
        "tropic01 performs bip-340 signing",
        "tropic01 signs bip-340",
    ):
        if phrase in text:
            raise ValueError(f"{path}: BIP-340 signing inside TROPIC01 must remain a future-gated claim")

    required_security_terms = {
        "tropic01",
        "pairing key",
        "mac-and-destroy",
        "key wrapping",
        "bip-340",
    }
    missing_terms = sorted(term for term in required_security_terms if term not in text)
    if missing_terms:
        raise ValueError(f"{path}: custom wallet security_requirements must mention {', '.join(missing_terms)}")

    roadmap = value.get("tropic01_schnorr_roadmap")
    if not isinstance(roadmap, dict):
        raise ValueError(f"{path}: tropic01_schnorr_roadmap must be an object")
    expected = {
        "current_public_api": "not_supported",
        "future_vendor_roadmap": "planned",
        "rev_a_signing_engine": "esp32_s3_host_mcu",
    }
    for field, expected_value in expected.items():
        if roadmap.get(field) != expected_value:
            raise ValueError(f"{path}: tropic01_schnorr_roadmap.{field} must be {expected_value}")
    product_gate = str(roadmap.get("product_gate", "")).lower()
    if "public api" not in product_gate or "vendor" not in product_gate:
        raise ValueError(f"{path}: tropic01_schnorr_roadmap.product_gate must mention public API and vendor")
    validate_custom_wallet_key_material_lifecycle(value, path)


def validate_custom_wallet_key_material_lifecycle(value: dict, path: Path) -> None:
    lifecycle = value.get("key_material_lifecycle")
    if not isinstance(lifecycle, dict):
        raise ValueError(f"{path}: key_material_lifecycle must be an object")
    missing_fields = sorted(REQUIRED_CUSTOM_WALLET_LIFECYCLE_FIELDS - set(lifecycle))
    if missing_fields:
        raise ValueError(f"{path}: key_material_lifecycle missing {', '.join(missing_fields)}")

    for field in sorted(REQUIRED_CUSTOM_WALLET_LIFECYCLE_FIELDS - {"wipe_events"}):
        _require_non_empty_string(lifecycle.get(field), path, f"key_material_lifecycle.{field}")

    secret_at_rest = str(lifecycle["secret_at_rest"]).lower()
    if "plaintext" not in secret_at_rest or "no plaintext" not in secret_at_rest:
        raise ValueError(f"{path}: key_material_lifecycle.secret_at_rest must forbid plaintext secrets at rest")
    if "wrapped" not in secret_at_rest and "encrypted" not in secret_at_rest:
        raise ValueError(f"{path}: key_material_lifecycle.secret_at_rest must require wrapped or encrypted storage")

    unlock_location = str(lifecycle["unlock_location"]).lower()
    if "esp32" not in unlock_location or "ram" not in unlock_location or "tropic01" not in unlock_location:
        raise ValueError(f"{path}: key_material_lifecycle.unlock_location must mention ESP32 RAM and TROPIC01")

    plaintext_persistence = str(lifecycle["plaintext_persistence"]).lower()
    if "ram-only" not in plaintext_persistence and "ram only" not in plaintext_persistence:
        raise ValueError(f"{path}: key_material_lifecycle.plaintext_persistence must require RAM-only plaintext")
    forbidden_outputs = (
        "flash",
        "logs",
        "crash dumps",
        "usb reports",
        "companion descriptors",
        "debug output",
    )
    missing_outputs = sorted(output for output in forbidden_outputs if output not in plaintext_persistence)
    if missing_outputs:
        raise ValueError(
            f"{path}: key_material_lifecycle.plaintext_persistence must forbid {', '.join(missing_outputs)}"
        )

    wipe_events = lifecycle.get("wipe_events")
    if not isinstance(wipe_events, list) or not wipe_events:
        raise ValueError(f"{path}: key_material_lifecycle.wipe_events must be a non-empty list")
    if not all(isinstance(event, str) and event.strip() for event in wipe_events):
        raise ValueError(f"{path}: key_material_lifecycle.wipe_events must contain non-empty strings")
    missing_wipe_events = sorted(REQUIRED_CUSTOM_WALLET_WIPE_EVENTS - set(wipe_events))
    if missing_wipe_events:
        raise ValueError(f"{path}: key_material_lifecycle.wipe_events missing {', '.join(missing_wipe_events)}")

    pin_policy = str(lifecycle["pin_attempt_policy"]).lower()
    if "tropic01" not in pin_policy or "mac-and-destroy" not in pin_policy:
        raise ValueError(f"{path}: key_material_lifecycle.pin_attempt_policy must require TROPIC01 MAC-and-Destroy")

    export_policy = str(lifecycle["backup_export_policy"]).lower()
    if "device review" not in export_policy or "physical approval" not in export_policy:
        raise ValueError(
            f"{path}: key_material_lifecycle.backup_export_policy must require device review and physical approval"
        )
    if "disabled by default" not in export_policy:
        raise ValueError(f"{path}: key_material_lifecycle.backup_export_policy must be disabled by default")
    if "danger-zone" not in export_policy:
        raise ValueError(f"{path}: key_material_lifecycle.backup_export_policy must require danger-zone copy")


def validate_bom(path: Path) -> None:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = set(reader.fieldnames or [])
        missing_headers = sorted(REQUIRED_BOM_HEADERS - headers)
        if missing_headers:
            raise ValueError(f"{path}: missing BOM headers: {', '.join(missing_headers)}")
        designators: set[str] = set()
        categories: set[str] = set()
        rows: list[dict[str, str]] = []
        for row_number, row in enumerate(reader, start=2):
            rows.append({key: value or "" for key, value in row.items()})
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
        required_categories = REQUIRED_BOM_CATEGORIES
        if path.name == "custom-persistent-secret-wallet.csv":
            required_categories = REQUIRED_CUSTOM_WALLET_BOM_CATEGORIES
        missing_categories = sorted(required_categories - categories)
        if missing_categories:
            raise ValueError(f"{path}: missing required BOM categories: {', '.join(missing_categories)}")
        if path.name == "custom-persistent-secret-wallet.csv":
            validate_custom_wallet_bom_rows(path, rows)


def validate_custom_wallet_bom_rows(path: Path, rows: list[dict[str, str]]) -> None:
    row_text = [
        " ".join(
            (
                row.get("category", ""),
                row.get("description", ""),
                row.get("notes", ""),
            )
        ).lower()
        for row in rows
    ]
    if any("tropic01" in text and "reset pin" in text for text in row_text):
        raise ValueError(f"{path}: TROPIC01 reset must use controlled power cycling, not a reset pin component")
    has_power_cycle_component = any(
        "tropic01" in text
        and (
            "load switch" in text
            or "power-gating" in text
            or "power-cycle" in text
            or "power cycle" in text
        )
        for text in row_text
    )
    if not has_power_cycle_component:
        raise ValueError(f"{path}: custom wallet BOM must include a TROPIC01 power-cycle/load-switch component")


def _flatten_text(value: object) -> str:
    if isinstance(value, list):
        return " ".join(_flatten_text(item) for item in value)
    if isinstance(value, dict):
        return " ".join(_flatten_text(item) for item in value.values())
    return str(value)


def _list_text(value: object) -> str:
    if not isinstance(value, list):
        return ""
    return " ".join(str(item).lower() for item in value)


def validate_raspberry_os_profile(path: Path) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("schema_version") != 1:
        raise ValueError(f"{path}: schema_version must be 1")
    if value.get("profile_type") != "raspberry_qr_vault_os_profile":
        raise ValueError(f"{path}: profile_type must be raspberry_qr_vault_os_profile")
    if value.get("device_class") != "raspberry_qr_vault":
        raise ValueError(f"{path}: device_class must be raspberry_qr_vault")
    if value.get("boot_media") != "removable_microSD":
        raise ValueError(f"{path}: boot_media must be removable_microSD")
    if value.get("network_policy") != "wireless_disabled_or_absent":
        raise ValueError(f"{path}: network_policy must be wireless_disabled_or_absent")
    if value.get("session_secret_policy") != "ram_only":
        raise ValueError(f"{path}: session_secret_policy must be ram_only")
    if value.get("session_secret_input_policy") != "no_seed_files_or_secret_cli_args":
        raise ValueError(f"{path}: session_secret_input_policy must be no_seed_files_or_secret_cli_args")
    if value.get("persistent_secret_storage_allowed") is not False:
        raise ValueError(f"{path}: persistent_secret_storage_allowed must be false")
    if value.get("swap_enabled_during_signing") is not False:
        raise ValueError(f"{path}: swap_enabled_during_signing must be false")
    if value.get("remote_access_enabled_during_signing") is not False:
        raise ValueError(f"{path}: remote_access_enabled_during_signing must be false")
    _require_non_empty_string_list(
        value.get("setup_interfaces_removed_before_signing"),
        path,
        "setup_interfaces_removed_before_signing",
    )
    _require_non_empty_string_list(value.get("required_disabled_services"), path, "required_disabled_services")
    disabled_services = set(value["required_disabled_services"])
    missing_services = sorted(REQUIRED_RASPBERRY_OS_DISABLED_SERVICES - disabled_services)
    if missing_services:
        raise ValueError(f"{path}: required_disabled_services missing {', '.join(missing_services)}")
    _require_non_empty_string_list(value.get("acceptance_evidence"), path, "acceptance_evidence")
    evidence_text = _list_text(value["acceptance_evidence"])
    for label, keywords in REQUIRED_RASPBERRY_OS_EVIDENCE_KEYWORDS.items():
        if not any(keyword in evidence_text for keyword in keywords):
            raise ValueError(f"{path}: acceptance_evidence must mention {label}")
    _require_non_empty_string_list(value.get("notes"), path, "notes")
    notes_text = _list_text(value["notes"])
    if "tropic01" in notes_text:
        if "not this stateless qr vault" not in notes_text:
            raise ValueError(f"{path}: TROPIC01 mention must exclude the stateless QR vault")
    if "persistent-secret" in notes_text and "custom persistent-secret hardware-wallet" not in notes_text:
        raise ValueError(f"{path}: persistent-secret mention must stay under custom hardware-wallet framing")


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


def _manual_report_search_text(value: dict) -> str:
    fields = [
        json.dumps(value.get("hardware", {}), sort_keys=True),
        " ".join(str(item) for item in value.get("procedure", [])),
        str(value.get("observed_result", "")),
        " ".join(str(item) for item in value.get("limitations", [])),
    ]
    return " ".join(fields).lower()


def _mentions_signing_disabled(value: dict) -> bool:
    text = _report_text(value)
    return "signing_disabled" in text or "signing disabled" in text


def _discover_validation_files() -> dict[str, list[Path]]:
    return {
        "requirements": sorted(
            [
                *ROOT.glob("kits/*/requirements.json"),
                *ROOT.glob("pcb/*/requirements.json"),
            ]
        ),
        "raspberry_os_profiles": sorted(ROOT.glob("kits/*/os-profile.json")),
        "boms": sorted((ROOT / "bom").glob("*.csv")),
        "manual_reports": sorted(
            [
                *(ROOT / "reports").glob("*.json"),
                *(ROOT / "templates").glob("*.json"),
            ]
        ),
    }


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
    if value["target_family"] == "raspberry_stateless_qr_vault" and value["report_type"] == "os_profile_smoke":
        report_text = _manual_report_search_text(value)
        for label, keywords in REQUIRED_RASPBERRY_OS_REPORT_KEYWORDS.items():
            if not any(keyword in report_text for keyword in keywords):
                raise ValueError(f"{path}: Raspberry OS profile reports must mention {label}")
    if value["target_family"] == "raspberry_stateless_qr_vault" and value["report_type"] == "qr_flow_smoke":
        report_text = _manual_report_search_text(value)
        for label, keywords in REQUIRED_RASPBERRY_QR_FLOW_REPORT_KEYWORDS.items():
            missing_keywords = sorted(keyword for keyword in keywords if keyword not in report_text)
            if missing_keywords:
                raise ValueError(
                    f"{path}: Raspberry QR flow reports must mention {label}: {', '.join(missing_keywords)}"
                )
    if (
        value["report_type"] == "protocol_smoke"
        and value["target_family"] == "esp32_usb_nip46_signer"
        and not _mentions_signing_disabled(value)
    ):
        raise ValueError(f"{path}: ESP32 USB protocol_smoke reports must mention signing_disabled evidence")


def main() -> int:
    validation_files = _discover_validation_files()
    for requirements_path in validation_files["requirements"]:
        validate_requirements(requirements_path)
    for profile_path in validation_files["raspberry_os_profiles"]:
        validate_raspberry_os_profile(profile_path)
    for bom_path in validation_files["boms"]:
        validate_bom(bom_path)
    for report_path in validation_files["manual_reports"]:
        validate_manual_report(report_path)
    print("nSealr hardware validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
