# Roadmap

## Foundation: Reference Requirements And BOM

- ESP32-S3 USB signer requirements JSON.
- ESP32-S3 QR signer requirements JSON for T-Display S3 Pro OV5640 devkit
  validation.
- Raspberry/Pi stateless QR vault kit requirements JSON.
- Raspberry/Pi stateless QR vault OS profile JSON.
- ESP32-S3 USB signer reference BOM scaffold.
- Raspberry/Pi stateless QR vault kit BOM scaffold.
- Raspberry/Pi stateless QR vault OS profile report template.
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

Status note, 2026-05-10: the Raspberry/Pi stateless QR vault kit now has a
validated BOM scaffold. It records the SBC, camera, trusted display, physical
approve/reject/navigation controls, power, removable boot media, temporary
setup path, mechanical mounting, and wireless-disable evidence needed before
real Raspberry bring-up. It is not a purchase order, enclosure design, GPIO
driver, or PCB.

Status note, 2026-05-10: the Raspberry/Pi stateless QR vault kit now has a
validated OS profile scaffold. It requires removable microSD boot media,
disabled or absent wireless, RAM-only session custody, no swap during signing,
no remote access during signing, disabled setup services, and acceptance
evidence for wireless state, swap state, remote-login state, persistent-secret
absence, and power-cycle session loss. It is not a downloadable OS image.

Status note, 2026-05-10: the Raspberry/Pi stateless QR vault now has a
validated OS profile smoke-report template. Future completed reports must carry
evidence terms for removable boot media, wireless state, swap state, remote
access, RAM-only custody, persistent-secret absence, and power-cycle session
loss before Raspberry image acceptance can be claimed.

Status note, 2026-05-11: the Raspberry/Pi stateless QR vault OS profile now
requires a `session_secret_input_policy` of `no_seed_files_or_secret_cli_args`.
Future acceptance evidence must show that seed entry or session-secret input
does not depend on seed files, command-line secret arguments, shell history, or
persistent storage. This aligns hardware acceptance with the stateless
Raspberry CLI stdin harness while keeping real Pi seed-entry UX pending.

Status note, 2026-05-11: the hardware validator now discovers committed
requirements, Raspberry OS profiles, BOMs, manual reports, and report templates
from repository directories instead of relying on a fixed list of reference
paths. This keeps future hardware evidence under CI automatically while still
leaving custom PCB design, manufacturing files, and production signing release
gates out of scope.

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

Status note, 2026-05-10: LILYGO T-Display S3 dense-tags review-scenario smoke
used `NostrSeal/esp32` smoke-tool revision `daeea6d` against the existing
flashed firmware image `5280fab` on `/dev/cu.usbmodem1101`. It verified the
expanded 7-scenario review smoke with 8 USB serial exchanges, adding a
dense-tags valid `sign_event` request while preserving `signing_disabled` for
valid review requests and `unsupported_request` for the invalid request.

Status note, 2026-05-10: LILYGO T-Display S3 firmware revision `5280fab` was
built with ESP-IDF `v5.5.4`, flashed on `/dev/cu.usbmodem1101`, and
smoke-tested with 35 verified USB serial exchanges after the obsolete
`ReviewBodyLineStyle::Label` path was removed from active ESP32 review-detail
code. This preserved the `signing_disabled` USB contract and did not add a
production trusted-display or real-signing claim.

Status note, 2026-05-10: LILYGO T-Display S3 malformed serial transport smoke
used `NostrSeal/esp32` smoke-tool revision `f1d29d4` against the existing
flashed firmware image `5280fab` on `/dev/cu.usbmodem1101`. It verified the
expanded 38-exchange USB serial smoke, including checksum-mismatch,
malformed-base64url-payload, and overlong-frame transport vectors. Valid
`sign_event` still returned `signing_disabled`; invalid signing requests
returned `unsupported_request`; malformed transport returned `malformed_frame`
or `overlong_frame`.

Status note, 2026-05-10: LILYGO T-Display S3 firmware revision `628bd7f` was
built with ESP-IDF `v5.5.4`, flashed on `/dev/cu.usbmodem1101`, and
smoke-tested after adding a host-tested overlong serial input drain. The
38-exchange capability smoke passed, then the 7-scenario review smoke also
passed, confirming the overlong transport smoke leaves the serial reader ready
for fresh review requests. Real signing remains disabled.

Status note, 2026-05-10: LILYGO T-Display S3 overlong recovery smoke used
`NostrSeal/esp32` smoke-tool revision `f13c591` against the existing flashed
firmware image `628bd7f` on `/dev/cu.usbmodem1101`. It verified the expanded
39-exchange capability smoke, including a valid `post-overlong-recovery`
capability request immediately after the overlong-frame rejection. The board
accepted the fresh request, and real signing remains disabled.

Status note, 2026-05-10: LILYGO T-Display S3 companion serial smoke used
`NostrSeal/lab` smoke-tool revision `60f4200` and `NostrSeal/companion`
revision `40ab7bf` against the existing flashed firmware image `628bd7f` on
`/dev/cu.usbmodem1101`. The companion CLI generated, wrapped, sent, and
request-bound unwrapped `get_capabilities`, `get_signing_status`, and
`get_public_key` responses successfully. The same smoke generated a
`sign_event` request from the shared basic kind `1` fixture and verified the
request-matched `signing_disabled` response. This records companion/transport
hardware evidence only; no real signing gate changed.

Status note, 2026-05-10: LILYGO T-Display S3 current-head firmware smoke
rebuilt and flashed `NostrSeal/esp32` revision `8307c4b` on
`/dev/cu.usbmodem1101`. `idf-smoke-capabilities` passed with 39 verified
exchanges, `idf-smoke-review-scenarios` passed with 7 scenarios, and the lab
companion serial smoke verified a request-matched `signing_disabled` response
for a companion-generated `sign_event`. This aligns the physical board with
the current repository head while preserving every production signing blocker.

Status note, 2026-05-11: LILYGO T-Display S3 direct companion serial-line
smoke used `NostrSeal/esp32` revision `0dda7d6`, `NostrSeal/companion`
revision `b399ad0`, and `NostrSeal/lab` smoke-tool revision `a00af12` on
`/dev/cu.usbmodem1101`. The companion `nseal serial-line exchange` path opened
the board directly through Node `serialport`, verified get-capabilities output,
and verified the request-matched `signing_disabled` response for a
companion-generated `sign_event`. This records real companion-to-device
transport evidence only; it does not change any production signing gate.

Status note, 2026-05-11: after `NostrSeal/companion` revision `6bbf03a` moved
one-shot serial-line exchange ownership into `packages/transport`, the attached
LILYGO T-Display S3 on `/dev/cu.usbmodem1101` passed the lab companion
serial-line get-capabilities smoke and the shared `sign-event-disabled` smoke.
The second run returned request-matched `signing_disabled`. No firmware was
reflashed for this report, and no production signing gate changed.

Status note, 2026-05-11: LILYGO T-Display S3 firmware revision `3845b05` was
rebuilt with ESP-IDF `v5.5.4`, flashed on `/dev/cu.usbmodem1101`, and
smoke-tested after disabled-signing firmware log/copy alignment. ESP-IDF
verified image hashes during flash, and the post-flash capability smoke passed
with 39 verified exchanges, 9 response frames, and 30 expected rejection
frames. This keeps the physical board aligned with current disabled-signing
safety copy only; it does not claim camera, QR, key provisioning, secure boot,
debug-lock, signed-output, or production signing acceptance.

Status note, 2026-05-11: LILYGO T-Display S3 firmware revision `d2387b1` was
rebuilt with ESP-IDF `v5.5.4`, flashed on `/dev/cu.usbmodem1101`, and
smoke-tested after `unicode_review_rendering` was added to the runtime
signing-readiness gate and shared `get_signing_status` contract. ESP-IDF
verified image hashes during flash, and the post-flash capability smoke passed
with 39 verified exchanges, 9 response frames, and 30 expected rejection
frames. This proves the disabled-signing diagnostic still runs on the attached
board; it does not claim production Unicode review acceptance, key
provisioning, secure boot, debug-lock, signed-output, or production signing
acceptance.

Status note, 2026-05-11: LILYGO T-Display S3 firmware revision `311368a` was
rebuilt with ESP-IDF `v5.5.4`, flashed on `/dev/cu.usbmodem1101`, and
smoke-tested after host-core signing-status gate de-duplication. ESP-IDF
verified image hashes during flash, and the post-flash capability smoke passed
with 39 verified exchanges, 9 response frames, and 30 expected rejection
frames. This is firmware protocol evidence for the duplicate-free
signing-status diagnostic contract only; it does not claim key provisioning,
secure boot, debug-lock, signed-output, or production signing acceptance.

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
