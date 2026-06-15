# Placement Agent Brief — nSealr Universal Secure Device (TROPIC01)

You are an agent tasked with **re-placing every component on this PCB toward the best
possible layout** — ordered, aligned, symmetric, clean, with the whole board used both
**functionally and aesthetically**. This brief is self-contained; read the linked specs
for full detail.

---

## 0. THE ONE NON-NEGOTIABLE RULE

**Render and visually inspect the board after EVERY small step.** Not in batches — every
small move. After each change:

1. Render front **and** back (commands in §3).
2. **Read/open the rendered PNGs and actually look at them.**
3. Judge against the checklist (§7). Ask yourself, concretely:
   - Is everything **ordered** (no random scatter)?
   - Is it **aligned** (parts on shared X/Y axes, rows/columns)?
   - Is it **symmetric** where it should be (perimeter, connectors, mirrored blocks)?
   - Is it **clean** (no overlaps, even spacing, no silk-over-copper mess)?
   - Is **all the space used** — functionally (short critical nets) AND aesthetically
     (no large dead zones while other areas are crammed)?
4. If anything fails → **fix it before the next step.** Do not accumulate debt.

A step that is not visually verified does not count. If you cannot see the render, stop
and report — do not proceed blind.

---

## 1. Mission & definition of done
- Re-place all components honoring every HARD constraint (§4).
- Critical nets short (secure SPI/I2C, crystals, decoupling, soft-start caps) — §5/§6.
- Layout tidy: aligned, symmetric, evenly spaced, dead space minimized and balanced.
- **DRC clean** except the accepted edge-mounted-connector exception (USB-C posts).
- Two-sided rule intact (only `J2` on B.Cu).
- Result must be **routable**: verify with the Freerouting flow (§8) — target as few
  unrouted signals as possible (the auto-router plateaus at ~17; the rest is hand-routed,
  so make those few short/trivial).

## 2. Files & git
- Board (source of truth — the schematic is a STUB, ignore it for connectivity):
  `kicad/tropic01-universal-secure-device.kicad_pcb`
- `main` holds the clean reference placement. Work on a branch; commit small, reviewable
  steps. Never commit a half-broken board.
- Full design spec: `design-notes/` → `reference-dev-access-spec.md`,
  `mechanical-architecture.md`, `component-decisions.md`. READ THEM FIRST.

## 3. Environment & commands
- pcbnew Python: `/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3`
- kicad-cli: `/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli`
- Render front: `kicad-cli pcb render --side top --quality high --width 1500 --height 1300 --zoom 1.0 -o /tmp/front.png <board>`
- Render back:  `kicad-cli pcb render --side bottom ... -o /tmp/back.png <board>`
- 3D angled view (sanity): add `--perspective --rotate '-25,0,-35'`.
- DRC: `kicad-cli pcb drc --format json -o /tmp/drc.json <board>` then count
  `courtyards_overlap / clearance / hole_clearance / copper_edge_clearance / solder_mask_bridge`.
- **After ANY footprint move, before DRC/render: refill zones** in pcbnew:
  `pcbnew.ZONE_FILLER(b).Fill(b.Zones())`.

## 4. HARD constraints (never violate)
- **Size:** width = display = **42.72 mm** (never wider), height ≈ **36 mm**,
  board + battery ≤ 59.26 mm.
- **Corners:** **chamfered/rounded (R≈2.5 mm) on all 4 vertices.** A **M2 (Ø2.2) hole at
  each vertex** (4 total). Consequence: **the two top connectors must sit INBOARD**, off
  the edge/corner (so the chamfer doesn't cut them and the corner holes fit).
- **Two-sided:** ALL parts on F.Cu (incl. NFC antenna). **B.Cu = only `J2`** + display
  outline. The display lies flat on B.Cu. (A GND pour on B.Cu is allowed.)
- **Perimeter:** `J6`/`J9` = two connectors top, **inboard**, mouths up/out (J9=battery,
  J6=Qwiic). `ANT1` (NFC loop) top-center. `SW1` (button) center-right edge. `LED1` (RGB,
  top-view) center-left. `J1` (USB-C) bottom-center, all pads on-board. `J2` bottom-center
  on B.Cu.
- **Stackup:** F.Cu / In1=GND plane / In2 / B.Cu. Via 0.4 / hole 0.2 mm.
- **No invented MCU pins** (gate). Keep new pin uses datasheet-pending.

## 5. Component dependencies (what must be near what)
- `U1` STM32U585 (LQFP100, ~½ the board) = the hub, central. Orient so each interface
  faces its peripheral (LQFP100 sides: 1-25 / 26-50=TROPIC SPI+QSPI / 51-75=NFC SPI+USB /
  76-100=OPTIGA I2C+Touch+display).
- `U2` TROPIC01 (SPI) → **hug the STM32 SPI pins**. `U11` OPTIGA (I2C) → next to STM32 I2C.
- `U9` NFC + `X3` (27.12 MHz) + matching (`L30/L31/C30-33/R15`) → at `ANT1` (top), but as
  near the STM32 NFC-SPI pins as possible.
- `X1` (16 MHz HSE) → hug the STM32 HSE pins (NOTE: X1=STM32, X3=NFC — counterintuitive).
- `U5` flash → STM32 QSPI pins. `U7` ESD + CC 5.1k → at the USB-C.
- Power tree: USB-C→`U8`→`U10`(charger)→`SYS_PWR_IN`→`U3`(buck)→`SYS_3V3`; `U15`+`L15`
  backlight + RGB anode off `SYS_PWR_IN`; load switches `U4/U13/U14`→gated rails.
- Decoupling 100 nF → on each IC VDD pin. Soft-start caps `C6/C7/C8` → on their switch
  CT pin (`U4/U13/U14`).
(Full BOM + buses: see `reference-dev-access-spec.md` §5/§6.)

## 6. Placement heuristics (learned — do / don't)
**DO:** secure elements & crystals & decoupling & CT caps adjacent to their IC pins; group
each IC with its passives; ESD/CC at the USB-C; USB diff pair short; GND as a poured plane;
group test points by function (SWD on one Tag-Connect, UART TX/RX/GND together); use empty
regions to balance congestion.
**DON'T:** put a secure element on the side away from its STM32 pins; put a crystal near the
buck/boost switching nodes; leave decoupling on a shared rail far from the chip (caps on
shared SYS_3V3 scatter — assign each to its nearest IC by hand); block an IC's crystal/VDD
pins with a big neighbor (e.g. the RGB LED courtyard); scatter SWD across corners; cram all
power ICs around the USB-C; let connector solder land off the board edge.
**Order of work:** place anchors first (STM32 + perimeter connectors), then IC blocks in
zones, then each IC's passives, then the rest. Never passives first.
**Anti-patterns proven worse:** blind grid-snap / greedy packing of the whole board (scatters
functional groups); full from-scratch auto-placement when the board is already functional
(produced 75 DRC violations — worse). Prefer small, visually-verified, targeted iterations.

## 7. Per-step visual checklist (apply EVERY step)
After rendering front+back and looking:
- [ ] **Ordered** — components grouped logically, no random scatter.
- [ ] **Aligned** — parts share X/Y axes; decoupling in neat rows/columns by their IC.
- [ ] **Symmetric** — perimeter balanced (connectors, holes); mirrored blocks mirrored.
- [ ] **Clean** — 0 overlaps; even, consistent spacing; no silk text over pads/copper.
- [ ] **Space used** — functionally: critical nets short; aesthetically: no big dead zone
      while another area is crammed (balance density across the board).
- [ ] **Constraints still hold** — perimeter parts in place, B.Cu=only J2, all on-board,
      4 corner holes, chamfered corners.
- [ ] **DRC** — only the accepted USB-C edge posts; nothing new.
If any box fails → fix now.

## 8. Routability check (periodically, not every step)
Export DSN **with GND pours filled first** (so Freerouting treats GND as a plane, far less
congestion), run Freerouting, import SES, refill, count unrouted SIGNAL nets. The fewer and
shorter, the better the placement. ~17 signals left for the interactive router is the known
floor — make sure those are short/trivial.
`ExportSpecctraDSN(b,'/tmp/b.dsn')`; `java -jar freerouting-2.2.4.jar -de b.dsn -do b.ses -mp 30`;
`ImportSpecctraSES(b,'/tmp/b.ses')`.

## 9. Tooling gotchas
- Wrap `GetTracks()`/`GetFootprints()`/`Zones()` in `list()` (swig).
- Modify → save → reload between phases; refill zones after moves.
- `ExportSpecctraDSN(board, file)` / `ImportSpecctraSES(board, file)` (2-arg form).
- DRC on a `/tmp` copy without the project shows false `lib_footprint_mismatch` — run DRC
  on the board inside the project dir to get the true picture.
- A footprint placed in `/tmp` with no adjacent `.kicad_pro` uses default rules; min via is
  relaxed to 0.4/0.2 in the project's `.kicad_pro`.
- Some footprints lack a 3D model (test points, holes, jumpers, antenna, Tag-Connect,
  display outline) — that's expected; they render bodiless on purpose.

## 10. Security constraints
- Keep the TROPIC01 SPI and OPTIGA I2C **as short as possible** (integrity + harder to tap),
  ideally on inner layers over the GND plane. Two independent secure elements on separate
  buses, isolated from the touch I2C. Secure rails are gated (load switches) and current-
  measurable (0 Ω jumpers). Keep-out + ferrite under the NFC antenna; GND pour as shield.
- BOOT0/USB-DFU is exposed (reference board); in production it must be locked (RDP-2,
  bootloader disabled) — note it, don't rely on it being open.

## 11. When done
- Commit the final placement (clean, DRC-clean, constraints met) on the branch.
- Report: render front+back, the per-step checklist final state, the routability number,
  and any constraint you had to trade off (with the reason).
- Do NOT auto-wire the power-latch or invent MCU pins — those are human/datasheet gates.
