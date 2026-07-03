# Adversarial verification — finding "nfc-antenna" (concrete loop spec)

Date: 2026-07-03. Verifier: independent pass against the real `.kicad_pcb`, AN5276 Rev 6 text, local design notes, and independent recomputation.

## Verdict: CONFIRMED (electrical claims verified), with mandatory corrections to the recommendation

The inductance math, the AN5276 citations, and the Q estimate all check out against primary
sources. However, the exact rectangle specified (x 15.2-48.8, y 31.6-37.6) is **not placeable
on the board as it exists today**: it has hard copper/hole collisions with J6, J9, J7,
TP_UART_GND and two parked matching caps, and the entire region is currently covered by the
solid In1.Cu GND plane, an F.Cu pour, 22 F.Cu + 7 In2.Cu track segments and 4 vias. The
recommendation also omits the all-layer copper keepout that both AN5276 practice and the
project's own design note require. These are recommendation-level defects, not claim-level
errors, hence CONFIRMED with corrected_recommendation.

## 1. Claim-by-claim verification

### 1.1 Geometry -> inductance (CLAIMED La ~373 nH) — REPRODUCED EXACTLY
- Winding bundle depth: N*w + (N-1)*g = 4*0.4 + 3*0.3 = **2.5 mm**. Outer 33.6 x 6.0 ->
  inner window 28.6 x 1.0 mm, average dims a=31.1, b=3.5 mm — matches the finding's stated
  a_avg/b_avg.
- GMD bundle radius r_eq = 0.2235*(2.5+0.035) = **0.5666 mm** — matches claimed 0.567.
- Grover single-rectangle formula L1 = (mu0/pi)[a ln(2ab/(r(a+d))) + b ln(2ab/(r(b+d))) + 2d
  - 2(a+b)] = 23.33 nH; x N^2 = **373.3 nH**. Claim "~373 nH": exact match.
- Cross-check with ST's own AN2866-style engineering formula (d_eq = 2(w+t)/pi, N^1.8):
  **445 nH**. The two classical methods bracket 373-445 nH; formula uncertainty is ~+/-20%,
  so "expect 400-480 nH with ferrite" (ferrite typically +10..25%) is internally consistent.
- Fallback claim N=5, w0.35/g0.25 -> recomputed **520.3 nH** — matches claimed "~520 nH".
  Caveat: at N=5 the inner aperture collapses to 28.1 x **0.5 mm** (bundle depth 2.75 mm),
  i.e. the coil is nearly closed; N=4 (1.0 mm aperture) is already near the geometric floor
  for a 6.0 mm-tall loop.

### 1.2 AN5276 citations — ALL CONFIRMED against the local text extract
Source: /Users/vincenzo/Downloads/nsealr-datasheets/st25r3916b-antenna-design.pdf =
**AN5276 Rev 6, May 2023** (extract: scratchpad/pcb-review/an-antenna.txt).
- Target window: "A value to be targeted in loop antenna design for NFC reader applications
  is in the **200 to 1500 nH range**. Depending on the application higher inductance values
  can be chosen and are supported by the chip." — verbatim, page break "24/44" immediately
  above, i.e. **p.24-25 as cited** (Section 5.2 "Antenna design", antenna inductance).
- Q formula: Section 4.3 computes "Q = RPANT / (omega * LANT) = 2.76 kOhm / (2 pi * 13.56
  MHz * 926 nH) = **34.8**" — the finding's Q=Rp/(2*pi*f*L) formula and its Q~35 estimate
  are exactly the app-note's own reference-antenna value.
- 926 nH example: Section 4.2, VNA marker at 1 MHz reads "LANT = 926 nH, RSDC = 394 mOhm" —
  confirmed.
- VNA procedure: Section 4.2 step 2: "The impedance curve from **1 to 300 MHz** is displayed
  in the Smith chart", antenna disconnected from matching network, reader unpowered —
  the finding's first-article measurement recommendation matches the app note.
- DISCO/886 nH at 15 Ohm: corroborated by ST moderator posts on community.st.com
  ("...translates from target matching impedance (e.g. 15 Ohm) to the antenna inductance
  (e.g. 886nH). ... explained inside the AN5592") and AN5276's ~14.4 Ohm reader-mode
  matching starting point. Supporting citation holds.

### 1.3 Rac / Q (CLAIMED Rac ~0.9 Ohm, Q_unloaded ~35) — PLAUSIBLE, minor method note
- Skin depth at 13.56 MHz: recomputed 17.92 um — matches claimed 17.9 um.
- Rdc = rho*l/(w*t) with l = 4 x 2(31.1+3.5) = 276.8 mm -> 0.34 Ohm. Skin-limited area
  2*delta*(w+t)-4*delta^2 ~ w*t at t~2*delta, so K_skin ~ 1; +15% proximity gives only
  ~0.39 Ohm, i.e. the *stated method* yields Q~64, not Q~35. The claimed 0.9 Ohm implies an
  effective proximity/loss factor ~2.3x, which is in fact the more realistic figure for a
  tight 4-turn spiral (AN5276's own 926 nH antenna measures Q=34.8 despite RSDC=394 mOhm —
  its RF loss is ~5x DC). So the *number* (Q~35) is realistic; the *stated derivation*
  (+15% proximity) is internally inconsistent but conservative in the right direction.
  Not a refutation: the deliverable value is the defensible one.

### 1.4 Layer choice (F.Cu) — CONSISTENT with device orientation
J2 (display FFC) is on B.Cu and the display outline is drawn on B.Cu, so B.Cu faces the
display = device front; **F.Cu = device back = NFC tap face**. The design note
(nfc-rf-frontend.md, "Antenna loop") says "Back-side copper loop ... top-center" meaning the
device back — which IS F.Cu. Mechanical spec also mandates all components on F.Cu. No
contradiction. Note the same design note's rough target "1-3 uH" partially exceeds AN5276's
200-1500 nH window; the finding's 400-480 nH is the better-grounded target (note is stale,
as it also still cites the old 44 x 36 mm board).

## 2. What the finding got wrong / omitted (drives the corrected recommendation)

### 2.1 Hard copper/hole collisions inside the specified rectangle (measured from .kicad_pcb)
Loop copper bands for outer 33.6 x 6.0 @ depth 2.5: top y 31.6-34.1, bottom y 35.1-37.6,
left x 15.2-17.7, right x 46.3-48.8; inner free window only x 17.7-46.3, y 34.1-35.1.
- **J9** (JST PH S2B-PH-SM4-TB @ (44,37.5) rot180): mechanical pads at x[46.60,48.10]
  y[32.90,36.30] (right MP) — sits **squarely inside the right winding band** — and
  x[39.90,41.40] y[32.90,36.30] (left MP) — cuts both top and bottom bands.
- **J6** (JST SH SM04B-SRSS-TB @ (19,36.5) rot180): MP pads x[15.60,16.80] and
  x[21.20,22.40], y[33.73,35.52] — collide with left/top/bottom bands. Its signal pads
  (y 37.73-39.27) clear the band bottom (37.6) by only 0.13 mm.
- **J7** (TC2030 @ (28,38.5)): upper pad row (pads 2/4/6, y 37.47-38.26) overlaps the bottom
  band by 0.13 mm, and the NPTH locating hole @ (30.54,37.48) (dia 0.99, y 36.99-37.98)
  **punches through the bottom band**.
- **TP_UART_GND** pad @ (25,35) (1.0 mm) overlaps the bottom band by 0.4 mm.
- **C31 @ (32,32) and C33 @ (32,34)** (NFC front-end passives, currently netless) are parked
  inside the loop area.
- Clear of collisions: MH3/MH4 NPTH holes (x<=14.20 / x>=49.80, 1.0 mm clear of the loop
  edges — the x 15.2/48.8 extents were evidently chosen for this), board edge (0.675 mm
  copper-to-edge at y 31.6), and the R2.5 corner arcs.
- Even the existing 42x8 ANT1 "envelope" (graphics-less footprint, descr "documented
  envelope 42.00 x 8.00 mm" @ (32,33), i.e. y 29-37) already overlaps J6/J9 MP pads AND
  extends 1.925 mm above the board edge — the placement violates its own keepout today.

### 2.2 Copper under the loop — the biggest omission
Point-in-polygon tests on the zone fills in the .kicad_pcb: the **In1.Cu GND plane is FILLED
at every sampled point of the proposed antenna region** ((32,32.5),(32,34),(32,36),(20,36.8),
(45,33),(17,34),(47,36),(25,32) all FILLED); the F.Cu pour covers most of it; plus 22 F.Cu
and 7 In2.Cu routed segments and 4 vias inside x 15.2-48.8 / y 31.6-37.6. A solid plane
0.2-0.4 mm below the spiral produces image currents that collapse the inductance and the
radiated H-field — the 373 nH free-space computation is only valid with a **full-stack
copper keepout** under and inside the loop. The project's own design note already mandates
this ("Ground keep-out under the loop on all copper layers", nfc-rf-frontend.md), but the
finding's deliverable spec does not mention it. B.Cu is already empty in that strip (good).

### 2.3 No feasible shrink; connectors must move
Full-width loop bottom limited by J9's MP top edge (y 32.90) would leave ~1.1 mm of height —
useless. A loop confined between the connectors (x ~23.4-38.9 -> outer ~15.5 x 5.8 mm)
cannot reach useful inductance (N=6 at w0.35/g0.25 is geometrically impossible — negative
aperture; fewer turns land near/below 200 nH with a tiny aperture). Moving J9 down by the
required ~5 mm collides with U9 (courtyard from y 44.84, J9 bbox already reaches y 42.62).
=> The antenna strip only works as part of the pending re-floorplan (move J6/J9 fully below
y ~38 and reflow J7/JP1/TP_UART_*/U9 accordingly), which the outline fix (42.87 -> 42.72
HARD) forces anyway.

### 2.4 Naming / schematic prerequisite
No `NFC_ANT*` (or any `*ANT*`) net exists in the schematic or PCB. The ST25R3916B symbol's
RF pins (RFO1/RFO2/RFI1/RFI2) are DNC in kicad/lib/symbols/TROPIC01.kicad_sym; the design
note plans net names **ANT_A/ANT_B**. The recommendation's `NFC_ANT1/NFC_ANT2` names are an
invention; the RF pins must be added to the symbol from DS13541 and the front-end (L30/L31,
C30-C33, currently netless and scattered at (40,56.5)/(45.5,56)/(40,58)/(32,32)/(51.5,55.5)/
(32,34)) wired and regrouped before the loop footprint can be netted. Exit at x~34-38 /
y~37.6 to a matching block regrouped near U9 (40.17,48) is ~10-11 mm — the <=15 mm figure is
feasible after regrouping.

## 3. Evidence index
- Board: /Users/vincenzo/Documents/GitHub/nSealr/hardware/pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_pcb
  (ANT1 footprint block; J6/J9/J7/TP pad coordinates; zone filled_polygon PIP tests; segment/via census in x 15.2-48.8, y 31.6-37.6).
- AN5276 Rev 6 (local: /Users/vincenzo/Downloads/nsealr-datasheets/st25r3916b-antenna-design.pdf):
  p.24-25 (200-1500 nH window), sec 4.2 (1-300 MHz VNA, 926 nH / 394 mOhm example), sec 4.3 (Q = RPANT/(omega L) = 34.8).
- Design note: /Users/vincenzo/Documents/GitHub/nSealr/hardware/pcb/tropic01-universal-secure-device/design-notes/nfc-rf-frontend.md
  (topology, ANT_A/ANT_B, all-layer keepout, ferrite, DNC RF pins).
- ST community (moderator): "Problem with ST25R Antenna Matching Tool" — 886 nH / 15 Ohm reference pairing, AN5592.
  https://community.st.com/t5/st25-nfc-rfid-tags-and-readers/problem-with-st25r-antenna-matching-tool/td-p/611023
- Recomputation script output (this session): 373.32 nH (N=4 bundle-GMD), 445.0 nH (AN2866 N^1.8), 520.3 nH (N=5), skin depth 17.92 um.
