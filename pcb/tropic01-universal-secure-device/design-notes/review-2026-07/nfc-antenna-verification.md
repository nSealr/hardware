# Adversarial verification — Finding "nfc-antenna: front-end BOM incomplete"

Verdict: **CONFIRMED** (claim substantially holds; two sub-claims corrected; one additional wiring bug found during verification).

Verification date: 2026-07-03. Sources: the real board file, DS13541 Rev 11 (local PDF), AN5276 Rev 6 (local PDF `st25r3916b-antenna-design.pdf`), Trezor Safe 7 rev D main schematic (fetched from `trezor/trezor-hardware@master`, sheet 10 "NFC Reader").

## 1. What is actually on the board (measured, not from notes)

File: `/Users/vincenzo/Documents/GitHub/nSealr/hardware/pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_pcb`

### 1a. U9 (ST25R3916B-AQET, QFN32 @40.17,48) pad-to-net map (extracted from pad `(net ...)` fields)

| Pad | DS13541 Table 2 name | Net on board |
|---|---|---|
| 1 | VDD_IO | NFC_VCC |
| 2 | TAD1 | NO_NET (ok, test) |
| 3 | VDD_D | NFC_VDD_D |
| 4/5 | XTO/XTI | NFC_XTO / NFC_XTI |
| 7 | VDD_A | NFC_VDD_A |
| 8 | VDD | NFC_VCC |
| 9 | VDD_RF | NFC_VDD_RF |
| 10 | VDD_TX | NFC_VCC |
| 11 | VDD_AM | NFC_VDD_AM |
| **13/15** | **RFO1/RFO2** | **NO_NET** |
| **14** | **VDD_DR** | **NFC_VCC** (see bug, §4) |
| 17 | EXT_LM | NO_NET (ok) |
| 18/19 | AAT_A/AAT_B | NO_NET |
| 20 | I2C_EN | GND (correct for SPI, DS Fig.1) |
| **22/23** | **RFI1/RFI2** | **NO_NET** |
| 24 | AGDC | NFC_AGDC |
| 25 | TAD2 | NO_NET (ok) |
| 27, 29-32 | IRQ, SPI | NFC_IRQ / NFC_SPI_* |

The entire TX/RX RF path (RFO1, RFO2, RFI1, RFI2) is **not in the netlist at all** — worse than "unrouted": these pads are net-less, so they do not even appear among the 69 open connections.

### 1b. Front-end passives

- L30, L31 (`L_0402_1005Metric`, value `NFC_TUNE`) — **all pads NO_NET** (placeholders).
- C30-C33 (`C_0402`, value `NFC_TUNE`) — **all pads NO_NET** (placeholders). C31/C33 sit near ANT1 (32,32/32,34), C30 near L30 (40,58), C32 stranded at (51.5,55.5).
- ANT1 = envelope footprint with **zero pads**, no copper.
- With 2 L + 4 C you cannot implement even the minimal differential chain L0x2 + C0x2 + Csx2 + Cpx2 (needs 2 L + 6 C), before any RX divider/damping. The claim "Cp missing" holds under any assignment of the 4 caps.
- No refs anywhere for Cr1/Cr2, Cd1/Cd2, Rd1/Rd2 (checked whole PCB and all sheets).

### 1c. Supply decoupling — the one factual error in the finding

The finding says supply blocking caps are "missing". **They are not entirely missing.** Present and net-assigned on the PCB:

| Ref | Value | Net | DS13541 recommendation |
|---|---|---|---|
| C36 | 100nF | NFC_VDD_D | 2.2uF ‖ 10nF |
| C37 | 100nF | NFC_VDD_A | 2.2uF ‖ 10nF |
| C38 | 100nF | NFC_VDD_RF | 2.2uF ‖ 10nF (Trezor: 2x pairs on VDD_RF_DR) |
| C39 | 2.2uF | NFC_VDD_AM | 2.2uF NOM + **22nF NOM for AWS AM** (22nF absent) |
| C40 | 100nF | NFC_AGDC | 1uF ‖ 10nF |
| C41 | 100nF | NFC_VCC | (VDD/VDD_TX/VDD_IO rail; Trezor uses bulk pairs) |

Also present: X3 27.12MHz FA-238 3225 on NFC_XTO/XTI with C34/C35 (value placeholder `NFC_XTAL_LOAD`); U13 TPS22917 gate with C8 1nF CT-to-VIN (correct per TI DS: "Connect capacitor from this pin to VIN"); RJ2 0R NFC_VCC_SW→NFC_VCC. NFC_VCC_SW (switch output rail) has **no output/bulk capacitor at all**.

So the correct statement is: every regulator pin has a single 100nF (except VDD_AM's 2.2uF), i.e. the **networks** recommended by DS13541 §4.2.10 are incomplete (missing all 2.2uF bulks on A/D/RF_DR, all 10nF companions if 100nF→10nF swap isn't accepted, the 1uF on AGDC, the 22nF AWS on AM, and any bulk on VCC/VCC_SW). Net count of parts to add: 6-9 — the finding's "~7-9" count is right; its "missing" wording is wrong.

### 1d. Schematic state (this makes the finding stronger)

`kicad/sheets/optional_profiles.kicad_sch` (311 lines, read in full) contains **only** U9 as a 15-pin "source-backed pin subset" symbol (pins 1,6,8,10,12,16,20,21,26,27,29,30,31,32,33). The symbol **omits RFO1/RFO2, RFI1/RFI2, VDD_A, VDD_D, VDD_RF, VDD_DR, VDD_AM, AGDC, XTI/XTO, AAT_A/AAT_B, EXT_LM, TAD1/2 entirely**. None of L30/L31, C30-C41, X3 exist in any schematic sheet (grepped all 7 sheets + root): the NFC passives are PCB-only hand edits. Any fix must start by replacing the schematic symbol with a full 33-pad one and back-annotating C36-C41/X3/C34-C35.

## 2. Evidence check — every citation in the finding

1. **DS13541 Rev 11 §4.2.10 p.37-38** — VERIFIED VERBATIM. Extracted text (p.37/167-38/167): "For regulators recommended blocking capacitors are 2.2 μF in parallel with 10 nF, for pin AGDC 1 μF in parallel with 10 nF is suggested." Section header "4.2.10 Power supply system" confirmed.
2. **DS13541 Fig.1/Fig.2 note** — VERIFIED: "2.2 μF NOM for regulator AM and 22 nF NOM for AWS AM" (p.13-14). Also §4.2.10 VDD_AM paragraph: "Additionally, 100pF to 2.2nF can be used to improve RF decoupling."
3. **AN5276 Rev 6 §3.3** — VERIFIED: "The filter cutoff frequency should be between 8 and 17 MHz"; "the EMC cutoff frequency must not be comprised between 13 and 14 MHz"; "EMC inductors with a higher ESR (>1 Ω) can only be used for mid and low power matchings"; "Rated current of the chosen filter coils must be higher than the current in the matching network" (p.12/44). fc(270nH, 680pF) = 11.75 MHz — inside 8-17, outside 13-14: the proposed L0/C0 starting values are arithmetically sound.
4. **AN5276 §3.4** — matching network is "one series and two parallel capacitors, in differential topology" → Cp is a required element. §3.5 — VERIFIED: "The voltage at the receive pins must not exceed 3 Vpp. In HF reader mode and NFC transmit mode, the recommended signal level is 2.8 Vpp"; divider = two capacitors per RFI input.
5. **Trezor Safe 7 rev D sheet 10** (ts7_main_rev_d_sch.pdf, "TS7_Radio_NFC.SchDoc", 2025-10-23) — VERIFIED with minor corrections: L5/L6 = 270n; EMC/divider caps C77/C83 = 680p; Cs C71/C76 = 150p; **Cp C105/C106 = 68p (finding said 70p)**; Rdamp R37/R38 = 2R; divider series C78/C84 = 180p; supply networks: VDD_RF_DR (pins F6+E3 tied together!) = **2x (2u2‖10n)** C67-C70; VDD_AM = **4u7‖10n** C72/C73 + 22n C75 (the finding attributed the 4u7‖10n to RF_DR — it is on VDD_AM); VDD_D = 2u2‖10n C79/C80; VDD_AGD = 1u‖10n C81/C82; VDD_A = 2u2‖10n C87/C88; crystal 27.12MHz 2.0x1.6mm CL=8pF with 10p loads C89/C90.

## 3. Sub-claims that are interpretation, not fact (kept, flagged)

- "L-match recalc for our La=400 nH gives Cs~180p/Cp~240p": the antenna does not exist (ANT1 is a padless envelope), so La=400nH is an assumption. Values are plausible for a low-turn 42x8mm loop (Trezor's La~1uH coil uses 150p/68p; lower La → larger caps) but cannot be verified; the finding itself marks them `tuning_required`, which is the correct posture.
- 0402→0603/0805 inductor upgrade: supported by AN5276 §3.3 ESR/current requirements (typical 0402 multilayer 270nH parts have ESR well above 1 Ω and Irms ≈100-150mA); strictly mandatory only for full-power matching, but correct as a default for a reader that must drive through a display/battery stack.
- AAT DNP provision (AN5322/MB1414): consistent with AAT_A/AAT_B pads (18/19) currently NO_NET; reasonable optional provision, not verified in depth.

## 4. NEW bug found while verifying (adjacent, same area)

**U9 pad 14 (VDD_DR) is tied to NFC_VCC (the raw VDD/VDD_TX rail), while pad 9 (VDD_RF) is a separate net (NFC_VDD_RF) carrying only C38.** DS13541 §4.2.10 (p.38): VDD_DR is the antenna-driver supply input fed from the VDD_RF regulator; the only sanctioned alternative is "VDD_RF and VDD_DR have to be externally connected to VDD_TX" **together** (>350 mArms case; "connection of VDD_RF to supply voltage higher than VDD_TX is not allowed"). Trezor ties F6+E3 into one net VDD_RF_DR. The current split (driver on raw rail, regulator output floating into a lone 100nF) defeats the VDD_RF regulator/PSRR entirely and is not a supported topology. Fix: net-tie pad 14 to NFC_VDD_RF (rename NFC_VDD_RF_DR), keep decoupling at both pads.

## 5. Corrected recommendation

1. Fix schematic first: replace the 15-pin U9 subset symbol with a full 33-pad ST25R3916B symbol; back-annotate the PCB-only parts (X3, C34-C41, L30/L31, C30-C33) into `optional_profiles.kicad_sch` so ERC/netlist parity is real.
2. Rewire VDD_DR: connect U9 pad 14 to NFC_VDD_RF (one net VDD_RF_DR, Trezor-style), NOT to NFC_VCC.
3. Supply networks — **upgrade, don't add from scratch**: VDD_A (C37) and VDD_D (C36) → 2.2uF‖10nF each; VDD_RF_DR → 2.2uF‖10nF (Trezor uses two pairs, one per pin); VDD_AM → keep C39 2.2uF, add 22nF (AWS) and optionally 100pF-2.2nF RF decoupling; AGDC (C40) → 1uF‖10nF; add bulk (>=2.2uF‖100nF) on NFC_VCC and an output cap on NFC_VCC_SW (currently none).
4. RF path — as in the original finding: assign nets to L30/L31/C30-C33 and add the missing refs: Cp x2, Cr1/Cr2 (180pF start), Cd1/Cd2 (680pF start), Rd1/Rd2 (0R start, 2R provision). Starting values L0=270nH / C0=680pF (fc=11.7MHz) confirmed sound; Cs/Cp start 180p/240p acceptable but meaningless until ANT1 becomes real copper — mark all `tuning_required`.
5. L30/L31 to 0603/0805, ESR<0.5-1Ω, Irms above matching current (AN5276 §3.3); antenna-node caps C0G/NP0 >=50V.
6. Optional: DNP AAT varicap provision on pads 18/19 per AN5322.

## Files/paths referenced

- Board: `/Users/vincenzo/Documents/GitHub/nSealr/hardware/pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_pcb`
- NFC sheet: `/Users/vincenzo/Documents/GitHub/nSealr/hardware/pcb/tropic01-universal-secure-device/kicad/sheets/optional_profiles.kicad_sch`
- DS13541: `/Users/vincenzo/Downloads/nsealr-datasheets/st25r3916b-datasheet.pdf` (Rev 11; §4.2.10 p.37-38; Table 2 p.20-21; Fig.1/2 p.13-14)
- AN5276: `/Users/vincenzo/Downloads/nsealr-datasheets/st25r3916b-antenna-design.pdf` (Rev 6; §3.3 p.12, §3.4-3.5 p.13)
- Trezor: `https://raw.githubusercontent.com/trezor/trezor-hardware/master/electronics/trezor_safe_7/ts7_main_rev_d_sch.pdf` sheet 10 (local copy in scratchpad/trezor/)
