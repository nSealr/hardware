# Schematic ERC Remediation

Status: schematic ERC clean; still blocking before PCBWay or release-candidate
claims because PCB routing and fresh DRC evidence are missing.

The current KiCad schematic is still a generated source-backed scaffold. It
binds selected component pins to named nets, but it does not yet implement all
real circuits, power symbols, no-connect decisions, pull networks, or
hierarchical sheet pins required for ERC-clean production review.

## Current Evidence

- KiCad ERC on 2026-06-09 reports 0 violations after source-backed binding
  remediation.
- The generated `production/erc/triage.json` is the authoritative violation
  breakdown for this revision.
- Historical context: an earlier scaffold reported 213 violations, and a tested
  attempt to move generated wires from the pin `(at ...)` coordinate to the
  apparent pin endpoint increased ERC from 213 to 487 violations. Do not repeat
  that change without a minimal KiCad reproduction proving the endpoint model.
- Tropic Square reference devboards in `.cache/external-repos/tropicsquare-devboards`
  use actual circuit wiring with local labels and junctions around TROPIC01,
  not only global-label stubs. Rev A0 should follow that pattern.

## Root Cause

The generated sheets now place core symbols, source-backed support passives,
test pads, power flags, and explicit no-connects for the current Rev A0
schematic. Earlier scaffold-only sheets attached short wires plus labels to
only the source-backed pins from `schematic-binding.json`; KiCad correctly
reported:

- pins from full MCU/display/USB symbols that have no explicit connection or
  no-connect decision;
- power pins without a driven power source/PWR_FLAG/power symbol;
- USB-C CC/SBU/shield pins without the required Rd, shield, ESD, or no-connect
  circuit;
- display, NFC, TROPIC01, and STM32 pins that need real support components,
  not only net labels;
- footprint-link warnings for generic connector symbols that must become
  source-backed connector symbols or accepted custom symbols.

## Completed ERC Fixes

- `power_usb.kicad_sch`: USB-C support, USB ESD, VBUS current limiting,
  BQ24074 charger/PowerPath programming passives, TPS62840 3.3 V VSET resistor,
  USB VBUS sense network, and power flags are materialized.
- `stm32u5_host.kicad_sch`: STM32U5 power/analog pins, reset/BOOT0 strap
  passives, SWD pins, HSE, USB, display, TROPIC01, NFC, OPTIGA, QSPI, and
  expansion assignments are materialized from the pinmux ledger.
- `tropic01.kicad_sch`: TROPIC01 VCC/GND/SPI/GPO pins, official
  pull-up/pull-down pad policy, load switch, CT capacitor, and local decoupling
  are materialized.
- `display_controls.kicad_sch`: TFT/touch connectors, display mode pins,
  backlight driver support parts, side button, side LED, and display load
  switch CT capacitor are materialized.
- `secure_element_2.kicad_sch`: OPTIGA Trust M pin subset and I2C pull-ups are
  materialized.
- `optional_profiles.kicad_sch`: ST25R3916B power/SPI/IRQ/crystal pin subset,
  NFC load switch, CT capacitor, crystal loads, and hidden test pads are
  materialized. Antenna matching values remain measurement-gated.

## Remaining Fix Order

1. `storage_expansion.kicad_sch`
   - Complete QSPI NOR pull-ups, decoupling, hold/write-protect policy, and
     power symbols.

2. `optional_profiles.kicad_sch`
   - Keep NFC antenna/matching blocked until first-article RF tuning with
     display, battery, and enclosure stack.

3. Footprints and routing
   - Verify local `nSealr_Display` FFC footprints against Molex/Newhaven
     mechanical drawings before ordering.
   - Route all nets, add power/ground zones, then run DRC fresh against the
     routed PCB.

4. Root hierarchy
   - Replace cross-sheet global-label scaffolding with hierarchical sheet pins
     or a source-backed flat schematic structure.
   - Keep ERC at 0 after each sheet group, regenerate `erc/triage.*`, and do not
     release until DRC is also clean or every remaining warning has a documented,
     datasheet-backed waiver.

## Release Gate

The project must not produce a `release_outputs_valid: true` PCBWay manifest
until:

- ERC is clean or all residual warnings are reviewed and justified;
- DRC runs freshly against the current PCB;
- the board has routed copper, vias, and zones;
- NFC antenna/matching is either finalized or clearly excluded from the
  manufacturing build;
- BOM, position file, Gerbers, drill, and render all match the same KiCad
  revision.
