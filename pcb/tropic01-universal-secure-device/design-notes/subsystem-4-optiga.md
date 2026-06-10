# Subsystem 4 — OPTIGA Trust M second secure element (USON-10) design

Date: 2026-06-10
Status: design captured, verified from OPTIGA Trust M datasheet Rev 3.70
(Figure 2 integration). Clean rebuild.

## Pinout (verified) and connections

| Pin | Name | Connection |
| ---: | --- | --- |
| 10 | VCC | `+3V3` + 100 nF |
| 1 | GND | `GND` |
| 8 | SCL | `SE2_I2C_SCL` ← MCU PB6 (I2C4) + **10 kΩ** pull-up to +3V3 |
| 3 | SDA | `SE2_I2C_SDA` ← MCU PB7 (I2C4) + **10 kΩ** pull-up to +3V3 |
| 9 | RST | `SE2_RST` ← MCU PB5 (soft/hardware reset support) |
| 2,4,5,6,7 | — | no-connect |

## Rules

- **Dedicated I2C bus** (I2C4), not shared with the touch controller — keeps the
  second secure element isolated from the display bus.
- Simple integration (no hibernation MOSFET) for Rev A0; `RST` wired so firmware
  can use IFX soft reset or hardware reset.
- Pull-up value (10 kΩ per datasheet) trimmed to the chosen I2C frequency.

## ERC gate

VCC/GND/SCL/SDA/RST bound; pull-ups present; unused pins no-connect; ERC clean
before subsystem 5 (NFC).
