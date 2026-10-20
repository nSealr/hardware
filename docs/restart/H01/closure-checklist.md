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
| C01 | The finite kit/package/pin/electrical table is now in pin-electrical-contract.md. Exact header/pad/AF, PA7/PB0 default bridges and ROM overlaps, STMod branch/load/control and installed Wi-Fi internal pull-up correction are source-bound. U585 kitPH4/5 is not LQFP100-equivalent; PB11 is absent; PB14 DBCC2 and kitPB15 CC2 are distinct, with the initial false physical-conflict/alert draft explicitly corrected. No complete custom allocation is inferred. Normal external3V logic translation/current/contact/default-off requirements are specified, not implemented. Radio quiet from POR, powered-off I/O, received silicon/ROM/kit/jumpers and actual fixture remain unproved; any dependent operation stops. C03/C04/C09 finish system lifetime and effective owners, not a new source market. | Package/electrical; interfaces; reset |
| C02 | Resolve the existing common display interface contract. Waveshare/Adafruit controller/rail conflicts remain adverse; the AF/ST7789VI breakout is deferred, not interchangeable with rawDB/ILI9341V. Selected rawDB source reading is recorded in panel-subset-review.md. Coordinator permits a conditional factory-default-only interface/qualification contract, not valid startup, selected display, energizing or H04 freeze. Remaining H01: normal external logic-rail/level/current/blanking/contact requirements underC03/C09 and effective host clock/phase/final-completion/consent correspondence. Exact module startup/internal-power/factory-state evidence is a named unsatisfied H02 stop before any operation needing it; no blind internal-power experiment, new panel/controller/driver or outreach. Without evidence the module remains unqualified and replacement requires separate coordinator scope. Both complete host paper tuples must carry these obligations; no six-criterion waiver. | Package/electrical; interfaces; power/reset |
| C03 | Finish one explicit clock/supply/reset/time tuple for each host. For U585 bind chosen Run/suspend modes, actual USB48MHz source/accuracy, HCLK/TRDT, SPI/I2C timing,3.3V/HSLV-off and USB-supply/brownout limits. Decide the already read secure polling SysTick alternative with strict wrap/ownership/clock-state limits; TIM2 stays excluded. For S3, s3-clock-time-review.md / s3-clock-proposal.json now bind the conditional CPU160/APB80/PLL480/UNIT1 polling tuple and unbounded stock init/read remedies; remaining source decisions are supply/reset/watchdog/IRQ/startup/effective ownership and reference/PHY condition allocation, including ANALOG-160 avoidance. Do not repeat the now-read selected clock/timer bodies. Read only the current PWR/RCC/clock/electrical fields needed by those choices. Close with named valid controls, finite deadlines and startup order; no new timer/peripheral. | Package/clocks; interfaces/time; power/reset |
| C04 | Finish the developer→owner-secured→update/recovery state tables using the already retained flash/options/eFuse/boot sources. Bind root and update authority, rollback metadata/counter, debug/download/logging gates, recovery route, surviving/erased state and interrupted-write rules. Resolve the recorded S3 XTS/key-purpose/download wording against the exact selected state; distinguish JTAG-only disable from whole USB/CDC disable. U585 ROM entry/Go/watchdog behavior must match the application policy. Document required values/transitions without executing fuses or provisioning. | Boot/owner/update; NV/reset |
| C05 | The finite allocation/ownership decision table is now in memory-ownership-contract.md and memory-ownership-proposal.json: fixed internal address maps, aggregate16KiB request/result/review caps, one pending operation, separate public/private row buffers, secret data/stack/backend partitions, master/core exclusions and lock/reset lifetime. Caps remain unmeasured qualification limits; no hostile-app claim. Existing U585/S3 init/linker differences have scoped remedies; other effective source/IRQ/lifecycle decisions remain under C03/C04/C06/C07. H02 must prove actual generated map/features/master/allocator/stack/copy fit, supported complete-workload capacity and clearing. No new DMA/accelerator/MPU-sandbox feature or broad source reading is needed for this table. | Memory/ECC/cache/protection/buses |
| C06 | Finite selected endpoint/control/IN/error/current-register and normative reading/triage is now in u585-usb-endpoint-contract.md and u585-usb-proposal.json. The OUT64/68 model/driver correspondence is an **unsatisfied interface property**, with neither mode selected/supported/qualified. H02 stops dependent enumeration/operation until corrected applicable source or evaluated separately reviewed finite public-data diagnostics resolve it; no ordinary probe assumes conformance. Generic EP0/bulk bounds, source-specific IRQ masks/ack, ZLP, finite failure and TCPP-only Hibernate0x08/readback validity are specified. Class/VID/PID remain unselected, lawful identity/class-source reading before enumeration; no CDC/Bridge/T01 implemented claim. Complete supply/reset/clock-loss/attach lifetime is C03/C09; address/short-IN/errata/effective bounded adapter gates remain before use. Reading/triage complete does not close the unsatisfied criterion; no new driver/IP/class or broad source leads. | Interfaces/interrupts; power/USB; memory masters |
| C07 | Finite selected same-kit USB/SPI/input reading and requirements are now in s3-usj-contract.md, s3-attach-contract.md and s3-spi-input-contract.md / s3-spi-input-proposal.json. OTG remains deferred for missing normative IP semantics; fixedUSJCDC remains unselected, not supported by bypassing descriptors/lifecycle/power gates. Exact fixed identity/current/power-status fields remain unknown with named read-only received-capture/refusal before dependent use. Neither whole-kit bus power nor external fixture is selected. SPI2CPU64B/MSB/mode/CS/clock/padded-tail/finite-abort and six-input shared-core IRQ/debounce requirements now have pinned source correspondence; stock polling/UPDATE/cleanup and GPIO conflict-warning paths need scoped remedies. Remaining clock/system IRQ/startup and effective console/owner lifecycle are C03/C04; pin/rail/attach lifetime C01/C09. No additional driver/peripheral/host/fixture components/protocol or broad source leads; H02 effective build/capture/clock/ownership/waveform/physical gates remain. Source triage does not admit transport or sign the complete interface criterion. | Interfaces/interrupts; lifecycle; memory/USB |
| C08 | The finite conditional source-to-contract table is now in entropy-contract-review.md; bind its32-byte/100ms-fill/8-draw/200ms-total qualification limits and pre-use stops into the final memory/lifecycle host tables. Coordinator permits nominal U585 HSI48/A only as documentary reference: proposed real clock/AHB/profile conformity is unproven, no accepted entropy/certificate/H04 claim, strict H02 stop before any entropy-dependent use, no new clock/DRBG lead. S3 supported API/SAR ownership and health/source questions remain explicit pre-use qualification gates. Retain startup/health/reseed dependencies, exact internal SAR/RF ownership on S3, fixed-pattern exclusion, bounded failures and whole-output invalidation. Reuse the accepted S02 maintained software backend and its ABI/secret-memory limits. Finish only source dependencies actually used; unused accelerators remain reset/clock excluded. Close with positive and negative requirements, not entropy statistics or a target benchmark. | RNG/health/crypto; memory/reset |
| C09 | Bind both paper configurations to an exact permissible kit supply/USB attach/suspend/disconnect arrangement and update/reset/NV-write policy. Read remaining applicable USB2/ECN/Type-C clauses and existing kit power branches; resolve EN/CC/VBUS status validity and pre-configuration/suspend/inrush/backfeed requirements. Retain at most the two accepted H03 power-chain approaches with concrete feasibility/deferral reasons. Distinguish source-backed limits and calculated budgets from currents/thresholds still to measure. No battery chemistry, power architecture or component expansion. | Power/brownout/NV/reset; package/USB |
| C10 | Complete the bounded G9 comparison and assemble acceptance evidence. Read only exact ZJ/package/rail/AF costs, current relevant memory/display-master/GTZC/cache ownership and the existing DK2 PC13/LSE circuit/erratum correspondence. Decide promotion or reasoned documentary deferral against the same UI/RAM workload and declared Rust/license support; no full G9 port. Then sign all six rows for each U585/S3 paper tuple, update comparison/probe requirements and write fresh result/handoff metadata. Reconcile source/claim IDs and every blocking finding, run required existing hardware CI once for the final documentary candidate, obtain distinct exact-candidate substantive review and address it. Coordinator owns task graph, source-freeze resolution and integration. | G9 comparison; all six signed rows; acceptance/review |

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
