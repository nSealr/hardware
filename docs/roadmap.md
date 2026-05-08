# Roadmap

## Foundation: Reference Requirements And BOM

- ESP32-S3 USB signer requirements JSON.
- ESP32-S3 QR signer requirements JSON for T-Display S3 Pro OV5640 devkit
  validation.
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
same flashed firmware and includes invalid metadata rejection evidence. The
latest ESP32-S3 DevKitC-1 protocol-smoke report rebuilds and reflashes firmware
revision `2597403`, then verifies that serial-wrapped invalid `sign_event`
request vectors from `NostrSeal/specs` are rejected with deterministic
`unsupported_request` frames while runtime signing remains disabled.

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
