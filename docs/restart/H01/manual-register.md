# H01 manual register — selected review, incomplete host gate

**Explicitly resumed by the maintainer on 20 October 2026.**
The same day's brief stop was explicitly revoked before the subsequent kit/boot
checkpoint; H01 remains active and incomplete.
[Resumed source notes](resume-source-notes.md) bind the new selected
cache/GPIO/watchdog and kit reading. [Pause reading notes](pause-reading-notes.md)
and [PAUSE-HANDOFF.md](PAUSE-HANDOFF.md) remain historical recovery evidence,
including the corrected VIQ package allocation. No new host sign-off or
independent acceptance is implied.

The auditable record is [manual-register.json](manual-register.json). It records
original-byte hashes where an original was obtained, exact URLs, revisions,
reviewed sections, inherited correspondence and remaining work. No manufacturer
manual is redistributed here. A null hash is an access/retrieval gap, not a hash
of extracted text or an HTML error page. A source entry is not a full-manual read.

The 20 October [U585 field manifest](u585-peripheral-manifest.json) records the
source-derived lock/reset/clock proposal. The later
[S3 fixed-CDC assessment](s3-usb-serial-assessment.md) registers23 bounded public
source/original files, including full AR2022-004 V1.1 and the selected IDF
driver/compile controls. Unrelated fetched bodies remain unread, and the
alternative is unselected. The resulting147 document entries are an inventory.
The subsequent [U585 SPI correspondence](u585-spi-review.md) adds3 pinned
software/metadata sources; the current150 entries remain an inventory, with
every actual read range and unread remainder distinguished in JSON.

The later [two-host memory contract](memory-ownership-contract.md) registers
three pinned IDF app/bootloader linker sources and selected current memory,
PMS/lock, master/core reset and HAL initialization correspondence. The195 entries
remain an inventory, with exact reading and excluded bodies in JSON. Fixed
address/copy/stack/queue caps are unmeasured qualification proposals; no alias
double count, admitted fit, physical clearing or hostile-app isolation follows.

**H01 is not complete and no U5 or S3 host probe is admitted by this candidate.**
RM0456 Rev7 is now a verified current original with selected body reading. The
remaining mandatory current-body and concrete-subset checks remain in [review-coverage.md](review-coverage.md). SE-specific gaps do not
block unrelated host research, but remain hard selected-service gates.

The first source candidate's independent review requested changes. Its evidence
is preserved, and [review-response.md](review-response.md) maps the author fixes.
The limited follow-up review is preserved in
[independent-review-followup/report.md](independent-review-followup/report.md).
[current-manual-notes.md](current-manual-notes.md) records the new actual reading;
none of it silently promotes a source inventory into complete host admission.
[configuration-review.md](configuration-review.md) adds current U585
security/flash/power body findings, proposed kit/header identities and real panel
contradictions. [usb-configuration.md](usb-configuration.md) records actual
current normative clauses and remaining controller/power requirements.
The resumed increment additionally establishes U585 internal-SRAM cache bypass,
the G9 GPU2D/DCACHE2 nonsecure exception, GPIO silent-zero input hazards, the
3.3 V HSLV prohibition, IWDG early-wake reload behavior and kit startup branch
limits. Exact scopes and remaining configuration work are in the resumed notes.

| Register IDs | Version and actual reading | Consequence |
| --- | --- | --- |
| `u5-rm7`, `st-u5-rm6-jp` | Verified official Rev7 March2026 original,3651 pages; selected masters/reset/clock/RNG/USB text and revision history now read. Preserved Rev6 retains only its historical coverage. | Retrieval closed through bounded curl-cffi HTTP/2; prior failures preserved. Remaining used current body/delta and exact configuration still prevent H01 sign-off. |
| `u585-ds`, `u585-es` | DS13086 Rev10 July2024 selected features/SRAM/supply/reset excerpts. ES0499 Rev12 June2026 summary plus selected memory/flash, SAES, LPTIM/IWDG, SPI, USB and UCPD bodies now read. | Native originals now hashed; core/system pp.7–16 also read with X/W/U mapping. Exact VI/VIQ electrical/AF and remaining used errata/driver correspondence remain. |
| `u5g9-ds`, `u5g9-es`, `u5g9-opn`, `u5g9-kit`, `u5g9-dk2`, `u5g9-um3223` | DS14102 **Rev5 May2026** selected SRAM/power/graphics/ordering text; ES0595 Rev4 selected DSI/SAES bodies now read. Native current originals hashed; UM3223 cover/§§1–2 and7.5–8.6 directly read. LQFP144/UFBGA144 outlines visually inspected and mechanical tables read. | Exact pads/AF/rails/GTZC/driver/license remain. DK2 PC13 button plus LSE crystal intersects ES0595§2.2.1;50-pin RGB is not DSI or a universal FPC. No footprint/board qualification. |
| `u5a5-ds`, `u5a5-es`, `st-h5-98864_en`, `h573-ds`, `h573-es` | U5A family DS13543 Rev3 feature screen; H573 DS14121 Rev5 feature screen; current preserved H5 RM0481 Rev5 only §3.11 lifecycle inherited. Remaining current errata/subsets incomplete. | Conditional alternatives, not additional admitted ports. |
| `s3-module`, `s3-trm`, `s3-es` | Module v1.8: variants/pins/straps/electrical/current/flash; pinout p.10 visually checked. TRM v1.8: exact selected page list covers DMA/memory/eFuse/clock/reset/GPIO/interrupt/timer/power/PMS/world/USB/SPI/RNG. Errata v1.3: all technical §§1–4. | Stronger selected coverage, not a full 1531-page manual read. Exact selected driver, pin/configuration and unresolved register-wording checks remain. |
| `s3-rng-sdk`, `s3-boot-sdk`, `s3-flash-sdk`, `s3-ota-sdk`, `s3-usb-sdk-current`, `s3-board` | Versioned IDF v6.1 selected technical bodies; redirected USB component page and DevKitC guide are mutable snapshots with original HTML hashes. | SDK describes software expectations; chip behavior still needs TRM/errata correspondence. No target build or fuse operation occurred. |
| `s3-idf-random`, `s3-idf-boot-random`, `s3-idf-sleep`, `s3-idf-rtc-header`, `s3-idf-usb-struct`, `s3-idf-usb-ll`, `s3-usb-component`, `s3-usb-config`, `s3-usb-device` | Nine freshly hashed immutable source files; exact full/selected function and line coverage in JSON. RNG functions, sleep avoidance correspondence, USB direction fields and wrapper configuration/dependency boundary read. | Source behavior does not qualify a chosen binary or replace comprehensive USB IP register specifications, which TRM §32.5 p.1242 identifies as NDA-limited. The wrapper's lower-bounded TinyUSB dependency is not an exact driver lock. |
| `s3-ar2026-005`, `st-tn1474`, `st-tn1489`, `st-sa0055` | Current manufacturer technical security bulletins read; ST originals unavailable, web extraction clearly labelled. | Scope includes physical AES fault attack, shared-resource timing, exact certified-service limits and affected SFI manufacturing tuples. No blanket security ranking. |
| `p4-ds`, `p4-es`, `esp-classic-ds` | P4 DS pre-release0.7 feature screen; errata v1.4 October12'26 all technical body; classic ESP32 DS5.3 feature/status screen only. | P4 boot/maintenance gates bind actual silicon and algorithm. Classic ESP32 is not S3. |
| `nxp-mcxn947-ds`, `mcxn947-rm`, `mcxn947-security-rm` | Fresh DS8.2 pp.1–6 feature/package/revision/resource screen. Current RM7/security-RM6 catalogue entries require an account; bodies unread. | No additional port or security-state assumption. |
| `nxp-se051-*`, `nxp-se05x-api`, `nxp-sems-update`, `nxp-host-binding` | Preserved public DS/configuration/update selected sections rehashed; current catalogue checked. API/errata/middleware/personalization access remains unresolved. | Mandatory exact command, policy, errata, update and developer-distribution documentation before H02S/H04 selection. |
| `optiga-m-*` | Preserved DS3.70, reference manual3.70, releases3.02, I2C2.03 rehashed; only recorded algorithm/pin/HMAC/authorization/derivation/release excerpts inherited. | Complete object/channel/counter/reset/update state machine and exact standard purchasable configuration remain open. |
| `tropic-*` | Preserved DS A.11/API1.4/PIN1.2/pairing1.3/catalogue2/advisory1.0 matched; selected original review retained. Fresh preparation advisory bytes agree. | T310 is explicitly within advisory scope; no qualified fix or native Nostr signing/ECDH inferred. |
| `ti-bq24074`, `ti-bq25628`, `ti-tps63802`, `ti-tusb320lai`, `diodes-ap2112` | Fresh TI originals match archived hashes; selected functional/startup/current-limit/watchdog/regulation/CC sections read. AP2112 selected historical dropout evidence rehashed. | No chosen chemistry/OPN, thermal/current qualification or complete implementation circuit. |
| `usb-c-normative`, `usb-typec-r2p5`, `usb2-*`, `nxp-i2c-spec` | Current Type-C2.5 and USB2/ECN bundle originals retrieved and selected sink/power clauses read in usb-configuration.md. Remaining applicable clauses open. UM10204 Rev7 original and narrow recorded I2C evidence retained. | Component/application notes cannot close USB normative clauses or actual bus loading/timing. |
| `embassy-stm32-*`, `esp-hal-cargo`, `esp-rust-book` | Exact source commits and original hashes; declared feature/module/toolchain screen only. | Neither a feature declaration nor source readability is a verified driver, target build, license audit or maintained release choice. |
| `st-pins-*`, `ref-safe7-main`, `ref-ts1303/1401/1501/1702` | Exact ST XML signal/pad correspondence and same-hash selected visual drawings retained. | No approved netlist/footprint. XML lacks the electrical/AF/master proof; reference exports lack native assembly/layout qualification. |

New primary rows `u5-an4230`, `nist-e11-public-use`, `nist-e116-public-use`,
`u5-embassy-rng` and `s3-tinyusb-*` document the current entropy configuration,
CED wording conflict, candidate RNG policy/wait gaps and the actual device USB
reset/FIFO/IRQ path. Exact source versions and read ranges are in JSON; no
resolved target build or physical result is inferred.

The [U585 kit/boot correspondence](u585-kit-usb-boot-review.md) adds AN2606,
the official MB1551 design archive and OPLA metadata, and selected TCPP03/kit
reading. The register now has153 entries and53 claims. Its explicit correction
withdraws the initial apparent pin9/11 conflict: native PDF, SchDoc and PCB agree.
ROM resource ownership, watchdog behavior, mode-dependent USB status and the
currently excluded ADC4 sensing path still require concrete policy.

[U585 I2C/CC correspondence](u585-i2c-ucpd-review.md) adds6 exact source
originals,159 total document entries and57 claims. Selected current I2C/UCPD
register/body and native clock-tree reading distinguishes actual counted
completion, deadline features, revision-specific trimming and the HSI16/PCLK1
metadata discrepancy. A source count is not a complete configuration signoff.

[U585 OTG source correspondence](u585-otg-source-review.md) adds4 existing
candidate dependency originals,163 total entries and61 claims. CPU FIFO/endpoint
facts correspond, while effective time features, warning-only recovery, ZLP
erratum handling and software VBUS behavior remain unqualified. Remaining
endpoint/control/interrupt/time-base reading and distinct review stay open.

[U585 interrupt/core-time correspondence](u585-interrupt-review.md) adds the
current PM0264 Rev8 native original and17 selected IRQ mappings against both
exact AI/VI metadata objects.164 entries/64 claims remain selected evidence,
not a completed host. The [finite closure checklist](closure-checklist.md)
fixes the remaining ten H01 work items and separates later H02/H04 evidence.

Every retained claim points to a locator and an owner in [claims.json](claims.json).

[U585 clock/power correspondence](u585-clock-power-review.md) records the
existing kit's U19/X2 and pinned RCC dependency sources,174 document entries
and74 claims. Its [conditional calculation tuple](u585-clock-proposal.json)
does not establish an actual clock, bounded stock startup, permitted USB supply
or complete host. The coordinator's conditional display milestone allocation
is recorded in [panel-subset-review.md](panel-subset-review.md), retaining the
exact module-evidence H02 stop and mandatory H01 external interface limits.

[S3 fixed-CDC contract correspondence](s3-usj-contract.md) adds6 exact pinned
source originals,180 entries and77 claims. Public FIFO/IRQ fields and selected
owner-security helper/shared-lock behavior now have exact reading scopes.
This is neither an effective build nor a completed power/descriptor/lifecycle
contract. Fixed CDC and the conditional external attach fixture remain
unselected; original code/manuals and the native register render stay private.

[Conditional S3 attach/descriptor correspondence](s3-attach-contract.md) adds
selected current USB normative and exact kit/module/electrical reading, keeping
180 documents and79 claims. Thresholds, GPIO8 status and autonomous isolation
are proposed fixture requirements; the descriptor/status gate can still reject
self-power. Three new private native ECN renders resolve selected redlines
and preserve the resistor figure/table discrepancy. No new component lead or
physical result is introduced.

[S3 clock/time correspondence](s3-clock-time-review.md) adds8 exact pinned
clock/SYSTIMER source originals,188 entries and81 claims. Selected current
clock/timer body and native register/reference-module reading make the
conditional CPU160/APB80/PLL480 and UNIT1 polling tuple reviewable. Finite
snapshot/PLL remedies and reference/PHY/effective-feature conditions remain;
no stock source or actual clock is qualified.

[Two-host entropy/crypto correspondence](entropy-contract-review.md) adds4
exact existing S3 dependency originals,192 document entries and83 claims.
Its finite provider/ownership/failure table preserves S02 all-or-error semantics
and source limits. Nominal U585 HSI48/A is only the coordinator's conditional
documentary reference, with an explicit pre-use H02 stop. S3 internal SAR
source/health and actual call-path qualifications remain pre-use gates. No
entropy or real identity was generated, no new ADC/timer/backend was selected,
and the native pattern/example difference is not called an SDK defect.

[Existing Newhaven panel correspondence](panel-subset-review.md) adds the
current breakout product/specification and the raw module's recommended
connector identity,167 entries/69 claims. The breakout is a different
AF/ST7789VI assembly and is deferred for the common four-wire/DC/backlight
proposal. Raw DB/ILI9341V command/reset/mechanical reading does not resolve
its startup/internal-power, normal rail margin or fixture requirements. The
initial private CB/CF absence inference is withdrawn after actual list/body
reading. C02 and all six host signoff rows remain open.
The [pin/errata ledger](pin-errata-ledger.json) retains adverse findings and
contradictions, including S3 RTC address/provisioning/download/USB register
wording, XTS-enable and SPI-bit-order discrepancies, current U585 USB wording,
P4 algorithm/revision limits, and U5G9 package revision changes. Unread
sections remain unread even where a document was successfully downloaded.

The public analysis is newly written. Reuse of private historical research is
limited to verified public source identity and actual previously reviewed
sections/pages. Original hashes were recomputed before reuse; the public record
does not copy private working histories. Repository heads checked during
preparation still matched the pinned TROPIC/Safe7 sources; later Infineon/NXP
repository checks likewise matched. This is a dated currentness check, not a
promise that vendor documentation will never change.

The [U585 endpoint/control table](u585-usb-endpoint-contract.md) records the
finite C06 reading, four new native register/formula views and selected USB2
standard-request/endpoint and applicable errata text. The195-source inventory
does not grow in this increment. OUT64/68 remains an unsatisfied source
property; source triage is not a completed criterion, driver or USB admission.

The [S3 SPI/input source table](s3-spi-input-contract.md) adds four pinned IDF
driver/LL originals with exact selected functions and unread callees distinguished,
plus two native SPI bit-order/event views. The199 entries remain an inventory.
Observed source gaps imply finite adapter/ownership requirements, not an
upstream failure reproduction, driver selection, USB/kit or display admission.
