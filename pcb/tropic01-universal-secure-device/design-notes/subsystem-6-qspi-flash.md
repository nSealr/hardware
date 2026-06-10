# Subsystem 6 — W25Q128JV QSPI NOR flash (SOIC-8) design

Date: 2026-06-10
Status: design captured (standard W25Qxx SOIC-8 pinout; OCTOSPI mapping from the
pinmux ledger). Clean rebuild.

## Pinout and connections (to STM32 OCTOSPI1)

| Pin | Name | Connection |
| ---: | --- | --- |
| 1 | /CS | `QSPI_NCS` ← MCU PE11 |
| 2 | DO / IO1 | `QSPI_IO1` ↔ MCU PE13 |
| 3 | /WP / IO2 | `QSPI_IO2` ↔ MCU PE14 |
| 4 | GND | `GND` |
| 5 | DI / IO0 | `QSPI_IO0` ↔ MCU PE12 |
| 6 | CLK | `QSPI_CLK` ← MCU PE10 |
| 7 | /HOLD / IO3 | `QSPI_IO3` ↔ MCU PE15 |
| 8 | VCC | `+3V3` + 100 nF |

## Rules

- Quad mode: IO0-IO3 plus CLK + /CS; /WP and /HOLD are reused as IO2/IO3 in quad
  mode (do not also pull them, the controller drives them).
- 100 nF decoupling at VCC; keep CLK short and away from the NFC loop.
- QSPI NOR is **not** secure storage by itself — secrets stay in TROPIC01/OPTIGA;
  flash holds firmware/assets with integrity protection from the host.

## ERC gate

All 8 pins bound; decoupling present; ERC clean before subsystem 7 (display).
