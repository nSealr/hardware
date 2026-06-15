# Component Decisions (finalized)

Date: 2026-06-11
Status: all component selections delegated and made. These complete the
datasheet-driven design so the netlist/PCB build needs no further input
(except first-article NFC RF tuning, a physical measurement).

## Core (frozen)

STM32U585VIT6 · TROPIC01 TR01-C2P-T301 · OPTIGA Trust M SLS32AIA ·
ST25R3916B-AQET · W25Q128JV · USB4105-GF-A · ER-TFT024IPS-3 (50-pin FFC).

## Power

- **Battery**: LiPo **402040** (4.0×20×40 mm, 3.7 V, ~400 mAh, JST PH 2.0 → J9),
  off-board in the enclosure.
- **Charger** BQ24074: `R_ISET` 4.42 kΩ (~200 mA, 0.5C), `R_ILIM` 3.3 kΩ
  (~485 mA, USB-500), `R_ITERM` per datasheet (~40 mA). Bypass: 1 µF (IN),
  4.7 µF (OUT), 4.7 µF (BAT). PGOOD/CHG 100 kΩ pull-ups.
- **Buck** TPS62840 → +3V3: inductor **2.2 µH** (≥1 A, e.g. 0805), 10 µF in/out,
  VSET resistor for 3.3 V; EN→VIN (always-on); MODE→auto-PWS.
- **Load switch** TPS22917 → +3V3_TROPIC_SW (ON = TROPIC_PWR_EN), 1 µF out.
- A second **TPS22917** gates the NFC supply (ON = NFC_PWR_EN) → NFC_VCC_SW.

## USB

- **ESD**: USBLC6-2SC6 on D+/D- (USB_*_CONN → ESD → USB_*); CC1/CC2 5.1 kΩ to GND.

## Backlight driver (new)

- **TPS61165DBVR** (boost WLED CC driver), single output to LEDA, the four
  cathodes LEDK1-4 tied to its CC sink (~80 mA total), PWM dimming from
  TFT_BACKLIGHT_PWM. Boost L 10 µH, Schottky, 1 µF/2.2 µF out per datasheet.

## Clocks

- STM32 HSE: **16 MHz** crystal + two load caps (~8 pF, matched to CL).
- NFC: **27.12 MHz** crystal + load caps (ST reference).

## Pull-ups / passives

- Decoupling **100 nF 0402** at every IC supply pin; bulk per rail (10/4.7/1 µF).
- Touch I2C: 4.7 kΩ; OPTIGA I2C4: 10 kΩ; expansion I2C: 4.7 kΩ.
- Default passive package **0402**; power passives 0603/0805 as needed.

## Expansion

- **J6** Qwiic on a **dedicated I2C** (STM32 I2C3, isolated from touch/OPTIGA),
  4.7 kΩ pull-ups, +3V3 + GND.

## Controls

- SW1 EVQP7C side button → BTN_USER.
- **Status LED = RGB** (Broadcom **ASMB-MTB0-0A3A2**, common-anode PLCC-4, top-view).
  Common anode → **SYS_PWR_IN** (~3.5–4.4 V, so green/blue Vf ~3.0–3.2 V have headroom
  that 3V3 lacks); each colour cathode via a resistor (**RLED1 470 Ω** red, **RLED2/3
  220 Ω** green/blue) to **LED_R/LED_G/LED_B**, MCU drives active-low (sink) with PWM.
  Placed center-left (opposite SW1), top-emitting. MCU pins for LED_R/G/B are
  datasheet-pending (see `production/pinmux-ledger.json` → `rgb_status_led`).

## Stackup

- 4-layer: F.Cu signal / In1 GND plane / In2 signal / B.Cu signal.

## Developer access & reference features (2026-06-15)

To make this the definitive secure-element reference board (see
`reference-dev-access-spec.md`):

- **SWD programming:** one **Tag-Connect TC2030** footprint `J7`
  (SWDIO/SWCLK/NRST/SYS_3V3/GND) replacing the scattered SWD test pads.
- **BOOT0 / USB-DFU:** normally-open solder jumper `JP1` (BOOT0↔SYS_3V3); set it +
  power-cycle to enter the STM32U5 USB-DFU bootloader (flash with no debugger).
  `R22` 100 k holds BOOT0 low. **No RESET button** (power-cycle / SWD covers it).
- **UART console:** `TP_UART_TX/RX/GND` grouped for bring-up logs.
- **Per-rail current sense:** series 0 Ω jumpers `RJ1` (TROPIC01) and `RJ2` (NFC)
  so each secure element's supply draw is measurable.
- **One button only (`SW1`)** = user input + (firmware) power/wake.
- **Power-latch (true-off on `SW1`):** designed but **not wired** — it's the
  critical power path needing schematic-level design + bench validation; full
  reference design in `reference-dev-access-spec.md`. Board ships always-on for now.
- **Not fitted (board at capacity, display-sized):** GPIO/SPI edge breakout and a
  3rd/4th mounting hole — no contiguous space; documented as deferred.

Remaining gates: **first-article NFC antenna tuning** (matching values + loop
geometry, measured on the prototype) and the **power-latch validation** above.
