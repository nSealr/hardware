# TROPIC01 Universal Secure Device — Single-FFC Display Swap + Custom-Board Cleanup

Date: 2026-06-10
Status: design approved, implementation in progress
Board: `pcb/tropic01-universal-secure-device` (Rev A0)
Branch: `tropic01-product-implementation`

## Problem

Two unrelated cleanups for the Rev A0 board before routing starts:

1. **Display connector.** The frozen panel (Newhaven `NHD-2.4-240320AF-CSXP-CTP`)
   exposes display and capacitive touch on **two separate flex cables**, so the
   board carries two connectors: `J2` (Molex 54132-4062, 40-pin 0.5 mm, display)
   and `J2B` (Molex 52271-0679, 6-pin 1.0 mm, touch). A single-FFC panel is more
   standard, simpler to source, and removes a connector and a custom footprint.

2. **Deprecated custom board.** The repository still contains the deprecated
   standalone PCB project `pcb/custom-persistent-secret-wallet/`. The final
   product is the single `tropic01-universal-secure-device`.

Routing has not started, so changing the connector now is cheap (it only touches
the schematic-intent generators, not copper).

## Decision 1 — Panel: BuyDisplay/EastRising ER-TFT024IPS-3

A 2.4" IPS 240×320 panel whose display **and** capacitive touch are carried on a
**single 50-pin, 0.5 mm pitch, top-contact FFC**.

Evidence (datasheet `ER-TFT024IPS-3_Datasheet`, Rev 1.0 Feb-2022):

- §2.1: "FPC Connector: 50 Pin, 0.50mm Pitch, SMD Horizontal Type Top contact".
- §2.3: controller ST7789V; interface 8080 8/9/16/18-bit parallel, 3/4-wire
  serial SPI, RGB.
- §4.1 pin table: pins **44–47 are dual-purpose** —
  `XR(X+)/SCL`, `YD(Y+)/SDA`, `XL(X-)/INT`, `YU(Y-)/RESET`, documented as
  "Capacitive touch SCL/SDA/INT/RESET, I2C interface". This is the key fact:
  **display + capacitive touch share one FFC.**
- Capacitive touch panel option is order code `ER-TPC024-1`, controller FT6336.
- §4.3: VCI/VDDI operating 2.5–3.3 V (typ 2.8 V); 3.3 V is within spec.
- §4.4 backlight: 4 parallel LED strings, Vf 3.2 V, 80 mA total at 4×20 mA.

### Frozen interface (replaces the Newhaven mapping)

Single connector `J2`, 50-pin FFC. Net names on the STM32 side are **unchanged**,
so the STM32U585 pinmux does not move; only the connector pin map changes.

| FFC pin(s) | Panel signal | Net | Notes |
| --- | --- | --- | --- |
| 1 | LEDA | `TFT_BACKLIGHT_A` | backlight anode |
| 2–5 | LEDK1–LEDK4 | `TFT_BACKLIGHT_K` | 4 cathodes tied; driven by CC/PWM |
| 6–9 | IM0–IM3 | strap | **IM3:IM2:IM1:IM0 = 1110** → 4-wire 8-bit Serial Interface II (SCL, SDI, D/CX, SDO, CSX) |
| 10 | RESET | `TFT_RST` | |
| 11–14 | VSYNC/HSYNC/DOTCLK/DE | NC | RGB-only, unused in SPI |
| 15–32 | DB17–DB0 | NC | parallel data, unused in SPI |
| 33 | SDO | `TFT_SPI_MISO` | |
| 34 | SDI | `TFT_SPI_MOSI` | |
| 35 | RD | NC | |
| 36 | WRX(D/CX) | `TFT_DC` | data/command in serial mode |
| 37 | D/CX(SCL) | `TFT_SPI_SCK` | serial clock |
| 38 | CSX | `TFT_CS` | |
| 39 | TE | `TFT_TE` (optional) | tearing-effect to MCU GPIO; NC acceptable |
| 40,41 | VDDI | `DISPLAY_VCC_SW` | interface rail |
| 42 | VCI | `DISPLAY_VCC_SW` | logic rail |
| 43,48–50 | GND | `GND` | |
| 44 | XR(X+)/SCL | `TOUCH_I2C_SCL` | capacitive touch I2C |
| 45 | YD(Y+)/SDA | `TOUCH_I2C_SDA` | capacitive touch I2C |
| 46 | XL(X-)/INT | `TOUCH_INT` | active-low |
| 47 | YU(Y-)/RESET | `TOUCH_RST` | active-low |

### Component-freeze changes

- `DISP1`: Newhaven `NHD-2.4-240320AF-CSXP-CTP` → **ER-TFT024IPS-3** (2.4" IPS
  240×320, ST7789V + FT6336 capacitive on one FFC).
- `J2`: single **50-pin 0.5 mm top-contact FFC/FPC** connector. Use a
  KiCad-shipped `Connector_FFC-FPC` footprint (e.g. Hirose `FH12-50S-0.5SH`
  class, top-contact) so no custom footprint is needed.
- **Remove `J2B`** entirely (the 6-pin touch connector).
- Retire the custom `nSealr_Display.pretty` Molex footprints (54132-4062,
  52271-0679); they are no longer referenced.
- Touch controller noted as FT6336 (was FT5426); same I2C bus, re-verify the I2C
  address in firmware.

### Out of scope / remaining gates (unchanged by this change)

- PCB routing, fresh DRC, PCBWay release (board stays `blocked`).
- Backlight LED driver final selection (CC boost vs sink + PWM on
  `TFT_BACKLIGHT_PWM`); 3.3 V vs dedicated 2.8 V display rail is a margin choice.
- 3D model for the 50-pin FFC; retire the 6-pin model.
- NFC antenna/matching first-article tuning.
- Actual `.kicad_pcb` footprint placement of the new `J2` (KiCad GUI step after
  regeneration).

## Decision 2 — Cleanup scope (corrected after investigation)

**Important finding:** the name "custom" survives in two different forms, and
only one is deprecated.

- **Deprecated, safe to remove:** the standalone PCB project directory
  `pcb/custom-persistent-secret-wallet/`. On this branch it is already an empty
  directory (0 files); on `main` it still has a stub `requirements.json`.
- **NOT deprecated — keep:** the `custom_hardware_wallet` route and
  `custom_hardware_persistent` custody are the **persistent-signer contract of
  the final tropic01 board**. Evidence:
  - `pcb/tropic01-universal-secure-device/requirements.json` requires referencing
    route `custom_hardware_wallet` and custody `custom_hardware_persistent`.
  - `scripts/validate_hardware.py` maps `tropic01_universal_secure_device` to
    include `custom_hardware_wallet`, `custom_hardware_persistent`,
    `policy-manual-only-persistent-device`.
  - The spec-vector fixtures (`accounts/`, `grants/`, `custody/`, `policies/`,
    `policy-changes/`, `route-selections/`) exercise that contract.

The old custom board was **absorbed into** tropic01 as its persistent-signer
role. Removing the `custom_hardware_wallet` fixtures/contract would break the
final board's own requirements and the test suite.

**Action:** remove only `pcb/custom-persistent-secret-wallet/`. Leave the
`custom_hardware_wallet` contract and fixtures intact.

## Implementation approach

The schematic intent is generated by pure-Python scripts and validated by the
test suite — no KiCad runtime needed for the intent. Apply the display change at
the source and regenerate:

1. Edit the source-of-truth scripts:
   `materialize_tropic01_universal_pinmux_ledger.py`,
   `materialize_tropic01_universal_schematic_binding.py`,
   `materialize_tropic01_universal_net_contract.py`,
   `materialize_tropic01_universal_kicad_schematics.py`,
   `materialize_tropic01_universal_placement.py`, and
   `scripts/validate_hardware.py` — replace the Newhaven J2 + J2B definitions
   with the single ER-TFT024IPS-3 J2 mapping above.
2. Regenerate artifacts (binding, net contract, pinmux ledger, schematics,
   placement, PCBWay BOM/manifest) by running the scripts.
3. Update prose design notes: `component-freeze.md`, `datasheets.md`,
   `pinmux.md`.
4. Update tests in `tests/test_validate_hardware.py` to assert the new panel,
   single FFC, no `J2B`, and FT6336.
5. Remove `pcb/custom-persistent-secret-wallet/`.

## Verification

- `make test` (verify_repo + 79+ unittests) green.
- `schematic-coverage.json` stays `required_refs_bound`.
- `pcbway-manifest.json` stays `blocked` (board not routed) — expected.
- `git grep` confirms no remaining reference to `J2B`, Molex 54132/52271, NHD-2.4,
  or FT5426 in the tropic01 board sources.
