# custom-wallet-min — Design Notes

Human design notes for the KiCad board **`custom-wallet-min`** — the general open secure-element platform that
the product **nSealr One** (`custom_hardware_wallet`, decision spec §2 solution #5) is built on. The board name
is deliberately generic ("useful to any maker"); the product is the device, the board is its platform.

These notes are the **decisions behind** the electrical-intent contract. Read them first, then the contract:

- Contract: [`../production/netlist-contract.json`](../production/netlist-contract.json) (required buses + release gates)
- BOM variant **A** (core-behind-display + FPC): [`custom-wallet-min-core-behind-display.csv`](../../../bom/custom-wallet-min-core-behind-display.csv)
- BOM variant **B** (core-with-display, direct panel): [`custom-wallet-min-core-with-display.csv`](../../../bom/custom-wallet-min-core-with-display.csv)
- Board overview: [`../README.md`](../README.md)
- Spec: [`2026-07-14-nsealr-five-solution-device-matrix-design.md`](../../../../docs/specs/2026-07-14-nsealr-five-solution-device-matrix-design.md)
  §2 (five solutions), §2.1 (assurance ladder), §2.2 (SE roles), §3 (hardware/MCU/SE/language rationale),
  §3.1 (platform trust), §6 (open decisions).

This board is a **design-only** deliverable for Phase 02. Schematic capture with datasheet-verified pins, ERC and
DRC land in **Task 04**; fabrication and bring-up are **Phase 10**. Nothing here orders a board.

---

## 1. Scope and assurance role (§2, §2.1)

`custom-wallet-min` is the flagship, **mainstream-tier** device: a *hardened firmware signer with an SE-backed
vault, key-split, and a trusted display*. On the §2.1 assurance ladder it sits **above** the connected software
signer (solution 4, nSealr Key — no discrete SE) and **below** the in-chip signer (solution 3, nSealr Card —
JavaCard, signs inside the card). This is the **Trezor/Coldcard tier**: the firmware signs, and secrets live in
an encrypted vault behind a hardware PIN with the decryption key split across chips.

Design constraints (all deliberate):

- **Minimal, all-SMD, turnkey-sourceable.** No through-hole assembly; the only consigned item is the external
  display panel.
- **Display-agnostic.** The security core renders to a "dumb" external SPI panel it drives itself (WYSIWYS
  preserved), so the core can sit behind any screen.
- **One electrical core, two layout variants.** One schematic + one firmware; the variants differ only in how the
  panel is mounted.
- **Battery-operable**, USB-C-primary, USB-only signing in v1.
- **General open SE platform** — Bitcoin / Nostr / SSH / PGP / FIDO / generic — useful to any maker.

---

## 2. Subsystem rationale

| Subsystem | Part(s) | Rationale |
|---|---|---|
| Host MCU | **ESP32-S3-WROOM-1-N16R8** (`U1`) | Native USB, largest maker sourcing/ecosystem, Secure Boot v2 + Flash Encryption. 16 MB flash / 8 MB PSRAM top-bin. The nSealr One firmware is its own crate `apps/one`, reusing the shared `nsealr-core` signing core together with `apps/key` (same ESP32-S3 core), with the vault + hardware PIN + key-split layered on top (§3). |
| Open vault SE | **TROPIC01 `TR01-C2P-T310`** (`U2`) | Mandatory open/auditable encrypted seed vault: hardware PIN anti-bruteforce, TRNG/PUF, X25519 secure channel, attestation, and Ed25519 / P-256 ECDSA for auxiliary SSH / FIDO2 / age / device-attestation use (§2.2). SPI + host power-cycle control. |
| Key-split SE | **OPTIGA Trust M `SLS32AIA010MS`** (`U3`), populated; **ATECC608B** alternate footprint, **DNP** | 2nd-vendor, vendor-diverse SE so no single chip holds the plaintext decryption key (§2.2). I²C. A build populates exactly one 2nd-vendor SE; the DNP designation applies **only** to the ATECC608B alternate footprint. |
| Display | External panel over `J3`; **CST816** touch on I²C | Curated driver family ST7789 / ST7789V2 / ST7796 via a board-profile registry. Reference panel: Waveshare 1.69" ST7789V2 + CST816 (consigned accessory, not a placed part). |
| USB / power | USB-C `USB4105-GF-A` (`J1`) + **USBLC6-2SC6** ESD (`D1`) + **AP2112K-3.3** LDO (`U4`) | USB-C is the primary power source and the only signing transport in v1. |
| Battery | MX1.25 LiPo `53398-0271` (`J5`) + **BQ24074** power-path charger (`U5`) + **MAX17048** fuel gauge (`U6`) | Seamless USB/battery; battery cell user-supplied / optional (§3, §7). |
| Confirm | **Omron B3U-1000P** tactile (`SW1`) | On-board physical confirm/approve — the trusted-consent input (not the external touch). |
| Expansion | Gated 0.1" header (`J4`) + gated Qwiic JST-SH `SM04B-SRSS-TB` (`J6`) | Both default-off maker ports. |
| Programming | Tag-Connect TC2030 pads (`J7`) | Bench serial console / bring-up only; the field update path is USB-C DFU, not these pads. |

---

## 3. Secure-element roles — "SE-as-safe", not "SE-as-signer" (§2.2)

The board composes secure elements as **vault + key-split + attestation**, never as the signer:

| SE | Role | In-chip capability used |
|---|---|---|
| **TROPIC01** (mandatory, open) | Encrypted seed vault + anti-brute PIN gate + entropy + attestation + auxiliary SSH/FIDO signer | TRNG, PUF, PIN anti-bruteforce, X25519 secure channel, Ed25519 / P-256 ECDSA (SSH, FIDO2/P-256, age, device attestation) |
| **2nd-vendor SE** (populated, key-split) | Multi-vendor key-split so no single chip holds the plaintext decryption key | Secret storage behind auth — OPTIGA Trust M (populated) or ATECC608B (alternate, DNP); vendor-diverse from TROPIC01 |

With the 2nd SE populated (the default), the vault's decryption key is split **MCU ⊕ TROPIC01 ⊕ OPTIGA** — the
configuration the spec §7 headline acceptance runs.

---

## 4. The firmware-signs model (SE-as-safe)

Bitcoin/Nostr **secp256k1 ECDSA + BIP-340 Schnorr are signed by the Rust firmware** (`k256` / `rust-secp256k1`),
with **deterministic-k (RFC 6979)** and **anti-klepto (sign-to-contract)** so a compromised device cannot exfil
the key through biased nonces. The signing flow:

1. The user authenticates with the **hardware PIN**, enforced by TROPIC01 anti-bruteforce (escalating delays;
   configurable wipe-after-N).
2. The seed is **unwrapped from the TROPIC01 vault into RAM only at sign time**. The vault's decryption key is
   **split MCU ⊕ SE(s)** (Coldcard model), so no single chip ever holds the plaintext seed at rest.
3. The firmware signs, showing the transaction/event on the **trusted display**; the user approves with the
   **on-board physical confirm button** (never the touch panel).
4. The seed is **wiped from RAM** after signing.

**"All-signatures-in-SE" is an explicit non-goal on this board.** In-element signing (the private key never
leaving an SE, every signature produced in-chip) is the release gate of **solution 3, the smartcard (nSealr
Card)** only — a separate device. This board must **not** introduce that gate. TROPIC01's own Ed25519 / P-256
ECDSA is used for auxiliary SSH / FIDO2 / attestation, not for the Bitcoin/Nostr secp256k1 signing path.

---

## 5. Key-split provision (§2.2)

The 2nd-vendor SE footprint is **provisioned so the decryption key can be split MCU ⊕ SE(s)**. OPTIGA Trust M is
the populated BOM line (`U3`); ATECC608B is an alternate footprint carrying the DNP designation. A build populates
exactly one 2nd-vendor SE — never both. This is the `key_split_provision` release gate: it is met by the presence
of the placed 2nd-vendor SE, independent of the ERC/DRC gates.

---

## 6. Display-agnostic FPC + the A/B layout-variant delta (§3)

The MCU renders to an external "dumb" SPI panel from the curated **ST7789 / ST7789V2 / ST7796** driver family, with
**CST816** touch on I²C (touch is informational/UI only — never accepted as approve/reject consent). The security
core is small and sits behind any screen. Two layout variants share **one schematic and one firmware** and differ
**only in the `J3` display-mount row**:

- **Variant A — core-behind-display:** compact security board + **FPC** flat cable to any external panel
  (`J3` = Hirose FH12-18S-0.5SH(55), 18-pos 0.5 mm FPC). Maximum display-agnosticism.
- **Variant B — core-with-display:** a display-sized board with the panel mounted directly, no flat cable
  (`J3` = Hirose DF40C-18DP-0.4V(51) board-to-board panel-tail). Same electrical design, different enclosure.

Both BOMs are otherwise identical; the layout variant is purely the connector type at `J3`.

---

## 7. Power-subsystem rationale (§3)

- **USB-C** (`J1` GCT USB4105-GF-A + `D1` ESD) is the primary power source **and the only signing transport in
  v1**.
- **Battery-operable:** an **MX1.25 2-pin LiPo connector** (`J5`, Waveshare convention; the cell is
  user-supplied / optional and is **not** a placed BOM row) feeds a **BQ24074** power-path charger (`U5`) that
  charges over USB-C and runs the board seamlessly on either source (dynamic power-path). A **MAX17048** fuel gauge
  (`U6`, I²C, downstream of the LDO) reports state-of-charge. The **AP2112K-3.3** LDO (`U4`) provides the 3.3 V
  rail downstream of the BQ24074 system node.
- This is the r3 spec §3 design (MX1.25 + BQ24074 + MAX17048), **not** a legacy nPM1300 carry-over.

The `battery_option_power_path` release gate is met by the presence of `J5` + `U5` + `U6`; the battery cell itself
being user-supplied/optional does not gate the design.

---

## 8. Connectivity policy (§3, §3.1)

- **USB-C is the only signing transport in v1.** All signing and field DFU go over USB-C.
- **BLE** silicon is already inside the WROOM module (zero BOM cost), but it is **disabled by default and out of
  scope for v1**. NIP-46-over-BLE is reserved as an explicitly-flagged, opt-in **future** feature for the
  battery-powered use case, and is **never** enabled in a high-assurance profile (spec §6 [DEC], default
  off/future opt-in).
- **WiFi is never used.**
- **No wireless update path exists on any nSealr device.** The ESP32-based devices (solutions 2, 4, 5) update via
  **USB-DFU through the Hub**, signature-verified against the burned root of trust with eFuse anti-rollback in
  secure mode (§3.1).

---

## 9. Expansion and Qwiic gating design (§3)

Two maker ports, both **default-off** so they add no attack surface when unused:

- **Gated 0.1" SPI/I²C/GPIO header** (`J4`): the bus is exposed only via series jumpers (unpopulated) / a load
  switch, so it is isolated unless deliberately enabled.
- **Gated Qwiic / STEMMA-QT JST-SH 4-pin I²C port** (`J6`, JST SM04B-SRSS-TB): standard Qwiic pinout
  (GND / 3V3 / SDA / SCL), isolated default-off, opt-in only.

Gating is explicit opt-in; neither port is live in a shipped high-assurance profile unless the owner enables it.

---

## 10. Secure Boot v2 / Flash Encryption (§3.1)

The ESP32-S3 host supports **Secure Boot v2 + Flash Encryption**. These are **eFuse policy, not placed parts**:
dev units ship **eFuse-virgin (unlocked)** — full JTAG/flash freedom, the maker-platform promise — and **secure
mode** is entered by an owner-run, Hub-guided provisioning flow that burns the eFuses with the owner's choice of
root of trust (their own key, or the nSealr release key). Burning is irreversible. Genuine-check uses the
TROPIC01 factory attestation cert chain (Tropic Square CA) verified locally, no phone-home. The
`secure_boot_v2_flash_encryption_fuses` gate is therefore **designed-in now** and **exercised at provisioning
(Phase 10 / §3.1)**.

---

## 11. Explicitly out of scope

Matching the board README and spec §2 (decision "drop JavaCard; firmware signs"):

- **No JavaCard, no card socket, no ISO 7816, no SE051.** In-element signing lives only on the smartcard
  product (solution 3).
- **No NFC.**
- **No camera.**
- **No wireless data path.** BLE present but disabled by default (never high-assurance); WiFi never; no wireless
  update path.

(The netlist contract states these same exclusions in non-triggering wording — "no near-field radio interface, no
image-sensor input, no card socket / applet path" — so its forbidden-token grep stays clean; the plain-language
list lives here and in the board README.)

---

## 12. General open SE platform framing (§2.4, §3)

The board is a **general open secure-element platform**: Bitcoin, Nostr, SSH, PGP, FIDO, and generic secret use.
The KiCad board name `custom-wallet-min` is frozen and kept generic to honour the "useful to any maker" goal; the
product built on it is **nSealr One** (firmware crate `apps/one`).

---

## 13. Release-gate map (contract ↔ this phase)

The contract's `release_gates` encode this phase's definition of done **and** the Phase 10 physical gate, in the
mainstream **SE-as-safe + firmware-signs** model. Status at the end of Task 03:

| Gate | Status now | Satisfied / verified at |
|---|---|---|
| `manual_datasheet_pinmux_review` | deferred | Task 04 (schematic capture binds MCU pins from datasheets) |
| `no_llm_invented_pin_numbers` | met (in force) | Honoured here (contract is logical-intent, no pin numbers); finally checked at Task 04 |
| `kicad_erc_pass` (ERC=0) | **deferred — NOT claimed** | Task 04 (no wired schematic exists yet; not run) |
| `kicad_drc_pass` (DRC=0) | **deferred — NOT claimed** | Task 04 (board is empty-but-valid; not run) |
| `all_smd_turnkey_sourcing` | met | Both BOMs are all-SMD turnkey; only the external panel is consigned |
| `tropic01_present` | met | BOM `U2` = TR01-C2P-T310 (mandatory open vault) |
| `key_split_provision` | met | BOM `U3` = OPTIGA Trust M populated; ATECC608B alt footprint DNP |
| `secure_boot_v2_flash_encryption_fuses` | deferred (designed-in) | eFuses burned at secure-mode provisioning (Phase 10 / §3.1) |
| `onboard_confirm_button` | met | BOM `SW1` = Omron B3U-1000P on-board tactile |
| `battery_option_power_path` | met | BOM `J5` + `U5` + `U6` present; cell user-supplied/optional |
| `no_fabrication_before_phase_10_bringup` | met (in force) | Physical gate honoured — no board ordered; released only at Phase 10 |

The two live-verifiable KiCad gates (`kicad_erc_pass`, `kicad_drc_pass`) are **not** claimed as passing: they are
satisfied only in Task 04 when a real wired schematic/board exists and ERC/DRC actually run (ratchets only tighten;
never claim a number without a run).

---

## 14. Open-decisions log (spec §6 defaults in force)

| # | Decision | Default / status |
|---|---|---|
| §6.1 | Public naming / trademark | **RESOLVED 2026-07-17** — products nSealr Vault / Card / Key / **One** + nSealr Hub; the `custom-wallet-min` board name unchanged |
| §6.2 | Duress/decoy-wallet PIN on the custom | Default **v1.1** (designed-for, not in the v1 gate) [DEC] |
| §6.3 | NIP-46-over-BLE (battery use case) | Default **off / future opt-in**, never in high-assurance profiles [DEC] |
| §6.4 | TROPIC01 production silicon | **RESOLVED 2026-07-18 → `TR01-C2P-T310`** (sole MPN; T301 dropped, T10x samples excluded). BOM line frozen (`freeze_status: frozen`). Clears the Phase 10 fabrication precondition on this [DEC] |

Resolved earlier (2026-07-15, §6): all-Rust; drop JavaCard → mainstream SE-as-safe + firmware-signs;
display-agnostic + two layout variants; battery-operable + Waveshare-style ports, USB-only signing in v1;
2nd-vendor key-split SE populated by default (OPTIGA populated / ATECC608B alt DNP); repo consolidation into the
`firmware` cargo workspace; §2.3 secret-lifecycle matrix; §3.1 platform-trust model.
