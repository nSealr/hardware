# TROPIC01 Universal Secure Device — Clean Rebuild (no technical debt)

Date: 2026-06-10
Status: design foundation; build proceeds subsystem by subsystem.
Supersedes: the board-B scaffold for the electrical design (connectivity is rebuilt
from scratch). Mechanical concept and component freeze are carried over.

## Why rebuild

Board B accumulated technical debt that any further patching keeps fighting:
incomplete scaffold schematic (212 ERC), non-standard name-only net format,
inherited manual placement, undesigned NFC RF front-end (DNC pins), library
mismatches. A clean rebuild gives a **complete, correct netlist from the start**,
which is the root fix for routability (the 46 unrouted nets were a symptom of
incomplete connectivity, not the router).

## Method (no-debt, deterministic)

The electrical design is rebuilt in the **schematic binding** (the project's
source of truth), making it **complete**: every pin of every component is bound
to its correct net, datasheet-driven, with power flags. Each subsystem is taken
to **ERC-clean before moving on**. Then: connectivity-driven placement → 4-layer
routing → DRC → PCBWay package.

## Component freeze (carried over)

| Ref | Part | Role |
| --- | --- | --- |
| U1 | STM32U585VIT6 (LQFP100) | host MCU |
| U2 | TROPIC01 TR01-C2P-T301 (QFN32) | primary secure element |
| U11 | OPTIGA Trust M SLS32AIA (USON-10) | second secure element |
| U9 | ST25R3916B-AQET (QFN32) | NFC/RFID front-end |
| U5 | W25Q128JV (SOIC-8) | QSPI NOR flash |
| U10 | BQ24074 (VQFN-16) | LiPo charger + power path |
| U3 | TPS62840 | 3.3 V buck |
| U4 | TPS22917 | TROPIC01 load switch |
| J1 | GCT USB4105-GF-A | USB-C 2.0 receptacle (edge) |
| J2 | 50-pin 0.5 mm FFC | display (ER-TFT024IPS-3): SPI + touch I2C |
| J6 | JST SM04B-SRSS-TB | Qwiic/STEMMA I2C expansion |
| J9 | JST S2B-PH-SM4-TB | LiPo connector (battery off-board) |
| SW1 | EVQP7C | single side button |
| DISP1 | ER-TFT024IPS-3 | 2.4" IPS display (off-board envelope) |

## Stackup (the routing lesson)

4-layer: **F.Cu (signal) / In1.Cu (GND plane) / In2.Cu (signal) / B.Cu (signal)**.
This gives **3 signal layers + 1 solid GND reference** — enough to route this
density (board B failed with only 2 signal layers). The GND plane under the NFC
loop and USB/SPI is kept for signal integrity.

## Mechanical concept (carried over)

Device = display size (~42.7 × 59.5 mm). Front = display; behind it, lower
portion = PCB (~44 × 36 mm), upper portion = battery. Components on the PCB
back-facing side (toward the case back); display mates on the other side. NFC
antenna loop on the back, top-center; tap on the back. Battery off-board (only
J9). One physical button + touch.

## Subsystem build order (each ERC-clean before next)

1. **Power tree**: USB-C VBUS + CC pulldowns + D+/D- ESD; BQ24074 charger +
   power-path (VBUS/BAT/SYS) + ISET/ILIM/status; TPS62840 buck → +3V3; TPS22917
   load switch → +3V3_TROPIC; bulk + decoupling; PWR_FLAG on every rail.
2. **STM32U585**: full pinout — power pins + per-pin decoupling, VBAT, NRST,
   BOOT0, the SWD port, the HSE crystal + load caps, USB D+/D-, and every
   peripheral net from the pinmux ledger.
3. **TROPIC01**: SPI1 to the MCU, power-cycle control via the load switch, GPO,
   decoupling, NU-pin policy.
4. **OPTIGA Trust M**: I2C4 + reset + pull-ups + decoupling.
5. **ST25R3916B NFC**: SPI2, crystal, supplies/decoupling, and the **full RF
   front-end** (RFO1/RFO2 → EMC L0/C0 → matching Cs/Cp → back-side loop →
   RFI1/RFI2 divider), with starting values flagged `tuning_required`.
6. **QSPI flash**: OCTOSPI bus + decoupling.
7. **Display**: the 50-pin FFC — SPI, touch I2C with pull-ups, backlight LED
   driver + PWM, IM straps (4-wire Serial Interface II), power.
8. **Controls / debug**: SW1, status LED + resistor, the SWD/UART/power test
   pads, expansion J6.

## Verification gates

- Per subsystem: KiCad ERC clean (no unconnected/undriven on that subsystem).
- Whole board: ERC clean → placement → DRC clean (exclude intentional edge
  USB-C) → routing 0 unrouted → PCBWay manifest unblocked.
- First-article NFC RF tuning remains the only measurement gate.
