# Part Selections — resolving every placeholder + specifying every added part

Date: 2026-07-03. Turns the review's fix specs into concrete, purchasable parts
so the BOM goes from 16/103 to complete. Every value is traceable to a
`review-2026-07/` report (nfc-rf-frontend, power-architecture, mcu-secure,
mechanical-display, trezor-safe7-reference). Parts chosen to be widely
distributor-stocked (Digi-Key/Mouser/LCSC) and, where practical, basic/extended
on JLCPCB/PCBWay assembly. **Values marked `TUNE` are first-article starting
points to be finalized by VNA measurement (RF) — see synthesis §1 Gate 2.**

Convention: C0402/R0402 = 1005-metric; all C0G/NP0 where noted are 50 V.

---

## A. Placeholders resolved (the 16 flagged)

| Ref | Was | Now | MPN (example) | Src |
|---|---|---|---|---|
| **X1** | "16MHz" | 16.000 MHz, CL=8 pF, ESR≤80 Ω, 3225-4 | Abracon **ABM8-16.000MHZ-B4Y-T** (or Epson TSX-3225 16.0000M) | mcu H1 |
| C18 | HSE_LOAD | **8 pF** C0G 0402 | — | mcu H1 (C=2·(CL−Cstray)=2·(8−4)≈8) |
| C19 | HSE_LOAD | **8 pF** C0G 0402 | — | mcu H1 |
| **X3** | "FA-238 27.12MHz" | 27.120 MHz, CL=8 pF, ESR≤50 Ω | Epson **FA-238 27.1200MF-C8** class (8 pF grade) — matches Trezor | nfc §5 / trezor |
| C34 | NFC_XTAL_LOAD | **10 pF** C0G 0402 | — | nfc §5 (Trezor 8pF+2×10pF) |
| C35 | NFC_XTAL_LOAD | **10 pF** C0G 0402 | — | nfc §5 |
| C30 | NFC_TUNE | **680 pF** C0G 0402 (EMC filter C0a) `TUNE` | — | nfc §3 |
| C31 | NFC_TUNE | **680 pF** C0G 0402 (EMC filter C0b) `TUNE` | — | nfc §3 |
| C32 | NFC_TUNE | **180 pF** C0G 0603 (series match Cs1) `TUNE` | — | nfc §3 |
| C33 | NFC_TUNE | **180 pF** C0G 0603 (series match Cs2) `TUNE` | — | nfc §3 |
| L30 | NFC_TUNE | **270 nH** wirewound 0603, ESR<0.5 Ω, Isat>0.5 A (EMC L0a) | Würth 744765127A class | nfc §3/§5 |
| L31 | NFC_TUNE | **270 nH** 0603 (EMC L0b) | — | nfc §3 |
| **D15** | D_SCHOTTKY | **DELETE** (backlight boost removed, see C-block) | — | power P1 |
| **L15** | 10uH | **DELETE** (backlight boost removed) | — | power P1 |
| **R15** | BL_SENSE | **DELETE** (backlight boost removed) | — | power P1 |
| RJ1/RJ2 | 0R | **KEEP** — correct current-sense jumpers (not placeholders) | 0 Ω 0402 | — |

## B. Backlight driver replacement (fab-blocker C3)

The panel is 4 **parallel** LEDs (common anode LEDA, cathodes LEDK1–4, Vf≈3.2 V,
~80 mA). Replace the boost with a **4-channel WLED current-sink** from SYS_PWR_IN
(4.4 V USB / 2.9–4.2 V batt — always ≥ Vf+headroom), PWM-dimmed.

| New ref | Part | Role |
|---|---|---|
| U15 (repl.) | **TI LP5024 / LM36011** class — *use* **Kinetic KTD2026** or **TI LM3697** ... | 4-sink WLED driver, I2C or PWM, from SYS_PWR_IN |
| — chosen: | **TI LM3697** (dual-string) or **ON NCP5623** | recommend a simple **4×parallel sink**: tie the 4 cathodes, sink to one channel of a **TI TLC5947/LM36011** |

> ⚠️ **CORRECTION (verified 2026-07-04): AL8860 is WRONG — do not use.** Diodes AL8860
> min VIN = **4.5 V** > SYS_PWR_IN's 4.4 V max (USB) and far above battery 2.9–4.2 V → it
> would **never turn on**. (A buck also can't regulate a 3.2 V load once Vin < ~3.7 V.)
> **Requirement:** drive 4 parallel Vf-3.2 V/80 mA strings from SYS_PWR_IN **2.9–4.4 V**,
> PWM-dimmed. **Correct class = a low-Vin WLED driver with current sinks:** a
> **charge-pump / buck-boost** WLED driver (constant brightness across the whole Li range),
> or a **linear 4-channel current sink** accepting graceful dim below ~3.5 V. The exact
> MPN needs its own selection + check (this is the one review fix that was mis-specified).
> `TFT_BACKLIGHT_PWM` → the driver's PWM/CTRL pin.

## C. Added decoupling / support parts (from the H-series findings)

All 0402 unless noted; C0G for <10 nF, X5R/X7R for ≥100 nF; place at the pin.

| Qty | Value | Where | Finding |
|---|---|---|---|
| 1 | 100 nF | NRST @ U1 pin14 | H3 |
| 1 | 47 kΩ | TROPIC CSN→TROPIC_VCC (switched) | H2 |
| 1 | 4.7 µF 0805 | BQ24074 IN (VBUS_LIMITED) | H6 |
| 1 | 4.7–10 µF 0805 | BQ24074 BAT / J9 | H6 |
| 1 | 10 µF 0805 | BQ24074 OUT (SYS_PWR_IN) | H6 |
| 1 | 4.7 µF 0603 | TPS62840 VIN | H6 |
| 1 | 10 µF 0805 | TPS62840 VOS/L1 (at the pin) | H7 |
| 1 | 2.2–4.7 µF | TROPIC_VCC bulk @ U2 | trezor/mcu |
| 3 | 2.2 µF∥10 nF ×3 | ST25R3916B VDD_A, VDD_D, VDD_RF/DR | H9/nfc §5 |
| 1 | 2.2 µF | ST25R3916B VDD_AM | nfc §5 |
| 1 | 1 µF∥10 nF | ST25R3916B AGDC | nfc §5 |
| 3 | 10 µF+1 µF+100 nF | NFC_VCC @ U9 | H9 |
| 2 | 100 nF | OPTIGA VCC, QSPI VCC | H16 |
| 2 | 4.7 kΩ | Touch I2C SCL/SDA pull-ups→SYS_3V3 | H13 |
| 2 | 100 kΩ | NFC_PWR_EN, TFT_PWR_EN pulldowns | H14 |
| 1 | 100 nF | VBAT_SENSE reservoir @ ADC pin | H19 |
| 1 | 2.2 µF+100 nF | DISPLAY_VCC_SW @ U14 + 1 µF near J2 | H21 |
| 1 | 1 µF+10 nF | VDDA/VREF+ @ U1 | mcu |
| 1 | 10 µF 0805 | VDD bulk @ U1 | mcu |
| 1 | TVS 5 V | VBUS @ J1 (e.g. TPD1E10B06 / SMF5.0A) | H20/trezor |
| 1 | 100–200 mA polyfuse | J6 Qwiic | H22 |
| C6 | **470 pF** | C6 1nF→470 pF (TROPIC VCC ramp ≤1 ms) | H15 (value change) |
| R9 | ISET/ILIM | R9→**3.24 kΩ**, R10→per battery (**3.57 kΩ** for 250 mAh@1C), R12→**2.94 kΩ** | H4/H5 |

## D. NFC RF front-end parts to ADD (matching/RX network, from nfc §3)

| Ref (new) | Value | Role | `TUNE` |
|---|---|---|---|
| Cp1/Cp2 | 120 pF C0G 0603 (240 pF diff) | parallel match | yes |
| Cr1/Cr2 | 180 pF C0G 0402 | RX series | yes |
| Cd1/Cd2 | 680 pF C0G 0402 | RX shunt | yes |
| Rd1/Rd2 | 0 Ω 0402 (→1.8–2.7 Ω) | damping | yes |
| (opt) AAT | varicap net DNP | auto-tune provision | — |

## E. Connector / mechanical parts

| Ref | Change | Part |
|---|---|---|
| **J2** | bottom→**top contact** + mirror pinout (C1/C2) | **Hirose FH12A-50S-0.5SH(55)** = ER-CON50HT-1 |
| **J-ANT** (new) | antenna FPC feed | 2-pin BTB or Molex 0.5 mm FPC / solder pads for `NFC_ANT1/2` |
| **DISP1** | old Newhaven → correct | `Display_Envelope_ER-TFT024IPS-3_42.72x59.46mm` (doc only) |
| J9 | shift right x≈46.5 (battery) | S2B-PH-SM4-TB (keep); consider adding NTC line (trezor) |
| Fiducials | add | 3× F.Cu + 2–3× B.Cu, Fiducial_1mm_Mask2mm |
| TP_3V3/BOOT0/GND/NRST/SWCLK/SWDIO | add (C6) | TestPoint_Pad_D1.0mm, grouped near J7 |

## F. Antenna FPC (separate small flex, D2)

Per Trezor-style + nfc §6: **Ø≈30 mm loop, L≥1 µH** (or the 34×6 mm strip form if
the back-cover space is rectangular), 2 terminals to J-ANT. Ferrite backing
**Würth WE-FSFS 374006** (cut to fit) between loop and the display frame. This FPC
is its own tiny fab item; matching network stays on the main board at U9. Final
turns/inductance set by first-article VNA tuning.

## Open sourcing note
All selections are widely stocked and swappable for JLCPCB/PCBWay basic-parts
equivalents at assembly time. **Two items still need a concrete pick + check before
ordering: the WLED backlight driver (AL8860 was rejected — see the correction above;
a low-Vin charge-pump/buck-boost or linear 4-sink is needed) and the low-profile
battery connector (JST-SH SM02B-SRSS-TB per `standard-parts.md`).** The FH12A display
connector and everything else are settled.

---

# Bare-board composability — can nSealr TROPIC01 sell BARE and be built with standard parts?

Date: 2026-07-04. Scope: verify the board can ship BARE (no display, no battery, no NFC
antenna) and be composed by the buyer from STANDARD, easy-to-source, non-exotic off-the-shelf
parts. Recommend the exact standard MPNs + connectors per external interface.

Sources: board authority `pcb/tropic01-universal-secure-device/README.md` + `design-notes/`
(board-truth.json, mechanical-fit.md, mechanical-display-integration.md, nfc-fpc.md,
part-selections.md, connectivity-spec.md); local datasheets; distributor/vendor web checks
(JST, Hirose, ST, BuyDisplay, Molex, Digi-Key/Mouser/LCSC) done this session.

**Overall verdict: ACHIEVABLE.** Four of the five external interfaces already map to buyable
standard parts. Two things block a clean "bare board + standard add-ons" story and both have a
concrete standard swap: (1) the **battery connector J9 (JST-PH, tall + collides with MH4)** →
go to **JST-SH**; (2) the **NFC antenna feed (Hirose BM28 0.35 mm)** is fine-pitch/reflow-only →
go to a **1.0 mm FFC or a 2-pin BTB**. The NFC antenna FPC itself is inherently custom (ship it
with the product; it is NOT a buyer-sourced standard). The display is standard-connector but
single-vendor.

---

## 1. BATTERY CONNECTOR (the main question) — VERDICT: swap JST-PH → JST-SH

### The current problem (confirmed)
- Current J9 = **JST-PH `S2B-PH-SM4-TB`**. Note: this is **already the SIDE-ENTRY (right-angle)
  SMT** variant — the "S2B" prefix = side entry; "B2B" = top entry. So "use a side-entry PH"
  does **not** help: the PH series is intrinsically tall at 2.0 mm pitch.
- Height (Z above PCB) ≈ **6.0 mm** (design-notes measured from JST ePH.pdf p.5; distributor
  data lists the side-entry PH as **8.0 mm mounting footprint / 4.5 mm width**). It is the
  **tallest F.Cu part on the board** and single-handedly drives the device to **~13.5 mm cased**.
- It **collides with MH4**: shifted right to x≈46.5 to clear the 32 mm cell, the ~8 mm PH body
  reaches x≈50.5 and overlaps the MH4 clearance hole (49.3–52.5). With PH you can have the 32 mm
  cell **or** MH4 clearance, not both.
- Current rating is not the issue (PH = 2 A; the cell needs ~250–580 mA peak).

### Candidate comparison (side-entry / horizontal, 2-pin, SMT)

| Connector | Example MPN | Pitch | Z-height | Body width | Rated | Fixes thickness? | Clears MH4? |
|---|---|---|---|---|---|---|---|
| **JST-PH** (current) | S2B-PH-SM4-TB | 2.0 mm | **~6.0 mm** | ~8 mm | 2 A | ✗ | ✗ |
| **JST-SH** (recommended) | **SM02B-SRSS-TB** | 1.0 mm | **~2.9 mm** | ~4.3 mm | **1 A** | ✓ | ✓ |
| JST-GH (secure alt.) | SM02B-GHS-TB | 1.25 mm | ~3.4 mm | ~4.9 mm | 1 A | ✓ | ✓ (tighter) |
| JST-ZH | S2B-ZR-SM4A-TF | 1.5 mm | ~3.6 mm | ~5.4 mm | 1 A | ✓ | borderline |

### Recommendation: **JST-SH `SM02B-SRSS-TB`** (1.0 mm, 2-pin, side-entry SMT)
- **Z-height ≈ 2.9 mm** → no longer the tallest F.Cu part (SW1 side button / J1 USB-C ~3.2–3.5 mm
  now dominate) → **resulting device thickness ≈ 11.0 mm cased** (front 0.8 + display 2.3 +
  [J2 gap 2.0 + PCB 1.6 + tallest-part 3.5] + back 0.8). That is **the same ~11 mm as the
  solder-tab option the README recommends — but PLUGGABLE**, which is what you want for a bare board.
- **MH4 collision cleared**: 2-pin SH body is only ~4.3 mm wide → at x≈46.5 it spans ~44.3–48.7,
  MH4 hole starts at 49.3 → ~0.6 mm gap. The 32 mm LP502030 cell and MH4 now coexist.
- **1 A rating is adequate**: system peak from the battery is ~460–580 mA (README power budget,
  incl. NFC TX bursts), charge set to 250 mA → ~1.7× margin.
- **Consistency bonus**: the board already uses the JST-SH family — J6 (expansion) is
  `SM04B-SRSS-TB`. Reusing SH for the battery means one connector family, one crimp tool, fewer
  BOM lines.
- **Trade-off / the one caveat (what cells ship with):** the maker-default 1S LiPo pigtail is
  **JST-PH 2.0** (Adafruit, SparkFun, Turnigy, most 100–2000 mAh packs). **JST-SH 1.0** is the
  established *wearable / FPV / compact* connector (1 A, SMD) but is less common as a factory
  pigtail. This is a non-issue in practice because **you are already telling the buyer the exact
  cell (EEMB LP502030)**: LiPo vendors crimp the connector to order — 1.0 / 1.25 / 1.5 / 2.0 mm
  are all standard options (confirmed on EEMB/PKCell/AliExpress listings). So the buyer orders
  "LP502030 with JST-SH pigtail," or uses a JST **PH-to-SH adapter** cable. Spec it in the
  "recommended standard parts" list shipped with the bare board.

**If you insist the battery must mate the default PH-2.0 pigtail that most cells ship with:** keep
`S2B-PH-SM4-TB` but accept ~13.5 mm thickness AND move MH4 inboard (breaks corner symmetry) or
accept a ≤30 mm / lower-capacity cell. This is strictly worse than SH; only choose it if
"plug any random hobby LiPo unmodified" outranks thickness. The README's own fallback (solder
tabs) gives ~11 mm but is NOT pluggable, so **SH is the best standard + pluggable + low-profile
answer.**

> **BATTERY VERDICT: JST-SH `SM02B-SRSS-TB`, ~2.9 mm tall → device ~11.0 mm cased.** Standard
> (Digi-Key/Mouser/LCSC), same family as J6, clears MH4, fits the 32 mm cell. Order the LP502030
> with an SH pigtail (a standard crimp option) or use a PH→SH adapter.

---

## 2. DISPLAY — VERDICT: connector is standard; the module is single-vendor but not exotic

- **ER-TFT024IPS-3** (EastRising/BuyDisplay, 2.4" IPS 240×320, ST7789V + FT6336 cap-touch, single
  50-pin 0.5 mm FFC, top-contact): **ordinary panel, single-source module.** The 2.4" IPS ST7789
  panel is ubiquitous and cheap, but this **exact model with this exact 50-pin FFC pinout is sold
  by BuyDisplay/EastRising, NOT stocked on Digi-Key/Mouser** (confirmed). It is reliable and
  low-MOQ (buy 1-off on their site), so "easy to source" = yes from one vendor; "multi-distributor
  commodity" = no.
- **Is the 50-pin FFC the exotic part vs a common 8-pin SPI breakout?** No — it is the *normal*
  form for an OEM cover-glass module. Raw modules of this class break out the full interface
  (8080 parallel + SPI + cap-touch I2C + backlight) on a ~40–54-pin 0.5 mm FFC; 50-pin is typical
  (the prior Newhaven NHD-2.4 candidate was also ~50-pin FFC). The common **8-pin SPI breakout**
  (Adafruit/Waveshare) is a *different product class*: a small carrier PCB with the FFC already
  mated + level shifters + its own header — you **cannot fold that flat behind the glass** for a
  thin handheld. For THIS integrated thin design the 50-pin raw-FFC module is the correct and
  standard choice.
- **Connector `FH12A-50S-0.5SH(55)` (Hirose, top-contact, 50-pin 0.5 mm)** — a **standard,
  buyable Hirose part** on Digi-Key/Mouser (this is the C1/C2 fix already in the register: the
  committed board wrongly uses the bottom-contact `FH12-50S-0.5SH`). Keep it.
- **The real lock-in is the pinout, not the connector.** Any 2.4" module you target pins its FFC
  differently, so the board is always tied to ONE module's 50-pin map. There is no "generic 2.4in
  SPI module pinout" to design against.

> **DISPLAY VERDICT: KEEP ER-TFT024IPS-3 + `FH12A-50S-0.5SH(55)` (both standard-form; connector is
> a commodity Hirose part).** Not exotic, but document it as **single-vendor (BuyDisplay)** and
> publish the exact 50-pin pinout in the bare-board "required standard parts" sheet so a buyer can
> source that model (or a pin-compatible clone). No cheaper "more standard" swap exists that keeps
> the fold-flat thin form; the 8-pin breakout is not usable here.

---

## 3. NFC — VERDICT: reader is standard; swap the fine-pitch feed; the antenna FPC is custom

- **ST25R3916B reader: STANDARD & AVAILABLE.** Active/in-production, ships-today at Digi-Key &
  Mouser (`ST25R3916B-AQET` 32-UFQFN ~$6.5; also `-AQWT` QFN, `-BWLT` WLCSP), ~8-week factory
  lead. No concern. Keep.
- **Antenna feed `BM28` (Hirose 0.35 mm mezzanine, Trezor's part): NOT buyer-friendly / borderline
  exotic.** It is a catalog part (available, many pin counts), BUT at **0.35 mm pitch** it is
  **reflow-in-nitrogen recommended, vacuum pick-and-place designed, rated only 10 mating cycles,
  and needs a ≥0.3 mm FPC stiffener** — i.e. fine-pitch, not hand-assemblable, not meant for
  repeated connect/disconnect. Wrong fit for a "bare board a buyer composes."
- **Recommended standard feed connector (mates a 2-wire NFC antenna FPC):**
  1. **Primary — a standard 1.0 mm-pitch 4-position FFC/FPC connector** (feed on the middle 2 pads,
     GND on the outer 2). This is the exact scheme off-the-shelf NFC antenna flexes already use
     (e.g. the iLabs 13.56 MHz flex antenna uses a "1 mm pitch 4-lead flat cable, feed on the
     middle pins, 2 GND pins around it"). Coarse-pitch, hand-assemblable, buyable (Hirose FH12,
     Molex, JST), and lets a buyer clip in a standard NFC-antenna FPC. Keep the differential pair
     short (<8 mm) and void all copper under the feed/loop.
  2. **Alternate — a 2-pin board-to-board (e.g. JST/Molex 0.8–1.0 mm BTB)** if you want a soldered,
     RF-clean parallel-fold like Trezor without the 0.35 mm pitch.
  - Design-notes caution: a plain 2-pin **JST-SH/wire** feed adds series L + ground-return
    asymmetry on the high-Q antenna node — acceptable if you re-tune, but the 1.0 mm FFC (symmetric
    feed+GND) or a BTB is preferred for RF.
- **Are standard 13.56 MHz NFC antenna FPCs buyable off-the-shelf?** **Yes for generic ones, but
  NOT for THIS device.** Off-the-shelf adhesive/flex NFC antennas exist (Molex 146236 series,
  iLabs flex, Digi-Key RFID-antenna category). **However this design needs a CUSTOM loop:**
  ~38 × 20 mm rectangular/oval to fit the 22.66 mm battery band, ~1 µH at 3–4 turns, with a Würth
  WE-FSFS ferrite backing, tuned on a VNA to the on-board matching network. An off-the-shelf
  fixed-L antenna won't match the geometry or the matching values. → **The antenna FPC is a
  product-supplied custom flex (ship it with the board or publish its gerbers), NOT a buyer-sourced
  standard part.** Only the *feed connector* should be standard so board↔flex mate reliably.

> **NFC VERDICT: reader ST25R3916B = STANDARD (keep). Feed connector: swap BM28 0.35 mm → a
> standard 1.0 mm 4-pin FFC (feed+GND) or a 2-pin BTB. Antenna FPC = CUSTOM, shipped with the
> product — flag it as the one interface that cannot be "buyer off-the-shelf."**

---

## 4. OVERALL — external interfaces vs buyable-standard mapping

| Interface | Part on the bare board | Buyer add-on | Standard? | Action |
|---|---|---|---|---|
| **Display FFC** (50-pin 0.5 mm, top-contact) | `FH12A-50S-0.5SH(55)` (Hirose) | ER-TFT024IPS-3 module | Connector ✓ commodity; module ✓ ordinary but **single-vendor (BuyDisplay)** | Keep; publish exact 50-pin pinout + model. Fix C1/C2 (currently wrong bottom-contact `FH12-50S`). |
| **Battery** | J9 | 1S LiPo (LP502030) + pigtail | **Swap PH→SH** to be standard+low-profile+MH4-clear | **`SM02B-SRSS-TB` (JST-SH)**; order cell with SH pigtail / PH→SH adapter |
| **NFC antenna feed** | J-ANT | antenna FPC | Connector: BM28 0.35 mm is fine-pitch/exotic | **Swap to 1.0 mm 4-pin FFC or 2-pin BTB** |
| **NFC antenna FPC** | — | the loop flex | **NOT a standard off-the-shelf part** (custom ~38×20 mm, ~1 µH, ferrite, VNA-tuned) | Ship with product / provide gerbers; the one non-composable item |
| **USB-C** | J1 `USB4105-GF-A` (GCT, 16-pin, top-mount horizontal) | USB-C cable (commodity) | ✓ standard, Digi-Key/Mouser stocked; FS → no impedance control | Keep (swappable for any standard 16-pin USB-C receptacle) |
| **Expansion** | J6 `SM04B-SRSS-TB` (JST-SH, Qwiic/STEMMA-QT) | Qwiic cable | ✓ standard | Keep (add polyfuse per H22) |
| **Debug** | J7 Tag-Connect **TC2030** footprint (pads only, no connector) | TC2030-IDC cable | ✓ standard (Tag-Connect) | Keep |
| **Side button** | SW1 `EVQ-P7J01P` (Panasonic) | — (on-board) | ✓ standard | Keep |

**Exotic items to change (all have a standard swap):**
1. **J9 JST-PH → JST-SH `SM02B-SRSS-TB`** — thickness 13.5 → ~11 mm, clears MH4, stays pluggable+standard.
2. **NFC feed BM28 0.35 mm → 1.0 mm 4-pin FFC (or 2-pin BTB)** — hand-assemblable, mates standard NFC flex.
3. **Display connector** already flagged (C1/C2): bottom-contact `FH12-50S` → top-contact `FH12A-50S-0.5SH(55)`.

**Genuinely can't be "buyer off-the-shelf" (document, don't pretend otherwise):**
- The **NFC antenna FPC** (custom geometry/inductance/ferrite, VNA-tuned) → product-supplied.
- The **display model** is single-vendor (BuyDisplay) though the *connector* is a commodity.

---

## Bottom line
- **Battery connector (headline answer): use JST-SH `SM02B-SRSS-TB`** — 1.0 mm side-entry SMT,
  **~2.9 mm tall, 1 A**, same family as J6. **Resulting device thickness ≈ 11.0 mm cased** (down
  from ~13.5 mm), and the J9↔MH4 collision is cleared with the 32 mm cell in place. Order the
  LP502030 with an SH pigtail (standard crimp option) or a PH→SH adapter.
- **Display:** standard-form; **keep ER-TFT024IPS-3 + Hirose `FH12A-50S-0.5SH(55)`**; single-vendor
  module, commodity connector — not exotic, publish the pinout.
- **NFC:** reader **ST25R3916B is standard/stocked**; **replace the BM28 0.35 mm feed with a
  1.0 mm 4-pin FFC or a 2-pin BTB**; the **antenna FPC is custom** and ships with the product.
- **USB-C, expansion, debug, button:** all already standard, buyable, keep.
- **Standalone-bare-board goal: ACHIEVABLE** with the two connector swaps above; the only interface
  that cannot be a buyer-sourced commodity is the tuned NFC antenna flex, which the product must
  supply.
