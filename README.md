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
- TROPIC01 Universal Secure Device: the only active custom hardware product
  direction in this repository.

## TROPIC01 Universal Secure Device

The custom hardware target is a single compact portrait board for open-source
projects that need a TROPIC01-based secure element device.

Core product decisions:

- TROPIC01 primary open secure element.
- STM32U5 host MCU.
- OPTIGA Trust M class I2C second secure element.
- 2.4 inch portrait capacitive touch display.
- USB-C female receptacle only, centered on the bottom short edge.
- ST25R3916B NFC/RFID controller with a real tuned antenna path.
- LiPo connector and BQ24074-class power path.
- QSPI NOR flash.
- Two high side-actuated physical buttons.
- Hidden back-side pogo/test pads.
- No microSD slot.
- No BLE/WiFi/radio module in Rev A0.

Authoritative files:

- `docs/superpowers/specs/2026-06-08-tropic01-universal-secure-device-design.md`
- `docs/superpowers/plans/2026-06-08-tropic01-universal-secure-device-implementation.md`
- `pcb/tropic01-universal-secure-device/requirements.json`
- `bom/tropic01-universal-secure-device.csv`

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
