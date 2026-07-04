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
