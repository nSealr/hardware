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

REQUIRED_TROPIC01_UNIVERSAL_INTERFACES = {
    "usb_c_native",
    "usb_c_bus_powered",
    "usb_c_receptacle_only",
    "display",
    "touch_display",
    "physical_buttons",
    "side_physical_buttons",
    "secure_boot_capable",
    "encrypted_storage_capable",
    "debug_lock_capable",
    "tropic01_spi",
    "tropic01_gpo_irq",
    "tropic01_power_cycle_control",
    "tropic01_pairing_lifecycle",
    "external_host_spi_selectable",
    "second_secure_element_i2c",
    "lipo_power_path",
    "lipo_battery_connector",
    "nfc_power_gated",
    "qspi_flash",
    "hidden_pogo_test_pads",
    "no_microsd_slot",
    "expansion_i2c",
    "expansion_uart",
    "expansion_spi",
}

VALID_DEVICE_CLASSES = {
    "esp32_s3_qr_signer",
    "esp32_s3_usb_signer",
    "raspberry_qr_vault",
    "tropic01_universal_secure_device",
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

REQUIRED_TROPIC01_UNIVERSAL_BOM_CATEGORIES = REQUIRED_BOM_CATEGORIES | {
    "expansion",
    "protection",
    "secure_element",
    "storage",
}

REQUIRED_TROPIC01_UNIVERSAL_BOM_FREEZE_HEADERS = {
    "manufacturer",
    "mpn",
    "package",
    "footprint",
    "datasheet",
    "alternate_mpn",
    "freeze_status",
}

VALID_TROPIC01_UNIVERSAL_BOM_FREEZE_STATUSES = {
    "frozen",
    "candidate",
    "proxy_footprint",
    "tuning_required",
    "footprint_only",
}

REQUIRED_TROPIC01_UNIVERSAL_CORE_MPNS = {
    "U1": "STM32U585VIT6",
    "U1_ALT": "STM32U575VIT6",
    "U2": "TR01-C2P-T301",
    "U2_ALT": "TR01-C2P-T310",
    "U3": "TPS62840DLCR",
    "U4": "TPS22917DBVR",
    "U5": "W25Q128JVSIQ",
    "J1": "USB4105-GF-A",
    "DISP1": "NHD-2.4-240320AF-CSXP-CTP",
    "J2": "54132-4062",
    "J2B": "52271-0679",
    "SW1 SW2": "EVQP7J01P",
    "U9": "ST25R3916B-AQET",
    "U10": "BQ24074RGTR",
    "U11": "OPTIGA-TRUST-M-SLS32AIA",
    "J6": "SM04B-SRSS-TB(LF)(SN)",
    "J9": "S2B-PH-SM4-TB(LF)(SN)",
}

REQUIRED_TROPIC01_UNIVERSAL_NETLIST_BUSES = {
    "power",
    "usb2_device",
    "tropic01_spi",
    "display_tft_spi",
    "display_touch_i2c",
    "qspi_nor",
    "nfc_spi",
    "second_secure_element_i2c",
    "side_buttons",
    "expansion",
    "manufacturing_test",
}

REQUIRED_TROPIC01_UNIVERSAL_NETLIST_RELEASE_GATES = {
    "manual_datasheet_pinmux_review",
    "no_llm_invented_pin_numbers",
    "schematic_symbols_have_verified_pin_numbers",
    "kicad_erc_pass",
    "kicad_drc_pass",
    "usb_differential_pair_length_and_impedance_review",
    "nfc_matching_network_measured_with_final_antenna",
    "pcbway_export_unblocked_only_after_routing",
}

REQUIRED_TROPIC01_UNIVERSAL_PINMUX_RELEASE_GATES = {
    "no_llm_invented_pin_numbers",
    "stm32_cube_or_datasheet_pinmux_review",
    "st25r3916b_pin_and_matching_review",
    "kicad_schematic_nets_match_this_ledger",
    "erc_clean_before_pcb_update",
}

REQUIRED_TROPIC01_UNIVERSAL_SCHEMATIC_BINDING_RELEASE_GATES = {
    "no_llm_invented_pin_numbers",
    "all_bound_nets_match_pinmux_ledger",
    "schematic_symbols_have_verified_pin_numbers",
    "layout_review_required_for_rf_usb_display_power",
    "erc_clean_before_pcb_update",
    "pcbway_export_unblocked_only_after_routing",
}

REQUIRED_TROPIC01_UNIVERSAL_SCHEMATIC_COMPONENT_REFS = {
    "U1",
    "U2",
    "J1",
    "J2",
    "J2B",
    "U5",
    "U9",
    "U11",
    "SW1",
    "SW2",
}

REQUIRED_TROPIC01_UNIVERSAL_STM32_ASSIGNMENTS = {
    "USB_DM",
    "USB_DP",
    "USB_VBUS_SENSE",
    "TROPIC_SPI_CSN",
    "TROPIC_SPI_SCK",
    "TROPIC_SPI_MISO",
    "TROPIC_SPI_MOSI",
    "TROPIC_GPO",
    "TROPIC_PWR_EN",
    "TFT_SPI_SCK",
    "TFT_SPI_MOSI",
    "TFT_CS",
    "TFT_DC",
    "TFT_RST",
    "TFT_BACKLIGHT_PWM",
    "TFT_PWR_EN",
    "TOUCH_I2C_SCL",
    "TOUCH_I2C_SDA",
    "TOUCH_INT",
    "TOUCH_RST",
    "SE2_I2C_SCL",
    "SE2_I2C_SDA",
    "SE2_RST",
    "NFC_SPI_CSN",
    "NFC_SPI_SCK",
    "NFC_SPI_MISO",
    "NFC_SPI_MOSI",
    "NFC_IRQ",
    "NFC_PWR_EN",
    "QSPI_CLK",
    "QSPI_NCS",
    "QSPI_IO0",
    "QSPI_IO1",
    "QSPI_IO2",
    "QSPI_IO3",
    "BTN_LEFT",
    "BTN_RIGHT",
    "EXP_UART_TX",
    "EXP_UART_RX",
    "SWDIO",
    "SWCLK",
    "BOOT0",
    "NRST",
}

REQUIRED_TROPIC01_UNIVERSAL_PINMUX_ASSIGNMENT_FIELDS = {
    "pin_name",
    "physical_pin",
    "function",
    "bus",
    "source",
    "source_table",
    "evidence",
    "review_status",
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
    "tropic01_universal_secure_device": (
        "hardware reference platform",
        "nsealr-account-descriptor-v0",
        "custom_hardware_wallet",
        "custom_hardware_persistent",
        "policy-manual-only-persistent-device",
        "fido2",
        "pkcs#11",
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
    elif device_class == "tropic01_universal_secure_device":
        required_interfaces = REQUIRED_TROPIC01_UNIVERSAL_INTERFACES
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
    if device_class == "tropic01_universal_secure_device":
        validate_tropic01_universal_secure_device(value, path, mandatory, optional)


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


def validate_tropic01_universal_secure_device(
    value: dict,
    path: Path,
    mandatory: set[str],
    optional: set[str],
) -> None:
    if value.get("product_mode") != "usb_c_connected_tropic01_universal_reference_rev_a":
        raise ValueError(f"{path}: product_mode must be usb_c_connected_tropic01_universal_reference_rev_a")

    interface_text = " ".join(sorted(mandatory | optional)).lower()
    if "tropic01_reset" in interface_text or "tropic01_reset_pin" in interface_text:
        raise ValueError(f"{path}: TROPIC01 reset must be modeled as power-cycle control, not a reset pin")
    for forbidden in ("radio", "wifi", "ble"):
        if any(forbidden in interface.lower().replace("-", "_").split("_") for interface in mandatory):
            raise ValueError(f"{path}: {forbidden} must not be mandatory on the universal product")
    if any("microsd" in interface.lower() and interface != "no_microsd_slot" for interface in mandatory | optional):
        raise ValueError(f"{path}: microSD is excluded from the single universal product")

    flattened = "\n".join(
        _flatten_text(value.get(field))
        for field in (
            "design_intent",
            "host_controller_decision",
            "mechanical_decision",
            "display_decision",
            "rev_a0_component_decisions",
            "board_profiles",
            "security_requirements",
            "review_requirements",
            "identity_policy_requirements",
            "layout_requirements",
            "component_selection_requirements",
            "notes",
        )
    ).lower()
    if "air-gapped" in flattened or "airgapped" in flattened:
        raise ValueError(f"{path}: USB connected universal Rev A must not claim air-gapped operation")

    required_terms = {
        "stm32u5",
        "stm32u585vit6",
        "stm32u575vit6",
        "lqfp100",
        "tropic01",
        "tr01-c2p-t301",
        "tr01-c2p-t310",
        "portrait",
        "smartphone-like",
        "touch",
        "side buttons",
        "usb-c receptacle",
        "usb-c plug",
        "deferred",
        "display",
        "physical",
        "power-cycle",
        "external-host",
        "nfc",
        "battery",
        "lipo",
        "power-path",
        "second secure element",
        "optiga",
        "pogo",
        "no microsd",
        "do not include microsd",
        "secure boot",
        "debug lock",
        "pairing",
        "maintenance mode",
        "laser fault injection",
        "3.3 v",
        "polling",
        "mac-and-destroy",
    }
    missing_terms = sorted(term for term in required_terms if term not in flattened)
    if missing_terms:
        raise ValueError(f"{path}: universal TROPIC01 requirements must mention {', '.join(missing_terms)}")

    host_decision = value.get("host_controller_decision")
    if not isinstance(host_decision, dict):
        raise ValueError(f"{path}: host_controller_decision must be an object")
    if "stm32u5" not in _flatten_text(host_decision).lower():
        raise ValueError(f"{path}: host_controller_decision must select STM32U5")

    component_decisions = value.get("rev_a0_component_decisions")
    if not isinstance(component_decisions, dict) or not component_decisions:
        raise ValueError(f"{path}: rev_a0_component_decisions must be a non-empty object")
    component_text = _flatten_text(component_decisions).lower()
    for term in (
        "tr01-c2p-t301",
        "tr01-c2p-t310",
        "libtropic 4.0.0",
        "stm32u585vit6",
        "stm32u575vit6",
        "w25q128jv",
        "optiga",
        "no microsd",
    ):
        if term not in component_text:
            raise ValueError(f"{path}: rev_a0_component_decisions must mention {term}")

    profiles = value.get("board_profiles")
    if not isinstance(profiles, list) or not profiles:
        raise ValueError(f"{path}: board_profiles must be a non-empty list")
    profile_text = _flatten_text(profiles).lower()
    for required in ("nfc", "lipo", "battery", "touch", "side buttons", "usb-c receptacle", "optiga", "pogo"):
        if required not in profile_text:
            raise ValueError(f"{path}: board_profiles must mention {required}")
    if "microsd" in profile_text and "do not include microsd" not in flattened:
        raise ValueError(f"{path}: board_profiles must not include microSD")


def validate_bom(path: Path) -> None:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = set(reader.fieldnames or [])
        missing_headers = sorted(REQUIRED_BOM_HEADERS - headers)
        if missing_headers:
            raise ValueError(f"{path}: missing BOM headers: {', '.join(missing_headers)}")
        if path.name == "tropic01-universal-secure-device.csv":
            missing_freeze_headers = sorted(REQUIRED_TROPIC01_UNIVERSAL_BOM_FREEZE_HEADERS - headers)
            if missing_freeze_headers:
                raise ValueError(f"{path}: missing BOM freeze headers: {', '.join(missing_freeze_headers)}")
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
            if path.name == "tropic01-universal-secure-device.csv":
                _validate_tropic01_universal_bom_freeze_fields(path, row, row_number)
            designators.add(designator)
            if required == "true":
                categories.add(category)
        required_categories = REQUIRED_BOM_CATEGORIES
        if path.name == "tropic01-universal-secure-device.csv":
            required_categories = REQUIRED_TROPIC01_UNIVERSAL_BOM_CATEGORIES
        missing_categories = sorted(required_categories - categories)
        if missing_categories:
            raise ValueError(f"{path}: missing required BOM categories: {', '.join(missing_categories)}")
        if path.name == "tropic01-universal-secure-device.csv":
            validate_tropic01_universal_bom_rows(path, rows)


def validate_tropic01_universal_bom_rows(path: Path, rows: list[dict[str, str]]) -> None:
    by_designator = {row.get("designator", ""): row for row in rows}
    for designator, expected_mpn in REQUIRED_TROPIC01_UNIVERSAL_CORE_MPNS.items():
        row = by_designator.get(designator)
        if row is None:
            raise ValueError(f"{path}: universal BOM must include {designator} {expected_mpn}")
        if row.get("mpn", "").strip() != expected_mpn:
            raise ValueError(f"{path}: {designator} must use MPN {expected_mpn}")

    combined_text = "\n".join(" ".join(row.values()).lower() for row in rows)
    for required_text in (
        "stm32u5",
        "tropic01",
        "qspi",
        "display",
        "physical",
        "usb-c",
        "female",
        "receptacle",
        "nfc",
        "lipo",
        "battery",
        "power-path",
        "optiga",
        "second secure element",
        "pogo",
        "side",
    ):
        if required_text not in combined_text:
            raise ValueError(f"{path}: universal BOM must mention {required_text}")
    if "microsd" in combined_text:
        raise ValueError(f"{path}: universal BOM must not include microSD rows")
    if "reset pin" in combined_text and "tropic01" in combined_text:
        raise ValueError(f"{path}: TROPIC01 reset must use controlled power cycling, not a reset pin component")

    has_usb_c_receptacle = any(
        row.get("required", "").strip().lower() == "true"
        and "usb-c" in " ".join(row.values()).lower()
        and "receptacle" in " ".join(row.values()).lower()
        and "female" in " ".join(row.values()).lower()
        and "plug" not in row.get("description", "").lower()
        for row in rows
    )
    if not has_usb_c_receptacle:
        raise ValueError(f"{path}: universal BOM must use a required female USB-C receptacle")

    for required_surface in ("nfc", "lipo", "battery", "optiga"):
        if not any(
            required_surface in " ".join(row.values()).lower()
            and row.get("required", "").strip().lower() == "true"
            for row in rows
        ):
            raise ValueError(f"{path}: {required_surface} must be required in the universal BOM")


def _validate_tropic01_universal_bom_freeze_fields(path: Path, row: dict[str, str], row_number: int) -> None:
    required = row.get("required", "").strip().lower()
    designator = row.get("designator", "").strip()
    freeze_status = row.get("freeze_status", "").strip()
    if freeze_status not in VALID_TROPIC01_UNIVERSAL_BOM_FREEZE_STATUSES:
        raise ValueError(
            f"{path}:{row_number}: freeze_status must be one of "
            + ", ".join(sorted(VALID_TROPIC01_UNIVERSAL_BOM_FREEZE_STATUSES))
        )
    if required != "true":
        return
    missing_fields = [
        field
        for field in ("manufacturer", "mpn", "package", "footprint", "datasheet", "freeze_status")
        if not row.get(field, "").strip()
    ]
    if missing_fields:
        raise ValueError(f"{path}:{row_number}: {designator} missing required BOM freeze fields: {', '.join(missing_fields)}")


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
    if "tropic01" in notes_text and "universal secure device" not in notes_text:
        raise ValueError(f"{path}: TROPIC01 mention must stay under universal secure-device framing")


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
        "netlist_contracts": sorted(ROOT.glob("pcb/*/production/netlist-contract.json")),
        "pinmux_ledgers": sorted(ROOT.glob("pcb/*/production/pinmux-ledger.json")),
        "schematic_bindings": sorted(ROOT.glob("pcb/*/production/schematic-binding.json")),
        "manual_reports": sorted(
            [
                *(ROOT / "reports").glob("*.json"),
                *(ROOT / "templates").glob("*.json"),
            ]
        ),
    }


def validate_netlist_contract(path: Path) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("schema_version") != 1:
        raise ValueError(f"{path}: schema_version must be 1")
    if value.get("board") != "tropic01-universal-secure-device":
        raise ValueError(f"{path}: board must be tropic01-universal-secure-device")
    if value.get("status") != "pinmux_review_required":
        raise ValueError(f"{path}: status must be pinmux_review_required")

    required_buses = value.get("required_buses")
    if not isinstance(required_buses, dict):
        raise ValueError(f"{path}: required_buses must be an object")
    missing_buses = sorted(REQUIRED_TROPIC01_UNIVERSAL_NETLIST_BUSES - set(required_buses))
    if missing_buses:
        raise ValueError(f"{path}: required_buses missing {', '.join(missing_buses)}")
    for bus_name, nets in required_buses.items():
        if not isinstance(nets, list) or not nets:
            raise ValueError(f"{path}: required_buses.{bus_name} must be a non-empty list")
        if not all(isinstance(net, str) and net.strip() for net in nets):
            raise ValueError(f"{path}: required_buses.{bus_name} must contain non-empty strings")

    release_gates = value.get("release_gates")
    if not isinstance(release_gates, list) or not release_gates:
        raise ValueError(f"{path}: release_gates must be a non-empty list")
    missing_gates = sorted(REQUIRED_TROPIC01_UNIVERSAL_NETLIST_RELEASE_GATES - set(release_gates))
    if missing_gates:
        raise ValueError(f"{path}: release_gates missing {', '.join(missing_gates)}")


def validate_pinmux_ledger(path: Path) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("schema_version") != 1:
        raise ValueError(f"{path}: schema_version must be 1")
    if value.get("board") != "tropic01-universal-secure-device":
        raise ValueError(f"{path}: board must be tropic01-universal-secure-device")
    if value.get("status") != "partial_datasheet_pinmux_confirmed":
        raise ValueError(f"{path}: status must be partial_datasheet_pinmux_confirmed")

    stm32u5 = value.get("stm32u5")
    if not isinstance(stm32u5, dict):
        raise ValueError(f"{path}: stm32u5 must be an object")
    if stm32u5.get("status") != "partial_lqfp100_pinmux_confirmed":
        raise ValueError(f"{path}: stm32u5.status must be partial_lqfp100_pinmux_confirmed")
    assignments = stm32u5.get("assignments")
    if not isinstance(assignments, dict) or not assignments:
        raise ValueError(f"{path}: stm32u5.assignments must contain source-backed assignments")
    missing_assignments = sorted(REQUIRED_TROPIC01_UNIVERSAL_STM32_ASSIGNMENTS - set(assignments))
    if missing_assignments:
        raise ValueError(f"{path}: stm32u5.assignments missing {', '.join(missing_assignments)}")
    pin_owners: dict[str, str] = {}
    for net_name, assignment in assignments.items():
        if not isinstance(assignment, dict):
            raise ValueError(f"{path}: {net_name} must be a source-backed evidence object")
        missing_fields = sorted(REQUIRED_TROPIC01_UNIVERSAL_PINMUX_ASSIGNMENT_FIELDS - set(assignment))
        if missing_fields:
            raise ValueError(
                f"{path}: {net_name} missing source-backed evidence fields: {', '.join(missing_fields)}"
            )
        if assignment.get("review_status") != "source_backed":
            raise ValueError(f"{path}: {net_name} must have source-backed evidence")
        if not isinstance(assignment.get("pin_name"), str) or not assignment["pin_name"].strip():
            raise ValueError(f"{path}: {net_name}.pin_name must be a non-empty string")
        if not isinstance(assignment.get("physical_pin"), int) or assignment["physical_pin"] <= 0:
            raise ValueError(f"{path}: {net_name}.physical_pin must be a positive integer")
        for field in ("function", "bus", "source", "source_table", "evidence"):
            if not isinstance(assignment.get(field), str) or not assignment[field].strip():
                raise ValueError(f"{path}: {net_name}.{field} must be a non-empty string")
        pin_key = f"{assignment['pin_name']}:{assignment['physical_pin']}"
        previous_owner = pin_owners.setdefault(pin_key, net_name)
        if previous_owner != net_name:
            raise ValueError(f"{path}: {net_name} reuses STM32 pin already assigned to {previous_owner}")

    tropic01 = value.get("tropic01")
    if not isinstance(tropic01, dict) or tropic01.get("status") != "datasheet_pinout_confirmed":
        raise ValueError(f"{path}: tropic01.status must be datasheet_pinout_confirmed")
    tropic01_pins = tropic01.get("pins", {})
    for pin_number, expected_name in {"5": "SPI_SDI", "6": "SPI_SDO", "7": "SPI_SCK", "8": "SPI_CSN"}.items():
        if tropic01_pins.get(pin_number) != expected_name:
            raise ValueError(f"{path}: TROPIC01 pin {pin_number} must be {expected_name}")

    display = value.get("display")
    if not isinstance(display, dict):
        raise ValueError(f"{path}: display must be an object")
    if display.get("tft_4wire_spi_mode_select") != {"IM0": "0", "IM1": "1", "IM2": "1"}:
        raise ValueError(f"{path}: display 4-wire SPI mode select must be IM0=0 IM1=1 IM2=1")

    st25r3916b = value.get("st25r3916b")
    if not isinstance(st25r3916b, dict):
        raise ValueError(f"{path}: st25r3916b must be an object")
    if st25r3916b.get("status") != "controller_pinout_confirmed_antenna_matching_required":
        raise ValueError(f"{path}: st25r3916b.status must keep antenna matching required")
    st25_pins = st25r3916b.get("qfn32_pins", {})
    for pin_number, expected_name in {"20": "I2C_EN", "27": "IRQ", "29": "BSS", "30": "SCLK", "31": "MOSI", "32": "MISO"}.items():
        if st25_pins.get(pin_number) != expected_name:
            raise ValueError(f"{path}: ST25R3916B pin {pin_number} must be {expected_name}")
    if "matching_required" not in _flatten_text(st25r3916b).lower():
        raise ValueError(f"{path}: ST25R3916B antenna matching must stay measurement-gated")

    optiga = value.get("optiga")
    if not isinstance(optiga, dict) or optiga.get("status") != "datasheet_pinout_confirmed":
        raise ValueError(f"{path}: optiga.status must be datasheet_pinout_confirmed")
    optiga_pins = optiga.get("pins", {})
    for pin_number, expected_name in {"1": "GND", "3": "SDA", "8": "SCL", "9": "RST", "10": "VCC"}.items():
        if optiga_pins.get(pin_number) != expected_name:
            raise ValueError(f"{path}: OPTIGA pin {pin_number} must be {expected_name}")
    if "dedicated" not in _flatten_text(optiga).lower():
        raise ValueError(f"{path}: OPTIGA I2C policy must require a dedicated bus")

    release_gates = value.get("release_gates")
    if not isinstance(release_gates, list) or not release_gates:
        raise ValueError(f"{path}: release_gates must be a non-empty list")
    missing_gates = sorted(REQUIRED_TROPIC01_UNIVERSAL_PINMUX_RELEASE_GATES - set(release_gates))
    if missing_gates:
        raise ValueError(f"{path}: release_gates missing {', '.join(missing_gates)}")


def validate_schematic_binding(
    path: Path,
    pinmux_path: Path | None = None,
    netlist_contract_path: Path | None = None,
) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("schema_version") != 1:
        raise ValueError(f"{path}: schema_version must be 1")
    if value.get("board") != "tropic01-universal-secure-device":
        raise ValueError(f"{path}: board must be tropic01-universal-secure-device")
    if value.get("status") != "schematic_binding_pre_routing":
        raise ValueError(f"{path}: status must be schematic_binding_pre_routing")

    release_gates = value.get("release_gates")
    if not isinstance(release_gates, list) or not release_gates:
        raise ValueError(f"{path}: release_gates must be a non-empty list")
    missing_gates = sorted(REQUIRED_TROPIC01_UNIVERSAL_SCHEMATIC_BINDING_RELEASE_GATES - set(release_gates))
    if missing_gates:
        raise ValueError(f"{path}: release_gates missing {', '.join(missing_gates)}")

    components = value.get("components")
    if not isinstance(components, dict) or not components:
        raise ValueError(f"{path}: components must be a non-empty object")
    missing_components = sorted(REQUIRED_TROPIC01_UNIVERSAL_SCHEMATIC_COMPONENT_REFS - set(components))
    if missing_components:
        raise ValueError(f"{path}: components missing {', '.join(missing_components)}")
    for ref, component in components.items():
        if not isinstance(component, dict):
            raise ValueError(f"{path}: components.{ref} must be an object")
        for field in ("role", "sheet", "pins"):
            if field not in component:
                raise ValueError(f"{path}: components.{ref}.{field} is required")
        if not isinstance(component["sheet"], str) or not component["sheet"].strip():
            raise ValueError(f"{path}: components.{ref}.sheet must be a non-empty string")
        board_dir = path.parents[1]
        if (board_dir / "kicad").exists() and not (board_dir / component["sheet"]).exists():
            raise ValueError(f"{path}: components.{ref}.sheet does not exist: {component['sheet']}")
        if not isinstance(component["pins"], dict) or not component["pins"]:
            raise ValueError(f"{path}: components.{ref}.pins must be a non-empty object")

    pinmux_path = pinmux_path or path.with_name("pinmux-ledger.json")
    netlist_contract_path = netlist_contract_path or path.with_name("netlist-contract.json")
    pinmux = json.loads(pinmux_path.read_text(encoding="utf-8"))
    netlist_contract = json.loads(netlist_contract_path.read_text(encoding="utf-8"))
    stm32_assignments = pinmux.get("stm32u5", {}).get("assignments", {})
    if not isinstance(stm32_assignments, dict) or not stm32_assignments:
        raise ValueError(f"{pinmux_path}: stm32u5.assignments must be available for schematic binding")

    u1_pins = components["U1"]["pins"]
    for net_name, assignment in stm32_assignments.items():
        pin_binding = u1_pins.get(net_name)
        if not isinstance(pin_binding, dict):
            raise ValueError(f"{path}: U1 missing schematic binding for {net_name}")
        if pin_binding.get("net") != net_name:
            raise ValueError(f"{path}: U1 {net_name} binding must use net {net_name}")
        for field in ("pin_name", "physical_pin"):
            if pin_binding.get(field) != assignment.get(field):
                raise ValueError(
                    f"{path}: U1 {net_name} {field} mismatch: "
                    f"{pin_binding.get(field)!r} != {assignment.get(field)!r}"
                )
        if pin_binding.get("review_status") != "source_backed":
            raise ValueError(f"{path}: U1 {net_name} binding must be source_backed")

    bound_nets: set[str] = set()
    for component in components.values():
        for pin in component["pins"].values():
            if isinstance(pin, dict) and isinstance(pin.get("net"), str) and pin["net"].strip():
                bound_nets.add(pin["net"])

    review_required = value.get("review_required_nets")
    if not isinstance(review_required, dict):
        raise ValueError(f"{path}: review_required_nets must be an object")
    contract_nets = {
        net
        for nets in netlist_contract.get("required_buses", {}).values()
        if isinstance(nets, list)
        for net in nets
        if isinstance(net, str)
    }
    missing_contract_nets = sorted(contract_nets - bound_nets - set(review_required))
    if missing_contract_nets:
        raise ValueError(
            f"{path}: contract nets must be bound or explicitly review-required: "
            f"{', '.join(missing_contract_nets)}"
        )
    for net_name, review in review_required.items():
        if not isinstance(review, dict) or review.get("review_status") != "explicitly_unbound":
            raise ValueError(f"{path}: review_required_nets.{net_name} must be explicitly_unbound")
        if net_name in bound_nets:
            raise ValueError(f"{path}: {net_name} cannot be both bound and explicitly_unbound")
        if not isinstance(review.get("reason"), str) or not review["reason"].strip():
            raise ValueError(f"{path}: review_required_nets.{net_name}.reason must be a non-empty string")


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
    for contract_path in validation_files["netlist_contracts"]:
        validate_netlist_contract(contract_path)
    for ledger_path in validation_files["pinmux_ledgers"]:
        validate_pinmux_ledger(ledger_path)
    for binding_path in validation_files["schematic_bindings"]:
        validate_schematic_binding(binding_path)
    for report_path in validation_files["manual_reports"]:
        validate_manual_report(report_path)
    print("nSealr hardware validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
