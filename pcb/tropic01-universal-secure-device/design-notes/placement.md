# Placement Intent

Status: placement intent before KiCad board generation.

## Board Shape

- Portrait smartphone-like rectangle.
- Target compact envelope follows the `42.8 mm x 59.91 mm` Newhaven display
  module as closely as electrical, NFC, USB, and battery constraints allow.
- Initial PCB target envelope: approximately `48 mm x 68 mm`.

## Front

- Display covers the front face.
- UI defaults to portrait, but firmware may support horizontal views.

## Edges

- Bottom short edge: centered USB-C female receptacle.
- Top short edge: NFC antenna FPC or tuned antenna keep-out.
- Upper left long edge: side-actuated physical button.
- Upper right long edge: side-actuated physical button.

## Back

- STM32U5, TROPIC01, and OPTIGA form a compact secure island.
- TROPIC01 is placed close to STM32U5 and away from USB connector stress,
  switching regulators, battery connector, and NFC antenna.
- ST25R3916B sits near the top NFC/matching region.
- BQ24074 and battery connector sit where a LiPo can be supported by the case.
- QSPI flash sits close to STM32U5.
- Hidden pogo/test pads sit on the back where a fixture can reach them without
  creating user-facing holes in the enclosure.

## Prohibited Placement Shortcuts

- No decorative NFC loop.
- No front-facing button footprints.
- No USB-C plug footprint.
- No microSD slot.
- No BLE/WiFi/radio module footprint in Rev A0.
