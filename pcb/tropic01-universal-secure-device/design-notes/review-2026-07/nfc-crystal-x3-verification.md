# Adversarial verification — Finding: NFC crystal X3 placement/spec (area nfc-antenna)

Verdict: **CONFIRMED** (every factual claim checked against the board file and primary sources; the situation is in fact slightly worse than claimed). Recommendation is sound in substance but needs geometric and scope corrections (see end).

## 1. Claimed distances — verified from the .kicad_pcb (exact pad coordinates)

File: `/Users/vincenzo/Documents/GitHub/nSealr/hardware/pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_pcb`

Extracted absolute pad positions (footprint `at` + rotated pad offsets):

| Pad | Net | Position (mm) |
|---|---|---|
| U9 pad 4 | NFC_XTO | (37.735, 47.750) |
| U9 pad 5 | NFC_XTI | (37.735, 48.250) |
| U9 pad 22/23 | RFI1/RFI2 (unassigned in PCB: NO net on pads) | (42.610, 47.25/46.75) |
| X3 pad 1 | NFC_XTO | (46.350, 54.100) |
| X3 pad 3 | NFC_XTI | (44.650, 51.900) |
| X3 pads 2/4 | GND | (46.35,51.9) / (44.65,54.1) |
| C34 pad 1 | NFC_XTO | (49.520, 37.500) |
| C35 pad 1 | NFC_XTI | (48.020, 54.000) |

Measured distances:
- U9.4 (XTO) -> X3.1: **10.70 mm**; U9.5 (XTI) -> X3.3: **7.82 mm**. Finding's "~9.3 mm" (center-based) is an accurate summary; exact pad-to-pad values bracket it.
- C34 (XTO load cap) pad 1 is **16.0 mm** from X3 center (finding said 15.7 — trivial rounding, same conclusion). C35 (XTI load cap) is close (2.7 mm) — only C34 is stranded.
- "QFN body in the path": geometrically true. The straight line X3.1(46.35,54.1) -> U9.4(37.735,47.75) passes through the U9 body extent (body 5x5 mm centered (40.173,48): x 37.67–42.67, y 45.5–50.5); at x=40.17 the line is at y≈49.6, inside the body.

**Worse than claimed:** NFC_XTO is already partially routed as a ~19 mm loop — F.Cu from X3.1 along y≈54.66, then In2.Cu up the right edge at x=51.19 from y=52.9 to y=40.39, then diagonally to C34 at (49.52,37.5). This run skirts the NFC antenna envelope (ANT1 `NFC_Antenna_Envelope_42x8mm` @(32,33): y 29–37) — C34 itself sits 0.5 mm below the envelope's bottom edge. Neither NFC_XTO nor NFC_XTI is routed to U9 pins 4/5 yet (both appear in the 69 open connections). A 27.12 MHz Pierce loop of this size adjacent to the 13.56 MHz RX field is exactly what the finding warns about.

## 2. C34/C35 have no value — verified, and understated

- PCB footprint Value property for both C34 and C35 is the placeholder string **`NFC_XTAL_LOAD`** (kicad_pcb lines 2561, 16287). No capacitance value anywhere.
- **The schematic does not contain the crystal circuit at all.** The U9 symbol in `kicad/sheets/optional_profiles.kicad_sch` (lines 8–38) is `TROPIC_SQUARE:ST25R3916B_QFN32`, described as a "source-backed pin subset": it exposes only pins 1,6,8,10,12,16,20,21,26,27,29,30,31,32,33 — **pins 4 (XTO), 5 (XTI), 22/23 (RFI1/2), 13/15 (RFO1/2) are absent from the symbol.** No X3/C34/C35 symbol exists in any sheet (`grep -rn '"X3"'` across all .kicad_sch: zero hits). The crystal exists only as PCB footprints with nets hand-assigned to pads — which is why "schematic parity 0" can coexist with an unspecified oscillator.
- **The production BOM omits the parts entirely:** `production/bom/pcbway-bom.csv` has 16 rows (U1–U11, J1/J2/J6/J9, SW1) — no X3, no C34/C35, no passives at all.

## 3. Crystal spec claims — verified against DS13541 Rev 11 (local PDF)

`/Users/vincenzo/Downloads/nsealr-datasheets/st25r3916b-datasheet.pdf`:
- **Section 4.2.5 "Quartz crystal oscillator", p.32** — verbatim: "The quartz crystal oscillator operates with 27.12 MHz crystals" and "A feedback loop is controlling the bias current in order to regulate amplitude on XTI pin to 1 VPP." Exactly as cited in the finding.
- **No internal load caps and no CL/ESR requirement documented anywhere** in the 167-page DS: full-text search for load capacitance hits only the I2C bus C_BUS table (Table 130, p.150). Electrical tables only say "27.12 MHz Xtal connected to XTO and XTI" (notes on pp.~152–157). Figure 2 "Minimum system configuration" (p.14) shows a crystal on XTI/XTO **with two external caps to ground** — external load caps are required and CL must be chosen by the designer.
- Pin assignment Table 2 (pp.20–21) confirms: pin 4 = XTO, pin 5 = XTI, pins 22/23 = RFI1/RFI2 (receiver inputs).

## 4. FA-238 CL-grade ambiguity — verified (DigiKey)

- [FA-238 27.1200MB-W](https://www.digikey.com/en/products/detail/epson/FA-238-27-1200MB-W/7727147): 27.12 MHz, **CL = 12 pF**, ESR 50 ohm max, 3.2x2.5 mm.
- [FA-238 27.1200MB-C](https://www.digikey.com/en/products/detail/epson/FA-238-27-1200MB-C/7727144): same frequency/package, **CL = 18 pF**.
The board value "FA-238 27.12MHz" (X3 Value property, kicad_pcb line 1583) therefore does not determine the load caps. Claim holds exactly.

## 5. Trezor reference claim — verified from primary source

`trezor/trezor-hardware`, `electronics/trezor_safe_7/ts7_main_rev_d_sch.pdf`, sheet 10/16 "NFC Reader" (rev D, 10/23/2025), same ST25R3916B: crystal **X3 27.12 MHz, 2.0x1.6 mm, annotated "CL = 8pF, Cpin = 3pF"**, load caps **C89 = C90 = 10p** to GND. Matches the finding's citation exactly, and validates Cpin ≈ 3 pF for this chip's XTI/XTO (Trezor math: 10p/2 + 3p = 8 pF = CL).

## 6. Recommendation review — sound, with corrections

The direction (crystal <=3 mm from pins 4/5, caps at the crystal with short GND returns, away from RFI 22/23 and the antenna band, pin the MPN and cap values) is correct practice for a Pierce oscillator next to a 13.56 MHz receiver and is consistent with Trezor's implementation. Corrections:

1. **"Left side of U9" is not directly usable.** U1 (LQFP100 @(28,50), courtyard right edge ≈ x 36.2) leaves only ~1.5 mm to U9's left pads (x 37.735). Place X3 below the lower-left corner of U9 instead — target center ≈ (37.5–38.5, 51.3–52.0), pads toward pins 4/5 (which sit at y 47.75/48.25, upper half of the left edge). That yields ~3.5–4.5 mm pin-to-pad, meets the <=3–5 mm intent, keeps the loop away from RFI (right edge) and the antenna band (top). TP_UART_TX/RX @(38,52)/(38,53.5) currently occupy that area and must move — the mechanical spec wants debug features grouped anyway.
2. **Rip up the existing NFC_XTO route** (F.Cu + In2.Cu, x≈51.2 corridor to (49,38)) and move C34 next to X3; today C34 sits 0.5 mm from the antenna envelope with a ~19 mm oscillator trace — strictly worse than the "unrouted" the finding implies.
3. **Fix the data model, not just the PCB:** add XTO/XTI (and RFI/RFO — pads 22/23 currently have no net) to the U9 schematic symbol, add X3/C34/C35 schematic symbols, and add crystal + caps to `production/bom/pcbway-bom.csv` (they are absent entirely).
4. **Values:** FA-238 27.1200MB-W (CL 12 pF, ESR 50 ohm) with C34 = C35 = 15 pF C0G 0402 is a defensible pinning: C_each = 2*(CL − Cpin − Ctrace) = 2*(12 − 3 − 0.7) ≈ 16.6 pF -> 15 pF standard value (residual parasitics close the gap). The Trezor-verified alternative (2.0x1.6 mm CL = 8 pF crystal + 2x10 pF) is equally valid and saves area; either is acceptable, but exactly one must be pinned in schematic + BOM.
