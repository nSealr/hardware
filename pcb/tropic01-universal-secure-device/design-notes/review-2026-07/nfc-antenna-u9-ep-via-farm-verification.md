# Adversarial verification — U9 (ST25R3916B) exposed-pad via farm missing

Verifier run: 2026-07-03. Verdict: **CONFIRMED**.

Finding under test (area nfc-antenna): "U9 exposed pad has no via farm: zero vias exist within
2 mm of U9 center (129 vias total on board). EP is pin 33 'Thermal pad (GND)' and is both the
thermal path and RF/substrate return; the chip dissipates up to ~1 W during continuous field-on
and all components are on F.Cu, so In1 is the only heat spreader."

## 1. Board-file verification (primary source: the .kicad_pcb)

File: `/Users/vincenzo/Documents/GitHub/nSealr/hardware/pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_pcb`

Via extraction (regex on `(via (at x y) (size s) (drill d)`):

- **Total vias parsed: 129** — matches the finding exactly. All are 0.6 mm annular / 0.3 mm drill.
- U9 footprint anchor: `(at 40.1727 48)`, footprint `Package_DFN_QFN:QFN-32-1EP_5x5mm_P0.5mm_EP3.45x3.45mm`.
- Nearest vias to U9 center:
  - (37.769, 50.382) — 3.382 mm
  - (39.433, 51.403) — 3.481 mm
  - (43.750, 47.355) — 3.638 mm
- **Vias within 2 mm of U9 center: 0. Within 3 mm: 0.** Within 5 mm: 11.
- Cross-check for any other vertical GND path: **no through-hole pads of any footprint within
  5 mm of U9** (all neighbors are SMD). The EP genuinely has no vertical connection to the
  In1.Cu GND plane; heat/current must spread laterally on F.Cu at least 3.4 mm to the nearest via.

EP pad definition in U9 (verbatim from the board file):

```
(pad "33" smd rect
    (at 0 0)
    (size 3.45 3.45)
    (property pad_prop_heatsink)
    (layers "F.Cu" "F.Mask")
    (net "GND")
    (zone_connect 2)
)
```

- EP = pad 33, 3.45 x 3.45 mm, net GND, **F.Cu only** — matches the finding's evidence.
- Pads 12, 16, 21 (GND_DR1, GND_DR2, VSS) are all net GND on the board.
- GND zones exist on F.Cu, In1.Cu and B.Cu, so the EP is connected to the F.Cu pour
  (zone_connect 2 = solid), but without vias that pour is the only heat/current path.

## 2. Datasheet verification (DS13541 Rev 11, local extraction `st25r3916b.txt` from
`/Users/vincenzo/Downloads/nsealr-datasheets/st25r3916b-datasheet.pdf`)

- Table 2 pin list (extracted text lines 1015-1065, DS pages 20-21):
  - Pin 33: `NA NA P Thermal pad (GND)` — exact match.
  - Pin 21: `C1,C2,C3 VSS P Ground, die substrate potential` — exact match.
  - Pin 12: `GND_DR1 P Antenna driver ground, including driver VSS`.
  - Pin 16: `GND_DR2 P Antenna driver ground, including driver VSS`.
- Dissipation (DS p.38, "VDD_RF regulator" section): "**The voltage drop of the transmitter
  current is the main source of the ST25R39xxB power dissipation.** This voltage drop is
  composed of a drop in the transmitter driver and of a drop in the VDD_RF regulator."
- Absolute maximum ratings (DS p.143, Table): `IVDD_LDO` max **350 mA** (internal regulator),
  `IVDD_EXT` **500 mA** peak (regulator bypassed), `TJun` max **125 C**. Footnotes 3 and 5:
  "**Provide good thermal management to ensure that junction temperature remains below the
  specified value.**"
- Sanity of the "~1 W" figure: NFC supply is the power-gated `NFC_VCC_SW` rail
  (design-notes/subsystem-5-nfc.md lines 27-33). Even at 3.3 V, worst-case field-on with the
  internal regulator is 3.3 V x 350 mA ~= 1.15 W total draw, the majority dissipated in the
  driver + VDD_RF regulator drop per the DS quote above. "Up to ~1 W" is a defensible
  worst-case ballpark, not refutable; typical matched-antenna reader operation will be lower
  (roughly 0.3-0.7 W) but the DS explicitly requires thermal management at these currents.

## 3. Reference-practice verification

- KiCad official library ships the exact drop-in variant
  `Package_DFN_QFN:QFN-32-1EP_5x5mm_P0.5mm_EP3.45x3.45mm_ThermalVias`
  (`/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints/Package_DFN_QFN.pretty/`):
  **3x3 thru-hole via grid at 1.0 mm pitch, 0.2 mm drill / 0.5 mm annular, pad_prop_heatsink,
  all-layer**, plus F.Paste windowed into 9 x 0.93 mm squares (~65% coverage) to control solder
  wicking into the vias. This independently validates the recommended geometry almost verbatim.
- Trezor Safe 7 main board (production hardware wallet, `ts7_main.txt` line 1653) uses the same
  **ST25R3916B**, i.e. this is a proven chip whose reference implementations (ST X-NUCLEO-NFC06A1
  etc.) all stitch the EP.

## 4. Verdict

**CONFIRMED.** Every factual element of the claim checks out against primary sources:
via count (129), zero vias within 2 mm (nearest 3.382 mm), EP = pin 33 Thermal pad (GND),
pin 21 VSS die substrate, EP 3.45x3.45 on F.Cu only, DS-mandated thermal management with
transmitter drop named as the main dissipation source, and no alternate vertical GND path
(no TH pads within 5 mm). The recommendation is sound; minor refinements below.

## 5. Corrected/refined recommendation

The 3x3 grid at 1.0-1.1 mm pitch with 0.3 mm drills is geometrically valid (outer span
2.0-2.2 mm inside the 3.45 mm EP) and consistent with the board's existing 0.6/0.3 via stack.
Two refinements:

1. Simplest robust fix: swap U9's footprint to the library variant
   `QFN-32-1EP_5x5mm_P0.5mm_EP3.45x3.45mm_ThermalVias` (3x3 grid, 1.0 mm pitch, 0.2 mm drill,
   0.5 mm annular, all-layer) — it also windows F.Paste into 9 pads (~65% coverage), which
   free-standing manually-placed vias would NOT do; 100% paste over open 0.3 mm vias risks
   solder wicking/voiding under the EP. If PCBWay's standard drill floor forces 0.3 mm,
   manually place 9 x 0.6/0.3 vias at 1.0-1.1 mm pitch and reduce EP paste to a windowed
   pattern (or accept minor wicking, as the vias are heatsink-class).
2. Keep the second half of the original recommendation: GND_DR1/GND_DR2 (pads 12/16,
   "Antenna driver ground, including driver VSS" per DS Table 2) and the EMC-filter/matching
   shunt-cap grounds each get their own via to In1 immediately adjacent to the pad, so the
   13.56 MHz TX return loop closes in the plane under the chip rather than detouring >=3.4 mm
   across the F.Cu pour to the nearest existing via.
