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
CUSTOM_WALLET_REQUIREMENTS = ROOT / "pcb/custom-persistent-secret-wallet/requirements.json"
SPECS_SNAPSHOTS = ROOT / "tests/fixtures/specs"
CUSTOM_WALLET_ACCOUNT = json.loads(
    (SPECS_SNAPSHOTS / "vectors/accounts/custom-hardware-wallet-slot-0.json").read_text(encoding="utf-8")
)
CUSTOM_WALLET_POLICY = json.loads(
    (SPECS_SNAPSHOTS / "vectors/policies/manual-only-persistent-device.json").read_text(encoding="utf-8")
)
CUSTOM_WALLET_SCOPED_POLICY = json.loads(
    (SPECS_SNAPSHOTS / "vectors/policies/scoped-automation-daily-use.json").read_text(encoding="utf-8")
)
CUSTOM_WALLET_GRANT = json.loads(
    (SPECS_SNAPSHOTS / "vectors/grants/custom-hardware-wallet-kind-1-session.json").read_text(encoding="utf-8")
)
CUSTOM_WALLET_POLICY_CHANGE = json.loads(
    (SPECS_SNAPSHOTS / "vectors/policy-changes/custom-hardware-wallet-enable-kind-1-automation.json").read_text(
        encoding="utf-8"
    )
)
CUSTOM_WALLET_ROUTE_SELECTION = json.loads(
    (SPECS_SNAPSHOTS / "vectors/route-selections/custom-hardware-wallet-sign-event-slot-0.json").read_text(
        encoding="utf-8"
    )
)


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

    def test_custom_persistent_secret_wallet_requirements_are_valid(self) -> None:
        validate_requirements(CUSTOM_WALLET_REQUIREMENTS)

    def test_custom_wallet_requirements_match_shared_route_descriptor(self) -> None:
        value = json.loads(CUSTOM_WALLET_REQUIREMENTS.read_text(encoding="utf-8"))
        identity_text = "\n".join(value["identity_policy_requirements"])
        route = CUSTOM_WALLET_ACCOUNT["signer_route"]
        capabilities = CUSTOM_WALLET_ACCOUNT["capabilities"]
        recovery = CUSTOM_WALLET_ACCOUNT["recovery"]
        selection = CUSTOM_WALLET_ROUTE_SELECTION["selection"]

        self.assertEqual(CUSTOM_WALLET_ACCOUNT["format"], "nsealr-account-descriptor-v0")
        self.assertEqual(route["type"], "custom_hardware_wallet")
        self.assertEqual(route["repository"], "hardware")
        self.assertEqual(route["transport"], "usb")
        self.assertEqual(route["custody"], "custom_hardware_persistent")
        self.assertEqual(route["trusted_review"], "device_display")
        self.assertEqual(route["policy_support"], "scoped_automation")
        self.assertTrue(capabilities["physical_review"])
        self.assertTrue(capabilities["physical_approval"])
        self.assertTrue(capabilities["persistent_grants"])
        self.assertEqual(recovery["type"], "hardware_wallet_slot")
        self.assertTrue(recovery["backup_required"])
        self.assertEqual(CUSTOM_WALLET_ACCOUNT["policy_profile_id"], "policy-manual-only-persistent-device")
        self.assertIn(route["type"], CUSTOM_WALLET_POLICY["route_types"])
        self.assertEqual(CUSTOM_WALLET_POLICY["mode"], "manual_only")
        self.assertFalse(CUSTOM_WALLET_POLICY["grants_allowed"])
        self.assertIn(route["type"], CUSTOM_WALLET_SCOPED_POLICY["route_types"])
        self.assertTrue(CUSTOM_WALLET_SCOPED_POLICY["grant_constraints"]["device_confirmation_required"])
        self.assertEqual(CUSTOM_WALLET_GRANT["account_id"], CUSTOM_WALLET_ACCOUNT["account_id"])
        self.assertEqual(CUSTOM_WALLET_GRANT["route_type"], route["type"])
        self.assertEqual(
            CUSTOM_WALLET_GRANT["permission"],
            {"method": "sign_event", "parameter": "1", "event_kind": 1},
        )
        self.assertEqual(CUSTOM_WALLET_POLICY_CHANGE["proposal"]["account_id"], CUSTOM_WALLET_ACCOUNT["account_id"])
        self.assertEqual(CUSTOM_WALLET_POLICY_CHANGE["proposal"]["route_type"], route["type"])
        self.assertEqual(CUSTOM_WALLET_POLICY_CHANGE["proposal"]["current_policy_id"], CUSTOM_WALLET_POLICY["policy_id"])
        self.assertEqual(
            CUSTOM_WALLET_POLICY_CHANGE["proposal"]["proposed_policy_id"],
            CUSTOM_WALLET_SCOPED_POLICY["policy_id"],
        )
        self.assertEqual(
            CUSTOM_WALLET_POLICY_CHANGE["proposal"]["proposed_grant_ids"],
            [CUSTOM_WALLET_GRANT["grant_id"]],
        )
        self.assertFalse(CUSTOM_WALLET_POLICY_CHANGE["proposal"]["companion_authoritative"])
        self.assertTrue(CUSTOM_WALLET_POLICY_CHANGE["proposal"]["device_review_required"])
        self.assertTrue(CUSTOM_WALLET_POLICY_CHANGE["proposal"]["physical_approval_required"])
        self.assertEqual(selection["account_id"], CUSTOM_WALLET_ACCOUNT["account_id"])
        self.assertEqual(selection["route_type"], route["type"])
        self.assertEqual(selection["repository"], route["repository"])
        self.assertEqual(selection["custody"], route["custody"])
        self.assertFalse(selection["contains_secret_material"])
        self.assertIn(route["type"], identity_text)
        self.assertIn(route["custody"], identity_text)
        self.assertIn(CUSTOM_WALLET_ACCOUNT["policy_profile_id"], identity_text)
        self.assertIn("sign_event kind 1", identity_text)

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

    def test_custom_persistent_secret_wallet_bom_is_valid(self) -> None:
        validate_bom(ROOT / "bom/custom-persistent-secret-wallet.csv")

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

    def test_custom_wallet_rejects_missing_tropic01_power_cycle_control(self) -> None:
        original = json.loads(CUSTOM_WALLET_REQUIREMENTS.read_text(encoding="utf-8"))
        original["mandatory_interfaces"] = [
            item for item in original["mandatory_interfaces"] if item != "tropic01_power_cycle_control"
        ]

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "requirements.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "tropic01_power_cycle_control"):
                validate_requirements(path)

    def test_custom_wallet_rejects_air_gapped_claim_on_usb_transport(self) -> None:
        original = json.loads(CUSTOM_WALLET_REQUIREMENTS.read_text(encoding="utf-8"))
        original["notes"].append("This Rev A board is an air-gapped USB wallet.")

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "requirements.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "air-gapped"):
                validate_requirements(path)

    def test_custom_wallet_rejects_current_tropic01_bip340_signing_claim(self) -> None:
        original = json.loads(CUSTOM_WALLET_REQUIREMENTS.read_text(encoding="utf-8"))
        original["security_requirements"].append("TROPIC01 currently performs BIP-340 signing for Nostr events.")

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "requirements.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "BIP-340"):
                validate_requirements(path)

    def test_custom_wallet_rejects_battery_power_in_rev_a_interfaces(self) -> None:
        original = json.loads(CUSTOM_WALLET_REQUIREMENTS.read_text(encoding="utf-8"))
        original["optional_interfaces"].append("battery_power")

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "requirements.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "battery_power"):
                validate_requirements(path)

    def test_custom_wallet_rejects_dedicated_tropic01_reset_interface(self) -> None:
        original = json.loads(CUSTOM_WALLET_REQUIREMENTS.read_text(encoding="utf-8"))
        original["optional_interfaces"].append("tropic01_reset_pin")

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "requirements.json"
            path.write_text(json.dumps(original), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "power-cycle control"):
                validate_requirements(path)

    def test_custom_wallet_bom_requires_tropic01_power_cycle_component(self) -> None:
        original = (ROOT / "bom/custom-persistent-secret-wallet.csv").read_text(encoding="utf-8")
        original = original.replace(
            "U4,power,TROPIC01 load switch or power-gating circuit,true,"
            "Used for controlled TROPIC01 power-cycle reset and recovery.\n",
            "U4,power,Auxiliary 3.3 V rail monitor,true,Used for generic power-good monitoring.\n",
        )

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "custom-persistent-secret-wallet.csv"
            path.write_text(original, encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "power-cycle/load-switch"):
                validate_bom(path)

    def test_custom_wallet_bom_rejects_tropic01_reset_pin_component(self) -> None:
        original = (ROOT / "bom/custom-persistent-secret-wallet.csv").read_text(encoding="utf-8")
        original += "TP9,secure_element,TROPIC01 reset pin test pad,false,Do not add this component.\\n"

        with tempfile.TemporaryDirectory() as temp_root:
            path = Path(temp_root) / "custom-persistent-secret-wallet.csv"
            path.write_text(original, encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "not a reset pin component"):
                validate_bom(path)

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
