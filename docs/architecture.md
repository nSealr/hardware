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
  the first ESP32 USB/NIP-46 signer reference board.
- `pcb/reference-esp32-s3-qr-signer/requirements.json`: checked requirements
  for the ESP32 stateless QR vault devkit validation path, currently centered
  on the T-Display S3 Pro OV5640 candidate.
- `bom/reference-esp32-s3-signer.csv`: first BOM scaffold with required and
  optional component categories.
- `scripts/validate_hardware.py`: validation for requirements and BOM quality.

The USB/NIP-46 reference requirements keep TROPIC01 out of the MVP and leave
persistent-secret secure-element research to the custom hardware-wallet family.
Mandatory hardware focuses on native USB, local review display, physical
approve/reject controls, and ESP32-S3 security capabilities. Review hardware
must support a flow that binds physical approval to both displayed request id
and displayed approval digest before firmware signing is enabled.

The QR signer requirements add camera, battery, wireless-disable, physical
approval, and touch-not-approval constraints for stateless devkit validation.
They explicitly exclude persistent signing secrets and TROPIC01 interfaces.
They are not a custom PCB, schematic, or manufacturing package.
