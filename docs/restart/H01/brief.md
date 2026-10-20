# H01 — component manuals and bounded feasibility review

Specification candidate, 2026-10-18. Author: `/root/h01_author`. Issue:
[nSealr/nsealr#20](https://github.com/nSealr/nsealr/issues/20).
This brief awaits the coordinator's exact-candidate review before H01 register
implementation. It selects no component, assembly or production configuration.

## Inputs and ownership

The authoritative input is `nSealr/nsealr` commit
`7b5553685dac56029a4379be12054154b6b5e0b5`, task graph revision 11. H01 is ready;
its P01 dependency is integrated. Read the accepted P01 requirements and threat
models, S02 secret/entropy contracts, architecture, validation and PCB-development
contract at that commit. Code establishes existing behavior; component behavior
requires the manufacturer manual and applicable errata. [Input notes](input-notes.json)
bind these documents, the six unchanged H01 acceptances and the preparation checks.

The editable repository is `nSealr/hardware`, starting at
`340697d6713a671e9e01b0dc874ec999ab071601`, branch `restart/h01-manuals`, isolated
worktree `/home/tux/nsealr/.restart-tools/goal/h01`. Preparation writes only this
brief and `input-notes.json`. The coordinator owns the canonical graph and task
state. Source/canonical checkouts and private historical research stay read-only.
After approval, the proposed implementation scope is `docs/restart/H01/` plus a
narrow root `README.md` navigation/status correction. That correction will point
to the accepted portfolio and register, label legacy artifacts as investigation
inputs, and remove active reliance on the old five-family/S3-QR taxonomy. It will
not migrate or rewrite old kit fixtures or import a legacy BOM as the new design.

## Intended result and product constraints

Produce a versioned public, paraphrased component/manual register, bounded option
comparison, and pin/errata/review ledger that a different engineer can audit and
use to prepare H02/H02S/H03. H01 can close with explicit SE access gaps when the
host-relevant review is complete. That is documentation/triage acceptance only.
H02S and H04 retain mandatory selected-SE documentation and measured behavior
gates. An inaccessible MCU document likewise cannot support an admitted host
probe whose correctness depends on it.

The design serves a general-purpose programmable Board/SDK and a separately
qualified Nostr Signer. Preserve the four independent Signer profiles: connected
commercial ESP32 without SE, offline Pi, offline P4, and initially connected
custom Board. No profile is a universal security rank; lack of an SE is not
itself a declaration that a profile is compromised. The generic SDK has no Nostr
schemas or policy dependency. Its initial model is one trusted firmware image;
TrustZone, a second core, SDK libraries or multiple SEs do not establish hostile
application isolation.

Use P01's actual workload: complete inspectable review, physical consent,
bounded host input, local nsec entry/backup/recovery, and connected message
operations. Quantitative capacities and recovery ergonomics remain measured
gates. An attractive screen or a working signature is insufficient. Separate
development, owner-secured and product-qualified lifecycle states, identifying
which roots, counters, secrets and update authorities survive each transition.

Trace the review to P01 PROD-02/03 (entropy and recovery), PROD-04/05 (consent and
review), PROD-07 (connected message workload), PROD-09 (bounds), PROD-11
(lifecycle) and PROD-12 (generic platform). Reuse S02's accepted maintained-crypto
candidate and link evidence within their stated limits; H01 does not rerun the
portable benchmark campaign or treat section sizes as measured target RAM.

## Bounded candidates and comparison rules

These are investigation labels, not complete orderable identities. Before a
candidate is admitted for a probe, resolve its exact ordering code, package,
power option, relevant silicon revision and evaluation-board differences from
primary documents. Unknown received silicon stays unknown until H02/H02S.

| Candidate group | Bounded purpose and entry rule |
| --- | --- |
| STM32U585VI, VIQ differences | Main TrustZone host investigation. Complete the relevant current RM0456, DS13086 and ES0499 review; reconcile the historical pad witness with the selected package/power option and current alternate-function tables. Do not treat the 64-pin part or a 144-pin kit as pin-equivalent. |
| ESP32-S3, exact module/SoC variant | Mandatory host comparator for the same bounded USB/display/input/crypto workload. Review its actual boot/eFuse/recovery, memory protection, buses/DMA, internal versus external memory and radio exposure. Pin the SDK/toolchain, TRM, datasheet and errata. It is not assumed equivalent to Arm TrustZone. |
| STM32U5A5VJ | Conditional U5 memory alternative if the U585 budget fails. Triage exact DS13543/ES0553/package/peripheral differences; admit additional detailed probe review only on a recorded resource reason. |
| STM32U5G9ZJ and exact package alternatives | Mandatory document-level UI/RAM/package/power/toolchain comparison alongside U585. Review DS14102, ES0595 and relevant RM0456 graphics/memory ownership; distinguish the published Safe 7 designation from an exact OPN and from U5G9J-DK1's different package. Promote only if the required review/recovery UI or platform workload benefits materially and the pin, supply, memory-isolation, maintained-driver and manufacturing budgets remain viable; otherwise record the concrete rejection or deferral reason. No automatic selection from Safe 7 adoption and no additional bench port in H01. |
| STM32H573 | Conditional lifecycle alternative. Triage current RM0481, exact datasheet/errata and owner/debug/update behavior. No additional full port merely because this family has different lifecycle mechanisms. |
| ESP32-P4 and classic ESP32 | Document-only comparison of their relevant architectural and developer tradeoffs. P4's independent QR profile continues separately. Pin silicon/SDK differences; distinguish P4 silicon from kits with a companion radio. Classic ESP32 is not a substitute name for S3. Any proposed replacement for H02's U5/S3 scope goes to the coordinator before work expands. |
| NXP MCXN947 | One bounded non-ST TrustZone screen to challenge a vendor-specific shortlist. Check exact package, memory/UI fit, second-core/peripheral ownership and lawful access to reference/security manuals. The current index labels those manuals account-required; catalogue access is not manual review. Do not add a bench port without a demonstrated advantage and an amended brief. |
| SE051C2, OPTIGA Trust M, TROPIC01 | At most these three initial SE approaches. Identify exact OPN, silicon/applet/firmware/configuration, algorithms and object policies. Compare actual custody/wrapping/PIN/reset/channel/update services and developer access. No automatic equivalence, native BIP340, non-exportable Nostr ECDH or independent dual-SE protection. |

Keep the comparison multidimensional: required threat boundary; internal secret
memory and DMA ownership; boot/debug/recovery and firmware-owner control; UI
bandwidth and recovery input; USB capability; entropy/crypto backend; power and
pins; maintained Rust support versus a narrow vendor C adapter; reproducible
developer access, licensing and maintainability. Separate manufacturer capability,
software support, engineering inference and actual measurement. An SDK API is not
proof of register/electrical behavior. Avoid a weighted security score that hides
a failed required property. A failed mandatory comparator requires an explicit
replacement/scope decision, not an empty or silently reduced comparison.

Power/UI/expansion triage is equally bounded. Start with BQ24074 versus BQ25628
charger leads, TPS63802 regulation and the historical AP2112 dropout question,
against USB-only and optional protected single-cell operation; retain at most two
viable power-chain approaches for H03. Treat nPM1300 as a reference cross-check,
not an automatic third architecture. Chemistry, full usable
voltage range, NTC/protection, current entitlement, thermal limits, absent-battery
operation and reverse/backfeed behavior determine viability. A LiFePO4 reference
does not authorize a generic 4.2 V Li-ion charger. A reference part remains only a
lead until its exact datasheet and implementation context are checked.

For display/input, compare a directly controlled modest SPI panel plus physical
controls with one larger-bandwidth panel approach only if readable review and
local recovery justify it. Identify panel controller, complete module revision,
mating connector/contact orientation, rail/logic limits, backlight and touch/input
ownership; there is no universal display FPC. Camera and NFC remain conditional
modules with a named use, pin/memory/power cost and attack surface, not compulsory
custom-board features inherited from offline profiles or wallet references.
USB-C is initially a 5 V sink investigation; compare the retained TUSB320LAI
controller lead with the chosen host's applicable UCPD/CC approach, using current
USB-IF normative clauses as well as component documentation. Their access and
review are open; a release-index page is insufficient. PD, source/host role and
higher current are not assumed. Maker expansion must have useful documented buses and
power, safe startup/disconnect and lifecycle controls while keeping SE and trusted
UI paths private. GPIO count alone is not a pin or isolation contract.

## Manual review procedure and output contract

1. Reconcile exact sources before reuse. Recompute preserved original hashes,
   compare upstream pins/current revisions and record the changed claim scope.
   Carry forward only the previously read sections or visually inspected pages.
   A source download, derived text or a past review title is not a new complete
   manual review. The preparation verified 75 archived original hashes and
   unchanged upstream pins; the four TROPIC schematic exports and advisory also
   match fresh downloads. Reinspect only new relevant claims or changed sources.
2. Publish `manual-register.json` and a concise readable register. Each document
   entry records candidate identity, manufacturer, ID/revision/date, original URL,
   retrieval time/status, original-byte hash/size when available, document type,
   access/redistribution terms, supersession/delta, actually reviewed sections and
   drawing pages, reviewer, extracted requirements, related errata and open work.
   Label full, selected-section, inherited-section, index-only, inaccessible and
   unreviewed accurately. A failed retrieval has no invented original hash;
   extraction hashes are explicitly not original-document hashes. Publish links,
   metadata and original analysis; keep unlicensed/restricted originals private.
3. Give each claim a stable ID, evidence section/page/register/table, exact
   applicability, reasoning, open assumption, required negative case and closure
   owner. Pair it with a status such as documented, calculated, unverified or
   measurement-required. No source review is upgraded to bench proof. Resolve
   contradictions against manufacturer documentation; code may be wrong.
4. Produce `option-comparison.md`, a machine-readable pin/errata ledger and
   `review-coverage.md`. Record exact pad/AF and package, power domain, reset/strap
   state, owner, peripheral/DMA/master access, interface/voltage limits, competing
   use, source and unknown. For applicable errata record affected revisions,
   configuration, mitigation, driver/probe implication and residual limit. The
   ledger is a feasibility witness, not a netlist, footprint approval or BOM.
5. Produce a practical `probe-plan.md` and result/handoff evidence mapping every
   unchanged H01 acceptance to reviewed artifacts. List separate host-probe
   admission gaps, SE access/command gaps and selected-design work due at H04.
   Independent review must judge the content and exact candidate, not merely
   JSON shape or link availability. The coordinator records final task state.

For each admitted U5/S3 host probe, finish the sections needed by its concrete
configuration, including the current revision delta and errata. The coverage
matrix must contain the following rows with exact document locators and signed
review outcomes; broad chapter names below are work instructions, not sign-off.

| Required review | What the later probe must establish |
| --- | --- |
| Package, supplies, clock/reset/boot straps and electrical limits | Identified kit/package/silicon, safe wiring/voltage, reset/clock and current-limited startup. |
| Boot ROM, flash/option/eFuse, debug, signed update, rollback and owner transition | Exact enforcement and recoverability on authorized sacrificial hardware; allowed transitions and erased/surviving state. No fuse operation in H01. |
| Memory map/ECC/cache, attribution/protection, buses and DMA | Internal secret placement; display/input/USB/expansion ownership and access assumptions; actual peak stack/RAM and coexistence under load. |
| USB, display/input interfaces, GPIO/AF, interrupts and timers | Comparable request/review/input workload, host-flood behavior, bandwidth and timing; no SE driver prerequisite. |
| RNG/health tests and crypto engine/backend interfaces | Startup dependencies, fallible source path, no silent fallback, exact linked binary/ABI, real invocation and fault handling. Statistics alone cannot qualify entropy. |
| Power states, brownout, nonvolatile writes and reset defaults | Idle/active/update current, interrupted-state behavior and recovery; identified instrumentation limits. |

Only needed peripherals enter the completed host subset. A deferred camera, NFC
or unselected panel is explicitly outside that probe, with required review before
its admission/H04; its unread chapters cannot justify a future feature claim.
The U5 historical Rev 6 text may guide locators but cannot close current Rev 7
register behavior. Arm core architecture references supplement the chip manual;
they do not prove the vendor's peripheral/security interconnect.

## Known gaps and reference limits to retain

- **STM32:** [RM0456 Rev 7, March 2026](https://www.st.com/resource/en/reference_manual/rm0456-stm32u575585-armbased-32bit-mcus-stmicroelectronics.pdf)
  is still the current official locator checked during preparation. The web
  reader exceeded its size limit. The preserved complete original is Rev 6;
  the relevant current delta and exact datasheet/errata review remain open.
- **SE051:** the [current manufacturer catalogue](https://www.nxp.com/products/SE051)
  still identifies AN12543 Rev 4.5 and SE051 errata Rev 1.1; API/middleware/
  personalization access and applicable update/developer distribution terms
  remain unresolved. Public middleware headers and AN12907 are not substitutes
  for the mandatory exact command/policy documents. Record access failures
  without bypassing restrictions. Vendor applet authority and owner MCU firmware
  authority are separate.
- **TROPIC:** the unchanged [public advisory](https://raw.githubusercontent.com/tropicsquare/tropic01/90747cac7c0261408c0ca767d272894f481f2cf2/doc/security_advisories/ODR_TR01_SA_2026012900_1v0.pdf)
  includes TR01-C2P-T310. Its public v1.0 date is 2026-06-03, not the January
  report date. No qualified fix for the intended part/threat is established here;
  an expected hardened-part date is not a received, qualified remediation.
- **Reference boards:** Safe 7's published Rev D design uses U5G9, not U585;
  published firmware revC-to-hardware-revision correspondence remains open.
  Its custom DSI/UI flex and LiFePO4 power design are not generic display/cell
  contracts. Preserve the narrow historical schematic/source review, not an
  assertion of a whole-product audit. TROPIC's USB development firmware is a
  host bridge and command bench, not a locally isolated custody signer. Exposed
  shield buses and plug wiring cannot be copied as production isolation or a
  two-orientation USB-C receptacle design.

## Evidence, checks and stop conditions

H01 requires software/research resources only. All 16 physical/resource registry
entries were unknown at the pinned graph; an inventory request is pending with
the coordinator. No sample, instrument, operator or measurement is inferred.
H02/H02S/H03 procedures will name received board/silicon/configuration, supply and
current measurement, scope/logic/debug setup, controlled power interruption,
operator, conditions, public fixtures, binary hashes and expected positive and
negative results. H01 defines coverage; those tasks perform it. H04 combines
reviewed documentation, calculations and representative measurements; H08/H09
repeat applicable claims on actual assemblies.

Preparation checks: parse the JSON, verify pinned input/hash correspondence,
inspect the two-file diff and run `git diff --check`. Implementation checks:
validate register references/hashes and exact identities; inspect a source-to-
claim sample plus every blocking claim; run existing hardware `make ci` and
record its actual environment/results. Existing repository scripts may assume a
directory named `hardware` or sibling legacy repositories; report such failures
and use a documented equivalent checkout/context rather than weaken checks.
Run the canonical plan validator read-only when reconciling the final handoff;
the coordinator owns graph mutation and affected integration CI. Do not add
tests that merely require prose strings or a new orchestration service.

Stop host admission on a mandatory unread/current manual or erratum, unsupported
required lifecycle, impossible UI/memory/pin budget, or unresolved protection
boundary. Stop SE selection on missing mandatory access, unsupported commands,
unresolved advisory applicability or unreproducible developer access. Continue
independent host research where unaffected. Unresolved blockers cannot become
accepted compromises while the affected guarantee remains advertised.

There is no PCB capture/layout, component freeze, purchase/fabrication order,
physical measurement, irreversible provisioning or production-secret use in this
brief. First publish the exact brief candidate for coordinator review and wait;
after acceptance, implement only the approved register scope. A distinct agent
must review the final implementation diff and evidence before H01 can close.
