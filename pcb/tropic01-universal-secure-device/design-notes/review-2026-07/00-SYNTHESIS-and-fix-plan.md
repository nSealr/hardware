# TROPIC01 Universal Secure Device — Deep Review Synthesis & Fix Plan

Date: 2026-07-03. Consolidates the 2026-07 multi-agent deep review (DFM/PCBWay,
MCU+secure-elements, power-architecture, NFC/RF front-end, mechanical/display,
+ Trezor Safe 7 reference and placement re-floorplan). Every finding here is
traceable to a per-area report in this directory, each sourced to datasheet
pages / app-notes / the Trezor Safe 7 open hardware / measured board geometry.

---

## 1. Executive assessment (honest verdict)

The board has **good bones but is NOT fabricable**, and it **cannot be made
fab-ready by patching the PCB**. Root cause (independently reached by three
reviewers and already stated in the pre-existing `AUDIT-findings.md`):

- **The schematic is a stub.** The KiCad sheets contain only ~11 major symbols;
  live ERC = **146 errors**. ~90 passives, the entire NFC RF front-end, and the
  power ICs exist only as PCB footprints with partial hand-added nets.
- **The generator is half-abandoned and has drifted from the board.** The
  source-of-truth `production/schematic-binding.json` lists only **17
  components**; it does not even contain the buck (U3), charger (U10) or
  backlight (U15), yet those are netted on the PCB (hand-edited in later). The 6
  required test points are in the binding but **absent from the PCB**. So
  re-materializing would not reproduce the board, and hand-patching cannot
  restore a single source of truth.
- Consequently **no ERC ever validated the full design**, which is why
  fab-blocking errors survived (below).

**What is genuinely good (keep):** TROPIC01 (U2) tie-offs match the datasheet +
official devboard + Trezor exactly; OPTIGA (U11) pinout correct; power-tree
*topology* is sound (USB-C → current-limit → power-path charger → single 3.3 V
buck + power-gated islands); STM32 per-pin 100 nF + VCAP well placed; the buck is
adequately sized; via geometry (0.6/0.3) and QFN paste/mask are DFM-correct; USB
is Full-Speed so no controlled impedance is needed; the *major-part placement* is
largely sensible.

**Correct path = schematic-first rebuild** in real KiCad: real symbols (all
pins), real values, ERC-clean schematic → netlist → layout (reuse the good
placement, fix the flagged parts) → route → DRC → fab package. This is "how a PCB
is really made" and what turns this draft into a buildable design.

**Two hard gates that no amount of desk work removes:**
1. **Final interactive routing.** Autorouting plateaus at this density (~28–69
   nets remain); the last cross-board nets need GUI push-and-shove. Scriptable in
   bulk, but the polish is a human-GUI step.
2. **First-article RF tuning.** Every NFC reviewer + AN5276 require the antenna
   matching values to be finalized by **VNA measurement on a physical first
   article with the ferrite + display + battery + back cover assembled**. This is
   physics, not tooling. "Fab-ready" for the NFC portion means "ready to build a
   first article to measure and tune" — the normal industry flow for NFC.

---

## 2. Two gating product decisions (user's call — everything downstream depends on them)

### D1 — Battery capacity vs board height
| Option | Board H | Battery zone | Real cell | Capacity | Cost |
|---|---|---|---|---|---|
| A (keep) | 39.80 | 42.72×19.66 | LP401525-class | ~100–150 mAh | no re-floorplan of top strip height |
| **B (rec.)** | **36.80** | 42.72×22.66 | **EEMB LP502030** (20.5×32×5.3) | **250 mAh** | requires top-strip re-floorplan (also needed for the antenna) |

Recommendation: **B**. The antenna already forces a top-strip re-floorplan, so
the incremental cost of shrinking to 36.8 is small, and it ~doubles battery life.
Requires shifting J9 right to x≈46.5 for the 32 mm cell. Drives the charge-current
resistor (D-dependent) and J9 position.

### D2 — NFC antenna: on-main-PCB loop vs on-FPC-behind-cover (Trezor style)
| Option | What | Pros | Cons |
|---|---|---|---|
| **On-board loop (rec. to try first)** | ~34×6 mm, 4-turn F.Cu loop top-center + 4-layer keepout | one part, no extra connector | detuned by battery/display proximity; must clear the top strip; tuning-gated |
| On-FPC (Trezor) | loop on a flex behind the back cover + BTB connector | robust, decoupled from board planes | adds an FPC part + connector + mechanical design |

Recommendation: design the **on-board loop** (fits the "small & tidy, one board"
goal) but keep `NFC_ANT1/2` brought to a 2-pin provision so an FPC fallback is
possible if first-article Q is unacceptable.

---

## 3. Master defect register

Severity: **[C]** fab-blocking / non-functional · **[H]** important / reliability
· **[M]** quality/DFM. Each item → source report in this dir.

### 3.1 Fab-blocking [C]
| # | Defect | Fix | Src |
|---|---|---|---|
| C1 | Display connector J2 is **FH12-50S (bottom-contact)**; ER-TFT024IPS-3 needs **top-contact** → tail can never mate | Change to **FH12A-50S-0.5SH(55)** (=ER-CON50HT-1); rebuild footprint from FH12A drawing (slot E=25.57) | mechanical |
| C2 | J2 **pin order mirrored** — all 50 signals reversed (LEDA↔GND, 2.8 V onto RESET/IM, SPI/touch scrambled) | Mirror pad numbering (pin-1 to +x local) or reverse the 50-pin map; verify vs physical tail pin-1 at first article | mechanical |
| C3 | Backlight: TPS61165 **boost** feeding **4 parallel** LEDs from a 4.4 V node — cannot regulate below Vin, ~4× LED overdrive, **cannot switch off** | Replace U15/L15/D15/C13/C15/R15 with a **4-sink WLED driver** (or charge-pump) from SYS_PWR_IN with PWM dimming | power |
| C4 | Entire **NFC RF front-end uncaptured**: ST25R3916B symbol exposes only 15/33 pins (RFO1/2, RFI1/2, XTO/XTI, VDD_A/D/RF/DR/AM, AGDC, AAT missing); **antenna is empty copper** | Rebuild symbol (33 pins, DS Table 2); draw the loop (§4 nfc report); add the matching/RX/EMC network | nfc |
| C5 | **69 open connections** (40 GND + TROPIC/NFC SPI, VBUS, NRST, QSPI…) — board is unrouted | Complete routing after re-floorplan (bulk auto + GUI polish) | dfm |
| C6 | **6 required test points absent** from PCB (TP_3V3/BOOT0/GND/NRST/SWCLK/SWDIO) → validator red | Add grouped near J7 TC2030 (mcu report gives coords) | mcu |

### 3.2 Important — reliability / correctness [H]
| # | Defect | Fix | Src |
|---|---|---|---|
| H1 | HSE X1 load caps **placeholder value + 6.5–13.7 mm away** | Pick crystal MPN (CL 8–12 pF, ESR≤80 Ω); compute C18/C19; move to crystal pads; nudge X1 toward pins 12/13 | mcu |
| H2 | **Missing 47 kΩ CSN pull-up** on TROPIC01 (datasheet+devboard+Trezor all have it) | Add 47 k CSN→TROPIC_VCC (switched rail) | mcu |
| H3 | **No 100 nF on NRST** (DS Fig 38) | Add 100 nF NRST→GND at pin 14 | mcu |
| H4 | Charge current **788 mA** (2.6–5.3C for a 150–300 mAh cell) + >1.2 W linear dissipation | Set R_ISET per chosen cell (e.g. 3.57 k→250 mA for LP502030@1C); recompute ITERM | power |
| H5 | Input current-limit chain **inverted/USB-non-compliant** (charger 1.36 A > front-end 0.96 A > USB 0.5 A) | R9→3.24 k (≈497 mA); keep TPS2553 27 k as backstop | power |
| H6 | Charger caps missing: **0 on IN, 0 on BAT, only 1 µF on OUT** | 4.7 µF IN, 4.7–10 µF BAT, 10 µF OUT — at the pins | power |
| H7 | **Buck output cap 37.6 mm from U3** (VOS needs direct short trace, 10 µF min) | 10 µF X5R at L1.2/VOS; keep C2 as remote bulk | power |
| H8 | ST25R3916B **VDD_RF/VDD_DR strap** matches neither DS config | Regulator mode: tie VDD_DR(14)→VDD_RF(9), 1 µF+100 nF, use Adjust Regulators | power/nfc |
| H9 | **NFC decoupling 8–12 mm from U9**, and 7–9 regulator bypass caps missing (VDD_A/D/RF/AM/AGDC) | Add per DS §4.2.10 (2.2µF∥10nF etc.); move C36–C40 to <1 mm from pins | nfc |
| H10 | **No EP vias under U9** (thermal + RF return); no driver-ground vias | 3×3 via farm in EP; per-pin vias on GND_DR1/2 | nfc |
| H11 | **No GND keepout under antenna** — all 4 layers pour over the loop band (shorted-turn, 30–50% L loss) | 4-layer rule-area keepout under loop +1 mm; reroute the segments/vias in the band | nfc |
| H12 | X3 27.12 MHz **9.3 mm from XTO/XTI with the QFN in between**; load caps valueless/15.7 mm away | Move X3 ≤3 mm from pins 4/5; C34/C35 = 15 pF at the crystal; pin FA-238 CL suffix | nfc |
| H13 | **Touch/Qwiic I2C has no pull-ups** — bus cannot work | Add 4.7 k SCL/SDA→SYS_3V3 | power |
| H14 | **NFC_PWR_EN / TFT_PWR_EN float** during reset/DFU (TPS22917 ON must not float) | 100 k pulldowns (matches TROPIC's R5) | power |
| H15 | TROPIC01 **VCC ramp ~1.6 ms > 1 ms** DS limit (CT=1 nF) | C6 → 470 pF | power |
| H16 | OPTIGA & QSPI flash **missing local 100 nF**; OPTIGA footprint has a **phantom EP** (package has none) | Add 100 nF at each VCC; fix USON-10 footprint (remove EP) | mcu |
| H17 | LED_G on **PC15 = no timer** (no HW PWM) + backup-domain pin | Move LED_G→PE9 (TIM1_CH1); record I2C instance split | mcu |
| H18 | USB ESD U7 **9 mm off the D+/D− path** (stub, not flow-through) | Move U7 inline ~(33.5,63); consider R3/R4 0 Ω | mcu |
| H19 | VBAT_SENSE divider **248 kΩ ≫ 470 Ω ADC limit** (garbage readings) | 100 nF reservoir at the ADC pin (or rescale) | mcu |
| H20 | VBUS bulk cap **31 mm from J1**; **no VBUS TVS** | Move/add 10 µF at J1; add 5 V TVS | power |
| H21 | DISPLAY_VCC_SW rail **zero decoupling** | 2.2 µF+100 nF at U14; 1 µF near J2 | power |
| H22 | J6 Qwiic on SYS_3V3 **unfused** | 100–200 mA polyfuse or amend contract | power |

### 3.3 Quality / DFM [M]
| # | Item | Fix | Src |
|---|---|---|---|
| M1 | J2 ~4.4 mm too far from the fold (needs r≈2.1 mm bulge) | Move J2 mouth-face to y≈48.0 (anchor ≈(32,43.6)) | mechanical |
| M2 | DISP1 envelope still models the OLD Newhaven display, parked off-board | Replace with ER-TFT024IPS-3 42.72×59.46 envelope on B doc layers | mechanical |
| M3 | Spec doc height **59.26 → 59.46** (CTP glass vs BL frame) | Correct mechanical-architecture.md + derived numbers | mechanical |
| M4 | No **fiducials** (double-sided assembly needs them) | 3× 1 mm on F.Cu + ≥2 on B.Cu | dfm |
| M5 | **BOM 16/103** — every passive, crystal, LED, load switch missing | Regenerate full BOM from the rebuilt design | dfm/mcu |
| M6 | Assembly needs **panelization** (board < 50×50 min) + centroid/.pos (absent) | PCBWay tab-route panel; generate centroid | dfm |
| M7 | Stale production artifacts (pcbway-manifest "unrouted", drc.json 2026-06-11) | Regenerate at fab-export | dfm |
| M8 | 261 silk graphic lines 0.10–0.12 mm < 0.15 min | Thicken to 0.15 | dfm |
| M9 | Design-rule guardrails were too loose | **DONE** (commit 830da58): annular 0.15, hole 0.3, h2h 0.3, edge 0.3, mask 0.1 | dfm |

---

## 4. Execution plan (schematic-first rebuild)

Phased; each phase gated on the prior. Local commits + repo validators green at
the end.

**Phase R0 — decisions + docs (fast).** Resolve D1/D2. Correct the mechanical
spec (M3), connector part (C1), DISP1 envelope (M2).

**Phase R1 — schematic source of truth.** Choose the lever: either (a) extend the
home-grown binding/contract generator to a *complete* per-pin, per-value,
all-component model and re-materialize into a clean board, or (b) build a real
KiCad schematic (all symbols with full pins, values, ERC). Given the generator is
already drifted, (b) is the honest choice but (a) may be faster to a first
netlist; decide during R1 after scoping the generator. Deliverable: an **ERC-clean
netlist** covering all ~120 components incl. the NFC front-end (C4), corrected
connector/pinout (C1/C2), backlight driver (C3), all decoupling (H-series), test
points (C6).

**Phase R2 — placement / re-floorplan.** Apply the placement report's moves:
shrink to H (D1), clear the top strip, place the antenna + keepout (C4/H11),
group debug + testpoints (C6), put every decoupling cap at its pin (H-series),
relocate X1/X3 + load caps (H1/H12), inline the USB ESD (H18), EP via farms (H10).
0 courtyard overlaps.

**Phase R3 — routing.** Net-classes (power/RF/USB widths). Autoroute the bulk,
then GUI push-and-shove for the remainder (**Gate 1**). GND zones on F/B + In1
plane + stitching vias. DRC 0 + 0 unconnected (excluding documented edge-connector
clearances).

**Phase R4 — fab package + first article.** Full BOM (M5), centroid, fiducials
(M4), gerbers/drill, panelization note (M6), ENIG/4L/1.6 order params, regenerate
production artifacts (M7). Ship as a **first article** for bring-up + **RF tuning**
(**Gate 2**), then freeze production values.

**Realistic deliverable of a headless effort:** phases R0–R2 complete and
verifiable; R3 bulk-routed with the polish flagged for GUI; R4 package assembled
with the two gates (routing polish, RF tuning) explicitly called out. That is a
genuine, honest "fab-ready-for-first-article" state — the correct end point for a
secure NFC device before you commit to a production run.
