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

- Machine-readable ESP32-S3 signer reference requirements.
- First open BOM scaffold for a reference USB signer board.
- Validation script and tests for required interfaces, security/review
  requirements, approval-digest review binding, BOM headers, BOM categories,
  and duplicate designators.

The current files are requirements and BOM scaffolding, not routed PCB files.

## Initial Layout

- `pcb/`: KiCad and board design files.
- `enclosures/`: 3D case designs and mechanical notes.
- `bom/`: component lists and sourcing notes.
- `docs/`: assembly, test, and hardware security guides.

## Quality Baseline

Run the repository verification loop with:

```sh
make ci
```

## License

Hardware design files, PCB sources, BOMs, enclosure files, and assembly
artifacts are released under CERN-OHL-P-2.0 unless a file says otherwise.
