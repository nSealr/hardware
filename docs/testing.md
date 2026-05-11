# Testing

## Current Baseline

```sh
make ci
```

The baseline runs repository verification, unit tests for hardware validators,
bytecode compilation, and directory-driven validation of committed
requirements, OS profiles, BOMs, reports, and report templates.

## Implemented Tests

- Reference requirements validation.
- ESP32-S3 QR signer requirements validation.
- Raspberry/Pi stateless QR vault kit requirements validation.
- Raspberry/Pi stateless QR vault OS profile validation.
- Raspberry/Pi stateless QR vault OS profile smoke-report template validation.
- Directory-driven discovery for committed requirements, Raspberry OS profiles,
  BOMs, reports, and report templates.
- Raspberry/Pi stateless QR vault seed-entry policy validation, requiring
  acceptance evidence that session-secret input does not use seed files,
  command-line secret arguments, shell history, or persistent storage.
- Reference USB signer BOM validation.
- Raspberry/Pi stateless QR vault kit BOM validation.
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
- LILYGO T-Display S3 development-gate signing-status protocol-smoke report
  validation for revision `f5753e2`, confirming the firmware builds and flashes
  with ESP-IDF v5.5.4, passes 35 USB serial exchanges, reports
  `development_accepted_gates` separately from production `missing_gates`, and
  preserves `signing_disabled`.
- LILYGO T-Display S3 UTF-8 review-renderer protocol-smoke report validation
  for revision `719d680`, confirming the firmware builds and flashes with
  ESP-IDF v5.5.4 after host-core review wrapping was hardened to preserve
  UTF-8 codepoint boundaries, passes 35 USB serial exchanges, and preserves
  `signing_disabled`.
- LILYGO T-Display S3 ASCII punctuation review-renderer protocol-smoke report
  validation for revision `571cc48`, confirming the firmware builds and
  flashes with ESP-IDF v5.5.4 after common printable ASCII punctuation glyphs
  were added to the host-buildable review display path, passes 35 USB serial
  exchanges, and preserves `signing_disabled`.
- LILYGO T-Display S3 ASCII punctuation glyph protocol-smoke report validation
  for revision `fedcb5f`, confirming the firmware builds and flashes with
  ESP-IDF v5.5.4 after caret and backtick glyph coverage was added, verifies
  image hashes, passes 39 USB serial capability exchanges, passes the
  7-scenario review smoke, and preserves `signing_disabled`.
- LILYGO T-Display S3 review-detail-page protocol-smoke report validation for
  revision `c5f60b2`, confirming the firmware still builds and flashes after
  the ESP32 host-core consumed shared review-detail-page vectors, passes 35 USB
  serial exchanges, and preserves `signing_disabled`.
- LILYGO T-Display S3 review-scenario protocol-smoke report validation for
  smoke-tool revision `af88ee5`, confirming the attached board accepted the
  basic, tagged, long-content, scroll-window, Unicode fallback, and
  request-error review scenarios over USB serial while preserving
  `signing_disabled` for valid `sign_event` review requests and deterministic
  `unsupported_request` for the invalid request.
- LILYGO T-Display S3 dense-tags review-scenario protocol-smoke report
  validation for smoke-tool revision `daeea6d`, confirming the expanded
  7-scenario smoke accepted the dense-tags valid `sign_event` request over USB
  serial while preserving `signing_disabled` for valid review requests and
  deterministic `unsupported_request` for the invalid request.
- LILYGO T-Display S3 review-detail style-cleanup protocol-smoke report
  validation for revision `5280fab`, confirming the firmware still builds and
  flashes after the obsolete `ReviewBodyLineStyle::Label` path was removed
  from active ESP32 review-detail code, passes 35 USB serial exchanges, and
  preserves `signing_disabled`.
- LILYGO T-Display S3 malformed serial transport protocol-smoke report
  validation for smoke-tool revision `f1d29d4`, confirming the expanded
  38-exchange USB serial smoke rejects checksum-mismatch, malformed-base64url,
  and overlong transport vectors with deterministic `malformed_frame` or
  `overlong_frame` errors while preserving `signing_disabled`.
- LILYGO T-Display S3 overlong serial-input drain protocol-smoke report
  validation for firmware revision `628bd7f`, confirming the firmware builds
  and flashes with ESP-IDF v5.5.4, passes the 38-exchange malformed transport
  smoke, then still accepts the 7-scenario review smoke after the overlong
  drain path.
- LILYGO T-Display S3 overlong serial recovery protocol-smoke report
  validation for smoke-tool revision `f13c591`, confirming the expanded
  39-exchange capability smoke sends a valid `post-overlong-recovery`
  capability request immediately after the overlong-frame rejection and the
  attached board accepts it while preserving `signing_disabled`.
- LILYGO T-Display S3 companion serial protocol-smoke report validation for
  lab smoke-tool revision `60f4200` and companion revision `40ab7bf`,
  confirming the real companion CLI can generate, wrap, exchange, and
  request-bound unwrap `get_capabilities`, `get_signing_status`, and
  `get_public_key` responses against the attached board, then send a shared
  basic `sign_event` request and verify the request-matched `signing_disabled`
  refusal path.
- LILYGO T-Display S3 current-head firmware protocol-smoke report validation
  for ESP32 revision `8307c4b`, confirming the attached board was rebuilt,
  reflashed, passed the 39-exchange capability smoke, passed the 7-scenario
  review smoke, and returned request-matched `signing_disabled` for a
  companion-generated `sign_event`.
- LILYGO T-Display S3 Unicode signing-gate protocol-smoke report validation
  for ESP32 revision `d2387b1`, confirming the firmware rebuilds, flashes, and
  exposes `unicode_review_rendering` as a missing signing-readiness gate while
  preserving `signing_disabled`.
- LILYGO T-Display S3 direct companion serial-line protocol-smoke report
  validation for ESP32 revision `0dda7d6`, companion revision `b399ad0`, and
  lab smoke-tool revision `a00af12`, confirming the direct `nseal serial-line
  exchange` path can request capabilities from the attached board and can verify
  the request-matched `signing_disabled` refusal for a companion-generated
  `sign_event`.
- LILYGO T-Display S3 package-owned companion serial-line protocol-smoke report
  validation for companion revision `6bbf03a`, confirming the refactored
  `exchangeSerialLineRequest` boundary still drives the attached board through
  `nseal serial-line exchange`, verifies get-capabilities output, and verifies
  the request-matched `signing_disabled` refusal for a companion-generated
  `sign_event`.
- LILYGO T-Display S3 disabled-signing copy protocol-smoke report validation
  for ESP32 revision `3845b05`, confirming the firmware rebuilt and reflashed
  with ESP-IDF v5.5.4 after disabled-signing log/copy alignment, verified
  image hashes, passed 39 USB serial exchanges, and preserved
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
- LILYGO T-Display S3 manual button-approve display-smoke report validation,
  tying the `button-approve` manual exerciser from ESP32 revision `d455056` to
  firmware revision `f4f4fc0` on the attached board. The operator confirmed
  short KEY/GPIO14 page traversal, long KEY/GPIO14 approve closure, final
  `Review OK` / `Closed` / `Not signed` / `Signing disabled`, and preserved
  `signing_disabled`.
- LILYGO T-Display S3 manual button-reject display-smoke report validation,
  tying the `button-reject` manual exerciser from ESP32 revision `d455056` to
  firmware revision `f4f4fc0` on the attached board. The operator confirmed
  long BOOT/GPIO0 reject closure, final `Rejected` / `Closed` / `Not signed` /
  `Signing disabled` / `Send new request`, and preserved `signing_disabled`.
- Negative requirements test for missing mandatory interfaces.
- Negative requirements test for missing approval-digest review binding.
- Negative QR requirements tests for missing camera, missing disabled wireless
  policy, missing `qr_requirements`, and missing core QR contract terms for the
  shared `nseal1` envelope, trusted review, and physical approval.
- Negative Raspberry QR requirements test for missing response QR display
  output.
- Negative Raspberry QR OS profile tests for enabled swap, enabled remote
  access during signing, and persistent signing-secret storage.
- Negative Raspberry OS profile smoke-report test requiring power-cycle
  evidence to appear in report evidence fields rather than only in expected
  text.
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
