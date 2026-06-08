import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import validate_hardware
from scripts.validate_hardware import (
    validate_bom,
    validate_manual_report,
    validate_raspberry_os_profile,
    validate_requirements,
)


ROOT = Path(__file__).resolve().parents[1]
REFERENCE_REPORT = ROOT / "reports/esp32-s3-devkitc-1-detection-2026-05-08.json"
RASPBERRY_OS_REPORT_TEMPLATE = ROOT / "templates/raspberry-qr-vault-os-profile-smoke.json"
RASPBERRY_QR_FLOW_REPORT_TEMPLATE = ROOT / "templates/raspberry-qr-vault-full-flow-smoke.json"
TROPIC01_UNIVERSAL_REQUIREMENTS = ROOT / "pcb/tropic01-universal-secure-device/requirements.json"
TROPIC01_UNIVERSAL_KICAD = ROOT / "pcb/tropic01-universal-secure-device/kicad"
SPECS_SNAPSHOTS = ROOT / "tests/fixtures/specs"


def load_reference_report() -> dict:
    return json.loads(REFERENCE_REPORT.read_text(encoding="utf-8"))


class HardwareValidationTests(unittest.TestCase):
    def test_reference_requirements_are_valid(self) -> None:
        validate_requirements(ROOT / "pcb/reference-esp32-s3-signer/requirements.json")

    def test_reference_qr_signer_requirements_are_valid(self) -> None:
        validate_requirements(ROOT / "pcb/reference-esp32-s3-qr-signer/requirements.json")

    def test_esp32_qr_requirements_pin_waveshare_3_5b_c_secondary_target(self) -> None:
        value = json.loads(
            (ROOT / "pcb/reference-esp32-s3-qr-signer/requirements.json").read_text(encoding="utf-8")
        )

        self.assertEqual(value["secondary_devkit_candidate"]["sku"], "ESP32-S3-Touch-LCD-3.5B-C")
        self.assertEqual(value["secondary_devkit_candidate"]["display_driver"], "AXS15231B")
        self.assertEqual(value["secondary_devkit_candidate"]["display_bus"], "QSPI")
        self.assertEqual(value["secondary_devkit_candidate"]["camera_module"], "OV5640")

    def test_esp32_qr_requirements_reject_missing_secondary_target(self) -> None:
        original = json.loads(
            (ROOT / "pcb/reference-esp32-s3-qr-signer/requirements.json").read_text(encoding="utf-8")
        )
        original.pop("secondary_devkit_candidate", None)

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "requirements.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "secondary_devkit_candidate"):
                validate_requirements(path)

    def test_esp32_qr_requirements_reject_unselected_waveshare_sku(self) -> None:
        original = json.loads(
            (ROOT / "pcb/reference-esp32-s3-qr-signer/requirements.json").read_text(encoding="utf-8")
        )
        original["secondary_devkit_candidate"] = {
            "sku": "ESP32-S3-Touch-LCD-3.5-C",
            "display_driver": "ST7796",
            "display_bus": "SPI",
            "camera_module": "OV5640",
        }

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "requirements.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "ESP32-S3-Touch-LCD-3.5B-C"):
                validate_requirements(path)

    def test_reference_raspberry_qr_vault_requirements_are_valid(self) -> None:
        validate_requirements(ROOT / "kits/reference-raspberry-qr-vault/requirements.json")

    def test_tropic01_universal_secure_device_requirements_are_valid(self) -> None:
        validate_requirements(TROPIC01_UNIVERSAL_REQUIREMENTS)

    def test_tropic01_universal_secure_device_is_single_product_with_second_se_and_no_microsd(self) -> None:
        value = json.loads(TROPIC01_UNIVERSAL_REQUIREMENTS.read_text(encoding="utf-8"))
        flattened = json.dumps(value, sort_keys=True).lower()

        self.assertEqual(value["device_class"], "tropic01_universal_secure_device")
        self.assertIn("second_secure_element_i2c", value["mandatory_interfaces"])
        self.assertIn("hidden_pogo_test_pads", value["mandatory_interfaces"])
        self.assertIn("no_microsd_slot", value["mandatory_interfaces"])
        self.assertNotIn("second_secure_element_dnp", value["optional_interfaces"])
        self.assertNotIn("microsd_dnp", [item.lower() for item in value["optional_interfaces"]])
        self.assertIn("optiga", flattened)
        self.assertIn("pogo", flattened)
        self.assertIn("covered by the enclosure", flattened)
        self.assertIn("do not include microsd", flattened)

    def test_tropic01_universal_secure_device_pins_rev_a0_component_decisions(self) -> None:
        value = json.loads(TROPIC01_UNIVERSAL_REQUIREMENTS.read_text(encoding="utf-8"))
        decisions = value["rev_a0_component_decisions"]
        security_text = "\n".join(value["security_requirements"]).lower()

        self.assertEqual(decisions["tropic01_default_part"], "TR01-C2P-T301")
        self.assertIn("TR01-C2P-T310", decisions["tropic01_preferred_part"])
        self.assertIn("libtropic 4.0.0", decisions["tropic01_firmware_target"])
        self.assertEqual(decisions["mcu_primary"], "STM32U585VIT6 LQFP100")
        self.assertIn("STM32U575VIT6", decisions["mcu_fallback"])
        self.assertIn("W25Q128JV", decisions["storage_primary"])
        self.assertIn("OPTIGA", decisions["second_secure_element"])
        self.assertIn("Trust M", decisions["second_secure_element"])
        self.assertIn("no microSD", decisions["removable_storage_policy"])
        self.assertIn("polling fallback", security_text)
        self.assertIn("maintenance mode", security_text)
        self.assertIn("laser fault injection", security_text)
        self.assertIn("3.3 v spi", security_text)

    def test_reference_usb_signer_requirements_reference_identity_policy_contracts(self) -> None:
        value = json.loads((ROOT / "pcb/reference-esp32-s3-signer/requirements.json").read_text(encoding="utf-8"))
        text = "\n".join(value["identity_policy_requirements"])

        self.assertIn("nsealr-account-descriptor-v0", text)
        self.assertIn("esp32_usb_nip46", text)
        self.assertIn("policy-manual-only-persistent-device", text)
        self.assertIn("policy-scoped-automation-daily-use", text)
        self.assertIn("grant-esp32-usb-kind-1-session", text)

    def test_qr_requirements_reject_missing_identity_policy_contract_terms(self) -> None:
        original = json.loads(
            (ROOT / "pcb/reference-esp32-s3-qr-signer/requirements.json").read_text(encoding="utf-8")
        )
        original.pop("identity_policy_requirements", None)

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "requirements.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "identity_policy_requirements"):
                validate_requirements(path)

    def test_qr_requirements_reject_persistent_grant_claims(self) -> None:
        original = json.loads(
            (ROOT / "kits/reference-raspberry-qr-vault/requirements.json").read_text(encoding="utf-8")
        )
        original["identity_policy_requirements"] = [
            "Use nsealr-account-descriptor-v0 route raspberry_qr_vault.",
            "Use policy-manual-only-qr-vault.",
            "Allow persistent_grants: true for convenience.",
        ]

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "requirements.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "persistent_grants: false"):
                validate_requirements(path)

    def test_raspberry_qr_requirements_require_seedsigner_compatibility_profile(self) -> None:
        original = json.loads(
            (ROOT / "kits/reference-raspberry-qr-vault/requirements.json").read_text(encoding="utf-8")
        )
        original.pop("seed_signer_compatibility", None)

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "requirements.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "seed_signer_compatibility"):
                validate_requirements(path)

    def test_raspberry_qr_requirements_reject_missing_seedsigner_display_target(self) -> None:
        original = json.loads(
            (ROOT / "kits/reference-raspberry-qr-vault/requirements.json").read_text(encoding="utf-8")
        )
        original["seed_signer_compatibility"] = {
            "primary_physical_target": "Raspberry Pi Zero",
            "supported_board_targets": ["Raspberry Pi Zero"],
            "display_targets": ["Waveshare 1.3 inch LCD HAT ST7789 240x240 SPI"],
            "camera_targets": ["Pi Zero-compatible OV5647 camera"],
            "control_targets": ["Waveshare HAT GPIO buttons"],
            "os_targets": ["SeedSigner OS pi0 Buildroot profile"],
            "acceptance_targets": ["Boot and review on Pi Zero hardware"],
        }
        original["seed_signer_compatibility"]["display_targets"] = []

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "requirements.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "display_targets"):
                validate_requirements(path)

    def test_raspberry_qr_requirements_require_gpio_button_profile(self) -> None:
        original = json.loads(
            (ROOT / "kits/reference-raspberry-qr-vault/requirements.json").read_text(encoding="utf-8")
        )
        original["seed_signer_compatibility"].pop("gpio_button_profile", None)

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "requirements.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "gpio_button_profile"):
                validate_requirements(path)

    def test_raspberry_qr_gpio_button_profile_requires_reject_mapping(self) -> None:
        original = json.loads(
            (ROOT / "kits/reference-raspberry-qr-vault/requirements.json").read_text(encoding="utf-8")
        )
        del original["seed_signer_compatibility"]["gpio_button_profile"]["actions"]["reject"]

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "requirements.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "gpio_button_profile.actions.reject"):
                validate_requirements(path)

    def test_raspberry_qr_gpio_button_profile_requires_distinct_approve_reject_pins(self) -> None:
        original = json.loads(
            (ROOT / "kits/reference-raspberry-qr-vault/requirements.json").read_text(encoding="utf-8")
        )
        original["seed_signer_compatibility"]["gpio_button_profile"]["actions"]["reject"] = [33]

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "requirements.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "approve and reject pins must be distinct"):
                validate_requirements(path)

    def test_reference_usb_signer_bom_is_valid(self) -> None:
        validate_bom(ROOT / "bom/reference-esp32-s3-signer.csv")

    def test_reference_raspberry_qr_vault_kit_bom_is_valid(self) -> None:
        validate_bom(ROOT / "bom/reference-raspberry-qr-vault-kit.csv")

    def test_tropic01_universal_secure_device_bom_is_valid(self) -> None:
        validate_bom(ROOT / "bom/tropic01-universal-secure-device.csv")

    def test_tropic01_universal_secure_device_bom_freezes_core_mpns(self) -> None:
        with (ROOT / "bom/tropic01-universal-secure-device.csv").open(encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        by_designator = {row["designator"]: row for row in rows}

        expected_mpns = {
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
        for designator, mpn in expected_mpns.items():
            self.assertEqual(by_designator[designator]["mpn"], mpn)

        self.assertEqual(by_designator["U2"]["freeze_status"], "frozen")
        self.assertEqual(by_designator["DISP1"]["freeze_status"], "frozen")
        self.assertEqual(by_designator["U11"]["required"], "true")
        self.assertEqual(by_designator["U11"]["freeze_status"], "candidate")
        self.assertEqual(by_designator["ANT1"]["freeze_status"], "tuning_required")

    def test_tropic01_universal_secure_device_bom_mounts_receptacle_battery_nfc_second_se_and_no_microsd(self) -> None:
        with (ROOT / "bom/tropic01-universal-secure-device.csv").open(encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        by_designator = {row["designator"]: row for row in rows}
        bom_text = "\n".join(" ".join(row.values()).lower() for row in rows)

        self.assertIn("USB-C receptacle", by_designator["J1"]["description"])
        self.assertIn("female", by_designator["J1"]["notes"].lower())
        self.assertNotIn("plug", by_designator["J1"]["description"].lower())
        self.assertEqual(by_designator["U9"]["required"], "true")
        self.assertEqual(by_designator["ANT1"]["required"], "true")
        self.assertEqual(by_designator["U10"]["required"], "true")
        self.assertEqual(by_designator["J9"]["required"], "true")
        self.assertEqual(by_designator["U11"]["required"], "true")
        self.assertIn("power-gated", by_designator["U9"]["notes"].lower())
        self.assertIn("power-path", by_designator["U10"]["description"].lower())
        self.assertIn("optiga", by_designator["U11"]["description"].lower())
        self.assertNotIn("microsd", bom_text)

    def test_tropic01_universal_secure_device_pcbway_bom_export_excludes_dnp_rows(self) -> None:
        from scripts import export_tropic01_universal_pcbway

        rows = export_tropic01_universal_pcbway.pcbway_bom_rows(
            export_tropic01_universal_pcbway.load_bom(ROOT / "bom/tropic01-universal-secure-device.csv")
        )
        by_designator = {row["Designator"]: row for row in rows}

        self.assertEqual(by_designator["J1"]["Manufacturer Part Number"], "USB4105-GF-A")
        self.assertEqual(by_designator["U11"]["Manufacturer Part Number"], "OPTIGA-TRUST-M-SLS32AIA")
        self.assertNotIn("U1_ALT", by_designator)
        self.assertNotIn("U2_ALT", by_designator)

    def test_tropic01_universal_secure_device_pcbway_bom_export_excludes_non_pcba_rows(self) -> None:
        from scripts import export_tropic01_universal_pcbway

        rows = export_tropic01_universal_pcbway.pcbway_bom_rows(
            export_tropic01_universal_pcbway.load_bom(ROOT / "bom/tropic01-universal-secure-device.csv")
        )
        designators = {row["Designator"] for row in rows}

        self.assertIn("SW1,SW2", designators)
        self.assertNotIn("DISP1", designators)
        self.assertNotIn("ANT1", designators)
        self.assertFalse(any(designator.startswith("TP_") for designator in designators))

    def test_tropic01_universal_secure_device_pcbway_manifest_is_blocked_until_kicad_release_checks_pass(self) -> None:
        manifest = json.loads(
            (ROOT / "pcb/tropic01-universal-secure-device/production/pcbway-manifest.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(manifest["board"], "tropic01-universal-secure-device")
        self.assertEqual(manifest["usb_connector"], "USB4105-GF-A")
        self.assertEqual(manifest["second_secure_element"], "OPTIGA-TRUST-M-SLS32AIA")
        self.assertEqual(manifest["microsd"], "excluded")
        self.assertFalse(manifest["release_outputs_valid"])
        self.assertEqual(manifest["erc"], "blocked")
        self.assertEqual(manifest["drc"], "blocked")
        self.assertIn("no routed KiCad PCB", " ".join(manifest["blocked_reasons"]))

    def test_tropic01_universal_secure_device_pcbway_export_rejects_unrouted_board(self) -> None:
        from scripts import export_tropic01_universal_pcbway

        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            board = root / "board.kicad_pcb"
            board.write_text('(kicad_pcb (version 20240108) (net 0 ""))', encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "not routed"):
                export_tropic01_universal_pcbway.validate_board_ready_for_export(board)

    def test_tropic01_universal_secure_device_kicad_sources_exist(self) -> None:
        expected = [
            TROPIC01_UNIVERSAL_KICAD / "tropic01-universal-secure-device.kicad_pro",
            TROPIC01_UNIVERSAL_KICAD / "tropic01-universal-secure-device.kicad_sch",
            TROPIC01_UNIVERSAL_KICAD / "tropic01-universal-secure-device.kicad_pcb",
            TROPIC01_UNIVERSAL_KICAD / "sheets" / "power_usb.kicad_sch",
            TROPIC01_UNIVERSAL_KICAD / "sheets" / "stm32u5_host.kicad_sch",
            TROPIC01_UNIVERSAL_KICAD / "sheets" / "tropic01.kicad_sch",
            TROPIC01_UNIVERSAL_KICAD / "sheets" / "display_controls.kicad_sch",
            TROPIC01_UNIVERSAL_KICAD / "sheets" / "storage_expansion.kicad_sch",
            TROPIC01_UNIVERSAL_KICAD / "sheets" / "secure_element_2.kicad_sch",
            TROPIC01_UNIVERSAL_KICAD / "sheets" / "optional_profiles.kicad_sch",
        ]

        for path in expected:
            self.assertTrue(path.exists(), f"missing KiCad source {path}")

    def test_tropic01_universal_secure_device_kicad_sources_include_second_secure_element_sheet(self) -> None:
        sheet = (TROPIC01_UNIVERSAL_KICAD / "sheets" / "secure_element_2.kicad_sch").read_text(
            encoding="utf-8"
        ).lower()

        self.assertIn("optiga", sheet)
        self.assertIn("trust m", sheet)
        self.assertIn("i2c", sheet)
        self.assertIn("u11", sheet)
        self.assertIn("second secure element", sheet)

    def test_tropic01_universal_secure_device_kicad_sources_remove_stale_custom_hardware_choices(self) -> None:
        kicad_text = "\n".join(
            path.read_text(encoding="utf-8", errors="replace")
            for path in TROPIC01_UNIVERSAL_KICAD.rglob("*.kicad_sch")
        )
        board_text = (TROPIC01_UNIVERSAL_KICAD / "tropic01-universal-secure-device.kicad_pcb").read_text(
            encoding="utf-8",
            errors="replace",
        )
        combined = f"{kicad_text}\n{board_text}"

        self.assertNotIn("microSD", combined)
        self.assertNotIn("Second SE profile: DNP", combined)
        self.assertNotIn("PCB NFC LOOP", combined)
        self.assertNotIn("USB-C plug", combined)

    def test_tropic01_universal_secure_device_board_drawings_include_display_and_nfc_features(self) -> None:
        board_text = (TROPIC01_UNIVERSAL_KICAD / "tropic01-universal-secure-device.kicad_pcb").read_text(
            encoding="utf-8",
            errors="replace",
        )

        self.assertIn("DISP1 PORTRAIT TOUCH DISPLAY ENVELOPE 42.8 x 59.91 mm", board_text)
        self.assertIn("ANT1 TOP EDGE NFC ANTENNA FPC OR TUNED KEEP-OUT", board_text)
        self.assertNotIn("PCB NFC LOOP", board_text)

    def test_tropic01_universal_secure_device_kicad_board_contains_final_core_refs(self) -> None:
        board_text = (TROPIC01_UNIVERSAL_KICAD / "tropic01-universal-secure-device.kicad_pcb").read_text(
            encoding="utf-8",
            errors="replace",
        )

        for ref in ("U1", "U2", "U9", "U10", "U11", "J1", "J2", "J2B", "SW1", "SW2"):
            self.assertIn(f'"{ref}"', board_text)
        self.assertIn("USB4105-GF-A", board_text)
        self.assertIn("USB_C_Receptacle_GCT_USB4105", board_text)
        self.assertIn("Molex_54132-4062", board_text)
        self.assertIn("Molex_52271-0679", board_text)
        self.assertIn("SW_SPST_EVQP7A", board_text)
        self.assertIn("OPTIGA-TRUST-M-SLS32AIA", board_text)

    def test_reference_raspberry_qr_vault_os_profile_is_valid(self) -> None:
        validate_raspberry_os_profile(ROOT / "kits/reference-raspberry-qr-vault/os-profile.json")

    def test_main_validator_checks_reference_raspberry_qr_vault_kit_bom(self) -> None:
        validated_boms: list[str] = []

        with (
            patch.object(validate_hardware, "validate_requirements", return_value=None),
            patch.object(validate_hardware, "validate_raspberry_os_profile", return_value=None),
            patch.object(validate_hardware, "validate_manual_report", return_value=None),
            patch.object(validate_hardware, "validate_bom", side_effect=lambda path: validated_boms.append(Path(path).name)),
        ):
            validate_hardware.main()

        self.assertIn("reference-esp32-s3-signer.csv", validated_boms)
        self.assertIn("reference-raspberry-qr-vault-kit.csv", validated_boms)

    def test_main_validator_discovers_repository_validation_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            paths = [
                root / "pcb/custom-usb/requirements.json",
                root / "kits/custom-raspberry/requirements.json",
                root / "kits/custom-raspberry/os-profile.json",
                root / "bom/custom.csv",
                root / "reports/custom-report.json",
                root / "templates/custom-template.json",
            ]
            for path in paths:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("{}", encoding="utf-8")

            validated_requirements: list[Path] = []
            validated_profiles: list[Path] = []
            validated_boms: list[Path] = []
            validated_reports: list[Path] = []

            with (
                patch.object(validate_hardware, "ROOT", root),
                patch.object(validate_hardware, "validate_requirements", side_effect=validated_requirements.append),
                patch.object(validate_hardware, "validate_raspberry_os_profile", side_effect=validated_profiles.append),
                patch.object(validate_hardware, "validate_bom", side_effect=validated_boms.append),
                patch.object(validate_hardware, "validate_manual_report", side_effect=validated_reports.append),
            ):
                validate_hardware.main()

            self.assertEqual(
                [root / "kits/custom-raspberry/requirements.json", root / "pcb/custom-usb/requirements.json"],
                validated_requirements,
            )
            self.assertEqual([root / "kits/custom-raspberry/os-profile.json"], validated_profiles)
            self.assertEqual([root / "bom/custom.csv"], validated_boms)
            self.assertEqual(
                [root / "reports/custom-report.json", root / "templates/custom-template.json"],
                validated_reports,
            )

    def test_reference_manual_hardware_report_is_valid(self) -> None:
        validate_manual_report(REFERENCE_REPORT)

    def test_raspberry_os_profile_report_template_is_valid(self) -> None:
        validate_manual_report(RASPBERRY_OS_REPORT_TEMPLATE)

    def test_raspberry_qr_flow_report_template_is_valid(self) -> None:
        validate_manual_report(RASPBERRY_QR_FLOW_REPORT_TEMPLATE)

    def test_manual_report_accepts_protocol_smoke_type(self) -> None:
        original = load_reference_report()
        original["report_type"] = "protocol_smoke"
        original["expected_result"] = "The device refuses sign_event with signing_disabled."
        original["observed_result"] = "sign_event returned signing_disabled."
        original["limitations"] = ["Protocol smoke only; signing disabled."]

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "report.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            validate_manual_report(path)

    def test_protocol_smoke_report_rejects_missing_disabled_signing_evidence(self) -> None:
        original = load_reference_report()
        original["report_type"] = "protocol_smoke"
        original["expected_result"] = "The device answers capability requests."
        original["observed_result"] = "The device answered capability requests."
        original["limitations"] = ["Protocol smoke only; no production signing claim."]

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "report.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "signing_disabled"):
                validate_manual_report(path)

    def test_requirements_reject_missing_required_interfaces(self) -> None:
        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "requirements.json"
            path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "device_class": "esp32_s3_usb_signer",
                        "mandatory_interfaces": ["usb_c_native"],
                        "security_requirements": [],
                        "review_requirements": [],
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "missing mandatory interfaces"):
                validate_requirements(path)

    def test_requirements_reject_missing_approval_digest_review_binding(self) -> None:
        original = json.loads((ROOT / "pcb/reference-esp32-s3-signer/requirements.json").read_text(encoding="utf-8"))
        original["review_requirements"] = [
            item for item in original["review_requirements"] if "approval_digest" not in item
        ]

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "requirements.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "approval_digest"):
                validate_requirements(path)

    def test_qr_requirements_reject_missing_camera_interface(self) -> None:
        original = json.loads(
            (ROOT / "pcb/reference-esp32-s3-qr-signer/requirements.json").read_text(encoding="utf-8")
        )
        original["mandatory_interfaces"] = [
            item for item in original["mandatory_interfaces"] if item != "camera"
        ]

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "requirements.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "camera"):
                validate_requirements(path)

    def test_raspberry_qr_requirements_reject_missing_response_qr_display(self) -> None:
        original = json.loads(
            (ROOT / "kits/reference-raspberry-qr-vault/requirements.json").read_text(encoding="utf-8")
        )
        original["mandatory_interfaces"] = [
            item for item in original["mandatory_interfaces"] if item != "response_qr_display"
        ]

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "requirements.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "response_qr_display"):
                validate_requirements(path)

    def test_qr_requirements_reject_missing_qr_requirements(self) -> None:
        original = json.loads(
            (ROOT / "pcb/reference-esp32-s3-qr-signer/requirements.json").read_text(encoding="utf-8")
        )
        del original["qr_requirements"]

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "requirements.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "qr_requirements"):
                validate_requirements(path)

    def test_qr_requirements_reject_missing_core_qr_contract_terms(self) -> None:
        original = json.loads(
            (ROOT / "pcb/reference-esp32-s3-qr-signer/requirements.json").read_text(encoding="utf-8")
        )
        original["qr_requirements"] = ["Decode QR input before request review."]

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "requirements.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "nsealr1"):
                validate_requirements(path)

    def test_qr_requirements_reject_missing_wireless_disabled_policy(self) -> None:
        original = json.loads(
            (ROOT / "pcb/reference-esp32-s3-qr-signer/requirements.json").read_text(encoding="utf-8")
        )
        original["security_requirements"] = [
            item for item in original["security_requirements"] if "Wireless must be disabled" not in item
        ]

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "requirements.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Wireless must be disabled"):
                validate_requirements(path)

    def test_qr_requirements_reject_tropic01_interfaces(self) -> None:
        original = json.loads(
            (ROOT / "pcb/reference-esp32-s3-qr-signer/requirements.json").read_text(encoding="utf-8")
        )
        original["optional_interfaces"].append("tropic01_spi")

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "requirements.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "TROPIC01"):
                validate_requirements(path)

    def test_raspberry_os_profile_rejects_swap(self) -> None:
        original = json.loads(
            (ROOT / "kits/reference-raspberry-qr-vault/os-profile.json").read_text(encoding="utf-8")
        )
        original["swap_enabled_during_signing"] = True

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "os-profile.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "swap"):
                validate_raspberry_os_profile(path)

    def test_raspberry_os_profile_rejects_remote_access_during_signing(self) -> None:
        original = json.loads(
            (ROOT / "kits/reference-raspberry-qr-vault/os-profile.json").read_text(encoding="utf-8")
        )
        original["remote_access_enabled_during_signing"] = True

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "os-profile.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "remote_access"):
                validate_raspberry_os_profile(path)

    def test_raspberry_os_profile_rejects_persistent_secret_storage(self) -> None:
        original = json.loads(
            (ROOT / "kits/reference-raspberry-qr-vault/os-profile.json").read_text(encoding="utf-8")
        )
        original["persistent_secret_storage_allowed"] = True

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "os-profile.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "persistent_secret_storage"):
                validate_raspberry_os_profile(path)

    def test_raspberry_os_profile_requires_seed_entry_policy(self) -> None:
        original = json.loads(
            (ROOT / "kits/reference-raspberry-qr-vault/os-profile.json").read_text(encoding="utf-8")
        )
        original.pop("session_secret_input_policy", None)

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "os-profile.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "session_secret_input_policy"):
                validate_raspberry_os_profile(path)

    def test_raspberry_os_profile_requires_seed_entry_evidence(self) -> None:
        original = json.loads(
            (ROOT / "kits/reference-raspberry-qr-vault/os-profile.json").read_text(encoding="utf-8")
        )
        original["acceptance_evidence"] = [
            item for item in original["acceptance_evidence"] if "seed" not in item.lower()
        ]

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "os-profile.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "seed_entry"):
                validate_raspberry_os_profile(path)

    def test_manual_report_rejects_missing_production_signing_flag(self) -> None:
        original = load_reference_report()
        del original["production_signing_enabled"]

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "report.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "production_signing_enabled"):
                validate_manual_report(path)

    def test_manual_report_rejects_persistent_secrets_on_stateless_targets(self) -> None:
        original = load_reference_report()
        original["target_family"] = "esp32_stateless_qr_vault"
        original["persistent_secret_present"] = True

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "report.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "stateless targets must not report persistent secrets"):
                validate_manual_report(path)

    def test_manual_report_rejects_tropic01_on_stateless_targets(self) -> None:
        original = load_reference_report()
        original["target_family"] = "esp32_stateless_qr_vault"
        original["tropic01_used"] = True

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "report.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "stateless targets must not report TROPIC01 usage"):
                validate_manual_report(path)

    def test_raspberry_os_profile_report_rejects_missing_power_cycle_evidence(self) -> None:
        original = json.loads(RASPBERRY_OS_REPORT_TEMPLATE.read_text(encoding="utf-8"))
        original["observed_result"] = "Wi-Fi, Bluetooth, swap, SSH, and persistent signing secret checks passed."
        original["procedure"] = [
            step for step in original["procedure"] if "power-cycle" not in step.lower() and "power cycle" not in step.lower()
        ]
        original["limitations"] = [
            item for item in original["limitations"] if "power-cycle" not in item.lower() and "power cycle" not in item.lower()
        ]

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "raspberry-os-report.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "power_cycle"):
                validate_manual_report(path)

    def test_raspberry_qr_flow_report_rejects_missing_camera_scan_evidence(self) -> None:
        original = json.loads(RASPBERRY_QR_FLOW_REPORT_TEMPLATE.read_text(encoding="utf-8"))
        original["hardware"]["camera"] = "TBD physical camera details"
        original["procedure"] = [
            step
            for step in original["procedure"]
            if "camera" not in step.lower() and "nsealr1" not in step.lower()
        ]
        original["observed_result"] = (
            "Display, GPIO buttons, response QR, companion verification, "
            "RAM-only custody, and approval_digest checks remain documented."
        )

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "raspberry-qr-flow-report.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "camera_scan"):
                validate_manual_report(path)

    def test_raspberry_qr_flow_report_rejects_missing_gpio_evidence(self) -> None:
        original = json.loads(RASPBERRY_QR_FLOW_REPORT_TEMPLATE.read_text(encoding="utf-8"))
        original["hardware"]["physical_controls"] = "TBD controls"
        original["procedure"] = [
            step
            for step in original["procedure"]
            if all(term not in step.lower() for term in ("gpio", "button", "approve", "reject", "scroll"))
        ]
        original["observed_result"] = (
            "Pi Zero camera nsealr1 QR scan, trusted display review, response "
            "QR, companion verify-response, RAM-only custody, request id, and "
            "approval_digest checks remain documented."
        )

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "raspberry-qr-flow-report.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "physical_controls"):
                validate_manual_report(path)


if __name__ == "__main__":
    unittest.main()
