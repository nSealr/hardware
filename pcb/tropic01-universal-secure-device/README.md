# TROPIC01 Universal Secure Device — Board Design Record (single source of truth)

**This file is the one authoritative reference for the board.** It supersedes every
other design note. Last verified: 2026-07-04 (7-area deep review + adversarial
re-verification against primary sources: datasheets, the TROPIC01 devboards, and
the Trezor Safe 7 open hardware).

The board is a handheld **Nostr hardware signer**: STM32U585 host + **TROPIC01**
(open secure element) + **OPTIGA Trust M** (second SE) + **ST25R3916B** NFC reader,
a 2.4" IPS touch display, USB-C, a single LiPo, one side button. It is the lower
half of a device that sits behind the display; the battery fills the upper half;
the NFC antenna is a back-cover flex.

> **Design principle — standalone board, standard add-ons (governs every external
> interface).** The board is a **standalone product, sellable bare** (no display, no
> battery, no NFC antenna). The buyer composes the device with **standard, easy-to-source,
> non-exotic off-the-shelf parts**: an ordinary SPI/FFC display, a common single-cell
> LiPo with a **standard pluggable connector** (NOT solder tabs — the battery must be a
> swappable standard part), a standard NFC antenna via a standard feed connector. The
> enclosure is 3D-printable (or PCBWay). **Consequence:** every external connector
> (display FFC, **battery**, NFC feed, USB-C) must be a canonical, distributor-stocked
> part — this is why the battery connector choice (§1) matters and why solder tabs are
> rejected despite being thinner.
>
> **Verified — the goal is achievable with 3 connector swaps to standard parts:**
> (a) battery **J9 JST-PH → JST-SH `SM02B-SRSS-TB`** (2.0 mm PH is intrinsically ~6 mm
> tall; SH is ~2.9 mm → device ~11 mm, clears the MH4 collision, 1 A, same family as J6);
> (b) NFC feed **BM28 0.35 mm → a standard 1.0 mm 4-pin FFC** (the BM28 is fine-pitch /
> N2-reflow / not hand-assemblable = borderline-exotic); (c) display **FH12-50S →
> FH12A-50S-0.5SH(55)** (already fix C1/C2 — a commodity Hirose part). Everything else is
> standard/buyable (USB-C, Qwiic J6, TC2030, button, ST25R3916B). **Two things are
> intrinsically product-supplied, not buyer-sourced:** the **VNA-tuned NFC antenna flex**
> (custom, must ship with the product) and the **exact display model** (ordinary ST7789
> class, but the 50-pin FFC module is single-vendor BuyDisplay — document the model+pinout).

> **Status (honest):** the board is **fully designed and specified** but **not yet
> fab-ready**. Three steps remain, all needing tools/hardware this record cannot
> substitute: (1) **place + route** in the KiCad GUI (push-and-shove — headless
> auto-routing plateaus at this density); (2) the **antenna FPC** must be drawn as
> its own flex deliverable; (3) **first-article RF tuning** on a VNA. For an NFC
> device this state = "ready to build a first article to tune". Everything up to
> those gates is captured here.

---

## 1. Mechanical — the hard geometry (verified to the millimetre)

**Display: EastRising ER-TFT024IPS-3** (2.4" IPS 240×320, ST7789V + FT6336 cap
touch, single 50-pin 0.5 mm FPC, **top-contact**).
- Datasheet §2.2: **outline with FPC folded = 42.72 (W) × 59.46 (H) × 2.3 (T) mm.**
  (The `59.26` in old notes was the CTP *glass* height; the governing envelope is
  the **59.46** backlight frame.)
- Active area 36.72 × 48.96, **not vertically centred**: top margin 2.90, bottom
  (FPC/COG ledge) 7.60. FPC tail exits the **bottom** edge, folds 180° behind.

**Board:** **42.72 × 36.8 mm** (width = display width, HARD; height = the lower
portion behind the display). 4 rounded corners R2.5 with an M2 hole in each fillet
(MH1–4). Same rectangular footprint as the display; nothing overhangs it.

**Two-sided stack:** component side = **F.Cu** (all ICs/passives/connectors + the
NFC feed); display side = **B.Cu**, which carries **only J2** (the display FFC) —
the display lies flat against it.

**Battery (the "does it fit in plan?" answer — YES):**
- Battery zone = display − board = 42.72 × **(59.46 − 36.8) = 22.66 mm**, coplanar
  with the board, above it, within the display footprint.
- Cell **EEMB LP502030, 250 mAh, 20.5 × 32.0 × 5.3 mm.** It fits **only rotated**:
  the **32.0 mm side runs along the WIDTH** (42.72) and the **20.5 mm side along the
  HEIGHT** (22.66, margin **2.16 mm**). It does NOT fit with the long side vertical.
  **Board 36.8 + battery 22.66 = 59.46 exactly — zero slack.**
- Screen footprint (in plan) = board footprint (lower) **+** battery footprint
  (upper), exactly as intended. ✓ Largest cell: **250 mAh (LP502030) with the JST
  plug; ~340 mAh (LP502035) if the battery is soldered** (tabs remove the ~5.8 mm plug band).

**Thickness (Z-stack) — total ≈ 13.5 mm cased (~11.9 bare); it fits.** Set by the
*board* column (display 2.3 + J2 gap 2.0 + PCB 1.6 + **J9 JST-PH 6.0** = 9.6 mm
behind the display), NOT the battery column (cell 5.3 + ferrite 0.5 + FPC 0.2 =
6.0 mm) — the two sides are independent in-plane columns and **need not be equal
thickness** (the flat case-back tracks the taller, J9).

⚠️ **J9 (the vertical JST-PH) is the single limiting part** and it drives a
HIGH-LEVERAGE decision: it is ~6 mm tall (→ the tallest part → device ~13.5 mm), it
**collides with MH4** when shifted right for the 32 mm cell (body reaches x50.5; MH4
clearance starts x49.3), **and** caps the cell length. Per the standalone-board principle the fix must keep a **standard pluggable
connector** (NOT solder tabs). *(The current S2B-PH-SM4-TB is already side-entry — the 2.0 mm
PH family is just intrinsically ~6 mm tall.)* **→ Swap J9 to JST-SH `SM02B-SRSS-TB`**
(1.0 mm, 2-pin, side-entry SMT, **~2.9 mm tall, 1 A**, same family as J6): device drops to
**~11 mm** (SH is no longer the tallest part — USB-C/button ~3.5 mm dominate), the J9↔MH4
collision clears (~0.6 mm gap with the 32 mm cell), still a standard pluggable connector.
**Caveat:** most cells ship a JST-PH 2.0 pigtail; SH is the wearable/FPV standard → order
the LP502030 with an SH pigtail (a standard crimp option) or supply a PH→SH adapter.

**Top edge — three connectors across 42.72 mm:** J6 expansion (x≈19) · **J-ANT**
NFC-FPC feed (BM28 BTB, top-center x≈32, see §3) · J9 battery (right). ⚠️ With a
JST-PH J9 you can have the 32 mm cell **or** J9 clear of MH4, not both — the solder-tab
option above removes this constraint. MH3/MH4 sit in the top corner fillets.

---

## 2. Architecture (what is correct — keep)

Verified against datasheets + the TROPIC01 devboards + Trezor Safe 7. **No
false-good was found in re-verification** — these are genuinely right:

| Block | Part | Status |
|---|---|---|
| Host MCU | STM32U585VIT6 LQFP100 | per-pin 9×100 nF ≤2.4 mm + VCAP 4.7 µF **correct**; pinmux verified (SPI1 TROPIC, SPI2 NFC, SPI3 TFT, OCTOSPI1 flash, USB FS, SWD, I2C1 touch / I2C4 OPTIGA) |
| Primary SE | TROPIC01 TR01-C2P-T301 QFN32 | tie-offs match DS Table 1 + devboard **exactly** (VCC 1/11/22/24; GND+NU 3/9/10/30/31; DNC rest); SPI to U1 4.6 mm; power-gated by U4 TPS22917 (CT→VIN correct) |
| Second SE | OPTIGA Trust M USON-10 | pinout exact per DS Table 6 (NC 2/4-7 floating; RST weak internal pull-up); I2C4, isolated |
| NFC | ST25R3916B QFN32 | controller correct (see §3 for the RF work that's missing) |
| Flash | W25Q128JVSIQ | QE=1 factory → quad wiring w/o pull-ups **correct** |
| Power tree | USB-C → TPS2553 limiter → BQ24074 power-path charger → TPS62840 3.3 V buck + gated islands | topology **sound**; buck **adequate** (750 mA vs ~460–580 mA budget) |
| USB | GCT USB4105 + TPD4E05U06 ESD | Full-Speed → **no controlled impedance needed** |
| Debug | Tag-Connect **TC2030 (J7)** = SWD (SWDIO/SWCLK/NRST/VTref/GND); BOOT0 via JP1 | SWD consolidated on J7; scattered SWD test pads intentionally **not** used (fewer debug attack surfaces on a secure device) |

---

## 3. NFC antenna — on a back-cover FPC over the battery (verified sound)

**Decision:** the 13.56 MHz loop is on a **back-cover flex (FPC)**; the matching
network stays on the main board at U9; a feed connector **J-ANT** (top-center)
carries `NFC_ANT1/2` to the flex, which folds up so the loop lies **over the
battery**, with a **ferrite sheet between loop and battery**.

**Verified:** this is **structurally identical to Trezor Safe 7** (their NFC coil is
on a back-cover FPC too, Ø30 combo with the Qi coil, BTB feed) — a shipping,
proven design. Loop-over-battery-with-ferrite is mainstream (every smartphone runs
NFC over its battery this way). Three concrete requirements from verification:
1. **Loop geometry:** Ø30 mm (Trezor's) does **not** fit the 22.66 mm battery band →
   make it a **rectangular/oval loop ≈ 38 × 20 mm** (area ≈ 760 mm² ≈ Trezor's, so
   ~1 µH at 3–4 turns is reachable).
2. **Ferrite mandatory:** the LiPo is the worst-case eddy sink directly behind the
   loop. Würth **WE-FSFS** 364-material, ≥0.1–0.3 mm, sized > loop +1 mm. Expect La
   +10–30 % and some Q loss; **a first-article read-range test (not just VNA) is
   required** — this is the one antenna risk (over-cell vs Trezor's over-cover).
3. **Feed connector J-ANT:** use a **standard 1.0 mm 4-pin FFC** (differential feed on
   the middle 2 pins, GND on the outer 2 — the scheme off-the-shelf NFC flexes use).
   *(NOT the Hirose BM28 0.35 mm mezzanine that Trezor uses — verified borderline-exotic:
   fine-pitch, nitrogen-reflow, needs an FPC stiffener, not hand-assemblable. A standard
   1.0 mm FFC keeps the standalone-board principle. A 2-pin BTB is the alternative.)* Keep
   the post-match differential feed **< 8 mm** → **move U9 + the matching network up toward
   top-center** (as drawn U9 is ~14 mm below J-ANT — the feed is too long). Void all 4
   copper layers under the feed and loop.
4. **Matching for a 1 µH FPC loop (NOT the on-board-strip numbers):** use Trezor's
   published values — **Lemc 270 nH, Cemc 680 pF, Cs ≈ 150 pF/leg, Cp ≈ 70 pF diff,
   Rdamp ≈ 2 Ω, Cr ≈ 180 pF, Cd ≈ 680 pF**. (The 370 nH strip's Cs 180/Cp 240 pF do
   NOT apply — higher L needs ~2.7× less resonating C.) X3 = 27.12 MHz, CL 8 pF +
   2×10 pF. Mark all matching caps `tuning_required`.

**The FPC is its own fab deliverable** (flex stackup, coverlay, stiffener at the
connector, ferrite BOM line) — currently undesigned. See §5 G1.

---

## 4. Defects to fix (verified register)

Fab-blockers **[C]** all CONFIRMED under primary-source attack; important **[H]**;
DFM **[M]**. Fixes are specified; corrections from re-verification are marked ⚠.

### Fab-blocking [C]
| # | Defect | Fix |
|---|---|---|
| C1 | J2 = Hirose FH12-50S (**bottom**-contact); display needs **top**-contact → won't mate | swap to **FH12A-50S-0.5SH(55)**; rebuild footprint (footprint editor) |
| C2 | J2 **pin order mirrored** (pad-1/LEDA at x=44.25 but tail pin-1 lands at x≈19.75) | fix in the footprint rebuild (pin-1 to low-x); verify vs physical tail at first article. **Do the mirror ONCE, in the footprint — not also via net-reversal** |
| C3 | Backlight boost drives **4 parallel** LEDs from a 4.4 V node → overdrive, can't switch off | **RESOLVED (verified 2026-07-04): replace TPS61165 + L15 + D15 with `MP3022` (Monolithic Power) — a 4-channel inductorless charge-pump WLED driver, 2.7–5.5 V in, 30 mA/ch (120 mA cap. for our 80 mA), per-channel current limit, PWM/pulse dimming.** It drives the panel's 4 separate cathodes (LEDK1-4) as balanced current sinks and its 1×/1.5×/2× charge pump works both above and below Vf across the whole Li range (fixes the boost's "can't-regulate-down"; the charge pump removes the inductor+diode → less EMI). Wiring: VIN→SYS_PWR_IN, EN←TFT_BACKLIGHT_PWM, CPO→LEDA, D1-4→LEDK1-4, + flying caps. Alt: MAX1576 (boost, 100 mA/ch). ⚠️ NOT AL8860 (min VIN 4.5 V), NOT a plain boost. **⚠️ The MP3022 footprint is specialized (not in the KiCad std lib) → build it from the datasheet in the footprint editor before placing.** |
| C4 | NFC RF front-end **uncaptured**: ST25R3916B symbol has 15/33 pins; ANT1 empty copper | rebuild the 33-pin symbol; wire the front-end (§3); draw the FPC loop |
| C5 | 69 open connections (unrouted) | complete routing (GUI, after re-floorplan) |
| C6 | Board vs debug spec inconsistent: 6 SWD-redundant TP_* are "required" but SWD is on J7 | **remove the SWD-redundant TP_* from the required BOM** (J7/TC2030 provides them); keep TP_UART + TP_BOOT0 |

### Important [H] — with the re-verification corrections
- ⚠ **47 kΩ pull-up goes on `TROPIC_SPI_MISO` (SDO) → TROPIC_VCC** — **NOT CSN**.
  (Verified: devboard R1 is on SDO/MISO; TROPIC01 SDO is High-Z at idle → the
  pull-up gives libtropic a clean 0xFF idle. Old notes/03-connectivity said CSN —
  wrong pin.)
- ⚠ **Charge current** R10=1.13k → 788 mA = **3.15C** for the 250 mAh cell → set
  **R10 = 3.57 kΩ** (250 mA, 1C); R12 (ITERM) = 2.94 kΩ; **R9 (ILIM) = 3.24 kΩ**
  (497 mA, USB-compliant — the chain is currently inverted: 1.36 A > 0.96 A > 0.5 A).
- ⚠ **VBAT_SENSE** divider 1M/330k = 248 kΩ ≫ the **14-bit ADC1 R_AIN limit (100 Ω**,
  not 470) → add 100 nF reservoir at the ADC pin (or rescale).
- **HSE X1** load caps are placeholder + 6.5–13.7 mm away → pick 16 MHz CL 8 pF
  crystal, C18/C19 = 8 pF, move to the crystal pads.
- **Missing caps at the pin:** NRST 100 nF; OPTIGA VCC 100 nF; QSPI VCC 100 nF;
  TROPIC_VCC 2.2–4.7 µF bulk; buck **10 µF at VOS** (current bulk is 37.6 mm away);
  charger IN 4.7 / OUT 10 / BAT 4.7 µF (currently zero); NFC VDD rails (7–9 caps at
  the pins) + NFC_VCC 10+1+0.1 µF; DISPLAY_VCC_SW 2.2 µF+100 nF; VBUS 10 µF at J1.
- **ST25R3916B VDD_DR→VDD_RF** strap (regulator mode). **C6 TROPIC ramp** 1 nF→470 pF.
- **Pull-downs** 100 k on NFC_PWR_EN / TFT_PWR_EN (TPS22917 ON must not float).
  **Touch I2C pull-ups** 4.7 k (currently absent → bus can't work).
- **LED_G** off PC15 (no timer/PWM) → PE9 (TIM1_CH1). **USB ESD U7** inline on D±.
- **VBUS TVS**; **Qwiic J6** polyfuse.

### DFM [M]
DISP1 envelope still models the OLD Newhaven display → replace with ER-TFT024IPS-3
envelope. Add **fiducials** (3 F.Cu + 2–3 B.Cu, double-sided assembly). **BOM** now
complete (`production/bom/pcbway-bom-complete.csv`, 97 parts, 0 placeholders).
Design rules already tightened to PCBWay minimums. Panelize (board < 50×50) + centroid
at export. J2 mouth-face → y≈48 (fold reach).

---

## 5. Open design decisions (found by the completeness critic — resolve before fab)

These are **system-boundary** gaps a schematic review misses. Several are
security-relevant on a wallet.

- **G1 [must] The antenna FPC is decided but undesigned** — no J-ANT connector on the
  board yet (ANT1 on-board must be removed), no flex gerbers/stackup/stiffener, no
  connector chosen, no ferrite BOM line. Biggest hole; it is the feature you most want. → design the FPC (§3).
- **G2 [must] Loop over the battery = worst-case metal proximity.** Works with full
  ferrite coverage but expect range loss; plan a first-article **read-range test** and
  a fallback (loop shifted off the cell if the industrial design allows).
- **G3 [must] Brown-out:** the 3.3 V **buck can't hold regulation below ~3.4 V VBAT**;
  an NFC-TX burst (250–500 mA) near end-of-charge can dip the rail and **reset the MCU
  mid-crypto**. Decide: buck-boost (TPS63802) for immunity + full capacity, or firmware
  UV-cutoff ≈3.5 V + set STM32 BOR. (Old power note P14 mis-assumed the buck regulates at 2.9 V — it can't.)
- **G4 [must] No ship mode** → a 250 mAh cell deep-discharges in storage (weeks). Add a
  latched load-switch / ship-mode, or a documented auto-shutdown + storage policy.
- **G5 [should] ESD only on USB** — add **button RC (100 Ω+100 nF)**, an antenna-terminal
  ESD provision, and Qwiic ESD (needed for IEC 61000-4-2 / CE-FCC).
- **G6 [should, security] No hardware tamper** — STM32U5 TAMP pins unused; wire ≥1 to a
  case-open switch/mesh and enable tamper→backup-domain secret-erase.
- **G7 [should] No LSE + VBAT tied to SYS_3V3** → RTC/tamper-timestamp is **not
  persistent** (resets when the LiPo dies). Add 32.768 kHz LSE + a small VBAT backup, or
  document secure-time as non-persistent.
- **G8 [must] Battery connector J9 = the top mechanical decision** (see §1): the JST-PH
  makes the device ~13.5 mm, collides with MH4, and caps the cell → **go to solder tabs /
  low-profile pads** (~11 mm, 340 mAh, collision cleared). Plus [should]: enclosure stack
  drawing — button plunger stroke, USB-C aperture Z-alignment, screw-boss keepouts, display bond.
- **G9 [should] Thermal** — add EP via-farms for U10 (charger) & U3 (buck) (only U9's was
  specced) + a one-line Tj = Ta + θJA·P budget. (Fine once the 250 mA charge current is set.)
- **G11 [should, security] No SWD lockdown plan** — TC2030 SWD is exposed on a shipped
  wallet. Plan **RDP level 2** (or fuse/disable SWD) after provisioning.
- **G12 [minor] 13.56 MHz intentional-radiator pre-compliance** (FCC 15.225 / EN 300 330)
  — budget a first-article test.

*(Satisfied by silicon, not gaps: STM32 TRNG + TROPIC01 RNG → no external entropy part;
VIT6 is LDO-only → no SMPS inductor.)*

---

## 6. Files in this folder (what's authoritative)

- **`README.md`** (this file) — the single source of truth.
- **`kicad/`** — the canonical board (`.kicad_pcb/.kicad_pro`), the schematic sheets
  (`sheets/*.kicad_sch` — currently **stubs**; the schematic must be rebuilt from §2–4,
  since the generator drifted from the hand-edited board), libs/models.
  ⚠️ **The committed `.kicad_pcb` is the pre-rebuild baseline** (42.72×39.8 mm, on-board
  ANT1, `make ci` green). The GUI finish applies this record: §1 shrink to 36.8 mm, §3
  FPC antenna (remove ANT1, add J-ANT), §4 fixes, then place + route. This README is the
  spec the board file is brought up to — not a description of the current file.
- **`production/`** — machine contracts consumed by the repo validators
  (`netlist-contract.json`, `pinmux-ledger.json`, `schematic-binding.json`,
  `pcbway-manifest.json`) + **`bom/pcbway-bom-complete.csv`** (the real BOM).
- **`docs/`** — the **project design documents**, one per subsystem (`mechanical.md`,
  `power.md`, `mcu-and-secure-elements.md`, `nfc.md`, `placement.md`, `connectivity.md`,
  `parts-and-bom.md`, `fabrication-dfm.md`, `open-decisions.md`, `verification.md`,
  `reference-trezor-safe7.md`, `board-measurements.json`). This README is the overview;
  these are the per-subsystem detail. **This is the project record, not a dated review.**

## 7. The finish (the three gates)
1. **Schematic + placement + route** in KiCad GUI, from §2–4 + `docs/placement.md`
   (per-component position/rotation) + `docs/connectivity.md` — density ~79 % is
   routable; final routing is push-and-shove.
2. **Draw the antenna FPC** (§3, G1) as its own flex.
3. **Build a first article → tune the antenna on a VNA + read-range test** (§3, G2),
   then freeze the `tuning_required` values. Order params: 4-layer / 1.6 mm / ENIG /
   min-hole 0.3 / no impedance control / tab-route panel / double-sided assembly.
