# TROPIC01 Universal Secure Device Rev A

Rev A is the single custom hardware product direction for this repository.

## Product Shape

- Portrait, smartphone-like rectangle.
- Touch display on the front.
- USB-C female receptacle centered on the bottom short edge.
- NFC/RFID antenna path on the top short edge.
- Two side-actuated physical buttons high on the left and right long edges.
- Main electronics on the back side.
- Hidden pogo/test pads covered by the enclosure.

## Core Mounted Hardware

- TROPIC01 primary open secure element.
- STM32U5 host MCU.
- OPTIGA Trust M class I2C second secure element.
- 2.4 inch portrait capacitive touch display.
- USB-C female receptacle.
- ST25R3916B NFC/RFID controller.
- LiPo connector and BQ24074-class power path.
- QSPI NOR flash.
- Two high side-actuated physical buttons.
- Hidden back-side pogo/test pads.
- Compact I2C/UART/SPI expansion pads or connector.

## Excluded From Rev A

- USB-C male plug variant.
- microSD slot.
- BLE.
- WiFi.
- Radio module.
- Camera.
- Large 3.5-4.0 inch display.
- Consumer enclosure.
- Production certification claims.

## Security Notes

TROPIC01 is the open primary trust anchor. The OPTIGA-class second secure
element provides independent defense in depth for attestation, anti-clone, and
policy work. STM32U5 owns UI, USB, NFC policy, firmware update, and debug lock.

NFC is included for mobile/passkey/contactless workflows but must be power-gated
and disabled by default in hardened firmware. microSD and radios are excluded to
avoid unnecessary attack surface and enclosure complexity.

## Current Status

The repository currently contains requirements and BOM contracts. KiCad
schematic, PCB routing, NFC antenna tuning, and PCBWay production outputs remain
future implementation work. Do not treat generated manufacturing files as
release-ready until ERC, DRC, routing, and manifest checks pass.
