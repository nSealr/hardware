# Subsystem 5 — ST25R3916B NFC/RFID (QFN32) design

Date: 2026-06-10
Status: design captured, verified from ST25R3916B datasheet DS13541 Rev 11
(Figure 2, differential antenna driving) + AN5276. Clean rebuild. The RF
front-end detail is in `nfc-rf-frontend.md`.

## Digital interface (to STM32 SPI2)

| ST25R3916 pin | Net | MCU |
| --- | --- | --- |
| BSS (SPI SS) | `NFC_SPI_CSN` | PB12 |
| SCLK | `NFC_SPI_SCK` | PB13 |
| MISO | `NFC_SPI_MISO` | PB14 |
| MOSI | `NFC_SPI_MOSI` | PB15 |
| IRQ | `NFC_IRQ` | PD0 (EXTI) |
| I2C_EN | `GND` | — (tie GND to select **SPI** mode) |
| MCU_CLK | no-connect | optional clock output, unused |

## Clock

- **XTI / XTO**: crystal `X3` (e.g. 27.12 MHz per the ST reference) with two load
  caps + the series feedback per datasheet.

## Supplies (Figure 2) and power-gating

- `VDD_IO` → `+3V3` (digital IO, 1.65-5.5 V).
- `VDD`, `VDD_TX` (2.4-5.5 V), `VDD_A`, `VDD_D`, `VDD_RF`, `VDD_DR` → the
  NFC supply, each with local decoupling; `VDD_AM` with **2.2 µF** (regulator AM)
  / **22 nF** (AWS AM) per the datasheet.
- The whole NFC supply is **power-gated** by `NFC_PWR_EN` (MCU PB1) via a load
  switch → `NFC_VCC_SW`, so the reader is off unless used.
- Grounds: `GND_A`, `GND_D`, `VSS`, `AGD`, `GND_DR1`, `GND_DR2`, EP → `GND`.

## RF front-end (differential) — see nfc-rf-frontend.md

`RFO1/RFO2` → EMC filter (`L30/L31` + `C30/C31`) → matching (`Cs/Cp`) →
back-side antenna loop → `RFI1/RFI2` capacitive divider. `AAT_A/AAT_B` support
automatic antenna tuning; `EXT_LM`, `TAD1/TAD2` per datasheet. Matching values
and loop geometry are first-article **tuning gates**.

> Open item now resolved: the RF pins are named `RFO1/RFO2/RFI1/RFI2` (not DNC) —
> the project ST25R3916 symbol must expose them; their exact QFN32 pin numbers
> come from the DS13541 pin-function table at binding time.

## ERC gate

All digital + supply + ground pins bound; I2C_EN→GND; crystal + caps; the RF
front-end nets bound (values flagged tuning); ERC clean before subsystem 7.
