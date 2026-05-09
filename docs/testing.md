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
- ESP32-S3 DevKitC-1 serial review-boundary protocol-smoke report validation
  for revision `dfdeec9`, confirming the firmware builds, flashes, preserves
  `signing_disabled`, and keeps deterministic invalid-request rejection after
  compiling the serial `sign_event` trusted-review boundary into host-core.
- ESP32-S3 DevKitC-1 current-head protocol-smoke report validation for
  revision `61b51df`, confirming the firmware still builds, flashes, verifies
  image hashes, passes 33 USB serial exchanges, preserves `signing_disabled`,
  and keeps deterministic invalid-request rejection.
- LILYGO T-Display S3 signing-status protocol-smoke report validation for
  revision `7ca2548`, confirming the firmware builds with ESP-IDF v5.5.4,
  flashes over `/dev/cu.usbmodem1101`, verifies image hashes, passes 35 USB
  serial exchanges, exposes `get_signing_status`, reports all then-missing
  signing gates while `signing_enabled` is false, and preserves
  `signing_disabled`.
- LILYGO T-Display S3 refined signing-status protocol-smoke report validation
  for revision `d67f587`, confirming the firmware still builds and flashes
  with ESP-IDF v5.5.4, passes 35 USB serial exchanges, reports parser limits
  and approval-digest binding as implemented in `get_signing_status`, keeps the
  remaining production signing gates missing, and preserves
  `signing_disabled`.
- LILYGO T-Display S3 raster-regression protocol-smoke report validation for
  revision `1dc19f5`, confirming the firmware still builds and flashes after
  moving boot/review-frame rasterization into a host-buildable module, passes
  35 USB serial exchanges, and preserves `signing_disabled`.
- LILYGO T-Display S3 button-logic protocol-smoke report validation for
  revision `c5c59f2`, confirming the firmware still builds and flashes after
  moving debounce and short/long press classification into a host-buildable
  module, passes 35 USB serial exchanges, and preserves `signing_disabled`.
- LILYGO T-Display S3 status-frame protocol-smoke report validation for
  revision `f4f4fc0`, confirming the firmware still builds and flashes after
  moving Ready, review-decision, timeout, and request-error display frames into
  a host-buildable module, passes 35 USB serial exchanges, and preserves
  `signing_disabled`.
- Negative requirements test for missing mandatory interfaces.
- Negative requirements test for missing approval-digest review binding.
- Negative QR requirements tests for missing camera, missing disabled wireless
  policy, missing `qr_requirements`, and missing core QR contract terms for the
  shared `nseal1` envelope, trusted review, and physical approval.
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
