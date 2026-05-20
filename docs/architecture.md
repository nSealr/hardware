# Architecture

`nSealr/hardware` contains open hardware reference material.

## Responsibilities

- BOMs.
- Wiring diagrams.
- KiCad design files.
- Enclosure notes.
- Display, button, camera, and module compatibility notes.
- Provisioning and debug jig documentation.
- Hardware security notes.

PCB work must follow proven firmware and UX requirements, not precede them.

Per-family feature target and current status live in `nSealr/specs`
`vectors/features/signer-feature-matrix-v0.json`. Hardware requirements can
state which boards, displays, cameras, controls, and provisioning paths are
needed to satisfy those targets, but they must not create new feature behavior
or new signer-family taxonomy outside that shared contract.

## Implemented Foundation

- `pcb/reference-esp32-s3-signer/requirements.json`: checked requirements for
  the first ESP32 USB/NIP-46 signer reference board.
- `pcb/reference-esp32-s3-qr-signer/requirements.json`: checked requirements
  for the ESP32 stateless QR vault devkit validation path, currently centered
  on the T-Display S3 Pro OV5640 candidate and validating Waveshare
  `ESP32-S3-Touch-LCD-3.5B-C` as the preferred secondary case-plus-OV5640
  target with AXS15231B/QSPI display constraints.
- `kits/reference-raspberry-qr-vault/requirements.json`: checked requirements
  for the Raspberry/Pi stateless QR vault kit validation path, covering camera,
  trusted display, physical buttons, response QR display, wireless disablement,
  removable boot media, RAM-only custody, and explicit SeedSigner-compatible
  Pi Zero hardware targets.
- `kits/reference-raspberry-qr-vault/os-profile.json`: checked operating
  profile for future Raspberry/Pi stateless QR vault images, requiring
  removable boot media, disabled or absent wireless, RAM-only session custody,
  no swap, no remote access during signing, disabled setup services, and
  acceptance evidence.
- `pcb/custom-persistent-secret-wallet/requirements.json`: checked
  requirements for the first custom persistent-secret wallet Rev A. This is a
  USB-C bus-powered connected/no-wireless, no-battery, TROPIC01-assisted
  hardware-wallet scaffold, not an air-gapped QR vault.
- `bom/reference-esp32-s3-signer.csv`: first BOM scaffold with required and
  optional component categories.
- `bom/reference-raspberry-qr-vault-kit.csv`: first kit BOM scaffold for the
  Raspberry/Pi stateless QR vault path, covering the single-board computer,
  camera, trusted display, physical controls, power, boot media, temporary
  setup path, and wireless-disable evidence.
- `bom/custom-persistent-secret-wallet.csv`: first component-class BOM scaffold
  for the custom wallet Rev A, covering ESP32-S3, TROPIC01, USB-C, power,
  protection, display, physical controls, and provisioning/test pads.
- `templates/raspberry-qr-vault-os-profile-smoke.json`: validated manual
  report template for future Raspberry OS profile acceptance evidence.
- `templates/raspberry-qr-vault-full-flow-smoke.json`: validated manual
  report template for future Raspberry QR-flow acceptance evidence across Pi
  camera scan, trusted display review, GPIO controls, response QR output, and
  companion verification.
- `reports/esp32-s3-devkitc-1-detection-2026-05-08.json`: first manual
  hardware validation report, recording ESP32-S3 board detection only.
- `scripts/validate_hardware.py`: directory-driven validation for
  requirements, Raspberry OS profiles, BOM quality, manual reports, and report
  templates.

The USB/NIP-46 reference requirements keep TROPIC01 out of the MVP and leave
persistent-secret secure-element research to the custom hardware-wallet family.
Mandatory hardware focuses on native USB, local review display, physical
approve/reject controls, and ESP32-S3 security capabilities. Review hardware
must support a flow that binds physical approval to both displayed request id
and displayed approval digest before firmware signing is enabled.

The QR signer requirements add camera, battery, wireless-disable, physical
approval, and touch-not-approval constraints for stateless devkit validation.
They also require explicit QR contract text for the shared `nsealr1` envelope,
trusted review, and physical approval. They explicitly exclude persistent
signing secrets and TROPIC01 interfaces. They are not a custom PCB, schematic,
or manufacturing package.
They also pin the shared `nsealr-account-descriptor-v0` route
`esp32_qr_vault`, `policy-manual-only-qr-vault`, and
`persistent_grants: false` so QR hardware work cannot drift into grant storage
or policy automation.

The USB/NIP-46 requirements pin the shared `esp32_usb_nip46` route,
`policy-manual-only-persistent-device`,
`policy-scoped-automation-daily-use`, and
`grant-esp32-usb-kind-1-session` as future persistent-route contracts only.
Manual-only is the default policy; scoped automation requires a separate
device-reviewed policy change and the v0 grant menu is limited to
`sign_event` kind `1`. That does not clear firmware signing gates or create a
PCB requirement for production grant storage before provisioning and security
policy are accepted.
The target persistent-device hardware model is an encrypted vault with seed
profiles, BIP-39 passphrase namespaces, standalone key slots, per-public-key
policy, one device-level v0 unlock ceremony, wipe/export policy, secure boot,
flash encryption or equivalent persistent-secret protection, and debug lock.
The current scoped-automation contract is a validator scaffold, not the final
policy UI.

The custom persistent-secret wallet Rev A requirements bring TROPIC01 into the
custom wallet family as a concrete secure-element dependency for secure channel,
TRNG, device authenticity, pairing-key lifecycle, MAC-and-Destroy PIN attempt
hardening, and key wrapping/unlock material. They intentionally keep current
BIP-340 signing on the ESP32-S3 host MCU while preserving direct TROPIC01
Schnorr/BIP-340 as future vendor-roadmap work. Because Rev A uses USB data
transport, validation rejects air-gapped wording for that board. Battery
interfaces are excluded from Rev A so power, recovery, and logistics stay simple
until a separate portable branch is justified.
The hardware test suite also consumes shared specs snapshots for
`custom-hardware-wallet-slot-0`, `policy-manual-only-persistent-device`,
`custom-hardware-wallet-enable-kind-1-automation`,
`policy-scoped-automation-daily-use`,
`grant-custom-hardware-wallet-kind-1-session`, and
`custom-hardware-wallet-sign-event-slot-0`. That keeps Rev A's hardware
requirements bound to the canonical route descriptor, default manual policy,
future scoped policy, policy-change review, v0 `sign_event` kind `1` grant,
and route-selection contract while preserving the rule that account descriptors
and hardware artifacts are secretless metadata.

The Raspberry QR vault kit requirements follow the same stateless QR contract
without ESP32-specific secure boot or flash-encryption assumptions. They require
camera input, a trusted local display, tactile physical approval/rejection,
response QR output, disabled wireless, and removable boot-media discipline
before any Pi build can be treated as more than a desktop harness.
They pin the shared `nsealr-account-descriptor-v0` route
`raspberry_qr_vault`, `policy-manual-only-qr-vault`, and
`persistent_grants: false` so the Pi kit cannot grow persistent grants,
TROPIC01, or policy automation by hardware drift.
The checked compatibility profile centers the kit on the SeedSigner-style
Raspberry Pi Zero stack: Pi Zero-class board, Pi/ZeroCam OV5647 camera,
Waveshare-compatible ST7789 240x240 SPI display HAT, GPIO joystick/buttons,
removable microSD boot media, and SeedSigner-OS/Buildroot reference shape.
The same requirements pin the first 40-pin GPIO review-button map shared with
`nSealr/raspberry`: BOARD 37/right for `next`, BOARD 35/down for `scroll`,
BOARD 33/center for `approve`, and BOARD 40/KEY1 for `reject`, with reject
precedence documented before physical-control acceptance can be claimed.
Pi 3/4/5 variants can be documented later only as development or accessibility
variants that preserve the same offline QR and RAM-only custody boundary.
The companion kit BOM is a validation scaffold, not a purchase order: it keeps
wireless mitigation, removable boot media, temporary setup/debug removal, and
RAM-only custody visible before Raspberry hardware acceptance starts.
The OS profile adds the software-side acceptance boundary for that same kit:
no swap-backed secret leakage, no remote login during signing, and explicit
wireless/secret/session-loss evidence before a Raspberry image can be treated
as a stateless QR vault image.

Manual hardware reports are structured evidence for bring-up work. They must
record hardware, source repo, firmware commit, exact procedure, expected and
observed results, limitations, and safety flags. Validation rejects reports
that enable production signing, and stateless target reports must not claim
persistent secrets or TROPIC01 usage.
Raspberry OS profile smoke reports additionally need explicit evidence terms
for removable boot media, wireless state, swap state, remote access, RAM-only
custody, persistent-secret absence, and power-cycle session loss.
Raspberry QR-flow smoke reports additionally need explicit evidence for Pi
Zero camera scanning of `nsealr1` QR requests, trusted local display review,
physical GPIO `next`/`scroll`/`approve`/`reject` controls, signed-event
response QR output, companion `verify-response`, request id and
`approval_digest` binding, no USB data transport, RAM-only custody, no
persistent secret, and no TROPIC01.
Future QR vault hardware acceptance should also prove that session key-source
flows stay RAM-only and avoid microSD/file secret transfer. SeedSigner
SeedQR/CompactSeedQR import is a BIP-39/NIP-06 compatibility goal, not Bitcoin
wallet-state import.
The top-level validator discovers committed validation inputs under `pcb/`,
`kits/`, `bom/`, `reports/`, and `templates/` so future hardware artifacts do
not need bespoke wiring before CI checks their schema and safety flags.
