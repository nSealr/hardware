# Completeness Critic — what the 7-area review missed or covered thinly

Date: 2026-07-04. Scope: adversarial gap-hunt, NOT re-litigating the known 6C/22H/9M register.
Sources read in full: `00-SYNTHESIS-and-fix-plan.md`, `board-truth.json`, `mcu-secure-elements.md`,
`power-architecture.md`, `nfc-rf-frontend.md`, `mechanical-display-integration.md`, `dfm-pcbway.md`,
`trezor-safe7-reference.md`. Datasheets cross-checked: TPS62840 (buck-only), BQ24074, ST25R3916B
AN5276, ER-TFT024IPS-3, STM32U585 DS13086.

The prior review is genuinely strong on the *electrical schematic* and *DFM* axes. The gaps below are
overwhelmingly at the **system / product / physical-integration** boundary — the seams between the PCB
and (a) the enclosure, (b) the battery discharge physics, (c) the FPC antenna that was *decided* but
never *designed*, (d) security posture beyond pin tie-offs. These are exactly the class of defect that
survives a schematic review and then bites the first article.

---

## G1 [CRITICAL] The DECIDED FPC antenna is entirely undesigned — board + every report still describe the on-board loop

- D2 was decided 2026-07-03 = **FPC antenna** (loop moves to a back-cover flex, matching stays on
  main board, `NFC_ANT1/2` go to a feed connector J-ANT). But nothing downstream reflects it:
  - `board-truth.json` still has the **on-board** `ANT1` envelope at (32,33) F.Cu; there is **no J-ANT
    connector** anywhere in the placement (only J1/J2/J6/J7/J9). The user's "J-ANT top-center next to
    J9/J6" element does not exist on the board.
  - `nfc-rf-frontend.md` §2–5 spec an **on-board 33.6×6 mm 4-turn loop** with a 4-layer keepout — i.e.
    the whole detailed antenna section is for the *rejected* option. The FPC path is one paragraph (§6).
  - **No FPC deliverable exists**: no flex gerbers, no flex stackup (1-layer vs 2-layer, coverlay,
    stiffener at the connector), no separate panelization/PO, no strain-relief or fold-radius spec for
    the *antenna* flex (distinct from the display-tail fold in mechanical §2.3).
  - **No connector selected.** Trezor uses a 6-pin BM28B0.6-6DP/2-0.35V BTB. The RF loop carries a large
    circulating current (tuned tank, ~0.5–2 A depending on Q); a BTB in that path adds series R + parasitic
    L that detunes and drops Q. J-ANT MPN, contact count (double-up pins), and its placement/keepout are
    all unspecified.
  - **No ferrite BOM line, no ferrite MPN/thickness** (nfc §4 names WE-FSFS *for the on-board case*, not
    sized for the FPC-over-battery stack).
- Net: a whole fab item (the flex), a whole connector, a ferrite part, and a re-floorplan (remove ANT1,
  add J-ANT, free the top strip) are missing. This is the single largest completeness hole and it sits on
  the exact feature the user most wants validated.
- Verdict: **NEEDS-FIRST-ARTICLE + design work.** The FPC must be drawn as its own deliverable before any
  fab package is meaningful.

## G2 [HIGH] Loop stacked OVER the LiPo is the worst-case metal proximity — the FPC-over-battery model was never analyzed

- The user's model folds the FPC so the NFC loop lies **over the battery** on the back-top. A LiPo pouch is
  a large aluminized-foil + electrode sheet = a strong eddy-current sink **directly behind** the loop.
- `nfc-rf-frontend.md` §4 only analyzed the **coplanar** battery (in-plane, "clips the fringing field,
  tens of kHz shift" — small). The **stacked** case is a different, much worse geometry and is unanalyzed.
  AN5276 §5.1 explicitly lists batteries/large planes as field killers. Trezor's Ø30 loop sits on the back
  cover **not on the cell** — they avoided exactly this.
- Even with a full ferrite shield (µ′≈110–120, ≥0.1–0.3 mm, sized > loop +1 mm) between loop and cell,
  expect meaningful range loss; without full ferrite coverage the loop is nearly shorted. A fallback layout
  (loop over the back-cover area **away** from the cell) and a first-article **read-range** test (not just
  VNA tuning) must be planned.
- Verdict: **NEEDS-FIRST-ARTICLE.** Add ferrite spec sized to the loop, and a range-vs-position test.

## G3 [HIGH] Low-battery operating window / brown-out from a 3.3 V *buck* on a 1-cell LiPo is unanalyzed (and P14 mis-states it)

- U3 TPS62840 is a **step-down (buck) only**. It physically cannot hold 3.3 V once VBAT drops below
  ~3.4–3.5 V (Vout + dropout). Yet `power-architecture.md` P14 computes "~0.6 A × 3.3/2.9 V ÷ 0.85" — i.e.
  it assumes the rail still regulates 3.3 V at **2.9 V input**, which is impossible for a buck. So:
  1. Usable capacity is truncated (the 3.4→3.0 V tail of the LiPo is unusable), shrinking effective mAh.
  2. **Brown-out under NFC TX:** ST25R3916B TX bursts pull 250–500 mA; on a small cell near end-of-charge
     the battery + BQ24074 BATFET IR drop can momentarily sag VBAT under the buck dropout → the 3.3 V rail
     dips → STM32 can reset **mid-crypto / mid-SPI to the secure element**. No analysis of this interaction.
- No spec anywhere for: STM32 **BOR level** selection, an **under-voltage lockout / low-battery cutoff**
  threshold, graceful-shutdown-before-dropout, or the **SE reset order** on brown-out. Trezor's PMIC gives
  UVLO for free; ours has none. Options: buck-boost (e.g. TPS63802) for brown-out immunity + full capacity,
  or firmware UV cutoff ≈3.5 V (accept lost capacity) with BOR set high enough for a clean reset.
- Verdict: **CONFIRMED gap.** Pick the low-battery strategy and set BOR; this is a security-relevant
  reliability item, not a nicety.

## G4 [HIGH] No true off / ship mode — the cell can be deep-discharged in storage

- BQ24074 has no ship-mode FET; the buck EN is tied to VIN (always-on); SW1 is a plain MCU GPIO. With a cell
  connected and the device "off", quiescent draw (buck Iq + STM32 Stop + VBAT_SENSE 3.2 µA + leakages)
  slowly pulls the LiPo below the pack PCM cutoff → cell damage / non-recoverable. On a 250 mAh cell this is
  weeks, not years. Trezor gets hardware power-on + ship mode from the nPM1300; the Trezor cross-check listed
  ship mode as "UX", but for a small cell it is a **battery-safety** completeness gap.
- Fix direction: load-switch on the buck EN latched by a button/charger ship-mode, or a documented storage
  charge policy + auto-shutdown. Verdict: **CONFIRMED gap.**

## G5 [HIGH] ESD/EMC coverage stops at USB — exposed antenna, button, and Qwiic are unprotected

- All ESD work (U7 TPD4E05U06, the recommended VBUS TVS) is on USB only. Uncovered user-touch / field paths:
  - **NFC antenna**: a large exposed conductor on the back cover is a direct ESD injection route into
    RFI1/2 / RFO1/2. ST reader designs sometimes add antenna-terminal ESD/spark-gap; ours has none.
  - **SW1 button**: user-touched metal straight to a GPIO; no series R + TVS/cap. Trezor uses 100 Ω + 100 nF
    at the button (also debounce).
  - **J6 Qwiic**: user-accessible SYS_3V3 + I2C with no ESD and (P17) no fuse.
- For a security product that will need IEC 61000-4-2 (±8 kV) and CE/FCC, these are first-article EMC-lab
  failures. Verdict: **CONFIRMED gap** — add button RC+TVS, antenna-terminal ESD provision, Qwiic ESD.

## G6 [HIGH] No hardware tamper / case-intrusion on a "secure device" — STM32 TAMP + backup-erase unused

- Trezor wires TAMP → STM32 tamper pin (+ header). Ours leaves **all STM32U5 TAMP pins unused**, has **no
  case-open switch, no light sensor, no tamper mesh** (dfm reviewer also couldn't confirm Trezor's mesh).
  The STM32U5's anti-tamper → automatic backup-domain **secret-erase** feature is completely unexploited.
  A physical attacker gets unlimited, undetected access. The prior reviews list TAMP only as
  "SHOULD-CONSIDER"; for a wallet this is a security-completeness gap, not an optional.
- Fix direction: wire ≥1 TAMP to a case-open switch/mesh, enable tamper→backup-erase, store the device
  secret in backup SRAM. Verdict: **CONFIRMED gap.**

## G7 [MEDIUM] LSE absent AND VBAT backup domain has no cell → secure time / tamper timestamp is not persistent

- Known: no 32.768 kHz LSE (RTC on LSI) — flagged in mcu/trezor reports. **New completeness point:**
  STM32 **VBAT is tied to SYS_3V3** (mcu §1.1) — there is no coin cell / supercap. So RTC + backup registers
  + tamper timestamp **reset whenever the LiPo dies**. For attestation / anti-rollback / tamper-time this is
  a hole even if an LSE is added. Decide: LSE + a small VBAT backup source, or explicitly document that
  secure time is non-persistent. Verdict: **CONFIRMED gap (thinly covered).**

## G8 [MEDIUM] Enclosure integration beyond the PCB is unquantified

Mechanical review nailed J2/outline/battery but did **not** cover:
- **SW1 actuation:** only the 0.32 mm edge overhang is noted (mechanical §3). No plunger stroke, no case-wall
  cutout dimension, no confirmation the side actuator reaches through the wall.
- **USB-C J1 alignment:** only XY overhang noted; the receptacle mouth **Z-height above the board** vs the
  case aperture (and whether a mid-mount/flush cutout lines up) is unspecified.
- **Screw bosses:** MH1–4 are clearance holes, but the mating case bosses (typ. Ø3.5–4 mm) intrude and are
  **not** keepout-checked against neighbours — MH2 (50.9,68.4) sits by SW1/D15/U8; MH4 (50.9,33.6) sits in
  the top-strip / antenna zone.
- **Display bonding:** the front bond of the CTP glass to the case bezel (adhesive/foam gasket) is not
  specified; only the B-side COF-bump clearance (§2.3) is.
- **Total Z-stack:** no single thickness number. Display ~4.2 + air + board 1.6 + tallest F.Cu part **J9
  JST-PH = 6.0 mm** → the device is ≥~12 mm thick at J9; is J9 the right (tall) connector for a thin secure
  device, or should the battery use solder tabs / a low-profile BTB? Unaddressed.
- Verdict: **CONFIRMED gap** — needs an enclosure stack drawing before first article.

## G9 [MEDIUM] Thermal: no junction-temp budget, no EP via-farm for the charger (U10) or buck (U3)

- Only `nfc` specced U9's EP via farm. The **biggest dissipator, U10 BQ24074 (linear charger)**, and U3
  TPS62840 got **no EP thermal-via spec**, and the same measurement method that found "0 vias under U9" would
  find none under U10/U3. At the *corrected* 250 mA charge U10 ≈0.3–0.5 W (Tj rise ≈20 °C @ θJA~40 °C/W —
  fine); at the *un*corrected 788 mA it is ~1.58 W and thermally folds back (power P2). Point: the all-F.Cu
  layout is thermally OK **once P2 is applied**, but nobody wrote the one-line Tj = Ta + θJA·P budget for
  U10/U3/U9/backlight-driver or drew their EP via farms. Verdict: **PARTIAL** — add EP vias + a thermal note.

## G10 [MEDIUM] FPC + double-sided assembly manufacturing details are thin

- The antenna FPC (G1) is a **separate fab process** (flex, coverlay, stiffener) needing its own drawing,
  fab notes, and PO — none exist. Double-sided assembly is noted for fiducials but **MSL handling / bake**
  for TROPIC01/OPTIGA/QFN and the **reflow profile** for a 0.4 mm-pitch QFN with parts on both sides are not
  called out. The **tuning gate** now spans main board + flex + ferrite + battery + back cover as one
  assembly; the procedure/owner for tuning a *flex* antenna (vs the on-board loop the reports describe) is
  unspecified. Verdict: **PARTIAL.**

## G11 [MEDIUM] Firmware↔hardware dependency checklist not consolidated; production SWD lockdown missing

- **Satisfied by silicon (record so they're not mistaken for gaps):** STM32U585 has on-chip TRNG and
  TROPIC01 has its own RNG → no external entropy part needed; VIT6 is LDO-only → no SMPS inductor needed.
- **Genuine gaps:** LSE (G7), TAMP (G6), the 47k MISO pull-up libtropic needs (already in mcu §3 — keep).
- **New:** nothing in hardware plans **RDP/readout protection**. The TC2030 SWD is **always exposed** on a
  shipped secure device = a debug-attack surface. A production plan for RDP level 2 (or disabling/fusing SWD
  after provisioning) is absent from all reports. Verdict: **CONFIRMED gap.**

## G12 [LOW] Regulatory pre-compliance for the 13.56 MHz intentional radiator is unscoped

- The NFC reader is an intentional radiator → FCC Part 15.225 / EN 300 330 field-strength + harmonic limits,
  which the EMC filter (fc 8–17 MHz) and Q control feed directly. No pre-compliance plan / test budget is
  mentioned anywhere. First-article is the right time, but it should be on the list. Verdict: **CONFIRMED
  gap (minor at this stage).**

---

## Cross-check vs Trezor Safe 7 (what they have that we're still missing, completeness lens)

| Trezor feature | Ours | Already flagged? | Completeness delta |
|---|---|---|---|
| LSE 32.768 kHz | none (LSI) | yes | + **no VBAT backup cell** → time not persistent (G7, new) |
| TAMP → MCU tamper pin | unwired | "consider" | + no case switch/mesh/light sensor; backup-erase unused (G6) |
| Battery NTC / JEITA | 10k fixed, no NTC | yes | (adequately covered) |
| Ship mode / HW power-on (nPM1300) | none | "UX nicety" | + **deep-discharge safety** on a small cell (G4, elevated) |
| PMIC UVLO | STM32 BOR only | no | + **buck can't hold 3.3 V at low VBAT** (G3, new) |
| Antenna on back-cover FPC **off the battery** | decided-FPC but undesigned, user wants it **over** the cell | thin | G1 + G2 (biggest holes) |
| Button RC (100 Ω+100 nF) | bare GPIO | no | ESD/debounce (G5) |

## Bottom line

The schematic-level review is thorough and its 6C/22H/9M register is sound. The **uncovered risk is at the
system boundary**: the FPC antenna the user cares about is decided-but-unbuilt (G1) and placed in the worst
metal-proximity spot (G2); the LiPo→3.3 V buck brown-out / low-battery window is unanalyzed and one prior
calc (P14) is physically wrong (G3); there is no ship mode (G4), no ESD beyond USB (G5), and — on a *secure*
device — no tamper detection, no persistent secure time, and no SWD lockdown plan (G6/G7/G11). Thermals are
fine once the charge current is fixed but lack EP vias/Tj numbers for U10/U3 (G9). None of these are fixable
by patching the current board; they need design decisions before a first article is worth building.
