# TROPIC01 Open Hardware Inventory

This inventory captures the public TROPIC01 hardware material used to shape the
TROPIC01 Universal Secure Device.

## Useful Reference Boards

- TROPIC01 USB DevKit: useful for `libtropic` API bring-up, firmware update
  research, and STM32 host integration patterns.
- TROPIC01 Arduino Shield: useful for no-solder SPI prototyping, but its
  5 V/level-translation assumptions should not be copied into the native 3.3 V
  universal device core.
- TROPIC01 Mini Board: useful as the closest compact QFN32 integration
  reference for package, decoupling, pull network, and SPI breakout.
- TROPIC01 Raspberry Pi Shield and Click boards: useful for host experiments,
  Linux SPI work, and external-host mode validation.
- Trezor Safe 7: useful as a defense-in-depth reference for TROPIC01 plus a
  second secure element, NFC, UI separation, and antenna/FPC partitioning.

## Component Lessons

- TROPIC01 package is QFN32 4x4 mm with 0.4 mm pitch and exposed pad.
- Public TROPIC01 integration uses SPI SDI/SDO/SCK/CSN, GPO/IRQ where
  available, VCC, GND, and documented pull pins. Do not invent a dedicated
  reset pin.
- Use local decoupling close to every TROPIC01 VCC pin.
- Include the reference pull network shown in Tropic Square designs.
- Add a TROPIC01 power-control path so firmware can recover by power cycling
  the chip after SPI/session errors.
- Bring TROPIC01 SPI and GPO/IRQ to hidden test pads or fixtures for bring-up,
  then lock or cover them in hardened builds.

## Product Lessons

- TROPIC01 is the primary open secure element, not the application processor.
- STM32U5 is the Rev A0 host MCU.
- OPTIGA Trust M class I2C secure element is included as independent defense in
  depth.
- NFC/RFID is useful enough to include, but must be power-gated and treated as a
  contactless attack surface.
- microSD is excluded from the single product because it adds enclosure openings,
  filesystem parsing, and misuse risk as supposed secure storage.
- BLE/WiFi/radio are excluded from Rev A0.

## Firmware And Provisioning Lessons

- Public ECC commands are P-256/ECDSA and Ed25519/EdDSA; firmware must not claim
  unverified TROPIC01 Schnorr/BIP-340 support.
- Pairing-key lifecycle is part of the product design. Prototype flows may use
  default pairing keys, but hardened flows need owned pairing keys and a plan to
  invalidate defaults where appropriate.
- MAC-and-Destroy is a useful primitive for PIN attempt hardening, but product
  firmware still needs a reviewed PIN/KEK design.
- Firmware update paths are signed and lifecycle-sensitive. The June 3, 2026
  TROPIC01 laser fault injection advisory must remain visible in the threat
  model and update policy.
