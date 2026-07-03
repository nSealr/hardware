# Adversarial verification — finding "nfc-antenna" (42x8 mm envelope impossible)

Date: 2026-07-03
Verdict: **CONFIRMED** (and the situation is worse than the finding states; recommendation needs correction)

## 1. What the finding claims

The declared 42x8 mm NFC antenna envelope (ANT1 @ (32,33), top-center) is physically
impossible with the current top-strip floorplan, blocked by J9, J6, MH3/MH4 courtyards
and interior passives/testpoints.

## 2. Primary-source verification of every cited number

All courtyards below were recomputed **directly from the .kicad_pcb footprint blocks**
(`/Users/vincenzo/Documents/GitHub/nSealr/hardware/pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_pcb`),
including rotation, not from board-truth.json.

| Ref | Claimed | Measured (F.CrtYd, world coords) | Match |
|---|---|---|---|
| J9 S2B-PH-SM4-TB @(44,37.5) rot180 | y to 32.4, x 39.4–48.6 | x[39.40,48.60] y[32.40,42.60] | exact |
| J6 SM04B-SRSS-TB @(19,36.5) rot180 | y to 33.2, x 15.1–22.9 | x[15.10,22.90] y[33.22,39.78] | exact |
| MH3 @(13.1,33.6) | corner to x=14.7, y 32.0–35.2 | circle r=1.55 → x[11.55,14.65] y[32.05,35.15] | exact |
| MH4 @(50.9,33.6) | corner to x=49.3 | x[49.35,52.45] y[32.05,35.15] | exact |
| TP_UART_GND @(25,35) | inside band | circle r=1.0 → x[24,26] y[34,36] | yes |
| C1 0603 @(28,35.5) | inside band | y[34.77,36.23] | yes |
| C40 0402 @(38,36) | inside band | y[35.54,36.46] | yes |
| C31 0402 @(32,32) | inside band | y[31.54,32.46] | yes |
| C33 0402 @(32,34) | inside band | y[33.54,34.46] | yes |
| C34/C36/C39/R19 @(50/38/35.5/33, 37.5) | boundary y37–38 | y[37.03,37.99] | yes |

Visual confirmation: `scratchpad/pcb-review/crop-topstrip.png` / `render-top.png` show
J6, J9, both M2 corner holes, TP_UART_GND, the TC2030 pad field (J7), JP1 and the 0402s
fully occupying the strip. No clear 42x8 band exists.

## 3. The envelope requirement is real (not a stale note)

- ANT1 footprint in the .kicad_pcb itself: `(descr "Centered upper 13.56 MHz NFC antenna
  keepout/envelope; documented envelope 42.00 x 8.00 mm")`. The footprint is an **empty
  placeholder** — no pads, no courtyard, no graphics — so DRC=0 proves nothing here.
- `design-notes/mechanical-architecture.md` (user-confirmed HARD): "Loop antenna (copper
  loop) at the top-center of the component side, with a ground keep-out under the loop
  (no pour that would detune it)". Its ASCII floorplan (lines 56–63) draws
  `[ ANT1 NFC ]` as its own row along the top edge with J6/J9 on the row **below** it —
  i.e. the spec itself intends the band to be clear of J6/J9.
- `design-notes/nfc-rf-frontend.md` (line 61): "**Ground keep-out** under the loop on
  all copper layers (no pour inside/below the loop)". (Note: this note says *back-side*
  loop while mechanical-architecture.md says *component-side F.Cu* loop — a contradiction
  to resolve, but irrelevant to the collision: the keep-out spans all layers and the M2
  holes are through-holes.)
- ST **AN5276 Rev 6**, §5.1 (p.20/44, local text extract `pcb-review/an-antenna.txt`):
  "The best case of an antenna placement is far away from electronics or other
  components like batteries, displays, or large ground planes that harm the effective
  radiated RF field."

## 4. Facts the finding missed — the conflict is HARDER than claimed

1. **The envelope as placed does not even fit on the board.** 42x8 centered at (32,33)
   spans y[29.0,37.0]; the top board edge is y=30.925 → the envelope extends **1.925 mm
   off-board**. Flush to the top edge it would occupy y[30.925,38.925].
2. **The 42 mm width is unachievable under ANY re-floorplan.** MH3/MH4 are HARD
   (mechanical spec: M2 hole in each R2.5 corner fillet, immovable). Their courtyards
   leave only x[14.65,49.35] = **34.7 mm** between them at y[32.05,35.15]; the gap
   between MH3 courtyard and the left board edge is 0.985 mm — unroutable for a 1–3 turn
   loop. So the *documented* 42 mm envelope can never be honored on-board; the true
   achievable on-board loop is ~33–34 mm wide (or its side legs must duck below y≈35.4).
3. **All three GND pours currently cover the antenna band.** Zones at pcb lines 29489
   (F.Cu), 32072 (B.Cu), 32799 (In1.Cu), each with outline x[11.2,52.8] y[31.6,70.2].
   No antenna keep-out rule area exists (the only F.Cu keepout is x[26.7,29.3]
   y[37.9,39.1], unrelated). This directly violates nfc-rf-frontend.md line 61 and
   AN5276 §5.1 the moment a loop is drawn.
4. **C31/C33 placement note:** per nfc-rf-frontend.md, C30–C33 are the EMC/matching
   caps that belong in the matching block near U9 (mechanical-architecture.md line 80:
   "Matching network near U9 … per ST AN5276"); their current parking at (32,32)/(32,34)
   inside the keep-out band contradicts both notes. As shunt caps they would drag GND
   copper into the loop interior.

## 5. Recommendation audit

The original recommendation is directionally right but numerically insufficient:

- "move J6/J9 down to y>=40": with J6 CrtYd half-height 3.28 mm and J9's 5.10 mm,
  clearing a band ending at y=38.6 requires **J6 center y ≥ 41.9** and **J9 center
  y ≥ 43.7** — which collides with the U11 OPTIGA (14.5,43) and U10 BQ24074 (48,45.12)
  neighborhoods. "y>=40" as written still leaves both courtyards inside the band.
- It does not mention that the **42 mm width is dead on arrival** because of the fixed
  corner holes (see §4.2) — clearing components is not enough; the envelope itself must
  be re-documented (~34 x 7 mm usable, x≈[15.2,48.8], y≈[31.5,38.5]) or moved off-board.
- It does not mention the **GND pour redraw + all-layer keep-out rule area**, which is a
  required part of the fix (§4.3).
- The Trezor fallback is validated: trezor-hardware clone,
  `electronics/trezor_safe_7/` contains a dedicated **ANT FPC**
  (`ts7_fpc_ant_rev_d_sch.pdf` / `_views.pdf`; README lists "ANT FPC"), and the TS7
  main-board schematic exposes an `NFC_COIL`/`COIL` interface to the ST25R3916-class
  NFC block (`ts7_main.txt` lines 61–69). So a dedicated antenna FPC on the back cover
  fed from NFC_ANT1/2 is a proven pattern for exactly this chip family and form factor.

## 6. Verdict

**CONFIRMED.** Every geometric fact in the finding checks out against the .kicad_pcb
primary source; the requirement (keep-out envelope) is confirmed by the footprint
description, both design notes, and AN5276 §5.1. Additional evidence (envelope
overhanging the board edge, 34.7 mm max width between fixed M2 courtyards, GND pours
covering the band on F/In1/B) makes the finding stronger than stated. The recommendation
needs the corrections in §5.
