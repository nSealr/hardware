# Fab Handoff Checklist — from "reviewed design" to "first-article gerbers"

Date: 2026-07-03. This is the execution checklist that turns the committed design
(`00-SYNTHESIS`, `01-part-selections`, `placement-refloorplan`, the 7 area
reports) into a first-article fab package. Steps marked **[GUI]** need the KiCad
interactive editor (or a PCB contractor, ~½–1 day); steps marked **[HW]** need a
physical first article. Everything else is specified to coordinate/value level in
the referenced docs.

## State at handoff
- **Decisions locked:** H = 36.8 mm, 250 mAh LP502030, **NFC antenna on a
  back-cover FPC** (main board keeps only the matching net + `NFC_ANT1/2` feed).
- **Geometry done** (branch `feature/pcb-rebuild-2026-07`, WIP): outline is
  42.72 × 36.8 mm, MH3/MH4 at the new top fillets, on-board ANT1 removed. (30 DRC
  are the top-strip parts still to be re-placed — step 2.)
- **Design rules** already at PCBWay minimums (annular 0.15 / hole 0.3 / h2h 0.3 /
  edge 0.3 / mask 0.1), committed on `main`.
- Toolchain proven: `scratchpad/routing/pcb_edit_lib.py`, Freerouting 2.1.0 on
  JDK26, KiCad 10.0.3 cli + bundled python; renders + DRC used to verify each stage.

## Why the finish is GUI/first-article (honest)
A full multi-agent review + an independent density check established that this
board's dense re-placement and final routing need the interactive push-and-shove
router, and that the 13.56 MHz antenna cannot be finalized without VNA tuning on a
physical article. Headless scripting did the geometry cleanly and can bulk-route,
but forcing the tidy final placement/route headless yields a degraded,
un-verifiable board. This is the normal first-article flow for an NFC device.

## Execution steps

**1. Schematic source of truth [decide].** Either extend the generator's
`schematic-binding.json` + `netlist-contract.json` to the *complete* per-pin,
per-value model (add the NFC front-end via a rebuilt 33-pin ST25R3916B symbol, the
replaced backlight driver, all decoupling, the corrected J2 pinout, the 6 TPs, the
J-ANT feed) — or capture a real KiCad schematic. Either way the deliverable is an
**ERC-clean netlist** for all ~120 parts. Parts + values are fully specified in
`01-part-selections.md`; connectivity fixes in the area reports.

**2. Placement [GUI].** Apply `placement-refloorplan.md` §3 (the **FPC/A variant**
positions) — it is a full (ref, current→proposed x,y,rot) table with the added
caps' at-pin landings in §3e. Keep U1's decoupling ring intact; put every added
cap at its pin; crystals X1/X3 hard against their pins; NFC matching compact at U9;
debug group + 6 TPs grouped near J7; J9 to (44,42); J-ANT feed near U9. Target
density ~79 % (feasible). 0 courtyard overlaps.

**3. Connector fix [GUI].** Rebuild J2 as **FH12A-50S-0.5SH(55)** (top-contact)
with **mirrored pad numbering** (mechanical report §2.1–2.2). Replace DISP1 with
the `ER-TFT024IPS-3_42.72x59.46` envelope (§4). Fix J2 y to mouth-face ≈48.0 (§2.3).

**4. Backlight driver swap [GUI+sch].** Replace TPS61165+L15+D15+R15 with the
4-sink/buck WLED driver from `01-part-selections.md §B` (AL8860 from SYS_PWR_IN).

**5. Route [GUI].** Net-classes: power (0.3–0.4 mm), USB D± coupled pair, NFC feed.
Freerouting for the bulk (DSN with GND pours pre-filled → treats GND as plane),
then interactive push-and-shove for the ~remaining cross-board nets. GND zones on
F/B + In1 plane + stitching vias (grid + at each IC GND + U2/U9 EP). U9 EP via
farm (3×3). **DRC 0 + 0 unconnected** (excluding the documented edge-connector
clearances).

**6. Fab package.** Regenerate full **BOM** (all ~120 parts, mark RF caps `DNP?`
no — mark them `tuning`, mark DISP1/J-ANT-loop/TP as non-PCBA), **centroid/.pos**,
add **fiducials** (3×F.Cu + 2–3×B.Cu), gerbers X2 (F/In1/In2/B + mask/paste/silk +
Edge.Cuts), Excellon PTH + separate NPTH, drill map. Order params: 4L / 1.6 mm /
1 oz-in-1 oz-out / **ENIG** / min-hole 0.3 / no impedance control / tab-route panel
(board < 50×50) / double-sided assembly / X-ray U2,U9. Regenerate the stale
`production/pcbway-manifest.json` + `drc/`. Update repo validators
(`materialize_*`, `update_*`) and green `make ci` (the 6 TPs land in step 2).

**7. Antenna FPC.** Separate tiny flex: Ø≈30 mm loop (or 34×6 strip), L≥1 µH, 2
terminals to J-ANT, Würth WE-FSFS ferrite backing. Own fab item (`01 §F`).

**8. First article + tuning [HW].** Build a small run; **VNA-measure** La/Q with
the full stack (ferrite+display+battery+cover); set the matching caps (Cs/Cp/Cr/Cd/
Rd) and crystal loads per STSW-ST25R004; scope RFI ≤3 Vpp + Type-A timing. Then
freeze production values.

## The two irreducible gates
- **[GUI]** final push-and-shove routing (steps 2/5 interactive polish).
- **[HW]** antenna RF tuning (step 8) — physics, true for any NFC device.
