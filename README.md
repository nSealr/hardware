# nSealr Hardware

Open hardware reference designs, BOMs, validation contracts, and production
notes for nSealr signer and secure-device hardware.

Feature targets and current status are defined in `nSealr/specs`
`vectors/features/signer-feature-matrix-v0.json`. This repository provides
hardware artifacts for those families; it must not create separate signer-family
behavior outside the shared specs contract model.

## Current Hardware Lines

- ESP32-S3 USB/NIP-46 signer reference requirements.
- ESP32-S3 stateless QR vault requirements and accepted display/camera devkit
  targets.
- Raspberry/Pi stateless QR vault kit requirements, OS profile, BOM, and smoke
  report templates.

## Archived Hardware

The legacy TROPIC01 Universal Secure Device board has been retired from this
repository. Its complete design — KiCad project, BOM, production contracts,
docs, and board-specific scripts — was archived with full git history to the
private, read-only repository `nSealr/hardware-legacy-tropic01-universal`. It is
superseded by the minimal custom hardware wallet direction recorded in the
`nSealr/specs` five-solution device-matrix decision; the replacement board will
be introduced in a later program phase.

## Quality Baseline

Run the repository verification loop with:

```sh
make ci
```

or the hardware validator directly:

```sh
python3 scripts/validate_hardware.py
python3 -m unittest tests.test_validate_hardware -v
```

## Layout

- `pcb/`: requirements and KiCad board design files.
- `kits/`: off-the-shelf kit requirements before custom PCB work.
- `enclosures/`: 3D case designs and mechanical notes.
- `bom/`: component lists and sourcing notes.
- `reports/`: manual hardware validation reports.
- `templates/`: validated report templates for future manual acceptance runs.
- `docs/`: architecture, testing, assembly, and security notes.

## License

Hardware design files, PCB sources, BOMs, enclosure files, and assembly
artifacts are released under CERN-OHL-P-2.0 unless a file says otherwise.
