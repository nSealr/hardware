# Verification — User's NFC-on-FPC model (loop-over-battery)

Date: 2026-07-04. Scope: validate the user's decided NFC architecture (J-ANT feed top-center →
FPC folds up → NFC loop over the battery, ferrite between loop and battery) against PRIMARY
sources: Trezor Safe 7 rev D antenna FPC + main schematic, ST AN5276 Rev 6, board-truth.json,
mechanical-display-integration.md, nfc-rf-frontend.md.

Primary evidence pulled this session (not from design notes):
- `ts7_fpc_ant_rev_d_sch.pdf` p.1 — Trezor antenna-FPC schematic. Connector **J1 = BM28B0.6-6DP/2-0.35V**.
  Designer note verbatim: **"Qi coil: L≈13.5uH, R≈1.5–2 ohm (depends on Cu thickness & plating). NFC coil: L≈1uH."**
  Net names ANT_QI, ANT_NFC, NTC_1/2 across the 10 pads (variant "No NTC" → NTC nets crossed out).
- `ts7_fpc_ant_rev_d_views.pdf` p.1 — **outer Ø = 30.00 mm** (dimensioned). Top view = a single FPC
  disc carrying BOTH a dense multi-turn Qi spiral (13.5 µH) and the outermost NFC turns (1 µH);
  connector tab with J1 at the bottom. So the Trezor NFC coil and the Qi RX coil share ONE FPC disc.
- `ts7_main.txt` — mating half on the main board is **BM28B0.6-6DS/2-0.35V** (lines 1177, 2187);
  NFC EMC inductor "270n" (L5/L6), "Cpin = 3pF" on the 27.12 MHz crystal (2.0×1.6 mm), NFC_50R net.
- AN5276 Rev 6 p.20 verbatim: *"The best case of an antenna placement is far away from electronics
  or other components like **batteries, displays, or large ground planes** that harm the effective
  radiated RF field."* (an-antenna.txt L1044–1045).

---

## What Trezor actually does (the reference for the user's model) — CONFIRMED

Trezor Safe 7 puts the NFC loop on a **back-cover FPC**, combined with the Qi wireless-charging RX
coil on the same Ø30 mm disc. A Qi RX coil is ALWAYS backed by a ferrite sheet (mandatory to shield
the RX coil from the battery/metal behind it); that same ferrite shields the NFC turns. The FPC
returns to the main board through a **Hirose BM28 0.35 mm-pitch board-to-board (mezzanine) connector**;
the matching network + ST25R3916B stay on the main board. NFC coil L ≈ **1 µH**, outermost turns.

=> The user's architecture (loop on a back-cover FPC, over the battery, ferrite between loop and
battery, matching on the main board, BTB feed connector) is **structurally identical to Trezor Safe 7**.
It is a proven, shipping design. The only Trezor element we DON'T need is the Qi coil (we have no
wireless charging), so our FPC is NFC-only and can be simpler/smaller.

---

## VERDICT 1 — loop-over-battery-works: CONFIRMED (with ferrite; and fix the loop geometry)

- RF soundness: a LiPo pouch is a lossy foil conductor; an unshielded loop laid flat on it would be
  heavily damped (eddy losses → La down, Q down, field killed). AN5276 p.20 explicitly names batteries
  as field-harming (quote above). **The mitigation is a ferrite sheet between loop and battery** — this
  is exactly how essentially every smartphone runs NFC over its battery, and how Trezor's Qi+NFC combo
  coil sits over its cell. So loop-over-battery is not merely acceptable, it is mainstream known-good
  practice **provided a ferrite backing is present**. (AN5276 itself does not prescribe the ferrite —
  that guidance is Würth ANP022 / general RFID practice + the Qi-combo precedent; do not cite AN5276 as
  the ferrite source.)
- Ferrite: **Würth WE-FSFS**, 364-material (µ′≈110–120, low µ″ at 13.56 MHz), e.g. cut from **374006**
  (0.3 mm) or a thinner 0.1/0.2 mm variant. Cover the loop aperture + ~1 mm margin. Expect the ferrite
  to RAISE La ~10–30 % (installed La for a 1 µH bare loop → ~1.1–1.3 µH) and add modest loss; the
  battery behind the ferrite then only lightly loads Q. **All matching must be finalized with ferrite +
  battery + display + back cover assembled** (first-article VNA gate, AN5276 §4).
- GEOMETRY CAUTION (concrete, from mechanical §5): the battery zone at H=36.8 (Option B) is
  **42.72 (w) × 22.66 (h) mm**. A **Ø30 mm circular loop (Trezor's size) does NOT fit** in a 22.66 mm-tall
  band — 30 > 22.66. To keep the loop entirely over the battery (off the PCB ground planes), make it a
  **rectangular/oval loop ≈ 38 × 20 mm** (area ≈ 760 mm², comparable to Trezor's Ø30 = 707 mm², so ~1 µH
  is still reachable at 3–4 turns). If instead the loop is allowed to extend south of y=34 over the PCB,
  the full 4-layer copper keepout of nfc-rf-frontend.md §4 becomes mandatory under that overhang.
  **Do not copy Trezor's Ø30 verbatim — resize to the 22.66 mm battery band.**
- Better place than over the battery? Marginally, over the display frame is WORSE (the module's metal
  backlight frame spans the full 59.46 mm and is a solid eddy sink at 1–3 mm). Over-battery-with-ferrite
  is the best available location given the industrial design; keep it.

## VERDICT 2 — feed-path-ok: PARTIAL / NEEDS-WORK (feed too long as currently placed)

- Measured from board-truth.json: **U9 (ST25R3916B) is at (40.173, 48.0)** — mid-board, ~14 mm below
  the top edge, NOT near the top. A J-ANT at top-center (~x=32, next to J9@(44,37.5) / J6@(19,36.5),
  y≈35–36) is **≈14.5–16 mm** from U9 center (√(8.17² + 12–13²)). The matching network output (antenna
  node, high-Q, stray-C-sensitive) would then run ~15 mm to J-ANT. That **exceeds nfc-rf-frontend.md
  §2's own ≤15 mm feed guideline** and is longer than Trezor keeps its BTB-to-matching run.
- Recommendation: **move U9 + the whole matching network UP to just below J-ANT** (e.g. U9 → ~(32, 42)
  with J-ANT at ~(32, 35)) so the post-match differential feed is **< 8 mm**. This is feasible only
  inside the already-required top-strip re-floorplan (mechanical §5). Keep the feed a tightly-coupled
  differential pair (0.4 mm / 0.3 mm gap), and **void all copper (all 4 layers) under the feed and under
  the loop** — In1 GND under the feed acts as a shorted turn. If U9 cannot move, keep the matching at U9
  and route the shortest possible symmetric pair; treat the ~15 mm feed inductance (~10–20 nH) as part of
  La in tuning.

## VERDICT 3 — connector-choice: CONFIRMED direction; concrete MPN below

- Trezor's proven part is the **Hirose BM28 series, 0.35 mm pitch, 0.6 mm stack height mezzanine BTB**:
  FPC side **BM28B0.6-6DP/2-0.35V**, board side **BM28B0.6-6DS/2-0.35V** (6 signal contacts). A soldered
  BTB is RF-cleaner than a ZIF/FFC clamp for a differential antenna node and is the right choice.
- We only need 2 signals (NFC_ANT1/2) — no Qi, no NTC. Two options:
  1. **Reuse Trezor's exact part** (BM28B0.6-6DP/2-0.35V + …-6DS…): assign 2 pads to the diff pair,
     ground/leave the rest → proven, gives mechanical margin. Recommended primary.
  2. Smaller BTB if board space is tight: Hirose **DF37** or Molex SlimStack 0.4 mm 4-pin, or a 2-pin
     BTB. Any of these works; verify current rating covers the TX antenna-node current (matching-network
     current at full power can be a few hundred mA — BM28 handles 0.3 A/contact, fine).
- Do NOT use a plain 2-pin JST/wire connector for the antenna node (adds uncontrolled series L and a
  ground-return asymmetry). A mezzanine BTB keeps the FPC parallel-fold geometry Trezor uses.

## VERDICT 4 — matching-values-for-FPC-loop: nfc-rf-frontend.md §3 numbers DO NOT apply as-is (PARTIAL)

The §3 table (Cs 180 pF, Cp 240 pF) was derived for the **small on-board strip La ≈ 370–480 nH**. An FPC
loop over the battery is BIGGER → **L ≈ 1 µH** (Trezor's own value for a Ø30 combo coil). Re-derive:

- ω = 2π·13.56 MHz = 8.519e7 rad/s. X_L = ωL = **85.2 Ω** at 1 µH.
- Total resonating C at 13.56 MHz: C_res = 1/(ω²L) = 1/((8.519e7)²·1e-6) = **≈ 138 pF**
  (vs ≈ 372 pF for the 370 nH strip — i.e. the required C scales as 1/L, ~2.7× LESS capacitance).
- **Cheapest, safest starting point: adopt Trezor Safe 7's published 1 µH-coil values directly** (they
  ship exactly our L): **Lemc 270 nH, Cemc 680 pF** (fc = 1/(2π√(270n·680p)) = **11.7 MHz** ✓, in AN5276's
  8–17 MHz band, out of 13–14), **Cs ≈ 150 pF/leg, Cp ≈ 70 pF differential, Rdamp ≈ 2 Ω**, RX divider
  **Cr ≈ 180 pF / Cd ≈ 680 pF**. Sanity: 2×150 pF series (=75 pF) + 70 pF diff ≈ 145 pF ≈ the 138 pF
  resonance target. ✓
- Net delta vs §3: **EMC filter (Lemc/Cemc) and the RX divider (Cr/Cd) carry over unchanged** (they don't
  depend on La); only **Cs and Cp change** — Cp drops hard (240 pF → ~70 pF) and Cs drops (180 → ~150 pF)
  because higher L needs far less resonating C. Mark Cs, Cp, Cr, Cd, Rd `tuning_required`; finalize with
  the full mechanical stack + ferrite on a VNA (STSW-ST25R004 / eDS Tuning).

---

## Bottom line
The user's NFC-on-FPC model is sound and Trezor-precedented: FPC loop over the battery with a ferrite
sheet, matching on the main board, BTB feed connector. Three concrete corrections: (1) the loop must be
resized to ~38×20 mm to fit the 22.66 mm battery band (Ø30 doesn't fit); (2) move U9+matching toward
top-center or accept a ~15 mm feed as tuned-in L — the feed as drawn is too long; (3) for the 1 µH FPC
loop use Trezor's Cs≈150/Cp≈70 pF, NOT §3's Cs 180/Cp 240 (those are for the 370 nH on-board strip).
