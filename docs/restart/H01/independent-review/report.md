# H01 independent source review — request changes

Reviewer: `/root/h01_substance_review`, 2026-10-18. Repository:
`nSealr/hardware`. Frozen candidate:
**`d5d75306a082215453d329e31ca9c11d6effa80d`**; substantive source commit:
**`19362fc9a12bed43070c56642b4a932f1bc6a545`**. The approved brief is
`e10dd2426146e0aa3bbcf04af6a9b1bb59f7e868`, with distinct coordinator approval
`8041bac701f32aa289f6cfba019a7baaac04403e`.

**Request changes.** The S3 errata ledger reverses a destructive-setting
mitigation, and abbreviates another workaround incorrectly. The fact that the
candidate admits no host does not make these errors acceptable in a reusable
research record. Do not use this candidate's ledger as a probe procedure.

The explicit **H01 incomplete** status is accurate. Acceptance index 0 remains
partial; indices 1 and 5 remain unmet. This review approves neither H01 completion
nor any part, host, wiring, target build, physical guarantee or irreversible
operation. No physical operation occurred in this review. The reviewer changed
only this independent-review directory in a separate worktree.

## Required corrections

### R1 — high: ANALOG-160 mitigation has the opposite meaning

[The ledger at line 678](../pin-errata-ledger.json#L678), row
`E-S3-ANALOG160`, places `BIAS_SLEEP=0 and PD_CUR=1` in
`documented_mitigation`. In the actual **ESP32-S3 SoC Errata v1.3 §3.3,
printed p.7 / physical PDF page 9**, that conjunction is the condition that
can permanently damage the chip. The workaround disables that configuration.
It applies to **v0.0, v0.1 and v0.2**; the vendor records the software avoidance
in **ESP-IDF v4.4.2+, v5.0 and later**. The original hash is
`8f349bdd0b4e9bca24e49d777ac3b416ff2d2c48253a49653162e84f4b484500`.
[Manufacturer errata](https://documentation.espressif.com/esp-chip-errata/en/latest/esp32s3/esp-chip-errata-en-master-esp32s3.pdf).

Move the precise dangerous conjunction into `configuration`; state explicitly in
`documented_mitigation` that it must be prevented, with the versioned workaround.
Require inspection of the chosen sleep/ULP/touch implementation, including any
Rust HAL or custom path that does not inherit IDF's workaround. A stated IDF
version alone does not prove the selected binary uses that path. Verify the
correction by source reading; deliberately exercising the damaging setting is
not an appropriate negative test.

### R2 — medium: TOUCH-100 omits the rest of the workaround

[The ledger at line 748](../pin-errata-ledger.json#L748), row
`E-S3-TOUCH100`, says only to discard the first two scans. **S3 errata v1.3
§3.7, printed p.10 / physical page 12**, concerns the raw data of the first
two **`TOUCH_SCAN_DONE_INT` interrupts** and instructs software to skip those
interrupts and then disable/stop using them. It does not authorize a stream of
subsequent raw scan interrupts merely because two samples were discarded.
Applicability is again v0.0/v0.1/v0.2, in the same original above.

Use the exact interrupt name, preserve the whole vendor workaround, and keep
the distinction between raw scan interrupts and other qualified touch-driver
paths. Physical buttons remain the proposed bounded input approach; an unused
touch peripheral does not excuse an inaccurate future-use ledger entry.

### R3 — clarify documentary admission before the next handoff

[G02](../review-coverage.md#L34) groups exact kit/module/silicon identity into
an H01 admission gate, while the brief correctly leaves received silicon unknown
until H02. Split the two records explicitly:

- **H01:** proposed exact OPN/package, documented kit revision and configuration,
  allowed silicon/ROM revisions, relevant errata, completed required reading and
  remaining measured checks. This can be completed without already owning a kit.
- **H02:** match the received marking/revision, board/jumpers and actual binary
  against those conditions before wiring or running the affected probe.

This clarification does not admit any current host. Current RM0456 Rev7 and
other mandatory selected-subset gaps remain hard gates, and zero admitted
subsets cannot satisfy the unchanged H01 acceptance.

## Blocking claims and adverse evidence examined

The following conclusions concern documentary accuracy only. Exact reading
coverage and source bindings are also recorded in [review.json](review.json).

| Claim / gate | Independent source check and disposition |
| --- | --- |
| **C01 / G01, current U5 manual** | The retained original is RM0456 **Rev6, January 2025**, not Rev7. Its cover and original hash match. The author's failed-retrieval records were inspected, as was the coordinator's additional 75-second verified-TLS attempt with zero response bytes. No usable current original is established in this environment. That is a retrieval failure, not proof of access restriction or global unavailability. No failed route was repeated by this reviewer; no Rev6 delta sign-off or host substitution follows. |
| **C16 / G03, SE051** | The current NXP catalogue still marks AN12543 **Rev4.5** and SE051 errata **Rev1.1** account-required; their bodies were not available. AN12973 Rev2.0 §§1–2.3 supports distinguishing C2 OEF/app tuples and changing recovery credentials. AN12907 Rev1.2 §§1–3 supports the separate NXP applet-update authority and the additional key-rotation step for invalidating older scripts. Public headers do not close command, policy, errata or developer-rights gates. [NXP catalogue](https://www.nxp.com/products/SE051). |
| **C19 / G03, TROPIC** | The original public advisory v1.0 lists **TR01-C2P-T310, boot 2.0.1/app 2.0.0/SPECT 1.0.0**, and states broader current-architecture applicability. Printed pp.2–6 and 10 distinguish the physical attack, current-device maintenance mitigations, future silicon work, the **2026-06-03** disclosure and Q4 availability forecast. No received, qualified remedy follows from the forecast. The candidate correctly retains the selection gate. |
| **C12, S3 AES** | AR2026-005 v1.0's complete technical body supports the distinction between general-purpose AES-128 and flash XTS-AES. Its impact reasoning assumes short-lived/device-unique keys. An enduring SE wrapping key does not inherit that lifetime limit, and the advisory does not establish a complete fix. TRM §24's **external clock** glitch detector is not a power-glitch countermeasure that negates this advisory. |
| **C13, ST timing / physical scope** | TN1474 Rev1's required conditions include shared resources and secret-dependent secure execution, with malicious nonsecure code execution in the described attack. TN1489 Rev1 is a general physical-assurance bulletin, not a newly demonstrated break of every STM32. It requires the exact service and physical-resistance certification scope. Both support the candidate's one-trusted-image and no universal physical-isolation claims. [TN1474](https://www.st.com/resource/en/technical_note/tn1474-security-bulletin-tn1474stpsirt-information-on-softwarebased--microarchitectural-timing-sidechannel-attacks-on-mcus-with-trustzone-for--armv8m-stmicroelectronics.pdf), [TN1489](https://www.st.com/resource/en/technical_note/tn1489-security-bulletin-tn1489stpsirt-physical-attacks-on-stm32-and-stm32cube-firmware-stmicroelectronics.pdf). |
| **C14, SA0055** | Rev2 pp.1–3 affects the listed SFI binaries/configurations; for U5/L5 the impact is external-flash SFI confidentiality. U5 remedy is the matching **v6.0.0** RSSe/personalization set in **X-CUBE-RSSe ≥1.2.0**, with the specified supported programming/HSM setup. H523/533 listing does not establish H573 runtime exposure. [SA0055](https://www.st.com/resource/en/security_advisory/sa0055-sfi-security-enhancement-for-stm32h523533-microcontrollers-stm32u5-series-and-stm32l5-series-stmicroelectronics.pdf). |
| **C15, P4** | Errata v1.4 §§1–4 confirms ROM-764 on v3.0, fixed v3.1; ROM-770 on v3.1, fixed v3.2; ROM-816 on v3.2 with the specified fuse/download/POR sequence. ECDSA_DS-836 covers **v3.0/v3.1/v3.2**, while ECDSA_DS-837 covers **v0.0/v1.0/v1.3**. RSA_DS is the stated workaround for the ECDSA verification issues. This does not make all P4 configurations unusable or establish a software BIP340 defect. Replace the vague “earlier revisions” shorthand with those exact lists during revision. |

The P4 source also contains v3.0 **DMA-767** (memory-to-memory channel 0 shares
the RMT permission identity) and **Analog-765** (output-regulator behavior with
the peripheral domain off). Neither is represented as an individual ledger row.
That is tolerable for an explicitly incomplete document-only screen, but these
conditions must enter any future P4 ownership/power admission. Do not treat the
current abbreviated ledger as the complete P4 errata set.

## Host, power, bus and reference samples

**U5G9:** independent primary extraction confirms DS14102 **Rev5, May2026**;
the revision history identifies a package-information repair. §3.5 p.27 lists
the separate memory banks and SRAM3 ECC capacity effect. §7 p.344 decodes
Z/144, T/LQFP, J/UFBGA and Q/SMPS-capable pinout. The larger internal-memory
case and package distinction in C02/C03 are supported; current RM master
attribution and the exact usable workload remain open. The dynamic manufacturer
ZJJ6Q ordering row was not independently reproduced, so commercial OPN evidence
must remain traceable rather than inferred solely by decoding a valid-looking
code. [DS14102](https://www.st.com/resource/en/datasheet/stm32u5g9nj.pdf).

ES0595 Rev4's EXTI/ECC/VBAT findings match the ledger. The additional selected
DSI/SAES bodies, §§2.9–2.10 pp.19–20, are accessible: automatic DSI clock control
is constrained; EoT/HS contention indications have specific limitations; the
SAES backup-key transfer requires ascending reads for the named KEYSEL modes.
Those are useful concrete next readings, not universal failures of graphics or
SAES. [ES0595](https://www.st.com/resource/en/errata_sheet/es0595-stm32u5fxxx-and-stm32u5gxxx-device-errata-stmicroelectronics.pdf).

**New bounded lead:** [UM3223 Rev2, November2025](https://www.st.com/resource/en/user_manual/um3223-discovery-kit-with-stm32u5g9zj-mcu-stmicroelectronics.pdf)
§§1–2 pp.2–3 identifies **STM32U5G9J-DK2, MB1918/MB1860,
STM32U5G9ZJT6Q LQFP144**, with 3.3 V operation and an 800×480 RGB panel. It is
a closer package/power reference than DK1 for the ZJT6Q lead. Reviewer read
cover/§§1–2 through official web PDF extraction; a new bounded native retrieval
timed out, so original-byte hash is **null**, not invented. No schematic/full
manual review, additional port, purchase or automatic selection follows.

**Software support:** the pinned Embassy manifest and gated module declarations
were inspected directly. They support the candidate's limited statement that
U5G9 chip features and graphics drivers exist; they do not prove the complete
selected configuration, license/dependency closure or actual target execution.

**S3 and U585 pin samples:** module v1.8 Tables3-1 and6-2 support the S3 USB/SPI/
debug/strap pin witness, GPIO35–37 PSRAM reservation, and 3.0–3.6 V supply.
All 48 U585 VI/VIQ pad/signal pairs were compared with the pinned manufacturer's
XML. The Q variant's different display/UART pad numbers are preserved. XML
does not supply a completed AF/electrical/reset or DMA-security contract.
ES0499 Rev12 cover independently confirms X/0x2001, W/0x3001, U/0x3007; its
selected bodies remain work, particularly USB and UCPD paths.
[ES0499](https://www.st.com/resource/en/errata_sheet/es0499-stm32u575xx-and-stm32u585xx-device-errata-stmicroelectronics.pdf).

**Entropy:** TRM25 and the v6.1 RNG SDK body support C07's continuous-source and
fallibility concern. Passing randomness statistics or receiving a returned u32
does not establish source health. The always-mixed secondary source is not the
documented substitute for the qualified main source. A source-loss detection
mechanism and selected adapter remain unimplemented/unqualified here.

**SE services:** standard Trust M Rev3.70 Tables1–4 lists standard V3 variants
and NIST/Brainpool ECC, not a wallet-specific native BIP340 capability. The
selected HMAC/authorization manual pages support a bounded service lead only.
SE051 C2's generic curve/algorithm list likewise cannot establish a complete
non-exportable Nostr command/policy contract. C17's restraint is appropriate.

**Two power chains / 5 V sink:** TI originals support C22/C23's conditional
investigation. BQ24074's current limits and system priority do not grant USB
entitlement. BQ25628's ILIM/TS_BIAS pin assignments differ from BQ25629's D−/D+;
IINDPM resets to 3.2 A, and its watchdog resets a selected subset rather than
every field. These facts support a hardware-safe initial limit/charge policy.
TPS63802 requires startup/load/effective L/C and reverse-current analysis;
its shutdown feature is not a complete board backfeed proof. TUSB320LAI's
dead-battery/shutdown Rd and current-status functions are not a PD contract.
The candidate correctly leaves the actual USB normative clauses open; the
[USB-IF release page](https://www.usb.org/document-library/usb-type-cr-cable-and-connector-specification-release-25)
is an index, not their review. Add TPS63802 **§§9.3.5–9.3.8 pp.11–12** to the
reading locators when discussing detailed startup/reverse behavior; pp.14–17
alone cover different parts of that story.

**Reference samples:** a fresh rendering of the rehashed original TS1501 schematic
shows GPO via the 1 kΩ path to GPIO5/physical29; GPIO25 is a chip-select
option, not GPO. Safe7's main PDF display sheet shows a custom 24-contact
connector, DSI/touch/control and separate backlight/switched rails. The filename
is RevD while this sheet's title block is C; record per-sheet revisions when
needed. These selected observations support the candidate's reference limits,
not an entire Safe7 audit. SE/trusted-UI paths must remain separate from maker
expansion in the owner-secured Signer contract; no pin-count argument or
reference shield can establish that isolation.

The preserved-render pixel comparison was inconclusive because the newly
rendered images differed. The reviewer therefore inspected fresh renders of the
hashed originals directly. Only TS1501 physical page 1 and Safe7 physical page
13 were visually inspected; see [the drawing log](logs/drawing-correspondence.json).
No original drawing or rendered page is included in this public report.

## Available-source work to carry forward

These are bounded documentary tasks, not permission to run probes or add ports.
Keep each proposed host's required subset explicit and record unread sections.

| Candidate / subsystem | Concrete next reading and required result |
| --- | --- |
| S3 module / selected SPI panel / buttons | Finish TRM v1.8 §§6.10–6.13 pp.481–496, the selected GPIO registers, SPI §30.5.8.2 p.1124 and §30.6 p.1141 against the exact module pads and chosen driver's configuration. Record mux, reset, strap, sleep and competing-use constraints. Identify the panel/controller and its rails before promoting a pin witness to an allocation. |
| S3 USB / watchdog / lifecycle | Complete the selected §32.4 register path and exact driver choice of CPU FIFO or USB-master DMA; distinguish it from GDMA. Read the used watchdog paths in chapter13, including §§13.2–13.3 pp.674–679, and the selected XTS/lifecycle paths in chapter23 alongside eFuse/ROM and versioned SDK documentation. Resolve source contradictions explicitly; do not treat a disabled or unused peripheral as reviewed. |
| U585 VI and VIQ | Read DS13086 Rev10 package, supply and AF tables for the exact proposed order suffix, separately for VI/VIQ. Review ES0499 Rev12 bodies for the selected SRAM, RNG, USB and UCPD paths against the allowed X/W/U revision set. Public pin XML and a cover/summary review do not replace those bodies or the current RM0456 gate. |
| U5G9 ZJT6Q lead | Continue DS14102 Rev5 memory/supply/package/graphics constraints and ES0595 Rev4 DSI/SAES conditions for the actual proposed implementation. UM3223 Rev2's exact DK2 part and 3.3 V/RGB configuration justify bounded supply/display/connector reading and schematic acquisition; keep its new original hash null until bytes are obtained and verified. This adds no port and does not close RM0456 Rev7. |
| 5 V USB sink and two TI power chains | Read the applicable USB normative attach/current, suspend, inrush and backfeed clauses. For each exact charger/boost/controller OPN, bind CE/EN/reset/ILIM/IINDPM/NTC/charge defaults, selected watchdog behavior and startup/reverse-current conditions to an initial current budget and proposed circuit. Document permitted CC-current transitions separately from a PD contract. |
| Private SE / trusted UI / expansion | Keep inaccessible SE command/policy/errata bodies explicit; select no SE from a public algorithm list alone. Record bus/controller ownership, exposed pins and failure behavior independently for trusted UI/SE and maker expansion. The TROPIC future-fix forecast remains unqualified. |

Documentary completion establishes a proposed configuration and its allowed
revision set. H02 then checks the received hardware and binary against it.
Neither an absent kit nor a convenient manual retrieval determines the host
ranking; neither an empty admitted-host set nor existing repository tests
satisfies the H01 brief.

## Evidence integrity and limits

[The read-only probe](probes/check_evidence.py) passed with exit 0: all **11**
result-bound artifact hashes/sizes and all **50** non-null original hashes/sizes
matched. The other **20** records do not claim a validated original. Seven
independent `pdftotext -layout` extractions matched preserved text byte-for-byte.
Source IDs and claim/pin/errata references were consistent. See
[the correspondence log](logs/evidence-correspondence.json). These checks did
not detect or excuse R1/R2; actual erratum reading did.

The review sampled the stated source sections and reference sheets. It did not
re-review every one of 70 documents, every nonblocking claim, full host manuals,
all source contradictions, private firmware/reference layouts or production
designs. Web-only ST readings have no independently retained original hash.
Inherited reading stays inherited; index-only and inaccessible bodies stay open.

The author's basename-dependent `make ci` setup failure remains recorded. Its
reported unchanged 43-test run in the correctly named exact-source checkout is
repository-tooling evidence only; this reviewer did not rerun it or convert it
into manual, target or hardware acceptance. The review probe and whitespace
checks are the new checks in this branch.

After R1/R2/R3 corrections, freeze a new candidate, refresh result bindings and
have a distinct reviewer check the changed source. Continue the available U585
datasheet/errata, S3 concrete subset, U5G9/DK2 document triage and USB/power work.
Keep the RM0456 Rev7 and selected-SE gates visible. The canonical graph remains
coordinator-owned and H01 remains incomplete.
