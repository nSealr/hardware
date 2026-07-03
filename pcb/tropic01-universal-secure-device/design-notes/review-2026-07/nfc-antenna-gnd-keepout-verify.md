# Adversarial verification — finding "nfc-antenna: GND pours cover antenna region, no keepout"

Verifier run: 2026-07-03. Sources: the actual `.kicad_pcb`, AN5276 Rev 6 (local PDF), AN2972 Rev 10 (ST web), board stackup section.

## Verdict: CONFIRMED (with two minor factual corrections and a corrected keepout extent)

## 1. Zone geometry — VERIFIED

Parsed all `(zone ...)` blocks in
`/Users/vincenzo/Documents/GitHub/nSealr/hardware/pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_pcb`:

| zone | net | layer | fill | outline bbox |
|---|---|---|---|---|
| c53bf021 | GND | F.Cu | yes, filled | x[11.24, 52.76] y[31.60, 70.20] |
| 8a69dca6 | GND | B.Cu | yes, filled | x[11.24, 52.76] y[31.60, 70.20] |
| e7e5c73f | GND | In1.Cu | yes, filled | x[11.24, 52.76] y[31.60, 70.20] |
| ec8e196e | — (rule area) | F.Cu only | keepout | x[26.73, 29.27] y[37.87, 39.13] |

- The three GND zones have identical 8-point outlines matching the claimed x[11.2,52.8] y[31.6,70.2]. Claim VERIFIED.
- The only rule area in the whole file is the 2.54 x 1.26 mm F.Cu one centered on J7 TC2030 @(28, 38.5) — `(tracks allowed) (vias not_allowed) (copperpour not_allowed) (footprints not_allowed)`. Matches the claim's "only existing F.Cu keepout is the 2.5x1.3 mm TC2030 rule area". No antenna keepout exists on any layer. VERIFIED.

## 2. Actual fill coverage of the antenna region — VERIFIED with one nuance

ANT1 envelope: 42 x 8 mm @(32,33) → x[11,53] y[29,37]; on-board portion y[30.925, 37].
Point-in-polygon sampling of the zones' `filled_polygon` data at (32,33.5), (20,34), (44,34), (32,36), (16,32.5), (48,32.5):

- **F.Cu**: FILLED at all 6 samples; largest filled polygon spans y[31.60, 48.51]. Solid pour co-planar with any future loop.
- **In1.Cu**: FILLED at all samples (single filled polygon covering essentially the whole board). This is the killer: per the stackup section of the .kicad_pcb, "dielectric 1" between F.Cu and In1.Cu is **prepreg 0.18 mm** — the claim's "solid GND ~0.2 mm below" is accurate.
- **B.Cu — CORRECTION**: the B.Cu zone *outline* includes the band, but its current *fill* does not reach it. Topmost B.Cu filled polygon starts at y=41.33 (bboxes: y[41.33,70.20], y[45.09,57.84], y[43.24,51.62]). Today there is no B.Cu copper in the antenna band — the fill island there was removed for lack of connection. The finding's "GND pours on F.Cu, B.Cu AND In1 ... cover the whole antenna region" is therefore overstated for B.Cu **as filled today**. However this does not weaken the finding: 40 GND connections are still open and via stitching is pending; as soon as any GND via lands in the top band, the B.Cu fill will flow back in. A B.Cu keepout is still required.

## 3. Copper objects in the band — counts corrected, substance VERIFIED

Track/via extraction (KiCad 10 `(net "NAME")` format; 926 segments, 129 vias total):

- Strict ANT1 envelope x[11,53] y[29,37] (endpoint or intersection test — same result): **22 F.Cu segments, 5 In2.Cu segments, 3 vias** (VBUS @26.26,35.89; NFC_VDD_AM @36.72,36.15; SWCLK @31.37,35.72). No track arcs exist in the file.
- Recommended keepout rect x[14.2,49.8] y[30.9,38.6]: **31 F.Cu, 9 In2.Cu, 5 vias** (adds NFC_XTO @48.91,38.11 and SWDIO @27.37,37.22).
- The claimed "25 F.Cu / 6 In2 / 4 vias" sits between the two band definitions — a counting-window difference, not a factual error. Offending nets: SYS_3V3 (long run at y≈34.7–37.5 straight through the band), SWCLK/SWDIO (to J7), VBUS, NFC_VDD_AM, NFC_AGDC, CHARGER_ITERM, NFC_XTO, TOUCH_I2C_SCL/SDA.

## 4. Citations — VERIFIED verbatim

- **AN5276 Rev 6** ("Antenna design for ST25R3916/16B..." — local PDF `/Users/vincenzo/Downloads/nsealr-datasheets/st25r3916b-antenna-design.pdf`), **section 5.1 "Boundary conditions and simulation model", page 20/44**: "The best case of an antenna placement is far away from electronics or other components like batteries, displays, or large ground planes that harm the effective radiated RF field." Exact quote, exact section, exact page. VERIFIED.
- **AN2972** (ST, "How to design an antenna for dynamic NFC tags", Rev 10 Sep 2025), **section 3.5.2**: "no copper planes above or below the antenna, and no copper planes surrounding the antenna"; Figures 14/15 show flux blocked by overlapping copper (no energy transfer), Figure 16 shows a short-circuited loop *surrounding* the tag as not recommended — which is precisely the "never a closed ring around the aperture" advice. VERIFIED. (AN2972 is written for tags, but the magnetics — image/eddy currents in copper under a 13.56 MHz loop collapsing inductance and Q — apply identically to the ST25R3916B reader loop; AN5276 5.1 is the reader-side statement.)

## 5. Physics sanity check

A solid plane 0.18 mm (In1) below a 13.56 MHz PCB loop produces near-perfect image-current cancellation of the magnetic flux: L and Q collapse, radiated field ≈ 0. "Magnetically shorted" is a fair engineering description. No ferrite-sheet workaround is plausible at 0.18 mm within a 1.53 mm stackup.

## 6. Recommendation assessment — direction right, extent wrong

- The proposed keepout **x[14.2, 49.8] is narrower than the ANT1 envelope (x 11–53, 42 mm wide)**. If the loop uses the documented envelope ("Centered upper 13.56 MHz NFC antenna keepout/envelope; documented envelope 42.00 x 8.00 mm", .kicad_pcb line 15922), copper would sit under the outer turns on both sides. Either (a) the keepout must span the full envelope + 1 mm margin, i.e. effectively the full board width at y ≤ ~38.5 (the zone edge-clearance already stops copper at x=11.24/52.76), or (b) the loop must first be formally shrunk below 42 mm and the keepout sized to the *final* loop outer dimension + 1 mm, not to the aperture only — copper under the traces detunes too (AN2972 3.5.2 says no copper below the antenna, not merely below its aperture).
- Multi-layer rule area (no copper pour / no tracks / no vias) on all 4 copper layers is correct and expressible as a single KiCad rule area with all copper layers selected. y from the top board edge (30.925) down to ~38.5 leaves the TC2030 rule area and J7 pads just outside.
- Feed exception: correct in principle, but note none of the tracks currently in the band are the antenna feed — RFO1/RFO2 matching from U9 @(40.17,48) is not routed yet (NFC nets are among the 69 opens). NFC_VDD_AM / NFC_AGDC are supply/measurement nets and must be rerouted out of the band like the rest.
- Spoked/slotted pour outside the aperture: consistent with AN2972 Fig 16/17 (no closed conductive ring around the loop). Sound.
- Rerouting scope: 22–31 segments + 3–5 vias depending on final keepout rectangle (list above), all reroutable southward; SYS_3V3 and SWD runs are the bulk.

## Files
- Board: /Users/vincenzo/Documents/GitHub/nSealr/hardware/pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_pcb (zones at the four uuids above; stackup lines 52–92: F.Cu 35 um / prepreg 0.18 / In1.Cu / core 1.12 / In2.Cu / prepreg 0.18 / B.Cu)
- AN5276 Rev 6 local: /Users/vincenzo/Downloads/nsealr-datasheets/st25r3916b-antenna-design.pdf (sec 5.1 p.20/44)
- AN2972 Rev 10: https://www.st.com/resource/en/application_note/an2972-how-to-design-an-antenna-for-dynamic-nfc-tags-stmicroelectronics.pdf (sec 3.5.2, Fig 13–17)
