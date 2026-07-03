# Floorplan / Placement Review + Concrete Re-Floorplan for the 36.8 mm Shrink

Board: `pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_pcb`
Data: `design-notes/review-2026-07/board-truth.json` (103 fps, 926 tracks, 129 vias). Renders read (top/bottom).
Frame: KiCad, **+y = down**. Current outline x[10.64, 53.36] (W = 42.72), y[31.0, 70.8] (H = 39.80), center (32.0, 50.9). F.Cu = component side; B.Cu carries only J2 (display FFC) + DISP1 envelope (off-board placeholder at 110,125).

All coordinates below are **mm in board frame**. Where I give a "NEW frame" position it assumes the shrink is taken **off the top edge** (USB J1 stays at the bottom): **new top edge y = 34.0**, new height 36.8, MH3/MH4 fillet centers → y ≈ 36.6. Center of the new board is (32.0, 52.4).

---

## 0. Executive verdict (read this first)

1. **The macro-zoning is defensible, the micro-placement is not.** The coarse plan — U1 left-of-center, NFC+power in the right column, secure island + USB along the bottom, OPTIGA/QSPI/HSE in the left column, antenna top — is sound and matches `placement.md`. What looks "random" is the **support-passive and RF placement**: decoupling and matching parts are scattered 8–18 mm from their ICs, load caps sit in the wrong ICs' decoupling rows, and the RF matching network is smeared across the whole board including *inside the antenna envelope*. That is the real defect, and it is systemic (the schematic is a stub — passives were auto-dropped with no proximity constraint; see `AUDIT-findings.md`).

2. **The 36.8 mm shrink is NOT feasible as a single-side F.Cu placement if the 13.56 MHz loop stays on-board.** With the antenna keepout (≈271 mm² of F.Cu blocked at top) **and** the ~40 decoupling/matching parts the electrical reviews require added, single-side courtyard density hits **~94 %** — unroutable in practice on 4 layers. The clean fix is to **move the NFC loop to a back-cover FPC** (small BTB/2-pad feed stays on the main board): that removes the keepout and drops density to **~78 %** — comfortably feasible. Keeping the loop on-board forces spilling passives to B.Cu (conflicts with the "B.Cu = J2 only" rule and the tight display gap) or abandoning the height gain.

3. **Two parts are the hard casualties of the top keepout: the battery connector J9 (9.25 × 10.25 mm) and the grouped debug cluster (J7 + 6 TPs).** Neither fits in the top strip once the antenna claims it, and the center column is fully consumed by U1 (17.5 mm) between the keepout and the USB. Both must relocate to side/bottom real estate (J9 accepts longer pigtail leads; the TPs can go to B.Cu pogo pads per the original `placement.md` intent).

---

## 1. Cluster analysis (per major IC): are the support passives adjacent + oriented right?

Distances are center-to-center from `board-truth.json` (the electrical reviews quote pad-to-pad, ~0.5–2 mm tighter; both agree on the verdict). "Row" = the visible horizontal band of parts in the render.

### U1 — STM32U585 LQFP100 @ (28,50)  — decoupling GOOD, clocks/reset BROKEN
- **VDD/VDDA/VREF/VBAT 100 nF (C50–C58) + VCAP 4.7 µF (C59): correctly clustered, 1.9–3.5 mm, one per pin.** This is the one well-placed cluster on the board (render: neat ring of 0402s hugging the LQFP). No change.
- **HSE X1 @ (14,54) is a scatter failure.** C18 load cap 6.5 mm from X1, **C19 load cap 13.7 mm away** — C19 physically sits in U1's *bottom decoupling row* at (26.5,59.5), between C54 and R3. A crystal load cap on the far side of the MCU is unambiguous evidence of unconstrained auto-placement. X1 itself is 14.6 mm (center) from U1; PH0/PH1 (pins 12/13) are on U1's left edge ~ (20.3, 49.5). **Move X1 to ~(17.5, 51) hard against U1's left edge; C18/C19 flanking the crystal within 1.5 mm, tight GND loop, no traces under it.**
- **NRST: no cap at all** (DS Fig 38 wants 100 nF at the pin). Add.
- Orientation of the 0402 ring is fine (mixed 0°/90° following the pin edges). No rotation issues.

### U2 — TROPIC01 QFN32 @ (23.34,64) rot −90  — count OK, distribution one-sided
- 3×100 nF present (C3/C4/C5) = DS Fig 24 count, all **3.6–5.0 mm and all clustered on the south side** while the rot −90 QFN has VCC pins on three faces. Redistribute one-per-VCC-face.
- Power gate U4 (TPS22917) 10.8 mm away, RJ1 0 Ω sense jumper 5.6 mm — acceptable, but no bulk cap on TROPIC_VCC. Add 2.2–4.7 µF.
- **Positive:** U2↔U1 SPI1 is 14.75 mm center / ~4.6 mm pad-to-pad — excellent adjacency for the secure bus. Keep U2 where it is (left of USB, next to U1's bottom-left).

### U9 — ST25R3916B NFC QFN32 @ (40.17,48)  — WORST cluster on the board
- The single NFC_VCC cap **C41 is 12.4 mm away** at (50,40.5), over by U10/U3. Regulator caps C36/C37/C38/C39/C40 sit **8.8–12.2 mm** from the QFN (they are internal-LDO stability caps — must be *at the pins*).
- **RF matching network is smeared across the entire board:** L30 8.5, L31 9.6, C30 10.0, C32 13.6, and **C31 (18.0 mm) and C33 (16.2 mm) are literally inside the antenna envelope** at (32,32)/(32,34). A 13.56 MHz L-match must be a compact chain hugging U9's RFO/RFI pins with the feed running straight to the loop; this is the opposite.
- **X3 27.12 MHz @ (45.5,53) is 7.3 mm from U9 with the QFN body between it and XTO/XTI**, and its load cap **C34 is 16.1 mm** from the crystal (C35 is fine at 3.2 mm). Wrong on two counts.
- This whole quadrant must be rebuilt as a tight RF cluster (Section 3).

### U3 — TPS62840 buck @ (48.44,49)  — output cap absent at the converter
- L1 (2.2 µH) is 3.4 mm — OK. VIN cap C14 is 10.1 mm. **Output bulk C2 (4.7 µF) is 37.6 mm away** (top-left corner) and L1→C2 is 34.3 mm. The DS demands ≥10 µF directly at VOS/L1. Today there is nothing >100 nF within 10 mm of the inductor. Add 10 µF at VOS; keep C2 as remote bulk.

### U10 — BQ24074 charger @ (48,45.12)  — programming resistors OK-adjacent, power caps missing
- R9–R13 program resistors are 3.5–3.9 mm — reasonable. **No IN, OUT, or BAT bulk caps exist on the whole charger** (DS wants 1–10 µF IN, 4.7–47 µF OUT and BAT). C14 1 µF at 6.4 mm is the only nearby bulk and it is shared with the buck VIN. Add IN/OUT/BAT caps at the pins.

### U5 — W25Q128 QSPI SOIC-8 @ (15.73,63.56)  — no local decoupling
- Nearest cap is C17 2.2 µF at 3.9 mm (already double-booked as VDDA-area bulk); no dedicated 100 nF at VCC pin 8. Add one within ~1.5 mm. QSPI bus to U1 is ~12 mm — fine for 48–80 MHz SDR.

### U11 — OPTIGA Trust M USON-10 @ (14.5,43)  — no local decoupling
- I2C pull-ups R6/R7 are 3.5/4.3 mm — good. **No cap within 5 mm of VCC pin 10** (nearest is U1's C58 at 7.4 mm). Add 100 nF at the pin.

### U15 — TPS61165 backlight boost @ (49.245,59)  — passives near, topology wrong
- L15 4.5, D15 8.9, C13 2.5, R15 2.5 mm — physically this cluster is *fine*. The problem is electrical (P1 in the power review: a boost cannot regulate a 3.2 V parallel-LED panel below a 4.4 V input). Whatever driver replaces it, keep the same local cluster discipline. C15 (output 1 µF) at 11.2 mm should come in to the driver.

**Cluster scorecard:** U1-decoupling OK · U1-clocks/reset BROKEN · U2 partial (one-sided) · U9 BROKEN x2 (matching + Xtal + supply all scattered) · U3 BROKEN (Cout 37.6 mm) · U10 BROKEN (no power caps) · U5 BROKEN (no cap) · U11 BROKEN (no cap) · U15 OK physically.

---

## 2. Signal-flow critique

- **USB chain:** J1 (32,66.2) → **U7 ESD is 9.3 mm to the *right*** of the connector's D+/D− pads (41,68.5), using only pins 1/2 of the USON-10 → each ESD tie is a stub, not flow-through, and the direct 15.7 mm J1→U1 path is forced to ≈39 mm. Functionally OK at FS, but move U7 **inline** at ~(33.5,63) so D+/D− pass its pins on the way to R3/R4 → U1 PA11/PA12. VBUS bulk C1 is 31 mm from J1 and there is no VBUS TVS (power review P9). Series R3/R4 22 Ω can drop to 0 Ω (AN4879).
- **Power flow:** J1→U8 limiter (44.5,64)→U10 charger (48,45)→U3 buck (48.44,49)→SYS_3V3. The topology walks bottom-right → mid-right → out to the rail, which is a reasonable right-column spine. But the **buck output cap is 37.6 mm from the buck** (breaks the DCS-Control loop), the charger has **no IN/OUT/BAT caps**, and SYS_PWR_IN has a single 1 µF doing input duty for charger + buck + backlight. The *routing* order is fine; the *decoupling* is the failure.
- **NFC feed path (U9 → matching → antenna):** currently incoherent — matching parts orbit U9 at 8–18 mm and two of them sit under the antenna. There is **no clean U9→match→loop line**. Re-floorplan must create one: U9 just below the top keepout, matching chain stacked between U9's RFO/RFI pins and the loop's bottom-edge feed exit, X3 island on the *opposite* face of U9 from the RF pins.
- **Secure SPI adjacency:** U1↔U2 (TROPIC SPI1) 4.6 mm pad-to-pad — the one genuinely good signal placement; preserve it. OPTIGA is on I2C4 (slow) — proximity non-critical. QSPI U5↔U1 ~12 mm — fine.
- **QSPI:** acceptable length; just add the missing VCC cap and match CLK/IO lengths at route time.

---

## 3. Concrete re-floorplan (NEW frame, top edge y = 34.0)

Legend: **MUST** = correctness or hard constraint · **SHOULD** = quality/SI/manufacturing · **COULD** = optimization.
"→" gives proposed (x, y[, rot]). Positions are targets; run DRC and expect ±0.3 mm nudges.

### 3a. Antenna, mounting holes, and the top-strip evacuees

| Ref | Current (x,y,rot) | Proposed (x,y,rot) | Class | Reason |
|---|---|---|---|---|
| ANT1 loop | 32.0, 33.0, 0 | **32.0, 37.6, 0** (outer 33.6×6.0, x15.2–48.8, y34.6–40.6) | MUST | Occupies cleared top-center strip; 4-layer no-copper keepout under loop +1 mm (y≈33.6–41.6). |
| MH3 | 13.1, 33.6 | **13.1, 36.6** | MUST | New top-left fillet center after shrink. |
| MH4 | 50.9, 33.6 | **50.9, 36.6** | MUST | New top-right fillet center. |
| MH1 / MH2 | 13.1/50.9, 68.4 | unchanged | — | Bottom fillets fixed. |
| J9 battery (9.25×10.25) | 44.0, 37.5, 180 | **see note ▼** | MUST | In the keepout; must leave the top strip. Too large (10.25 mm tall) to hide in the 7.6 mm sliver or the 4.5 mm corners outside the loop x-span. |
| J6 Qwiic (7.85×6.61) | 19.0, 36.5, 180 | **14.8, 55.5, 90** (left edge, opening out) | MUST | Evacuate keepout; expansion connector wants an edge; left-mid edge is the least-congested edge slot. |
| J7 TC2030 (7.05×4.05) | 28.0, 38.5, 0 | **see debug note ▼** | MUST | In keepout; anchor of the debug group. |
| JP1 BOOT0 | 33.5, 39.5, 0 | **with debug group** | MUST | Move with J7 (it is a debug feature). |
| TP_UART_GND | 25.0, 35.0, 0 | **with debug group** | MUST | In keepout + splits the UART triplet (21.4 mm from TX/RX today). |

**▼ J9 battery — relocation decision (pick one):**
- **A (recommended, ties to feasibility):** put the **NFC loop on a back-cover FPC** (Section 4 escape valve). The top strip is then free of keepout and J9 returns to the top edge at **(44.0, 42.0, 180)** — essentially "the old J9, moved south 3 mm" as the mechanical note anticipated. Cleanest lead dress to the coplanar battery.
- **B (on-board loop kept):** J9 → **(49.0, 47.0, 90)** on the right edge just below MH4, opening facing the top edge; this shoves U10/U3 ~4 mm south (Section 3c). Longer pigtail up the right edge to the battery — electrically fine for a DC cell.

**▼ Debug group (grouped per constraint) — two placements:**
- If FPC antenna (A): keep the group in the **top-center strip** below the new edge — **J7 (28.0, 42.5, 0)**, testpoint bank as in `mcu-secure-elements.md` §6 shifted +3 mm in y: TP_SWDIO (26.5, 44.5), TP_SWCLK (28.0, 44.5), TP_NRST (29.5, 44.5); TP_3V3 (23.0, 40.7), TP_GND (23.0, 42.3), TP_BOOT0 (23.0, 43.9); TP_UART_TX (24.6, 42.3), TP_UART_RX (24.6, 43.9), TP_UART_GND (25.0, 41.0). All grouped within a ~7×5 mm block. JP1 → (31.5, 43.5).
- If on-board loop (B): the top-center is keepout and U1's top edge is at y≈42.2, so there is **no room** for J7 there. Move the debug group to **B.Cu pogo pads** at the bottom-back per `placement.md` ("hidden pogo/test pads on the back") — J7 stays F.Cu at **(16.0, 46.5, 0)** in the left column, the 6 required TPs + UART TPs become 1.0 mm pogo lands on B.Cu clustered at ~(24–30, 60–66) where B.Cu is clear of the display module. This is the honest answer when the loop eats the top.

### 3b. Center + left column (secure/host)

| Ref | Current | Proposed | Class | Reason |
|---|---|---|---|---|
| U1 STM32 | 28.0, 50.0 | **28.0, 51.0** | SHOULD | Drop 1 mm so U1 top (→ y42.25) clears the antenna keepout (41.6) with margin; bottom → 59.75, still ≥0.6 mm above J1. |
| C50–C59 (U1 decoupling) | ring @ 1.9–3.5 mm | **track U1 +1 mm in y** | SHOULD | Keep the good ring intact; move as a rigid group with U1. |
| X1 HSE | 14.0, 54.0 | **17.5, 51.0, 0** | MUST | To U1 left edge at PH0/PH1 (pins 12/13 ≈ (20.3,50)); kills the 6.5/13.7 mm load-cap loops. |
| C18 HSE load | 14.0, 47.5 | **16.0, 51.0** | MUST | Flank X1 within 1.5 mm, tight GND. |
| C19 HSE load | 26.5, 59.5 | **19.0, 51.0** | MUST | Was stranded in U1's bottom row 13.7 mm away. |
| U11 OPTIGA | 14.5, 43.0 | **15.0, 46.5** | MUST | Below keepout, left of U1 top; frees the y<41.6 band. |
| (new) C_OPTIGA 100 nF | — | **16.8, 46.5** | MUST | Local VCC decoupling (review §4). |
| U5 QSPI | 15.73, 63.56 | **15.7, 64.5** | SHOULD | Stay bottom-left near U1 QSPI pins; nudge to clear J6/X1 repack. |
| (new) C_QSPI 100 nF | — | **19.5, 63.5** | MUST | Local VCC (pin 8) decoupling. |
| LED1 RGB | 13.7, 50.0 | **13.5, 58.5** | SHOULD | Push down the left edge to make the OPTIGA/HSE/J6 stack fit; still edge-visible. |
| RLED1/2/3 | 15–18, 44–47.5 | **cluster @ 13–15, 56–60** | SHOULD | Follow LED1. |

### 3c. Right column (NFC + power)

| Ref | Current | Proposed | Class | Reason |
|---|---|---|---|---|
| U9 NFC | 40.17, 48.0 | **44.5, 45.5** | MUST | Just below keepout, near the loop feed; RFO pins face up to the loop, RFI/SPI face U1. |
| L30/L31 (EMC L) | 40/45.5, 56–56.5 | **41.5/43.0, 42.5** | MUST | Series in the feed between loop exit and U9 RFO — top of the U9 cluster. |
| C30/C31 (EMC C, =C0a/b) | 40/32, 58/32 | **41.5/43.0, 43.5** | MUST | C31 was *inside the antenna*; pull the whole EMC/match chain to U9. |
| C32/C33 (Cs series) | 51.5/32, 55.5/34 | **45.5/47.0, 43.5** | MUST | C33 was inside the antenna; series match at RFO. |
| (new) Cp, Cr1/2, Cd1/2, Rd1/2 | — | **ring U9 within 2 mm** | MUST | Missing match/RX/damping parts (nfc review §3). |
| X3 27.12 MHz | 45.5, 53.0, 90 | **41.0, 48.5, 90** | MUST | ≤3 mm from XTO/XTI (pins 4/5), on the U9 face *away* from RFI; out of the antenna band. |
| C34/C35 Xtal load | 50/48.5, 37.5/54 | **40.0/42.0, 48.5** | MUST | C34 was 16 mm from X3; flank the crystal ≤2 mm. |
| C36–C40 NFC reg caps | 35.5–50, 36–43.5 | **ring U9 ≤1.5 mm** | MUST | Internal-LDO stability caps must sit at their pins. |
| C41 + new 10 µF/1 µF | 50.0, 40.5 | **NFC_VCC bulk @ 43–46, 47** | MUST | Only NFC_VCC cap is 12.4 mm away; add 10 µF+1 µF+100 nF at U9. |
| RJ2 0 Ω | 40.5, 44.0 | **46.5, 47.0** | SHOULD | Keep in the NFC_VCC feed at U9. |
| U10 charger | 48.0, 45.12 | **49.0, 51.5** (or 55.5 if J9-B) | MUST | Vacate the y<41.6 band and the U9 area; power sub-column below NFC. |
| R9–R13 | 44.5–51.5, 43.5–48 | **cluster @ 47–52, 50–53** | SHOULD | Follow U10. |
| (new) C_U10 IN/OUT/BAT | — | **at U10 pins 13/10-11/2-3** | MUST | Charger has zero bulk caps today. |
| U3 buck | 48.44, 49.0 | **43.5, 54.5** | SHOULD | Group with L1; VOS faces the new Cout. |
| L1 2.2 µH | 45.06, 48.79 | **45.5, 54.5** | SHOULD | Keep 3.4 mm to U3. |
| (new) C_U3 VOUT 10 µF | — | **47.0, 54.5** | MUST | At VOS/L1 (P5). C2 4.7 µF stays as remote bulk. |
| C14 VIN 1 µF | 50.0, 39.0 | **49.5, 53.0** | MUST | Was in the keepout band; to U3/U10 VIN. |
| SW1 button | 52.0, 52.0, 90 | **52.0, 57.0, 90** | SHOULD | Right edge; drop with the power block so U9 gets the upper-right. (Mechanical: confirm case button height.) |
| U13/U14 load sw | 41/44.76, 54/59 | **41–45, 58–60** | COULD | Keep near their loads (NFC/display rails). |
| U15 backlight + L15/D15/C13/C15/R15 | 46.5–49.2, 56.5–67.5 | **cluster @ 47–51, 61–66** | COULD | Physically fine; electrical redesign (P1) separate. |

### 3d. Bottom band (USB + secure)

| Ref | Current | Proposed | Class | Reason |
|---|---|---|---|---|
| J1 USB-C | 32.0, 66.2 | **32.0, 66.2** | — | Bottom-center, fixed. |
| U2 TROPIC | 23.34, 64.0, −90 | **23.34, 64.0, −90** | — | Keep (4.6 mm SPI to U1). Redistribute C3/C4/C5 one-per-face; add 2.2–4.7 µF bulk. |
| U4 TROPIC sw | 14.0, 58.57 | **14.0, 62.0** | COULD | Keep in the TROPIC_VCC feed. |
| U7 ESD | 41.0, 68.5 | **33.5, 62.5** | SHOULD | Inline between J1 D+/D− and R3/R4 (flow-through, not stub). |
| C1 VBUS 10 µF | 28.0, 35.5 | **34.5, 68.0** | MUST | 31 mm from J1 today; to the VBUS pads. |
| (new) VBUS TVS | — | **30.0, 68.0** | SHOULD | No VBUS transient protection today (P9). |
| U8 VBUS limiter | 44.5, 64.0 | **45.0, 66.5** | COULD | Keep near J1 VBUS / battery path. |
| R1/R2 CC, R3/R4 series | 39, 61–62.5 / 30–37.5, 59.5 | **around U7/J1** | SHOULD | Keep the CC + series pairs tight to the connector. |

### 3e. Where every ADDED decoupling cap lands (summary, at-pin)

| Net / IC | Add | Land at |
|---|---|---|
| U1 NRST | 100 nF | ~(18.5, 49.5) at pin 14 |
| U1 VDDA / VREF+ | 1 µF each | beside C52/C53 (left-top of U1 ring) |
| U1 VDD bulk | 10 µF | next to C59, U1 bottom row |
| U1 VBAT_SENSE | 100 nF | at pin 15 reservoir |
| U2 TROPIC_VCC | 2.2–4.7 µF | south face of U2 with C3 |
| U9 NFC_VCC | 10 µF + 1 µF + 100 nF | (43–46, 47) at U9 VDD/VDD_TX |
| U9 VDD_A/D/RF+DR/AM, AGDC | 2.2 µF∥10 nF ×4 + 1 µF∥10 nF | ring U9 ≤1.5 mm (7–9 caps) |
| U3 VIN / VOUT | 4.7 µF / 10 µF | at U3 VIN pins / at VOS (47.0, 54.5) |
| U10 IN/OUT/BAT | 4.7/10/4.7 µF | at pins 13 / 10-11 / 2-3 |
| U5 QSPI VCC | 100 nF | (19.5, 63.5) |
| U11 OPTIGA VCC | 100 nF | (16.8, 46.5) |
| Display rail (U14 VOUT / J2) | 2.2 µF+100 nF / 1 µF | at U14 / near J2 VCI |
| I2C1 pull-ups | 2×4.7 k | at the touch/Qwiic bus |
| NFC_PWR_EN / TFT_PWR_EN | 2×100 k pulldown | at U13/U14 ON pins |

---

## 4. Utilization + feasibility of 36.8 mm

Areas (NEW 36.8 frame, W = 42.72):

| Quantity | Value |
|---|---|
| Board area (36.8 × 42.72) | 1572 mm² |
| − corner arcs | −5 |
| − antenna keepout on F.Cu (35.6 × 7.6, loop+1 mm, clipped to top edge) | **−271** |
| = **Effective F.Cu placeable (on-board loop)** | **≈ 1296 mm²** |
| F.Cu courtyard today (minus ANT1 loop) | 1144 mm² |
| + ~40 required new decoupling/matching/protection parts (~2 mm² ea) | +80 |
| = **F.Cu courtyard demand** | **≈ 1224 mm²** |

- **On-board loop @ 36.8 mm → density ≈ 94 %.** Single-side courtyard density above ~85 % on a 4-layer board is where routing typically fails; 94 % is not routable without spilling parts to B.Cu (blocked over most of the center by the display module) or dropping "optional" parts. **Not feasible as specified.**
- **FPC antenna @ 36.8 mm → density ≈ 78 %.** Removing the keepout *and* the loop returns 1567 mm² of placeable area. **Feasible.** This is the recommended path and the NFC reviewer already floated it (`nfc-rf-frontend.md` §6: FPC on the back cover, only `NFC_ANT1/2` on a small connector).
- **Keep 39.8 mm + on-board loop → density ≈ 86 %.** Marginal-feasible, but it defeats the whole purpose (no battery room). Not the ask.

**What must give if the 36.8 mm loop-on-board combination is forced:**
1. Vertical budget is the binding constraint, not horizontal: from keepout bottom (y≈41.6) to USB top (y≈60.4) is **18.8 mm**, and **U1 alone is 17.5 mm**. The entire center column is U1 — nothing else fits above or below it there. All support parts live in the left/right side columns and the bottom band, which is why every column is oversubscribed.
2. **J9 (10.25 mm tall) cannot live at the top** (keepout) and doesn't fit the 4.5 mm corners outside the loop x-span → right-edge or accept the FPC route.
3. **Debug cluster cannot sit in the top-center** (keepout + U1) → B.Cu pogo pads (matches `placement.md` intent) or the FPC route frees the strip.
4. The buck/charger/NFC caps the electrical reviews demand are the +80 mm² that pushes density from 86 %→94 %; they are non-negotiable for correctness, so they can't be the thing that "gives".

**Bottom line on feasibility:** 36.8 mm is achievable **only** by moving the 13.56 MHz loop to a back-cover FPC (leaving a BTB/2-pad feed on the main board). With the loop on the main board, 36.8 mm forces passives onto B.Cu (violating the "B.Cu = J2 only" rule and fighting the ~1–3 mm display gap) and pushes the battery connector and debug pads to compromised locations — I would not commit to a single-side route at that density.

---

## 5. How this pairs with the electrical reviews (do these together in the re-place)

Every scattered-passive finding in `mcu-secure-elements.md`, `power-architecture.md`, and `nfc-rf-frontend.md` is fixed **for free** by the re-cluster above, because re-placing to "cap at pin" is the same operation as the electrical fix. Sequence: (1) resolve schematic-first so ERC runs and the added parts exist as real nets (per `AUDIT-findings.md` root-cause), (2) decide FPC-vs-on-board antenna (feasibility gate), (3) place the fixed clusters from Section 3, (4) reserve the 4-layer keepout, (5) route with proper power net-classes. Do **not** try to nudge the current 39.8 mm placement into 36.8 mm post-hoc — the audit already showed a post-hoc squeeze couldn't even fit the VCAP cap at 39.8 mm.
