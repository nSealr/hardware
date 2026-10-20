# H01 affected independent source review

Reviewer: `/root/h01_substance_review`, 2026-10-18, in its own isolated
`review/h01-followup` worktree. Exact reviewed candidate:
**`6f95cc298c5a8108d5c0bdaedfd53e7b81b130ed`**. Substantive source:
**`6b45f6f79e1888bdf2ec6680d14dd951b7019327`**. Separate material correction:
**`16a7d4bfaa9b144581ae06fb67424718ffb10482`**.

**PASS for the material corrections and the bounded research statements checked
below. H01 remains INCOMPLETE.** This is neither a whole-task pass nor admission
of a host, part, wiring plan, driver or probe. No new blocking documentation
error was found in the affected scope. The original request-changes review
`5186b7207fa397ceb4cd237d710d8adc163c6eb0`, preserved by `f713951`, remains
unchanged evidence about the old `d5d7530` / `19362fc` candidate.

The approved brief and input are unchanged. The candidate still has zero host
admissions and zero selected components; that does not satisfy acceptances 1 or
5. Current RM0456 Rev7, required host subsets, selected-SE access/remediation,
USB normative/electrical and exact panel/power/expansion gates remain open.

## Required corrections rechecked

| Original request | Independent check | Disposition |
| --- | --- | --- |
| R1: ANALOG-160 mitigation inversion | Re-read S3 errata v1.3 §3.3, printed p.7, from the retained original. The ledger now places `BIAS_SLEEP=0 AND PD_CUR=1` in the damaging condition and explicitly prevents it. v0.0/v0.1/v0.2 and the documented IDF workaround are retained. | **Closed for documentation.** No damaging physical test is permitted. |
| R2: TOUCH-100 abbreviated workaround | Re-read §3.7, printed p.10. The ledger now names `TOUCH_SCAN_DONE_INT`, skips its first two interrupts, and then disables/stops their use. It does not qualify touch operation. | **Closed for documentation.** |
| R3: proposed versus received identity | Read the changed coverage matrix, admission plan, response and handoff. H01 requires the proposed exact OPN/package, allowed revision/configuration and documentary sign-off. H02 matches the received unit and binary before execution. | **Closed for wording.** No already-owned kit prerequisite or vacuous zero-host pass remains. |

The S3 erratum original's SHA256 is
`8f349bdd0b4e9bca24e49d777ac3b416ff2d2c48253a49653162e84f4b484500`.
[Manufacturer errata](https://documentation.espressif.com/esp-chip-errata/en/latest/esp32s3/esp-chip-errata-en-master-esp32s3.pdf).

The pinned IDF sleep source adds useful, limited correspondence: the reviewed
default branches pair bias/current settings consistently, and the two assertions
reject the forbidden conjunction before applying the bias fields. Assertions
disabled at build time and custom callers remain outside that assurance. The
v6.1 tag independently resolves to the stated commit
`fff9895c82d744c7237be8847347bdd1b07c6643`.
[Sleep source](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/esp_hw_support/port/esp32s3/rtc_sleep.c#L159),
[paired defaults](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/esp_hw_support/port/esp32s3/include/soc/rtc.h#L123).

## New material statements checked

**S3 GPIO, SPI, watchdog and XTS:** TRM v1.8 supports the function-4
GPIO10–13 witness, the distinct reset-input defaults for GPIO4–7, hold/output
enable constraints and the stated interrupt/light-sleep distinction. These
facts do not allocate panel controls or establish debounce/consent behavior.
Chapter13 supports C25's clock/reset-domain distinction and the limits of
automatic feeding and accidental-write protection. Chapter23 supports C26's
separation of key material, encryption enable and plaintext-register cleanup.
The manual destroys the encrypted result; that wording does not prove wiping
the separate readable plaintext bank.

The new SPI contradiction is real: Tables30.5-9/10 footnotes reverse the
one-bit order given by Table30.5-5 and register30.6. The new XTS contradiction
is also real: p.913's enable prose differs from the odd/even population-count
definition at p.433. The candidate correctly preserves both without producing
a register/fuse recipe or claiming an implementation is qualified.
[TRM v1.8](https://documentation.espressif.com/esp32-s3_technical_reference_manual_en.pdf).

**S3 USB and selected vendor source:** the candidate correctly identifies
§32.5 p.1242 as the comprehensive-register NDA boundary. **This corrects the
§32.4 next-reading locator in my original report**, which stays preserved;
§32.4 describes OTG/HNP/SRP. Public functional text and headers remain useful
without replacing missing normative semantics. The IN/OUT structure names
support the recorded direction distinction, but do not resolve every hardware
side effect or establish DMA isolation.

The checked esp-usb manifest fixes its own revision while leaving the underlying
TinyUSB dependency lower-bounded. Its configuration enables slave support and
conditionally DMA with priority; its installation path selects internal
full-speed device PHY for the reviewed S3 branch unless setup is skipped.
Self-powered VBUS handling is separate. No actual nSealr binary is established.
The low-level IDF file contains global/host helpers, not the selected device
controller driver. C11/C27 and the open exact-dependency/configuration gates are
therefore appropriately limited.
[Pinned manifest](https://github.com/espressif/esp-usb/blob/fc9bead300f82484eace377d5dea2f3e11163206/device/esp_tinyusb/idf_component.yml),
[configuration](https://github.com/espressif/esp-usb/blob/fc9bead300f82484eace377d5dea2f3e11163206/device/esp_tinyusb/include/tusb_config.h#L92).

**U585:** ES0499 Rev12's applicability tables and selected bodies support the
SPI/USB/IWDG rows and the **X-only** UCPD Rd limit. W/U do not inherit that Rd
erratum. The USB packet-count/size comparison, two-register “single write” note
and mode-status naming are present in the manufacturer text; the candidate
correctly withholds a literal write procedure. The watchdog interrupt and reset
effects differ; backup-domain reset affects its clock and security attribution.
Selected ECC, flash recovery and SAES-ordering text also supports the bounded
notes. Current RM and driver correspondence remain necessary.
[ES0499 Rev12](https://www.st.com/resource/en/errata_sheet/es0499-stm32u575xx-and-stm32u585xx-device-errata-stmicroelectronics.pdf).

**U5G9 and DK2:** current primary extraction is DS14102 Rev5; the stale Rev4
search excerpt was not used as current evidence. The bank/ECC distinction,
package-dependent rails, supply sequencing, GPU2D's two AHB masters and the
DMA2D/LTDC master paths support the new bounded triage. Ordering text separates
Z/144, J/UFBGA, T/LQFP and Q pinout; it does not itself guarantee commercial
availability. The 27-May-2026 history records the package repair. No original
hash or visual package-drawing review was invented.
[DS14102 Rev5](https://www.st.com/resource/en/datasheet/stm32u5g9nj.pdf).

ES0595 Rev4 supports the specific RevZ DSI restrictions and ascending SAES
backup-key reads; it does not show a universal graphics/SAES failure.
The official DK2 feature page independently confirms ZJT6Q/LQFP144, 3.3 V and
800×480 parallel RGB. Its presence adds no port or design selection. The
750/1500 KiB RGB565 buffer arithmetic is correct. UM3223 cover/§§1–2 remains
my prior reading; no fresh full power/jumper/connector/schematic review occurred.
[ES0595 Rev4](https://www.st.com/resource/en/errata_sheet/es0595-stm32u5fxxx-and-stm32u5gxxx-device-errata-stmicroelectronics.pdf),
[DK2 primary feature page](https://estore.st.com/en/stm32u5g9j-dk2-cpn.html).

**Power and other affected entries:** TPS63802 §§9.3.3–9.3.10 support the new
startup/reverse-energy/PG discussion. Reverse energy can raise VIN before
protection intervenes; PG alone cannot certify board isolation. The two power
investigations and USB entitlement gate remain. The revised P4 ECDSA revision
lists match errata v1.4 §§3.12–3.13. Safe7's filename/sheet distinction preserves
the prior observation without a new whole-product review.
[TPS63802](https://www.ti.com/lit/ds/symlink/tps63802.pdf),
[P4 errata](https://documentation.espressif.com/esp-chip-errata/en/latest/esp32p4/esp-chip-errata-en-master-esp32p4.pdf).

## Actionable follow-ups before admission

These extend already-open implementation/subset gates; they are not new reasons
to reject the accurately incomplete research record.

- **Entropy configuration:** the reviewed `hw_random.c` has a bringup-bypass
  branch returning a fixed pattern. An eventual build/adaptor record must
  explicitly exclude `CONFIG_ESP_BRINGUP_BYPASS_RANDOM_SETTING`, as well as
  enforce source ownership and fallibility. The boot-source comment about its
  secondary clock does not replace the RNG contract. The candidate correctly
  makes no qualified entropy claim.
  [Pinned implementation](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/esp_hw_support/hw_random.c#L48).
- **USB completion/error paths:** the inspected global low-level reset/flush
  helpers contain polling loops without their own timeout. Trace the actual
  locked device implementation and its recovery policy; do not assume those
  host/global helpers are used or that a wrapper's successful installation
  proves bounded recovery. Keep the §32.5 questions narrowly tied to the chosen
  mode and its required semantics.
- **U585 system/reset subset:** keep ES0499 §2.2.15's RevX USB/reset coupling
  and §§2.2.22/2.2.26's distinct W versus X/W low-power applicability in the
  next exact allowed-revision matrix. These are concrete available readings
  within the existing system/clock/retention gate, not whole-family rejection.
  The new SPI/USB rows still need exact selected-driver correspondence.
- **U5G9/package and USB power:** complete exact pad/AF/rail and graphics
  ownership/workload mapping, lawful current-RM acquisition and the relevant
  DK2 electrical subset. Continue the USB normative/current/startup/backfeed
  work independently. No repeated failed RM route or newly owned kit is needed
  to make progress on the other available sources.

## Binding, coverage and limits

[The read-only probe](probes/check_bindings.py) passed. It independently matched
the coordinator's result/handoff hashes, **21** source artifacts against both
source and candidate commits, **2** verification artifacts, **9** new source
originals, **4** affected previously retained originals, and all **7** preserved
old-review files. The original-identity fields of the prior **70** source records
remain unchanged. Three fresh PDF text extractions match the preserved text.
These are correspondence checks, separate from the source reading above.
[Binding log](logs/bindings.json).

[review.json](review.json) records exact reading scopes and source hashes.
Web-only ST reads retain null original hashes. The unused portions of manuals,
dependencies, drivers and physical drawings were not independently signed off.
The old blocking claims C01/C16/C19 and their source identities remain unchanged;
their prior substantive review is inherited and their gates are still open.
No new attempt to acquire RM0456 Rev7, restricted SE bodies or a TROPIC remedy
was made during this affected review.

The preserved fresh `make ci` log reports **43 existing repository tests** at
`6b45f6f`; this reviewer did not rerun them. The earlier basename setup failure
remains recorded. Neither run establishes manual correctness or hardware
qualification. This branch adds only review evidence; no source, graph, CAD,
target build, physical operation, purchase, inquiry, secret or provisioning
action occurred. The coordinator may record the material fixes as reviewed
while keeping H01 running/incomplete.
