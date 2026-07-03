# Adversarial verification — Finding: ANT1 is a mechanical envelope with zero pads / zero copper (area: dfm-pcbway)

Verdict: **CONFIRMED** (the finding is understated — the entire NFC RF chain is missing, not just the coil).

Verification date: 2026-07-03. All evidence checked against primary sources.

## 1. Claim vs. board file — CONFIRMED

`/Users/vincenzo/Documents/GitHub/nSealr/hardware/pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_pcb`, line 15918:

```
(footprint "nSealr_Mechanical:NFC_Antenna_Envelope_42x8mm"
    (layer "F.Cu") (at 32 33)
    (descr "Centered upper 13.56 MHz NFC antenna keepout/envelope; documented envelope 42.00 x 8.00 mm")
    ... (attr board_only exclude_from_pos_files exclude_from_bom)
```

Measured content of the ANT1 block (1172 bytes total):
- `(pad ...)` entries: **0**
- `fp_line/fp_rect/fp_poly/fp_arc/fp_circle` graphics: **0** — it is not even a drawn envelope, just an anchor point with hidden text properties.
- Free copper check: **0** `gr_*` graphics on F.Cu anywhere in the file; **0** copper zones other than the three full-board GND pours (see §4) and one small keepout. The only F.Cu tracks intruding into the envelope region (y<37) are 0.2 mm signal traces (JP1/J7/testpoint fanout), not a loop antenna.
- The string `NFC_ANT` occurs exactly **once** in the whole .kicad_pcb — the ANT1 `Value` property (line 15935). No NFC_ANT1/NFC_ANT2 nets exist on the board.

## 2. The RF interface is missing end-to-end (stronger than the original claim)

### 2.1 U9 pads on the PCB (footprint block at line ~4849)
Pad→net dump of U9 (QFN32):

| Pad | Datasheet pin (DS13541 Fig. 4, p.19) | Net on board |
|-----|-----|-----|
| 13 | RFO1 (antenna driver out) | **none** |
| 15 | RFO2 (antenna driver out) | **none** |
| 22 | RFI1 (receiver in) | **none** |
| 23 | RFI2 (receiver in) | **none** |
| 17/18/19 | EXT_LM / AAT_A / AAT_B | none |
| 12/14/16 | GND_DR1 / VDD_DR / GND_DR2 | GND / NFC_VCC / GND (consistent, confirms pin mapping) |

### 2.2 Schematic
- `kicad/sheets/optional_profiles.kicad_sch`: the U9 symbol is explicitly a "ST25R3916B NFC/RFID front-end, QFN32 **source-backed pin subset**" — grep for `RFO|RFI|NFC_ANT` across all seven sheets returns **zero** pin or net hits (only two note strings). No EMC filter, no matching caps, no RX divider components exist on the sheet.
- The sheet itself documents the gap: `"Antenna nets remain measurement-gated until FPC/matching/enclosure are finalized."` (line 45).

### 2.3 The project's own contracts already require what is missing
- `production/netlist-contract.json` → `required_buses.nfc_spi` includes **`NFC_ANT1`, `NFC_ANT2`**; `release_gates` includes **`nfc_matching_network_measured_with_final_antenna`**.
- `production/schematic-binding.json` → `review_required_nets.NFC_ANT1/NFC_ANT2`: `"review_status": "explicitly_unbound"`, reason `"Antenna FPC and matching network must be tuned with final mechanics and enclosure."`
- `production/pcbway-manifest.json` lists `ANT1` under `required_non_pcba_rows` and is `status: "blocked"`.
- `production/placement-plan.json` line 10: `"ANT1 TOP EDGE NFC ANTENNA FPC OR TUNED KEEP-OUT"` — a PCB-coil vs FPC-antenna decision was deferred and never made.

## 3. Datasheet / app-note requirements — the antenna is not optional

- **DS13541 Rev 11 (ST25R3916B datasheet), §2.1 System diagram, p.13-14**: "Figure 1 and Figure 2 show the **minimum system configuration** for, respectively, single ended and differential antenna configurations. **Both include the EMC filter**." Both figures terminate RFO1/RFO2 into an antenna coil and return RX to RFI1/RFI2. QFN32 pinout confirming pin numbers: Figure 4, p.19 (RFO1=13, VDD_DR=14, RFO2=15, RFI1=22, RFI2=23, AGDC=24).
- **AN5276 Rev 6 (Antenna design for ST25R3916/16B...), §3 Antenna interface stage, p.8**: "From the ST25R3916 antenna driver output pins RFO1 and RFO2, the TX signal goes through the EMC filter into the matching network and to the antenna. The RX signal coming from the antenna is led through the capacitive voltage divider back into the ST25R3916 receiver input pins RFI1 and RFI2." Required blocks: EMC filter (§3.3, L_EMC1,2 + C_EMC1,2), matching network (§3.4, C_S1,2 + C_P + R_Q), capacitive voltage divider (§3.5), antenna coil (§3.6). Matching values must be derived from a **measured** coil (§4 antenna parameters via network analyzer; §6 STSW-ST25R004 matching tool; §7 design verification).

Local PDFs: `/Users/vincenzo/Downloads/nsealr-datasheets/st25r3916b-datasheet.pdf`, `/Users/vincenzo/Downloads/nsealr-datasheets/st25r3916b-antenna-design.pdf` (AN5276 Rev 6, May 2023, 44 pp).

## 4. Two additional facts that break the recommendation as given

1. **GND pours flood the envelope on 3 of 4 layers.** The .kicad_pcb contains full-board GND zones on F.Cu, B.Cu and In1.Cu, all with identical polygon `(xy 14.74 31.6) (xy 49.26 31.6) ...` — i.e. copper fill starts at y=31.6 and spans the full width, directly inside the antenna envelope region (envelope y=29..37). A 13.56 MHz loop drawn on F.Cu over a solid In1 GND plane ~0.2-0.3 mm below (and B.Cu below that) would have its inductance and Q gutted by eddy-current image currents; AN5276's coil model (§5) assumes no adjacent solid plane. The only existing keepout zone is elsewhere (x 26.7–29.3, y 37.9–39.1, near JP1/J7). A copper + plane keepout on **all** layers under the coil is mandatory.
2. **The envelope hangs 1.93 mm off the board.** Envelope 42x8 mm centered at (32,33) spans y=29..37; the board top edge is y=30.925. Only ~42 x 6.08 mm of the envelope is actually on the PCB. Any on-board coil must fit ~6 mm of height (plus clearance to the y=31.6 pour edge, which must be pushed down anyway), or the outline/envelope must be re-anchored. Note also the LiPo battery sits immediately above the top edge per mechanical-architecture.md — its foil pouch is another detuning surface to keep clear of.

## 5. Verdict and corrected recommendation

**CONFIRMED.** ANT1 at (32,33) has 0 pads and 0 copper primitives; no antenna copper, no NFC_ANT1/2 nets, and U9's RFO1(13)/RFO2(15)/RFI1(22)/RFI2(23) pads are netless. The board cannot provide NFC as fabricated, and the project's own release gate (`nfc_matching_network_measured_with_final_antenna`) and required bus (`NFC_ANT1/2`) cannot be satisfied.

The original recommendation ("draw the coil, retune the U9 matching network") presupposes a matching network that **does not exist**. Corrected sequence:

1. **Decide coil vs FPC** (placement-plan.json already frames the choice). Given only ~6 mm on-board height and the battery directly above, an off-board FPC/wire antenna in the enclosure may outperform a PCB coil; if PCB coil, a ~40 x 5.5 mm 3-4 turn rectangular loop is feasible per AN5276 §5 (Fig. 13-17 size/trace/gap tradeoffs).
2. **Schematic first**: extend the U9 symbol to the full RF pin set and add the AN5276 §3 differential chain — EMC filter (L_EMC1/2 + C_EMC1/2), matching (C_S1/2, C_P1/2, R_Q), capacitive RX divider into RFI1/RFI2 — creating nets NFC_ANT1/NFC_ANT2 as required by netlist-contract.json. Seed values from the STSW-ST25R004 matching tool.
3. **Board**: replace the padless ANT1 footprint with a real antenna footprint (two pads on NFC_ANT1/2), re-anchor it fully inside the outline, and cut copper/plane keepouts on all 4 layers under the coil (pull the y=31.6 GND pour edges below the coil area). Place the EMC filter and matching parts adjacent to U9 pins 13/15.
4. **Then** fabricate a tuning spin, measure the real coil (AN5276 §4/§7, network analyzer), finalize matching values, and only then treat the `nfc_matching_network_measured_with_final_antenna` gate as passable. Keep matching footprints 0402 with DNP flexibility.
