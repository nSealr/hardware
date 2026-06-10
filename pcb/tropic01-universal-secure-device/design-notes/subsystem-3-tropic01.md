# Subsystem 3 — TROPIC01 primary secure element (QFN32) design

Date: 2026-06-10
Status: design captured (pinout source-backed in pinmux-ledger.json). Clean rebuild.

## Pinout (verified, from pinmux-ledger)

| Pin | Name | Connection |
| ---: | --- | --- |
| 1, 11, 24 | VCC | `+3V3_TROPIC_SW` (switched rail from U4) + 100 nF each |
| 2, 12, 23 | GND | `GND` |
| 4 | GPO | `TROPIC_GPO` → MCU PB2 (EXTI input; firmware also supports polling) |
| 5 | SPI_SDI | `TROPIC_SPI_MOSI` ← MCU PA7 (host drives in) |
| 6 | SPI_SDO | `TROPIC_SPI_MISO` → MCU PA6 |
| 7 | SPI_SCK | `TROPIC_SPI_SCK` ← MCU PA5 |
| 8 | SPI_CSN | `TROPIC_SPI_CSN` ← MCU PA4 |
| others | NU | per TROPIC01 datasheet section 11 connection guidance (no-connect unless the datasheet requires a tie) |

## Rules

- SPI mode **CPOL=0 CPHA=0, MSB-first**, 3.3 V logic only.
- **No reset pin**: recovery is by power-cycling `+3V3_TROPIC_SW` through the
  TPS22917 load switch (`TROPIC_PWR_EN` = MCU PB0 → U4 ON). This is the Rev A0
  mandated method.
- Decoupling: 100 nF at each VCC pin + one 1 µF bulk on `+3V3_TROPIC_SW`.
- Keep the TROPIC01 SPI (SPI1, PA4-7) separate from the display/NFC SPI buses.
- June 2026 laser fault-injection advisory stays in the threat model / firmware
  update policy (documentation, not a board change).

## ERC gate

VCC/GND/SPI/GPO bound; NU pins explicitly no-connect; decoupling present; then
ERC clean before subsystem 4 (OPTIGA).
