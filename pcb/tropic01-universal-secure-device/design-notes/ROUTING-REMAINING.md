# Routing — remaining work (finish in KiCad's interactive router)

Date: 2026-06-11
Status: **~96% auto-routed.** The design, placement and 6-layer stackup are
complete and committed. This document lists exactly what is left so the board
can be finished in KiCad's interactive (push-and-shove) router and taped out.

## Two board files

- `kicad/tropic01-universal-secure-device.kicad_pcb` — **clean foundation**
  (placement + 6-layer + GND planes, 0 tracks, DRC-clean). The canonical board.
- `kicad/tropic01-universal-secure-device-WIP-routing.kicad_pcb` — the
  **~96% auto-route** to finish from (1096 tracks, 230 vias). Open this one to
  complete the routing; it already contains all the work below except the items
  listed here.

## Why this is a manual step

The board is dense (90 parts, fine-pitch ICs, 4 signal layers). Freerouting +
a custom A* router (pin-escape, dog-leg fanout, smoothing, multi-pin MST) got to
~96%. The remainder are **boxed-in fine-pitch IC pins** whose escape channels are
occupied by neighbour traces — connecting them requires *rip-up & retry*, which
the interactive router does and scripts cannot do cleanly. Budget ~½ day.

## 1. Unrouted signal nets (8 connections)

Use **Route → Route Single Track** (X). Each is a short point-to-point; the
ratsnest airwire shows it.

| Net | From | To | Note |
| --- | --- | --- | --- |
| `TROPIC_SPI_MOSI` | U2.5 (TROPIC01) | U1.32 (STM32) | TROPIC01 SPI; pins 5/6 are the tight 0.4mm-pitch cluster — fan out to In2/In3 with a via just outside the QFN |
| `TROPIC_SPI_MISO` | U2.6 | U1.31 | same cluster as MOSI |
| `NFC_IRQ` | U9.27 (ST25R3916B) | U1.81 | route on In2/In3 |
| `TOUCH_I2C_SCL` | U1.95 | J2.44 (FFC) | the four touch nets are adjacent on both ends — route as a bus on one inner layer |
| `TOUCH_I2C_SDA` | U1.96 | J2.45 | |
| `TOUCH_RST` | U1.97 | J2.47 | |
| `TOUCH_INT` | U1.98 | J2.46 | |
| `DISPLAY_VCC_SW` | U14.5/6 | J2.7,8,9,40,41,42 | display power; widen to ~0.3mm, connect the FFC VCI/VDDI pins to U14 VOUT |

Tip: route the TROPIC01 SPI pair and the touch bus on **In3** (least congested),
dropping a via just outside each IC. Keep TROPIC01 SPI short and away from the
NFC analog/RF area.

## 2. Unconnected GND pins (~12)

These are GND pins boxed in by their IC's own fine-pitch pins (the F/B copper
pours + In1/In4 planes cannot reach them, and a normal via won't fit at pitch).
KiCad shows them as GND airwires. Finish with **via-in-pad** (set a 0.3/0.15mm
via — the project rule already allows down to 0.4mm; bump it to 0.3mm in
Board Setup → Constraints if you use 0.3mm, and request via-in-pad fill at the
fab) or a short trace into the chip's exposed pad:

- **U1 (STM32U585) VSS** pins 27, 49, 74 — via-in-pad to the In1 plane.
- **U2 (TROPIC01) QFN GND** pins 2, 3, 12, 23, 30, 31 + the exposed pad — short
  traces into the EP (already via-stitched), or via-in-pad.
- **U9 (ST25R3916B) GND** pins 6, 16, 26 — into its EP / via-in-pad.
- **U10 (BQ24074), U3 (TPS62840), U4 GND** pins and a few bypass-cap GND pads —
  via-in-pad where a 0.4mm via fits, else into the nearest EP.

The exposed pads of U2/U9/U11 already have thermal via arrays to the planes, so
routing a perimeter GND pin to its own EP grounds it.

## 3. DRC violations to resolve (~42)

`kicad-cli pcb drc` on the WIP board reports ~42 real items, mostly:

- **30 clearance** — a few auto-routed signal traces sit too close (notably
  `SE2_RST` vs `SE2_I2C_SCL` near U11, and some GND stitch traces). Nudge/re-route.
- **4 shorting_items** — GND stitch vias/traces grazing a signal pad/track; move
  the via or re-route the short segment.
- **3 copper_edge_clearance** — J1 USB-C shield + SW1 button pads at the board
  edge (inherent to edge-mounted parts; add a small local outline notch or accept,
  PCBWay handles it).
- **3 track_dangling / 1 hole_to_hole / 2 silk** — trim dangling stubs, space the
  one hole pair, move the 2 silk labels off pads.

Run DRC, fix, repeat until clean.

## 4. Fab spec (for PCBWay)

- 6-layer, stackup **F.Cu(sig) / In1(GND) / In2(sig) / In3(sig) / In4(GND) / B.Cu(sig)**.
- Min via relaxed to **0.4/0.2mm** (set in the project; standard PCBWay capability).
  If you use 0.3mm via-in-pad for GND, request **via fill + cap**.
- Board outline 44.1 × 42.1 mm; 2× M2 mounting holes (bottom corners).
- Trace/space 0.2/0.2 mm. GND: 2 inner planes + F/B pours + stitching vias.

## 5. After routing is clean

1. `Edit → Fill all zones` (B).
2. DRC = 0 (excluding the inherent edge-mounted-connector clearances).
3. `File → Fabrication Outputs → Gerbers` (all 6 copper + mask + silk + edge) and
   **Drill Files**.
4. Pick-and-place (`.pos`) + BOM for assembly.
5. Zip and upload to PCBWay; flag the 6-layer stackup and any via-fill request.
