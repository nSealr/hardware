# Architecture

`NostrSeal/hardware` contains open hardware reference material.

## Responsibilities

- BOMs.
- Wiring diagrams.
- KiCad design files.
- Enclosure notes.
- Display, button, camera, and module compatibility notes.
- Provisioning and debug jig documentation.
- Hardware security notes.

PCB work must follow proven firmware and UX requirements, not precede them.

## Implemented Foundation

- `pcb/reference-esp32-s3-signer/requirements.json`: checked requirements for
  the first ESP32-S3 USB signer reference board.
- `bom/reference-esp32-s3-signer.csv`: first BOM scaffold with required and
  optional component categories.
- `scripts/validate_hardware.py`: validation for requirements and BOM quality.

The reference requirements make TROPIC01 and camera support optional until their
respective feasibility tracks are proven. Mandatory hardware focuses on native
USB, local review display, physical approve/reject controls, and ESP32-S3
security capabilities.
