# H01 manual register — selected review, incomplete host gate

The auditable record is [manual-register.json](manual-register.json). It records
original-byte hashes where an original was obtained, exact URLs, revisions,
reviewed sections, inherited correspondence and remaining work. No manufacturer
manual is redistributed here. A null hash is an access/retrieval gap, not a hash
of extracted text or an HTML error page. A source entry is not a full-manual read.

**H01 is not complete and no U5 or S3 host probe is admitted by this candidate.**
RM0456 Rev7 is a mandatory unresolved current-manual gap. Other concrete subset
checks remain in [review-coverage.md](review-coverage.md). SE-specific gaps do not
block unrelated host research, but remain hard selected-service gates.

| Register IDs | Version and actual reading | Consequence |
| --- | --- | --- |
| `u5-rm7`, `st-u5-rm6-jp` | Current official locator identifies RM0456 Rev7 March2026. Web-reader/native retrieval did not yield the original. Preserved Rev6 January2025 is hashed; only its recorded memory/security/lifecycle excerpts are inherited. | No current register or relevant delta sign-off from the historical text. Native ST, DM-ID, China, family and Japan alternatives were tried; the guessed Japan “Rev7” response was HTML, not PDF. |
| `u585-ds`, `u585-es` | DS13086 Rev10 July2024 selected features/SRAM/supply/reset excerpts through primary web extraction. ES0499 Rev12 June2026 applicability/index only. | Exact VI/VIQ electrical/AF, supply pads and selected erratum bodies remain open. |
| `u5g9-ds`, `u5g9-es`, `u5g9-opn`, `u5g9-kit` | DS14102 **Rev5 May2026** supersedes stale Rev4 snippets; selected feature/security/lifecycle extracts. ES0595 Rev4 July2026: summary and core/system body pp.1–9. Exact ZJ OPN table and distinct NJ-kit overview read. | LQFP144 versus UFBGA144 is explicit. No package drawing visual clearance. Full memory/power/graphics path and DSI/SAES erratum bodies remain open. |
| `u5a5-ds`, `u5a5-es`, `st-h5-98864_en`, `h573-ds`, `h573-es` | U5A family DS13543 Rev3 feature screen; H573 DS14121 Rev5 feature screen; current preserved H5 RM0481 Rev5 only §3.11 lifecycle inherited. Remaining current errata/subsets incomplete. | Conditional alternatives, not additional admitted ports. |
| `s3-module`, `s3-trm`, `s3-es` | Module v1.8: variants/pins/straps/electrical/current/flash; pinout p.10 visually checked. TRM v1.8: exact selected page list covers DMA/memory/eFuse/clock/reset/GPIO/interrupt/timer/power/PMS/world/USB/SPI/RNG. Errata v1.3: all technical §§1–4. | Stronger selected coverage, not a full 1531-page manual read. Exact selected driver, pin/configuration and unresolved register-wording checks remain. |
| `s3-rng-sdk`, `s3-boot-sdk`, `s3-flash-sdk`, `s3-ota-sdk`, `s3-usb-sdk-current`, `s3-board` | Versioned IDF v6.1 selected technical bodies; redirected USB component page and DevKitC guide are mutable snapshots with original HTML hashes. | SDK describes software expectations; chip behavior still needs TRM/errata correspondence. No target build or fuse operation occurred. |
| `s3-ar2026-005`, `st-tn1474`, `st-tn1489`, `st-sa0055` | Current manufacturer technical security bulletins read; ST originals unavailable, web extraction clearly labelled. | Scope includes physical AES fault attack, shared-resource timing, exact certified-service limits and affected SFI manufacturing tuples. No blanket security ranking. |
| `p4-ds`, `p4-es`, `esp-classic-ds` | P4 DS pre-release0.7 feature screen; errata v1.4 October12'26 all technical body; classic ESP32 DS5.3 feature/status screen only. | P4 boot/maintenance gates bind actual silicon and algorithm. Classic ESP32 is not S3. |
| `nxp-mcxn947-ds`, `mcxn947-rm`, `mcxn947-security-rm` | Fresh DS8.2 pp.1–6 feature/package/revision/resource screen. Current RM7/security-RM6 catalogue entries require an account; bodies unread. | No additional port or security-state assumption. |
| `nxp-se051-*`, `nxp-se05x-api`, `nxp-sems-update`, `nxp-host-binding` | Preserved public DS/configuration/update selected sections rehashed; current catalogue checked. API/errata/middleware/personalization access remains unresolved. | Mandatory exact command, policy, errata, update and developer-distribution documentation before H02S/H04 selection. |
| `optiga-m-*` | Preserved DS3.70, reference manual3.70, releases3.02, I2C2.03 rehashed; only recorded algorithm/pin/HMAC/authorization/derivation/release excerpts inherited. | Complete object/channel/counter/reset/update state machine and exact standard purchasable configuration remain open. |
| `tropic-*` | Preserved DS A.11/API1.4/PIN1.2/pairing1.3/catalogue2/advisory1.0 matched; selected original review retained. Fresh preparation advisory bytes agree. | T310 is explicitly within advisory scope; no qualified fix or native Nostr signing/ECDH inferred. |
| `ti-bq24074`, `ti-bq25628`, `ti-tps63802`, `ti-tusb320lai`, `diodes-ap2112` | Fresh TI originals match archived hashes; selected functional/startup/current-limit/watchdog/regulation/CC sections read. AP2112 selected historical dropout evidence rehashed. | No chosen chemistry/OPN, thermal/current qualification or complete implementation circuit. |
| `usb-c-normative`, `nxp-i2c-spec` | USB release index only, normative review open. UM10204 Rev7 original and narrow recorded I2C evidence retained. | Component/application notes cannot close USB normative clauses or actual bus loading/timing. |
| `embassy-stm32-*`, `esp-hal-cargo`, `esp-rust-book` | Exact source commits and original hashes; declared feature/module/toolchain screen only. | Neither a feature declaration nor source readability is a verified driver, target build, license audit or maintained release choice. |
| `st-pins-*`, `ref-safe7-main`, `ref-ts1303/1401/1501/1702` | Exact ST XML signal/pad correspondence and same-hash selected visual drawings retained. | No approved netlist/footprint. XML lacks the electrical/AF/master proof; reference exports lack native assembly/layout qualification. |

Every retained claim points to a locator and an owner in [claims.json](claims.json).
The [pin/errata ledger](pin-errata-ledger.json) retains adverse findings and
contradictions, including S3 RTC address/provisioning/download/USB register
wording, P4 algorithm/revision limits, and U5G9 package revision changes. Unread
sections remain unread even where a document was successfully downloaded.

The public analysis is newly written. Reuse of private historical research is
limited to verified public source identity and actual previously reviewed
sections/pages. Original hashes were recomputed before reuse; the public record
does not copy private working histories. Repository heads checked during
preparation still matched the pinned TROPIC/Safe7 sources; later Infineon/NXP
repository checks likewise matched. This is a dated currentness check, not a
promise that vendor documentation will never change.
