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

## Host review sign-off matrix

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
| Package/supplies/clock/reset/straps/electrical | DS13086 Rev10 selected features/SRAM/supply/reset excerpts; exact VI/VIQ XML pad witness. Current package/AF/electrical tables and remaining RM0456 Rev7 body incomplete; current native originals and selected clock/reset text now read. | Module1.8 pp.2–4,9–18,27–30; TRM1.8 chapters7–8 and selected GPIO supply/reset table; exact N8R8 lead. Proposed kit schematic/revision/header conflicts and remaining electrical requirements open. | Selected reading signed by author; **documentary admission open**. H02 later matches received marking/configuration. A 144-pin kit does not certify a 100-pin custom allocation. |
| Boot/flash/options/eFuse/debug/update/rollback/owner | Historical RM0456 Rev6 OEM/RDP locators only; current Rev7 gate. DS lifecycle feature labels do not close transitions. | TRM §§5.1–5.3.3, chapter8; versioned IDF secure-boot/flash/OTA selections. Register/coding/download/update contradictions recorded. | **Open** H01 concrete lifecycle/configuration review, then H02 authorized sacrificial-unit tests. No irreversible operation performed or implicitly authorized. |
| Memory/ECC/cache/protection/buses/DMA | Current DS §3.5 and bus-matrix excerpt; historical security selections. Complete current RM attribution/masters, exact buffers and ECC/error policy missing. | TRM chapters3–4, selected15–16; explicit DMA/core/cache/USB-master concerns. No complete protection configuration or linked budget. | Selected reading signed; **open** H01 chosen-master/register checks and H02 actual peak memory/coexistence. One trusted image, no hostile-app claim. |
| USB/display/input/GPIO/AF/interrupt/timer | Pin-signal witness plus current ES0499 selected SPI/USB/UCPD bodies. Current RM/peripheral and exact driver correspondence remain open. | Selected GPIO matrix/interrupt/reset/IO_MUX text; SPI state/CS timing and bit-order contradiction; USB public functional text and pinned wrapper configuration. §32.5 comprehensive register specifications are NDA-limited. Pinned candidate TinyUSB device FIFO/reset/IRQ path now traced; effective build lock and bounded error policy plus kit/panel requirements remain open. | **Open** H01 exact bounded configuration. Unselected panel/controller has no wiring or performance approval. Software headers do not prove missing IP semantics. |
| RNG/health/crypto/backend | Current RM48 entire functional/register text and AN4230Rev14 selected configuration read; actual candidate RNG driver policy/waits have explicit gaps. Remaining used SAES/PKA/clock attribution not signed off. S02 portable crypto evidence remains within its accepted limits. | Entire RNG SDK technical body plus TRM25; pinned random/boot-entropy functions read. Fixed-pattern bring-up option must be excluded. Source ownership and fallible adapter remain unimplemented. | Reading signed where listed; **open** H01 source-to-implementation requirements and H02 entropy-source fault/actual linked-call evidence. Statistics alone are insufficient. |
| Power/brownout/NV writes/reset defaults | Selected DS supply/retention excerpts and ES core/system bodies pp.7–16 plus prior flash/ECC/watchdog bodies; used RM power/NV and driver sequence still open. | TRM chapters7/13/23 and selected10 plus MWDT/RWDT register text; pinned sleep defaults/assertions correspond to ANALOG-160 avoidance. Full selected caller/reset/NV/clear policy remains open. | **Open** H01 configuration and H02/H03 waveform/interruption/retention evidence. Reset or ciphertext destruction is not automatic secret erasure. |

U5G9 has a separate mandatory **document-level**, not bench-port, review: current
DS14102 Rev5 banked memory, selected supply/graphics/ordering text, ES0595 Rev4
DSI/SAES bodies, visually inspected native package outlines, directly read
DK2 power/clock/input/RGB reference versus DK1, and current
Embassy declarations are recorded. **Exact pads/AF/rails, current RM master
ownership and driver/license/workload work remain**; this is not a completed
host subset. U5A5/H573/MCXN947/classic/P4 are bounded
conditional/document screens; none silently replaces a failed main comparator.

## Open gates and next actions

| Gate | Actual unresolved evidence | Owner/action |
| --- | --- | --- |
| G01 current U5 manual | **Original retrieval closed**: current3651-page Rev7 native PDF rehashed. Selected masters/reset/clock/RNG/USB and history read. Remaining required current body and relevant delta are open. | H01: complete the used current sections, exact configuration and driver correspondence. Do not repeat solved retrievals or replace mandatory U5/S3 comparison. |
| G02 concrete host subset | Exact proposed host/kit OPN/package/revision and allowed silicon/ROM/configuration set, selected register/driver correspondence; U585 exact current electrical/AF and remaining errata subset; U5G9 remaining document triage. | H01: close documentary conditions before signing. H02 separately matches actual received hardware and binary before execution. Lack of an already-owned kit does not block available H01 reading. |
| G03 selected SE documents and service | SE051 API/errata/update access; all candidates' exact OPN/config/command/reset policies; TROPIC advisory remediation unresolved. | H02S/H04: lawful access and exact reproducible developer/service qualification. Continue independent host research. |
| G04 USB normative/electrical | Current complete USB normative clauses, CC/current entitlement/suspend/inrush/backfeed, exact parts and wiring. | H01/H03 before electrical admission; H04 complete design review. |
| G05 panel/power/expansion | Exact panel/FPC/cell/protection/OPNs, power budgets, domain ownership and physical limits. At most two retained power approaches. | H03/H04; no board selection or wiring from placeholder interfaces. |
| G06 physical resources | All 16 pinned resource entries unknown. No received board, scope, supply, logic analyzer or operator inferred; coordinator inventory request pending. | Coordinator/resource owner then H02/H02S/H03. No concrete purchase/fabrication/provisioning approval implied. |
| G07 independent review | Old R1/R2/R3 corrections received limited PASS at6f95. New current manual/driver substance requires an affected recheck. Old request-changes review remains immutable. | Coordinator assigns exact fresh candidate to a separate source/manual-substance reviewer; task graph remains coordinator-owned. |

## The six unchanged H01 acceptances

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
