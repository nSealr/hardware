# Placement — the definitive floorplan (digital-prototype spec)

Board **42.72 × 36.8 mm**, frame x[10.64, 53.36] y[34.0, 70.8], **+y = down**, R2.5
corners, MH1–4 in the fillets. F.Cu = component side; B.Cu = display side (only J2).
This is the per-component position/rotation/grouping the KiCad placement executes.
Targets are exact; expect ±0.3 mm nudges from the DRC/render loop. Utilization ≈ **79 %**
(FPC antenna → no on-board loop/keepout) — **feasible on a single F.Cu side**.

## Principles (why each part sits where it does)
1. Decoupling cap **touches its IC power pin**, pads pointing at the pin (min. loop).
2. Crystal **against its oscillator pins**, load caps flanking, guard GND, nothing under it.
3. Buck: Cin→VIN, L→SW, Cout→VOS, tight loop.
4. Secure SPI (MCU↔TROPIC) **adjacent**; QSPI flash near the MCU QSPI pins; USB D± short + ESD inline.
5. RF (NFC): matching **compact at U9's RFO/RFI**, differential feed **< 8 mm** and symmetric to J-ANT; 4-layer copper keepout under the feed.
6. Power spine USB→limiter→charger→buck in a physical column.
7. Rotate each IC so its **most-connected side faces** what it talks to.
8. Mechanical anchors fixed first; everything places around them.

## 1. Fixed anchors (mechanical — placed first)
| Ref | Pos (x,y) | Rot | Note |
|---|---|---|---|
| J1 USB-C (USB4105) | 32.0, 66.2 | 0 | bottom-center, mouth out the bottom edge; shield posts on-board |
| J2 display FFC (**B.Cu**) | 32.0, ~44 | 180 | back side, mouth-face y≈48 toward the bottom edge (fold reach); FH12A top-contact |
| SW1 side button | 52.0, 55.0 | 90 | right edge, actuator overhangs ~0.3 mm |
| MH1–4 | 13.1/50.9 × 36.6/68.4 | — | corner fillets, M2 |
| **J6** expansion (JST-SH) | 15.5, 37.3 | 90 | top-left, opening up/out |
| **J-ANT** NFC feed (1.0 mm FFC) | 33.0, 35.6 | 0 | **top-center**, next to J6/J9; differential feed down to U9 |
| **J9** battery (**JST-SH** SM02B-SRSS-TB) | 47.0, 37.5 | 90 | top-right, low-profile ~2.9 mm; clears MH4; 32 mm cell span to the left |

## 2. NFC cluster — TOP-CENTER-RIGHT, hugging J-ANT (moved up so the feed is short)
| Ref | Pos | Rot | Why |
|---|---|---|---|
| U9 ST25R3916B | 40.5, 42.0 | 0 | just below J-ANT, clear of U1's right edge (x36.75); RFO/RFI face up to the feed |
| L30/L31 EMC (270 nH) | 37.0/39.0, 39.0 | 0 | in the feed, between J-ANT and U9 RFO |
| C30/C31 EMC (680 pF) | 37.0/39.0, 40.2 | 0 | with L30/L31 |
| C32/C33 Cs (150 pF) | 41.5/43.0, 39.5 | 0 | series match at RFO |
| Cp/Cr/Cd/Rd (new) | ring x38–45, y40–45 | — | parallel-match + RX divider + damping at the antenna node |
| X3 27.12 MHz | 44.0, 44.5 | 90 | ≤3 mm from U9 XTO/XTI, on the side away from RFI, out of the feed |
| C34/C35 xtal load (10 pF) | 43.0/45.0, 44.5 | 0 | flank X3 |
| C36–C40 reg caps (2.2 µF∥10 nF) | ring U9 ≤1.5 mm | — | internal-LDO bypass at their pins |
| NFC_VCC 10+1+0.1 µF + RJ2 | 43–46, 46 | — | switched-rail bulk at U9 |
| EP via-farm (3×3) | under U9 | — | thermal + RF return to In1 GND |

## 3. Center + left column (host + secure)
| Ref | Pos | Rot | Why |
|---|---|---|---|
| U1 STM32U585 | 28.0, 51.5 | 0 | center; top y≈42.75 clears the NFC/top strip; bottom y≈60.25 above USB |
| C50–C59 (decoupling ring + VCAP) | 1.9–3.5 mm around U1 | — | **keep the good ring intact**, move rigidly with U1 |
| X1 HSE 16 MHz | 17.5, 51.0 | 0 | against U1 left edge (PH0/PH1); C18/C19 8 pF flanking at 16.0/19.0, 51.0 |
| U11 OPTIGA | 15.0, 46.0 | 0 | left, above U5; +100 nF at pin 10 |
| U5 W25Q128 QSPI | 15.7, 64.0 | 0 | bottom-left, near U1 OCTOSPI pins; +100 nF at pin 8 |
| LED1 RGB + RLED1–3 | 13.3, 58.5 | 0 | left edge, top-emitting; resistors clustered |
| new: NRST 100 nF (18.5,49.5), VDDA/VREF 1 µF, VDD 10 µF | at U1 pins | — | see connectivity.md |

## 4. Right column (power spine) + bottom band (USB + TROPIC)
| Ref | Pos | Rot | Why |
|---|---|---|---|
| U10 BQ24074 charger | 49.0, 45.5 | 0 | right, below MH4/J9; +IN 4.7/OUT 10/BAT 4.7 µF at pins; R9-R13 clustered |
| U3 TPS62840 buck + L1 | 47.5/49.5, 51.0 | 0 | Cin→VIN, L1→SW, **10 µF Cout at VOS** |
| U15 WLED driver (TBD, low-Vin) | 49.0, 57.0 | 0 | backlight; reselect part (README C3) |
| U13/U14 load switches | 45/48, 60 | 0 | near NFC/display rails; +100 k pulldowns on ON |
| U2 TROPIC01 | 23.3, 64.0 | -90 | bottom-left, **SPI 4.6 mm to U1** (keep); 3×100 nF one-per-face + 2.2 µF bulk; 47 k on **MISO** |
| U4 TROPIC load-switch | 14.0, 62.0 | 0 | in the TROPIC_VCC feed |
| U7 USB ESD | 33.5, 62.5 | 0 | **inline** on D± between J1 and U1 (flow-through) |
| U8 VBUS limiter | 45.5, 66.5 | 0 | near J1 VBUS; C_VBUS 10 µF + TVS at J1 |
| R1/R2 CC, R3/R4 series | around J1/U7 | — | tight to the connector |

## 5. Debug group (grouped per constraint) — top-center-left
J7 TC2030 (27.0, 40.5, 0) = SWD; JP1 BOOT0 (30.5, 39.5); TP_UART_TX/RX/GND clustered
at (24–26, 40–42). All within one ~7×4 mm block. (SWD-only debug surface; no redundant SWD test pads.)

## 6. Feasibility
Center column = U1 (17.5 mm) between the top strip (y≈37–42) and the USB band (y≈60+).
Side columns + top/bottom bands hold everything else. F.Cu courtyard ≈ 79 % of the 1572 mm²
board (no antenna keepout, FPC) → routable single-side. B.Cu carries only J2.

*(This definitive plan supersedes the earlier "re-floorplan review" analysis, which is in
git history. The exact placed board is produced by executing this in KiCad with render/DRC
verification — the final ±0.3 mm nudges and the last-10% tidy are interactive.)*
