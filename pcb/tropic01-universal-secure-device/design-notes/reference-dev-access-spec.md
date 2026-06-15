# Reference Developer-Access & Eval Features — Design Spec

Date: 2026-06-15
Status: brainstorm approved; pending implementation
Approach: **A — "reference handheld"** (keep the display-sized form, add
space-efficient developer access).

## Revision 2026-06-15a — controls & power (supersedes "B" below)

After review, the buttons/power were simplified and made more correct:

- **One button only: `SW1`** = user input **and** power. **No RESET button, no
  BOOT0 button.**
- **Power = soft-latch on `SW1`, giving a true OFF (zero draw).** `SW1` starts the
  rail by gating the buck `U3` (TPS62840) `EN` (today tied always-on); the MCU then
  holds it via a **`PWR_HOLD`** GPIO; long-press → MCU releases → real off. **USB
  insertion auto-starts** the rail. With the battery this is the on/off; `J9` is
  removable for zero-draw storage.
  - **REVIEW-REQUIRED (critical power path):** exact topology (discrete soft-latch
    vs dedicated pushbutton-controller IC), values, and 3.3 V/4.2 V level handling
    must be datasheet-designed and **bench-validated** before fab — gated like the
    NFC matching network, not "done".
- **BOOT0 = a small jumper (`BOOT0`↔`SYS_3V3`)**, not a button. DFU stays possible
  without a debugger (set jumper + power-cycle); SWD via `J7` already flashes
  everything; `R22` 100 k keeps BOOT0 low normally.
- **Reset needs no button:** power-cycle, or the debugger via `J7` (NRST is on it).
- **Why:** for a battery secure device one multi-purpose button (power+user) is the
  clean norm; RESET/BOOT0 buttons were redundant and ate scarce edge space.

Because the board is **at capacity**, the remaining additions (BOOT0 jumper, UART
group, current-sense jumpers, power-latch parts, breakout) are placed in **one
holistic pass** that reserves room for all of them — not dropped into gaps.

## Goal

Turn the board into the **definitive, self-contained secure-element reference
platform**: any project that wants to build on a secure element can pick this
board up and **program, debug, field-update, extend, and power-profile** it
without bespoke tooling.

## Hard constraints (unchanged — must still hold)

- **Display-sized handheld envelope** (board = display width; board + battery ≤
  display height). Do **not** grow the board. See `mechanical-architecture.md`.
- **B.Cu carries only `J2`** (display lays flat). All new parts go on **F.Cu**.
- Keep **0 courtyard/clearance overlaps**; DRC clean except the accepted
  edge-mounted USB-C exception.
- Respect the `no_llm_invented_pin_numbers` gate: any new MCU pin use is recorded
  as **datasheet-pending**, never invented.
- Don't break existing nets/components.

## Features

### Must-have

**A. SWD programming consolidation**
- Add one **Tag-Connect TC2030-NL** footprint (2×3, 1.27 mm, no installed
  connector) on F.Cu, in an accessible spot.
- Nets: `SWDIO`, `SWCLK`, `NRST`, `SYS_3V3`, `GND` (+ key/NC pin).
- Remove the now-redundant scattered SWD test pads (`TP_SWDIO`, `TP_SWCLK`,
  `TP_NRST`) — folded into the TC2030. Keep `TP_3V3`, `TP_GND` as general probe
  points.
- Rationale: one debugger landing site instead of 5 pads in 4 corners.

**B. USB-DFU firmware update (no debugger)**
- **RESET** tactile: `NRST` ↔ `GND`.
- **BOOT0** access: tactile (`BOOT0` ↔ `SYS_3V3`) with a pulldown on `BOOT0`
  (verify the existing one, add if missing).
- Hold BOOT0 + tap RESET → STM32U5 built-in **USB-DFU** over USB-C.
- These are **developer/maintenance controls**, distinct from the single
  user-facing approve/reject button `SW1` (the "one user button" UX in
  `mechanical-architecture.md` still holds). They may be small **tactiles** or, to
  avoid any accidental-press surface on a finished unit, **pads/jumpers** —
  default to tactiles for the reference board; the enclosure can omit/recess them.

**C. UART console, grouped**
- Group `EXP_UART_TX`, `EXP_UART_RX`, `GND` into a labeled 3-pad strip on F.Cu
  (replacing the scattered `TP_UART_*` + bottom GND).

**D. Self-documenting silk**
- Clear labels on every header, test point, and connector. Final silk legibility
  pass happens at the post-routing polish step.

### Optional (include if they fit; must-haves win on space)

**E. GPIO/SPI breakout (castellated edge)**
- Castellated pads on a free board edge exposing: a few spare STM32 GPIOs, the
  expansion SPI bus (`EXP_SPI_*`), `SYS_3V3`, `GND` (I2C already on Qwiic `J6`).
- Pin count set by available edge length. New MCU pins = datasheet-pending.

**F. Per-rail current measurement**
- Series 0 Ω / jumper (0402) on each secure-element supply: `TROPIC_VCC_SW`,
  the OPTIGA (SE2) rail, `NFC_VCC_SW` — so each element's draw can be measured.
- ~3 jumpers.

### To verify (may not fit)

**G. 4 mounting holes** (add 2 at the top). The top edge is crowded
(battery/NFC/connectors); verify before committing.

### Deferred

**H. Lanyard hole** — this is an **enclosure** feature (the PCB outline = display
outline), not a PCB change now.

## Space plan

Board is ~68% courtyard-filled with ~23 small free pockets. Implementation order:
must-haves (A–D) first, then E and F. If space gets tight, must-haves take
priority; the result will report exactly what fit and what did not.

## Success criteria

- SWD on a single footprint; RESET + BOOT0 accessible for USB-DFU; UART grouped.
- E and F added where space allows.
- 0 courtyard/clearance overlaps; DRC clean except the accepted USB-C edge posts;
  B.Cu still only `J2`; board envelope unchanged.
- `netlist-contract.json`, `pinmux-ledger.json`, and `component-decisions.md`
  updated; all new MCU pin uses flagged datasheet-pending.

## Open questions / risks

- KiCad availability of the TC2030 footprint (verify; import if absent).
- Presence of an existing `BOOT0` pulldown (verify).
- Breakout pin count is limited by free edge length.
- All new MCU pin assignments require datasheet-backed pinmux review (existing
  project gate `pinmux_review_required`).
