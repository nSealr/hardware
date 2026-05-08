# NostrSeal Hardware

Open hardware reference designs for NostrSeal signer devices.

This repository should contain buildable, inspectable, and modifiable hardware
artifacts: devkit wiring, PCB design files, BOMs, enclosures, and provisioning
fixtures.

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
  Pro OV5640 candidate line.
- First open BOM scaffold for a reference USB signer board.
- Machine-readable manual hardware validation reports, starting with ESP32-S3
  board detection evidence.
- Validation script and tests for required interfaces, security/review
  requirements, approval-digest review binding, stateless QR vault exclusion of
  TROPIC01 interfaces, BOM headers, BOM categories, duplicate designators, and
  manual hardware report safety flags.

The current files are requirements and BOM scaffolding, not routed PCB files.

## Initial Layout

- `pcb/`: KiCad and board design files.
- `enclosures/`: 3D case designs and mechanical notes.
- `bom/`: component lists and sourcing notes.
- `reports/`: manual hardware validation reports.
- `docs/`: assembly, test, and hardware security guides.

## Quality Baseline

Run the repository verification loop with:

```sh
make ci
```

## License

Hardware design files, PCB sources, BOMs, enclosure files, and assembly
artifacts are released under CERN-OHL-P-2.0 unless a file says otherwise.
