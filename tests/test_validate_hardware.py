import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_hardware import validate_bom, validate_manual_report, validate_requirements


ROOT = Path(__file__).resolve().parents[1]
REFERENCE_REPORT = ROOT / "reports/esp32-s3-devkitc-1-detection-2026-05-08.json"


def load_reference_report() -> dict:
    return json.loads(REFERENCE_REPORT.read_text(encoding="utf-8"))


class HardwareValidationTests(unittest.TestCase):
    def test_reference_requirements_are_valid(self) -> None:
        validate_requirements(ROOT / "pcb/reference-esp32-s3-signer/requirements.json")

    def test_reference_qr_signer_requirements_are_valid(self) -> None:
        validate_requirements(ROOT / "pcb/reference-esp32-s3-qr-signer/requirements.json")

    def test_reference_raspberry_qr_vault_requirements_are_valid(self) -> None:
        validate_requirements(ROOT / "kits/reference-raspberry-qr-vault/requirements.json")

    def test_reference_bom_is_valid(self) -> None:
        validate_bom(ROOT / "bom/reference-esp32-s3-signer.csv")

    def test_reference_manual_hardware_report_is_valid(self) -> None:
        validate_manual_report(REFERENCE_REPORT)

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

            with self.assertRaisesRegex(ValueError, "nseal1"):
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


if __name__ == "__main__":
    unittest.main()
