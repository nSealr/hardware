# H01 coverage and gates

Author review, 2026-10-18, `/root/h01_author`. Exact implementation still requires
a distinct reviewer. **No host configuration is admitted; H01 remains incomplete.**
The accepted brief and its approval are preserved unchanged. Register/claims
publication is useful progress, not a substitute for its completion criterion.

The first candidate received a distinct **request-changes** review, preserved in
[independent-review/report.md](independent-review/report.md). The author responses
are in [review-response.md](review-response.md); the limited follow-up review of6f95 is preserved in
[independent-review-followup/report.md](independent-review-followup/report.md).
The new current-manual/driver candidate needs another affected review.
[Current notes](current-manual-notes.md) give actual reading and remaining tasks.

Explicit maintainer resumption on 20 October 2026 supersedes the historical
pause. [Resumed source notes](resume-source-notes.md) record `/root/h01_resume`'s
additional current ICACHE/DCACHE, GPIO and IWDG body/register reading and
native kit drawing review. This advances selected evidence in the memory,
input, recovery and kit rows; it does not sign any complete host configuration.
All six documentary rows below remain incomplete.

The [U585 initialization contract](u585-initialization.md) and
[peripheral manifest](u585-peripheral-manifest.json) further bind the selected
current GTZC lock and RCC field reading. The 66 reset/clock rows and 64 TZSC
field correspondences are source-derived proposals, requiring exact-device
software correspondence and distinct review; they do not sign a complete row.

The [S3 fixed-CDC assessment](s3-usb-serial-assessment.md) adds a bounded
same-kit alternative with public register text and pinned vendor-source
correspondence. Stock overflow/reset/error and output-writer behavior prevent
selection now. AR2022-004's two separate ROM-download gates are newly read;
the controller choice, lifecycle, power/VBUS and six-row signoffs remain open.

[U585 SPI correspondence](u585-spi-review.md) advances the CPU-driven display
interface subset using current body/register text, errata and selected source.
Its exact bounded adapter, final panel/clock/hold tuple and complete bus/
interrupt coverage remain open. Reading this subset does not sign the row.

[U585 kit/boot correspondence](u585-kit-usb-boot-review.md) adds selected ROM
resource/watchdog and TCPP03 control reading, and checks sheet9 against native
CAD. The apparent U8 pin9/11 conflict is withdrawn; the sources agree. PF14's
analog divider still needs ADC4 or another fully specified sensing policy.
Boot/CC/I2C/reset/power and all six documentary signoffs remain open.

[U585 I2C/CC correspondence](u585-i2c-ucpd-review.md) advances the short
polling control contract, source-to-metadata checks and current register text.
It preserves revision limits and exact byte-count/deadline/recovery gaps in
the pinned I2C source. The UCPD constructor enables DMA requests and NVIC;
it is not equivalent to the proposed no-PD/no-DMA configuration. Final control,
clock, reset, low-power and interrupt policy remains open.

[U585 OTG source correspondence](u585-otg-source-review.md) adds selected
current CPU-FIFO, state/reset/interrupt and actual Rust device-path reading.
The ZLP erratum, effective USB time feature, failure propagation, buffer bounds
and VBUS override behavior prevent selecting the candidate driver now.
Remaining endpoint/control/model, interrupt/time-base and normative work remain;
this advances a subset and does not sign any complete host row.

[U585 interrupt/core-time reading](u585-interrupt-review.md) adds exact IRQ/
priority-width correspondence, field-specific security/masking and conditional
polling SysTick requirements. Its final handler/priority/clock/deadline tuple
remains unselected. The [finite closure checklist](closure-checklist.md) now
limits the remaining work to ten explicit H01 items, with H02/H04 work separate.

The [finite U585 endpoint/control table](u585-usb-endpoint-contract.md) closes
its selected reading/triage only. RM3269's OUT formula68 versus the pinned
driver64 remains an **unsatisfied interface property**, not a supported
conditional mode. No dependent enumeration/normal probe is admitted; class/IDs,
address on-wire correspondence and short-IN/errata/effective-adapter conditions
remain explicit before use. C03/C09 still bind complete TCPP/attach lifetime.

The [S3 SPI/control table](s3-spi-input-contract.md) completes that finite
selected source table, including the stock polling/cleanup/UPDATE and padded-tail
requirements, shared-core GPIO IRQ controls and conflict-warning behavior.
The underlying USB descriptor/route, clock/reference, lifecycle and physical
display/fixture stops remain. No whole host row is signed by this subset.

The [pin/electrical contract](pin-electrical-contract.md) adds the exact two-kit
signal/pad/header tables, installed mux/module source correspondence and normal
external rail/translation/contact/blanking requirements. It does not establish
unpowered isolation, radio quiet from POR or a complete custom LQFP100 design.
C03/C04/C09 and the unsatisfied display/USB/source conditions remain. The new
touchscreen/generic-Board priorities are a concrete comparison delta in
option-comparison.md; the old no-touch subset is a baseline, not a product freeze.

The [finite C03 system table](system-runtime-contract.md) specifies active
supply/reset/watchdog/IRQ/startup ownership and refusal guards. It explicitly
retains unsupported rail-valid and RC clock-loss timing inferences, conditional
clock/reference/effective-build limits, and the separate C04/C09 obligations.
Source/requirement-table completion does not sign a qualified clock, watchdog,
transport or complete power/host criterion.

## Host review sign-off matrix

[The finite entropy/crypto table](entropy-contract-review.md) supersedes the
older open-ended RNG source-reading scope for its exact retained paths. U585
nominal-HSI48/A is a conditional manufacturer reference with an explicit
coordinator H02 stop; S3's supported SAR lease needs exact source/ownership and
failure-observability qualification before use. The maintained software route
and backend-scratch gates are retained; unused accelerators are not new reading
tasks. This signs the conditional documentary table, not an entropy provider,
complete host row or physical result.

The [finite memory/ownership table](memory-ownership-contract.md) and
[allocation](memory-ownership-proposal.json) complete the C05 address/capacity/
copy/master proposal. Both hosts have separate secret data, secret stack/backend,
public transport/render and runtime partitions, with one pending operation and
row-only rendering. These are qualification caps, not measured product maxima.
The original input semantics and entropy stops remain; effective build/linker/
master/stack/clearing evidence belongs to H02 and the remaining host source
decisions remain in C01–C09. This does not sign the complete memory host row.

“Selected reviewed” below signs only the stated reading, not a complete probe or
measured result. Locators resolve through [manual-register.json](manual-register.json).

H01 documentary sign-off binds an exact **proposed** OPN/package, allowed
silicon revision and configuration requirements to reviewed manuals and errata.
It does not require an already-owned kit. H02 separately identifies the actual
received unit and confirms it meets that proposal before any physical probe.
Unknown received identity is therefore an H02 resource/execution gate, not a
reason to defer otherwise available H01 reading. The mandatory U5/S3 comparison
and current RM0456 Rev7 gate remain; admitting zero hosts cannot pass H01.

| Required row | U585 main investigation | S3 comparator | Review outcome / closure |
| --- | --- | --- | --- |
| Package/supplies/clock/reset/straps/electrical | DS13086 Rev10 selected features/SRAM/supply/reset excerpts; exact VI/VIQ XML pad witness. Current package/AF/electrical tables and remaining RM0456 Rev7 body incomplete; current native originals and selected clock/reset text now read. | Module1.8 pp.2–4,9–18,27–30; TRM1.8 chapters7–8 and selected GPIO supply/reset table; exact N8R8 lead. Exact v1.1 kit schematic now visually read; header allocation proposed. Two diode-ORed ports and absent native-USB VBUS sense constrain the fixture; remaining electrical requirements open. | Selected reading signed by author; **documentary admission open**. H02 later matches received marking/configuration. A 144-pin kit does not certify a 100-pin custom allocation. |
| Boot/flash/options/eFuse/debug/update/rollback/owner | Current Rev7 chapters3–4 and selected chapter7 lifecycle/options/protection body now read; proposed boot root/WRP/HDP/OEM transitions recorded in configuration-review.md. Final allocation/update/rollback/runtime policy remains open. | TRM §§5.1–5.3.3, chapter8; versioned IDF secure-boot/flash/OTA selections. Register/coding/download/update contradictions recorded. | **Open** H01 concrete lifecycle/configuration review, then H02 authorized sacrificial-unit tests. No irreversible operation performed or implicitly authorized. |
| Memory/ECC/cache/protection/buses/DMA | Current attribution/RAMCFG/ECC/cache source and exact-device manifest plus finite SRAM1/2 public/secret/stack/runtime allocation; all implemented SRAM secure/privileged, DMA/master exclusions and both MPCBB locks specified. Stock global init/effective calls require scoped remedies. | Selected memory/PMS/reset/clock controls, fixed SRAM1 alias-aware allocation and named DMA deny/lock policy; exact pinned app/bootloader linker bounds correspond. CPU0World0 only, CPU1 reset/gated, PSRAM/RTC/trace secret placement excluded. | C05 conditional documentary table signed by author; complete host row remains **open** pending C01–C09 package and distinct review. H02 effective map/features/masters/stack/peak/clearing/coexistence required. One trusted image, no hostile-app claim. |
| USB/display/input/GPIO/AF/interrupt/timer | Pin-signal witness plus current ES0499 selected SPI/USB/UCPD bodies. Current GPIO functional/register text §§13.1–13.4.13 now read; silent-zero reads, additional-function ownership and HSLV prohibition recorded. Remaining peripheral/interrupt/AF and exact driver correspondence stay open. | Selected GPIO matrix/interrupt/reset/IO_MUX text; SPI state/CS timing and bit-order contradiction; USB public functional text and pinned wrapper configuration. §32.5 comprehensive register specifications are NDA-limited. Pinned candidate TinyUSB device FIFO/reset/IRQ path now traced; effective build lock and bounded error policy plus kit/panel requirements remain open. | **Open** H01 exact bounded configuration. Unselected panel/controller has no wiring or performance approval. Software headers do not prove missing IP semantics. |
| RNG/health/crypto/backend | Current RM48 entire functional/register text and AN4230Rev14 selected configuration read; actual candidate RNG driver policy/waits have explicit gaps. Remaining used SAES/PKA/clock attribution not signed off. S02 portable crypto evidence remains within its accepted limits. | Entire RNG SDK technical body plus TRM25; pinned random/boot-entropy functions read. Fixed-pattern bring-up option must be excluded. Source ownership and fallible adapter remain unimplemented. | Reading signed where listed; **open** H01 source-to-implementation requirements and H02 entropy-source fault/actual linked-call evidence. Statistics alone are insufficient. |
| Power/brownout/NV writes/reset defaults | Selected DS supply/retention excerpts and ES core/system bodies pp.7–16 plus prior flash/ECC/watchdog bodies; current RM power, interrupted-write and full IWDG functional/register text through §61.7.6 now read. EWI writes refresh the counter. Native kit supply/radio branches reviewed; exact startup, timeout, final power and reset-clear policy remain open. | TRM chapters7/13/23 and selected10 plus MWDT/RWDT register text; pinned sleep defaults/assertions correspond to ANALOG-160 avoidance. Full selected caller/reset/NV/clear policy remains open. | **Open** H01 configuration and H02/H03 waveform/interruption/retention evidence. Reset or ciphertext destruction is not automatic secret erasure. |

U5G9 has a separate mandatory **document-level**, not bench-port, review: current
DS14102 Rev5 banked memory, selected supply/graphics/ordering text, ES0595 Rev4
DSI/SAES bodies, visually inspected native package outlines, directly read
DK2 power/clock/input/RGB reference versus DK1, and current
Embassy declarations are recorded. **Exact pads/AF/rails, current RM master
ownership and driver/license/workload work remain**; this is not a completed
host subset. U5A5/H573/MCXN947/classic/P4 are bounded
conditional/document screens; none silently replaces a failed main comparator.

## Open gates and next actions

[Existing Newhaven panel correspondence](panel-subset-review.md) now records
the raw DB module's selected mechanical, pin, electrical, command and reset
body. The distinct AF/ST7789VI breakout is deferred for the present common
four-wire/DC/backlight subset. C02 still needs exact module startup/internal
power, rail margin, fixture and effective host timing correspondence; no panel
or documentary host row is signed. Required H02 visible-render/failure evidence
is separate from these remaining H01 source/configuration decisions.

[U585 clock/power correspondence](u585-clock-power-review.md) adds selected
CRS, existing regulator/crystal and pinned Rust startup reading. The
[calculation proposal](u585-clock-proposal.json) makes the MSIS drift envelope,
latency, SPI/I2C and short-deadline conversions reviewable. Source gaps prevent
calling the stock init bounded or the fitted reference qualified. The existing
self-powered/TCPP Hibernate path remains conditional. No six-row signoff or
completed U585/S3 paper tuple follows from this increment.

[S3 fixed-CDC contract correspondence](s3-usj-contract.md) adds selected pinned
register/structure, security-helper and eFuse-table reading. The public IRQ
field set and finite FIFO/stream/reset requirements are explicit, with no
stock-driver conformance or FIFO-erasure inference. JTAG-only disable and
whole-CDC disable remain separate, including shared-lock order requirements.
C07 still needs clock, descriptor/current and attach/suspend closure; the
coordinator permits one conditional external J4 attach-fixture assessment,
not a new host/port/driver, selected fixture or electrical waiver. Both paper
host configurations and all six signoffs remain incomplete.

[S3 attach/descriptor correspondence](s3-attach-contract.md) adds the finite
conditional fixture thresholds, power/default/isolation and source-status
requirements, plus the exact received-unit descriptor/status capture and
refusal gate. It records newly read USB power/status/configuration bodies and
selected native ECN redlines. No captured response, fixture implementation,
permissible self-power mode or USB compliance follows. The fixed descriptor
and actual source must agree before this route can be selected.

| Gate | Actual unresolved evidence | Owner/action |
| --- | --- | --- |
| G01 current U5 manual | **Original retrieval closed**: current3651-page Rev7 native PDF rehashed. Selected masters/reset/clock/RNG/USB and history read. Remaining required current body and relevant delta are open. | H01: complete the used current sections, exact configuration and driver correspondence. Do not repeat solved retrievals or replace mandatory U5/S3 comparison. |
| G02 concrete host subset | Exact proposed host/kit OPN/package/revision and allowed silicon/ROM/configuration set, selected register/driver correspondence; U585 exact current electrical/AF and remaining errata subset; U5G9 remaining document triage. | H01: close documentary conditions before signing. H02 separately matches actual received hardware and binary before execution. Lack of an already-owned kit does not block available H01 reading. |
| G03 selected SE documents and service | SE051 API/errata/update access; all candidates' exact OPN/config/command/reset policies; TROPIC advisory remediation unresolved. | H02S/H04: lawful access and exact reproducible developer/service qualification. Continue independent host research. |
| G04 USB normative/electrical | Current normative originals and selected sink/current/suspend/inrush/backfeed clauses now read in usb-configuration.md; remaining applicable clauses, exact controller/configuration and kit power wiring still open. | H01/H03 before electrical admission; H04 complete design review. |
| G05 panel/power/expansion | Exact panel/FPC/cell/protection/OPNs, power budgets, domain ownership and physical limits. At most two retained power approaches. | H03/H04; no board selection or wiring from placeholder interfaces. |
| G06 physical resources | All 16 pinned resource entries unknown. No received board, scope, supply, logic analyzer or operator inferred; coordinator inventory request pending. | Coordinator/resource owner then H02/H02S/H03. No concrete purchase/fabrication/provisioning approval implied. |
| G07 independent review | Old R1/R2/R3 corrections received limited PASS at6f95. New current manual/driver substance requires an affected recheck. Old request-changes review remains immutable. | Coordinator assigns exact fresh candidate to a separate source/manual-substance reviewer; task graph remains coordinator-owned. |

## The six unchanged H01 acceptances

[S3 clock/time correspondence](s3-clock-time-review.md) and its
[conditional tuple](s3-clock-proposal.json) add exact fixed clock and UNIT1
polling requirements. Stock PLL and snapshot waits remain unbounded; a source
default or shared `esp_timer` timestamp is not a fallible deadline. Reference,
PLL/PHY, effective owner/features, supply/startup and IRQ conditions remain
required, followed by H02 actual implementation and measurement. No timer or
host signoff is closed by this source increment.

| Index | Required outcome | Evidence and present status |
| --- | --- | --- |
| 0 | Exact part/package/silicon and official document identity/revision/date/URL/hash/errata for every candidate. | [Register](manual-register.json), [options](option-comparison.md), [pin/errata ledger](pin-errata-ledger.json). **Partial**: exact leads are separated, but some proposed order suffixes/allowed-revision sets and original identities remain open. Received identity is a later H02 check, not an H01 ownership prerequisite. |
| 1 | Viable alternative triage and signed required sections for every admitted MCU probe; H04 remainder recorded. | Options and matrix above. **Incomplete**: meaningful triage exists, but mandatory U5/S3 comparison cannot be vacuously passed by admitting zero hosts. |
| 2 | Unavailable/restricted documents and unsupported features identified before freeze. | G01–G05 and H01-C01/C16/C17/C19. **Recorded**; no part freeze. |
| 3 | No full-manual claim from a link inventory. | Each document's reading/origin/remaining fields; explicit full versus selected/index/inaccessible distinction. **Recorded**; full 1531-page S3 and 3651-page current U5 manual review is not claimed. |
| 4 | Openness and reproducible API/errata/update access are selection criteria; SE access does not stop unrelated research. | SE/toolchain tables and G03. **Recorded**, with actual host research performed independently and no selected-SE waiver. |
| 5 | Complete host-relevant register/triage milestone may retain explicit SE gaps, with H02S/H04 hard gates. | [Probe plan](probe-plan.md) and this matrix. **Not met**: remaining current host-manual body and concrete-subset work prevent H01 closure. |

Source/claim consistency checks and existing repository CI test record integrity;
they cannot change these substantive statuses. Physical claims remain for H02,
H02S and H03 representative setups, H04 design review, and H08/H09 actual
assemblies. No measured capacity, entropy quality, energy, timing, fault resistance
or PCB behavior is established here.


The [finite C04 owner/update contract](owner-update-contract.md) and
[proposal](owner-update-proposal.json) now bind developer/owner/update/recovery
authority, exact U585 protections/journal/slots/destructive owner replacement
and S3 key purposes/shared locks/fixed roots/finite floor/app-only OTA. Three
selected pinned sources are newly registered (205 entries total); claims
H01-C97–C99 include the exact unbounded/unchecked eFuse-helper correspondence.
A log, outer success or equal reads is not a checked floor commit. Required
bounded error-preserving effective source/config/map/fit and every pre-use
power/entropy/display/USB/custody gate remain. No provisioning, implemented
boot/update, persistent vault, irreversible action or complete host signoff follows.
