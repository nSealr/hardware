# Power Architecture Review — TROPIC01 Universal Secure Device

Reviewer scope: power tree topology, regulator/charger correctness vs datasheets, current budget, layout of power stages, inrush/sequencing, charge-current sanity.
Date: 2026-07-03. Sources: actual pad-to-net extraction from `tropic01-universal-secure-device.kicad_pcb` (fp-nets.json in this directory), local datasheet PDFs in `/Users/vincenzo/Downloads/nsealr-datasheets/`, TI datasheets fetched (TPS2553 SLVSAB4-class, TPS61165 SLVS790E), TROPIC01 DS Rev A.11, ST25R3916B DS13541 Rev 11 + antenna appnote, TROPIC01 Mini Board TS1701 reference design, Trezor Safe 7 rev D schematics (trezor/trezor-hardware).

**Important context:** the KiCad schematic sheets are stubs (power_usb.kicad_sch contains only J1 + J9 and the note "final charger/power-path implementation remains layout reviewed"). The power tree exists only in the PCB netlist. The BOM CSV lists majors only — U13/U14/U15, L1/L15, D15, and every R/C are absent from it.

## 1. Reconstructed power tree (from PCB pad nets — ground truth)

```
J1 USB-C (VBUS, A4/A9/B4/B9)          J9 LiPo (pin1=VBAT, pin2=GND)
  │  C1 10µF @(28,35.5)  [31mm from J1!]        │ R20 1M / R21 330k -> VBAT_SENSE -> PA? (U1.15)
  ▼                                             ▼
U8 TPS2553DBVR @(44.5,64)             U10 BQ24074RGT @(48,45.12)
  IN=1:VBUS  EN=3:VBUS (always-on)      TS=1: R13 10k->GND (fixed-NTC per DS)
  FAULT=4: R14 100k->3V3 (not to MCU)   BAT=2,3: VBAT  (NO BAT capacitor!)
  ILIM=5: R8 27k -> IOS ≈ 0.89–1.04A    CE=4: GND (charge enabled)
  OUT=6: VBUS_LIMITED                    EN2=5: SYS_PWR_IN, EN1=6: GND  -> ILIM-resistor mode
  │  R23 100k / R24 1M -> USB_VBUS_SENSE -> U1.68 (PA9, digital VBUS detect)
  │  (NO capacitor anywhere on VBUS_LIMITED!)
  ▼
  IN=13 ── BQ24074 power path ── OUT=10,11 = SYS_PWR_IN (4.4V on USB / VBAT-50..100mV on battery)
           ILIM=12: R9 1.18k -> IINmax = 1610/1180 ≈ 1.36A
           ISET=16: R10 1.13k -> ICHG = 890/1130 ≈ 0.79A
           ITERM=15: R12 4.12k -> ~109mA;  TMR=14: R11 46.4k -> 6.2h fast-charge timer
           PGOOD=7 / CHG=9: 100k pull-ups to 3V3, to MCU
  SYS_PWR_IN loads: C14 1µF @(50,39) [the ONLY cap on this node]
   ├─ U3 TPS62840DLC buck @(48.44,49): VIN=2,4  EN=4? no — EN(pin4)=SYS_PWR_IN, MODE(3)=GND,
   │    STOP(6)=GND, VSET(5)=R18 267k -> 3.3V (DS Table 1), SW(7)->L1 2.2µH -> SYS_3V3, VOS(8)=SYS_3V3
   │    Cout: C2 4.7µF @(13,36.5) — 37.6mm away (!)
   ├─ U15 TPS61165 backlight boost @(49.2,59): VIN=1, CTRL=2=TFT_BACKLIGHT_PWM(PA8),
   │    SW=3 -> L15 10µH @(49,63.5) + D15 schottky @(46.5,67.5) -> TFT_BACKLIGHT_A -> J2.1 (LEDA)
   │    FB=6 = TFT_BACKLIGHT_K = J2.2-5 (LEDK1-4) + R15 "BL_SENSE" (placeholder!) -> GND
   │    COMP=5: C13 220nF; Cout C15 1µF @(40.5,66)
   └─ LED1 RGB anode (per netlist contract, for G/B Vf headroom)
  SYS_3V3 loads (via TPS62840, 750mA rated):
   ├─ U1 STM32U585 (9 VDD pins + VCAP 4.7µF, 10x 100nF)
   ├─ U4 TPS22917 -> RJ1 0R -> TROPIC_VCC (U2, 3x100nF = TS1701 reference match)
   │    ON=3: TROPIC_PWR_EN (PC?) + R5 47k pulldown ✓; CT=4: C6 1nF->VIN; QOD(5) tied to VOUT(6) ✓
   ├─ U13 TPS22917 -> RJ2 0R -> NFC_VCC (U9 VDD_IO=1, VDD=8, VDD_TX=10, VDD_DR=14; C41 100nF only)
   │    ON=3: NFC_PWR_EN — NO pulldown
   ├─ U14 TPS22917 -> DISPLAY_VCC_SW -> J2 VCI/VDDI (pins 7-9, 40-42) — NO capacitor on rail
   │    ON=3: TFT_PWR_EN — NO pulldown
   ├─ U5 W25Q128JV, U11 OPTIGA (I2C pull-ups R6/R7 4.7k), J6 Qwiic (direct, unfused)
   └─ JP1 BOOT0 jumper, J7 TC2030 VTref
```

Topology intent is sound: USB current-limit switch → power-path linear charger → single 3.3V buck; power-gated islands for TROPIC01/NFC/display; backlight and RGB LED on the pre-buck node. The execution has one wrong topology (backlight), wrong resistor programming (charge/ILIM), and systematic capacitor omissions/misplacements.

## 2. Findings

### CRITICAL

**P1. Backlight boost topology is wrong for this panel (cannot regulate, overdrives LEDs, cannot turn off).**
- Panel (design-notes/subsystem-7-display.md, confirmed by J2 pad nets): ER-TFT024IPS-3 backlight = **4 parallel LED strings, common anode LEDA (FFC1), cathodes LEDK1-4 (FFC2-5), Vf ≈ 3.2V, ~80mA total**. All four cathodes are tied to one net feeding TPS61165 FB.
- TPS61165 (SLVS790E p.1) is a **boost** converter for **series** LED strings; required VOUT here = Vf + VFB = 3.2 + 0.2 ≈ 3.4V, while VIN = SYS_PWR_IN = **4.4V typ on USB** (BQ24074 VO(REG), DS Table row "OUT pin voltage regulation BQ24073/74: 4.3/4.4/4.5V") and 2.9–4.15V on battery. A boost cannot regulate VOUT below VIN: whenever SYS_PWR_IN > ~3.55V (Vf+VFB+VD15), the DC path VIN→L15→D15→LEDs conducts uncontrolled. At 4.4V input the excess ≈ 0.75V lands on R15: with R15 = 2.5Ω (200mV/80mA nominal) the string current is ~300mA ≈ **4x overdrive** → backlight degradation/burnout.
- Because a boost has no load-disconnect, CTRL=low does NOT stop this path: **the backlight cannot be switched off in hardware** for battery > ~3.6V, wrecking battery life and defeating TFT_PWR_EN gating.
- Trezor Safe 7 (ts7_main_rev_d_sch.pdf) also uses a TI boost WLED driver (TPS61062), but for a series string panel; it does not validate this parallel-LED configuration.
- Fix options: (a) replace U15/L15/D15/C13/C15/R15 with a **charge-pump or matched-current-sink WLED driver with 4 sinks** running from SYS_PWR_IN with PWM dimming (correct for 4x parallel, common-anode, Vf≈3.2V from 2.9–4.5V input); (b) keep TPS61165 but move its VIN to **SYS_3V3** (VOUT 3.4V ≥ VIN 3.3V — degenerate near-100% duty, marginal regulation, and adds ~90–100mA to the buck budget); (a) is strongly preferred.

**P2. Charge current is 788mA — 1.6C to 5C for any battery that fits.**
- R10 (ISET) = 1.13kΩ → ICHG = KISET/RISET = 890/1130 = **788mA typ** (KISET 797–975 AΩ, BQ24074 DS SLUS810N §Electrical Characteristics).
- Battery volume behind the display above the board is ~42.7 x 19.3mm → realistic single-cell LiPo of **150–300mAh**. 788mA = 2.6–5.3C — far outside safe 0.5–1C, and small JST-PH packs typically specify ≤1C.
- Also thermal: BQ24074 is a linear charger; at 5V in/3.7V battery with 788mA + system load, dissipation exceeds ~1.2W in a 3.5x3.5mm VQFN → guaranteed thermal-loop throttling.
- Fix: pick the battery first; then R_ISET = 890/ICHG. For 250mAh @1C: **3.57kΩ** (250mA); for 150mAh @1C: 5.9kΩ. Range allowed 590Ω–8.9kΩ. Recompute ITERM: R_ITERM = ITERM·RISET/KITERM (KITERM=0.030); for 25mA (10% of 250mA) with RISET 3.57k → **2.94kΩ** (today's R12 4.12k with R10 1.13k gives ~109mA). TMR 46.4k → 6.2h fast-charge timer stays fine.

**P3. Input current-limit chain is incoherent and USB non-compliant.**
- BQ24074 ILIM: R9 1.18k → IINmax = KILIM/RILIM = 1610/1180 = **1.36A typ** (KILIM 1500–1720 AΩ).
- Upstream TPS2553 with R8 27k → IOS = 23950/27^0.977 ≈ **0.96A nom** (0.89–1.04A per DS IOS equations).
- USB source: J1 is a UFP with Rd 5.1k only (R1/R2), no CC voltage monitoring → the design may legally draw only **default USB power (500mA)**.
- Consequence: charger asks 1.36A > front-end switch limit 0.96A > USB budget 0.5A. During charging + load, the TPS2553 will sit in current limit (droop, heat, FAULT), and any compliant/weak port will sag or shut down.
- Fix: R9 → **3.24kΩ** (1610/3240 ≈ 497mA) to make BQ24074 the 500mA-compliant limiter; keep TPS2553 at 27k (~0.96A) as fault backstop. If >500mA charging is wanted, add CC-level detection (ADC on CC1/CC2) and only then raise the limit dynamically (BQ24074 EN1/EN2 are hardwired, so it would have to stay at 500mA anyway — or move ILIM selection to a FET-switched resistor).

**P4. Charger input, battery and output capacitors are missing or undersized.**
- BQ24074 DS Pin Functions: IN requires **1–10µF** bypass → net VBUS_LIMITED has **zero capacitance** (only R23 and two IC pins on the whole net).
- BAT requires **4.7–47µF** → net VBAT has **no capacitor at all** (J9, R20, U10.2/3 only). Battery lead inductance + no local cap = charger loop stability risk and poor transient handling.
- OUT requires **4.7–47µF** → SYS_PWR_IN has a single **C14 1µF** at 6.4mm. This same 1µF is also the only input capacitance for the TPS62840 (DS: "A 4.7-µF ceramic capacitor is required" at VIN, U3 is 10.1mm away) and the TPS61165 (typ app: 4.7µF at VIN, U15 is 20.0mm away), and feeds the pulsed RGB LED.
- Fix: 4.7µF at U10 IN (pin 13) + 10µF at U10 OUT + 4.7–10µF at U10 BAT/J9, 4.7µF at U3 VIN pins, 4.7µF at U15 VIN. All within 1–2mm of the respective pins.

**P5. TPS62840 output capacitor effectively absent at the converter.**
- DS Table 3 (LC filter): 2.2µH (L1 DFE201610P-2R2M ✓) pairs with **10µF min** output capacitance (derating anticipated). VOS pin note: "Connect this pin directly to the output capacitor with a short trace."
- Board: the only bulk SYS_3V3 caps are C2 4.7µF @(13,36.5) — **37.6mm** from U3, L1→C2 34.3mm — plus C16/C17 2.2µF near the TROPIC corner. Nothing >100nF within 10mm of L1/VOS.
- Consequence: DCS-Control loop sees trace inductance instead of Cout → ripple/instability; VOS discharge feature acts on far node.
- Fix: place 10µF X5R/X7R directly at L1.2/VOS, keep C2 as remote bulk.

### IMPORTANT

**P6. ST25R3916B VDD_RF/VDD_DR strapping matches neither documented configuration.**
- Board: VDD_DR (U9 pin 14) tied to NFC_VCC (raw switched 3.3V); VDD_RF (pin 9) is an isolated net with only C38 100nF.
- DS13541 §Power supply system: normal mode drives the antenna drivers from the **VDD_RF regulator** (i.e., pin 9 tied to pin 14 externally — as drawn in the ST antenna-design appnote figure); bypass mode (TX > 350mArms) requires "**VDD_RF and VDD_DR** ... externally connected to VDD_TX". The hybrid on the board leaves the drivers unregulated (PSRR loss, field amplitude tracks battery) while the regulator drives only a cap.
- Fix: for a 3.3V handheld, use regulator mode: disconnect pin 14 from NFC_VCC and tie it to the NFC_VDD_RF net (pin 9) with 1µF+100nF; use the Adjust Regulators command (DS §4.1) at init.

**P7. TROPIC01 VCC ramp violates the 1ms datasheet limit.**
- TROPIC01 DS A.11 §9.1: **TVCC_RAMPUP ≤ 1ms**. TPS22917 DS switching characteristics: tR ≈ 1.6µs/pF x CT at VIN 3.6V (slower at 3.3V) → C6 = 1nF gives **≈1.6ms** rise. 
- Fix: C6 → **470pF** (tR ≈ 0.75ms). Inrush stays trivial: downstream capacitance is only 300nF (C3–C5), I = C·dV/dt ≈ 1.3mA. Same for C7/C8 only if the display/NFC rails ever need faster ramps (no hard limits found there; ST25R3916B has POR at 1.0–2.0V and no max ramp spec).

**P8. NFC supply decoupling inadequate and scattered.**
- NFC_VCC (VDD+VDD_TX+VDD_IO+VDD_DR) has only **C41 100nF at 12.4mm** from U9. With drivers supplied externally (current strap), TX pulls up to 350mArms (abs max 500mA peak, DS Table 122) as 13.56MHz-envelope bursts — a single distant 100nF guarantees rail collapse and TX amplitude modulation artifacts.
- Regulator bypass caps are all far from the QFN32: C36 VDD_D 10.7mm, C37 VDD_A 9.5mm, C38 VDD_RF 8.8mm, C39 VDD_AM 11.5mm, C40 AGDC 12.2mm. These are internal-LDO stability caps; ST reference designs put them at the pins.
- Fix: 10µF + 1µF + 100nF on NFC_VCC at U9; move C36–C40 to within ~1mm of their pins. (Also X3 load cap C34 sits 16.1mm from X3 — flagged for the layout reviewer.)

**P9. VBUS front-end: bulk cap 31mm from the connector, no VBUS transient protection.**
- C1 10µF (the only VBUS cap) is at (28,35.5): **31.0mm from J1**, 32.9mm from U8; TPS2553 DS requires ≥0.1µF at IN "as close to the IC as possible". TPS2553 abs max IN = 7V; USB-C hot-plug ringing with zero local capacitance can overshoot. U7 TPD4E05U06 covers D+/D-/CC only — VBUS has no ESD/TVS.
- Fix: move C1 (or add 10µF) adjacent to J1 VBUS pads + 100nF at U8 IN; add a 5V TVS (e.g., SMF5.0A / TPD1E05U06-class on VBUS) next to J1.

**P10. NFC_PWR_EN and TFT_PWR_EN float during MCU reset/boot/DFU.**
- TPS22917 DS pin table: ON — "Do not leave floating." Nets NFC_PWR_EN (U1.36–U13.3) and TFT_PWR_EN (U1.66–U14.3) have no pull resistor; TROPIC has R5 47k (matching the TS1701 reference). During NRST, BOOT0-DFU, or firmware crash the switch state is undefined.
- Fix: add 100k pulldowns on both nets (default-off islands, matches the security posture).

**P11. Touch/Qwiic I2C bus has no pull-up resistors.**
- TOUCH_I2C_SCL/SDA nets contain only J2.44/45, J6.3/4, U1.95/96. subsystem-7-display.md specifies 4.7k pull-ups to +3V3 — they were never instantiated (R6/R7 4.7k are on the SE2 bus). The bus cannot work.
- Note the rail choice: pull-ups to SYS_3V3 will back-feed the power-gated FT6336 through SDA/SCL when DISPLAY_VCC_SW is off (J6 is always powered, so gating while Qwiic is in use is inherently conflicted). Add 4.7k pull-ups to SYS_3V3 and have firmware treat display-off as bus-idle-high (FT6336 leakage through its I2C pads is small but should be sanity-checked on bring-up).

**P12. DISPLAY_VCC_SW rail has zero decoupling.**
- Net = U14.5/6 + six J2 pins (VCI 42, VDDI 40/41 + mirrored 7–9). ST7789V VCI/VDDI expect local 1µF+100nF; the FFC adds inductance. Add 2.2µF + 100nF at U14 VOUT and 1µF near J2.

**P13. Backlight BOM placeholders: R15 = "BL_SENSE", D15 = "D_SCHOTTKY", L15 = generic "10uH".**
- R15 sets LED current (I = 200mV/R15, TPS61165 DS); it has no value. D15 has no part number (needs low-Vf schottky, ≥0.5A, e.g., if topology survived). Moot if P1 is fixed by replacing the driver, but the rail cannot be built as drawn today.

### MINOR / VERIFIED-OK

**P14. Current budget — TPS62840 verdict: adequate, not undersized (with conditions).**
Worst realistic concurrent SYS_3V3 load:
| Load | Current | Source |
|---|---|---|
| STM32U585 @160MHz + peripherals | 20–40mA | DS headline 19.5µA/MHz (SMPS) + peripheral overhead |
| TROPIC01 processing peak | 25mA | DS A.11 §9.2 (Mac_And_Destroy peak 24.9mA) |
| W25Q128JV active | 25mA | Winbond DS ICC max |
| OPTIGA Trust M | 15mA max | DS: ICC avg 14mA, HW-limitable 6–15mA |
| ST25R3916B TX (field on) | 250–350mA | DS: IAL 23mA + driver ≤350mArms via regulator |
| Display logic + touch | ~25mA | ST7789V+FT6336 typicals |
| Qwiic J6 (must be capped) | 100mA | policy, see P17 |
| **Total** | **~460–580mA** | vs **750mA** TPS62840 rating |

Backlight is correctly NOT on the 3.3V rail (TPS61165 VIN = SYS_PWR_IN), so the classic backlight-boost-input-current trap is avoided. Conditions: keep NFC drivers in regulator mode ≤350mArms (see P6 — bypass mode allows 500mA peaks and breaks margin), cap Qwiic. On the input side, worst case ~0.6A x 3.3/2.9V ÷ 0.85 ≈ 0.8A from SYS_PWR_IN at battery cutoff — within BQ24074 battery-FET and TPS62840 ratings. Comparison: Trezor Safe 7 rev D uses an nPM1300 PMIC (integrated 800mA charger/power-path + two 200mA bucks) with the same ST25R3916B + TROPIC01; they split loads across rails and run the NFC TX off a higher-current node — our single 750mA buck is a legitimate simpler alternative at these budgets.

**P15. TPS61165 VIN minimum (3.0V) vs SYS_PWR_IN at battery cutoff (≈2.9–3.15V after VDO(BAT-OUT) 50–100mV)** — marginal at end of discharge. Moot once P1 replaces the part; keep VIN-min ≥ operating range in the replacement selection.

**P16. VBAT_SENSE divider (R20 1M/R21 330k) is hardwired: ~3.2µA permanent battery drain** (~28mAh/yr — acceptable) but 248kΩ source impedance is too high for the STM32 ADC without long sampling; add 100nF from VBAT_SENSE to GND at the pin. USB_VBUS_SENSE (R23 100k series + R24 1M pulldown into PA9 5V-tolerant) is fine as a digital detect.

**P17. J6 Qwiic is documented as "power-limited 3V3" (BOM note) but connects SYS_3V3 directly** — no polyfuse/switch. A shorted peripheral takes down the entire system rail. Add a 100–200mA polyfuse or a fourth TPS22917 with small ILIM-style series limiting, or amend the contract note.

**Verified correct (no action):**
- BQ24074 pin mapping is fully correct (TS=1 with 10k fixed per DS, BAT=2/3, CE=4 low, EN2=5 high via OUT (self-bootstrap: first ms in USB100 mode, then ILIM mode — acceptable), EN1=6 low, PGOOD/CHG open-drain with 100k pull-ups in the 1k–100k range, VSS+EP to GND).
- TPS2553 pin mapping correct (IN=1, GND=2, EN=3 to VBUS, FAULT=4 w/100k to 3V3, ILIM=5 27k, OUT=6). EN-to-VBUS auto-enable is valid (abs max 7V).
- TPS62840: pinout correct, VSET 267k = 3.3V (DS Table 1), MODE=GND (power save), STOP=GND, EN=VIN (always-on per contract), L1 2.2µH matches DS Table 3/4.
- TPS22917 islands: QOD (pin 5) tied to VOUT (pin 6) is a documented configuration and is exactly right for TROPIC01 power-cycling (fast rail collapse); CT cap to VIN is the correct node; TROPIC ON pin has the 47k pulldown mirroring the TS1701 reference.
- TROPIC01 decoupling 3x100nF equals the official Tropic Square TS1701 Mini Board reference BOM.
- ST25R3916B: VDD=VDD_TX=VDD_IO on one switched net satisfies "VDD and VDD_TX must be connected to the same power supply"; VDD_A/VDD_D/VDD_RF/VDD_AM/AGDC bypass nets exist with C36–C40 and C39 2.2µF matches the DS "2.2µF NOM for regulator AM"; digital pins 27–32 are rated −0.3..6V independent of VDD_IO, so power-gating NFC while the MCU SPI idles high does not violate abs-max (still park pins low in firmware as good practice).
- TROPIC01 IO abs max is 3.6V absolute (not VCC-referenced), so power-cycling with driven SPI is not an explicit violation; firmware should still tristate/park low during the cycle since back-injection behavior is unspecified.
- Sense jumpers RJ1/RJ2 (0R, current_sense bus) in series with TROPIC_VCC / NFC_VCC are a sane provision.

## 3. Priority fix list (schematic-first)
1. Replace backlight driver topology (P1) and give R15/D15 real values or delete them with the change.
2. Re-program charger: R10→3.57k (250mAh battery @1C), R12→2.94k, R9→3.24k (P2, P3).
3. Add the missing capacitors: U10 IN 4.7µF / OUT 10µF / BAT 4.7µF; U3 VIN 4.7µF + VOUT 10µF at the pins; U15(-successor) VIN 4.7µF; NFC_VCC 10µF+1µF; DISPLAY_VCC_SW 2.2µF+100nF; J1 VBUS 10µF local (move C1) (P4, P5, P8, P9, P12).
4. Restrap ST25R3916B VDD_DR→VDD_RF (P6).
5. C6 1nF→470pF (P7); add 100k pulldowns on NFC_PWR_EN/TFT_PWR_EN (P10); add 4.7k I2C pull-ups (P11).
6. Add VBUS TVS; Qwiic polyfuse (P9, P17).
7. Regenerate the BOM to include all power components (currently missing U13/U14/U15, L1/L15, D15, and every passive).
