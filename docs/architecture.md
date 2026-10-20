# Architecture

`nSealr/hardware` contains open hardware reference material: requirements, BOMs,
KiCad sources, kit profiles, validation reports, and production notes.

## Boundaries

Hardware owns exact electrical/mechanical artifacts, parts, pinout, expansion,
power and production tests. The [current product contract](https://github.com/nSealr/nsealr/blob/main/docs/product/contract.md)
owns Signer semantics; the [Board realization requirements](https://github.com/nSealr/nsealr/blob/main/docs/restart/pcb-development.md#product-choice-before-h04)
and canonical task graph own the programmable platform's hardware gates.
Board SDK supplies reusable device services without importing Nostr. Historical
specs/reference requirements do not define another current product taxonomy.

## Existing reference requirements, not support claims

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

The next custom hardware is a programmable security-oriented Board with
independent developer value. The Signer, a display/input/expansion diagnostic
and a generic key-operation example are bounded representative consumers.
Compare a quality touchscreen with the current controls/panel and study a
concrete two-SE architecture; no host, panel or chip pair is selected here.
Before freeze compare a few complete configurations with benefits, limits,
resource/development margin, indicative dated costs/uncertainty and missing
proof. Current API/manual, independent-review and physical gates remain hard
requirements. Owner firmware, debug, update/recovery and secret reset have
explicit lifecycle boundaries; the first image model does not isolate hostile
applications. Reference requirements, kits and templates remain useful inputs,
without transferring their old names or assumed guarantees to the new Board.

## Validation

`scripts/validate_hardware.py` is the repository contract validator. It checks
requirements files, kit OS profiles, BOM quality, manual reports, and report
templates. Unit tests in `tests/test_validate_hardware.py` pin accepted hardware
contracts and rejection behavior.
