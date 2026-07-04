# Adversarial Re-Verification (pass 2) — REMAINING [H]/[M] findings + backlight driver

Date: 2026-07-04. Scope: the README §4 [H]/[M] items NOT individually re-checked in
`design-notes/findings-recheck.md` (which already CONFIRMED C1–C4, E1–E7 power/MCU items,
and the verified-good list). Every claim below was attacked with a PRIMARY source
(datasheet text/tables) and, where net/placement-based, re-extracted FRESH from the live
`kicad/tropic01-universal-secure-device.kicad_pcb` (KiCad-10, net syntax is `(net "NAME")`
with no index; 104 footprints, 926 track segments, 129 vias).

Legend: CONFIRMED = holds vs primary · REFUTED = false as stated · PARTIAL = defect real,
wording/number needs correction.

---

## 1. HSE X1 load caps: 6.5–13.7 mm from crystal + placeholder → 8 pF (CL8pF 16 MHz). **CONFIRMED**
- Live board: X1 @(14.0,54.0) val `16MHz`, pads HSE_IN/GND/HSE_OUT/GND (topology OK).
  **C18 @(14.0,47.5) = 6.50 mm from X1; C19 @(26.5,59.5) = 13.66 mm** (center-center).
  README "6.5–13.7 mm" reproduced exactly. C19 sits in the U1 bottom decoupling row — clearly
  a stray drop, not at the crystal.
- Both C18/C19 value = literal placeholder string **`HSE_LOAD`**; X1 has no MPN. CL uncomputable,
  unbuyable — CONFIRMED.
- Value target 8 pF: C = 2·(CL − Cstray) = 2·(8 − ~4) ≈ 8 pF is a sound *starting* value for an
  8 pF-CL crystal; final value depends on measured board stray (2–5 pF ⇒ 6–12 pF window). Fix
  direction correct. Load caps must move to ≤2 mm of X1 pads with a tight ground return (AN2867).
- Verdict: CONFIRMED (placement + placeholder are real; 8 pF is a reasonable first value).

## 2. Missing 100 nF at NRST(14), OPTIGA VCC(10), QSPI/flash VCC(8). **CONFIRMED** (= re-confirms E6)
- Live nets: **NRST = {J7.3, R19(10k).1, U1.14} — no cap.** STM32U5 DS Fig 38 shows 0.1 µF on NRST
  as *recommended* robustness (not strictly mandatory); genuinely absent.
- **OPTIGA U11.10 VCC and flash U5.8 VCC are both tied straight to SYS_3V3** with NO dedicated local
  decoupler — the only caps on that net are U1's nine per-pin 100 nF + rail bulk (C2/C16/C17); nearest
  to U11.10 is ~5 mm, to U5.8 is C17 2.2 µF (double-booked as VDDA bulk) at 3.6 mm. CONFIRMED.
- Correction (carried from E6): NRST cap is DS-*recommended*, the OPTIGA/QSPI ones are standard
  practice; none is a hard "won't-boot," all are genuine local-decoupling gaps.

## 3. TROPIC_VCC bulk 2.2–4.7 µF missing; 3×100 nF clustered one-side. **CONFIRMED (both are "should", not DS-mandated)**
- Live: **TROPIC_VCC = C3/C4/C5 = 3×100 nF + RJ1(0R) + U2**. **No bulk cap present.** BUT DS Fig 24
  itself draws only 3×100 nF (board matches the official TS1701 reference exactly) — the 2.2–4.7 µF
  is a Trezor-style enhancement for the power-cycled SE, a best-practice add, **not** a datasheet
  requirement. CONFIRMED-but-characterize: recommended, not mandatory.
- Clustering: C3@(23,69), C4@(23,69), C5@(22.5,67.5) all south of U2@(23.34,64, rot −90) whose VCC
  pins 1/11/22/24 sit on three faces → two VCC pins are 4–5 mm from any cap (mcu note pad-to-pad
  pin1 5.45 mm, pin11 4.15 mm). Count is correct; **distribution is the defect** (spread one per VCC
  pin). CONFIRMED as a placement-quality item.

## 4. NFC decoupling / EP via-farm / X3 placement. **PARTIAL — every defect real; "caps missing" is stale wording**
- **KEY CORRECTION:** the nfc-rf-frontend note says the VDD_A/D/RF/AM/AGDC caps are "missing / pin
  not even in symbol." The **live board (later snapshot) HAS them netted:** NFC_VDD_D=C36(100nF·pin3),
  NFC_VDD_A=C37(100nF·pin7), NFC_VDD_RF=C38(100nF·pin9), NFC_VDD_AM=C39(**2.2µF**·pin11),
  NFC_AGDC=C40(100nF·pin24). So the caps are **present-but-wrong**, not absent.
- DS13541 §4.2.10 (verbatim, l.1934): *"For regulators recommended blocking capacitors are 2.2 µF in
  parallel with 10 nF, for pin AGDC 1 µF in parallel with 10 nF."* + (l.2020) *"2.2µF NOM for Regulator
  AM."* Vs board: **only VDD_AM's 2.2 µF is correct**; VDD_A/D/RF are single 100 nF (should be 2.2 µF∥10 nF),
  AGDC is 100 nF (should be 1 µF∥10 nF), and **no 10 nF parallel anywhere.** Real defect. + board-truth
  places them 8–12 mm from the pins (should be ≤1 mm). CONFIRMED.
- **NFC_VCC (VDD/VDD_TX/VDD_IO/VDD_DR, the 350 mArms TX rail) = only C41 100 nF.** Live-verified
  (NFC_VCC = C41 + RJ2 + U9.1/8/10/14). Distance C41@(50,40.5)→U9@(40.17,48) = **12.4 mm**. This is the
  worst gap — a TX rail needs 10 µF+1 µF+100 nF at the pins. CONFIRMED.
- **EP via-farm under U9: verified ZERO vias within 3 mm of U9 center** (fresh parse of all 129 vias).
  DS Table 2 pin 33 = thermal/RF-return GND pad → needs a ≥9-via 3×3 grid. CONFIRMED absent.
- **X3 27.12 MHz placement:** X3@(45.5,53) = 9.3 mm from XTO/XTI (pins 4/5) **with the U9 QFN body in the
  path**; load cap C34@(50,37.5) = ~16 mm from X3 (README "15.7"). CONFIRMED (crystal + caps must move to
  ≤2–3 mm of pins 4/5).
- Verdict: PARTIAL — all substantive defects (wrong values vs §4.2.10, no 10 nF parallels, 8–12 mm
  misplacement, NFC_VCC grossly under-decoupled, no EP via-farm, X3 misplaced) CONFIRMED; only the
  "caps missing" phrasing is stale (they exist but are 100 nF placeholders).

## 5. ST25R3916B VDD_DR / VDD_RF strap wrong (regulator vs bypass). **CONFIRMED**
- DS13541 §Power-supply system (l.2001–2006): the VDD_RF regulator current-limits at **350 mArms**;
  *"If a transmitter output current higher than 350 mArms is required the VDD_RF regulator cannot be
  used… VDD_RF and VDD_DR have to be externally connected to VDD_TX."* Pin roles (l.1020/1038):
  9 VDD_RF = "Regulated driver supply for antenna drivers" (regulator OUTPUT); 14 VDD_DR = "Antenna
  driver positive supply input."
- Live board: **U9.14 (VDD_DR) → NFC_VCC (=VDD_TX)**, but **U9.9 (VDD_RF) → NFC_VDD_RF, isolated, only
  C38 100 nF.** This matches **neither** mode: regulator mode needs 14 tied to 9 (board doesn't);
  bypass mode needs BOTH 9 and 14 to VDD_TX (board leaves 9 dangling on a cap). CONFIRMED.
- Fix per P6 direction is right (regulator mode: tie 14→9). Correction: decoupling on VDD_RF/VDD_DR
  should be **2.2 µF∥10 nF** per DS §4.2.10 (Trezor uses 4.7 µF+10 nF), not P6's stray "1 µF+100 nF."

## 6. C6 TROPIC ramp 1 nF → 470 pF (TPS22917 tR vs TROPIC 1 ms limit). **CONFIRMED**
- Live: C6 = **1 nF**, pads TROPIC_SW_CT(=U4.4/CT) ↔ SYS_3V3(=U4.1/VIN) → correct CT→VIN topology.
- Primary limit: **TROPIC01 DS A.11 §9.1 table — TVCCRAMPUP max = 1 ms** (verified in extract:
  "VCC 3.0/3.3/3.6 V … TVCCRAMPUP … 1 ms").
- TPS22917 DS §7.6: Output Rise Time tR = **1.6 µs/pF** (VIN 3.6 V, CT≥100 pF; ~1.5 at 3.3 V).
  **C6 1 nF ⇒ tR ≈ 1.6 ms > 1 ms** → violates the ramp limit. CONFIRMED.
- Fix 470 pF ⇒ tR ≈ 0.75 ms < 1 ms. OK. Nuance: if TVCCRAMPUP is read as full tON (3.8 µs/pF ⇒ 1.79 ms
  at 470 pF) it'd still be marginal; since downstream C is only 300 nF, inrush at a faster ramp is
  ~1.3 mA, so an even smaller CT (or CT open) is perfectly safe. 470 pF is a fine conservative pick.
- Doc nit: `part-selections.md` line 84 lists "C6 | **6.8 µF**" in the Value column while the note text
  says 470 pF — a typo in that table; intended value is 470 pF.

## 7. Pull-downs missing on NFC_PWR_EN / TFT_PWR_EN (TPS22917 ON "do not float"). **CONFIRMED (best-practice; internal Smart-Pulldown softens it)**
- Live nets: **NFC_PWR_EN = {U1.36, U13.3} only**; **TFT_PWR_EN = {U1.66, U14.3} only** — no resistor
  on either. By contrast **TROPIC_PWR_EN = {U1.35, U4.3, R5 47k→GND}** (has its pulldown). CONFIRMED.
- DS quote (l.153): ON pin — *"Active high switch control input. Do not leave floating."* CONFIRMED.
- Adversarial nuance: TPS22917 has an **internal Smart-Pulldown (RPD 750 kΩ typ)** that holds ON low at
  cold power-up until the MCU drives it high (DS §9.3.1, Table 9-1), then disconnects. So the *cold-boot*
  "floats → island unexpectedly on" risk is already mitigated internally; the genuine exposure is the
  **MCU-crash / Hi-Z-after-enable** window (smart pulldown disconnected, pin indeterminate). External
  100 kΩ pulldowns are cheap correct insurance and match the security "default-off" posture. Verdict:
  CONFIRMED as a valid SHOULD (not a hard "bus dead"); TROPIC already has it, NFC/TFT don't.

## 8. VBUS: bulk cap 31 mm from J1; no VBUS TVS. **CONFIRMED**
- board-truth: C1 10 µF @(28,35.5) — the only VBUS cap — is **31 mm from J1@(32,66.2)**. TPS2553 DS
  requires ≥0.1 µF at IN "as close to the IC as possible"; U8 has none local. CONFIRMED.
- USB ESD part U7 (TPD4E05U06) covers D+/D−/CC only — **VBUS has no TVS/ESD.** USB-C hot-plug ringing on
  a zero-local-cap VBUS can overshoot toward TPS2553 abs-max 7 V. CONFIRMED. Fix: 10 µF at J1 VBUS +
  100 nF at U8 IN + a 5 V TVS (SMF5.0A / TPD1E10B06-class) at J1.

## 9. DISPLAY_VCC_SW zero decoupling. **CONFIRMED**
- Live: **DISPLAY_VCC_SW = {J2.7/8/9/40/41/42, U14.5, U14.6}** — six FFC display-supply pins + the load
  switch output, and **not a single capacitor.** (DISPLAY_SW_CT=C7 1 nF is U14's CT slew cap, not rail
  decoupling.) ST7789V VCI/VDDI expect local 1 µF+100 nF and the FFC adds inductance. CONFIRMED.
  Fix: 2.2 µF+100 nF at U14 VOUT + 1 µF near J2.

## 10. DFM [M]: DISP1 old-Newhaven envelope; no fiducials; silk <0.15 mm; rules "too tight?" **CONFIRMED, with one REFUTE**
- **DISP1 envelope:** board-truth + mechanical note confirm DISP1 = value `NHD-2.4-240320AF-CSXP-CTP`,
  fp `Display_Envelope_42.8x59.91mm`, parked off-board at (110,125)/B — models the **OLD Newhaven** part,
  not ER-TFT024IPS-3 (42.72×59.46). CONFIRMED (also inflates gerber extents / pollutes pos+BOM → exclude
  or replace).
- **Fiducials:** dfm note confirms **0 fiducial footprints among 103/104**; J2 on B.Cu makes this a
  double-sided assembly → needs 3×F.Cu + 2–3×B.Cu fiducials. CONFIRMED.
- **Silk graphic lines:** 261 silk lines at 0.10–0.12 mm < PCBWay 0.15 mm min silk width → may print
  thin/patchy. CONFIRMED (minor).
- **"design rules tightened to PCBWay mins — are they TOO tight?" → REFUTED as a concern.** Actual
  geometry (all 129 vias 0.6 mm pad / 0.3 mm drill = 0.15 mm annular, aspect 5.3:1) is **exactly PCBWay
  minimum at standard price — manufacturable, NOT too tight** (zero margin on the annular ring, that's
  all). The real issue is the OPPOSITE: the `.kicad_pro` *rules* are too **LOOSE** (min_via_annular 0.1
  < 0.15, min_through_hole 0.2 = surcharge zone, hole-to-hole 0.25 < 0.28) → no guardrail for the
  remaining ~69-open routing. So "too tight" is unfounded; tighten the rules instead.

## 11. Backlight replacement: is AL8860 (buck WLED, SOT26) correct+available for 4×parallel LEDs (Vf 3.2 V, 80 mA) from SYS_PWR_IN 2.9–4.4 V? **REFUTED — AL8860 is the WRONG part (NEW defect: the C3 fix itself is broken)**
- Panel primary source (ER-TFT024IPS-3 DS, backlight table): **4-chip PARALLEL**, common anode LEDA +
  4 cathodes LEDK1–4, **Vf 3.2 V typ / 3.4 V max @ If = 80 mA total** (≤20 mA/chip). Confirmed.
- SYS_PWR_IN primary source: BQ24074 OUT VO(REG) = **4.4 V typ on USB**, **2.9–4.2 V on battery**.
- **AL8860 primary source (Diodes DS39014 Rev 8): "40 V 1.5 A BUCK LED DRIVER", input range 4.5 V–40 V,
  minimum VIN = 4.5 V**, step-down (Vin must exceed the LED voltage).
- Two independent disqualifiers:
  1. **AL8860's 4.5 V minimum input is ABOVE the 4.4 V max that SYS_PWR_IN ever provides** (and far above
     the 2.9–4.2 V battery range). The part sits below its own UVLO across the ENTIRE operating envelope →
     **it cannot power up / regulate at all.** This is decisive.
  2. Even ignoring UVLO, a **buck cannot regulate a 3.2 V load once Vin approaches/drops below ~3.7 V**,
     i.e. for most of the battery discharge — same class of failure the boost (C3) was rejected for.
- ⇒ **REFUTED.** AL8860 (named in README C3 and `part-selections.md §B`) is not a workable choice. This
  is effectively a NEW defect: the review's own fab-blocker fix specifies an unsuitable part.
- **Concrete correct verdict:** the panel exposes 4 separate cathodes precisely for a **current-sink**
  driver. Use a **low-Vin (≤2.9 V) WLED backlight driver with 4 matched current sinks (or a charge-pump/
  boost WLED driver), fed from SYS_PWR_IN, PWM-dimmed** — this is the review's OWN P1 option (a), which
  `part-selections` then wrongly overrode with AL8860. Because the rail (2.9–4.4 V) straddles Vf (3.2 V),
  the driver must be boost/charge-pump or buck-boost capable for full brightness at low battery; a plain
  linear/buck sink only holds full brightness down to ~3.4 V then dims (acceptable only if UV-cutoff is
  ~3.5 V anyway, per open item G3). A buck (AL8860) is categorically wrong here.

---

## Net verdict (this pass)
- CONFIRMED: #1 HSE, #2 NRST/OPTIGA/QSPI, #5 VDD_DR/RF strap, #6 C6 ramp, #7 EN pulldowns, #8 VBUS, #9 DISPLAY_VCC_SW.
- CONFIRMED-with-characterization (a "should", not DS-mandated / not a hard failure): #3 TROPIC bulk+clustering, #7 pulldowns (internal Smart-Pulldown covers cold boot).
- PARTIAL (defect real, wording/number to fix): #4 NFC (caps present-but-wrong, not "missing"), #10 (all confirmed EXCEPT the "too tight" rule concern is REFUTED — rules are too loose, not too tight).
- REFUTED: #11 AL8860 — wrong part (4.5 V min VIN > 4.4 V max supply; buck can't regulate a 3.2 V load from a 2.9–4.4 V rail).

## NEW defects the review missed
1. **[HIGH] The C3 backlight fix is itself broken:** AL8860 (README C3 + part-selections) has a 4.5 V
   minimum input that exceeds SYS_PWR_IN's 4.4 V ceiling — it can never operate. Re-select a
   4-sink / charge-pump low-Vin WLED driver (per the review's own P1 option a).
2. **[LOW/doc] `part-selections.md` §4 stale** re: NFC supply caps ("missing / not in symbol") — the live
   board HAS C36–C40 netted to U9's regulator pins; the true defect is wrong value (100 nF vs 2.2 µF∥10 nF)
   + no 10 nF parallels + 8–12 mm placement. Update the wording so the fix targets values/placement, not "add".
3. **[LOW/doc] `part-selections.md` line 84 typo:** C6 Value column says "6.8 µF" but the fix is 470 pF.
4. **[LOW/DFM reframe] Item-10 "rules too tight" is inverted:** the manufactured geometry is at PCBWay
   minimum (fine); the `.kicad_pro` DRC rules are too LOOSE (0.1 annular / 0.2 drill / 0.25 hole-to-hole)
   and give no guardrail for the unfinished routing — tighten to 0.15 / 0.3 / 0.3.
