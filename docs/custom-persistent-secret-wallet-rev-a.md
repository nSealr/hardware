# Custom Persistent-Secret Wallet Rev A

This document records the first concrete custom-wallet target for nSealr
hardware work. It is a requirements and BOM scaffold, not a schematic or KiCad
layout.

## Product Boundary

Rev A is a USB-C bus-powered connected hardware wallet. It has no battery,
charger, camera requirement, or QR transport requirement. Wireless is disabled
or excluded by firmware and production policy, but an ESP32-S3 module may still
physically include an antenna unless a later bare-chip design accepts RF layout
and certification work.

Because USB carries data, Rev A must not be described as air-gapped. The
stateless Raspberry/Pi and ESP32 QR vaults remain the offline QR transport
lines.

## Core Architecture

- ESP32-S3 owns USB transport, trusted review UI, physical controls, request
  validation, event id calculation, and current BIP-340 signing.
- TROPIC01 owns secure-channel anchored operations, TRNG contribution, device
  authenticity evidence, pairing-key lifecycle, MAC-and-Destroy PIN attempt
  hardening, and key wrapping or unlock material.
- Direct TROPIC01 Schnorr/BIP-340 signing is tracked as a future vendor-roadmap
  path. It is not a current Rev A assumption.
- TROPIC01 recovery/reset should be designed as controlled power cycling through
  a load switch, not as a dedicated reset pin.

## TROPIC01 Integration Notes

Use the Tropic Square open hardware designs as electrical references, not as a
direct copy of an ESP32 wallet board. The minimal TROPIC01 connection is SPI,
GPO/IRQ, 3.3 V power, local decoupling, and the reference pull network. The
Arduino Shield includes level shifting for 5 V Arduino hosts; that is not
required for a native 3.3 V ESP32-S3 custom board.

The public TROPIC01 API and current `libtropic`/`libtropic-arduino` surfaces
cover P-256/ECDSA and Ed25519/EdDSA. They do not expose secp256k1 Schnorr or
BIP-340 today. nSealr should still preserve a clean future branch for vendor
provided Schnorr support once Tropic Square ships or documents it.

## Required Evidence Before KiCad

- ESP32-S3 firmware can complete trusted review and physical approval with
  production signing still disabled.
- TROPIC01 secure session, identify, random, pairing-key, and MAC-and-Destroy
  flows run on a devkit or shield.
- The key-wrap/unlock model documents exactly when Nostr private key material
  enters ESP32-S3 RAM.
- Display size and navigation are accepted against complete event review pages.
- USB power, regulator current, thermal margin, ESD, fuse, and debug/provisioning
  requirements are documented.

## Repository Artifacts

- `pcb/custom-persistent-secret-wallet/requirements.json` defines the checked
  Rev A hardware requirements.
- `bom/custom-persistent-secret-wallet.csv` defines the first component-class
  BOM scaffold.
- `scripts/validate_hardware.py` rejects unsafe claims such as air-gapped USB
  operation, current TROPIC01 BIP-340 signing, or Rev A battery interfaces.
