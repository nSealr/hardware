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
- `kits/reference-raspberry-qr-vault/requirements.json`: checked requirements
  for the Raspberry/Pi stateless QR vault kit validation path, covering camera,
  trusted display, physical buttons, response QR display, wireless disablement,
  removable boot media, and RAM-only custody.
- `bom/reference-esp32-s3-signer.csv`: first BOM scaffold with required and
  optional component categories.
- `reports/esp32-s3-devkitc-1-detection-2026-05-08.json`: first manual
  hardware validation report, recording ESP32-S3 board detection only.
- `scripts/validate_hardware.py`: validation for requirements and BOM quality.

The USB/NIP-46 reference requirements keep TROPIC01 out of the MVP and leave
persistent-secret secure-element research to the custom hardware-wallet family.
Mandatory hardware focuses on native USB, local review display, physical
approve/reject controls, and ESP32-S3 security capabilities. Review hardware
must support a flow that binds physical approval to both displayed request id
and displayed approval digest before firmware signing is enabled.

The QR signer requirements add camera, battery, wireless-disable, physical
approval, and touch-not-approval constraints for stateless devkit validation.
They also require explicit QR contract text for the shared `nseal1` envelope,
trusted review, and physical approval. They explicitly exclude persistent
signing secrets and TROPIC01 interfaces. They are not a custom PCB, schematic,
or manufacturing package.

The Raspberry QR vault kit requirements follow the same stateless QR contract
without ESP32-specific secure boot or flash-encryption assumptions. They require
camera input, a trusted local display, tactile physical approval/rejection,
response QR output, disabled wireless, and removable boot-media discipline
before any Pi build can be treated as more than a desktop harness.

Manual hardware reports are structured evidence for bring-up work. They must
record hardware, source repo, firmware commit, exact procedure, expected and
observed results, limitations, and safety flags. Validation rejects reports
that enable production signing, and stateless target reports must not claim
persistent secrets or TROPIC01 usage.
