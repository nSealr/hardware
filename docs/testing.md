# Testing

## Current Baseline

```sh
make ci
```

The baseline runs repository verification, unit tests for hardware validators,
bytecode compilation, and directory-driven validation of committed requirements,
OS profiles, BOMs, reports, and report templates.

## Implemented Coverage

- Reference ESP32-S3 USB/NIP-46 requirements validation.
- ESP32-S3 stateless QR vault requirements validation.
- Raspberry/Pi stateless QR vault kit requirements validation.
- Raspberry/Pi stateless QR vault OS profile validation.
- Raspberry/Pi stateless QR vault report-template validation.
- Identity/policy requirement validation for ESP32 and Raspberry requirement
  sets.
- Rejection of stateless QR vault TROPIC01 usage.
- Manual hardware report validation.
- Directory-driven discovery for requirements, OS profiles, BOMs, reports, and
  templates.

## Custom Hardware Expectations

There is currently no active custom hardware board in this repository. The legacy
TROPIC01 Universal Secure Device board and its board-specific validators were
archived, with full git history, to the private read-only repository
`nSealr/hardware-legacy-tropic01-universal`.

When the next custom hardware board — the minimal custom hardware wallet from the
`nSealr/specs` five-solution device-matrix decision — lands, its requirements,
BOM, and production contracts get their own validation coverage here. KiCad
routing and PCBWay export tests must be added only after the schematic and board
source are generated from real nets; until then, generated manufacturing outputs
must be treated as invalid.
