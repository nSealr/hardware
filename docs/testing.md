# Testing

## Current Baseline

```sh
make ci
```

The baseline runs repository verification, unit tests for hardware validators,
bytecode compilation, and validation of the reference requirements and BOM.

## Implemented Tests

- Reference requirements validation.
- ESP32-S3 QR signer requirements validation.
- Reference BOM validation.
- Manual hardware report validation.
- ESP32-S3 DevKitC-1 build/flash/protocol smoke report validation.
- ESP32-S3 DevKitC-1 dynamic serial protocol-smoke report validation.
- Negative requirements test for missing mandatory interfaces.
- Negative requirements test for missing approval-digest review binding.
- Negative QR requirements tests for missing camera and missing disabled
  wireless policy.
- Negative manual report tests for missing production-signing safety flags,
  persistent secrets on stateless targets, and TROPIC01 usage on stateless
  targets.

## Required Tests

- File presence and naming checks.
- KiCad ERC/DRC when KiCad files exist and tooling is available.
- Hardware validation reports for physical builds.

Manual hardware tests must include exact parts, firmware commit, procedure,
result, photos or logs where useful, and known limitations.

Committed report files under `reports/` must keep `production_signing_enabled`
false unless the project explicitly creates a later production-signing release
gate. Stateless QR vault reports must also keep `persistent_secret_present` and
`tropic01_used` false.
