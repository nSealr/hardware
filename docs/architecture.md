# Architecture

`nSealr/hardware` contains open hardware reference material: requirements, BOMs,
KiCad sources, kit profiles, validation reports, and production notes.

## Boundaries

Hardware requirements can state which boards, displays, cameras, controls,
secure elements, provisioning paths, and debug policies are needed to satisfy
the shared `nSealr/specs` feature targets. They must not create new feature
behavior or signer taxonomy outside the shared specs contract model.

## Supported Hardware Lines

- `pcb/reference-esp32-s3-signer/requirements.json`: ESP32 USB/NIP-46 signer
  reference requirements.
- `pcb/reference-esp32-s3-qr-signer/requirements.json`: ESP32 stateless QR
  vault devkit validation path.
- `kits/reference-raspberry-qr-vault/requirements.json`: Raspberry/Pi stateless
  QR vault kit requirements.
- `kits/reference-raspberry-qr-vault/os-profile.json`: Raspberry/Pi stateless
  QR vault operating profile.

## Custom Hardware Direction

This repository currently has no active custom PCB. The legacy TROPIC01
Universal Secure Device board was archived, with full git history, to the
private read-only repository `nSealr/hardware-legacy-tropic01-universal`.

The next custom hardware direction — a minimal custom hardware wallet — is
defined by the `nSealr/specs` five-solution device-matrix decision and will be
introduced in a later program phase. Until that board lands, the reference
requirements, kits, BOMs, reports, and templates above are the maintained
contracts here.

## Validation

`scripts/validate_hardware.py` is the repository contract validator. It checks
requirements files, kit OS profiles, BOM quality, manual reports, and report
templates. Unit tests in `tests/test_validate_hardware.py` pin accepted hardware
contracts and rejection behavior.
