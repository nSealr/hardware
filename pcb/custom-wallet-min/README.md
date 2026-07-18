# custom-wallet-min

Minimal custom hardware-wallet board (`custom_hardware_wallet`, decision spec §2 #5 + §3).
This directory currently holds the **KiCad project skeleton only** — a hierarchical schematic split into
five subsystem sheets, an empty-but-valid board file, and the project lib-tables. Component symbols with
verified pin numbers and full wiring land in later Phase 02 tasks; the design notes and
`netlist-contract.json` follow after that.

The two **layout-variant BOMs** are authored and validated:
[`custom-wallet-min-core-behind-display.csv`](../../bom/custom-wallet-min-core-behind-display.csv)
(variant **A** — core behind display + **FPC** connector `J3`, Hirose `FH12-18S-0.5SH(55)`) and
[`custom-wallet-min-core-with-display.csv`](../../bom/custom-wallet-min-core-with-display.csv)
(variant **B** — panel mounted directly, `J3` is a **board-to-board panel-tail** connector, Hirose
`DF40C-18DP-0.4V(51)`). Both BOMs share **one electrical core** (one schematic + one firmware) and differ
**only in the `J3` display-mount row**.

## Scope

- **All-SMD.** No through-hole assembly; turnkey-sourceable parts only.
- **Host:** ESP32-S3-WROOM-1-N16R8 with an on-board physical **confirm button**. Secure Boot v2 +
  Flash Encryption eFuses are burned at provisioning (config policy, not a placed part).
- **Secure elements:** **TROPIC01** (`TR01-C2P-T310`) is the mandatory open vault (SPI + host power-cycle
  control — hardware PIN anti-bruteforce, TRNG/PUF, attestation). A **2nd-vendor SE is populated by
  default** for Coldcard-style key-split: **OPTIGA Trust M** on I²C is the real BOM line; **ATECC608B** is
  the alternate footprint and **DNP applies only to the alternate**.
- **Firmware signs (SE-as-safe).** The Rust firmware signs secp256k1 ECDSA + BIP-340 Schnorr. The secure
  elements are an **encrypted vault behind a hardware PIN** with the decryption key split MCU ⊕ SE(s); the
  seed is unwrapped into RAM only at sign time and wiped after. **There is no in-SE signing on this board**
  ("all-signatures-in-SE" is an explicit non-goal here; in-SE signing lives only on the smartcard solution).
- **Display-agnostic.** The MCU renders to an external "dumb" SPI panel over an **FPC connector** (curated
  ST7789 / ST7789V2 / ST7796 driver family) with CST816 touch on I²C. Reference panel: Waveshare 1.69"
  ST7789V2 + CST816 (external, consigned — not a placed panel on this board).
- **Two layout variants** share one schematic and one firmware, differing only in the display mount:
  **A** = core-behind-display + FPC, **B** = core-with-display.
- **Power / USB:** USB-C receptacle (GCT `USB4105-GF-A`) + ESD array + 3.3 V LDO. USB-C is the primary power
  source **and the only signing transport in v1**.
- **Battery-operable:** MX1.25 2-pin LiPo connector `J5` (Waveshare convention; battery user-supplied /
  optional), **BQ24074** power-path charger `U5` (seamless USB/battery), and **MAX17048** fuel gauge `U6`
  (I²C, downstream of the LDO).
- **Gated expansion:** a SPI/I²C/GPIO 0.1" header **and** a **Qwiic / STEMMA-QT JST-SH 4-pin I²C port** `J6`
  (`SM04B-SRSS-TB`) — both **default-off**, explicit opt-in only.
- **General open SE platform** (Bitcoin / Nostr / SSH / PGP / FIDO / generic), useful to any maker.

## Explicitly out of scope

- **No JavaCard, no card socket, no ISO 7816, no SE051.**
- **No NFC.**
- **No camera.**
- **No wireless data path.** BLE silicon is present in the WROOM module but **disabled by default** (never in
  a high-assurance profile); **WiFi is never used**; there is **no wireless update path** on any nSealr device.

## Fabrication gate

**Fabrication and bring-up are Phase 10.** This board stops at the design-complete gate (ERC = 0, DRC = 0,
validator + release gates). **Do not fabricate before the Phase 10 bring-up.**

## Layout

```
kicad/
  custom-wallet-min.kicad_pro     project file
  custom-wallet-min.kicad_sch     ROOT sheet (instantiates the five sub-sheets)
  custom-wallet-min.kicad_pcb     empty-but-valid board (layout in Phase 10)
  sym-lib-table / fp-lib-table    project libraries (minimal; global libs only for now)
  sheets/
    host.kicad_sch                ESP32-S3 host, strapping, confirm button, fuse policy
    secure_elements.kicad_sch     TROPIC01 + OPTIGA Trust M (ATECC608B alternate, DNP)
    display.kicad_sch             display-agnostic SPI panel over FPC + CST816 touch
    power_usb.kicad_sch           USB-C + ESD + LDO + BQ24074 + MAX17048 + MX1.25 LiPo
    expansion.kicad_sch           gated 0.1" header + gated Qwiic JST-SH I²C port
```

Built and verified with KiCad 10.0.3 (`kicad-cli`).
