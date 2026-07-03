# Trezor Safe 7 (rev D) — Competitive Reference vs. nSealr TROPIC01 board

**Analyst pass: 2026-07-03.** First shipping product on the TROPIC01 secure element; Trezor
publishes the open hardware. Cross-checked against our board
`hardware/pcb/tropic01-universal-secure-device/` (ground truth: `design-notes/review-2026-07/board-truth.json`
placement + the three prior subsystem reports `power-architecture.md`, `mcu-secure-elements.md`,
`nfc-rf-frontend.md`, all of which extracted nets from the `.kicad_pcb`).

## Sources actually opened (Read tool, page-by-page)

Main schematic `ts7_main_rev_d_sch.pdf` is a **15-page** hierarchical set. Page→sheet map
(verified from the extracted text + each sheet's title block):

| PDF page | Sheet (SchDoc) | Title | Rev |
|---|---|---|---|
| 2 | TS7_MCU | Microcontroller | D |
| 4 | TS7_USB | USB connector & protections | B |
| 5 | TS7_Power | Power management (PMIC) | C |
| 7 | TS7_Power_Batt | Battery interface | B |
| 8 | TS7_Conn_NF | Near-field (NFC/Qi) coils interface | B |
| 10 | TS7_Radio_NFC | NFC Reader | B |
| 11 | TS7_SE_Tropic | Tropic secure element | C |
| 12 | TS7_SE_Optiga | Optiga secure element | A |
| 13 | TS7_Display | Display interface | C |
| 15 | TS7_Conn_UI | UI FPC interface | D |

Plus `ts7_fpc_ant_rev_d_sch.pdf` (1 pg, antenna FPC schematic, rev D "No NTC") and
`ts7_fpc_ant_rev_d_views.pdf` (1 pg, antenna FPC layout view). All 12 pages above were opened
and read visually; nothing below is guessed. Pages 3 (MCU_Power), 6 (Power_Qi), 9 (Radio_BLE),
14 (Haptic) were not needed for the 8 target areas (Qi/BLE/haptic are subsystems we don't have).

**Headline architectural difference:** Trezor Safe 7 is a *richer* device — it adds Qi wireless
charging, a BLE radio (nRF), a haptic driver, and an ambient-light sensor that we do not have, and
it uses an integrated **nPM1300** PMIC + **MIPI-DSI** display + **STM32U5G9** where we use discrete
charger/buck + **SPI** display + **STM32U585**. Many "differ" verdicts below flow from those two
deliberate, legitimate scope choices, not from error.

---

## 1. TROPIC01 circuit (Trezor p.11 TS7_SE_Tropic rev C; ours: U2 TR01-C2P-T301)

| Item | Trezor Safe 7 (p.11) | Our board | Verdict |
|---|---|---|---|
| Decoupling | **3×100nF (C101/C102/C103) + 1×4.7µF bulk (C104)** on VCC (pins 1/11/24), to GND | 3×100nF (C3/C4/C5), **no bulk** | **SHOULD-ADOPT** the 4.7µF bulk (mcu-secure-elements.md §3 already flags this; we power-cycle U2 so a bulk cap on the switched rail helps the re-inrush and TX/crypto current steps) |
| Host interface | **SPI (SDI/SDO/SCK/CSN = pins 5/6/7/8) AND the TPDI bus (TPDI_CSN 22, RDY 14, CLK 17, DIO0-3 = 21/20/19/18)**, both brought to the MCU; GPO4/INT (pin 4) wired to host | SPI1 only (PA4-7); our TR01-C2P-T301 / ODD_TR01 A.11 silicon has no TPDI | **OK-to-differ** — Trezor's newer silicon variant exposes TPDI (debug/provisioning); SPI is the production data path on both. No level shifting either side (3.3V) |
| SPI pull-ups | **R31 47k to the switched 3V3 rail ("3T3")** on the SPI side (the SDO/MISO line per DS Fig 23), **R35 47k to GND** on the INT line; TPDI side R32/R33/R34 47k | **Missing** the 47k MISO/SDO pull-up entirely | **SHOULD-ADOPT** 47k on TROPIC_SPI_MISO → switched rail. This is the DS Fig 24 / TS1702 reference resistor; libtropic L1 relies on a clean 0xFF idle byte (mcu report §3, action #3) |
| CSN pull-up | No *dedicated* CSN pull-up on p.11 — the 47k house value sits on SDO + INT, not CSN | none | **OK-to-differ** — a CSN pull-up is optional hardening on both designs (mcu report lists it as DNP-able insurance); neither Trezor nor the DS mandates a specific CSN value |
| Test/scan modes | **SCAN_MODE(9), TPM(13), F_TEST_MODE(30), TEST_MODE(31) all tied to GND** | pins 30/31→GND, 22→VCC per DS Fig 24 (mcu report §3) | **MATCH** — both disable test/scan at the pins (security-correct) |
| Power-gating method | **YES, they power-cycle it. High-side P-FET Q4 = CSD25501F3**, gate pulled up by R36 47k, driven by PWR_EN → generates switched "3T3" rail; TP9 testpoint on the rail | **YES** — high-side **TPS22917 load-switch (U4)**, ON=TROPIC_PWR_EN + 47k pulldown, CT slew cap C6, QOD tied to VOUT, RJ1 0R sense jumper | **MATCH (intent) / OK-to-differ (part).** Both hard power-cycle the SE high-side. Ours is a single load-switch IC with defined slew + quick-output-discharge vs their discrete P-FET; **ours is arguably the tidier one-part solution.** Caveat unrelated to Trezor: our C6=1nF gives ~1.6ms ramp, over TROPIC01's 1ms TVCC_RAMPUP (power report P7 — drop to 470pF) |

**Note on the 47k "house value":** Trezor uses 47k on *every* SE pull/gate resistor (Q4 gate,
SDO, INT, and — see §8 — the OPTIGA and display gate P-FETs). We use 47k on the TROPIC ON-pin
pulldown (matches), but are missing it on MISO.

---

## 2. Host MCU & TROPIC01 connection (Trezor p.2 TS7_MCU rev D; ours: U1)

| Item | Trezor Safe 7 (p.2) | Our board | Verdict |
|---|---|---|---|
| Host MCU | **STM32U5G9ZJ** (BGA; high-end U5 "G9" with MIPI-DSI host, large flash/RAM) | STM32U585VIT6 (LQFP-100, no DSI) | **OK-to-differ** — we drive an SPI panel at 240×320; we don't need the DSI-class part. Legit cost/size choice |
| TROPIC link | Dedicated **TR_SPI** (own SPI instance) **+ TR_TPDI** (7-wire, on Port D) **+ TR_INT + TR_PWR_EN**, all **direct 3.3V, no level shifting** | SPI1 (PA4/5/6/7) + GPO→PB2 + PWR_EN, direct 3.3V | **MATCH** on the SPI path (no translators on either side). We simply don't wire TPDI |
| NFC link | Separate **NFC_SPI** instance + NFC_IRQ | SPI2 (PB12-15) + IRQ (mcu report §1.7) | **MATCH** |
| Clocks | **32MHz HSE (X1, 2016, CL=10pF, 2×12pF) + 32.768kHz LSE (Y1, 2012, CL=9pF, 2×12pF)** | 16MHz HSE (X1, values are placeholder "HSE_LOAD"); **no LSE** — RTC on LSI | **SHOULD-CONSIDER LSE** (security timestamp accuracy) + **SHOULD-FIX** our placeholder HSE caps/MPN (mcu report §1.3). Not a Trezor-specific gap but they show the correct pattern |
| NRST | **100nF (C5) on NRST** | **no cap on NRST** | **SHOULD-ADOPT** (mcu report §1.4, DS Fig 38). Cheap glitch/tamper robustness on a secure device |
| Tamper | **TAMP net wired to the STM32 tamper pin** (+ J10 header) | not wired | **SHOULD-CONSIDER** (see §8) |

---

## 3. NFC front-end (Trezor p.10 Radio_NFC rev B, p.8 Conn_NF, FPC PDFs; ours: U9)

| Item | Trezor Safe 7 | Our board | Verdict |
|---|---|---|---|
| Controller | **ST25R3916B, WLCSP** (ball grid, p.10) | ST25R3916B-**AQET (QFN32)** | **MATCH** — same silicon, different package |
| Antenna construction | **Off-board on a Ø30.00mm round FPC** (`ts7_fpc_ant_views` p.1 dimensions Ø30.00mm) behind the (non-metallic) back cover; NFC loop is the **outer** spiral, Qi coil the dense **inner** spiral, concentric. **NFC coil L ≥ 1µH** (FPC sch p.1 note); Qi coil L ≥ 13.5µH | **On-PCB** strip (ANT1, 42×8mm envelope), currently an unbuilt placeholder squeezed above the display frame with a coplanar battery | **SHOULD-CONSIDER the FPC approach.** Putting the loop on a flex on the back cover *decouples it from the main-board GND planes, battery and display metal* — the single biggest robustness win. nfc-rf-frontend.md §6 already lists "move loop to an FPC" as the recommended fallback. Our strip is viable but needs a 4-layer keepout + ferrite + first-article VNA tuning to work at all |
| Matching network | **Lemc 270nH, Cemc 680pF, Cs 150pF, Cp 70pF, Rdamp 2Ω, Cdiv 180pF** (Table 2 on p.10). Implemented: L5/L6 270n, C71/C86 150p (Cs), C77/C83 680p (Cemc), C105/C106 68p (Cp), C78/C84 180p (Cdiv), C76/C85 10p trims, **R37/R38 2Ω series damping** | Placeholders only (C30-C33/L30/L31 = "NFC_TUNE", no values); RJ1/RJ2 0R jumpers but no valued damping | **SHOULD-ADOPT the topology + EMC values.** Use Trezor's 270nH/680pF EMC filter (fc≈11.7MHz, in the 8-17MHz / ∉13-14MHz window) as-is; scale Cs/Cp because our target La≈400nH ≠ their 1µH (nfc report §3 already reproduced Trezor's table analytically and derived our starting values). Adopt the 2Ω series-damping provision |
| Ferrite / battery-display decoupling | Antenna on separate flex → inherently isolated from planes; ferrite is on the flex stack | none (planes currently cover the antenna band) | **SHOULD-ADOPT** ferrite + 4-layer keepout if we keep it on-PCB (nfc report §4) |
| Crystal + load caps | **X3 27.12MHz, 2.0×1.6mm (2016), CL=8pF, Cpin=3pF, load caps C89/C90 = 2×10pF** | X3 FA-238 27.12MHz (CL suffix unpinned), C34/C35 = "NFC_XTAL_LOAD" | **SHOULD-ADOPT** the explicit CL discipline: pin the FA-238 CL grade and set load caps to match (10pF if CL=8pF class, ~15pF if CL=12pF). nfc report §5 |
| Supply decoupling | **Full DS13541 §4.2.10 pattern**: VDD block C67/C69 2.2µF ∥ C68/C70 10nF; VDD_RF_DR C72 4.7µF ∥ C73 10nF; VDD_D C79 2.2µF ∥ C80 10nF; VDD_A C87 2.2µF ∥ C88 10nF; VDD_AGD C81 1µF ∥ C82 10nF; VDD_AM C75 22nF | Partial (C36-C40 + one 2.2µF), several DS pins not even in our symbol | **SHOULD-ADOPT** the full network (~7-9 caps + symbol pins missing — nfc report §5, the single largest BOM gap on the NFC block) |

---

## 4. Battery + charging (Trezor p.5 TS7_Power rev C, p.7 TS7_Power_Batt rev B)

| Item | Trezor Safe 7 | Our board | Verdict |
|---|---|---|---|
| Charger / PMIC | **nPM1300** (Nordic): integrated **800mA** Li-ion/Li-poly/**LiFePO4** charger, SYSREG 1500mA, 2× buck 200mA, 2× load-switch/LDO, LED driver, USB-CC detect, TWI (p.5 block diagram) | Discrete: **BQ24074** linear charger (U10) + **TPS2553** USB current-limit switch (U8) + **TPS62840** buck (U3) | **OK-to-differ** — single-PMIC vs discrete. power-architecture.md P14 explicitly calls our single-buck path "a legitimate simpler alternative at these budgets." Fewer firmware dependencies; more board area |
| Charge current | Up to 800mA under nPM1300 NTC/JEITA control | **788mA programmed (R10 1.13k) = 2.6-5.3C for the ~150-300mAh pack that physically fits** | **SHOULD-FIX (independent bug).** power report P2 — reprogram R_ISET to the chosen cell's 0.5-1C. Trezor's 800mA is fine for *their* larger cell + NTC; ours is mis-scaled for a tiny pack with no thermal feedback |
| Battery NTC / thermal | **Pack NTC monitored** (BAT_NTC, dual terminal — p.7 connector, p.5 nPM1300 NTC pin) → JEITA temperature-qualified charging | BQ24074 TS pin **fixed with 10k** (NTC disabled); 2-pin JST (VBAT+GND only), **no thermistor** | **SHOULD-CONSIDER** adding NTC sensing for a LiPo (safety); at minimum document the fixed-TS decision |
| Battery connector | **BM28B0.6-6DS/2-0.35V** (6-pin BTB): VBAT + GND + 2×NTC | JST **S2B-PH-SM4-TB** (2-pin) | **OK-to-differ** (connector choice), but ours carries no NTC |
| Protection | Pack-integrated + nPM1300 (OV/UV/OC + NTC) | Pack-integrated only; **also missing IN/OUT/BAT bulk caps** (power P4) | **OK-to-differ** on protection philosophy; **SHOULD-FIX** the missing charger caps regardless |
| Input source OR-ing | USB **and** Qi wireless OR'd into VBUS via dual Schottky **PMEG4010CPAS** (D1A/D1B) | USB only | **OK-to-differ** — we have no wireless charging |

---

## 5. USB-C protection chain (Trezor p.4 TS7_USB rev B)

| Item | Trezor Safe 7 (p.4) | Our board | Verdict |
|---|---|---|---|
| Connector | GCT **USB4720** receptacle | GCT **USB4105-GF-A** | OK-to-differ (both GCT USB-C) |
| VBUS ESD/TVS | **2× TPD1E10B06DPYR** (single-line, 6V standoff) on VBUS_A/VBUS_B | **NONE on VBUS** (U7 TPD4E05U06 covers only D+/D-/CC) | **SHOULD-ADOPT.** power report P9 independently flagged the missing VBUS transient clamp; Trezor confirms a discrete VBUS TVS is standard here |
| Data/CC/SBU ESD | **TPD6E05U06RVZR** (6-channel, 0.5pF) on DP/DN/CC1/CC2/SBU1/SBU2 | **TPD4E05U06DQAR** (4-channel) on DP/DN/CC1/CC2 | **MATCH (equivalent for our pin count)** — we don't route SBU, so 4-ch is adequate. (Our ESD placement is 9mm off-axis/stub — layout fix in mcu report §2, not a Trezor delta) |
| CC resistors (Rd) | **Integrated in nPM1300** — CC1/CC2 routed to the PMIC's CC pins, no discrete 5.1k | Discrete **R1/R2 5.1k Rd** pulldowns (correct UFP) | **OK-to-differ** — ours is the standard discrete-UFP approach; both correct |
| VBUS current limiting | Inside nPM1300 (SYSREG 1500mA + charger input limit) | TPS2553 (~0.96A) + BQ24074 ILIM (1.36A) | **SHOULD-FIX (independent).** power report P3 — our two limits + USB-default 500mA are incoherent/non-compliant. Not a Trezor delta, but they get it "for free" in the PMIC |
| Shield grounding | **1MΩ ∥ 4.7nF to GND** (R9/R10 1M, C28/C29 4n7), per shield | (not evident in placement) | **OK-to-differ / minor** — could adopt the 1M∥cap shield network |

---

## 6. Display + backlight (Trezor p.13 TS7_Display rev C)

| Item | Trezor Safe 7 (p.13) | Our board | Verdict |
|---|---|---|---|
| Panel interface | **MIPI DSI** (2 data lanes + clock, differential), connector J5 **DF37B-24DS-0.4V** (24-pin) | **SPI** (ST7789V) + 50-pin parallel FFC (Hirose FH12) — ER-TFT024IPS-3 | **OK-to-differ** — entirely different panel class; our SPI panel is the simpler/cheaper choice |
| Backlight driver | **TPS61062 boost** for a **SERIES LED string** (Vf **9.3V** ⇒ ~3 LEDs in series, If **40mA**); L7 15µH (SRN2510BTA-150M); FB regulates 500mV across R23 **12.4Ω** = 40mA; VIN = VSYS ("5V") | **TPS61165 boost** driving a **4-parallel common-anode** panel (LEDA + 4 cathodes), R15 = placeholder "BL_SENSE" | **SHOULD-FIX (critical, our topology is wrong).** power report P1: a boost is correct for a *series* string (exactly Trezor's case) but **cannot regulate/​shut off** our parallel-cathode panel — DC path over-drives the LEDs ~4× and can't be turned off for VIN>~3.6V. Trezor is the textbook example of *when* a boost is right; ours misapplies it. Replace with a 4-sink/charge-pump WLED driver **or** switch to a series-string panel |
| Backlight supply node | Off VSYS (pre-regulator) | Off SYS_PWR_IN (pre-buck) | **MATCH** — both correctly keep the backlight off the 3.3V logic rail |
| Display VCC gating | **P-FET Q3 CSD25501F3** gates VDISPL (gate R25 47k, PWR_EN); C96/C97 4.7µF decoupling | TPS22917 (U14) gates DISPLAY_VCC_SW, but **zero decoupling** (power P12) and **no default-off pulldown** on enable (P10) | **MATCH (gate concept) / SHOULD-ADOPT** the decoupling + a default-off pulldown that Trezor's 47k gate provides implicitly |
| Touch pull-ups | I2C SCL/SDA with **2k2** pull-ups (R11/R41); TC_INT; DISPL_RESET R42 10k | TOUCH_I2C present but **no pull-ups at all** (power P11) | **SHOULD-ADOPT** pull-ups (bus is dead without them) |

---

## 7. Physical button / touch (Trezor p.15 TS7_Conn_UI rev D, p.5)

| Item | Trezor Safe 7 | Our board | Verdict |
|---|---|---|---|
| Power button | Single side button → **nPM1300 SHPHLD pin** (BTN_USER) using the **PMIC's internal pull-up**; on the UI FPC via **R27 100Ω series + C100 100nF** (ESD/debounce). Enables hardware power-on / ship-mode. A **TPS3420** supervisor + button logic (p.5) sequences reset | Single button **SW1 EVQP7J01P** → MCU GPIO; BQ24074 has no ship-mode/​button power path | **OK-to-differ**, but Trezor's **hardware power-on-from-button + ship mode** (via PMIC) and the 100Ω+100nF debounce are a nice UX/battery feature we lack. Consider a series R + cap on our button |
| Capacitive touch | Separate touch controller on the display FPC, I2C (TC_I2C) + TC_INT interrupt, 2k2 pull-ups | FT6336 on display FFC, TOUCH_I2C — missing pull-ups (see §6) | **MATCH (architecture) / SHOULD-ADOPT** pull-ups |
| Status LED | RGB (APHF1608LSEEQBDZGKC) on UI FPC, MCU-driven, per-color R28 300Ω(R)/R29 68Ω(B)/R30 680Ω(G) | RGB LED1 ASMB-MTB0 on main PCB, MCU sink; LED_G is on PC15 (no timer AF — mcu report §1.7) | **OK-to-differ** on placement; **SHOULD-FIX** our LED_G pinmux independently |

---

## 8. EMC / layout / security tricks (across sheets)

| Trick | Trezor Safe 7 (page) | Our board | Verdict |
|---|---|---|---|
| Hardware power-cycling of **every** secure/critical rail | **P-FET high-side switch (CSD25501F3, 47k gate) on TROPIC (Q4, p.11), OPTIGA (Q2, p.12) AND display (Q3, p.13)**; plus a switched **M3V3** domain (Q5 P-FET + Q1 CSD13380F3 NMOS driver, p.5) | TROPIC (U4), NFC (U13), Display (U14) via TPS22917 load switches; **OPTIGA is always-on** SYS_3V3 | **OK-to-differ.** We gate 3 islands with clean load-switch ICs; Trezor gates 3 with discrete P-FETs. Our **not** gating OPTIGA is acceptable (hibernate is a SW feature per its DS), but gating it would improve parity/security posture. Our load-switch parts are the tidier implementation |
| Disable SE test/scan at pins | TROPIC SCAN/TPM/F_TEST/TEST → GND (p.11) | pins 30/31→GND, 22→VCC (mcu §3) | **MATCH** |
| Hardware tamper input | **TAMP net → STM32 tamper pin** (p.2) | not wired | **SHOULD-CONSIDER** — cheap anti-tamper on a secure wallet |
| Voltage supervisor / controlled reset | **TPS3420** push-button/supervisor (p.5) | STM32 internal BOR only | **OK-to-differ / minor** |
| Default-off enables | 47k on every P-FET gate → islands default OFF | TROPIC ON has 47k pulldown ✓; **NFC_PWR_EN / TFT_PWR_EN float** (power P10) | **SHOULD-ADOPT** 100k pulldowns on the floating enables |
| Dual secure elements | TROPIC01 + OPTIGA Trust M, both gated; OPTIGA I2C 2k2 pull-ups, RST 47k pulldown (p.12) | TROPIC01 + OPTIGA Trust M; OPTIGA I2C 4.7k pull-ups, RST direct | **MATCH (architecture)** |
| USB shield AC/DC ground | 1M ∥ 4.7nF (p.4) | (not evident) | minor, could adopt |
| Guard rings / tamper mesh / internal shielding | **Not determinable** from the schematic PDFs or the assembly-view PDFs I have (no gerbers/copper layers were provided) | — | **Cannot verify from sources** — stated honestly rather than guessed |

---

## Where OUR design is actually cleaner than Trezor

1. **STM32 per-pin decoupling** — 9×100nF, every one ≤2.4mm pad-to-pad, VCAP 4.7µF @1.8mm
   (mcu report §1.2). Exemplary; Trezor's is fine but ours is textbook-tight.
2. **Power-gate implementation** — a single **TPS22917 load switch** per island (with QOD fast
   discharge + CT-programmed slew) is a cleaner, lower-part-count high-side gate than Trezor's
   discrete P-FET + separate NMOS gate-driver (their M3V3 domain uses *two* transistors + a
   supervisor for what we do with one IC).
3. **Simpler, PMIC-free power tree** — for our (smaller, USB-only, no-Qi) load budget, one buck +
   discrete charger avoids a firmware-configured PMIC and its failure modes (power report P14
   endorses this).
4. **Thinner antenna option** — a correctly-built on-PCB loop needs no Qi coil, no back-cover FPC
   assembly, and no 6-pin BTB — *if* the keepout/ferrite/tuning work is done. (Today it's unbuilt,
   so this is potential, not realized.)

## Top SHOULD-ADOPT items (ranked)

1. **Fix the backlight topology (§6, critical).** Trezor's TPS61062-boost-into-series-string is the
   correct use of a boost; our TPS61165-boost-into-4-parallel-cathodes cannot regulate or switch off.
   Replace the driver (4-sink/charge-pump) or move to a series-LED panel.
2. **Add the 47k TROPIC MISO/SDO pull-up (§1)** to the switched rail — DS Fig 24 / TS1702 reference;
   libtropic depends on a clean 0xFF idle.
3. **Build the full NFC front-end (§3)** — adopt Trezor's matching topology + 270nH/680pF EMC filter +
   2Ω damping + full DS decoupling; pin the crystal CL and set 2×10pF loads; **strongly consider the
   FPC-on-back-cover antenna** to escape the plane/battery/display detuning trap.
4. **Add a VBUS TVS (§5)** — 2× TPD1E10B06-class, mirroring Trezor's discrete VBUS clamp.
5. **Add the 4.7µF TROPIC bulk (§1), 100nF on NRST (§2), I2C pull-ups (§6), default-off enable
   pulldowns (§8), and the missing charger/rail caps (§4)** — all low-cost, all mirror Trezor practice.
6. **Independent-of-Trezor bugs to fix anyway:** charge current 788mA→0.5-1C (§4), incoherent USB
   current-limit chain (§5), C6 slew 1nF→470pF for the 1ms TROPIC ramp (§1), HSE cap/MPN placeholders
   and LED_G pinmux (§2/§7).

**Consider (security parity):** a hardware TAMP input to the STM32 (§8), a 32.768kHz LSE for tamper
timestamps (§2), and battery NTC sensing (§4) — all present on Trezor, absent on ours.
