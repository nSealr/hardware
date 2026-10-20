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

Every retained claim points to a locator and an owner in [claims.json](claims.json).
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
