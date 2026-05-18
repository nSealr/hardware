# TROPIC01 Open Hardware Inventory

This inventory captures the TROPIC01 public hardware material used to shape the
nSealr custom wallet requirements.

## Useful Reference Boards

- TROPIC01 USB DevKit: useful for PC-side `libtropic` API bring-up and firmware
  update research. It uses an STM32 bridge and is not a complete nSealr signing
  device because it lacks trusted review controls.
- TROPIC01 Arduino Shield: useful for no-solder SPI prototyping. It includes
  level translation for Arduino-style hosts; that should not be copied into a
  native 3.3 V ESP32-S3 board unless a 5 V expansion header is added.
- TROPIC01 Mini Board: useful as the closest compact embedded reference for
  direct QFN32 integration and minimal passives.
- TROPIC01 Raspberry Pi Shield and Click boards: useful for host experiments,
  but not the default path for a pocket ESP32-S3 hardware wallet.

## Component Lessons

- TROPIC01 package is QFN32 4x4 mm with 0.4 mm pitch and exposed pad.
- The public pinout exposes SPI SDI/SDO/SCK/CSN, GPO/IRQ, VCC, GND, and
  configuration/no-use pins. Do not invent a dedicated reset pin.
- Use three local 100 nF decoupling capacitors for the TROPIC01 supply pins and
  keep them close to the package.
- Include the 47k reference pull network shown in Tropic Square designs.
- Add a TROPIC01 power-control path so firmware can recover by power cycling the
  chip after SPI/session errors.
- Bring TROPIC01 SPI and GPO/IRQ to test pads on prototypes for logic analyzer
  debugging.

## Firmware And Provisioning Lessons

- Public ECC commands are P-256/ECDSA and Ed25519/EdDSA today.
- Schnorr/BIP-340 support should be tracked as a planned vendor roadmap item,
  not represented as a current public API capability.
- Pairing-key lifecycle is part of the product design. Prototype flows may use
  default pairing keys, but production-like flows need owned pairing keys and a
  plan to invalidate defaults where appropriate.
- MAC-and-Destroy is a primitive for PIN attempt hardening. nSealr still needs a
  wallet-specific PIN/KEK design and tests.
- Firmware update paths are signed and lifecycle-sensitive. Treat custom
  firmware or vendor Schnorr enablement as a separate integration track.
