# Responses to the first H01 substantive review

The review at original commit
`5186b7207fa397ceb4cd237d710d8adc163c6eb0` is preserved unchanged under
[independent-review](independent-review/report.md), cherry-picked as `f713951`.
It reviews source `19362fc9a12bed43070c56642b4a932f1bc6a545` and handoff
`d5d75306a082215453d329e31ca9c11d6effa80d`. Its request-changes decision is
not overwritten by these author responses.

| Request | Author action and source | Remaining recheck |
| --- | --- | --- |
| **R1, ANALOG-160 inversion** | Separate correction `16a7d4b` moves the damaging conjunction into `configuration` and states that it must be prevented. Re-read original S3 errata1.3 §3.3 p.7 with its verified hash. Follow-up IDF v6.1 sleep branches, assertions and defaults provide specific source correspondence. | Distinct reviewer checks wording and source mapping. Chosen binary/callers and any Rust/custom path remain unqualified; no damaging physical test is permitted. |
| **R2, TOUCH-100 incomplete mitigation** | Same separate correction names `TOUCH_SCAN_DONE_INT`, skips its first two occurrences, then disables/stops using those interrupts as §3.7 p.10 requires. Physical controls remain the bounded proposed input. | Distinct reviewer checks the whole erratum, not merely a sample-discard claim. No touch path admitted. |
| **R3, documentary versus received identity** | Coverage/probe plan now distinguish H01 exact **proposed** OPN/package/allowed revision/configuration from H02 **received** marking/board/binary matching. G02 and acceptance0 no longer require an already-owned kit for documentary completion. | Exact documentary proposals still need sign-off. Current RM0456 Rev7 and mandatory U5/S3 comparison remain; zero admissions cannot pass H01. |

Additional review leads were acted on: U5G9 DS14102 Rev5 selected SRAM/power/
graphics/ordering and ES0595 DSI/SAES bodies; bounded DK2 reference; current
U585 ES0499 selected bodies; TPS63802 pp.11–12; exact P4 ECDSA revision lists;
Safe7 filename versus display-sheet revision C. No additional bench port or
part choice follows. P4 DMA-767/Analog-765 remain explicit future
ownership/power checks if a P4 configuration is promoted; the ledger is not a
claim to enumerate every applicable erratum for every future configuration.

The follow-up also corrects a **locator**, including the old handoff's wording:
S3 TRM §32.4 is OTG/HNP/SRP, while **§32.5 p.1242** states the comprehensive
register documentation's NDA boundary. The independent old report is kept
unaltered; current notes and handoff carry the corrected locator. Public
software is supporting evidence, not a replacement for absent normative
hardware semantics.

The author has addressed the requests in source. **Affected independent review
is pending**, and H01 remains incomplete. Existing 43 repository tests have no
bearing on whether these manual statements are correct. A reviewer should
check the errata correction first, then selected original/manual text and the
new contradiction dispositions, USB public-access boundary, U5 revision scope,
and whether the remaining work is stated without a hidden admission.

## Limited follow-up review received

Original review `2f9ea3a18d8fb18e3fbaa8f58b6272102f83b9c2` was imported
byte-exact as `88a8c09` before new source changes. Its limited PASS closes
R1/R2/R3 wording and checked bounded claims at6f95; H01 remains incomplete.
The next candidate maps its additional findings to current-manual-notes.md:
fixed-pattern RNG build exclusion, actual TinyUSB device waits, U585
revision-specific reset/low-power restrictions, and newly retrieved current RM.
This new substance requires a distinct affected review; neither prior report
has been rewritten.
