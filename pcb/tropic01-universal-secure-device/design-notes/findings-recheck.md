# Adversarial Re-Verification — nSealr TROPIC01 Secure Device PCB Review (verify2)

Date: 2026-07-04. Method: each prior finding attacked with a PRIMARY source; confirmed only
if evidence held. Net-level facts re-extracted FRESH from the live
`kicad/tropic01-universal-secure-device.kicad_pcb` (KiCad-10 `(net "NAME")` format), NOT
from the scratchpad JSON.

> DATA-HYGIENE NOTE: `scratchpad/pcb-review/our-padnets.json` (Jul-3) is STALE and disagrees
> with the current board (it shows OPTIGA U11 pins 2–8 all on I²C, U2 pins 15–22 all VCC,
> U1 pins 7/8 on LED_G). The current board + design-notes reports match my fresh extraction;
> only that JSON is wrong. Do not cite it.

Legend: CONFIRMED = holds vs primary · REFUTED = false as stated · PARTIAL = defect real but
wording/attribution/number needs correction.

## FAB-BLOCKERS

### C1 — J2 FH12-50S bottom-contact; display needs top-contact (FH12A-). CONFIRMED
- Board: J2 fp `Hirose_FH12-50S-0.5SH...Horizontal`, side B rot180.
- ER-TFT024IPS-3 DS §2.1: "50 Pin, 0.5mm Pitch, SMD Horizontal Type Top contact". Hirose
  catalog: FH12-*S-0.5SH = Bottom Contact; FH12A-*S-0.5SH = Top Contact (field "A"=top).
- Land patterns differ (FH12A slot E=25.57) → footprint rebuild, not a BOM swap. Fix =
  FH12A-50S-0.5SH(55)/ER-CON50HT-1. Caveat: top/bottom correctness tied to folded-tail
  orientation → verify pin-1 silk at first article. Naming/type mismatch itself unambiguous.

### C2 — J2 pin order mirrored (LEDA pad high-x, tail pin-1/LEDA low-x). CONFIRMED (geometry) / contingent on tail orientation
- Measured live: J2 pad "1" = (44.250,46.150) net TFT_BACKLIGHT_A (high-x); pad "50" =
  (19.750,46.150) net GND (low-x). Folded tail pin-1(LEDA) lands x≈19.75 → full 50-signal
  mirror (LEDA↔GND, 2.8V onto RESET/IM, SPI/touch scrambled).
- Board geometry is exactly as claimed. Mirror conclusion shares C1's tail-orientation read;
  reviewer flags first-article pin-1 verification. Fix C1+C2 together.

### C3 — 4 PARALLEL LEDs on a series-string boost from a >Vf node → overdrive/can't-off. CONFIRMED
- Board: J2.1=TFT_BACKLIGHT_A (anode); J2.2–5 all = TFT_BACKLIGHT_K (4 cathodes shorted).
  L15(SYS_PWR_IN→SW), D15(SW→anode), U15 TPS61165 FB=cathodes, R15(no value) cathodes→GND.
- TPS61165 DS p.1: "boost converter that drives LEDs in series" (can't regulate <VIN; DC L+D
  path). BQ24074 DS: OUT VO(REG)=4.3/4.4/4.5V → SYS_PWR_IN≈4.4V(USB)/3.0–4.2V(batt) is above
  the ~3.4V anode node → uncontrolled conduction + no HW off. CONFIRMED.

### C4 — ST25R3916B RF front-end uncaptured; ANT1 empty copper. CONFIRMED
- ANT1 = 0 pads/0 nets. Fresh U9 RF/aux pads NO_NET exactly at {2,13,15,17,18,19,22,23,25,28}
  = TAD1,RFO1,RFO2,EXT_LM,AAT_A,AAT_B,RFI1,RFI2,TAD2,MCU_CLK (DS13541 Table 2). Matching
  parts C30–C33/L30/L31 all NO_NET. "15/33 symbol pins" is a schematic-symbol figure (not
  PCB-checkable) but the material claim is confirmed. (XTO/XTI pins 4/5 ARE netted now —
  minor deviation from the report, immaterial.)

## ELECTRICAL

### E1 — 788 mA charge (R10=1.13k); fix for 250 mAh@1C. CONFIRMED (C-rate wording loose)
- R10=1.13k on CHARGER_ISET. BQ24074 DS KISET=890 AΩ → 890/1130 = 787.6 mA. 250 mA →
  RISET=3.56k (report 3.57k) ✓. Nuance: at 250 mAh, 788 mA = 3.15C (the "2.6–5.3C" is the
  150–300 mAh range). Defect (>>1C, >1.2W linear) real.

### E2 — ILIM chain inverted (charger 1.36A > TPS2553 0.96A > USB 0.5A). CONFIRMED
- R9=1.18k, KILIM=1610 → 1.36A. R8=27k → IOS ≈0.958A (DS IOS eq reproduces 15k→1700,49.9k→520).
  J1 Rd-only (R1/R2 5.1k), no CC ADC → USB default 500mA. Ordering backwards vs USB≥FE≥charger.

### E3 — "Missing 47k CSN pull-up (DS Fig24/devboard/Trezor)". PARTIAL — DEFECT REAL, PIN MISLABELED → SDO/MISO  [FLAG]
- Fresh board: TROPIC_SPI_MISO={U2.6,U1.31}; TROPIC_SPI_CSN={U2.8,U1.29}. No pull-up on the
  TROPIC SPI at all → missing-pull-up defect CONFIRMED.
- BUT reference puts it on SDO/MISO, NOT CSN: devboard ts1702.xml R1(47k) pin1→/SPI_MISO
  (IC1.6 SDO), pin2→VCC; CSN net has no resistor. TROPIC01 DS (l.1309–1314): SDO High-Z when
  not transmitting → pull-up gives clean 0xFF idle for libtropic L1. Board's own mcu report
  already corrected first-pass "CSN"→"SDO/MISO". Fixing CSN would not solve 0xFF-idle (CSN
  pull-up is only optional hardening).

### E4 — TPS62840 output cap 37.6 mm from U3 (needs 10 µF at VOS). CONFIRMED
- DS: 750mA; VOS "Connect directly to the output capacitor with a short trace"; typ Cout 10µF.
- Live coords: nearest SYS_3V3 bulk to U3(48.44,49): C2 4.7µF 37.6mm, C16 37.3mm, C17 32.4mm;
  L1→C2 34.3mm. Nothing ≥1µF within ~30mm of VOS. C14 1µF@10.1mm is INPUT (SYS_PWR_IN).

### E5 — LED_G on PC15 → no timer/PWM. CONFIRMED
- Fresh board: U1 pad 9 = LED_G (pads 7,8 NO_NET; stale JSON wrong). STM32U585 DS: LQFP100
  pin 9 = PC15-OSC32_OUT (backup domain, no timer AF, drive-restricted). Software-PWM only.

### E6 — Missing OPTIGA/QSPI/NRST 100nF; VBAT_SENSE 248k >> ADC 470Ω. CONFIRMED (NRST cap DS-recommended; 470Ω is the 12-bit figure)
- OPTIGA VCC(U11.10): no dedicated 100nF (nearest ~5.2mm). QSPI VCC(U5.8): no dedicated 100nF
  (nearest C17 2.2µF double-booked). NRST={R19 10k→3V3,U1.14,J7.3}, no cap — DS Fig38 0.1µF is
  recommended (robustness), not mandatory; genuinely absent.
- VBAT_SENSE: R20 1M ∥ R21 330k = 248kΩ. STM32 DS Table 106 max RAIN 14-bit ADC1 tops at 100Ω
  (12-bit row 470Ω; general 1000Ω@130°C). 248kΩ is 2–3 orders over → needs reservoir cap.
  Claim understates (14-bit limit is 100Ω, not 470Ω), doesn't overstate.

### E7 — Touch/Qwiic I²C has no pull-ups. CONFIRMED
- TOUCH_I2C_SCL={J2.44,J6.4,U1.95}; SDA={J2.45,J6.3,U1.96} — no resistors. R6/R7 4.7k are on
  the SE2/OPTIGA bus, not touch. Open-drain bus dead without pull-ups.

## VERIFIED-GOOD (tried to refute; none actually wrong)

### G1 — TROPIC01 tie-offs match DS Fig24 + devboard + Trezor. CONFIRMED CORRECT
- Fresh U2: VCC=1/11/22/24, GND=2/3/9/10/12/23/30/31/EP33, SPI=5/6/7/8, GPO=4, NC=13–21/25–29/32.
  DS Table1: VCC 1/11/24, GND 2/12/23, rest NU. Devboard: 3/9/10/30/31=PULLDN(GND),
  22=PULLUP(VCC),1/11/24=VCC. Board matches devboard NU handling exactly.

### G2 — OPTIGA pinout correct (NC 2/4-7 floating). CONFIRMED CORRECT
- Fresh U11: 1=GND,2=NC,3=SDA,4/5/6/7=NC,8=SCL,9=RST,10=VCC,EP=GND. OPTIGA Trust M DS Table 6
  exact match; RST has weak internal pull-up (direct-drive OK). Refutes stale JSON.

### G3 — TPS62840 adequate for ~460–580 mA. CONFIRMED
- DS: 750mA output. Budget 460–580mA (NFC TX ≤350mArms regulator mode) < 750mA, with the
  stated conditions. Not undersized.

### G4 — STM32 per-pin 100nF + VCAP correct. CONFIRMED
- 9×100nF, one per VDD/VBAT/VDDA/VREF+/VDDUSB pair, all ≤2.4mm. VCAP: DS l.1871 "4.7µF";
  board C59=4.7µF on U1.48. Correct. (Separate open gaps: no 1µF VDDA/VREF+, no 10µF VDD
  bulk — additional findings, not this claim being wrong.)

### G5 — W25Q128JVSIQ QE=1 quad-wiring correct. CONFIRMED
- Fresh U5: 1=NCS,2=IO1,3=IO2,4=GND,5=IO0,6=CLK,7=IO3,8=VCC. "IQ" suffix = QE factory-1
  (DS §7.1.4) → IO2/IO3 to OCTOSPI without pull-ups correct. (Note: pin JVSIQ suffix in BOM.)

## ACTUALLY-WRONG in the review's own claims (flag)
1. E3 mislabel (most important): 47k pull-up belongs on SDO/MISO→VCC, not CSN. Board is
   missing it entirely (defect real); a CSN-only fix would be ineffective.
2. E1 C-rate: at 250 mAh, 788 mA = 3.15C, not "2.6–5.3C" (that's the 150–300 mAh range).
3. E6 number: RAIN "470Ω" is the 12-bit value; 14-bit ADC1 limit is 100Ω. 248kΩ defect real, worse than stated.
4. our-padnets.json is stale/incorrect for U2/U9/U11/U1; all verdicts use fresh extraction.

## Net verdict
- Fab-blockers C1–C4: ALL CONFIRMED (C1/C2 contingent on first-article tail-orientation check).
- Electrical E1,E2,E4,E5,E7: CONFIRMED; E3: PARTIAL (defect real, pin=MISO not CSN); E6: CONFIRMED.
- Verified-good G1–G5: ALL CONFIRMED CORRECT — no false-good found.
