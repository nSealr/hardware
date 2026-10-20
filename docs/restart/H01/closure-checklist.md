# H01 finite closure checklist

This checklist fixes the remaining scope as of 20 October 2026. It supplements
the accepted brief; it does not change its six acceptances. H01 is incomplete.
The deliverable is two complete **paper configurations** for the already bounded
U585 and S3 workload, plus the G9 document comparison. It is not a target build,
received-unit qualification or a third bench port. Completing neither host does
not pass the milestone.

The maintainer's 20 October priority update makes the no-touch workload a
comparative baseline, not an irrevocable product choice. Generic Board/SDK
value, readable responsive touch, a physical confirmation decision and a
concrete two-SE composition study are explicit deltas in option-comparison.md.
Existing C01–C10 and security/physical/owner gates remain; root reconciles the
product requirements before H04. No new tracker or market sweep follows.

The existing register, memory/lock/reset manifest, selected source reviews and
adverse findings are evidence already collected. They are not new reading tasks
to repeat. Close only the ten items below; do not add hosts, peripheral features,
driver alternatives or another display market sweep. Required source details
must be read before signing a used guarantee. Unused chapter bodies remain
explicitly excluded.

| ID | Remaining H01 reading/decision and completion condition | Six-row coverage |
| --- | --- | --- |
| C01 | The finite kit/package/pin/electrical table is now in pin-electrical-contract.md. Exact header/pad/AF, PA7/PB0 default bridges and ROM overlaps, STMod branch/load/control and installed Wi-Fi internal pull-up correction are source-bound. U585 kitPH4/5 is not LQFP100-equivalent; PB11 is absent; PB14 DBCC2 and kitPB15 CC2 are distinct, with the initial false physical-conflict/alert draft explicitly corrected. No complete custom allocation is inferred. Normal external3V logic translation/current/contact/default-off requirements are specified, not implemented. Radio quiet from POR, powered-off I/O, received silicon/ROM/kit/jumpers and actual fixture remain unproved; any dependent operation stops. C03/C04/C09 now supply the finite system/owner/lifetime tables and named unsatisfied properties; effective/physical owners remain H02, not a new source market. | Package/electrical; interfaces; reset |
| C02 | Resolve the existing common display interface contract. Waveshare/Adafruit controller/rail conflicts remain adverse; the AF/ST7789VI breakout is deferred, not interchangeable with rawDB/ILI9341V. Selected rawDB source reading is recorded in panel-subset-review.md. Coordinator permits a conditional factory-default-only interface/qualification contract, not valid startup, selected display, energizing or H04 freeze. Normal external logic-rail/level/current/blanking/contact requirements are now in C01/C03/C09; finite host clock/phase/final-completion/consent requirements are in the existing SPI/runtime contracts. Their effective implementation and real behavior remain unqualified. Exact module startup/internal-power/factory-state evidence is a named unsatisfied H02 stop before any operation needing it; no blind internal-power experiment, new panel/controller/driver or outreach. Without evidence the module remains unqualified and replacement requires separate coordinator scope. Both complete host paper tuples must carry these obligations; no six-criterion waiver. | Package/electrical; interfaces; power/reset |
| C03 | The finite source/requirement table is now in system-runtime-contract.md /system-runtime-proposal.json, reusing the two clock/time calculations. U585LDO/VOS3/WS2/HSLV0/USB3Vvalidity, progress-onlyIWDG/EWI0, secureIRQ/EXTI7+15 and bootstrap-vs-qualified-time guards are explicit. S3MWDT0/RWDT counts/reset domains, readonlyEFUSEstage0shift, GPIO16/USJ96/faultsource routing and source-disable-map6 are specified. S3brownout reset-selector body576/register623 polarity is an unsatisfied source property; S3RCslow min/max and timedclockloss reset remain unestablished; neither on-chip monitor/BOR proves valid3V supply. Effective clock/reference/PHY/startup/IRQ/framework/binary and actual timing remain pre-use qualification gates, not supported functionality. C04/C09 now finish the finite lifecycle/power/attach source tables with named unsatisfied properties; no newtimer/peripheral/clock lead. | Package/clocks; interfaces/time; power/reset |
| C04 | The finite state/root/flash/counter/update/recovery requirements are now in owner-update-contract.md and owner-update-proposal.json. U585 exact root/HDP/WRP/journal/slot capacity and destructive OEM1/RDP1→0 owner replacement retain OTP/options survival and no ROM Go. S3 XTS256 two-key purposes, readable protected boot digests, fixed three-root succession, separate JTAG/wholeCDC/download/print/shared-lock fields, 16 finite antirollback bits and app-only OTA are explicit. Stock counter helpers have unbounded damaged-read retries and ignored read/write errors; bounded error-preserving full path and checked fresh floor commitment are mandatory before dependent use. No persistent vault/PIN scheme, implemented boot/update/map/fit, eFuse ceremony or custody is claimed; D02/S04/H02S/K01 and C09/H02 pre-use stops remain. No new backend/driver or irreversible operation. | Boot/owner/update; NV/reset |
| C05 | The finite allocation/ownership decision table is now in memory-ownership-contract.md and memory-ownership-proposal.json: fixed internal address maps, aggregate16KiB request/result/review caps, one pending operation, separate public/private row buffers, secret data/stack/backend partitions, master/core exclusions and lock/reset lifetime. Caps remain unmeasured qualification limits; no hostile-app claim. Existing U585/S3 init/linker differences have scoped remedies; other effective source/IRQ/lifecycle decisions remain under C03/C04/C06/C07. H02 must prove actual generated map/features/master/allocator/stack/copy fit, supported complete-workload capacity and clearing. No new DMA/accelerator/MPU-sandbox feature or broad source reading is needed for this table. | Memory/ECC/cache/protection/buses |
| C06 | Finite selected endpoint/control/IN/error/current-register and normative reading/triage is now in u585-usb-endpoint-contract.md and u585-usb-proposal.json. The OUT64/68 model/driver correspondence is an **unsatisfied interface property**, with neither mode selected/supported/qualified. H02 stops dependent enumeration/operation until corrected applicable source or evaluated separately reviewed finite public-data diagnostics resolve it; no ordinary probe assumes conformance. Generic EP0/bulk bounds, source-specific IRQ masks/ack, ZLP, finite failure and TCPP-only Hibernate0x08/readback validity are specified. Class/VID/PID remain unselected, lawful identity/class-source reading before enumeration; no CDC/Bridge/T01 implemented claim. Complete supply/reset/clock-loss/attach lifetime is C03/C09; address/short-IN/errata/effective bounded adapter gates remain before use. Reading/triage complete does not close the unsatisfied criterion; no new driver/IP/class or broad source leads. | Interfaces/interrupts; power/USB; memory masters |
| C07 | Finite selected same-kit USB/SPI/input reading and requirements are now in s3-usj-contract.md, s3-attach-contract.md and s3-spi-input-contract.md / s3-spi-input-proposal.json. OTG remains deferred for missing normative IP semantics; fixedUSJCDC remains unselected, not supported by bypassing descriptors/lifecycle/power gates. Exact fixed identity/current/power-status fields remain unknown with named read-only received-capture/refusal before dependent use. Neither whole-kit bus power nor external fixture is selected. SPI2CPU64B/MSB/mode/CS/clock/padded-tail/finite-abort and six-input shared-core IRQ/debounce requirements now have pinned source correspondence; stock polling/UPDATE/cleanup and GPIO conflict-warning paths need scoped remedies. C03/C04 now record finite clock/system IRQ/startup/console/owner requirements; C01/C09 record pin/rail/attach lifetime and negative outcomes. Effective implementation and all pre-use conditions remain H02. No additional driver/peripheral/host/fixture components/protocol or broad source leads; H02 effective build/capture/clock/ownership/waveform/physical gates remain. Source triage does not admit transport or sign the complete interface criterion. | Interfaces/interrupts; lifecycle; memory/USB |
| C08 | The finite conditional source-to-contract table is now in entropy-contract-review.md; bind its32-byte/100ms-fill/8-draw/200ms-total qualification limits and pre-use stops into the final memory/lifecycle host tables. Coordinator permits nominal U585 HSI48/A only as documentary reference: proposed real clock/AHB/profile conformity is unproven, no accepted entropy/certificate/H04 claim, strict H02 stop before any entropy-dependent use, no new clock/DRBG lead. S3 supported API/SAR ownership and health/source questions remain explicit pre-use qualification gates. Retain startup/health/reseed dependencies, exact internal SAR/RF ownership on S3, fixed-pattern exclusion, bounded failures and whole-output invalidation. Reuse the accepted S02 maintained software backend and its ABI/secret-memory limits. The existing finite table records the used source dependencies and positive/negative requirements; unused accelerators remain reset/clock excluded. Effective source/profile/clock/API/health/backend qualification is H02, not entropy statistics or a target benchmark. | RNG/health/crypto; memory/reset |
| C09 | The finite source/lifetime requirements and negative outcome are now in power-attach-lifetime-contract.md /proposal. Exact U585 CN8 power-only JP4[7–8] proposal (not PC), GDC1-open consumer incompatibility with UCPD supply, native CN1 vs UM CN14 label and S3 mutually exclusive supply methods/actual SGM2212 conditions are recorded. U585 valid EN/rise and autonomous VBUS-off data removal are **unsatisfied mandatory interface properties**; 13 ms normal software status handling does not close reset/clock-loss lifetime. S3 descriptor/status and allowed fixture remain unselected/unqualified; neither kit passes or fails aggregate current/suspend by assumption. USB ECN/default-current/inrush/backfeed/reset/write requirements and exactly two existing H03 chain decisions are finite. H02 dependent attach/enumeration/operations stop until the exact safe source/implementation properties close; no new fixture/port/component/controller/protocol, no physical or six-row signoff. | Power/brownout/NV/reset; package/USB |
| C10 | The finite G9 pin/rail/banked-memory/master/source/license comparison is now in g9-comparison-review/proposal; exact native MB1918 hierarchy closes PC13/B2–X1 source correspondence, while G9 promotion remains deferred. host-review-outcomes.md now distinguishes core1620/revision18 canonical6 criteria from each paper host6 signed source outcomes and first exact source/finite-diagnostic gates. No conditional/UNSATISFIED row is PASS and no probe/H01 closure is declared. Selected H01 documents are reconciled onto root b482 base with reviewed verifier/.gitignore/Board direction preserved. Required local make ci passed on integrated content85c77cc (43 tests) and canonical core1620 structure passed47 tasks; distinct exact-candidate final review and root hosted delivery/scope decision remain; no new source/host/driver/bench task. | G9 comparison; all six outcome rows; acceptance/review |

If an item discovers a mandatory unavailable source or an unsupported required
property, record the exact blocker and ask the coordinator for the required
scope/replacement decision. Do not count a conditional note, zero admitted
configurations or endlessly increasing the register as closure.

The following work belongs after H01 and does not block available documentary
reading or require an already owned kit:

* **H02:** identify the received board/silicon/ROM/lot/jumpers and actual panel;
  implement the reviewed bounded adapters/time/interrupt policy; pin the
  effective compiler/features/linker/lock/binary; measure target RAM, timing,
  coexistence, entropy-source failure, UI/recovery usability and host-flood
  behavior. Execute only separately authorized owner/provisioning procedures.
* **H02S:** mandatory exact SE API/errata/service/update access and command/state
  qualification. H01 may retain the explicit SE051 access and TROPIC remediation
  gates; these are not waivers for selection or custody claims.
* **H03/H04:** representative current, rail/reset/interruption, VBUS/inrush/
  suspend/backfeed, injection, waveform/thermal and physical-interface evidence;
  exact selected-design BOM, cell/protection/FPC, manufacturing and PCB review.
  H08/H09 later repeat applicable evidence on actual assemblies.

H01 must state these later gates and their expected positive/negative outcomes.
It must not claim their results. Earlier reviews/result files keep their original
candidate bindings; final acceptance needs new evidence for the final candidate.


## Historical C01–C09 checkpoint at4d3fa674, 20 October 2026

The finite selected source/requirements tables C01–C09 are now available together.
This is a reviewable **negative/conditional outcome**, not nine acceptance passes
or two admitted connected systems. The current source inventory is206 documents
and102 bounded claims; counts are inventory, never completeness evidence.

The packet consists of pin-electrical-contract/proposal (C01),
panel-subset-review and its coordinator factory-state allocation (C02),
system-runtime-contract/proposal and the two clock proposals (C03),
owner-update-contract/proposal (C04), memory-ownership-contract/proposal (C05),
u585-usb-endpoint-contract/proposal (C06), s3-usj-contract/s3-attach-contract/
s3-spi-input-contract/proposal (C07), entropy-contract-review (C08) and
power-attach-lifetime-contract/proposal (C09). The register, claims and ledger
bind exact actual reading, adverse outcomes, exclusions and owners. Earlier
checks/reviews keep their original candidate identities; none is a final review
of this packet or of the future current-main candidate.

Mandatory unsatisfied source/interface properties remain visible in C10:

* U585 OUT64/68 correspondence: neither programming model selected or supported;
  stop dependent enumeration/operation before source correction or separately
  reviewed/evaluated finite safe diagnostic evidence.
* U585 TCPP EN normal level/rise and independent VBUS-off data removal through
  reset/clock loss/absent firmware: the normal-running13 ms policy does not
  close them. No U585 fixture or board rework has been admitted.
* S3 brownout reset-selector polarity: conflicting body/register definitions,
  no selected polarity or qualified reset scope.
* Raw DB module startup/internal-power/factory state: coordinator permits only
  a conditional external interface/qualification specification. Stop before
  dependent use; no valid-startup, display selection, H02 display-feasibility
  completion or H04 freeze without exact source evidence.
* S3 fixed descriptor/power-source status and conditional fixture correspondence:
  unknown fields retain the named safe received-capture/refusal gate. No CDC,
  bus-powered kit or self-powered fixture is selected; capture does not waive
  missing OTG normative semantics or allow a security downgrade.
* U585 entropy real clock/divider/AHB/profile conformity: conditional nominal
  manufacturer reference only, no accepted entropy. H02 stops **before** every
  entropy-dependent use; statistics/frequency measurements do not recreate the
  raw-noise assessment. Other finite SAR/API/health/backend gates remain.

Known implementation gaps (bounded/error-preserving helpers, boot/journal/floor,
USB/address/errata, clocks/time/IRQ/master/lock/clearing) and received-unit
rail/current/capacitance/inrush/suspend/backfeed/thermal/waveform/UI/fit evidence
remain named pre-use H02/H03 conditions. Persistent custody and exact SE services
remain D02/S04/H02S/K01, under unchanged source/platform gates. No source question
is silently converted to a measurement, successful API call or conditional
functionality claim.

Only C10's already bounded G9 comparison, six-row **outcome** assembly, selected
surface reconciliation onto root-supplied hardwaremain b48229d47ea93ef552ccdf4521aab6b37880fe96
(tree b5cf9556a05a0cfaef4288cc784d990fcef94523), required integrated checks and
distinct final review remain in this finite documentary work. The immutable
original H01 source inputs and historical reviews are retained; no blanket
rebase, target build or physical operation is implied. An unsatisfied row stays
unsatisfied, so H01 admission cannot be declared from this packet alone.


Current C10 content/outcome assembly supersedes that checkpoint’s remaining
reading list; see host-review-outcomes.md and handoff-2026-10-20.md. The source
inventory is now210/105 claims, with every unsatisfied property preserved.
Required checks/review are reported only when actually performed; no milestone
closure, new task or physical operation follows.
