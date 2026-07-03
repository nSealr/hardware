# Mechanical / Display Integration Review — tropic01-universal-secure-device

Date: 2026-07-03. Reviewer scope: ER-TFT024IPS-3 datasheet verification, J2 (display FFC)
position/orientation/part, board outline vs HARD width, DISP1 envelope, battery zone.

Board: `/Users/vincenzo/Documents/GitHub/nSealr/hardware/pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_pcb`
Datasheet: `er-tft024ips-3-archive.pdf` (EastRising ER-TFT024IPS-3_Datasheet rev 1.0, Feb-22-2022, 24 pp) — verified page by page.
Connector catalog: Hirose FH12 series catalog 2017.1 (`fh12-full.pdf`, 20 pp).

Board coordinate convention: KiCad front view (looking at F.Cu), +y down.
Outline centerlines: left x=10.64, right x=53.36, top y=31.0, bottom y=70.8 (Edge.Cuts stroke 0.15 mm).

---

## 1. ER-TFT024IPS-3 datasheet ground truth (verified)

### 1.1 Module outline — the spec doc's 59.26 is WRONG
- Datasheet §2.2 (p.5): **"Outline Dimension with FPC Folded: 42.72(W) x 59.46(H) x 2.3(T) mm"**.
- Outline drawings: p.6 (no TP) "BL 59.46±0.2"; p.8 (capacitive TP, our variant) shows BOTH
  "BL/CTP 59.26±0.2" (CTP glass) and "BL 59.46±0.2" (backlight frame = largest layer).
- **The module envelope is 42.72 x 59.46 mm, not 59.26.** The 59.26 in
  `design-notes/mechanical-architecture.md` is the CTP glass height only. The board+battery
  budget must use 59.46 (+0.2 mm tolerance). Width 42.72±0.2 confirmed on all three drawings.
- CTP variant thickness: LCD 2.3±0.1 + CTP; touch COF (FT6336) sits ON the FPC tail,
  **MAX 1.7 mm** (p.8 side view); tail tip 0.30±0.03 (stiffener side + conductor side labeled).
  Budget ~4.2 mm for the display assembly in the case stack.

### 1.2 Active area position — NOT centered vertically
From p.6 (identical LCD in p.8): height chain 2.90 → A.A 48.96 → remainder 7.60 (59.46 total);
1.90 → V.A 50.96 → 6.60.
- **Top margin (away from FPC) = 2.90 mm; bottom margin (FPC/COG ledge end) = 7.60 mm.**
- Width: A.A 36.72 centered (3.00 both sides); V.A 38.72 (2.00 sides, no-TP); CTP V.A 37.32.
- The FPC exits the **bottom (42.72-wide) edge** — confirms the mechanical note.

### 1.3 FPC tail geometry (p.6 drawing, cross-checked by pixel measurement at 9.90 px/mm)
- **Tail flat length = 27.00 mm** from the module (BL) bottom edge to the contact tip
  (dim verified: 26.97 mm measured between the module edge line and the tip).
- Contact end: 50 contacts, 0.5 mm pitch, pad width 0.35, contact-end tail width **25.50 mm**.
- Dimension chain 6.00 / 25.50 / 31.50 decoded from extension lines (shared references):
  the 25.50-wide contact-end band sits **8.48 mm from EACH side edge → the insertion tip is
  EXACTLY CENTERED on the 42.72 width** (measured symmetric to <0.15 mm). The 31.50-wide
  root band is offset: it extends 6.00 mm beyond the tip band on ONE side (the pin-1 side),
  i.e. root band spans 2.42..34.24 mm from the pin-1-side module edge.
- Pin 1 (label "1" on the drawing) is at the tip-band end nearest that offset edge.
  Pin table (p.9): 1=LEDA, 2-5=LEDK1-4, 10=RESET, 33=SDO, 34=SDI, 37=D/CX(SCL), 38=CSX,
  40/41=VDDI 2.8V, 42=VCI 2.8V, 43+48-50=GND, 44-47=cap-touch SCL/SDA/INT/RESET.
- Connector requirement, §2.1 (p.5): **"FPC Connector: 50 Pin, 0.5mm Pitch, SMD Horizontal
  Type Top contact"**.

### 1.4 Mapping to board coordinates (display face away from F.Cu viewer → x mirrored)
Display mounted on the B side, face = device front; KiCad front view looks at the device BACK,
so the datasheet front view is mirrored in x. Display spans x 10.64..53.36 (flush = board
width), y 11.34..70.8 (bottom edge flush with board bottom edge).
- Folded-tail contact columns: tip band x = **19.12..44.88, centerline x = 32.00** (centered).
- **Tail pin 1 column ≈ x = 19.75 (LOW x / KiCad left)**; pin 50 ≈ x = 44.25.
- Root (31.5 mm) band: x ≈ 13.06..44.88 → folded-tail keepout swath on the B side.
- Folding 180° about the bottom edge does not swap left/right and flips the conductor face
  from "toward display back" to "away from board" — exactly what a **top-contact** connector
  mounted on B.Cu needs (Hirose catalog p.3 annotates top-contact type: "FPC/FFC conductive
  surface" on the side away from the mounting PCB).

---

## 2. J2 findings

### 2.1 CRITICAL — wrong connector variant: FH12-50S-0.5SH is a BOTTOM-contact part
- Hirose FH12 catalog p.3 "Series Configuration": **"FH12-**S-0.5SH" is listed under
  "Bottom Contact Type"** (p.4 table includes FH12-50S-0.5SH, HRS 586-0529-2).
  The **top-contact** series is **"FH12A-**S-0.5SH"** (p.6, "0.5mm Pitch Top Contact Type"),
  available in 50 pos: **FH12A-50S-0.5SH(55), HRS 586-0559-3**.
  Product number structure (p.2): 3rd field "Blank: standard; A: Top contact type".
- The display demands TOP contact (§1.3 above). With the bottom-contact part the folded
  tail's conductors face away from the contacts → **no electrical mating possible**.
- Affected artifacts:
  - BOM `production/bom/pcbway-bom.csv` line 10: `J2 ... FH12-50S-0.5SH(55)` (self-describes
    as "top-contact" — wrong; its own note "footprint must be checked against the panel FFC
    drawing" was never closed).
  - `design-notes/component-freeze.md:22` and `design-notes/mechanical-architecture.md:12`
    ("ER-CON50HT-1 / Hirose FH12-50S-0.5SH class" — ER-CON50HT is top-contact, the named
    Hirose part is not; someone dropped the 'A').
  - Footprint `Connector_FFC-PC:Hirose_FH12-50S-0.5SH...` is the bottom-type land pattern;
    FH12A differs (leads/fittings arrangement): FH12A-50S: A=29.1, lead span B=28.35,
    contact span C=24.5, fitting span D=29.5, **FPC slot width E=25.57** (perfect fit for the
    25.50 tail, ±0.035 lateral), height 2.0 mm, depth 6.2 incl. rear flip-lock actuator.
- FIX: change J2 to **FH12A-50S-0.5SH(55)** (or EastRising ER-CON50HT-1) and rebuild the
  footprint from the Hirose FH12A drawing.

### 2.2 CRITICAL — pin order mirrored (all 50 signals reversed)
Verified with pcbnew on the live board:
- J2 pad 1 = (44.250, 46.150) net `TFT_BACKLIGHT_A`; pad 50 = (19.750, 46.150) net `GND`.
- Physical folded-tail pin 1 (LEDA) lands at x ≈ 19.75 (§1.4) — i.e. exactly on J2 pad "50".
- The schematic/netlist maps display pin numbers 1:1 to J2 pads (netlist-contract:
  "TFT_SPI_MISO (display SDO, J2 pin 33)"), so as placed the mating is fully mirrored:
  LEDA↔GND, VDDI/VCI (2.8 V) onto IM/RESET pads, SPI/touch scrambled. Non-functional and
  potentially damaging.
- Note the footprint cannot be fixed by rotation: on B.Cu, rot180 gives mouth-to-bottom but
  pad1 at high-x; rot0 gives pad1 at low-x but mouth-to-top. The physical connector is
  left-right symmetric, so the fix is numbering, not mechanics.
- FIX: when rebuilding the footprint for FH12A (2.1), number the pads mirrored (pad 1 on the
  +x side of the footprint's local frame so that after the B-side flip it lands at low x), or
  equivalently reverse the 50-pin mapping in the schematic symbol. Keep contract text in sync.
- Residual risk: the pin-1 end was derived from the datasheet outline drawing read as a
  front view (standard for LCD modules; corroborated by the fold/top-contact consistency).
  **Verify against the physical module (pin-1 silk on the tail) at first article before fab.**

### 2.3 IMPORTANT — J2 is ~4.4 mm too far from the fold (tail cannot reach cleanly)
- Fold model: tail exits at the display back plane, wraps 180° at the bottom edge
  (radius r), then runs north in the 2.0 mm connector-height gap. Usable straight run
  = 27.0 − π·r. For r = 0.5..1.2 mm the fully-inserted tip line falls at
  **y ≈ 45.4..47.6** (measured from bottom edge: 23.2..25.4 mm).
- Current placement: anchor (32,48) rot180 → body 46.7..52.4, mouth face y=52.4,
  FPC stop ≈ y 50.5. Required fold consumption = 27.0 − (70.8−50.5) = 6.7 mm →
  **fold radius ≈ 2.1 mm, bulging ≈ 2 mm beyond the display bottom edge** — breaks the
  42.72 x 59.46 envelope ("nothing sticks out"), stresses the tail, and lifts the fold into
  the case-wall/USB-C region.
- TARGET (bottom-edge referenced, independent of the H decision):
  - contact tip / FPC-stop line: **y ≈ 45.7** (25.1 mm from bottom edge)
  - **mouth face line: y ≈ 48.0 ± 0.3** (22.8 mm from bottom edge), mouth facing the bottom
    edge (rot unchanged conceptually); nominal fold r ≈ 0.6, bulge ≤ 1.0 mm (give the case
    ≥1.0 mm internal clearance at the bottom edge for the fold).
  - x center: **keep 32.00** (tip band is exactly centered — current x is correct).
  - Equivalent anchor for the current footprint style: ≈ **(32.0, 43.6)** → move J2 ~4.4 mm
    north. With the rebuilt FH12A pattern, place by the mouth-face line above.
  - Tolerance check: tail 27.0±0.3 and fold r 0.5..1.2 keep the stop reachable
    (reach range 45.4..47.6 covers 45.7 with margin on the loose side).
- B side is otherwise empty (only J2) — no collision from the move; the folded COF bump
  (MAX 1.7, faces the board after folding) lands at y ≈ 58..61 in the 2.0 mm gap — OK, keep
  that swath (x 13.1..44.9, y from J2 mouth to bottom edge) free of B-side parts (it is) and
  of anything taller than ~0.3 mm (mask/silk/vias are fine).

---

## 3. Board outline — width is ALREADY compliant; the "42.87" is a bbox artifact

- Edge.Cuts centerlines: x = 10.64 and 53.36 → **width exactly 42.72 mm**; y = 31.0 and
  70.8 → **height 39.80 mm** (not 39.95). The 42.87 x 39.95 "bbox" includes the 0.15 mm
  Edge.Cuts stroke width (0.075 per side). Fabs (incl. PCBWay) rout along the graphic
  centerline; the Gerber profile is generated from centerlines.
- **Do NOT shrink 0.075 mm/side** — that would make the board 42.57, under-size vs the
  display. Record the real numbers (42.72 x 39.80) in the docs/validators instead.
- Edge-adjacent parts (checked, all fine as-is):
  - SW1 EVQ-P7J01P @(52,52): bbox reaches x=53.675, i.e. the side actuator overhangs the
    right edge by 0.32 mm — intentional for a side-actuated button.
  - J1 USB-C GCT USB4105 @(32,66.2): southernmost through-hole shield pads at y=69.04
    (1.76 mm inboard of the edge) and NPTH posts at y=61.84 — the "+0.8 mm bottom extension"
    goal is met; receptacle front overhangs to ~72.0 (normal).
  - MH1-4 M2 clearance holes: hole edge ~1.36 mm from each edge centerline — OK.
- Note: board width == display width with zero margin is per spec, but display BL tol is
  ±0.2 — the enclosure must locate the display, not the board edge.

---

## 4. DISP1 envelope replacement (currently stale + parked off-board)

Current: `DISP1` value `NHD-2.4-240320AF-CSXP-CTP`, fp `Display_Envelope_42.8x59.91mm`,
parked at (110,125) — models the OLD Newhaven part.

Replacement spec (new footprint `Display_Envelope_ER-TFT024IPS-3_42.72x59.46mm`, B side,
doc layers only: B.Fab outline + User.Drawings; courtyard optional on B.CrtYd for the
on-board portion):
- Module outline rect: x 10.64..53.36, y 11.34..70.8 → **anchor at center (32.00, 41.07)**
  (or anchor at bottom-center (32.00, 70.80) to make the flush-bottom constraint explicit).
- Active area window (36.72 x 48.96): x 13.64..50.36, y **14.24..63.20**
  (top margin 2.90, bottom margin 7.60 = COG/tail ledge).
- Mark the FPC exit + fold zone at the bottom edge: root band x 13.06..44.88; tip band
  x 19.12..44.88 with pin-1 tick at x=19.75; arrow "folds 180° to J2".
- Value field: `ER-TFT024IPS-3` (CTP, FT6336). Fix the pcbway-manifest/BOM references that
  still say NHD.
- The top ~19.7 mm of the drawn envelope (y 11.34..31.0) intentionally hangs past the board
  top edge — that is the battery bay; keep it on User.Drawings so it survives outside the
  outline.

---

## 5. Battery zone and board height

Zone = 42.72 wide x (59.46 − H) tall, behind the display above the board top edge.
Thickness budget: board 1.6 + tallest F.Cu part (J9 JST-PH, 6.0) ≈ 6 mm → 5.3 mm packs OK.

Constraint discovered: **J9's mated plug (JST PHR-2, ~5 mm deep + wire bend) always intrudes
~5 mm below the top edge into the zone** in its x band (~x 41.5..46.5 at J9 x=44). J6 is the
expansion port — unmated in normal use, not a battery keepout.

| Option | Top edge y | H (mm) | Zone (mm) | Best real cells (pack dims incl. PCM) | Capacity |
|---|---|---|---|---|---|
| A (as-is) | 31.0 | 39.80 | 42.72 x 19.66 | EEMB LP401525/LP501525 (~15.5 x 27 x 4-5.3); LP501535 too long once J9 plug band subtracted | ~100-150 mAh |
| B (spec) | 34.0 | 36.80 | 42.72 x 22.66 | **EEMB LP502030 250 mAh, pack 20.5 x 32 x 5.3** (20.5 fits with 2.1 mm margin) | **250 mAh** |
| B+ | 34.0 | 36.80 | same | LP502035/LP502040 (20.5 x 37..42) — length collides with J9 plug band and case walls | 340-400 mAh (stretch) |

- Option B requirement: the 32-mm-long LP502030 pack needs clear span from the left wall to
  the J9 plug band → **shift J9 right from x=44 to x ≈ 46.5** (plug band 43.6..48.6, still
  inboard of the MH4 fillet) giving 32.5 mm clear (11.1..43.6). Without the shift only a
  bare 30.5 mm cell fits (borderline).
- Option A (keep 39.80) is battery-starved: the 19.66 mm zone rejects every 20-mm-wide cell
  (20.5 real width > 19.66); practical ceiling ~150 mAh.
- **Recommendation: Option B — shrink to H=36.8** (the user-confirmed soft target, already
  proven placeable per mechanical-architecture status 2026-06-15). Top-strip re-floorplan
  required: move J6, J9, J7, JP1, TP_UART_GND, ANT1 south by ~3.0 mm; MH3/MH4 to the new
  fillet centers (13.1, 36.6)/(50.9, 36.6). J2's y target (§2.3) is bottom-referenced and
  unaffected.

### Recommended outline (exact)
- x0=10.64, y0=34.00, W=42.72, H=36.80 → corners (10.64,34.00)-(53.36,70.80),
  R2.5 fillets, Edge.Cuts stroke 0.15 (cut on centerline).
- Bottom edge, left/right edges, J1/SW1/MH1/MH2 unchanged.
- J2 target: x=32.00, mouth face y=48.0±0.3 facing bottom edge (anchor ≈ (32.0,43.6) in
  current-footprint terms), FH12A-50S-0.5SH(55) with mirrored pad numbering per §2.2.

---

## 6. Documentation corrections needed
- mechanical-architecture.md: 59.26 → 59.46 (module H, board+battery budget); battery space
  at H=36.8 is 22.66 (not "~22.5" — close but restate vs 59.46); "FH12-50S-0.5SH" →
  "FH12A-50S-0.5SH (top contact)"; board 42.72 x 39.80 current (not 42.87 x 39.95).
- component-freeze.md:22 same connector correction.
- pcbway-bom.csv J2 line: part number + description.
- netlist-contract note about "J2 pin 33" must be revisited after the pin-mirror fix.

## Evidence index
- ER-TFT024IPS-3 datasheet p.5 (§2.2 outline w/ FPC folded 42.72x59.46x2.3; §2.1 top-contact
  connector), p.6 (outline drawing: 2.90/48.96/7.60 chain, 6.00/25.50/31.50 tail chain,
  27.00 tail length, 1/50 pin labels), p.8 (CTP drawing: BL 59.46 vs CTP 59.26, MAX 1.7 COF),
  p.9 (pin table 1=LEDA...48-50=GND).
- Hirose FH12 catalog 2017.1: p.2 (number structure: A = top contact), p.3 (series config:
  FH12-*S-0.5SH = bottom contact; FH12A-*S-0.5SH = top contact), p.4 (FH12-50S dims),
  p.6 (FH12A-50S dims A=29.1 B=28.35 C=24.5 D=29.5 E=25.57, h=2.0).
- pcbnew pad dump: J2 pad1 (44.25,46.15) `TFT_BACKLIGHT_A`, pad50 (19.75,46.15) `GND`;
  J1 SH pads y=63.09/69.04, NPTH y=61.84.
- Edge.Cuts lines from board file: x 10.64/53.36, y 31.0/70.8, stroke 0.15.
- Cell data: EEMB LP502030 250 mAh typ, pack 20.5x32x5.3 (eemb.store/products/lp502030);
  EEMB LP502040 340 mAh, pack 20.5x42x5.3.
