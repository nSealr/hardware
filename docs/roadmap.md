# Roadmap

## Foundation: Reference Requirements And BOM

Implemented:

- ESP32-S3 USB signer requirements JSON.
- ESP32-S3 QR signer requirements JSON.
- Raspberry/Pi stateless QR vault kit requirements JSON.
- Raspberry/Pi stateless QR vault OS profile JSON.
- ESP32-S3 USB signer reference BOM scaffold.
- Raspberry/Pi stateless QR vault kit BOM scaffold.
- TROPIC01 Universal Secure Device requirements JSON.
- TROPIC01 Universal Secure Device BOM.
- Raspberry/Pi stateless QR vault OS profile report template.
- Raspberry/Pi stateless QR vault full QR-flow report template.
- Manual hardware validation report schema.
- Validator and tests, including review approval-digest binding.

## Active Custom Hardware: TROPIC01 Universal Secure Device

The active custom hardware direction is a single compact portrait board with
TROPIC01, STM32U5, OPTIGA-class second secure element, touch display, USB-C
female receptacle, NFC/RFID, LiPo power path, QSPI flash, side buttons, hidden
pogo pads, and no microSD/BLE/WiFi/radio in Rev A0.

Next milestones:

1. Build real KiCad schematic sheets from the approved product contract.
2. Verify exact footprints for display FFC connectors, USB-C, side buttons,
   OPTIGA package, NFC controller, battery connector, and TROPIC01 QFN.
3. Generate a compact portrait placement around the display envelope.
4. Route the board with controlled USB, clean power domains, short TROPIC01 SPI,
   NFC antenna strategy, and hidden pogo/debug access.
5. Run ERC and DRC.
6. Generate PCBWay BOM, position, Gerbers, drill, STEP, and manifest only after
   the design is connected and routed.
7. Bring up Rev A0 on bench: power, USB, display/touch, buttons, TROPIC01,
   OPTIGA, QSPI, NFC, battery path, and debug lock.

## Reference Hardware Lines

ESP32 and Raspberry/Pi work remains useful for validating transport, QR,
display, camera, and operating-profile assumptions. These are supported hardware
lines, but they are not the custom TROPIC01 PCB product.

## Production Readiness Gate

No file in `production/` is release-ready until the manifest records:

- requirements validation pass;
- BOM validation pass;
- KiCad ERC pass;
- KiCad DRC pass;
- non-empty routed copper;
- valid PCBWay BOM and position exports;
- NFC antenna tuning notes;
- explicit Rev A0 manufacturing limitations.
