# Mechanical Architecture — AUTHORITATIVE SPEC (hard constraints)

Date: 2026-06-11 (re-confirmed with the user; supersedes the 2026-06-10
"44.1 × 36" measured-board notes and the earlier enlargement to 44 × 42).
**These constraints are fixed — every placement/floorplan must respect them.**

## Display (chosen + confirmed from datasheet)

- **ER-TFT024IPS-3** (EastRising / BuyDisplay): 2.4" **IPS** TFT-LCD, 240×320,
  ST7789V controller, **FT6336 capacitive touch**.
- Single **50-pin 0.5 mm FPC**, SMD horizontal, **top-contact** (our connector
  `J2`, ER-CON50HT-1 / Hirose FH12-50S-0.5SH class).
- **Outline with FPC folded: 42.72 × 59.26 mm.** Active area 36.72 × 48.96 mm.
- **The FPC tail exits the BOTTOM edge of the display** and folds 180° behind to
  plug into `J2` (verified from the datasheet outline drawing, page 6).
- User criteria: 2.4", single connector, capacitive touch, LCD, good quality —
  this part satisfies all of them.

## Board size (HARD)

- **Width = display width = 42.72 mm.** The board must NOT exceed the display width
  (HARD). 
- **Board height = 36.8 mm** (the LOWER portion behind the display). Was ≈36; the
  bottom edge was extended +0.8 mm so the USB-C front through-hole shield posts sit
  fully on-board (a USB-C is 11.7 mm deep and must overhang the edge, but its front
  mounting-post holes must not break the edge). Height is "≈36" / soft; width is the
  hard dimension.
- **Board + battery ≤ display height (59.26 mm)** → ~**22.5 mm** above the board (same
  display outline) is the battery space (0.5 mm less than before, still ample for the
  off-board LiPo).
- Same rectangular shape as the display; nothing sticks out beyond the display.

## Two-sided stack (HARD)

The display lays FLAT against one PCB face:

- **Component side = F.Cu**: ALL ICs, passives, connectors (USB-C, button,
  J6/J9) and the NFC antenna go here. This is the case-back / inside of the device.
- **Display side = B.Cu**: the display rests flat here — it must be CLEAR of
  components, carrying **only `J2`** (the display FFC connector) + the display
  outline. No other parts on this face.

## Corners + mounting holes (HARD)

- **All 4 corners are rounded, R = 2.5 mm** (fillet, not a straight chamfer — the
  fillet keeps the corner screw clear of the edge).
- **One M2 (Ø2.2) mounting hole at each corner** (`MH1`–`MH4`, 4 total), each
  seated at the centre of its corner fillet (~1.3 mm edge clearance).
- **Consequence (HARD):** the two top connectors `J6`/`J9` must sit **INBOARD**,
  off the edge/corner — never on a corner — so the fillet doesn't cut them and the
  corner holes fit.

## Perimeter placement (HARD)

```
              ▲ TOP (battery space + NFC tap on the back)
   ╭··MH··───────[ ANT1 NFC ]──────────MH··╮   J6/J9 = 2 connectors near the TOP,
   │   [J6]                          [J9]   │   pulled INBOARD (NOT on the corners),
   │        ICs / passives          [SW1]   │   mouths facing OUT/up. J6=expansion,
   │      (component side, F.Cu)            │   J9=battery. ANT1 = NFC antenna
   │                                        │   CENTER-TOP. SW1 = button CENTER-RIGHT.
   ╰··MH··───────[ USB-C J1 ]──────────MH··╯   J1 = USB-C CENTER-BOTTOM. ·MH· = the 4
   │←────────── 42.72 mm (= display) ───────→│  corner M2 holes; corners rounded R2.5.
   - J2 (display FFC) on B.Cu, BOTTOM-CENTER, mouth toward the bottom edge
     (the display cable folds up from the bottom edge into it). The USB-C does
     NOT obstruct the cable (display lays over the components; cable passes by).
```

STM32 at the center is convenient but NOT a hard constraint — internal placement
is free as long as the perimeter constraints above hold.

## NFC / RFID antenna

Cards/tags are tapped on the **back** of the device (component side, F.Cu).

- **Loop antenna** (copper loop) at the **top-center** of the component side,
  with a ground keep-out under the loop (no pour that would detune it).
- **Ferrite sheet** between the loop and the battery (a bare LiPo shields/detunes
  the 13.56 MHz field). Adds one ferrite item to the BOM.
- **Matching network near `U9`** (ST25R3916B) per ST AN5276: RFO1/RFO2 → EMC
  filter → matching → loop → RFI1/RFI2.
- `L30/L31/C30–C33` (`NFC_TUNE`) + `ANT1` are placeholders kept clustered near `U9`.
- **First-article RF tuning is a HARD gate** — antenna + matching values are not
  final until measured with the real loop, battery, and enclosure.

## Battery

- Single-cell LiPo, **off-board**: the PCB exposes only the `J9` JST connector
  (no `BAT1` footprint). Sits in the ~23 mm upper space behind the display, within
  the display outline; no thicker than the board+component stack. Pick the largest
  cell that fits that space.

## Controls

- **One physical button** (`SW1`, side-actuated, center-right) + the capacitive
  touch panel = approve/reject. No second button.

## Layers

- **4-layer stackup** (chosen for cost; 4 routes as well as 6 here — the
  bottleneck is fine-pitch IC pin-escape congestion, not layer count):
  **F.Cu (signal) / In1 = GND plane / In2 (signal) / B.Cu (signal)**.
- Via 0.4 mm / drill 0.2 mm (min relaxed in the project `.kicad_pro`).
- Priority order: (1) respect all the constraints above, (2) smallest size,
  (3) tidiest layout. Do NOT trade size for routability.

## Status (2026-06-15)

- ✅ Board is **42.72 × 36 mm**, all perimeter constraints met, components on
  F.Cu, only `J2` on B.Cu (display side), **0 courtyard/clearance overlaps**.
- ✅ **Corners rounded R=2.5 mm + 4 M2 corner holes (`MH1`–`MH4`)** seated in the
  fillets; top connectors `J6`/`J9` inboard so nothing is clipped.
- ✅ Secure SPI short (TROPIC adjacent to STM32, ~2.4 mm); decoupling/CT caps
  adjacent to their ICs; RGB status LED (top-emitting); dev-access features
  (SWD TC2030, BOOT0 jumper, UART group, current-sense 0R jumpers).
- ⏳ Routing: GND poured as a plane; auto-router plateaus at ~17 signal nets →
  needs the interactive push-and-shove router for the final connections.
- ⏳ NFC RF front-end: tuning-gated (values not final until measured).
