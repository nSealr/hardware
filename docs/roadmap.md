# Roadmap

## Foundation: Reference Requirements And BOM

- ESP32-S3 USB signer requirements JSON.
- ESP32-S3 QR signer requirements JSON for T-Display S3 Pro OV5640 devkit
  validation.
- Raspberry/Pi stateless QR vault kit requirements JSON.
- Reference BOM scaffold.
- Manual hardware validation report schema.
- Validator and tests, including review approval-digest binding.

Status: implemented as the first open hardware foundation. This remains
requirements/BOM/report validation only; no custom PCB, schematic, or
manufacturing package exists yet. The first report records ESP32-S3 detection
only and is not a flash, display, GPIO, camera, or signing smoke test. A later
ESP32-S3 DevKitC-1 report records build, flash, and protocol smoke evidence for
the hardened firmware while keeping production signing disabled. A follow-up
protocol-smoke report records dynamic serial request-id handling against the
same flashed firmware and includes invalid metadata rejection evidence. Later
ESP32-S3 DevKitC-1 protocol-smoke reports rebuild and reflash the firmware,
then verify that serial-wrapped invalid signing-request vectors from
`NostrSeal/specs` are rejected with deterministic `unsupported_request` frames
while runtime signing remains disabled. The latest report covers revision
`dfdeec9` after the serial `sign_event` trusted-review boundary was compiled
into host-core. It confirms the USB serial scaffold still builds, flashes,
answers capability and development public-key requests, returns
`signing_disabled` for `sign_event`, and rejects invalid request vectors. It
does not test real camera, display, GPIO, storage, secure boot, debug lock, or
signing acceptance.

Status note, 2026-05-09: ESP32 stateless QR vault hardware requirements now
validate the `qr_requirements` contract explicitly. Requirements files must
retain the shared `nseal1` envelope, trusted review, and physical approval
terms before later devkit wiring, camera/display testing, or PCB work can claim
QR signer coverage.

Status note, 2026-05-10: Raspberry/Pi stateless QR vault kit requirements are
now validated separately from ESP32 requirements. They require camera, trusted
display, physical controls, response QR display, disabled wireless, removable
boot media, RAM-only session custody, and no TROPIC01 or persistent-secret
dependency before Pi hardware acceptance work begins.

Status note, 2026-05-09: ESP32-S3 DevKitC-1 firmware revision `61b51df` was
built with ESP-IDF `v5.5.4`, flashed on `/dev/cu.usbmodem1101`, and
smoke-tested with 33 verified USB serial exchanges. The current scaffold still
returns capability and development public-key responses, keeps `sign_event`
disabled with `signing_disabled`, and rejects invalid metadata/signing-request
frames deterministically.

Status note, 2026-05-10: LILYGO T-Display S3 firmware revision `c5f60b2` was
built with ESP-IDF `v5.5.4`, flashed on `/dev/cu.usbmodem1101`, and
smoke-tested with 35 verified USB serial exchanges after the ESP32 host-core
consumed shared review-detail-page vectors. The report is protocol smoke only:
it preserves the `signing_disabled` USB contract and does not claim production
trusted-display or real-signing acceptance.

Status note, 2026-05-10: LILYGO T-Display S3 review-scenario smoke used
`NostrSeal/esp32` smoke-tool revision `af88ee5` against the existing flashed
firmware image on `/dev/cu.usbmodem1101`. It verified 6 non-interactive review
scenarios and 7 USB serial exchanges covering basic, tagged, long-content,
scroll-window, Unicode fallback, and request-error inputs. Valid `sign_event`
review requests still returned `signing_disabled`; the invalid request returned
the expected `unsupported_request` frame.

## M14: Reference Designs

- Wiring diagrams.
- KiCad starter.
- Enclosure notes.
- Provisioning/debug jig.
- Assembly docs.

## Later

- Custom PCB.
- Manufacturing package.
- Release checklist for hardware revisions.
