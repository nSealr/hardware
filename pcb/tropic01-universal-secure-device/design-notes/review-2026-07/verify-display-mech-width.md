# Adversarial verification — finding "display-mech: board already meets 42.72mm HARD width"

Verdict: **CONFIRMED** (with minor numeric corrections that do not affect the conclusion).

## Claim under test

The board bbox 42.87 x 39.95 mm is inflated by the 0.15mm Edge.Cuts stroke; the Edge.Cuts
centerlines span exactly 42.72 x 39.80 mm, fabs cut on the centerline, therefore the HARD
width constraint is already met and the board must NOT be resized.

## Evidence 1 — raw .kicad_pcb Edge.Cuts geometry (primary source)

File: `/Users/vincenzo/Documents/GitHub/nSealr/hardware/pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_pcb`
(exactly 8 Edge.Cuts graphics, lines ~20965-21055; no footprint-embedded edge items — grep for
`(layer "Edge.Cuts")` returns only these 8 plus the layer definition):

- `gr_line (start 10.64 68.3) (end 10.64 33.5)` — left edge x = 10.64
- `gr_line (start 53.36 33.5) (end 53.36 68.3)` — right edge x = 53.36
- `gr_line (start 13.14 31) (end 50.86 31)` — top edge y = 31.0
- `gr_line (start 50.86 70.8) (end 13.14 70.8)` — bottom edge y = 70.8
- 4 corner `gr_arc`s, all verified R = 2.500 mm (e.g. start (10.64,33.5) mid (11.372233,31.732233) end (13.14,31) → center (13.14,33.5), r=2.5)
- every element: `(stroke (width 0.15))`

Centerline extents: 53.36 − 10.64 = **42.72 mm exactly**; 70.8 − 31.0 = **39.80 mm**.
Bbox with stroke: 42.72+0.15 = 42.87; 39.80+0.15 = 39.95 — matches the "measured" 42.87 x 39.95
and board-truth.json `origin (10.565, 30.925)` = (10.64−0.075, 31.0−0.075). The 42.87 figure is
therefore a stroke-inflated bounding box, not the physical board size.

## Evidence 2 — empirical Gerber profile export

Ran `kicad-cli pcb export gerbers --layers Edge.Cuts` (KiCad 10.0.3) on the actual board.
Output `tropic01-universal-secure-device-Edge_Cuts.gm1`:

- `%TF.FileFunction,Profile,NP*%` (official Gerber X2 board-profile attribute)
- Aperture `%ADD10C,0.150000*%` (0.15mm circle — thin, unambiguous)
- Draw coordinates are exactly the centerlines: `X10640000` (10.64), `X53360000` (53.36),
  `Y-31000000` (31.0), `Y-70800000` (70.8), arcs `I/J 2500000` (R2.5).

So the fab-facing profile spans 42.72 x 39.80 mm centerline-to-centerline.

## Evidence 3 — fab practice (PCBWay, the project's actual fab per production/pcbway-manifest.json)

PCBWay Help Center, "The outline of shape is too thick to ensure the dimension of PCB"
(https://www.pcbway.com/helpcenter/board_outline_issues/The_outline_of_shape_is_too_thick_to_ensure_the_dimension_of_PCB.html):
board dimension is measured from the **middle of the outline line**; a thin outline stroke is
recommended (0.15mm qualifies). The finished board will measure 42.72 mm ± routing tolerance
(PCBWay standard ±0.2 mm) — shrinking the outline by 0.075/side, as a naive "fix the bbox"
change would do, would produce a nominally 42.57 mm board, i.e. undersized vs the display.

## Evidence 4 — display datasheet supports the ±0.2 note in the recommendation

ER-TFT024IPS-3 datasheet (scratchpad copy `er-tft024ips-3-archive.pdf`, mechanical drawing):
"BL 42.72±0.2", "RTP 59.26±0.2", "BL/CTP 59.26±0.2". So the display module itself is only
controlled to ±0.2 mm — same order as PCB routing tolerance — which supports the recommendation
that the enclosure must locate the display, not the board edge.

## Evidence 5 — edge-adjacent component spot checks (all from the .kicad_pcb)

- **J1** USB4105 at (32, 66.2) rot 0: TH shield pads at local (±4.13, −3.11) and (±4.49, +2.84)
  → southernmost SH pad centers y = 69.04, i.e. 1.76 mm inboard of the centerline bottom edge
  y=70.8. NPTH posts at local y = −4.36 → y = 61.84. Matches the finding.
- **SW1** value `EVQP7J01P` at (52, 52) rot 90 (Panasonic side-actuated): F.CrtYd extends to
  x = 53.65 (+0.29 mm past the centerline edge); F.Fab (body+actuator drawing) to x = 53.40
  (+0.04 mm). The finding said "0.32 mm actuator overhang" — same direction and order of
  magnitude (exact value depends on whether courtyard or datasheet actuator tip is used);
  the overhang is small and intentional for a side-actuated button. Not a refutation.
- **MH1-4** NPTH drill 2.2 mm at (13.1, 33.6)/(50.9, 33.6)/(13.1, 68.4)/(50.9, 68.4), corner
  arc centers (13.14, 33.5) etc., R2.5. Lateral hole-wall-to-edge web = 13.1 − 1.1 − 10.64 =
  **1.36 mm** (as claimed). Minor correction: the true minimum web is **1.30 mm** — MH1/MH2
  hole wall to the bottom edge (70.8 − 68.4 − 1.1). Top holes have 1.50 mm vertically. All
  ≥1.0 mm, acceptable for 2.2 mm NPTH.

## Refutation attempts that failed

1. "Maybe the profile Gerber is plotted on the stroke outer edge" — refuted empirically: the
   exported Gerber draws are at the centerline coordinates.
2. "Maybe other Edge.Cuts items enlarge the extents" — refuted: only 8 edge items exist.
3. "Maybe the physical board is measured over the stroke" — refuted by PCBWay's stated policy
   (middle of the line) and by the Gerber X2 Profile semantics.

## Corrected recommendation (refinement, not reversal)

Do NOT resize the width — confirmed. Refinements:
1. Update docs/validators to record the board as **42.72 x 39.80 mm (Edge.Cuts centerline)**;
   fix any validator that measures the stroke-inflated bbox — it must measure centerline
   extents (or subtract one stroke width). Battery zone above the board is then
   59.26 − 39.80 = **19.46 mm**, not 19.31.
2. Keep the 0.15 mm Edge.Cuts stroke (PCBWay-compliant, unambiguous); optionally add the
   intended finished dimensions to the fab order notes as PCBWay suggests.
3. Note in mechanical-architecture.md that both the PCB (routing ±0.2) and the display
   (BL 42.72±0.2 per ER-TFT024IPS-3 drawing) carry ±0.2 mm tolerances, so the enclosure must
   datum on the display module, not the board edge.
4. Record the true minimum mounting-hole web as 1.30 mm (MH1/MH2 to bottom edge), not 1.36.
