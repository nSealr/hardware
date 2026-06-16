# Deep Audit Findings — nSealr TROPIC01 board (2026-06-16)

Source of pin data: official KiCad symbol `MCU_ST_STM32U5.kicad_sym` →
`STM32U585VITx` (LQFP100), cross-validated against `production/pinmux-ledger.json`
anchors (pin1=PE2, pin2=PE3, pin86=PD5, pin87=PD6, pin81=PD0, pin94=PH3) — all match.
The datasheets ARE all cited in the contracts (STM32U585 DS13086 r10, ST25R3916B
DS13541 r11, TROPIC01, OPTIGA Trust M, ER-TFT024IPS-3, GCT USB4105, AN5276).

## CRITICAL — real netlist bugs (from the contract, not layout)
1. **VCAP shorted to a signal.** STM32 pin 48 = **VCAP** (internal LDO core
   regulator output — must connect ONLY to a dedicated ~4.7 µF cap to GND) was
   wired to **EXP_I2C_SDA**. This corrupts the MCU core supply AND the I2C bus →
   MCU will not run. **Net un-shorted** (pin48→new VCAP net; EXP_I2C_SDA moved to
   pin60=PD13, a valid I2C4_SDA pin). **BUT the 4.7 µF VCAP cap could not be placed**
   — the board is saturated (no footprint-free spot within 13 mm of pin 48). VCAP
   therefore still has no decoupling → still non-functional until re-laid-out.

2. **I2C peripheral over-subscription (pinmux conflict).** Three I2C buses, but the
   chosen pins collectively support only two usable instances:
   - TOUCH (PB8/PB9) = **I2C1 only**.
   - OPTIGA/SE2 (PB6/PB7) = I2C1 or **I2C4**.
   - EXP/Qwiic (PB10 + SDA) = I2C2 (no free I2C2_SDA pin) or **I2C4**.
   With TOUCH locked to I2C1, both SE2 and EXP need I2C4 → impossible. One bus must
   move to pins on a free instance (I2C2/I2C3) — a **CubeMX pinmux re-solve**, which
   relocates pins and thus the layout.

## STM32 power architecture — mostly OK
- VDD(11,28,50,75,100)→SYS_3V3 ✓, VSS(10,27,49,74,99)→GND ✓, VBAT(6)→3V3 ✓,
  VDDA(22)→3V3, VSSA(19)→GND, VREF+(21)→3V3, VREF-(20)→GND, VDDUSB(73)→3V3 ✓.
- This LQFP100 uses the **LDO (VCAP pin 48)** — no SMPS inductor pins bonded.
- The 34 "unconnected" STM32 pads are **unused GPIO** (legitimate) — NOT power pins.
- Added earlier: **9× 100 nF local decoupling (C50–C58) at 1.9–3.5 mm from the VDD pins.**
- Improvements still wanted (functional without, better with): VDDA via ferrite +
  1 µF/10 nF; dedicated VREF+ cap.

## Other ICs — unconnected pads (need per-datasheet classification = schematic/ERC)
U2 TROPIC 19/37, U9 NFC 19/42 (incl. tuning-gated antenna pins), U11 OPTIGA 5/11,
U10 4, U7 4 (unused ESD channels), U3 2 (thermal). Mix of legitimate NC/thermal vs
possibly-missing — cannot classify without each symbol's pin functions (ERC territory).

## MAJOR — other
- **Power traces all 0.2 mm** (auto-router default) — undersized for the ~0.5–0.7 A
  charge path. Must be widened via a wider power **net-class + re-route** (post-route
  widening gives 192 clearance violations — too tight).
- **Routing ~84%** — 29 nets need the interactive push-and-shove router.

## Root cause + recommendation
The board was generated from a **partial, unverified netlist contract** (signal pins
only); the schematic is a **stub**, so **no ERC ever ran** — which is why the VCAP
short and the I2C conflict slipped through, and why power/NC pins are unresolved.
The board is also **capacity-limited**: even after enlarging to 39.8 mm, critical
parts (the VCAP cap) don't fit post-hoc.

**These issues are systemic, not incrementally board-fixable.** The correct path is
**schematic-first**: capture the full schematic using the cited datasheets and KiCad
symbols (which carry pin functions), resolve the pinmux in **CubeMX** (I2C instances,
VCAP, VDDA/VREF), run **ERC**, then do a fresh layout (which will have room reserved
for VCAP + proper power net-classes from the start).

## What was fixed at board level (committed)
- Board enlarged 36.8→39.8 mm; **9× STM32 decoupling** added.
- **USB-C** front posts brought on-board (no edge breakout); rounded corners + 4 holes.
- 3 redundant test points removed; UART grouped; RGB LED off the edge.
- Routing ~84%, GND plane solid, DRC = 0 (except the intentional WIP unrouted nets).
- VCAP net un-shorted (cap placement + I2C re-solve deferred to the schematic-first pass).
