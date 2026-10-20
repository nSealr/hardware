# H01 finite closure checklist

This checklist fixes the remaining scope as of 20 October 2026. It supplements
the accepted brief; it does not change its six acceptances. H01 is incomplete.
The deliverable is two complete **paper configurations** for the already bounded
U585 and S3 workload, plus the G9 document comparison. It is not a target build,
received-unit qualification or a third bench port. Completing neither host does
not pass the milestone.

The existing register, memory/lock/reset manifest, selected source reviews and
adverse findings are evidence already collected. They are not new reading tasks
to repeat. Close only the ten items below; do not add hosts, peripheral features,
driver alternatives or another display market sweep. Required source details
must be read before signing a used guarantee. Unused chapter bodies remain
explicitly excluded.

| ID | Remaining H01 reading/decision and completion condition | Six-row coverage |
| --- | --- | --- |
| C01 | Freeze the two exact proposed tuples: U585VIT6Q/custom-package witness and AII6QU/D01 kit relationship, S3 WROOM-1-N8R8/DevKitC-1v1.1, allowed silicon/ROM/lot conditions and developer/owner states. Finish only their selected DS package/AF/electrical rows against the already proposed signals. Resolve PA7/PB0 boot/conflicts, STMod DNF/control branches, radio hold/isolation and powered-off I/O assumptions from the existing kit/module sources. Retain the withdrawn pin9/11 reading as a correction. Output one complete pin/rail/reset/owner table per host, with explicit fixture requirements and exclusions. | Package/electrical; interfaces; reset |
| C02 | Resolve one common modest SPI display from the already examined leads. Waveshare/Adafruit controller/rail conflicts remain adverse; the existing authorized Newhaven module/breakout lead and linked ILI9341V are the bounded route still available for completion. Read only its exact module/board/connector correspondence, used controller commands, reset/power/logic/backlight timing and mechanical/contact drawing. Bind maximum SPI clock/phase, startup/blanking, complete-render condition and physical controls. Reject/defer the other leads explicitly; no further panel alternative. | Package/electrical; interfaces; power/reset |
| C03 | Finish one explicit clock/supply/reset/time tuple for each host. For U585 bind chosen Run/suspend modes, actual USB48MHz source/accuracy, HCLK/TRDT, SPI/I2C timing,3.3V/HSLV-off and USB-supply/brownout limits. Decide the already read secure polling SysTick alternative with strict wrap/ownership/clock-state limits; TIM2 stays excluded. For S3 bind its existing clock/reset/strap/sleep policy including ANALOG-160 avoidance. Read only the current PWR/RCC/clock/electrical fields needed by those choices. Close with named valid controls, finite deadlines and startup order; no new timer/peripheral. | Package/clocks; interfaces/time; power/reset |
| C04 | Finish the developer→owner-secured→update/recovery state tables using the already retained flash/options/eFuse/boot sources. Bind root and update authority, rollback metadata/counter, debug/download/logging gates, recovery route, surviving/erased state and interrupted-write rules. Resolve the recorded S3 XTS/key-purpose/download wording against the exact selected state; distinguish JTAG-only disable from whole USB/CDC disable. U585 ROM entry/Go/watchdog behavior must match the application policy. Document required values/transitions without executing fuses or provisioning. | Boot/owner/update; NV/reset |
| C05 | Turn the existing U585 GTZC/RCC manifest and S3 master/core/cache/PMS review into one concrete memory/ownership map per host: internal secret arena, public transport/render buffers, fixed request/queue/stack bounds and allowed masters. Bind P01/S02 workload bounds, current register exclusions and reset/lock lifetime. Finish only used S3 protection/coexistence controls and remaining U585 initialization correspondence. Software crypto remains the accepted S02 route; do not introduce SAES/PKA/graphics/DMA/MPU-sandbox features to close this item. | Memory/ECC/cache/protection/buses |
| C06 | Complete the existing U585 SPI/I2C/OTG device subset. Remaining RM72 endpoint/control/IN/error register/model text and applicable USB normative clauses must bind exact FIFO/packet/control bounds, reset/disable/flush, valid clear masks, ZLP workaround, VBUS/CC/EN policy and source IRQ acknowledgement. Decide TCPP-only versus already assessed UCPD sink controls and finish the already supported TCPP sensing policy. ADC4 remains excluded; if that policy cannot meet the requirement, record the exact source blocker for coordinator decision. Record exact bounded adapter requirements/remedies for the pinned Rust gaps. Do not label stock source conformant or add a driver. | Interfaces/interrupts; power/USB; memory masters |
| C07 | Finish the same-kit S3 transport decision between the already investigated OTG and fixed USB Serial/JTAG alternatives. OTG cannot bypass its missing normative IP semantics. Fixed CDC needs exact public TRM/errata/pinned IDF correspondence for reset/error/FIFO bounds, framing, exclusive stream writers and developer/owner behavior. Preserve no-J4-VBUS-sense and both-port power truth. Finish the existing S3 SPI/input/IRQ/source tuple for the same panel/workload, including current bit-order/CS/error discrepancies. A failure requires an explicit coordinator scope decision; no security downgrade or third transport/host. | Interfaces/interrupts; lifecycle; memory/USB |
| C08 | Finish the fallible RNG/crypto source-to-contract tables on both hosts: startup/health/reseed dependencies, exact internal SAR/RF ownership on S3, fixed-pattern exclusion, bounded failures and whole-output invalidation. Reuse the accepted S02 maintained software backend and its ABI/secret-memory limits. Finish only source dependencies actually used; unused accelerators remain reset/clock excluded. Close with positive and negative requirements, not entropy statistics or a target benchmark. | RNG/health/crypto; memory/reset |
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
