# H01 bounded option comparison

Research state on 2026-10-18; **no component selection or host admission**.
The current U5 reference-manual gap prevents H01 completion. The alternatives
below remain useful investigations, with different promotion criteria. They are
not a security ranking. Evidence IDs resolve in [the register](manual-register.json);
stable requirements, negative cases and closure owners are in [claims.json](claims.json).

The product boundaries are the accepted [P01 requirements](https://github.com/nSealr/nsealr/blob/7b5553685dac56029a4379be12054154b6b5e0b5/docs/restart/implementation/P01/requirements.md)
and [threat models](https://github.com/nSealr/nsealr/blob/7b5553685dac56029a4379be12054154b6b5e0b5/docs/restart/implementation/P01/threat-models.md).
The generic Board SDK has no Nostr dependency. Its first execution model is one
trusted firmware image. The separate Signer profiles remain commercial ESP32
without SE over USB, offline Pi, offline P4, and initially connected custom Board.
No SE does not mean automatically compromised; an SE does not establish a trusted
display, valid consent, secure host firmware or hostile-application isolation.

## MCU triage

| Investigation | Concrete benefit and constraint | Decision condition and remaining evidence |
| --- | --- | --- |
| **STM32U585VI / VIQ** | 160 MHz M33, internal flash, TrustZone-capable ownership, modest SPI UI and USB FS are plausible. DS13086 Rev10 gives 722 KiB total SRAM with SRAM3 ECC enabled, including backup/autonomous banks; not all bytes are interchangeable secret RAM. The 100-pin VI/VIQ XML witness exposes useful independent peripheral buses. | Retain as the main U5 investigation. Require RM0456 Rev7, current DS electrical/AF and ES0499 selected body review. Compare actual usable memory/stack/UI/USB/crypto, owner root replacement and recovery. Q power pads are not interchangeable with non-Q. Reject or promote a memory alternative on measured/linked workload evidence, not an arbitrary GPIO total. |
| **ESP32-S3-WROOM-1-N8R8** | Exact comparator lead: dual LX7, 512 KiB internal SRAM with cache/instruction/data distinctions, external 8 MB flash and 8 MB octal PSRAM, integrated radio, USB FS. Public functional TRM/errata/SDK are accessible; comprehensive USB register specifications have the §32.5 NDA boundary. Module memory consumes GPIO35–37. Internal secret arenas, radio/SAR ownership and USB's separate bus master need deliberate design. | Retain comparator; pin proposed silicon/module/kit configuration. GPIO/watchdog/XTS reading advanced, but selected SPI/USB/boot contradictions and driver correspondence remain. Exact dependency/access questions affect viability. External PSRAM is not an internal secret budget; vendor ephemeral-AES assumptions do not cover an enduring wrapping key. |
| **STM32U5G9ZJ** | Mandatory UI/platform comparison: DS14102 **Rev5 May2026**, materially larger banked RAM, DSI/LTDC and graphics masters. Current OPN table distinguishes **ZJT6Q LQFP144** from **ZJJ6Q UFBGA144**, both SMPS leads. DK2 corroborates ZJT6Q/3.3V/RGB; DK1 is a different package/supply reference. | Promote only if review/recovery or SDK workload benefits and exact pad/rail/AF, current RM master ownership, driver/license and manufacturing budgets close. Defer if a modest UI meets the need. Selected DS power/graphics/ordering and ES0595 DSI/SAES bodies are now read; configuration qualification remains. Safe7 use is not selection evidence. No new bench port. |
| **STM32U5A5VJ** | DS13543 Rev3 family memory screen provides a conditional larger-RAM path; VJ package/feature differences must be resolved rather than inheriting A9 graphics claims. Same broad M33 ecosystem can reduce a later port's work. | Conditional promotion only if U585's internal-memory/workload budget fails and A5's exact package/features beat the already-required G9 triage. DS/RM/ES0553 selected review and exact OPN are incomplete. No second full U5 port merely for catalogue coverage. |
| **STM32H573** | Current DS14121 Rev5 feature screen and preserved RM0481 Rev5 §3.11 expose a distinct lifecycle/debug-authentication approach; 250 MHz M33 and internal flash are relevant. Its 640 KiB main SRAM does not solve every large-framebuffer requirement. | Conditional lifecycle alternative. Promote only if an explicit owner/debug/recovery requirement cannot be met satisfactorily by retained hosts. Exact OPN, current ES0565, ST-iROT versus owner firmware authority and all used peripheral/manual paths remain open. SA0055's H523/533 applicability must not be transferred to H573. |
| **ESP32-P4** | Document-only screen of dual RISC-V, larger UI interfaces (DSI/CSI), USB HS/FS and package PSRAM. Separate P4 QR profile remains valid work. A kit's companion radio is a different component. | No replacement of the H02 U5/S3 scope. Exact revision/algorithm matters: ROM-764, ROM-770/816 and ECDSA_DS-836/837 have different applicability. A configuration that avoids an erratum by removing a required boot guarantee is not admitted. Current esp-hal source's P4 feature targets v3.x; that is not proof of a complete secure application or panel driver. |
| **Classic ESP32** | DS v5.3 feature screen: LX6, Wi-Fi/BT and mature ecosystem; it is a different SoC, memory/peripheral/security architecture from S3. Some older ordering codes are NRND/EOL. | Preserve the commercial ESP32 profile while requiring its exact module/board and transport contract. No new H01 port. Do not copy S3 native USB/TRM/boot assumptions into classic ESP32 or collapse the family names. |
| **MCXN947** | One non-ST screen: DS MCXNP184M150F70 Rev8.2 pp.1–6 identifies dual M33, up to 512 KiB SRAM (416 KiB with ECC), HS/FS USB, FlexIO and multiple DMA engines. MCXN947VKLT is HLQFP100; VDFT is VFBGA184; VPBT is HDQFP172. The older VNLT suffix is deprecated. | Defer additional port. No decisive internal-UI-memory advantage established, and reference/security manuals are account-required (catalogue Rev7/Rev6). Second core, enclave and accelerators require exact ownership/lifecycle review, not feature-count credit. Promote only on a concrete requirement advantage plus reproducible developer/manual access. |

Manufacturer headlines are not energy, throughput or security measurements. This
comparison does not compare vendor marketing benchmark numbers with unlike
conditions. A 240×320 RGB565 framebuffer is **150 KiB**; two 480×480 RGB565 buffers
are **900 KiB**, before stacks, fonts, USB and cryptography (H01-C04). Strip/tile
rendering can reduce memory at the cost of bandwidth and scheduling constraints.
P01's complete review and local recovery requirements decide whether it is usable.
Camera buffers from an offline profile are not compulsory custom-Board overhead.
DK2's 800×480 size would require 750 KiB per RGB565 framebuffer, or 1500 KiB
for two, before other allocations. This calculation is not a reason to adopt its
panel or proof that either host can meet a particular refresh/latency budget.

## Toolchain and firmware-owner implications

The fresh source screen pins Embassy to
[`69006a4`](https://github.com/embassy-rs/embassy/tree/69006a4158aa6d605ad8506ade0f2f79159131e3).
Its `embassy-stm32` feature list includes U585VI, U5A5VJ, U5G9ZJ and H573, and
`src/lib.rs` declares DSI, LTDC, GPU2D, DMA2D, GFXMMU, RNG and UCPD modules behind
configuration gates. Therefore an assertion that U5G9 has no Rust display support
would be unsupported. These declarations **do not prove** the exact chip feature
combination, graphics dependency licensing, secure attribution, performance or
build. A selected, maintained narrow vendor C adapter is allowed where it reduces
risk; it must have a pinned ABI, license, invocation and error path. No mandatory
all-Rust rule is inherited.

The fresh esp-hal screen pins
[`8ef1b67`](https://github.com/esp-rs/esp-hal/tree/8ef1b6716f48cfe34f7e0dd8cbcf738ce236da13).
That manifest reports version 1.2.0 and Rust 1.95.0, with S3 and P4 feature entries;
HEAD is an observation, not a selected release. Espressif's
[toolchain guide](https://docs.espressif.com/projects/rust/book/getting-started/toolchain.html)
requires the Espressif Xtensa toolchain for classic ESP32/S3. Standard Rust
RISC-V support does not by itself establish P4 HAL/USB/boot coverage. H02 must pin
compiler, target, HAL/PAC, linker script, vendor component revisions and complete
binary/map/ABI evidence. H01 performed no new target build or board port.

Development, owner-secured and product-qualified states need separate contracts.
For S3, digest revocation and finite antirollback fuse bits constrain future owner
root replacement. Flash encryption and app A/B update do not make every bootloader
or data-partition update atomic. For U5, current option-byte/regression behavior
must be reviewed before adopting an owner transition. Recovery must state what is
erased, what survives and which credential is needed; a “factory reset” label is
not sufficient. Identity backup and firmware-owner recovery are different secrets.

The follow-up [source notes](host-subset-notes.md) distinguish vendor RNG/sleep
source correspondence from a qualified Board implementation. They also show why
an esp-usb wrapper commit is insufficient without the underlying TinyUSB lock
and actual configuration. Current U585 USB errata likewise require exact driver
inspection; accessible S3 source is not a reason to discard the U5 comparison.

## SE and developer-access triage

| Candidate | Useful investigated services | Selection gate |
| --- | --- | --- |
| **SE051C2** | Public DS/configuration and AN12907 support a bounded algorithm/configuration/update-authority screen. Exact OPN, OEF and applet tuple remain unresolved. | AN12543 Rev4.5 API, errata Rev1.1 and current middleware/personalization/update terms are mandatory access gaps. Public headers are not an API or errata substitute. Obtain lawful access and reproducible developer rights before H02S selected-service claims or H04 selection. |
| **Standard OPTIGA Trust M V3** | Reviewed DS algorithm/pin excerpts, reference-manual HMAC/authorization/derivation sections and release/I2C document inventory. | No native BIP340 or non-exportable Nostr ECDH established. Exact standard order code, firmware/maintenance version, object metadata/channel/reset/counter policies and update delivery remain open. Firmware maintenance and host recovery/concurrency requirements need actual qualification. A wallet's customized part is not automatically the standard purchasable part. |
| **TROPIC01** | Public pin/algorithm/API, PIN-construction and pairing documents plus four devkit schematics improve inspectability. Host persistent state and default pairing replacement are explicit work. | Advisory ODR_TR01_SA_2026012900 v1.0, public **2026-06-03**, includes **T310** and the recorded firmware tuple. No qualified fix established. Future hardened-part forecasts and disclosure dates cannot close intended asset protection. Public source has bootloader/IP limits; “open” does not mean every layer is published. |

None is admitted as a native Nostr signer solely from an ECC label. BIP340, ECDSA,
Ed25519 and a generic ECDH service are different contracts. H02S must test the
exact curve/command/object-policy tuple and observe which material reaches host
memory. A wrapping/PIN design must account for host plaintext, persistent attempts,
reset, rollback and interrupted writes. Two SEs require a demonstrated composition
argument; merely adding both does not yield independent protection (H01-C16–C19).

These SE gates do not block independent MCU/USB/UI research. They also cannot be
silently converted into accepted compromises while the associated guarantee is
advertised. The present U5 host gate is an independent missing-manual problem.

## Power, USB, UI and expansion

Retain **at most two** power-chain investigations for H03:

1. **BQ24074 linear power path + TPS63802 3.3V buck-boost.** A simpler control
   path and absent-battery operation are useful. Validate worst-case charger
   dissipation, input-limit straps, system-versus-charge priority, protected-cell
   cutoff and regulator startup/load transient across the usable cell range.
2. **BQ25628 switching power path + TPS63802 where a fixed 3.3V rail is needed.**
   Investigate when thermal/current evidence justifies the extra control work.
   BQ25628's ILIM pin is not BQ25629's D+/D− function. Reset IINDPM and selective
   watchdog resets make a hardware-safe current limit/charge-enable state
   necessary before firmware can establish policy.

These are Li-ion/Li-polymer candidate chains, conditional on the exact protected
cell and charger configuration. They are not a LiFePO4 design. USB-only operation
must be assessed without assuming a battery buffers peaks. AP2112 is not a
full-cell-range 3.3V solution merely because its nominal output is 3.3V; dropout
and transient margin matter. nPM1300 is only a Safe7 reference cross-check, not a
third retained chain. No current, runtime or thermal result has been measured.

USB-C starts as a **5V sink**. TUSB320LAI supplies CC/current-class/dead-battery
functions, not an automatic PD power contract. Its pull-up domains, shutdown
state, VBUS sense network and current-status interpretation matter. An MCU UCPD
alternative consumes exact pins/dead-battery paths and requires current errata
review. Current USB-IF normative sink, default current, attach, suspend, inrush,
detach and backfeed clauses are still open; a release index or TI/SDK example is
not normative closure. A module's 0.5A supply-capability requirement is also not
permission to draw 0.5A immediately from any port.

First investigate a modest directly controlled SPI panel plus physical controls.
A larger DSI/LTDC path is justified only by readable full review/recovery or a
concrete SDK workload. Before admission record the **complete module/controller
revision**, connector/mating contact orientation, rail/logic limits, startup,
backlight current/control and touch/IRQ ownership. Controller-family names alone
are insufficient. The Safe7 RevD custom flex (DF37B 24-contact lead), separate
backlight and switched rails are a reference, not a universal FPC standard. Its
published U5G9 design and firmware revC mapping remain different evidence sets.

Maker SPI/I2C/UART/GPIO are useful only with documented pin/voltage/current/startup
contracts. Keep SE and trusted input/display paths private; define how development
firmware can reconfigure them and what the owner-secured Signer promises. The
[pin ledger](pin-errata-ledger.json) carries a bounded signal-presence witness,
explicit competing uses and unknown electrical/AF/master ownership. Camera and
NFC remain conditional modules with separate memory, power and attack-surface
costs. Neither is imported automatically from the Pi/P4 QR profiles.

## Reference correspondence

The Safe7 export whose filename says RevD and four TROPIC exports retain their original hashes and
only the previously inspected pages. TS1303's USB firmware is a command bridge,
not an isolated custody signer. Its plug wiring is not a two-orientation
receptacle reference. TS1401 translates the SPI signals but its GPO path is
separate; TS1501's GPO is GPIO5/physical29, not GPIO25; TS1702 has no host MCU or
regulator. Those distinctions guide later fixture wiring and prevent copying
reference assumptions into the custom Board. Full native CAD/BOM, assembly and
layout qualification have not been performed.
The distinct review found Safe7's display sheet (physical page13) has title-block
revision **C**. File naming, per-sheet revisions and firmware revision mappings
must be recorded independently before reusing a particular circuit.
