# Roadmap

## Foundation: Reference Requirements And BOM

Implemented:

- ESP32-S3 USB signer requirements JSON.
- ESP32-S3 QR signer requirements JSON.
- Raspberry/Pi stateless QR vault kit requirements JSON.
- Raspberry/Pi stateless QR vault OS profile JSON.
- ESP32-S3 USB signer reference BOM scaffold.
- Raspberry/Pi stateless QR vault kit BOM scaffold.
- Raspberry/Pi stateless QR vault OS profile report template.
- Raspberry/Pi stateless QR vault full QR-flow report template.
- Manual hardware validation report schema.
- Validator and tests, including review approval-digest binding.

## Custom Hardware Direction

The legacy TROPIC01 Universal Secure Device board has been archived, with full
git history, to the private read-only repository
`nSealr/hardware-legacy-tropic01-universal`.

The next custom hardware direction is a minimal custom hardware wallet defined by
the `nSealr/specs` five-solution device-matrix decision. Its board tree, BOM, and
production contracts will be added in a later program phase, at which point the
milestones and production gate below apply to that board.

## Reference Hardware Lines

ESP32 and Raspberry/Pi work remains useful for validating transport, QR,
display, camera, and operating-profile assumptions. These are supported hardware
lines, distinct from any future custom PCB product.

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
