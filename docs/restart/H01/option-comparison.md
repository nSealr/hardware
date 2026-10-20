# H01 bounded option comparison

Research state on 2026-10-18; **no component selection or host admission**.
The current U5 original has been retrieved; remaining required body and
configuration review still prevents H01 completion. The alternatives
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

## Maintainer priority update, 20 October 2026

The generic programmable Board and Nostr-independent SDK have autonomous product
value. The maintainer now explicitly prefers a readable, responsive touchscreen
and asks for a concrete two-SE study, with a third only for a distinct verifiable
benefit. The retained six-contact/no-touch tuples are **comparison baselines**,
not an irrevocable product choice. This update preserves the accepted threat,
owner, manufacturing and physical gates; it does not select a touch controller,
MCU, SE pair or production design. Root coordinates any requirements/acceptance
changes; this document records the concrete delta inside existing H01 scope.

The exact [DB module product](https://newhavendisplay.com/2-4-inch-ips-tft-lcd/)
declares no touchscreen. Its 45-contact specification provides no touch path.
The already deferred AF breakout is also explicitly no-touch. Neither can meet
the new preference by interpreting `CTXP` as a touch-controller identity. No
neighboring product or extra display search is admitted by this observation.

| Few representative uses | Useful baseline capability to qualify | Concrete limit / decision evidence |
| --- | --- | --- |
| Instrument/status and local approval console | Bounded public records, small updated regions, SPI/I2C/UART SDK services with explicit pin/current/owner contracts; review followed by separate physical consent. | Existing C05 caps are16KiB incoming/result/review and one operation, not arbitrary record/history capacity. No measured latency or safely exported expansion bus yet; fitted kit branches and private UI/SE paths constrain routing. |
| Credential or key-operation agent | One trusted owner firmware can expose a protocol-independent bounded operation/review/error API. S02's maintained software backend remains relevant beyond Nostr. | No new credential protocol, native SE signature capability or concurrent hostile application is inferred. Actual algorithm/backend RAM/stack/time and secret copies need K01/H02;16KiB is a qualification cap, not a demonstrated usable maximum. |
| Local provisioning, backup and recovery | Private row buffer and local controls can specify secret entry/review without sending recovery pixels over public USB staging. | Six-button text entry is a usability constraint, especially for long recovery data. A touchscreen could improve navigation/entry; it still needs exact input ownership, layout/legibility/error handling and a dedicated sensitive confirmation decision. No touchscreen or recovery workflow is qualified here. |

The actual proposals are U585 MSIS48 (calculation45–51MHz), not its headline
160MHz, and S3 CPU160/APB80. At nominal U585 SPI 3 MHz a 153600-byte RGB565 full
frame takes **409.6ms on the wire**; S3 SPI 2.5 MHz takes **491.52ms**. A240×32
rectangle takes 40.96/49.152ms respectively, before commands, scheduling and
optical response. These lower bounds cannot establish smooth full-screen
interaction, touch responsiveness or animation. Optical module bounds are
separate, and source clock/reference conditions remain unsatisfied. A faster
unreviewed divider/driver is not selected to conceal the limit.

C05 deliberately allocates row rendering and separate public/private buffers,
not a framebuffer. Its public 64 KiB and secret 64 KiB groups, 64 KiB stack/backend,
separate runtime/code and finite residual margins are **qualification budgets**;
none proves future SDK headroom or full-workload fit. A 150 KiB RGB565 frame cannot
be inserted into an already allocated arena without a new map/ownership budget.
External S3 PSRAM remains excluded for secrets. U585 remaining SRAM is not a
free framebuffer claim: ECC, master attribution, capacity and effective linker
ownership must be accounted. The mandatory existing G9 comparison will assess
its larger-RAM/display path against these concrete UI limits, with GPU2D/
DCACHE2's nonsecure boundary retained. No arbitrary new MCU or additional port
is opened.

For touch comparison, navigation, text entry, recovery and scrolling deserve
quality/latency checks; sensitive approval still needs a screen-generation/
operation binding, fresh input epoch and a separately evaluated physical
confirmation. A touch event or button edge alone grants no authority. A general
Board may run owner-installed firmware, with clearly different guarantees from
the qualified Signer; SDK programmability does not establish safe coexistence of
untrusted apps. This distinction must survive C04's install/update/recovery and
owner-transition tables.

The next hardware decision needs the existing G9 source comparison plus a small
coherent configuration comparison under root's H04 gate: demonstrable UI/SDK
benefit, exact pins/rails/memory/master ownership, maintained source/licenses,
indicative cost with uncertainty, missing measurements and a recommendation.
The current exact raw-panel page showed **USD 19.58 on 20 October 2026**, for the
module alone, before tax/shipping/connector/translation/backlight/assembly and
quantity changes. This is a dated indication, not a quote, complete BOM cost or
reason to prefer the electrically/startup-unqualified no-touch module. No
purchase or new supplier inquiry follows. Independent S03/T01/Pi work continues;
the user's listed boards are an unverified inventory, not H01 test results.

## MCU triage

| Investigation | Concrete benefit and constraint | Decision condition and remaining evidence |
| --- | --- | --- |
| **STM32U585VI / VIQ** | 160 MHz M33, internal flash, TrustZone-capable ownership, modest SPI UI and USB FS are plausible. DS13086 Rev10 gives 722 KiB total SRAM with SRAM3 ECC enabled, including backup/autonomous banks; not all bytes are interchangeable secret RAM. The 100-pin VI/VIQ XML witness exposes useful independent peripheral buses. | Retain as the main U5 investigation. Complete the remaining RM0456 Rev7 body, current DS electrical/AF and used ES0499/driver correspondence. Native originals and selected core/system/RNG/USB reads are now available. Compare actual usable memory/stack/UI/USB/crypto, owner root replacement and recovery. Q power pads are not interchangeable with non-Q. Reject or promote a memory alternative on measured/linked workload evidence, not an arbitrary GPIO total. |
| **ESP32-S3-WROOM-1-N8R8** | Exact comparator lead: dual LX7, 512 KiB internal SRAM with cache/instruction/data distinctions, external 8 MB flash and 8 MB octal PSRAM, integrated radio, USB FS. Public functional TRM/errata/SDK are accessible; comprehensive USB register specifications have the §32.5 NDA boundary. Module memory consumes GPIO35–37. Internal secret arenas, radio/SAR ownership and USB's separate bus master need deliberate design. | Retain comparator; pin proposed silicon/module/kit configuration. GPIO/watchdog/XTS reading advanced, but selected SPI/USB/boot contradictions and driver correspondence remain. Exact dependency/access questions affect viability. External PSRAM is not an internal secret budget; vendor ephemeral-AES assumptions do not cover an enduring wrapping key. |
| **STM32U5G9ZJ** | Mandatory UI/platform comparison: DS14102 **Rev5 May2026**, materially larger banked RAM, DSI/LTDC and graphics masters. Current OPN table distinguishes **ZJT6Q LQFP144** from **ZJJ6Q UFBGA144**, both SMPS leads. DK2 corroborates ZJT6Q/3.3V/RGB; DK1 is a different package/supply reference. | Promote only if review/recovery or SDK workload benefits and exact pad/rail/AF, current RM master ownership, driver/license and manufacturing budgets close. Defer if a modest UI meets the need. Selected DS power/graphics/ordering and ES0595 DSI/SAES bodies are read; native package outlines inspected. DK2 PC13/LSE requires explicit avoidance/review. RM master overview is now read; GTZC/cache and exact allocation still remain. Safe7 use is not selection evidence. No new bench port. |
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

The [current manual/driver notes](current-manual-notes.md) identify product-specific
RNG configuration and bounded-error-policy gaps in the pinned Embassy path,
and trace actual TinyUSB device reset/FIFO/IRQ waits. These are implementation
requirements, not reasons to reject an entire language or MCU family.

The earlier [source notes](host-subset-notes.md) distinguish vendor RNG/sleep
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
advertised. The present U5 host gate is an remaining current-manual content and configuration review.

The two-SE study is a required **composition question**, not a device count.
Within the three retained approaches, two concrete pair hypotheses can structure
the existing S04/H02S review, without selecting or asserting their services:

| Pair hypothesis, unselected | Proposed distinct role / one-compromise question | Unchanged mandatory gate |
| --- | --- | --- |
| SE051C2 + standard OPTIGA Trust M V3 | Independently provisioned wrapping/authorization components, both required for at-rest release, with separately validated persistent attempt policies. If one is compromised, the other must enforce its own credential/policy rather than trust the first device's success flag. Exact algorithm/output combination is not chosen. | Exact SE051 OPN/OEF/applet/API/errata/update access is missing; Trust M exact order/firmware/object/channel/counter/reset/update behavior is unqualified. Neither independent PIN throttling nor a composable wrapping service is established for these exact tuples. |
| TROPIC01 + standard OPTIGA Trust M V3 | Separately paired TROPIC authorization/PIN-side construction plus an independent Trust M wrapping/authorization component. Define independent credentials, host state and reset/attempt persistence before crediting diversity or protection after one compromise. | Applicable TROPIC advisory/remediation gate remains unsatisfied, including T310. Pairing/PIN notes do not qualify an intended vulnerable custody state. Trust M exact-service gates remain. No retry or alternative tuple bypasses S04's disposition. |

Serial wrapping, XOR shares or a second approval bit are not assumed secure
compositions. The construction needs exact algorithms, output/non-exportability,
credential distribution, persistent rate-limit semantics, rollback and interrupted
writes. A corrupt host can capture PIN input, request both authorized services,
read reconstructed plaintext and change an operation unless the actual protocol
prevents it. Two at-rest components therefore do not themselves isolate signing
from the MCU or bind display content to the operation. Native BIP340 and
non-exportable Nostr ECDH remain unestablished; key-at-rest and signing/use
protection must be assessed separately.

For either pair, specify separate owner/vendor update authorities, replacement,
identity and credential recovery, atomic host journal, one-device outage,
developer-document access and repeatable maintenance. Failure needs a defined
recovery path without an unadvertised single-device fallback. The kit's shared
I2C2 and custom-package pad/reset/additional-function constraints are real
allocation costs, not a private
dual-SE implementation. No third device has a demonstrated distinct benefit;
none is recommended on a device-count argument. Exact-service study and the
unchanged S04/H02S gates precede any selection, custody or H04 freeze claim.

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


## Finite G9 comparison outcome, 20 October 2026

The [G9 source/pin/master comparison](g9-comparison-review.md) and
[decision](g9-comparison-proposal.json) supersede the open-ended G9 reading
statements above for their exact selected scope. Native MB1918 sheets2/3/4/9
prove B2 reaches PC13 while X1 is an LSE crystal; ES0595 prevents inheriting it
as an unaffected LQFP control/reference combination. The RGB/touch path costs
33 GPIOs plus shared NRST, with actual baseline pin conflicts. Bank capacities
support a concrete larger-framebuffer question, not free3MiB or measured fit.
GPU2D traffic/DCACHE2 remain nonsecure despite secure control registers; private
scanout and complete source/build/driver/license/fault/optical evidence remain
required. Maintained pinned Rust modules exist, with exact unbounded/error/
completion limits; no all-Rust mandate or external middleware license is inferred.

Retain the already mandatory G9 comparison for H04 because the new touch/SDK/
recovery preference has a material memory/UI rationale; defer promotion, MCU/
panel selection and any port until exact power/pins/SE/expansion/master/privacy/
clock/fit/module/quality/manufacturing/cost gates close. Exact G9/custom-BOM cost
is unknown. This does not freeze the old no-touch baseline, add a component
market search, relax S04/physical gates or impede independent software/Pi work.
