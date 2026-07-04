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
