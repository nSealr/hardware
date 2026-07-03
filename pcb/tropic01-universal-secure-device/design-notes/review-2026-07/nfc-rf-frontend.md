# NFC / RF Front-End Review — ST25R3916B reader antenna (ANT1) and matching chain

Reviewer scope: 13.56 MHz reader antenna + EMC/matching network + crystal + supplies + EP grounding.
Date: 2026-07-03. Board: `hardware/pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_pcb` (KiCad 10, 4-layer 1.6 mm, F.Cu / In1=GND / In2 / B.Cu).

Evidence base (all verified, not taken from design notes):
- **AN5276 Rev 6** "Antenna design for ST25R3916/16B…" (local: `/Users/vincenzo/Downloads/nsealr-datasheets/st25r3916b-antenna-design.pdf`, extracted text `scratchpad/pcb-review/an-antenna.txt`)
- **DS13541 Rev 11** ST25R3916B datasheet (local PDF + extracted `ds-st25r3916b.txt`)
- **Trezor Safe 7 rev D** open hardware: `ts7_main_rev_d_sch.pdf` p.10 ("NFC Reader" sheet, rev B) + `ts7_fpc_ant_rev_d_sch.pdf` / `ts7_fpc_ant_rev_d_views.pdf` (antenna FPC)
- ST eDesignSuite NFC Inductance / Tuning calculators ([eds.st.com/antenna](https://eds.st.com/antenna/)), STSW-ST25R004 matching tool ([st.com](https://www.st.com/en/embedded-software/stsw-st25r004.html))
- ST25R3916-DISCO (MB1414 antenna daughterboard) — [product page](https://www.st.com/en/evaluation-tools/st25r3916-disco.html), ST community thread linking DISCO-size antenna to **La ≈ 886 nH** with 15 Ω target matching (AN5592 context)
- Würth WE-FSFS ferrite sheets — [product family](https://www.we-online.com/en/components/products/WE-FSFS), ANP022 ([element14 copy](https://community.element14.com/products/manufacturers/wuerth-elektronik/w/documents/3558/anp022-selection-and-characteristics-of-we-fsfs)), 374006 60×60×0.3 mm ([Mouser](https://www.mouser.com/ProductDetail/Wurth-Elektronik/374006))
- Epson FA-238 27.12 MHz — [FA-238 27.1200MB-W, CL=12 pF](https://www.digikey.ph/en/products/detail/epson/FA-238-27-1200MB-W/7727147) and [FA-238 27.1200MB-C, CL=18 pF](https://www.digikey.com/en/products/detail/epson/FA-238-27.1200MB-C/7727144)

---

## 0. Ground truth measured from the board (what actually exists today)

| Item | State (measured from .kicad_pcb) |
|---|---|
| ANT1 | Placeholder footprint `NFC_Antenna_Envelope_42x8mm` @ (32, 33) F.Cu, **no copper, no pads, no nets**. Drawn envelope bbox is actually **21.4 × 4.4 mm**, not 42×8 (name/graphic mismatch), and its top edge (y=30.8) overhangs the board edge (y=31.0) by 0.2 mm. |
| U9 pads | **All 33 pads NO_NET** (including VDD, GND, SPI, EP). The schematic symbol `TROPIC_SQUARE:ST25R3916B_QFN32` exposes only **15 of 33 pins** (VDD_IO, GND_D, VDD, VDD_TX, GND_DR1/2, I2C_EN, VSS, GND_A, IRQ, BSS, SCLK, MOSI, MISO, EP). Missing from the symbol: **RFO1(13), RFO2(15), RFI1(22), RFI2(23), XTO(4), XTI(5), VDD_A(7), VDD_D(3), VDD_RF(9), VDD_DR(14), VDD_AM(11), AGDC(24), AAT_A(18), AAT_B(19), EXT_LM(17), TAD1(2), TAD2(25), MCU_CLK(28)** (pin numbers per DS13541 Table 2, p.20-21). |
| Front-end passives | C30–C33 = `NFC_TUNE` (no value), C34/C35 = `NFC_XTAL_LOAD` (no value), C36–C38 = 100 nF, C39 = 2.2 µF, L30/L31 = `NFC_TUNE` (no value). **All netless**, scattered: C31 @(32,32) and C33 @(32,34) inside the antenna envelope; C32 @(51.5,55.5); C34 @(50,37.5) — 15.7 mm from X3. |
| X3 | FA-238 27.12 MHz @(45.5,53) rot90, netless. 9.3 mm (euclid) from U9 XTO/XTI pads (~37.7, 48) **with the QFN body in the path**. |
| Zones | GND pours on **F.Cu, B.Cu, In1.Cu** all span x[11.2,52.8] y[31.6,70.2] → they **cover the whole antenna band**. No antenna keepout exists (the only F.Cu keepout is the TC2030's own 2.5×1.3 mm rule area). |
| Copper in the antenna band (y<37.4) | 25 F.Cu segments, 6 In2.Cu segments, 4 vias. |
| Vias under U9 EP | **Zero** vias within 2 mm of U9 center (129 vias total on board). |
| Netlist contract | `production/netlist-contract.json` requires `NFC_ANT1`/`NFC_ANT2` in the `nfc_spi` bus and `NFC_VCC`/`NFC_VCC_SW` power gating — the RF nets are contract-mandated but unimplemented. |

---

## 1. Antenna interface topology (AN5276 §3, Figure 18) — what must be built

Differential drive, per AN5276 and DS13541 Figure 2:

```
RFO1(13) ─L0a─┬─ Cs1 ─┬──[Rd1]──● ANT_A ─────┐
             C0a      │                       │
              │      Cp (differential)     [ LOOP La ]
             GND      │                       │
RFO2(15) ─L0b─┴─ Cs2 ─┴──[Rd2]──● ANT_B ─────┘
             C0b
RX:  ANT_A ── Cr1 ──● RFI1(22) ── Cd1 ── GND
     ANT_B ── Cr2 ──● RFI2(23) ── Cd2 ── GND
```

- EMC filter (L0/C0): single-stage LC low-pass; **cutoff 8–17 MHz but NOT 13–14 MHz** (AN5276 §3.3, p.12-13). Inductor ESR < 1 Ω for full-power matching; rated current > matching-network current.
- Matching: L-topology, one series cap per leg + parallel cap(s) (AN5276 §3.4).
- RX capacitive divider at the antenna terminals; **RFI voltage must not exceed 3 Vpp, recommended 2.8 Vpp** (AN5276 §3.5, p.13).
- Q: system Q must satisfy **Q ≤ 41** for Type-A 106 kbit/s (`Q ≤ 13.56 MHz × 3 µs`, AN5276 p.18); ST recommends targeting much lower (example targets Q=8–20 via RQ = Q·ω·LANT, p.19). Antenna must be *designed* with Q above target and damped down (§3.6).
- Driver: RRFO = 1.7 Ω typ / 4 Ω max output resistance; RRFI = 12–16 kΩ (DS13541 Table 125).

## 2. Concrete manufacturable loop spec (≤42×8 mm strip, F.Cu, 4-layer 1.6 mm)

### Geometry constraints measured from the board
Top edge y=31.0, corner arcs R2.5 with M2 clearance footprints MH3 @(13.10,33.60) and MH4 @(50.90,33.60), courtyards reaching x=14.7 / x=49.3 between y 32.0–35.2. Practical clean aperture after re-floorplan: **x 15.2–48.8, y 31.6–37.6**.

### Recommended loop (primary candidate)
| Parameter | Value |
|---|---|
| Placement | F.Cu (faces the device back cover = tap surface; B.Cu faces the display) |
| Outer envelope | **33.6 × 6.0 mm**, x 15.2→48.8, y 31.6→37.6 |
| Turns | **N = 4** |
| Trace width | **0.4 mm** |
| Gap | **0.3 mm** (bundle width 2.5 mm) |
| Corners | rounded, **R = 1.0–1.5 mm outer** (or 45° chamfer ≥1 mm); no 90° corners |
| Copper | 35 µm (1 oz outer) |
| Feed | exit at bottom edge of loop near x≈34–38, run as tightly-coupled differential pair (0.4 mm / 0.3 mm gap) ≤15 mm to the matching network; adds ~10–20 nH — include in measurement |
| Terminals | `NFC_ANT1`/`NFC_ANT2` (contract nets) |

### Inductance estimate (show the math)
Method: Grover single-turn rectangle formula evaluated at the average turn dimensions with a GMD-equivalent bundle radius, then ×N² (the standard multiturn-bundle approximation behind HF reader antenna calculators; cross-checked against ST's eDS NFC Inductance tool class of formulas, AN2972 §antenna module):

```
L1 = (µ0/π)·[ a·ln(2ab/(r(a+d))) + b·ln(2ab/(r(b+d))) + 2d − 2(a+b) ],  d=√(a²+b²)
a_avg = a_out − W_b ;  b_avg = b_out − W_b ;  W_b = N·w + (N−1)·g ;  r_eq = 0.2235·(W_b + t)
L ≈ N²·L1(a_avg, b_avg, r_eq)
```

Computed candidates (skin depth 17.9 µm @13.56 MHz; Rac = Rdc·K_skin·1.15 proximity):

| Outer (mm) | N | w/g (mm) | **La est.** | trace len | Rac | X_L | **Q_unloaded** |
|---|---|---|---|---|---|---|---|
| 33.6×6.0 | 3 | 0.5/0.35 | 239 nH | 211 mm | 0.54 Ω | 20.3 Ω | ~37 |
| **33.6×6.0** | **4** | **0.4/0.3** | **373 nH** | 277 mm | 0.89 Ω | 31.8 Ω | **~36** |
| 33.6×6.0 | 5 | 0.35/0.25 | 520 nH | 341 mm | 1.25 Ω | 44.3 Ω | ~35 |
| 38.0×6.0 (notched corners) | 4 | 0.4/0.3 | 425 nH | 312 mm | 1.00 Ω | 36.2 Ω | ~36 |

Pick **N=4 → La ≈ 370 nH bare**; expect **+10–30 % from the ferrite backing** and small shifts from battery/back-cover → plan around **La ≈ 400–480 nH installed**. This sits comfortably in AN5276's recommended **200–1500 nH** window (§5.2, p.24-25) — the design note's "1–3 µH" target is not achievable nor needed in a 6 mm-tall strip. Q_unloaded ~35 > target system Q (14–20) → damping resistors control final Q, per AN5276 §3.6/§4.3. For calibration: AN5276's worked example antenna is 926 nH (p.19); the ST25R3916-DISCO antenna is ≈886 nH matched to 15 Ω.

**Verification gate:** after layout, measure La/RSDC/SRF at 1 MHz + SRF with a VNA per AN5276 §4.1–4.3 (S11, 1–300 MHz) **with ferrite + display + battery + back cover assembled**, then run STSW-ST25R004 / eDS Tuning calculator.

## 3. Matching topology + starting component values (our envelope)

Starting point computed for La = 400 nH, antenna Q_installed ≈ 30 (Rp ≈ 1.0 kΩ), target matching impedance 15–20 Ω differential (AN5276 Fig. 4 recommended region). L-match: Q_m = √(Rp/Rm − 1) ≈ 7–8; X_Cs,tot = Rm·Q_m; Cp resonates the remainder.

| Ref (per leg unless noted) | Role | **Start value** | Package | Tuning-gated? |
|---|---|---|---|---|
| L0a/L0b (=L30/L31) | EMC filter L | **270 nH** (e.g. WE-KI/WE-MK, ESR<0.5 Ω, Isat>0.5 A) | 0603/0805 | fixed after fc choice |
| C0a/C0b | EMC filter C | **680 pF** C0G 50 V → fc = 1/(2π√(L0C0)) = **11.7 MHz** ✓ (8–17, ∉13–14) | 0402 | no (recheck only) |
| Cs1/Cs2 | series match | **180 pF** C0G 50 V (calc 160–220 pF) | 0603 | **YES** |
| Cp | parallel match | **240 pF differential** — fit as 2×120 pF leg-to-leg pads + spare parallel pads | 0603 | **YES** |
| Rd1/Rd2 | series damping | **0 Ω** start; 1.8–2.7 Ω if Q>target (Trezor uses 2 Ω) | 0402 | **YES** |
| Cr1/Cr2 | RX series (RFI) | **180 pF** C0G | 0402 | **YES** (scope: RFI ≤3 Vpp, aim 2.8 Vpp) |
| Cd1/Cd2 | RX shunt (RFI→GND) | **680 pF** C0G (ratio ≈0.21) | 0402 | **YES** |

Sanity anchor — Trezor Safe 7 (La = 1 µH coil) ships: Lemc 270 nH, Cemc 680 pF, Cs 150 pF, Cp 70 pF, Rdamp 2 Ω, Cdiv 180 pF (+680 pF shunts, +10 pF trims). My analytic L-match on their numbers reproduces their table (Cp calc 72 pF vs 70 pF; Cs calc ~132 pF/leg vs 150 pF), so the same procedure applied to our smaller La gives the values above. All antenna-node caps ≥50 V C0G (node can reach tens of Vpp at Q≈20).

**BOM gap (finding):** the board provides only L30, L31, C30–C33 → per the table we are missing at minimum **2×Cp pads, 2×Cr, 2×Cd, 2×Rd** (6 caps + 2 res). Optional but recommended: AAT varicap network on AAT_A/AAT_B (as on MB1414/DISCO) as DNP provision — valuable given battery/display proximity detuning; see AN5322.

## 4. Ground keepout, battery, ferrite

### Keepout (mandatory)
- **Void ALL copper under the loop + 1 mm beyond its outer edge on every layer: F.Cu (except the loop itself), In1.Cu GND plane, In2.Cu, B.Cu.** Today all three GND pours cover the region; In1 sits ~0.2 mm below F.Cu — a solid plane there acts as a shorted turn (AN5276 §5.1 p.20 explicitly lists "large ground planes" with batteries and displays as field killers; AN2972 shows the no-copper-overlap rule; independent guides quote 30–50 % inductance loss over solid ground).
- Implement as KiCad rule areas on all 4 layers: **no copperpour, no tracks, no vias** (exception: the differential feed crossing at the loop entry). Keep the keepout *inside* aperture too (the loop's inner window), not just under traces.
- Reroute the 25 F.Cu + 6 In2.Cu segments and 4 vias currently in y<37.4.
- **Spoke/hatch alternative:** if mechanical rigidity or plane integrity demands copper nearer the loop, a *radially slotted* (spoked) pour — slots perpendicular to the loop conductor, 0.5 mm slots every 3–5 mm, connected only at the outer rim — breaks the eddy loop while retaining some plane. This recovers only part of the loss; prefer the full void. Never leave a closed conductive ring (including a stitching-via ring) around or under the aperture.

### Battery (coplanar above the top edge)
The LiPo is **not behind** the loop; it is coplanar, above the board top edge, inside the display outline. Its foil pouch edge will sit ~1.5–2.5 mm in-plane from the loop's top leg. In-plane conductors mainly clip the fringing field: expect a small L/Q reduction and a resonance shift of tens of kHz — far less severe than a stacked battery, but it **must be present during first-article VNA measurement and tuning**. Keep the battery tabs/nickel strips routed away from the top-center zone if possible.

### Ferrite sheet (required)
The display module (metal frame of the ER-TFT024IPS-3) spans the full 59.26 mm height, i.e. it sits directly behind the antenna region on the B.Cu side at ~1–3 mm. With all PCB layers voided, that frame becomes the nearest eddy-current sink.
- **Fit a flexible sintered ferrite sheet on the B.Cu surface covering the loop aperture + 1 mm margin ≈ 36 × 8 mm.**
- Part family: **Würth WE-FSFS**, 364-material (µ′ ≈ 110–120 at 13.56 MHz, low µ″ — recommended for 13.56 MHz RFID by Würth ANP022). Concrete: cut from **WE-FSFS 374006** (60 × 60 × 0.3 mm, 0.38 mm incl. PET+adhesive, laser-scribed 2×2 mm tiles, self-adhesive) or a thinner 0.1/0.2 mm variant of the same family if the display gap is tight. Alternatives: TDK Flexield IFL/IBF series, Kitagawa RFSN.
- Effect: raises La ~10–30 % and adds small loss → **matching values must be finalized with the ferrite installed** (tuning gate).
- The F.Cu side (toward back cover) stays ferrite-free — that is the radiating direction. Back cover must be non-metallic over the antenna window.

## 5. Crystal X3, NFC decoupling, and current placeholders — verification

### X3 27.12 MHz
- DS13541 §4.2.5 (p.32): oscillator runs on 27.12 MHz crystals, regulates XTI amplitude to 1 Vpp, IRQ at 750 mVpp for fast start. No internal load caps documented → external CL per crystal spec.
- **Value "FA-238 27.12MHz" is underspecified.** Epson FA-238 27.12 MHz exists in two CL grades: **FA-238 27.1200MB-W (CL = 12 pF)** and **MB-C (CL = 18 pF)**, ±50 ppm, ESR ≤50 Ω. The BOM must pin the full suffix. Carrier tolerance for NFC (±7 kHz = ±516 ppm) is easily met.
- Load caps C34/C35 (currently valueless `NFC_XTAL_LOAD`): C_each = 2·(CL − C_pin − C_trace). With MB-W (12 pF), pin cap ≈3 pF (Trezor annotates "Cpin = 3 pF" on the same chip) and ~0.5–1 pF trace → **15 pF ±1 starting**. (Trezor uses a CL=8 pF crystal with 2×10 pF — same formula, consistent.) If the 8 pF-class crystal is chosen instead, use 10 pF.
- **Placement is wrong today:** X3 @(45.5,53) is ~9.3 mm from XTO(4)/XTI(5) pads at (37.7, ~48) *with the QFN in between*, and C34 @(50,37.5) is **15.7 mm** from the crystal (C35 @(48.5,54) is 3.2 mm). Required: crystal ≤3 mm from pins 4/5, both load caps ≤2 mm from the crystal pads with direct via-to-In1 grounds; keep the 27.12 MHz island away from RFI1/RFI2 (pins 22/23, right side) and out of the antenna band.

### Supply decoupling (DS13541 §4.2.10, p.37-38 — exact quote: "For regulators recommended blocking capacitors are **2.2 µF in parallel with 10 nF**, for pin AGDC **1 µF in parallel with 10 nF** is suggested"; Fig.1/2: VDD_AM "2.2 µF NOM for regulator AM and **22 nF NOM for AWS AM**")

Required networks vs what exists (C36–C38 = 3×100 nF, C39 = 1×2.2 µF, all netless):

| Pin | Required | Present? |
|---|---|---|
| VDD (8) | 2.2 µF + 100 nF | partially (C39+one 100 nF, unbound) |
| VDD_TX (10) | 100 nF (+ shares bulk; VDD and VDD_TX must be same supply) | 1×100 nF unbound |
| VDD_IO (1) | 100 nF | 1×100 nF unbound |
| VDD_A (7) | **2.2 µF ∥ 10 nF** | **missing** (pin not even in symbol) |
| VDD_D (3) | **2.2 µF ∥ 10 nF** | **missing** |
| VDD_RF (9) + VDD_DR (14) tied | **2.2 µF ∥ 10 nF** (Trezor: 4.7 µF + 10 nF) | **missing** |
| VDD_AM (11) | **2.2 µF** (regulator use) or **22 nF only** (AWS) | **missing** |
| AGDC (24) | **1 µF ∥ 10 nF** | **missing** |

→ ~7–9 capacitors and the corresponding symbol pins/nets are missing. Trezor Safe 7 implements exactly the DS pattern (C67–C70 input, C72/C73 VDD_RF_DR 4.7µ+10n, C75 VDD_AM 22n, C79/C80 VDD_D 2.2µ+10n, C81/C82 AGD 1µ+10n, C87/C88 VDD_A 2.2µ+10n).

### C30–C39 / L30/L31 placeholders vs recommendation
- L30/L31: unvalued → **270 nH** (see §3). Footprint L_0402 is **too small** for a low-ESR 270 nH EMC inductor at full TX power — use 0603/0805 wirewound/multilayer with ESR <0.5 Ω and adequate current rating (AN5276 §3.3: ESR >1 Ω only acceptable for mid/low-power matchings).
- C30/C31 (=C0a/C0b): **680 pF** C0G 0402 50 V.
- C32/C33 (=Cs1/Cs2): **180 pF** C0G, prefer 0603 50 V.
- Missing refs to add: Cp pair, Cr1/Cr2, Cd1/Cd2, Rd1/Rd2 (see §3), plus the 5 supply networks and AGDC (§5).
- C31/C33 currently sit *inside* the antenna envelope at (32,32)/(32,34) — the matching network must live beside U9/the feed, **outside** the keepout.

## 6. Reference designs — how others do it

- **Trezor Safe 7** (same ST25R3916B, WLCSP): antenna is **not on the main PCB** — a dedicated Ø30 mm antenna FPC behind the back cover combines the NFC loop (**L = 1 µH**, 2-3 turns, outermost) with the Qi coil (13.5 µH), joined by a 6-pin BTB connector (BM28B0.6-6DP/2-0.35V); 2 Ω series damping, matching per §3 table; 27.12 MHz 2016 crystal CL=8 pF + 2×10 pF right at the chip. Lesson: in a battery+display sandwich, decoupling the antenna from the main board's planes (FPC on the back cover) is the robust solution — a valid fallback here if the top strip can't be cleared: keep `NFC_ANT1/2` on a small connector and move the loop to an FPC on the back cover.
- **ST25R3916-DISCO (MB1414)**: etched PCB antenna, **La ≈ 886 nH**, matched to 15 Ω, with the VHBR tuning circuit and **AAT varicap** network — ST's own boards budget for automatic antenna tuning; our AAT_A/AAT_B are currently unexposed/unused. Antenna daughterboard has no ground plane under the loop.

## 7. EP grounding (QFN32 5×5, EP 3.45×3.45)

DS13541 Table 2 pin 33: **"Thermal pad (GND)"** — it is both the thermal path and the RF return reference tied to the die substrate (VSS pin 21 = "die substrate potential"). Requirements:
- Solder EP to a GND copper pad; add **≥9 vias (3×3 grid, Ø0.3 mm drill, ~1.0–1.1 mm pitch) inside the EP** stitching F.Cu→In1 GND. Currently there are **zero** vias under U9.
- GND_DR1/GND_DR2 (12/16) carry the antenna driver return — give each its own via to In1 immediately at the pad; keep C0a/C0b ground vias adjacent so the TX loop area is minimal.
- The chip can dissipate ~0.5–1 W during continuous field-on at full power; without the via farm the QFN has no thermal path (all-F.Cu component rule makes In1 the only heat spreader).

---

## Priority actions (ordered)

1. Rebuild the ST25R3916B symbol with all 33 pins (DS13541 Table 2), bind the full front-end in the schematic (`NFC_ANT1/2` per netlist contract), re-import the netlist so U9/X3/C3x/L3x pads stop being netless.
2. Clear the top strip (J9, J6, TP_UART_GND, C1, C40, C31/C33 out of y<38.6) — re-floorplan gate; then draw the loop per §2 and the 4-layer keepout per §4.
3. Add the missing passives (§3, §5) with the starting values; mark Cs/Cp/Cr/Cd/Rd and C34/C35 `tuning_required`.
4. Move X3 + load caps next to pins 4/5; pin the FA-238 CL suffix in the BOM.
5. EP via farm + driver-ground vias (§7). Ferrite sheet part into the BOM/mechanical stack (§4).
6. First-article: VNA measurement per AN5276 §4 with full mechanical stack, run STSW-ST25R004, trim, scope-check RFI ≤3 Vpp and Type-A timings vs Q (§7.1–7.3).
