# nSealr Hardware

Open hardware reference designs for nSealr signer devices.

This repository should contain buildable, inspectable, and modifiable hardware
artifacts: devkit wiring, PCB design files, BOMs, enclosures, and provisioning
fixtures.

Feature targets and current status are defined in `nSealr/specs`
`vectors/features/signer-feature-matrix-v0.json`. This repository provides the
hardware artifacts needed by those families; it must not turn hardware
requirements into separate signer families or change shared feature behavior
outside the specs `contract_id` model.

## Planned Outputs

- ESP32-S3 reference build wiring diagrams.
- Display/button/camera module compatibility notes.
- KiCad PCB files for a custom signer board.
- BOM with substitutes and sourcing notes.
- 3D-printable enclosure files.
- Provisioning and debug jig documentation.

## Current Capabilities

- Machine-readable ESP32-S3 USB/NIP-46 signer reference requirements.
- Machine-readable ESP32 stateless QR vault requirements for the T-Display S3
  Pro OV5640 candidate line, including validated QR-contract requirements for
  `nsealr1`, trusted review, physical approval, and the confirmed Waveshare
  `ESP32-S3-Touch-LCD-3.5B-C` secondary target.
- Machine-readable Raspberry/Pi stateless QR vault kit requirements, including
  camera, trusted display, physical controls, response QR display, disabled
  wireless, RAM-only custody, no TROPIC01 dependency, and an explicit
  SeedSigner-compatible Pi Zero hardware profile with a validated 40-pin GPIO
  review-button map.
- Machine-readable Raspberry/Pi stateless QR vault OS profile, requiring
  removable boot media, disabled or absent wireless, RAM-only session custody,
  no swap during signing, no remote access during signing, and no persistent
  signing-secret storage.
- Account/custody target documentation for hardware acceptance: QR vault
  hardware must not introduce persistent secret or policy storage, while
  future ESP32 USB/custom persistent hardware must support an encrypted device
  vault, one device-level v0 unlock ceremony, and device-reviewed
  per-public-key policy before production signing claims.
- Machine-readable custom persistent-secret wallet Rev A requirements and BOM
  scaffold. Rev A is USB-C bus-powered, connected/no-wireless, no-battery, and
  TROPIC01-assisted. TROPIC01 direct Schnorr/BIP-340 is tracked as future
  vendor-roadmap work, not as a current public API claim.
- Validated Raspberry/Pi OS profile smoke-report template for future hardware
  acceptance evidence.
- First open BOM scaffolds for a reference USB signer board and a
  Raspberry/Pi stateless QR vault kit plus the custom persistent-secret wallet
  Rev A. The Raspberry kit BOM is centered on a Pi Zero-class board,
  Pi/ZeroCam OV5647 camera, Waveshare-compatible ST7789 240x240 display HAT,
  GPIO controls, removable microSD boot media, and SeedSigner-style enclosure
  assumptions.
- Machine-readable manual hardware validation reports, starting with ESP32-S3
  board detection evidence and continuing through ESP32-S3 USB/display signer
  protocol smoke evidence for disabled signing, malformed transport, review,
  and security-fuse audit gates.
- Validation script and tests for required interfaces, security/review
  requirements, approval-digest review binding, stateless QR vault exclusion of
  TROPIC01 interfaces, custom wallet TROPIC01/power-cycle/no-battery/no-air-gap
  boundaries, QR vault envelope/review/approval requirements,
  identity/policy route requirements, BOM headers, BOM categories, duplicate
  designators, manual hardware report safety flags, and directory-driven
  validation discovery for requirements, OS profiles, BOMs, reports, and
  report templates. ESP32 QR requirements validation now also rejects stale
  Waveshare `3.5-C` secondary-target drift.

The current files are requirements and BOM scaffolding, not routed PCB files.

## Initial Layout

- `pcb/`: KiCad and board design files.
- `kits/`: devkit and off-the-shelf hardware requirements before custom PCB
  work.
- `enclosures/`: 3D case designs and mechanical notes.
- `bom/`: component lists and sourcing notes.
- `reports/`: manual hardware validation reports.
- `templates/`: validated report templates for future manual acceptance runs.
- `docs/`: assembly, test, and hardware security guides.

## Quality Baseline

Run the repository verification loop with:

```sh
make ci
```

## License

Hardware design files, PCB sources, BOMs, enclosure files, and assembly
artifacts are released under CERN-OHL-P-2.0 unless a file says otherwise.
