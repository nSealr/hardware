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
  removable boot media, RAM-only custody, and explicit SeedSigner-compatible
  Pi Zero hardware targets.
- `kits/reference-raspberry-qr-vault/os-profile.json`: checked operating
  profile for future Raspberry/Pi stateless QR vault images, requiring
  removable boot media, disabled or absent wireless, RAM-only session custody,
  no swap, no remote access during signing, disabled setup services, and
  acceptance evidence.
- `bom/reference-esp32-s3-signer.csv`: first BOM scaffold with required and
  optional component categories.
- `bom/reference-raspberry-qr-vault-kit.csv`: first kit BOM scaffold for the
  Raspberry/Pi stateless QR vault path, covering the single-board computer,
  camera, trusted display, physical controls, power, boot media, temporary
  setup path, and wireless-disable evidence.
- `templates/raspberry-qr-vault-os-profile-smoke.json`: validated manual
  report template for future Raspberry OS profile acceptance evidence.
- `reports/esp32-s3-devkitc-1-detection-2026-05-08.json`: first manual
  hardware validation report, recording ESP32-S3 board detection only.
- `scripts/validate_hardware.py`: directory-driven validation for
  requirements, Raspberry OS profiles, BOM quality, manual reports, and report
  templates.

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
The checked compatibility profile centers the kit on the SeedSigner-style
Raspberry Pi Zero stack: Pi Zero-class board, Pi/ZeroCam OV5647 camera,
Waveshare-compatible ST7789 240x240 SPI display HAT, GPIO joystick/buttons,
removable microSD boot media, and SeedSigner-OS/Buildroot reference shape.
Pi 3/4/5 variants can be documented later only as development or accessibility
variants that preserve the same offline QR and RAM-only custody boundary.
The companion kit BOM is a validation scaffold, not a purchase order: it keeps
wireless mitigation, removable boot media, temporary setup/debug removal, and
RAM-only custody visible before Raspberry hardware acceptance starts.
The OS profile adds the software-side acceptance boundary for that same kit:
no swap-backed secret leakage, no remote login during signing, and explicit
wireless/secret/session-loss evidence before a Raspberry image can be treated
as a stateless QR vault image.

Manual hardware reports are structured evidence for bring-up work. They must
record hardware, source repo, firmware commit, exact procedure, expected and
observed results, limitations, and safety flags. Validation rejects reports
that enable production signing, and stateless target reports must not claim
persistent secrets or TROPIC01 usage.
Raspberry OS profile smoke reports additionally need explicit evidence terms
for removable boot media, wireless state, swap state, remote access, RAM-only
custody, persistent-secret absence, and power-cycle session loss.
The top-level validator discovers committed validation inputs under `pcb/`,
`kits/`, `bom/`, `reports/`, and `templates/` so future hardware artifacts do
not need bespoke wiring before CI checks their schema and safety flags.
