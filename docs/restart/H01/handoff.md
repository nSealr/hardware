# H01 corrected source candidate handoff

Substantive source commit:
**6b45f6f79e1888bdf2ec6680d14dd951b7019327**, branch
[`restart/h01-manuals`](https://github.com/nSealr/hardware/tree/restart/h01-manuals).
[result.json](result.json) binds 21 exact source artifacts and the separate
verification records. The approved brief/input remain unchanged.

**H01 is running/incomplete. No host or component is admitted.** Acceptances
1 and 5 cannot pass from zero admissions, repository tests or the volume of
research. The current RM0456 Rev7 and concrete host-subset gates remain. The
coordinator owns task-state decisions.

The old source `19362fc9a12bed43070c56642b4a932f1bc6a545` and handoff
`d5d75306a082215453d329e31ca9c11d6effa80d` are immutable review inputs.
Their distinct review, original `5186b7207fa397ceb4cd237d710d8adc163c6eb0`,
is preserved unchanged by cherry-pick `f713951208a4df3632f470c664358f275ab6e256`.
It requested changes. Separate commit
`16a7d4bfaa9b144581ae06fb67424718ffb10482` corrects ANALOG-160 and TOUCH-100
and distinguishes proposed from received hardware identity.
[review-response.md](review-response.md) maps R1/R2/R3; affected independent
review of this fresh candidate is pending.

The follow-up adds actual reading: S3 GPIO/interrupt/reset, watchdog and XTS
text; SPI state/timing; pinned vendor entropy/sleep functions and USB wrapper
configuration; U5G9 selected power/graphics/package/ordering and DSI/SAES errata;
current U585 USB/SPI/memory/watchdog/UCPD errata bodies; DK2 reference triage;
and TPS63802 startup/reverse-current details. New contradictions are retained.
S3 TRM **§32.5 p.1242** places comprehensive USB register specifications behind
an IP-provider NDA; **§32.4 is OTG/HNP/SRP**, correcting the old handoff locator.
Public headers are supporting software evidence, not normative IP semantics or
DMA-isolation proof.

There are now 81 source records, 27 claims, 25 pin witness rows, 25 errata rows
and 11 source contradictions. These describe coverage, not a quality score or
an exhaustive errata set. See [host-subset-notes.md](host-subset-notes.md) for
exact reading and interpretation limits.

## Remaining actionable work

| Work | Precise next evidence |
| --- | --- |
| **S3 proposal, pins and input** | Specify proposed exact kit/module/package, documented board revision, allowed silicon/ROM/configuration and complete panel/controller/rail/control requirements. Module1.8 p.31/application diagrams, proposed kit schematic/header/RGB conflicts and used GPIO routing/filter portions beyond the reviewed selections remain. GPIO10–13 function4 and reset/interrupt text are now read; they do not allocate panel control pins. H02 later identifies the received unit. |
| **S3 SPI** | Selected transaction/error/DMA registers and exact maintained driver still need correspondence. The state/CS timing and register30.6 text have been read. Reconcile the new table-footnote bit-order contradiction without adopting a guessed recipe. Panel/FPC timing and loading remain separate. |
| **S3 USB** | Lock the underlying TinyUSB dependency rather than relying on esp-usb's lower bound; bind the actual preprocessed device/CPU-FIFO-or-DMA configuration and endpoint/FIFO/reset/interrupt/timeout path. Close only required §32.5 IP-semantic questions, using lawful documentation. Unused host/DMA modes need not expand the probe. No external manufacturer inquiry has been sent. |
| **S3 lifecycle, reset and entropy** | Watchdog/XTS chapter text is now read. Still bind chosen stages/clocks/reset domains, all sleep callers, plaintext-buffer cleanup, ROM download allowlist, eFuse/bootloader-update contradictions and actual fallible entropy/crypto adapter. Reviewed IDF assertions/defaults do not qualify a different Rust path or assertions-disabled custom caller. Never physically exercise ANALOG-160's forbidden condition. |
| **U585 available documentation** | Current ES0499 selected bodies are accessible and recorded; finish applicable core/system/clock/retention/I2C bodies and exact allowed X/W/U/RSS/bootloader configuration. Read current DS13086 VI/VIQ AF/pad/electrical tables. Correspond selected USB/SPI mitigations to actual driver, resolving the documented wording issues. Current RM0456 remains a distinct gate. |
| **U5G9 bounded triage** | SRAM bank text, selected power/graphics and DSI/SAES errata are read. Exact ZJT6Q/ZJJ6Q pad/AF/rail mapping, package drawing correspondence, graphics-master/current-RM ownership, driver/license and workload budget remain. DK2 has a closer LQFP144/3.3V/RGB reference; UM3223 full relevant power/connector/schematic and original hash remain open. No new bench port. |
| **Current ST manual access** | RM0456 **Rev7 March2026** original/current relevant delta remains unavailable through recorded bounded routes. Rev6 is not a substitute. Seek a genuinely new lawful route; do not repeat failed routes without new evidence. Other ST web excerpts being accessible does not close the missing reference manual, and this gap does not choose S3. |
| **SE, USB power and expansion** | Continue useful accessible standard Trust M/TROPIC command/object/channel/reset/counter work while keeping selected SE051 API/errata access and TROPIC remediation hard gates. Read current USB normative clauses and exact power-chain/cell/panel/expansion requirements. Retain two power investigations. No owned kit, measured rail, SE fix or manufacturing choice is inferred. |

H01 documentary admission binds exact **proposed** parts, allowed revisions,
configuration and reviewed source conditions. It requires no already-owned kit.
H02 independently checks actual received hardware/binary before execution.
Neither distinction permits vacuous completion or waives the U5/S3 comparison.

## Verification and review request

JSON/unique-ID/reference checks pass; the nine new source-byte hashes and sizes
match their private originals. Existing 70 source identities were compared
with the old source record without changing their original hashes. The approved
brief/input hashes remain unchanged. These are integrity checks, not manual
correctness checks.

The fresh exact source `6b45f6f` passed unchanged `make ci` in the separately
owned, correctly named `/goal/h01-ci/hardware` checkout: repository verification,
all **43** existing tests, compilation checks and hardware-document validation.
[The actual log](checks/ci-6b45f6f.log) is preserved. The old author-worktree
basename failure remains recorded rather than changing the verifier. No target
port/build, new prose-matching test, physical measurement or provisioning ran.

Requested affected independent review: check R1/R2 against the original errata
and pinned sleep correspondence; check R3 documentary/received boundaries;
sample new manual locators and source hashes; assess new SPI/XTS/U585 USB
contradictions and §32.5 access limits; verify current U5 errata applicability
and U5G9/DK2 limits; confirm every blocking claim remains an actual gate.
Review source substance before counts or schema checks. The old request-changes
review is evidence, not approval of these changed files.
