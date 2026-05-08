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
- ESP32-S3 DevKitC-1 dynamic serial protocol-smoke report validation, including
  invalid metadata rejection.
- ESP32-S3 DevKitC-1 invalid signing-request protocol-smoke report validation,
  including 25 serial-wrapped invalid request vectors from `NostrSeal/specs`,
  unknown top-level field rejection, parameterless-method `params` rejection,
  structurally invalid `sign_event` `params`/`event_template` shapes, and
  deterministic `unsupported_request` responses.
- ESP32-S3 DevKitC-1 QR review I/O transcript protocol-smoke report validation
  for revision `b7aa30a`, confirming the host-core transcript helper can be
  compiled into the ESP-IDF component while the attached-board smoke still
  returns only capability, development public-key, `signing_disabled`, and
  deterministic invalid-request responses over USB serial.
- ESP32-S3 DevKitC-1 reflash-recovery protocol-smoke report validation for
  revision `f307b41`, recording a non-bootable factory app partition diagnosed
  from boot logs, a clean ESP-IDF reflash with image hash verification, and a
  passing post-reflash `idf-smoke-capabilities` run.
- Negative requirements test for missing mandatory interfaces.
- Negative requirements test for missing approval-digest review binding.
- Negative QR requirements tests for missing camera and missing disabled
  wireless policy.
- Negative manual report tests for missing production-signing safety flags,
  persistent secrets on stateless targets, and TROPIC01 usage on stateless
  targets.
- Negative ESP32 USB protocol-smoke report test requiring explicit
  `signing_disabled` evidence whenever production signing remains disabled.

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
