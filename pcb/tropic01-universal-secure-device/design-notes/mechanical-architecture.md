# Mechanical Architecture — Display-Sized Compact Device

Date: 2026-06-10
Status: design direction agreed; layout work pending.

This note records the product mechanical concept that drives PCB size, battery
placement, and the NFC/RFID antenna strategy. It supersedes the earlier
"full-size board with battery behind the whole PCB" assumption.

## Device concept

- The whole device is **as large as the 2.4" display** (EastRising
  ER-TFT024IPS-3, outline ~`42.72 mm` W × `59.46 mm` H, active `36.72 × 48.96`).
- Front face = the display.
- Behind the display, stacked side-by-side vertically:
  - **lower portion = the PCB** (electronics),
  - **upper portion = the LiPo battery**.
- The device outline is therefore the display outline; nothing sticks out beyond
  the display footprint.

## PCB sizing rule

- **Width = display width** (~`42.7 mm`, fit inside the display outline with
  case clearance).
- **Height = the minimum that still fits all components**, found by the compact
  placement pass — not a fixed number. The shorter the PCB, the more vertical
  room is left for the battery in the upper portion.
- The PCB occupies the **lower portion** of the display footprint.

### Component-side rule (important)

The PCB front faces the display, so tall components cannot sit on the front
without colliding with the panel. Electronics are placed on the **back side**
of the PCB (facing the case back), which also hosts the NFC antenna. Expect a
predominantly single-sided (back) population, which is what sets the minimum
height.

## Battery

- Single-cell LiPo, located in the **upper portion** behind the display, beside
  (above) the PCB — **not stacked on the PCB**.
- Electrically off-board: the PCB exposes **only the `J9` JST PH LiPo
  connector**; there is **no `BAT1` footprint/envelope on the PCB**.
- The BQ24074 power-path charger (`U10`) and `J9` live on the PCB; the cell
  lives in the enclosure.

## NFC / RFID antenna

Cards/tags are tapped on the **back** of the device (opposite the display).

- **Back-side loop antenna** (copper loop on the bottom layer), sized around the
  device perimeter so the tap zone covers most of the back.
- **Ground keep-out** under the loop over the PCB region (no copper pour that
  would short/detune the loop); the loop avoids dense component areas.
- **Ferrite sheet** between the loop and the battery in the upper portion: a bare
  LiPo would shield/detune the 13.56 MHz field; the ferrite isolates it and
  redirects the field outward. Adds one ferrite item to the BOM.
- **Matching network near `U9`** (ST25R3916B), per ST AN5276.
- **First-article RF tuning is a hard gate** — antenna and matching values are
  not final until measured with the real loop, battery, and enclosure.

## Controls

- **One physical button** (`SW1`, side-actuated) plus the capacitive touch panel
  is sufficient for approve/reject; the second button `SW2` is dropped.

## Display

- Single **50-pin 0.5 mm FFC** (`J2`) carrying display SPI + capacitive touch
  I2C; the separate touch connector `J2B` is removed. (Schematic intent already
  reflects this; the PCB footprint swap is pending.)

## Sizing result (measured from the adopted board B)

The adopted board B already realises the compact concept. Measured PCB outline:

- **`44.1 mm` wide × `36.1 mm` tall** (the existing component placement fits this
  on one main side), vs the display outline `42.72 × 59.46 mm`.
- **Board height ≈ `36 mm`** answers "how tall must the board be": it fits the
  full component set (STM32U585 LQFP100, both secure elements, NFC controller,
  QSPI flash, BQ24074 charger, regulators, 50-pin display FFC, USB-C, JST
  connectors, single button, mounting holes, ~40 passives).
- That leaves **≈ `23 mm`** of the `59.46 mm` display height **above the board for
  the battery** — enough for a small LiPo beside the PCB. The side-by-side
  arrangement therefore works without stacking the battery behind the PCB.

Minor follow-up: the width can be trimmed from `44.1 mm` to ≈ the display width
`42.72 mm` (move `SW1` slightly inward first, since it sits near the right edge).

## Status (2026-06-10)

Done automatically via the KiCad `pcbnew` Python module on the adopted board B:

- ✅ Display `J2` swapped to the single 50-pin FFC; `J2B` removed; display SPI +
  touch I2C nets assigned to the new `J2`.
- ✅ Battery off-board: `BAT1` removed, only `J9` kept.
- ✅ Single button: `SW2` dropped across board, BOM, validator, schematic, and
  placement.
- ✅ Compact size confirmed: `44.1 × 36.1 mm`, ~23 mm left for the battery.

## Remaining work (engineering / measurement gates)

1. **NFC/RFID RF front-end — not yet designed.** Today `U9` (ST25R3916B)
   antenna/RF pins, the matching network (`L30`, `L31`, `C30`–`C33`), and the
   `ANT1` keep-out are **all unconnected**. This requires a real RF front-end per
   ST AN5276: `U9` RFO1/RFO2 → EMC filter (L0/C0) → matching (series Cs +
   parallel Cp) → the back-side loop → RFI1/RFI2, with the loop placed top-center
   on the back and a ferrite over the battery region. The **topology** is
   deterministic; the **component values and final loop geometry are tuning-gated
   on the first article** (cannot be finalised without measurement).
2. **Routing** — no copper tracks/zones yet; needs routing (manual or an external
   autorouter such as Freerouting; KiCad 10 has no built-in autorouter).
3. **ERC/DRC** clean, then the PCBWay release gate.
4. Minor: trim board width to `42.72 mm`; reposition `ANT1` keep-out onto the
   board top-center (back side); swap the `DISP1` envelope to the ER-TFT024IPS-3
   outline (cosmetic).
