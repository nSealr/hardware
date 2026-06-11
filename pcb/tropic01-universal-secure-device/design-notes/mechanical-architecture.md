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

- **Width = display width = 42.72 mm.** The board must NOT exceed the display width.
- **Board height ≈ 36 mm** (the LOWER portion behind the display).
- **Board + battery ≤ display height (59.26 mm)** → ~**23 mm** above the board (same
  display outline) is the battery space.
- Same rectangular shape as the display; nothing sticks out beyond the display.

## Two-sided stack (HARD)

The display lays FLAT against one PCB face:

- **Component side = F.Cu**: ALL ICs, passives, connectors (USB-C, button,
  J6/J9) and the NFC antenna go here. This is the case-back / inside of the device.
- **Display side = B.Cu**: the display rests flat here — it must be CLEAR of
  components, carrying **only `J2`** (the display FFC connector) + the display
  outline. No other parts on this face.

## Perimeter placement (HARD)

```
              ▲ TOP (battery space + NFC tap on the back)
   ┌─[J6]────────[ ANT1 NFC ]────────[J9]─┐   J6/J9 = 2 connectors at the TOP
   │ corner        center-top      corner  │   CORNERS, mouths facing OUT (up).
   │                                        │   J6=expansion, J9=battery
   │        ICs / passives          [SW1]   │   (interchangeable). ANT1 = NFC
   │      (component side, F.Cu)            │   antenna CENTER-TOP. SW1 = button
   │   ·MH·         [ USB-C J1 ]      ·MH·  │   CENTER-RIGHT. J1 = USB-C
   └────────────────────────────────────────┘   CENTER-BOTTOM. ·MH· = M2 holes.
   │←────────── 42.72 mm (= display) ───────→│
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

- **Layer count is NOT a priority.** Use whatever routes well (6-layer baseline,
  more if needed). Priority order: (1) respect all the constraints above,
  (2) smallest size, (3) tidiest layout. Do NOT trade size for routability.

## Status (2026-06-11)

- ✅ New floorplan built to this spec: **42.87 × 36.15 mm**, ~23 mm battery space,
  all perimeter constraints met, components on F.Cu, only `J2` on B.Cu (display
  side), 0 courtyard/clearance overlaps. (In `/tmp` pending final review + commit.)
- ⏳ Pending: connector-orientation visual check, silkscreen cleanup, commit, then
  re-route on this clean compact base.
- ⏳ NFC RF front-end + routing: tuning-gated / interactive-finish (unchanged).
