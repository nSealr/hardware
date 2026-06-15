# Reference Developer-Access & Eval Features — Implementation Plan

> **For agentic workers:** implement task-by-task; each task is a pcbnew edit +
> a verification step + a commit. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Add space-efficient developer access (one SWD port, USB-DFU buttons,
grouped UART), per-rail current-sense jumpers, and an edge breakout to make the
board the definitive secure-element reference handheld — without growing the
display-sized envelope or putting anything but `J2` on B.Cu.

**Architecture:** The board is the source of truth (schematic is a stub). All
edits are headless pcbnew Python against
`kicad/tropic01-universal-secure-device.kicad_pcb`. Each task ends with a DRC +
net-integrity check and a commit. New MCU pin uses are recorded as
datasheet-pending (respecting the `no_llm_invented_pin_numbers` gate).

**Tech Stack:** KiCad 10 bundled pcbnew (`/Applications/KiCad/KiCad.app/Contents/
Frameworks/Python.framework/Versions/3.9/bin/python3`), `kicad-cli` for DRC/render.

**Conventions used by every task:**
- `KPY` = the pcbnew python above; `KCLI` = `…/MacOS/kicad-cli`; `BRD` =
  `kicad/tropic01-universal-secure-device.kicad_pcb`.
- Work on `/tmp/work.kicad_pcb` (copy of `BRD`), verify, then copy back and commit.
- Verify helper (reused): load board, assert target nets have the expected pads,
  assert 0 courtyard/clearance overlaps (excluding the 2 accepted USB-C edge
  posts), run `kicad-cli pcb drc`.
- Commit messages: no Co-Authored-By trailer.

---

### Task 1: Consolidate SWD onto one Tag-Connect TC2030 port

**Files:** Modify `BRD`.

- [ ] **Step 1: Add the TC2030 footprint and wire SWD, remove scattered SWD pads**

```python
import pcbnew
FM=pcbnew.FromMM
b=pcbnew.LoadBoard('/tmp/work.kicad_pcb')
CONN="/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints/Connector.pretty"
def net(n):
    x=b.FindNet(n);  return x if x else (lambda nn: (b.Add(nn) or nn))(pcbnew.NETINFO_ITEM(b,n))
tc=pcbnew.FootprintLoad(CONN,"Tag-Connect_TC2030-IDC-NL_2x03_P1.27mm_Vertical")
tc.SetReference("J7"); tc.SetValue("SWD_TC2030")
b.Add(tc); tc.SetPosition(pcbnew.VECTOR2I(FM(24.0),FM(58.5)))   # F.Cu, accessible; nudge if it overlaps
# ARM SWD-on-TC2030 (TC2030-CTX) pinout: 1=VCC 2=SWDIO 3=NRST 4=SWCLK 5=GND 6=NC
m={'1':'SYS_3V3','2':'SWDIO','3':'NRST','4':'SWCLK','5':'GND'}
for p in tc.Pads():
    if p.GetNumber() in m: p.SetNet(net(m[p.GetNumber()]))
for ref in ('TP_SWDIO','TP_SWCLK','TP_NRST'):    # folded into J7
    f=b.FindFootprintByReference(ref)
    if f: b.Delete(f)
b.Save('/tmp/work.kicad_pcb')
```

- [ ] **Step 2: Verify nets + overlaps + DRC**

Run a check script: assert `J7` pads carry `SYS_3V3/SWDIO/NRST/SWCLK/GND`; assert
`SWDIO`,`SWCLK`,`NRST` still each have ≥2 pads (MCU + J7); assert 0 new courtyard
overlaps; then `KCLI pcb drc /tmp/work.kicad_pcb`.
Expected: J7 wired; no overlap; DRC violations only the 2 USB-C edge posts + silk.
If J7 overlaps a part, move it (try 20.5,58.5 / 27,58 / 24,60) and re-check.

- [ ] **Step 3: Commit**

```bash
cp /tmp/work.kicad_pcb kicad/tropic01-universal-secure-device.kicad_pcb
git add kicad/tropic01-universal-secure-device.kicad_pcb
git commit -m "feat(pcb): consolidate SWD onto one Tag-Connect TC2030 (J7)"
```

---

### Task 2: RESET + BOOT0 buttons for USB-DFU flashing

**Files:** Modify `BRD`. (BOOT0 pulldown `R22` 100k already exists — do not add one.)

- [ ] **Step 1: Add two tiny SMD tactiles**

```python
import pcbnew
FM=pcbnew.FromMM
b=pcbnew.LoadBoard('/tmp/work.kicad_pcb')
BTN="/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints/Button_Switch_SMD.pretty"
def net(n):
    x=b.FindNet(n); return x if x else (lambda nn:(b.Add(nn) or nn))(pcbnew.NETINFO_ITEM(b,n))
def add_btn(ref,a,bnet,x,y):
    s=pcbnew.FootprintLoad(BTN,"Panasonic_EVQPUJ_EVQPUA"); s.SetReference(ref); s.SetValue("TACT")
    b.Add(s); s.SetPosition(pcbnew.VECTOR2I(FM(x),FM(y)))
    pads=list(s.Pads())               # 2-circuit tactile: 2 electrical nodes (4 pads)
    for p in pads:
        p.SetNet(net(a if p.GetNumber() in ('1','2') else bnet))
    return s
add_btn("SW2","NRST","GND",27.0,60.0)     # RESET: NRST<->GND
add_btn("SW3","BOOT0","SYS_3V3",30.0,60.0) # BOOT0<->3V3 (R22 holds it low normally)
b.Save('/tmp/work.kicad_pcb')
```

- [ ] **Step 2: Verify**

Assert `SW2` bridges `NRST`/`GND`, `SW3` bridges `BOOT0`/`SYS_3V3`; `BOOT0` still
has `R22` + `U1.94`; 0 new overlaps; DRC clean (except accepted). Nudge buttons if
they overlap (the SWD J7 is nearby — keep ≥0.3 mm).

- [ ] **Step 3: Commit**

```bash
cp /tmp/work.kicad_pcb kicad/...kicad_pcb && git add -A && \
git commit -m "feat(pcb): add RESET + BOOT0 tactiles for USB-DFU flashing"
```

---

### Task 3: Group the UART console pads

**Files:** Modify `BRD`.

- [ ] **Step 1: Cluster TX/RX/GND**

```python
import pcbnew
FM=pcbnew.FromMM
b=pcbnew.LoadBoard('/tmp/work.kicad_pcb')
TP="/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints/TestPoint.pretty"
def net(n):
    x=b.FindNet(n); return x if x else (lambda nn:(b.Add(nn) or nn))(pcbnew.NETINFO_ITEM(b,n))
# relocate existing TX/RX test points into a tight inline row + add a UART GND pad
tx=b.FindFootprintByReference('TP_UART_TX'); rx=b.FindFootprintByReference('TP_UART_RX')
bx,by=20.5,64.5
tx.SetPosition(pcbnew.VECTOR2I(FM(bx),FM(by)))
rx.SetPosition(pcbnew.VECTOR2I(FM(bx+1.6),FM(by)))
g=pcbnew.FootprintLoad(TP,"TestPoint_Pad_D1.0mm"); g.SetReference("TP_UART_GND"); g.SetValue("GND")
b.Add(g); g.SetPosition(pcbnew.VECTOR2I(FM(bx+3.2),FM(by)))
for p in g.Pads(): p.SetNet(net('GND'))
b.Save('/tmp/work.kicad_pcb')
```

- [ ] **Step 2: Verify** — TX/RX/GND within ~3.5 mm of each other, nets intact, 0
  overlaps, DRC clean. Nudge `bx,by` to a clear spot if needed.

- [ ] **Step 3: Commit** — `git commit -m "feat(pcb): group UART console pads (TX/RX/GND)"`

---

### Task 4: Per-rail current-sense jumpers (TROPIC01, NFC; OPTIGA if clean)

**Files:** Modify `BRD`. Inserting a series 0 Ω splits a rail: the load-switch
side keeps the old net; a NEW net feeds the IC + its decoupling; the jumper bridges
them.

- [ ] **Step 1: Split TROPIC + NFC rails and add 0 Ω jumpers**

```python
import pcbnew
FM=pcbnew.FromMM
b=pcbnew.LoadBoard('/tmp/work.kicad_pcb')
RES="/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints/Resistor_SMD.pretty"
def net(n):
    x=b.FindNet(n); return x if x else (lambda nn:(b.Add(nn) or nn))(pcbnew.NETINFO_ITEM(b,n))
def split(old,newname,load_refs,x,y,jref):
    # move every pad on `old` EXCEPT the load-switch outputs onto `newname`
    for f in b.GetFootprints():
        for p in f.Pads():
            if p.GetNetname()==old and f.GetReference() not in load_refs:
                p.SetNet(net(newname))
    j=pcbnew.FootprintLoad(RES,"R_0402_1005Metric"); j.SetReference(jref); j.SetValue("0R")
    b.Add(j); j.SetPosition(pcbnew.VECTOR2I(FM(x),FM(y)))
    pp={p.GetNumber():p for p in j.Pads()}; pp['1'].SetNet(net(old)); pp['2'].SetNet(net(newname))
split('TROPIC_VCC_SW','TROPIC_VCC',('U4',),  44.0,55.0,'RJ1')  # load switch U4 keeps TROPIC_VCC_SW
split('NFC_VCC_SW',  'NFC_VCC',  ('U13',), 44.0,57.0,'RJ2')   # load switch U13 keeps NFC_VCC_SW
b.Save('/tmp/work.kicad_pcb')
```

- [ ] **Step 2: Verify** — `TROPIC_VCC_SW` now only on U4 + RJ1.1; `TROPIC_VCC` on
  U2 pins + caps + RJ1.2 (same total pad count as before, minus one, plus jumper);
  likewise NFC. Net-island check: each rail still electrically one node *through*
  the jumper. 0 overlaps; DRC clean. Nudge jumper xy if overlapping.

- [ ] **Step 3 (conditional): OPTIGA** — find U11's decoupling cap on `SYS_3V3`
  (the 100 nF nearest U11). If exactly one cap, split: move `U11.10` + that cap onto
  `OPTIGA_VCC`, add `RJ3` 0 Ω bridging `SYS_3V3`↔`OPTIGA_VCC`. If the decap is
  ambiguous/shared, **skip OPTIGA** and note it (don't risk mis-cutting 3V3).

- [ ] **Step 4: Commit** — `git commit -m "feat(pcb): add current-sense 0R jumpers on secure-element rails"`

---

### Task 5: GPIO/SPI edge breakout (optional — fit what the edge allows)

**Files:** Modify `BRD`. No castellated footprint ships with KiCad, so use a row
of edge **SMD pads** (poor-man's breakout) on the longest free edge segment.

- [ ] **Step 1: Find the longest clear edge segment** (scan each board edge for a
  gap with no courtyard within 2 mm). Record its start/length.

- [ ] **Step 2: Add an N-pad SMD row** along that segment (1.27 mm pitch), exposing
  in order: `SYS_3V3`, `GND`, `EXP_SPI_SCK`, `EXP_SPI_MOSI`, `EXP_SPI_MISO`,
  `EXP_SPI_CSN`, then up to 3 spare STM32 GPIOs (pick from the documented free pads
  list; assign their nets as `EXP_GPIO0..2`). Use `TestPoint_Pad_D1.0mm` per pad,
  reference `J8` group / `TP_EXP*`. Stop when the segment is full.

```python
# pseudo-concrete: place k pads at (x0 + i*1.27, y_edge), each TestPoint_Pad_D1.0mm,
# nets = the ordered list above truncated to k. New GPIO nets also added to U1's
# chosen free pads (physical pins from the 36-free list), marked datasheet-pending.
```

- [ ] **Step 3: Verify** — pads on the edge, on correct nets, 0 overlap, DRC clean.
  If the longest free segment is < ~6 mm (fits < 4 pads), **reduce to power+SPI
  only or skip**, and record the decision.

- [ ] **Step 4: Commit** — `git commit -m "feat(pcb): add edge breakout (power/SPI/GPIO) — space-limited"`

---

### Task 6: Fourth/extra mounting holes (verify — may not fit)

**Files:** Modify `BRD`.

- [ ] **Step 1: Probe the top corners** for a clear ⌀2.2 mm M2 hole + keepout near
  (12, 36) and (51, 36), avoiding J6/J9/ANT1/battery space.
- [ ] **Step 2:** If clear, add `MH3`,`MH4` (`MountingHole_2.2mm_M2`, NPTH). If not,
  **record "does not fit"** and move on (no change).
- [ ] **Step 3: Verify** 0 overlap + DRC; **Commit** if changed.

---

### Task 7: Silk labels, contracts/docs, final verification

**Files:** Modify `BRD`, `production/netlist-contract.json`,
`production/pinmux-ledger.json`, `design-notes/component-decisions.md`,
`design-notes/mechanical-architecture.md`.

- [ ] **Step 1: Silk** — ensure visible references for `J7` (SWD), `SW2` (RST),
  `SW3` (BOOT0), the UART group, jumpers, breakout; add a short silk caption where
  space allows ("SWD","RST","BOOT","UART"). (Full legibility pass is post-routing.)
- [ ] **Step 2: Contracts** — add to `netlist-contract.json`: a `debug` bus
  (`SWDIO,SWCLK,NRST,SWO?`), `uart_console`, `current_sense` (TROPIC_VCC/NFC_VCC/
  OPTIGA_VCC), `edge_breakout` (EXP_SPI_*, EXP_GPIO0..2). In `pinmux-ledger.json`
  add an `edge_breakout` note with the physical pins used and
  `status: mcu_pinmux_pending_datasheet`. Validate JSON parses.
- [ ] **Step 3: Docs** — update `component-decisions.md` (dev-access section) and
  `mechanical-architecture.md` (note the dev controls vs single user button).
- [ ] **Step 4: Final verify** — `KCLI pcb drc` (expect only USB-C edge + silk),
  net-integrity (no unintended single-pad nets beyond `TFT_SPI_MISO`), render
  front+back (back still only `J2`).
- [ ] **Step 5: Commit** — `git commit -m "feat(pcb): silk + contracts/docs for reference dev-access features"`

---

## Self-review notes (spec coverage)

- Spec A (SWD) → Task 1. B (RESET/BOOT0 USB-DFU) → Task 2. C (UART) → Task 3.
  D (silk) → Task 7. E (breakout) → Task 5. F (current sense) → Task 4.
  G (4 mounts) → Task 6. H (lanyard) → deferred (enclosure), out of scope.
- All new MCU pins (breakout GPIOs) are datasheet-pending (Task 5/7) — respects the
  no_llm_invented_pin_numbers gate.
- Space risk: Tasks 5 and 6 are explicitly conditional and self-report if they
  don't fit; must-haves (1–3) come first.
