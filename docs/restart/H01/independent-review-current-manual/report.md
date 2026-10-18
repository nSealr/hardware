# H01 independent current-manual review

**PASS, limited to the accuracy of the affected research and retained corrections at the exact candidate below. H01 remains INCOMPLETE. No host, part, wiring, probe execution, or security qualification is admitted.** One low-priority stale-status sentence should be corrected in the next author change. This verdict does not satisfy acceptance 1 or 5, and zero admissions cannot satisfy either criterion.

Reviewer: `/root/h01_substance_review`, distinct from the author; 2026-10-18. Isolated branch `review/h01-current-manual`. Only this new review directory was written. The author checkout and both historical review directories were left unchanged.

| Binding | Exact value |
| --- | --- |
| Frozen candidate | `e39015ae20efd37d509054f4b98ddd68ee7e98c9` |
| Substantive source | `4d50d155c994e8e770d2b868c371cc04b646ad35` |
| Author result SHA256 | `5c10be2874d6eb6eb194f1c71259a95f3197fb7aef79b085064ee8a601b7836e` |
| Author handoff SHA256 | `2f8d26bdedd671e1d91e47639192bf049c3cfdac5293a4e3c177dc8ac76a5240` |
| Approved unchanged brief | `e10dd2426146e0aa3bbcf04af6a9b1bb59f7e868` |
| Distinct brief approval | `8041bac701f32aa289f6cfba019a7baaac04403e` |
| Prior limited review | `2f9ea3a18d8fb18e3fbaa8f58b6272102f83b9c2`, covering `6f95cc298c5a8108d5c0bdaedfd53e7b81b130ed` |
| Original request-changes review | `5186b7207fa397ceb4cd237d710d8adc163c6eb0`, covering `d5d75306a082215453d329e31ca9c11d6effa80d` |

## Finding and retained boundaries

**CM-1 — low, stale wording:** `option-comparison.md:101` still calls the present U5 host gate an “independent missing-manual problem.” Replace that with “remaining current-manual content and configuration review.” The current original exists and is independently verified. The opening of that file, current notes, result and coverage correctly say retrieval is closed, so this does not invalidate the substantive progress. The approved historical brief and immutable past reviews should retain their original wording and dates.

No new blocking source error was found in the affected claims. Earlier R1/R2/R3 remain fixed: the damaging ANALOG-160 conjunction is prohibited; TOUCH-100 retains the instruction to stop using the interrupts after the first two; H01 proposed identity and H02 received identity remain separate. I reread the manufacturer's two erratum bodies and the current ledger. No physical exercise of the damaging condition is permitted by this review.

The current U5 register access problem has changed from retrieval to incomplete content/configuration coverage. Source links, a successful download, the Rev 7 revision-history list, and 43 existing repository tests cannot close that coverage. No already-owned kit is necessary to finish the documentary proposal. Conversely, the missing kit/panel/configuration definition cannot be represented by an empty admitted-host set and called complete.

## Current original and evidence correspondence

The private author and coordinator copies of [RM0456](https://www.st.com/resource/en/reference_manual/rm0456-stm32u575585-armbased-32bit-mcus-stmicroelectronics.pdf) are byte-identical: 73,588,589 bytes, SHA256 `6edaaaae0c5d57c58ffc3a576d44e7b62e8d9cd0e495e8f61bab688226fc327c`. The cover and revision history establish Rev 7, March 2026 / 30 March 2026, 3651 pages. The recorded verified-TLS official retrieval is consistent with those retained bytes. Earlier timeout and size-cap attempts remain historical; they no longer establish present unavailability or access restrictions.

The [read-only probe](probes/check_bindings.py) and [result](logs/bindings.json) independently checked:

- All 26 author source-artifact hashes/lengths and their equality to the substantive commit; all four separately retained verification artifacts; exact result and handoff hashes.
- All 81 prior source identities: 75 unchanged identities, six originally null PDF hashes now resolved, plus nine new identities. This checks identity continuity, not fresh reading of 90 manuals or fresh availability of unchanged URLs.
- All 15 new/resolved retained original hashes and sizes, plus the unchanged pinned ESP-IDF random source used by the new build-exclusion claim.
- Eight fresh native PDF text extractions, including the complete current RM, exactly matching the private text used for reading. E11 DOCX text was independently extracted from ordered `w:t` elements and matched with whitespace removed. The DOCX embedded diagram was not inspected.
- Two fresh `pdftoppm` native DS14102 outline renders, byte-identical to the images visually inspected by this reviewer. Only hashes are retained; temporary renders were deleted.
- All 11 historical review files byte-for-byte against their original review commits; approved brief/input unchanged; unique source IDs and valid claim/pin/errata references.

The first probe run failed because my filename selector appended another extension to source IDs already ending in `.c`/`.h`. The exact files existed. I corrected that selector and reran without relaxing any hash expectation; the corrected run passed. [Execution note](logs/probe-execution.json) preserves that distinction. This was a reviewer probe defect, not a candidate or manufacturer failure.

No manufacturer PDF, extracted chapter, drawing or private history is redistributed here. The checked original hashes are in the bound register and the review log. Original acquisition/provenance, successful text correspondence and substantive reading are distinct evidence layers.

## Substantive findings checked against originals

### U5 RNG contract and product configuration

I read the complete functional/register text of current RM chapter 48, pp.1903–1919, including output FIFO behavior, startup/continuous health tests, clock errors, conditioning reset, RCC reset, tamper, power-mode sequencing and the register map. The candidate's conclusions are supported: output acceptance needs the status/data-ready contract and zero-word race check; a reset or disable does not imply all configuration or data state has been cleared; restoring the intended source policy is part of recovery. RM §48.7.1 makes CED bit 5 active low. Configuration locking and conditioning reset differ from central peripheral reset.

I also read [AN4230 Rev 14](https://www.st.com/resource/en/application_note/an4230-random-number-generation-validation-using-nist-statistical-test-suite-for-stm32-microcontrollers-stmicroelectronics.pdf) §5.1.1/start §5.1.2, §5.1.2.3, Tables 3–4 and revision history (pp.14,18–21,29), and the full extracted [E11 v1.1](https://csrc.nist.gov/CSRC/media/projects/cryptographic-module-validation-program/documents/entropy/E11_PublicUse.docx) and [E116 v1.2](https://csrc.nist.gov/CSRC/media/projects/cryptographic-module-validation-program/documents/entropy/E116_PublicUse.pdf) public-use texts. The product distinction is material:

| Evidence tuple, not an execution recipe | U575/U585 | U5Fx/U5Gx |
| --- | --- | --- |
| AN4230 Table 3 configuration base | `RNG_CR=0x00F00D00` | `RNG_CR=0x00F11F00` |
| Table 3 HTCR / NSCR | `0xA2B0` / `0x17CBB` | `0xA715` / `0x9049` |
| Public-use source | E11 v1.1, hardware “revision B and later” | E116 v1.2, revision Z |
| Public-use threshold evidence | E11 also describes `0x06E9C` for a different false-alarm parameter; it is not the Table 3 choice | E116 describes RCT 41 / APT 789 and explicitly corrects earlier NISTC bit 12 wording |
| Assessment conditions listed | CPU/AHB 160 MHz, RNG kernel 48 MHz, 25 °C, 3.3 V | CPU/AHB 160 MHz, RNG kernel 48 MHz, 25 °C, 3.3 V |

Those CR bases omit the final enable/interrupt/lock policy and the required write sequence. They must not be issued as a one-write initialization recipe. The NIST-hosted documents say to set bit 5 for clock-error detection; the current RM explicitly specifies the opposite polarity and AN4230's listed values clear it. `D-U5-RNG-CED` correctly preserves that conflict. AN4230's U545 example must not replace either product tuple. Special raw-noise test access is not an ordinary-kit capability. Output statistics or an RNG trait cannot establish certification reuse.

Before an actual certificate-use claim, reconcile E11's “revision B and later” language with the intended U585 revision and the current X/W/U identification scheme; do not infer that mapping from alphabetic order. Similarly, `RNG_VERR` in the public-use documents is not an authorization to access an undocumented public-RM register. These are remaining applicability questions, already consistent with the register's limited status.

### Pinned Embassy RNG source

I read all 729 lines of [rng.rs at `69006a4158aa6d605ad8506ade0f2f79159131e3`](https://github.com/embassy-rs/embassy/blob/69006a4158aa6d605ad8506ade0f2f79159131e3/embassy-stm32/src/rng.rs). The new C29 assessment is supported:

- `RngConfig` (lines 39–59) has no NSCR field; `reset_with_config` (295–362) does not write NSCR. Generic PAC enum names do not demonstrate the product tuples above.
- `reset()` calls `RngConfig::default()` (287–291), and seed recovery calls `reset()` (364–374). Suspend reconstructs selected fields with default remainder (518–535); resume performs an RCC reset (254–264). Thus a one-time custom initialization is insufficient proof of policy preservation.
- Precision for implementation review: a call requesting defaults does not prove every requested write takes effect. RM CONFIGLOCK can ignore configuration writes until peripheral reset. Resume's actual RCC reset loses the configuration. The state machine must cover both retained-lock and reset/unlocked cases.
- Retry count 3 does not bound conditioning, `poll_word`, startup, or recovery polls (313,373,382–399). Async `fill_bytes` synchronously invokes recovery (476), so a cooperative timeout around that future is insufficient during that call.
- Async output checks zero and can leave earlier chunks populated before returning an error (445–498). Generic blocking `poll_word`/fill does not reject zero. The separate crypto driver checks zero but ultimately unwraps errors (701–724). Trait adapters can return success after an infallible/blocking operation (557–609).

These are candidate-source findings. No target/PAC build, linked nSealr path, timing result or physical fault was established. Keep the actual adapter, error/panic policy, partial-output invalidation and reset lifecycle in the proposed configuration record.

### U585 reset, clock and USB errata

I read current RM pp.483–485,492,501–504 and the USB selections listed below, plus current [ES0499 Rev 12](https://www.st.com/resource/en/errata_sheet/es0499-stm32u575xx-and-stm32u585xx-device-errata-stmicroelectronics.pdf) cover/summary and all core/system bodies pp.7–16. The new revision conditions are correct:

- §2.2.15 OTG_FS/DCMI/PSSI reset coupling applies to X; W/U are not applicable. The simultaneous-use and independent-use sequences differ.
- §2.2.22 Stop 2/LDO/RAM-power-down reset lockup applies to W; X/U are not applicable. Recovery requires the described power-on sequence; the mitigation includes all specified RAM domains, including relevant caches/peripheral RAM.
- §2.2.26 low-power entry/flash-access problem applies to X/W, not U. Other masters' flash accesses matter, even outside the CPU prefetch/latency condition.
- §2.2.27 MSI PLL false unlock applies to X/W/U and has only a partial workaround; the stated 600 µs–1 ms relock interval is supported.
- §2.2.1 PC13/LSE applies to X/W/U for LQFP/UFQFPN; external-clock bypass and WLCSP/UFBGA cases differ.

Choosing U does not remove all errata. The remaining all-revision backup-domain, privilege-lock, trigger, debug, flash programming and other selected-service constraints remain relevant. In particular, software cannot infer backup-domain protection merely from DBP, nor infer complete secret clearing from an ordinary system reset.

Current RM §72.15.1 p.3164 directly defines `GOTGCTL.CURMOD` bit 21 (0 device, 1 host). Closing that subquestion of `D-U585-USB` is correct; `GINTSTS.CMOD` also exists. The packet-count/packet-size wording and the cross-register “single write” note remain separate unresolved questions. The checked reset/flush sections impose transaction-idle, completion and synchronization preconditions; a similar driver symbol is not proof of satisfying them.

### S3 actual TinyUSB device path and RNG build option

The preserved Espressif [registry version 0.21.0~2](https://components.espressif.com/components/espressif/tinyusb/versions/0.21.0~2) identifies repository commit `894ea01409e0407a7dbe0ee29b2d58a4691f9046`. I checked the relevant native device source, both complete common files and the S3 port selections. The source chain is concrete:

- `dcd_init` lines 479–488 calls `dwc2_core_init`; common initialization reaches `reset_core` and both FIFO flush helpers.
- `handle_bus_reset` lines 771–840 flushes FIFOs at 799–800; `dcd_int_handler` lines 1233–1239 calls it while holding `usbd_spin_lock(true)`.
- Endpoint disable waits for NAK-effective and disabled status at 353,357,375,379; common reset and flush helpers also poll without a software deadline.
- The port's S3 branch declares seven endpoint slots, five concurrent IN endpoints and 256 FIFO words. The allocation formula yields 62 RX words at 64-byte maximum packet size and seven slots; EP0 IN and each additional single-buffered 64-byte IN allocation consume 16 words. This is a checked software budget, not hardware-IP qualification.
- Setting the selected DMA enable predicate to zero makes it false. That alone does not establish reset register state, actual effective configuration, selected binary or hardware access isolation.

The actual device path therefore supports C30. It does not demonstrate a physical hang or exploit. The USB interpacket timeout setting is unrelated to bounding these CPU waits. Recovery must work in the actual interrupt/critical context. The earlier wrapper's lower-bound dependency declaration remains insufficient as a resolved stack lock. Public S3 TRM §32.5's register-specification access boundary remains unresolved for any required normative semantics; ST's register description must not be substituted as normative evidence for Espressif silicon.

I also reread pinned [ESP-IDF `hw_random.c`](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/esp_hw_support/hw_random.c), lines 48–61: the bring-up branch returns `0x5A5A5A5A`. The required effective-build exclusion is accurate. The prior SAR ownership/health/fallible-adapter and S3 AES advisory constraints are unchanged; source availability does not resolve them.

### U5G9, DK2 and package evidence

Direct [UM3223 Rev 2](https://www.st.com/resource/en/user_manual/um3223-discovery-kit-with-stm32u5g9zj-mcu-stmicroelectronics.pdf) §§1–2 and 7.5–8.6 supports the new claims: DK2 uses `STM32U5G9ZJT6Q`, LQFP144, a 3.3 V MCU system and 50-pin RGB connection to MB1860, with separate backlight supply/control and I2C2 touch. Table 10 maps I2C2 to MCU pads 10/11. That mapping is distinct from connector contacts 38/40. The board's 5 V input/power selector does not make expansion I/O 5 V compatible. It is neither DK1's DSI path nor the Safe 7 custom display contract.

UM §7.6.1 identifies the 32.768 kHz LSE crystal; §8.4 maps the blue button to PC13. [ES0595 Rev 4](https://www.st.com/resource/en/errata_sheet/es0595-stm32u5fxxx-and-stm32u5gxxx-device-errata-stmicroelectronics.pdf) §2.2.1 p.5 says PC13 transitions can disturb LSE on LQFP. Ignoring button events in software does not stop electrical transitions. A proposal must avoid that physical input/clock combination or use an explicitly unaffected documented alternative. This is not evidence that the reference board is globally unusable.

I visually inspected the native DS14102 Rev 5 Figures 85/87 at printed pp.329/333 (PDF physical 330/334), and read their mechanical tables/notes at pp.330–331/334–335. The 20 mm/0.5 mm LQFP144 and 10 mm/0.8 mm UFBGA144 statements and top/bottom orientation are supported. The exact native rerenders matched. This closes outline visibility only; no electrical pad assignment, footprint, PCB manufacturability or assembly has been approved.

Current RM §2.1 pp.129–134 supports the additional G9 LTDC/GPU2D/GFXMMU/OTG_HS master paths, GPU2D M0 through DCACHE2, and LPDMA1's SRAM4 limitation. I additionally sampled native DS13086/DS14102 covers and §3.5 SRAM banking: the larger G9 RAM is real, but ECC/bank/access restrictions remain part of allocation. A framebuffer calculation is not measured available memory or a complete trusted-UI ownership argument.

## Actual review scope and what remains inherited

Fresh reading comprised all current-note material above and these exact RM selections: cover; pp.129–134,483–485,492,501–504; complete RNG functional/register text pp.1903–1919; pp.3135–3137,3141,3164,3170–3175,3238–3240,3261–3266; revision history p.3637. Surrounding host-mode text was read where it shared a selected page; it is not an adopted host-mode configuration. RM diagrams were text-extracted, not all visually inspected. Tables/diagrams with very wide text were not treated as electrical pin-layout verification.

Fresh code reading: complete Embassy RNG; complete `dwc2_common.c/.h`; `dwc2_esp32.h` lines 1–160; `dcd_dwc2.c` lines 115–410,479–570,639–666,771–840,1190–1335; registry version/commit; the fixed-pattern RNG branch. Unused DMA/isochronous algorithms and the complete USB stack were not reviewed. No target build occurred.

The earlier full blocking-claim assessment and limited follow-up remain inherited at their exact commits. I did not repeat unchanged 70-source URL retrievals merely to update timestamps. Newly native originals do not retroactively make earlier web-only excerpts original-byte evidence. The public source and reading provenance fields retain that distinction. Current H01's 30 claims, 25 pin rows and 30 errata rows are an inventory, not a coverage verdict.

## Smallest concrete remaining documentary signoff

The next bounded deliverable should be **two complete proposed host-configuration records, U585 and S3, plus the required G9 document-level comparison**, with every existing six-row host signoff matrix row resolved for the proposed use or explicitly excluded with a source-backed reason. It is not another source-count milestone, a third bench port, or an RNG/USB-only substitute for the accepted full host-relevant review.

1. **Fix the proposal identities and workload.** Resolve one U585 VI or VIQ order code/power option, one S3 module and one exact primary-documented kit/schematic revision for each. The current DS13086 ordering example explicitly supports `STM32U585VIT6Q`: V=100 pins, I=2 MB flash, T=LQFP, 6=industrial grade, Q=SMPS pinout. It does not identify a bench kit. The existing S3 lead is `ESP32-S3-WROOM-1-N8R8`; a generic DevKitC name is insufficient to establish its installed module or header conflicts. Retain exact panel/module/controller/FPC identity and physical consent wiring; controller-family placeholders do not close the UI row. A 144-pin kit must have a separate mapping to the 100-pin custom proposal. H02 later checks received marks and configuration.
2. **Complete the U585 current body contract.** Use RM chapters 2–3 (map/security), 5–7 (GTZC/RAMCFG/flash/options), 8–11 (used caches/power/reset/clocks), 13/22/23 (used GPIO/interrupts), and the selected SPI/I2C/USB/watchdog/crypto paths. Current chapter locators include GPDMA 17, LPDMA 18, IWDG 61, WWDG 62, I2C 65, SPI 68, OTG_FS 72 and SAES 50. These locators are an index for next reading, not a claim those entire chapters were read here. Tie every actually used master, pin, clock, reset and error path to current DS electrical/AF tables and the ES applicability row. Explicitly disabling a DMA/accelerator in the proposal still requires its reset/ownership proof where it affects the boundary.
3. **Close lifecycle and bounded recovery on both hosts.** Write the development/owner-secured/product-qualified transition table, including exact roots, option/eFuse/flash settings, rollback, debug/download, reset causes and surviving/erased state. Trace the selected driver/configuration and linked entropy/crypto adapters. Preserve the S3 SPI/XTS contradictions, AES advisory's long-lived-key consequence, USB normative gap, forbidden sleep conjunction, and U585 USB wording issues until resolved for the actual path. Resolve safe timeout/recovery and partial-output/consent invalidation. No hardware or fuse action is needed to write and review these conditions.
4. **Finish G9's required comparison without promoting a port.** Complete exact ZJ pad/AF/rail allocation and graphics/buffer/cache/GTZC ownership, maintained driver/license assessment and workload resource reasoning. Record whether that advantage warrants later promotion or a concrete deferral. The PC13/LSE choice must be explicit. SDK module declarations alone cannot settle this comparison.
5. **Sign each complete documentary row and carry physical gates forward.** The author and distinct reviewer should bind the proposed identities, allowed revision set, exact software/configuration tuple, manuals and exclusions. H02 then establishes received identity, build/link evidence and physical results before execution/qualification. SE API/advisory access may remain explicitly gated for H02S/H04 as the accepted brief permits; it cannot waive unrelated host/power/panel requirements.

An exact **allowed first-probe configuration cannot yet be issued** from this candidate: kit/panel/pad/clock/lifecycle and recovery fields are not complete. The following are concrete **proposals for documentary closure**, not approvals or component selections:

| Proposed record | Bounded initial conditions worth evaluating | Fields that still prevent admission |
| --- | --- | --- |
| U585 VIQ paper proposal | `STM32U585VIT6Q`, LQFP100 SMPS pinout; initially consider revision U (`REV_ID=0x3007`) to remove the X/W-only reset/low-power conditions above; one trusted development image, private SPI UI and physical inputs; exclude PC13 transitions if using LSE crystal. | Exact kit and mapping, all supply/AF limits, clock/VOS/flash-latency policy, root/debug/option transitions, remaining all-U errata, selected driver and bounded entropy/USB recovery. U is not a blanket qualification. No option-byte change is authorized here. |
| S3 comparator paper proposal | Existing `ESP32-S3-WROOM-1-N8R8` lead; explicitly named allowed silicon revision, not inferred from module name; USB FS device-only CPU-FIFO proposal, no USB host/DMA/isochronous path; private SPI UI and physical controls; fixed-pattern RNG option excluded, unused touch/ULP/LCD_CAM paths excluded. | Exact kit/module/lot/schematic, radio/SAR ownership, endpoint descriptors and effective lock/build, master/memory policy, SPI/USB normative and driver issues, lifecycle/clear policy. Revision 0.2 alone does not resolve the lot-dependent USB ROM-download fuse erratum or other all-revision limitations. |

For the S3 software budget proposal, EP0=64 and a single additional 64-byte IN endpoint would allocate 62 RX +16 EP0 IN +16 additional IN =94 of 256 FIFO words in the pinned CPU-FIFO allocator. This is merely a concrete budget to evaluate once the transport descriptor is chosen; it does not admit that transport or establish a portable U585 configuration. Leaving crypto/owner-state testing out of an initial measurement run does not remove the requirement to finish the corresponding H01 documentary lifecycle contract.

## Validation and outcome

The independent correspondence probe passed after its filename-selector correction. Whitespace and publication-scope checks accompany this report commit. The author's exact-source existing-CI log reports 43 passing tests and the earlier basename-sensitive setup failure honestly; I did not rerun those unchanged tests or interpret them as target, entropy or electrical qualification.

Limited affected-source PASS is appropriate. CM-1 is actionable wording cleanup. Full H01 acceptance, actual host admission, purchases, physical measurements, hardware damage tests, fuses, production keys, main integration and release are outside this verdict.
