# DFM Review — PCBWay Fabrication + Assembly Readiness

Board: `/Users/vincenzo/Documents/GitHub/nSealr/hardware/pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_pcb`
(KiCad 10.0.3, 4-layer, 42.87 x 39.95 mm, 103 footprints, 926 track segments @0.2 mm, 129 vias all 0.6/0.3 mm)
Date: 2026-07-03. All PCBWay figures re-verified against pcbway.com July 2026.

---

## 1. PCBWay capability survey vs this board

### 1.1 Trace / space (4L, 1 oz outer, 1 oz inner)
- PCBWay standard: outer 35 µm Cu >= 5/6 mil (0.127/0.152 mm); inner 18-35 µm >= 4/4-4/5 mil. Cost-neutral if >= 6/6 mil. Source: [PCBWay capabilities](https://www.pcbway.com/capabilities.html), [min track/spacing by copper weight](https://www.pcbway.com/helpcenter/ordering_parameter_instruction/What_is_the_Min_Track_Spacing_for_1oz__2oz__3oz__Copper_weight_.html).
- Board: every routed segment is 0.2 mm (7.87 mil) with 0.2 mm clearance (Default netclass). **PASS with ~30% margin, no surcharge.**

### 1.2 Drill / via / annular ring — task premise was stale
- The task brief said "we use via 0.4 mm / drill 0.2 mm". **Measured reality: all 129 vias are 0.6 mm pad / 0.3 mm drill.** No 0.2 mm drills exist on the board.
- PCBWay: drill capability 0.15-6.3 mm, but **holes < 0.3 mm trigger extra charges** ([extra-cost policy](https://www.pcbway.com/helpcenter/paymentproblems/What_PCBs_will_be_charged_of_extra_cost_.html); a documented user saw 0.2 mm drills take a proto from $1/board to $10/board). Min annular ring **0.15 mm** ([annular rings page](https://www.pcbway.com/pcb_prototype/Annular_rings.html)).
- 0.6/0.3 via = 0.15 mm annular ring = exactly PCBWay minimum, standard price, aspect ratio 1.6/0.3 = 5.3:1 (well under their limit). **PASS.**
- **However the project rules would permit non-conforming geometry**: `.kicad_pro` has `min_via_annular_width: 0.1` (< PCBWay 0.15), `min_through_hole_diameter: 0.2` (surcharge zone), `min_hole_to_hole: 0.25` (< PCBWay ">= 11 mil (0.28 mm) spacing for holes <= 0.45 mm"), `min_copper_edge_clearance: 0.2` (< PCBWay recommended 0.25 mm line-to-edge). Nothing on the board violates PCBWay today, but the rules give no guardrail for the remaining ~69-open-connection routing work. Recommend: annular 0.125-0.15, through-hole min 0.3, hole-to-hole 0.3, copper-edge 0.3.

### 1.3 QFN 0.4 mm pitch (U2 TROPIC01)
- PCBWay assembly handles fine pitch down to 0.25 mm and QFN explicitly; X-ray inspection available for QFN/BGA ([SMT assembly capabilities](https://www.pcbway.com/pcb_prototype/SMT_Assembly_Capabilities.html), [assembly capabilities](https://www.pcbway.com/assembly-capabilities.html)). 0.4 mm pitch QFN32 is **within standard capability**; request X-ray on U2/U9 EP joints.
- Mask sliver check: U2 pads 0.2 mm wide on 0.4 mm pitch -> 0.2 mm copper gap; board global `pad_to_mask_clearance = 0` -> mask webs = 0.2 mm > PCBWay min mask bridge 4 mil (0.1016 mm, green). **Mask-defined webs survive — no gang opening needed.** Note `solder_mask_min_width` is unset in KiCad, so DRC would not catch future sliver violations; set it to 0.1 mm.

### 1.4 Paste apertures on QFN exposed pads — verified GOOD
- U2 (QFN32 4x4, EP 2.65 mm): EP copper pad 33 is F.Cu+F.Mask only; paste delivered by 4 separate 1.07 x 1.07 mm F.Paste-only apertures -> coverage 4(1.07^2)/2.65^2 = **65.2%** — inside the 50-80% window recommended by QFN app-notes (e.g. Microchip QFN AN, sec. on EP stencil design).
- U9 (QFN32 5x5, EP 3.45 mm): 9x 0.93 x 0.93 mm apertures -> **65.4%**. Both correct as-is; no stencil edit needed.

### 1.5 Surface finish — ENIG required
- Industry + PCBWay guidance: HASL is unsuitable below 0.5 mm pitch (uneven meniscus; QFN EP sits on a solder dome and lifts perimeter pins). ENIG coplanarity < 0.5 µm supports 0.4 mm QFN; also correct for J7 Tag-Connect TC2030 spring-pin pads (flat, corrosion-resistant, low contact resistance; HASL is explicitly poor for pressure-contact pads). Sources: [PCBWay surface finish comparison](https://www.pcbway.com/pcb_prototype/Comparison_of_several_PCB_surface_finish_types.html), Seeed/RayPCB fine-pitch finish guides.
- **Recommendation: ENIG (lead-free), expect +15-25% board cost. Set in pcbway-manifest / order notes.**

### 1.6 4-layer 1.6 mm stackup and USB impedance
- PCBWay default 4L/1.6 mm: 7628 prepreg (~0.195-0.21 mm) / ~1.2 mm core / 7628 ([stackup page](https://www.pcbway.com/multi-layer-laminated-structure.html)). Board file declares 0.035/0.18 prepreg/1.12 core/0.18/0.035 = 1.63 mm — compatible with their standard build (they will substitute their exact PP mix unless custom stackup is ordered).
- **Controlled impedance is NOT needed.** STM32U585 has USB OTG **Full-Speed only** (12 Mb/s, no HS PHY — STM32U575/585 datasheet DS13737, feature list). USB 2.0 FS edge rates are 4-20 ns; with J1 at (32, 66.2) and U1 at (28, 50) the D+/D- run is ~20-25 mm — two orders of magnitude below the critical length for FS. USB 2.0 spec impedance requirements (90 ohm +/-15%) target the cable/HS signaling, not short FS PCB traces. Route D+/D- as a coupled 0.2/0.2 pair over the In1 GND plane, length-matched within ~2 mm, and **do not pay for impedance control** (PCBWay charges extra for it; their own forum guidance confirms designing to the standard stackup nominal is fine).
- FYI if 90 ohm diff were ever wanted on their 7628 stackup: ~0.25-0.28 mm width / 0.15-0.2 mm gap microstrip — feasible without exotic geometry.

### 1.7 Outline / Edge.Cuts / board size
- Edge.Cuts = 4 lines + 4 arcs (R2.5 corners): PCBWay CNC-routs arcs natively, outline tolerance **+/-0.2 mm** ([manufacturing tolerances](https://www.pcbway.com/pcb_prototype/PCB_Manufacturing_tolerances.html)). Note for the mechanical fix: even after correcting 42.87 -> 42.72 mm HARD width, the routed board can be 42.72 +/- 0.2 mm — the enclosure/display margin must absorb up to 42.92 mm worst case, or the nominal must be set to 42.5-42.6.
- Fab size limits: min 3x3 mm, multilayer max 560x1150 mm — no issue. Castellations: n/a, none present.

---

## 2. Project rules & artifacts vs PCBWay (verdict)

| Item | Project value | PCBWay standard | Verdict |
|---|---|---|---|
| min track | 0.2 mm | 0.127 mm (5 mil outer 1 oz) | OK, margin |
| clearance | 0.2 mm | 0.152 mm (6 mil) | OK |
| via 0.6/0.3 (actual) | ann. 0.15 | ann. min 0.15, drill >= 0.3 free | OK, zero margin on ring |
| min_via_annular_width rule | 0.1 mm | 0.15 mm | **rule too loose — tighten** |
| min_through_hole rule | 0.2 mm | < 0.3 mm = surcharge | **tighten to 0.3** |
| min_hole_to_hole | 0.25 mm | 0.28 mm (holes <= 0.45) | **tighten to 0.3** |
| copper-to-edge | 0.2 mm | 0.25 mm recommended | **tighten to 0.3** |
| solder_mask_min_width | unset (0) | bridge >= 0.1016 mm | **set 0.1 for DRC** |
| mask expansion | 0 | fine (CAM adjusts) | OK |
| silk text 0.8 mm h / 0.15 w | matches 0.8 / 0.15 min | OK; but 261 silk lines at 0.10-0.12 mm | **thicken graphic lines to 0.15** |

- `production/pcbway-manifest.json` is **stale/blocked**: says "no routed KiCad PCB copper exists" while the board now has 926 segments + 129 vias. `production/drc/drc.json` is dated 2026-06-11 (4 violations / 262 unconnected vs today's 0 / 69). Both must be regenerated as part of the fab-export gate.
- Netclasses: only `Default` exists. No USB diff-pair class, no wider power class (TROPIC_VCC, VBUS, SYS_3V3, backlight all at 0.2 mm). Not a PCBWay problem, but define classes before finishing the 69 opens.

---

## 3. Assembly readiness

### 3.1 Fiducials — NONE on board (confirmed: 0 fiducial footprints among 103)
PCBWay fiducial rules ([design instruction](https://www.pcbway.com/helpcenter/design_instruction/PCB_Panelization__Breakaway_Rails__Fiducial_Marks__Tooling_Holes.html)): solid circle 1.0 mm bare copper, mask keepout radius 2R (3R better), all same size, 3 per side placed asymmetrically. Panel rails carry 3x 1.0 mm panel fiducials (1.7 mm mask opening), which PCBWay adds when they design the panel — but board-level fiducials are still recommended for the 0.4/0.5 mm-pitch parts.
**Action: add 3x Fiducial_1mm_Mask2mm on F.Cu near three corners (inside the MH1-4 keepouts, >= 5 mm from edge where possible) and — because J2 (0.5 mm FFC) sits on B.Cu — at least 2, ideally 3, on B.Cu as well.** Note J2-on-back makes this a **double-sided assembly** job (small extra cost, unavoidable per mechanical spec).

### 3.2 Panelization — REQUIRED for assembly
- PCBWay assembly panel minimum is **50 x 50 mm** ([panel requirements](https://www.pcbway.com/pcb_prototype/Panel_Requirements_for_Assembly.html)); the board is 42.87 x 39.95 mm -> below minimum as a single piece.
- R2.5 rounded corners rule out V-scoring (V-cut must run straight, uninterrupted). **Use tab-routing with stamp holes** (tabs >= 2 mm; 1.6 mm routing gap between boards; stamp holes 0.55-0.6 mm).
- Simplest path: tick "PCBWay does panel design" on the order — e.g. 2x2 with 5-8 mm rails + panel fiducials + 4 tooling holes. Constraints to communicate: **no tabs on the bottom edge center (J1 USB-C at (32, 66.2) is flush with the edge) and none on the right edge near SW1 (52, 52) — the side-actuated button overhangs; put tabs on top edge (antenna zone edges are copper-sensitive: keep tabs off the ANT1 coil area once it exists) and left edge / corners.**

### 3.3 BOM — MAJOR GAP
`production/bom/pcbway-bom.csv` has **16 line items for a 103-footprint board**. Present: U1-U5, U7-U11, J1, J2, J6, J9, SW1. **Missing: every passive (all R, C, L including L1 buck inductor and L15 backlight inductor), X1 16 MHz, X3 27.12 MHz, LED1 RGB, U13/U14 TPS22917, U15 TPS61165, U7-adjacent ESD parts, D*, FB*, JP1** — a turnkey quote is impossible.
- Column format vs [PCBWay BOM requirements](https://www.pcbway.com/helpcenter/pcb_assembly_ordering/What_file_format_should_BOM_be_.html): required *Designator, *Qty, *Mfg Part #, *Package — present. Missing recommended **"Type" (SMD/THT)** column and **"Item #"**. Add a **DNP/"do not populate" marking** convention and list ANT1, DISP1, TP_*, JP1(open) as DNP rows so PCBWay engineering doesn't query them (the manifest itself demands these as `required_non_pcba_rows`).
- CSV/xlsx accepted; PDF not.

### 3.4 Pick-and-place / centroid
- No `.pos`/centroid file exists under `production/`. PCBWay requires centroid (Designator, Mid X, Mid Y, Layer, Rotation) covering the same designators as the BOM ([assembly file requirements](https://www.pcbway.com/assembly-file-requirements.html)).
- Generate with KiCad "Footprint position (.pos/CSV, mm, both sides)"; **exclude DISP1, ANT1 and virtual/TP footprints**. Expect PCBWay engineers to confirm polarity/rotation of U2 (QFN pin 1), U9, U10 (VQFN), LED1, diodes against photos during EQ — answer with the F.Cu render.

### 3.5 Orientation marking / silkscreen
- Standard KiCad-library footprints carry pin-1 chevrons (U2's pad 1 is even a custom pin-1-marked pad). Ref-des text is 0.8 mm/0.15 stroke = PCBWay legibility minimum. 261 silk graphic lines at 0.10-0.12 mm are below their 0.15 mm silk width — they may print thin/patchy; bump to 0.15 mm during cleanup (minor).

### 3.6 THT vs SMT mix
- **Effectively an SMT-only build.** J6 (SM04B-SRSS-TB) and J9 (S2B-PH-SM4-TB) confirmed SMT per MPN and footprint. The only through-board features: J1 USB4105 hybrid — 24 SMT pads + **4x PTH shield posts drill 1.1 mm + 2 NPTH pegs 0.65/0.95 mm** (all >= 0.3 mm, standard; posts are hand/selective-soldered, PCBWay handles routinely). J7 Tag-Connect: 3x NPTH 0.9906 mm alignment holes, no paste (pads are `connect` type — correct).

---

## 4. Missing-for-fab checklist (definitive)

Blockers (cannot upload today):
1. **Routing incomplete — 69 open connections** (40 GND + TROPIC/NFC SPI, VBUS, NRST, etc.). No release gerbers until 0 opens + re-run DRC.
2. **ANT1 is a mechanical envelope with ZERO pads and zero copper** (`nSealr_Mechanical:NFC_Antenna_Envelope_42x8mm`). The 13.56 MHz antenna coil must be drawn as real F.Cu (or split to a flex/daughter part) *and* the ST25R3916B matching network retuned to the measured coil — see ST AN "ST25R3916 antenna matching" in `/Users/vincenzo/Downloads/nsealr-datasheets/`. Without it PCBWay would fabricate a board with no NFC antenna.
3. **BOM incomplete (16/103)** — see 3.3.
4. **No centroid/pos file** — see 3.4.
5. **DISP1 envelope parked off-board at (110,125) on B.Cu** — outside Edge.Cuts; it will inflate gerber extents and pollute pos/BOM exports. Remove it, or mark "exclude from position files / BOM / board" (KiCad footprint attributes) before export.
6. **Fiducials** — see 3.1.
7. **Stale production artifacts**: pcbway-manifest.json ("blocked", claims unrouted), drc/drc.json (2026-06-11). Regenerate at export.

Upload package once unblocked:
- Gerbers X2: F.Cu, In1.Cu, In2.Cu, B.Cu, F/B.Mask, F/B.Paste, F/B.SilkS, Edge.Cuts (single outline, arcs fine).
- Drill: Excellon PTH + **NPTH as separate file** (J1 pegs 0.65/0.95, J7 3x 0.9906, any MH1-4 NPTH), plus drill map.
- Centroid CSV (mm, both sides), BOM CSV per 3.3, stencil note: use provided F.Paste/B.Paste as-is (EP subdivision already correct).
- Order parameters: 4L, 1.6 mm, TG150 (auto-upgrade), 1 oz outer / 1 oz inner, **ENIG**, green mask / white silk (or per ID choice), min hole on order form = 0.3 mm, no impedance control, PCBWay-designed tab-route panel with rails + note on tab-free edges (3.2), double-sided assembly, X-ray on U2/U9.

---

## 5. Testpoints / testing
- Bare-board: PCBWay **flying-probe e-tests every board free at prototype quantity** against the gerber netlist ([E-test page](https://www.pcbway.com/pcb_prototype/Electronic_test___probe_test.html)); no testpoints needed for that (they probe pads/vias). Extra fees only for huge panels/qty.
- Assembled-board functional test is optional/quoted separately and *would* use testpoints. The repo's own contract requires TP_3V3 / TP_BOOT0 / TP_GND / TP_NRST / TP_SWCLK / TP_SWDIO which are **absent** (only TP_UART_TX/RX/GND exist at (38,52)/(38,53.5)/(25,35)). Add them in the debug cluster near J7 (28, 38.5) to green the validators and enable bring-up/HIL — not a PCBWay blocker, but a program blocker.
- Keep testpoint count trivial (<10k/board threshold irrelevant here).

## 6. Notable non-issues (verified OK)
- Via geometry 0.6/0.3 everywhere — standard, no surcharge (task premise of 0.4/0.2 was stale).
- QFN EP paste subdivision U2/U9 at ~65% — correct, leave alone.
- Mask webs on 0.4 mm pitch = 0.2 mm > 0.1016 mm min — no gang opening.
- Edge.Cuts arcs, board size, J1 drill sizes, SMT-only J6/J9 — all standard.
- USB FS needs no controlled impedance; default stackup fine.
