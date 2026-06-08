# Architecture

`nSealr/hardware` contains open hardware reference material: requirements, BOMs,
KiCad sources, kit profiles, validation reports, and production notes.

## Boundaries

Hardware requirements can state which boards, displays, cameras, controls,
secure elements, provisioning paths, and debug policies are needed to satisfy
the shared `nSealr/specs` feature targets. They must not create new feature
behavior or signer taxonomy outside the shared specs contract model.

## Supported Hardware Lines

- `pcb/reference-esp32-s3-signer/requirements.json`: ESP32 USB/NIP-46 signer
  reference requirements.
- `pcb/reference-esp32-s3-qr-signer/requirements.json`: ESP32 stateless QR
  vault devkit validation path.
- `kits/reference-raspberry-qr-vault/requirements.json`: Raspberry/Pi stateless
  QR vault kit requirements.
- `kits/reference-raspberry-qr-vault/os-profile.json`: Raspberry/Pi stateless
  QR vault operating profile.
- `pcb/tropic01-universal-secure-device/requirements.json`: the active custom
  hardware product direction.

## Custom Hardware Direction

The only active custom hardware product in this repository is the TROPIC01
Universal Secure Device.

The board is a compact portrait device with:

- TROPIC01 primary open secure element.
- STM32U5 application MCU.
- OPTIGA Trust M class I2C second secure element.
- 2.4 inch portrait capacitive touch display.
- USB-C female receptacle only.
- ST25R3916B NFC/RFID controller.
- LiPo battery connector and power-path charger.
- QSPI NOR flash.
- Two side-actuated physical buttons.
- Hidden pogo/test pads.
- No microSD, BLE, WiFi, or radio in Rev A0.

The current custom hardware files are requirements and BOM contracts. KiCad
schematic, routing, and PCBWay outputs must not be treated as production-ready
until ERC, DRC, routing, antenna validation notes, BOM, position, Gerbers, drill,
and manifest checks are complete.

## Security Model

TROPIC01 is the open primary trust anchor. The OPTIGA-class second secure
element provides independent defense in depth. STM32U5 owns USB, UI, NFC policy,
display/touch, physical button handling, firmware update, and debug lock.

Default Rev A0 excludes BLE/WiFi/radio and microSD because those surfaces add
attack paths and mechanical complexity. NFC is included because mobile/passkey
and contactless workflows are core use cases, but it must be power-gated and
disabled by default in hardened firmware.

## Validation

`scripts/validate_hardware.py` is the repository contract validator. It checks
requirements files, kit OS profiles, BOM quality, manual reports, and report
templates. Unit tests in `tests/test_validate_hardware.py` pin accepted hardware
contracts and rejection behavior.
