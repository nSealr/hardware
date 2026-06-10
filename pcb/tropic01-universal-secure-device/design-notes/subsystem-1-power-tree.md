# Subsystem 1 — Power Tree (datasheet-verified design)

Date: 2026-06-10
Status: design complete (pinouts verified from local datasheets); ready to
implement in the schematic binding. Part of the clean rebuild.

Topology: `USB-C VBUS → BQ24074 (charger + power path) → SYS → TPS62840 buck →
+3V3 → TPS22917 load switch → +3V3_TROPIC_SW`. Battery on `BAT`/`J9`.

## Rails

- `VBUS` (USB 5 V input), `VSYS` (BQ24074 OUT, power-path system rail),
  `VBAT` (battery), `+3V3` (main logic), `+3V3_TROPIC_SW` (switched secure rail),
  `GND`.
- PWR_FLAG on `VBUS` and `VBAT` (externally sourced); `+3V3`/`+3V3_TROPIC_SW`
  are driven by the regulator/switch output pins.

## J1 — USB4105-GF-A (USB-C 2.0, sink)

- `VBUS` (A4/A9/B4/B9) → `VBUS`; `GND` (A1/A12/B1/B12) + shield → `GND`.
- `CC1` (A5) → `USB_CC1` via 5.1 kΩ to GND (Rd, UFP/sink); `CC2` (B5) → 5.1 kΩ to GND.
- `D+` (A6/B6) → `USB_DP_CONN`; `D-` (A7/B7) → `USB_DM_CONN` → USB ESD array → `USB_DP`/`USB_DM` to the MCU.

## U10 — BQ24074 (RGT0016B, VQFN-16) — verified pinout

| Pin | Name | Connection |
| ---: | --- | --- |
| 1 | TS | thermistor network; if no NTC, 10 kΩ to GND + 10 kΩ to VBAT (TS-disable, keep in valid range) |
| 2,3 | BAT | `VBAT` (to J9) + 4.7 µF to GND |
| 4 | CE | enable charge: tie GND (or MCU GPIO) |
| 5 | EN2 | input-current mode select (with EN1) — set for USB 500 mA |
| 6 | EN1 | input-current mode select |
| 7 | PGOOD | open-drain; 100 kΩ pull-up to +3V3 (optional → MCU `PWR_PGOOD`) |
| 8 | VSS | `GND` |
| 9 | CHG | open-drain charge status; 100 kΩ pull-up to +3V3 (optional → MCU/LED) |
| 10,11 | OUT | `VSYS` + 4.7 µF to GND |
| 12 | ILIM | `R_ILIM` to GND — input current limit (KILIM≈1600; ~3.3 kΩ ≈ 500 mA) |
| 13 | IN | `VBUS` + 1 µF to GND |
| 14 | TMR | safety-timer cap to GND (or GND to disable) |
| 15 | ITERM | `R_ITERM` to GND — termination current |
| 16 | ISET | `R_ISET` to GND — fast-charge current (KSET≈890; e.g. 2.2 kΩ ≈ 400 mA) `tuning: per battery` |
| EP | thermal | `GND` |

`R_ISET`, `R_ILIM`, `R_ITERM` final values depend on the chosen LiPo capacity.

## U3 — TPS62840 (DLC, SON-8) — 3.3 V buck — verified pinout

| Pin | Name | Connection |
| ---: | --- | --- |
| 1 | GND | `GND` (+ EP) |
| 2 | VIN | `VSYS` + 10 µF to GND |
| 3 | MODE | tie low (forced PWM) or high (auto power-save) — choose for efficiency |
| 4 | EN | enable: tie VIN (always-on) or MCU GPIO |
| 5 | VSET | output-set resistor for **3.3 V** per the TPS62840 VSET table |
| 6 | STOP | output discharge control |
| 7 | SW | `L1` 2.2 µH to `+3V3` |
| 8 | VOS | `+3V3` (output sense) + 10 µF to GND |

## U4 — TPS22917 (DBV, SOT-23-6) — TROPIC01 load switch — verified pinout

| Pin | Name | Connection |
| ---: | --- | --- |
| 1 | VIN | `+3V3` |
| 2 | GND | `GND` |
| 3 | ON | `TROPIC_PWR_EN` (MCU GPIO, active-high) |
| 4 | CT | optional slew cap to VIN (or float) |
| 5 | QOD | quick output discharge (per datasheet) |
| 6 | VOUT | `+3V3_TROPIC_SW` + 1 µF to GND |

## Decoupling policy

- Every IC power pin: 100 nF local; bulk per rail (10 µF on +3V3, 4.7 µF on
  VSYS/VBAT, 1 µF on +3V3_TROPIC_SW).
- The load-switch lets firmware power-cycle TROPIC01 (its Rev A0 reset method).

## ERC gate for this subsystem

Every pin above bound (signal, rail, or explicit no-connect); PWR_FLAG on VBUS
and VBAT; pull-ups present; then KiCad ERC clean for the power sheet before
moving to subsystem 2 (STM32U585).
