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

## Sizing reality / open tension (must resolve before layout)

A first-order check at width ≈ `42.7 mm`, components on the back side only:

- The dominant blocks are the STM32U585 **LQFP100** (~`16 × 16 mm` courtyard) and
  the **50-pin display FFC** connector (~`28 mm` wide), plus USB-C, the two
  secure elements, the NFC controller, the QSPI flash, the BQ24074 charger, the
  regulators, the matching/charger inductors, two JST connectors, the button,
  and ~40-50 passives.
- Rough packed area for that set is on the order of `1800-2200 mm²` including
  courtyards, routing channels, and the NFC keep-out.
- At ~`39-40 mm` usable width that implies a board **height around `45-55 mm`**.

The display is only `59.46 mm` tall, so a `~50 mm` PCB would leave only
`~5-15 mm` above it — **not enough for a meaningful LiPo beside the board**.

So the "PCB in the lower portion, battery in the upper portion, both inside the
display footprint" arrangement does **not** comfortably fit this component set.
Ways to resolve, to decide before layout:

1. **Battery behind the PCB** (stacked in Z), PCB display-sized: simplest area
   fit, slightly thicker device. This is the most realistic default.
2. **Shrink the MCU** to a smaller STM32U5 package (LQFP64 or BGA) and pick
   denser parts to cut board area so a short PCB + side battery fits.
3. **Let the device be a bit taller than the display** (PCB extends past the
   display chin) to keep the side-by-side battery.
4. Some mix (e.g., smaller MCU + battery partly behind).

## Open layout work (gates)

1. **Compact placement pass**: place all back-side components at width ≈
   `42.7 mm` to find the minimum board height, then set the Edge.Cuts to that
   height and record how much vertical space remains for the battery.
2. Swap the `J2` PCB footprint to the 50-pin FFC and remove `J2B`.
3. Remove the `BAT1` on-board envelope; keep `J9`.
4. Draw the back-side NFC loop + ground keep-out + ferrite zone; place the
   matching network at `U9`.
5. Route, DRC, and first-article NFC tuning.
