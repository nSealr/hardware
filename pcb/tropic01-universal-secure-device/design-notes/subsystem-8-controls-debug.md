# Subsystem 8 — Controls, status, debug, expansion design

Date: 2026-06-10
Status: design captured. Clean rebuild. Final subsystem.

## SW1 — single side button

- `SW1` (EVQP7C side-actuated): one terminal → `BTN_USER` (MCU PE2, EXTI, with
  internal pull-up enabled in firmware), other → `GND`. Optional 100 nF debounce.
- One button + the capacitive touch panel form the approve/reject boundary.

## Status LED

- `LED1` (side-view) anode → `+3V3` (or a GPIO), cathode → `RLED1` series
  resistor → `LED_STATUS` (MCU PE3). Size `RLED1` for ~2-5 mA (e.g. 330-1 kΩ).

## Test pads (hidden, electronics side)

Pads only, no headers: `TP_SWDIO` (PA13), `TP_SWCLK` (PA14), `TP_NRST`,
`TP_BOOT0` (PH3), `TP_UART_TX` (PD5), `TP_UART_RX` (PD6), `TP_3V3`, `TP_GND`.
Firmware locks SWD before any production security claim.

## J6 — Qwiic/STEMMA QT expansion

`J6` (JST SM04B-SRSS-TB, 4-pin): `GND`, `+3V3`, `EXP_I2C_SDA`, `EXP_I2C_SCL`.
Bus assignment (which STM32 I2C, and pull-ups) is the one remaining
expansion-policy decision; keep it off the touch and OPTIGA buses. Cable exits
toward the upper service area, away from the USB/screw zone.

## ERC gate

SW1/LED/test-pad/J6 nets bound; pull-ups/series resistors present; ERC clean.
This completes the subsystem set — then the whole-board ERC, placement (rebuilt
connectivity-driven), 4-layer routing, DRC, and the PCBWay package.
