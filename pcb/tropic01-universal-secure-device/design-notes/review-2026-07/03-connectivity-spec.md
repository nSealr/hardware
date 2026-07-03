# Connectivity Spec — the net-by-net wiring delta for the rebuild

Date: 2026-07-03. Consolidates every **added or changed net connection** the
review requires into one schematic-capture reference, so wiring the schematic in
KiCad is mechanical. Source: the `review-2026-07/` area reports (cited per block).
Existing correct connectivity (SPI buses, power tree spine, pinmux) is unchanged —
see `production/netlist-contract.json` + the MCU report §1.7 for the verified map.

Notation: `PART.pin → NET`. New parts use the refs from `01-part-selections.md`.

---

## 1. Decoupling / bulk caps (all: one pad → the rail, other pad → GND)
Place at the pin (coordinates in `placement-refloorplan.md §3e`).

| Cap | Rail net | At |
|---|---|---|
| C_NRST 100 nF | NRST | U1 pin14 |
| C_VDDA 1 µF, C_VREF 1 µF | SYS_3V3 (via ferrite for VDDA opt.) | U1 pin22 / pin21 |
| C_VDDbulk 10 µF | SYS_3V3 | U1 bottom row |
| C_VBATsense 100 nF | VBAT_SENSE | U1 pin15 (ADC reservoir) |
| C_TROPICbulk 2.2–4.7 µF | TROPIC_VCC | U2 |
| C_U10_IN 4.7 µF | VBUS_LIMITED | U10 pin13 |
| C_U10_OUT 10 µF | SYS_PWR_IN | U10 pin10/11 |
| C_U10_BAT 4.7 µF | VBAT | U10 pin2/3 (and J9.1) |
| C_U3_VIN 4.7 µF | SYS_PWR_IN | U3 VIN |
| C_U3_VOUT 10 µF | SYS_3V3 | U3 VOS/L1.2 |
| C_U5 100 nF | SYS_3V3 | U5 pin8 |
| C_U11 100 nF | SYS_3V3 | U11 pin10 |
| C_U14o 2.2 µF + 100 nF | DISPLAY_VCC_SW | U14 VOUT |
| C_J2v 1 µF | DISPLAY_VCC_SW | near J2 VCI |
| C_VBUS 10 µF (move C1) | VBUS | at J1 VBUS pads |

## 2. Pull-ups / pull-downs / straps (report: mcu §3, power §P10/P11, nfc §5)
| R | Connection |
|---|---|
| R_CSN 47 k | TROPIC_SPI_CSN → **TROPIC_VCC** (switched rail, not SYS_3V3) |
| R_NFCen 100 k | NFC_PWR_EN → GND (TPS22917 U13 ON default-off) |
| R_TFTen 100 k | TFT_PWR_EN → GND (TPS22917 U14 ON default-off) |
| R_I2C 4.7 k ×2 | TOUCH_I2C_SCL → SYS_3V3, TOUCH_I2C_SDA → SYS_3V3 |
| **strap** | ST25R3916B **VDD_DR (U9 pin14) → VDD_RF net (pin9)** (regulator mode); remove pin14↔raw NFC_VCC |

## 3. Charger reprogramming (power §P2/P3, for the 250 mAh LP502030)
| R | Value | Sets |
|---|---|---|
| R10 (ISET) | **3.57 kΩ** | ICHG ≈ 250 mA (1C) |
| R12 (ITERM) | **2.94 kΩ** | ITERM ≈ 25 mA |
| R9 (ILIM) | **3.24 kΩ** | IINmax ≈ 497 mA (USB-compliant) |
| R11 (TMR) | 46.4 kΩ (keep) | 6.2 h timer |
| C6 (TROPIC CT) | **470 pF** (was 1 nF) | ramp ≤1 ms |

## 4. Backlight driver (AL8860 buck, replaces TPS61165 boost — power §P1, parts §B)
`U15 = AL8860WT-7 (SOT26)`, reuses L15/D15/R15 as the buck's L/diode/sense:
- `U15.VIN → SYS_PWR_IN` ; `U15.GND → GND`
- `U15.SW → L15 → TFT_BACKLIGHT_A (LEDA, J2)` ; freewheel `D15` cathode→SW node, anode→GND
- LED return: `LEDK1-4 (J2) tied → ISET/CSN sense node → R15 (1.25 Ω) → GND` (I ≈ 100 mV/R15 ≈ 80 mA)
- `U15.CTRL/PWM → TFT_BACKLIGHT_PWM (PA8)` ; `U15.EN → SYS_3V3` (or a GPIO)
- Cout at LEDA node per AL8860 DS.

## 5. NFC RF front-end (nfc §1/§3 — differential, ST25R3916B U9). All `TUNE`.
```
RFO1(13) ─ L30(270nH) ─┬─ C32(180pF) ─┬─ Rd1(0Ω) ─● NFC_ANT1 ──┐
                      C30(680pF)      Cp (2×120pF                │ → J-ANT → FPC loop
                       │              diff)        ┌─────────────┘
                      GND              │           │
RFO2(15) ─ L31(270nH) ─┴─ C33(180pF) ─┴─ Rd2(0Ω) ─● NFC_ANT2 ──┘
RX: NFC_ANT1 ─ Cr1(180pF) ─● RFI1(22) ─ Cd1(680pF) ─ GND
    NFC_ANT2 ─ Cr2(180pF) ─● RFI2(23) ─ Cd2(680pF) ─ GND
```
Reg-cap nets (each ∥ pair at its pin): VDD_A(7)=2.2µF∥10nF, VDD_D(3)=2.2µF∥10nF,
VDD_RF(9)+VDD_DR(14)=2.2µF∥10nF, VDD_AM(11)=2.2µF, AGDC(24)=1µF∥10nF; NFC_VCC bulk
10µF+1µF+100nF at VDD(8)/VDD_TX(10)/VDD_IO(1). X3 27.12 MHz: XTO(4)/XTI(5) with
C34/C35 10 pF each. EP(33)+VSS(21) → GND with a 3×3 via farm.
**Symbol must expose all 33 pins** (DS13541 Table 2) — the current symbol has 15.
J-ANT = 2-pin feed (BTB/solder pads) carrying NFC_ANT1/NFC_ANT2 to the FPC.

## 6. Display connector J2 (mechanical §2 — do in the footprint editor)
Swap to **FH12A-50S-0.5SH(55)** (top-contact). Net map by *physical* position:
the folded tail's **pin 1 (LEDA) lands at low board-x**. Map display pins →
the pad at each physical x (see mechanical report §1.3 pin table): 1=LEDA(=TFT_BACKLIGHT_A),
2-5=LEDK1-4, 10=RESET(TFT_RST), 33=SDO(TFT_SPI_MISO), 34=SDI(TFT_SPI_MOSI),
36=D/CX(TFT_DC), 37=SCL(TFT_SPI_SCK), 38=CSX(TFT_CS), 40/41=VDDI/42=VCI(DISPLAY_VCC_SW),
43/48-50=GND, 44=SCL/45=SDA/46=INT/47=RST (touch). **Verify pin-1 against the
physical tail mark at first article.** (Do NOT also reverse nets on a corrected
footprint — that double-mirrors.)

## 7. Test points (mcu §6 — greens the repo validator)
`TP_SWDIO→SWDIO, TP_SWCLK→SWCLK, TP_NRST→NRST, TP_3V3→SYS_3V3, TP_GND→GND,
TP_BOOT0→BOOT0` (the JP1/R22/PH3 net). Grouped near J7 (coords in mcu §6 / placement §3a).
Optional: PB3(TRACESWO, U1 pin89) → J7 pin6 for ITM.

## 8. Protection / misc
- VBUS TVS (TPD1E10B06 / SMF5.0A) → VBUS, GND, at J1.
- J6 Qwiic: add 100–200 mA polyfuse in the SYS_3V3 feed to J6.
- USB series R3/R4 → 0 Ω (AN4879); ESD U7 inline on D± (placement §3d).
- LED_G: move off PC15 → **PE9 (TIM1_CH1)** for HW PWM (mcu §1.7); record I2C
  instance split SE2=I2C4 / TOUCH=I2C1 in `pinmux-ledger.json`.

---
Verification: after capture, ERC must show every power pin driven, every net ≥2
endpoints, no floating enables. Then netlist → the layout per `placement-refloorplan.md`.
