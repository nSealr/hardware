# Subsystem 2 — STM32U585VIT6 host (LQFP100) design

Date: 2026-06-10
Status: design captured. Signal assignments are source-backed in
`production/pinmux-ledger.json`; the power/clock/reset support circuit is below.
Part of the clean rebuild.

## Signal nets (authoritative source: pinmux-ledger.json)

All peripheral nets come from the verified ledger and are NOT re-invented here:
USB (PA11/PA12 + PA9 VBUS sense), TROPIC01 SPI1 (PA4-7 + PB0 PWR_EN + PB2 GPO),
display SPI3 + controls (PC10/PC12/PC7/PC8/PC6/PA8/PC9), touch I2C1
(PB8/PB9/PE1/PE0), OPTIGA I2C4 (PB6/PB7/PB5), NFC SPI2 (PB12-15 + PD0 + PB1),
QSPI/OCTOSPI (PE10-PE15), expansion UART2 (PD5/PD6), buttons/LED (PE2/PE3),
SWD (PA13/PA14), BOOT0 (PH3), NRST.

## Power architecture (STM32U5 LQFP100; exact pin numbers per DS13086 Table 27 at binding time)

- **VDD** (multiple pins): all → `+3V3`, each with a local **100 nF**; one bulk
  **4.7 µF** near the device. **VSS** (multiple) → `GND`.
- **VDDA / VSSA**: `+3V3` via a small **ferrite/0 Ω + 1 µF + 100 nF** filter to
  `VDDA`; `VSSA` → `GND`.
- **VREF+ / VREF-**: `VREF+` to `VDDA` (or its own ref) with **1 µF + 100 nF**;
  `VREF-`→`GND`. (Double-bonded with VDDA on some packages.)
- **VBAT**: tie to `+3V3` (no coin cell) with **100 nF** (or to a backup cell if
  RTC-backup is wanted).
- **VDDUSB**: USB transceiver supply → `+3V3` with **100 nF** (+ 1 µF).
- **VDD11 / SMPS pins** (STM32U5 has an internal SMPS option): for the LDO
  configuration tie per datasheet; if using the internal SMPS, add the
  `VLXSMPS` inductor + `VDDSMPS`/`VSSSMPS` caps per the reference schematic. For
  Rev A0 simplicity use the **LDO** configuration (no SMPS inductor) unless the
  power budget requires SMPS.

## Clock

- **HSE crystal**: `X1` across `OSC_IN`(PH0)/`OSC_OUT`(PH1) with two load caps
  (`C18`/`C19`, value = 2·(CL − Cstray), e.g. ~8 pF for an 8 pF-CL crystal) and a
  feedback resistor only if required by the crystal.
- LSE (32.768 kHz) optional on PC14/PC15 — omit unless RTC accuracy is needed.
- HSI/MSI internal oscillators cover the rest.

## Reset / boot / debug

- **NRST**: **100 nF** to GND (no external pull-up needed; internal present);
  expose on a test pad.
- **BOOT0** (PH3): **10 kΩ pull-down** to GND (boot from main flash) + test pad
  to force system bootloader.
- **SWD**: SWDIO (PA13) + SWCLK (PA14) to test pads; firmware locks debug before
  any production security claim.

## ERC gate

Every STM32 pin bound: signal (ledger), power rail, or explicit no-connect for
unused GPIOs; decoupling present on every supply pin; HSE + load caps; then ERC
clean for the MCU sheet before subsystem 3 (TROPIC01).
