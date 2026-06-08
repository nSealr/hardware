# Testing

## Current Baseline

```sh
make ci
```

The baseline runs repository verification, unit tests for hardware validators,
bytecode compilation, and directory-driven validation of committed requirements,
OS profiles, BOMs, reports, and report templates.

## Implemented Coverage

- Reference ESP32-S3 USB/NIP-46 requirements validation.
- ESP32-S3 stateless QR vault requirements validation.
- Raspberry/Pi stateless QR vault kit requirements validation.
- Raspberry/Pi stateless QR vault OS profile validation.
- Raspberry/Pi stateless QR vault report-template validation.
- Identity/policy requirement validation for ESP32 and Raspberry requirement
  sets.
- TROPIC01 Universal Secure Device requirements validation.
- TROPIC01 Universal Secure Device BOM validation, including frozen MPN checks
  for TROPIC01, STM32U5, OPTIGA-class second secure element, display, USB-C
  receptacle, NFC controller, LiPo power path, QSPI flash, side buttons, and
  hidden pogo/test pads.
- Rejection of stateless QR vault TROPIC01 usage.
- Manual hardware report validation.
- Directory-driven discovery for requirements, OS profiles, BOMs, reports, and
  templates.

## Custom Hardware Expectations

The custom hardware test target is `tropic01_universal_secure_device`.

Tests currently assert:

- one single custom product direction;
- TROPIC01 as primary open secure element;
- STM32U5 host MCU;
- OPTIGA Trust M class second secure element included;
- USB-C female receptacle only;
- portrait touch display;
- two side physical buttons;
- NFC/RFID included and power-gated;
- LiPo connector and real power path;
- QSPI flash;
- hidden pogo/test pads;
- no microSD;
- no default BLE/WiFi/radio.

KiCad routing and PCBWay export tests must be added only after the schematic and
board source are generated from real nets. Until then, generated manufacturing
outputs must be treated as invalid.
