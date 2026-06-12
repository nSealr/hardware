# Routing — remaining work (finish in KiCad's interactive router)

Date: 2026-06-12
Board: `kicad/tropic01-universal-secure-device.kicad_pcb` —
**42.87 × 36 mm, 4-layer** (F.Cu signal / In1 GND plane / In2 signal / B.Cu signal),
clean placement, **0 tracks** (canonical foundation).

## Status

The design, placement, stackup and all mechanical constraints are **done and
committed**. Routing is the remaining step. Extensive automated routing
(Freerouting + a custom A* pipeline) was explored: it reaches **~96%** but cannot
produce a clean, fully-connected, DRC-clean result on this density. The last
**~17 connections** plus a clean ground fill need the **interactive (push-and-shove)
router** — this is normal for a dense, display-sized board.

Key facts established by the exploration (so they are not re-litigated):
- **4 layers route as well as 6** here — the bottleneck is fine-pitch IC
  pin-escape congestion, not layer count. (6→4 already applied; saves cost.)
- **Placement is not the bottleneck** — a pin-aware re-placement (STM32 rot270 for
  a short USB pair, peripherals at the MCU pin clusters) routes to the *same* ~17.
  The committed placement is kept for simplicity.
- USB is **Full-Speed** (STM32U585) → routing length is forgiving.

## How to finish (≈½ day, or a contractor)

1. **Open** the board in KiCad PCB editor.
2. **Auto-route the bulk first** (optional head-start): Tools → External Plugin →
   export Specctra DSN, run Freerouting (`java -jar freerouting.jar -de board.dsn
   -do board.ses -mp 100`), import the SES. This routes ~96% in one shot.
   (Skip if you prefer to hand-route everything.)
3. **Finish the ~17 cross-board nets** by hand (Route → X). They are:

   | Net | note |
   | --- | --- |
   | `TROPIC_SPI_SCK/CSN/MISO/MOSI`, `TROPIC_GPO` | TROPIC01↔STM32 secure SPI (U2 is adjacent to U1); pins 5/6 are the tight 0.4mm fanout |
   | `NFC_SPI_MISO`, `NFC_IRQ` | NFC controller U9 ↔ STM32 |
   | `SE2_I2C_SCL` | OPTIGA U11 ↔ STM32 |
   | `TOUCH_RST` | display FFC J2 ↔ STM32 |
   | `TROPIC_VCC_SW` (4), `VBUS` (3), `NFC_VDD_RF` | power nets — widen to ~0.3–0.4mm |

4. **Ground fill** (the clean way, in GUI): add a GND zone on **F.Cu and B.Cu**
   (the In1 GND plane is already there); fill (`B`); then add **stitching vias**
   from the F/B pours to the In1 plane (a grid + one next to each IC GND pad and
   under the exposed pads of U2/U9/U11). Min via is relaxed to **0.4/0.2 mm** in
   the project rules.
5. **DRC** → 0 (excluding the inherent edge-mounted-connector clearance on the
   USB-C/button); fix clearances/dangling as flagged; tidy silkscreen.

## Fabrication (PCBWay) once routing is clean

1. Fill zones (`B`).
2. File → Fabrication Outputs → **Gerbers** (F.Cu, In1, In2, B.Cu + mask + silk +
   Edge.Cuts) and **Drill files**.
3. **Pick-and-place** (`.pos`) + **BOM** for assembly.
4. Zip → upload; flag the **4-layer** stackup (~1.6mm) and the 0.2mm min drill.
