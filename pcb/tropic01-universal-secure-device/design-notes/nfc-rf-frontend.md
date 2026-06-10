# NFC / RFID RF Front-End (ST25R3916B) — Design Plan

Date: 2026-06-10
Status: topology defined; component values and loop geometry are first-article
tuning gates. Reference: ST **AN5276** "Antenna design for ST25R3916/16B…".

## Why this is not auto-completable

Two hard blockers, by design:

1. **The project ST25R3916B symbol does not expose the RF pins.** In
   `kicad/lib/symbols/TROPIC01.kicad_sym`, the antenna pins (`RFO1`, `RFO2`,
   `RFI1`, `RFI2`) are currently `DNC`. They must be defined from the datasheet
   (DS13541) before the front-end can be wired in the schematic. Confirm the
   exact QFN-32 pin numbers from the datasheet pin table — do not trust
   third-party summaries.
2. **The matching/loop values depend on the measured antenna inductance.** They
   are set with ST's antenna-matching calculator and then trimmed on the first
   article. They cannot be finalised without a board + measurement.

## What is already on the board (just unconnected)

`U9` (ST25R3916B), and the front-end passives are already placed but netless:
`L30`, `L31` (the two EMC-filter inductors `L0a`/`L0b`), and `C30`–`C33` (the
EMC shunt caps `C0a`/`C0b` plus the matching caps). `ANT1` is the antenna
keep-out. So the front-end BOM is essentially right; it needs wiring + values +
the loop.

## Topology (AN5276, differential, single antenna)

```
RFO1 ──L0a──┬── Cs1 ──┬───────────●  ANT terminal A ─┐
            C0a       Cp/2                            │
            │          │                          [ LOOP La ]  (back-side coil)
           GND        GND                             │
RFO2 ──L0b──┬── Cs2 ──┬───────────●  ANT terminal B ─┘
            C0b       Cp/2
            │          │
           GND        GND

RFI1 ── Cr1 ──● ANT terminal A ;  RFI1 ── Cd1 ── GND     (capacitive divider,
RFI2 ── Cr2 ──● ANT terminal B ;  RFI2 ── Cd2 ── GND      RX sense)
```

- **EMC filter** (`L0a`/`C0a`, `L0b`/`C0b`): low-pass, suppresses driver
  harmonics. Typical start: `L0 ≈ 220–470 nH`, `C0 ≈ 47–100 pF` (set cutoff so
  the filter resonates around the carrier per AN5276).
- **Matching** (`Cs1`/`Cs2` series, `Cp` parallel): transforms the antenna LC
  tank to the target driver impedance. Computed from `La` with ST's calculator.
- **RX divider** (`Cr`/`Cd`): scales the antenna voltage into `RFI1`/`RFI2`.
- **Optional damping `Rd`** across the antenna to set Q/bandwidth (needed for
  EMVCo/higher bitrates; may be DNP for a start).

## Antenna loop (the "spira")

- **Back-side copper loop**, placed **top-center of the PCB** (near `U9`/the
  matching block), so the tap target on the device back has no battery directly
  behind it.
- Rectangular spiral, **1–3 turns**, ~0.3–0.5 mm trace, ~0.3 mm gap, occupying
  the available top band of the `44 × 36 mm` board.
- **Ground keep-out** under the loop on all copper layers (no pour inside/below
  the loop).
- **Ferrite sheet** between the loop and the upper-area battery.
- Target inductance roughly `1–3 µH`; the exact turns/size are tuned to hit the
  matching target.

## Concrete next steps (in order)

1. Add `RFO1/RFO2/RFI1/RFI2` (and `VDD_DR`/`VDD_RF` rails) to the ST25R3916B
   symbol from DS13541.
2. Wire the front-end in the schematic binding: `RFO1→L30→…→ANT_A`,
   `RFO2→L31→…→ANT_B`, RX dividers to `RFI1/RFI2`, and assign roles to
   `C30`–`C33`.
3. Draw the back-side loop + ground keep-out + ferrite zone; connect to
   `ANT_A`/`ANT_B`.
4. Use ST's antenna-matching calculator with the measured/estimated `La` to set
   `Cs/Cp/Cr/Cd`; populate the BOM with those starting values (flagged
   `tuning_required`).
5. **First-article tuning**: measure resonance/return loss and trim the caps.

Everything up to step 4 is deterministic engineering; step 5 is the measurement
gate that no script can close.
