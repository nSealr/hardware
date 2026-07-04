# MCU + Secure Elements Review — STM32U585, TROPIC01, OPTIGA, W25Q128, USB, SWD/testpoints

Board: `/Users/vincenzo/Documents/GitHub/nSealr/hardware/pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_pcb` (measured 2026-07-03).
Evidence sources: STM32U575/585 DS13086 Rev 10 (local PDF), TROPIC01 datasheet ODD_TR01 rev A.11 (tropicsquare__tropic01 repo), TROPIC01 Mini Board TS1702 KiCad reference (tropicsquare__devboards), OPTIGA Trust M DS Rev 3.70 (local PDF), W25Q128JV DS (local PDF), TPS22917 DS (local text), Trezor Safe 7 rev D schematics (scratchpad clone).

Re-verification pass 2026-07-03 (second reviewer): every net-membership, placement and datasheet claim below was independently re-derived from `padnets.json`/`pads.json`, the extracted DS texts, the TROPIC01 Fig 24 page image, the TS1702 netlist XML and OPTIGA DS pp.15-17. Distances quoted as "pad-to-pad" were recomputed; all reproduce within 0.5 mm. **Two findings from the first pass were corrected:** the TROPIC01 47k pull-up is on **SDO/MISO, not CSN** (Section 3), and the OPTIGA PG-USON-10-2 package **does have an exposed pad** (Section 4).

---

## 0. Cross-cutting process finding (affects everything below)

**The schematic sheets contain ONLY the 11 major components** (U1, U2, U5, U9, U11, J1, J2, J9, SW1 + sheet symbols). Verified by extracting every `"Reference"` property from all 7 sheets: `stm32u5_host.kicad_sch` contains only U1; `tropic01.kicad_sch` only U2; etc. All ~90 passives, load switches, ESD, crystals, jumpers and testpoints exist **only as PCB footprints with netlist assignments**. Consequences:

- Cap/resistor values live only in the board file; several are unresolved placeholders: `C18`/`C19` = `HSE_LOAD`, `C30-C35` = `NFC_TUNE`/`NFC_XTAL_LOAD`, `R15` = `BL_SENSE`.
- `production/bom/pcbway-bom.csv` has 15 line items (majors only) — no passive is procurable from the current fab package.
- "Schematic parity 0" is true only for the narrow major-part binding; it is not evidence that the support networks are captured anywhere but copper.

**Action:** back-annotate the full support network into the sheets (or formally declare the PCB the source of truth and generate BOM from it), and resolve every placeholder value before fab.

---

## 1. STM32U585VIT6 (U1, LQFP100 @ (28,50))

### 1.1 Power pin identification (DS13086 Figure 15, LQFP100 non-SMPS pinout, p.100)
LQFP100 non-Q (VIT6 = LDO-only, no SMPS pins): VDD = pins 11, 28, 50, 75, 100; VSS = 10, 27, 49, 74, 99; VBAT = 6; VDDUSB = 73; VSSA/VREF−/VREF+/VDDA = 19/20/21/22; VCAP = 48. No VDDIO2 on this package. Board netlist ties all VDD-class pins to SYS_3V3 and matches this map exactly (VBAT→SYS_3V3 is legal per DS §3.9.1).

### 1.2 Requirement vs. implementation (DS §5.1.6, Figure 24 "power supply scheme without SMPS", p.154-155)
DS requires: n×100nF (one per VDD/VSS pair) + 1×10µF bulk on VDD; 100nF on VDDUSB; 100nF+1µF on VDDA; 100nF+1µF on VREF+; VCAP = 4.7µF, **ESR < 20mΩ @ 3MHz, rated ≥10V**; caps "as close as possible" to pins.

Measured per-pin nearest decoupler (pad-center to cap-center, from pads.json):

| U1 pin | Function | Cap | Value | Distance |
|---|---|---|---|---|
| 6 | VBAT | C50 | 100nF | 2.08 mm |
| 11 | VDD | C51 | 100nF | 2.08 mm |
| 21 | VREF+ | C53 | 100nF | 2.36 mm |
| 22 | VDDA | C52 | 100nF | 1.89 mm |
| 28 | VDD | C54 | 100nF | 2.08 mm |
| 48 | VCAP | C59 | 4.7µF | 1.89 mm |
| 50 | VDD | C55 | 100nF | 2.08 mm |
| 73 | VDDUSB | C56 | 100nF | 2.36 mm |
| 75 | VDD | C56/C57 | 100nF | 1.89 / 3.51 mm |
| 100 | VDD | C58 | 100nF | 1.89 mm |

**Verdict: the 100nF-per-pin plan is complete and well placed (9×100nF, all ≤2.4mm).** VCAP value correct. Gaps vs. Figure 24:
- **No 1µF on VDDA and no 1µF on VREF+** (explicitly drawn in Fig 24). Closest bulk is C17 2.2µF (17.5,58.5), ~4mm from the VDDA corner and shared-purpose. Add 2×1µF 0402 next to C52/C53. VREF+ matters here: VBAT_SENSE uses ADC1.
- **No 10µF VDD bulk near U1** (Fig 24: n×100nF + 1×10µF). Rail-wide bulk today = C16 2.2µF + C17 2.2µF + C2 4.7µF scattered; buck output cap is ~20mm away at the right edge. Add one 10µF 0603 near the U1 bottom row (e.g. next to C59).
- BOM must eventually capture the VCAP ESR/voltage spec (blocked by finding 0).

### 1.3 HSE 16MHz (X1 @ (14,54)) — BROKEN as placed
- PH0/PH1 = pins 12/13, pads at (20.325, 49.5/50.0). X1 HSE pads (HSE_IN at (12.9,54.85), HSE_OUT at (15.1,53.15)) are **6.1-9.2mm** pad-to-pad from pins 12/13 — tolerable per AN2867 but not good.
- Load caps: C18 @ (14,47.5) is **5.9mm** from the X1 HSE_IN pad; C19 @ (26.5,59.5) is **12.6mm** from X1 (it sits in the U1 bottom decoupling row between C54 and R3 — clearly a stray placement). Load caps must sit immediately at the crystal pads with a tight ground loop (AN2867 §layout guidelines; DS §5.3.9 HSE requires CL per crystal spec).
- Values are the literal placeholder string **"HSE_LOAD"** and X1 has no MPN (value "16MHz", Crystal_SMD_3225). CL cannot be computed; the part cannot be bought.
- **Action:** pick the crystal MPN (3225, 16MHz, CL typically 8-12pF, ESR ≤ 80Ω per AN2867 gm margin calc for STM32U5 HSE), compute C18/C19 = 2(CL − Cstray) ≈ 2×(CL−~3pF), move C18/C19 adjacent to X1, and ideally shift X1 ~2mm right toward pins 12/13. Keep GND guard and no signals under the crystal.

### 1.4 NRST (pin 14, pad (20.325,50.5))
- Net: R19 10k pull-up to SYS_3V3 @ (33,37.5) + J7 pin 3. **There is NO capacitor on NRST.** DS Figure 38 "Recommended NRST pin protection" (p.243) shows 0.1µF with note 3: "The external capacitor on NRST must be placed as close as possible to the device." Internal RPU is 30-50k (Table 102), so R19 is redundant (harmless, keep or drop), but the missing 100nF removes parasitic-reset filtering — on a secure device this is also a mild glitch/tamper robustness issue.
- **Action:** add 100nF NRST→GND near pin 14 (left side of U1, e.g. (18.5,45.5) region is free); keep it close to U1, not to J7.

### 1.5 BOOT0 (pin 94 = PH3-BOOT0)
R22 100k → GND strap + JP1 solder jumper → SYS_3V3 for DFU. Correct and conventional. No change.

### 1.6 ADC sense dividers
- **VBAT_SENSE (pin 15 = PC0 = ADC1_IN1): R20 1M / R21 330k divider → source impedance ≈ 248kΩ.** DS Table 106 "Maximum RAIN for 14-bit ADC1" tops out at **470Ω** for the listed sampling configurations (p.246). 248k is 3 orders of magnitude over; readings will be garbage unless a reservoir cap is added. **Action:** add 100nF from VBAT_SENSE to GND at the pin (battery voltage is quasi-DC, so cap+long sampling works), or rescale the divider. Standing drain 3.2µA @4.2V is acceptable.
- **USB_VBUS_SENSE (pin 68 = PA9): R23 100k series from VBUS_LIMITED / R24 1M to GND → ~4.55V at the pin at VBUS=5V.** PA9 has **no ADC channel**, so this can only be a digital VBUS detect (PA9 FT pin, abs max = min(VDD+4, 6) V per Table 21 with VDD up — OK; the 100k series bounds injection). Works, but document the intent; if ADC measurement of VBUS was intended, it is on the wrong pin with the wrong ratio.

### 1.7 Pinmux verification (Figure 15 + AF Tables 27/28)
All verified correct: HSE PH0/PH1 (12/13); TROPIC SPI1 PA4/PA5/PA6/PA7 = CSN/SCK/MISO/MOSI (pins 29-32); NFC SPI2 PB12-PB15 (51-54); TFT SPI3 PC10/PC12 (78/80); OCTOSPI1 Port-E PE10-PE15 = CLK/NCS/IO0-IO3 (pins 41-46); USB PA11/PA12 (70/71); SWD PA13/PA14 (72/76); USART2 PD5/PD6 (86/87); I2C: SE2 on PB6/PB7 (92/93), TOUCH on PB8/PB9 (95/96).

Two pinmux issues:
- **I2C instance allocation is forced:** PB8/PB9 carry **only I2C1** (AF4, no alternative); PB6/PB7 carry I2C1 *and* I2C4. Therefore TOUCH must be I2C1 and **SE2/OPTIGA must be I2C4** — the only valid combination. Consistent with the ledger's "dedicated bus" policy but the instance is not recorded anywhere. Record `SE2 = I2C4 (PB6/PB7 AF)`, `TOUCH = I2C1 (PB8/PB9 AF4)` in `production/pinmux-ledger.json`.
- **RGB LED: LED_G is on pin 9 = PC15 (OSC32_OUT).** PC15 has **no timer AF whatsoever** (AF table: only EVENTOUT) → no hardware PWM, contradicting the ledger topology "MCU active-low sink, PWM colour mixing". PC15 is also a VSW/backup-domain pin: DS note (p.133): "PC13, PC14 and PC15 are supplied through the power switch… speed must not exceed 2 MHz with a maximum load of 30 pF… must not be used as current sources (e.g. to drive a LED)". Sinking (our topology) is permitted at normal drive (DS §5.3.15: "PC13/14/15 have the same sink capability as other GPIOs"), so it will *light*, but only with software PWM on a restricted pin. LED_R = PE3 = TIM3_CH1 (AF2) OK; LED_B = PC1 = LPTIM1_CH1 (AF1) — usable but a LPTIM, awkward with TIM3 mixing. **Action:** move LED_G (and ideally LED_B) to free TIM pins — pins 38/39/40 = PE7/PE8/PE9 are NC; PE9 = TIM1_CH1, PE8 = TIM1_CH1N. Moving LED_G to PE9 also frees PC14/PC15 for a future 32.768kHz LSE (currently absent; RTC runs on LSI — acceptable but note for tamper timestamp accuracy).

---

## 2. USB: J1 (32,66.2) → U7 ESD (41,68.5) → R3/R4 22Ω (30/37.5, 59.5) → U1 PA11/PA12

- CC: R1/R2 5.1k pulldowns (UFP) present ✓, CC1/CC2 also clamped by U7 ch 4/5 ✓. VBUS: U8 TPS2553 limiter ✓ (other reviewer's domain).
- **ESD topology: U7 TPD4E05U06 is placed 9mm to the RIGHT of the connector signal pads.** J1 D+/D− pads are at (31.75/32.25, 61.18); U7 pins 1/2 at (40.6, 67.5/68.0). D+/D− must detour ~11mm to the ESD and ~13mm back, and since only pins 1/2 of the USON-10 are used, each ESD connection is a **tap/stub, not flow-through**. Direct J1→U1 distance is 15.7mm; the current path forces ≈39mm. At FS (12Mb/s, ~4-20ns edges) the stub is electrically small, so this will *function*; the real costs are (a) ESD strikes reach several mm of board trace before clamping, (b) pointless congestion in the USB corner (`USB_DM_CONN` is one of the 69 open nets — reroute is still cheap now). **Action:** move U7 directly between J1 signal pads and R3/R4, e.g. ~(33.5, 63), oriented so D+/D− pass over/by its pins in a flow-through manner; keep U7 GND via-stitched to the In1 plane.
- **Series 22Ω R3/R4:** ST's USB hardware guideline (AN4879) states the STM32 FS transceiver embeds the required output impedance and DP pull-up ("On-chip full-speed PHY", DS §3.50; no external series resistors in ST reference designs, e.g. Nucleo). 22Ω in series will slightly soften edges; usually still passes FS eye. Low-risk: change to 0Ω (keep the footprints) unless a compliance eye test says otherwise. External 1.5k DP pull-up correctly absent (integrated).
- VDDUSB (pin 73) = SYS_3V3 with C56 at 2.36mm ✓ (DS: VDDUSB 3.0-3.6V for USB).

---

## 3. TROPIC01 (U2 TR01-C2P-T301, QFN32 0.4mm pitch @ (23.34,64) rot -90)

Reference: TROPIC01 DS rev A.11 §3 (pinout), §11 Figure 24 "Typical application schematic" (p.63); TS1702 Mini Board KiCad; Trezor Safe 7 rev D sheet 11 (TS7_SE_Tropic).

- **Pinout/tie-off audit vs DS Table 1 + Fig 24: PERFECT match.** VCC = 1/11/22*/24 (*22 is NU-PULLUP tied to VCC exactly as Fig 24 draws), GND = 2/12/23/EP33 + NU-PULLDN pins 3/9/10/30/31 tied to GND as in Fig 24, 13-21/25-29/32 left NC as DNC/NC. SDI/SDO/SCK/CSN = 5/6/7/8 to SPI1 ✓, GPO pin 4 → PB2 (pin 37) — Fig 24 marks this optional "MCU_IRQ" wiring ✓ (useful: TROPIC01 GPO-polling fallback is in the BOM notes).
- **MISSING: the 47k SDO/MISO pull-up (CORRECTED — first pass wrongly said CSN).** DS Fig 24 (p.63) draws R1 47k from the **SDO line (pin 6, MCU_SPI_MISO)** to VCC — the junction dot is on the SDO row, verified on the page image. The TS1702 Mini Board netlist confirms it: R1 47k nodes are `IC1.6 (SDO)` ↔ net `/SPI_MISO` and `IC1.24 (VCC)` (ts1702.xml, nets 3 and 7). Functional reason: TROPIC01 tristates SDO when it has nothing to send, and the host L1 protocol interprets **0xFF as "chip has no response / busy"** (`libtropic/src/lt_l1.c:102` — "0xFF received in second byte means that chip has no response to send"); without the pull-up the MCU reads noise instead of a clean 0xFF and L1 polling misbehaves. Net `TROPIC_SPI_MISO` on this board connects only U2.6 ↔ U1.31 — no pull resistor anywhere on the TROPIC SPI. **Action: add 47k from TROPIC_SPI_MISO to TROPIC_VCC (the switched rail, NOT SYS_3V3, so the IO is not back-biased while U4 gates the rail off — TROPIC01 abs max on IO = 3.6V and unpowered-IO bias is not specified).** The STM32 SPI1 MISO input can also enable an internal weak pull-up, but the reference design treats the discrete 47k as required; follow it.
- *Optional hardening (not in the official reference):* a CSN pull-up to TROPIC_VCC would additionally keep the SE deselected while PA4 is Hi-Z during MCU reset/boot. `TROPIC_SPI_CSN` today connects only U2.8 ↔ U1.29. Cheap insurance on a secure element; mark DNP if the FW team objects.
- **Decoupling count OK (3×100nF = DS Fig 24 C1/C2/C3), distribution not.** Re-measured pad-to-pad: C3 → pin 24 1.57mm ✓, C3 → pin 22 1.65mm ✓, but **pin 1 (pad 24.744,62.05) nearest TROPIC_VCC cap is 5.45mm and pin 11 (21.394,63.4) is 4.15mm (C5)** — all three caps are clustered on the south side while the rot -90 QFN has VCC pins on three sides. Redistribute: keep C3 at pin 24, move C5 to the west side for pin 11, move C4 to the north-east for pin 1.
- **Bulk:** DS Fig 24 shows none, but Trezor Safe 7 adds 4.7µF (C104) beside its 3×100nF, and this design power-cycles U2 through U4. Recommend 2.2-4.7µF on TROPIC_VCC near U2 (inrush is managed by the TPS22917 slew).
- **Power-gate chain verified correct:** U4 TPS22917 VIN=SYS_3V3, ON=TROPIC_PWR_EN(PB0) with R5 47k pulldown (default-off ✓), CT: C6 1nF **CT→VIN** — this is the correct topology per TPS22917 DS §9.3.2 ("A capacitor to VIN on the CT pin sets the slew rate"), not CT→GND. RJ1 0Ω current-measurement jumper TROPIC_VCC_SW→TROPIC_VCC ✓. Trezor uses the same concept (P-FET high-side + 47k).
- Placement: CSN pad-to-pad U2↔U1 = **4.64mm** — excellent, no SI concern. 0.4mm-pitch QFN fanout needs 0.20mm pads / ~0.15mm traces / 0.1mm clearance — confirm against the PCBWay class chosen in the manifest (DFM reviewer's domain, flagging only).

---

## 4. OPTIGA Trust M (U11 @ (14.5,43))

Reference: OPTIGA Trust M DS Rev 3.70, Table 6 (p.17), §5, Figure 6 (p.15).

- **Pinout matches Table 6 exactly:** 1=GND, 3=SDA, 8=SCL, 9=RST, 10=VCC, 2/4/5/6/7 NC left floating ("shall be left floating" ✓ board has them NC).
- **RST (pin 9): "This pin has a weak internal pull-up resistor" (Table 6)** → direct drive from PB5 (pin 91) with no external pull-up is acceptable. Warm-reset timing t1 ≥ 10µs / reset-low ≤ 2500µs (Table 14) is firmware's job.
- **Hibernate is a software feature** (CloseApplication / hibernate current <2.5µA table entry describes VCC=0 state; Appendix A covers an *optional* MOSFET VCC-cut circuit). Always-on SYS_3V3 supply is fine; no hardware change needed.
- **MISSING local decoupling: no capacitor within 5.2mm of VCC pin 10 (pad 16.0,42.0).** Nearest SYS_3V3 cap pads: C58 (U1 pin-100's cap) 5.24mm, C50 6.48mm, C2 4.7µF 6.67mm. **Action: add 100nF at ~(16.5,40.8)** (free area between U11 and R6/R7).
- I2C pull-ups R6/R7 4.7k → SYS_3V3 ✓ good for 400kHz on this short bus (drop to ~2.2k only if 1MHz FM+ is wanted). Bus instance must be **I2C4** (see §1.7).
- **Footprint EP (CORRECTED — first pass wrongly claimed the package has no exposed pad):** OPTIGA DS **Figure 7 (p.16) shows a central pad marked "n.c.\*" with footnote "\*Connect the exposed pad with the copper area in the PCB to improve thermal dissipation"**, and the Figure 8 backside view shows the pad metal. So the board's choice — `Microchip_USON-10-1EP_3x3mm_P0.5mm` proxy with the EP netted to GND (U11 pad 11) — is electrically safe (EP is internally n.c.) and thermally per DS advice. Remaining minor check: DS Figure 6 dimensions the pad ≈1.7±0.1mm tall; verify the proxy's EP/paste (1.8mm class) does not exceed the actual pad metal enough to cause paste squeeze-out, and match the 2.5mm lead row span before fab.

---

## 5. W25Q128JVSIQ (U5 @ (15.73,63.56)) — OCTOSPI1

- **Part choice validated:** "JVSIQ" = QE bit factory-set to 1 (W25Q128JV DS §7.1.4: QE=0 default only for IM/JM options; §"the /HOLD pin function is not available" when QE=1) → wiring IO2=/WP and IO3=/HOLD straight to OCTOSPI with **no pull-ups is correct for this exact suffix**. Guard: if purchasing ever substitutes a JM part, quad boot breaks — pin the suffix in the BOM.
- Bus: OCTOSPI1 Port E (PE10-15, pins 41-46) ✓. CLK pad-to-pad U5.6→U1.41 = **12.1mm**. For the realistic 48-80MHz SDR target this is fine (ST OCTOSPI guidance AN5050: keep the bus short/matched; DS §5.3.34 gives up to 130MHz+ capability but that needs tuned layout). Match CLK/IO0-3/NCS within a few mm when routing (QSPI_CLK and QSPI_IO2 are still among the 69 open nets). Series R on CLK not required at these lengths/speeds.
- **MISSING local decoupling: no 100nF at VCC pin 8 (pad 19.322,61.654).** Nearest caps: C17 2.2µF at 3.64mm (already double-booked as the de-facto VDDA-area bulk), C16 2.2µF at 6.7mm. **Action: add 100nF within ~1.5mm of pin 8** (space available at ~(20.5,61.0)).

---

## 6. SWD / debug / required testpoints

- **J7 TC2030 pin map is the standard ARM TC2030-CTX assignment** — 1=VTref(SYS_3V3), 2=SWDIO, 3=NRST, 4=SWCLK, 5=GND, 6=NC ✓. Improvement: U1 pin 89 (PB3 = TRACESWO) is NC — wire it to J7 pin 6 for free ITM trace.
- **Repo-required testpoints TP_3V3/TP_BOOT0/TP_GND/TP_NRST/TP_SWCLK/TP_SWDIO are absent** (validator red). Free space verified around J7 (guide holes at (25.46,38.5), (30.54,37.48), (30.54,39.52); JP1 pads x=32.1-34.9 @ y 38.75-40.25; U1 pad row tops at y≈41.6; C58 at (21.0-22.0, 40.5); J6 body ends ~x=22). **Concrete proposal (TestPoint_Pad_D1.0mm, same as TP_UART_*):**
  - Row below J7: **TP_SWDIO (26.5, 40.5), TP_SWCLK (28.0, 40.5), TP_NRST (29.5, 40.5)** — 0.4-0.5mm clear of J7 pads above and U1 courtyard below; short stubs off the existing J7 nets.
  - Column left of J7: **TP_3V3 (23.0, 36.7), TP_GND (23.0, 38.3), TP_BOOT0 (23.0, 39.9)** — clear of J6 (≥1mm), guide hole (≥1.9mm), C58 (≥1.2mm). BOOT0 trace taps the JP1/R22/pin-94 net.
  - Run DRC after placing; a ±0.3mm nudge is available in all directions.
- **TP_UART_TX/RX at (38,52)/(38,53.5) are 15mm from the debug cluster** while TP_UART_GND is at (25,35) near J7 — the UART test triplet is split across the board and violates the "debug features grouped" constraint. **Action:** move TP_UART_TX/RX next to the new bank (e.g. (24.6,38.3)/(24.6,39.9), forming a 2-column grid with the ones above), or move all three UART TPs together below J7. Note TP_UART_GND (25,35) sits at the edge of the ANT1 envelope — keep copper TPs out of the final NFC coil area when the real antenna replaces the placeholder.

---

## 7. Trezor Safe 7 cross-check (scratchpad/pcb-review/trezor-hardware, rev D, sheet TS7_SE_Tropic)

Trezor wires a (newer-variant, 33-pin TPDI-capable) TROPIC01 with: 3×100nF (C101-C103) + 1×4.7µF (C104) on VCC; high-side P-FET power gating (Q4 CSD25501F3 + R36 47k on the gate) driven by PWR_EN; R35 47k in the SPI/GPO region (exact net not recoverable from the text-extracted sheet; the silicon variant differs from ODD_TR01 A.11); INT/GPO wired to the host; a dedicated 3V3 testpoint (TP9) at the SE. This independently corroborates: (a) power-cycling the SE is the intended integration pattern (our U4 TPS22917 ✓), (b) a bulk cap on the SE rail is good practice (we lack it), (c) 47k is the house value for SE pull resistors (we lack the reference-design MISO pull-up).

---

## Summary of required actions (priority order)

1. Resolve HSE: crystal MPN + real C18/C19 values; move both caps to X1; nudge X1 toward pins 12/13. (CRITICAL — MCU won't run USB/accurate clocks reliably otherwise; value is literally a placeholder.)
2. Add 100nF on NRST at pin 14 (DS Fig 38). (CRITICAL for robustness on a secure device.)
3. Add 47k MISO(SDO)→TROPIC_VCC pull-up (TROPIC01 DS Fig 24 R1 + TS1702 netlist; libtropic relies on 0xFF idle). Optionally also 47k on CSN as hardening. (CRITICAL for SE protocol reliability.)
4. Back-annotate all passives into schematic sheets + full BOM; kill all placeholder values. (Blocks fab.)
5. Add 100nF at OPTIGA VCC pin 10 (EP-to-GND is fine per DS Fig 7 note; only verify EP paste size).
6. Add 100nF at W25Q128 VCC pin 8; pin the JVSIQ suffix in the BOM.
7. Add VBAT_SENSE 100nF reservoir (ADC RAIN 248k ≫ 470Ω limit, Table 106).
8. Add 2×1µF (VDDA, VREF+) + 1×10µF VDD bulk near U1 (DS Fig 24).
9. Move LED_G off PC15 to a TIM pin (PE9 = TIM1_CH1 free); record I2C instance split (SE2=I2C4, TOUCH=I2C1) in the ledger.
10. Add the 6 required testpoints per the coordinates above; regroup TP_UART_TX/RX at the debug cluster.
11. Move U7 ESD inline between J1 and R3/R4 (~(33.5,63)); consider 0Ω for R3/R4 per AN4879.
12. Redistribute TROPIC01 100nF caps one-per-VCC-pin; add 2.2-4.7µF bulk on TROPIC_VCC; wire PB3→J7.6 (SWO).

Verified-good (no action): U1 per-pin 100nF plan (all ≤2.1mm pad-to-pad) and VCAP 4.7µF@1.8mm; BOOT0 strap; all peripheral pinmux assignments; TROPIC01 pin tie-offs incl. pins 30/31→GND and 22→VCC (Fig 24 match) and TPS22917 gate topology (C6 1nF CT→SYS_3V3=VIN, correct per TI DS pin table "Connect capacitor from this pin to VIN"); OPTIGA pinout/RST (internal weak pull-up, Table 6)/hibernate handling and EP-to-GND; W25Q128JVSIQ QE=1 quad wiring (DS §7.1.4: QE factory-fixed 1 for IQ/JQ); TC2030 pinout; SPI1↔TROPIC 4.64mm; OCTOSPI CLK 12.1mm.
