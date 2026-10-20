# Current-manual and driver follow-up

Author `/root/h01_author`, 2026-10-18. This advances the still-incomplete H01
research after the limited review of `6f95cc2`. That review is preserved byte for
byte in `independent-review-followup/`, original commit
`2f9ea3a18d8fb18e3fbaa8f58b6272102f83b9c2`, imported by `88a8c09` before these
changes. Its PASS does not cover this new candidate or close H01. There are no
host admissions, selected components, target builds or measurements.

## Current original and actual scope

The current [RM0456](https://www.st.com/resource/en/reference_manual/rm0456-stm32u575585-armbased-32bit-mcus-stmicroelectronics.pdf)
is **Rev7, 30 March 2026, 3651 pages**. The coordinator retrieved the original
from ST with verified TLS using curl-cffi0.15.0 Chrome HTTP/2. The author
independently rehashed all 73,588,589 bytes:
`6edaaaae0c5d57c58ffc3a576d44e7b62e8d9cd0e495e8f61bab688226fc327c`.
The earlier failed routes remain historical evidence, not a current access block.
The 32 MiB download cap was too small; a bounded 128 MiB retrieval succeeded.
No authentication, manufacturer correspondence or product dependency was needed.

The author read current body text at pp.129–134 (masters/targets and start of
attribution), 483–485 (reset domains), 492 (HSI48/SHSI), 501–504 (selected kernel
clocks and clock gating), **1903–1919 (the entire RNG chapter's functional and
register text)**, 3135–3137/3141 (OTG_FS implementation/device mode), 3164
(GOTGCTL), 3170–3175 (turnaround/reset/selected interrupt registers), 3238–3240
(core/device initialization; surrounding host material is not an adopted path),
3261–3266 (device reset/endpoint/FIFO/setup), and p.3637 revision history.
Diagrams were only text-extracted here; there is no claim of all-manual or
all-drawing review. The Rev7 history names changes to security, GTZC, flash,
power, RCC, GPIO, interconnect, GPDMA, ADC4, SDMMC, TIM1/8, LPUART and OTG_HS.
That chapter list is **not** a completed Rev6-to-Rev7 content delta. Fresh current
reading replaces stale assumptions only for the stated sections.

The same working route obtained native originals of DS13086 Rev10, ES0499
Rev12, DS14102 Rev5, ES0595 Rev4, UM3223 Rev2 and **AN4230 Rev14, July2026**.
Search indexing still showed an earlier AN4230 revision. Exact bytes, text hashes,
reading and remaining work are in `manual-register.json`. Originals remain
private. A first author script used an unsupported response-context-manager API;
that local failure was preserved and corrected before the successful retrieval.

## Entropy: hardware contract and source correspondence

[AN4230 Rev14](https://www.st.com/resource/en/application_note/an4230-random-number-generation-validation-using-nist-statistical-test-suite-for-stm32-microcontrollers-stmicroelectronics.pdf)
§5.1.3 Tables3–4 separates the U585 and U5G9 configurations and their E11/E116
certificates. The reviewed U545 example is not a portable U5 configuration.
For H02 the requirement is an exact product-specific noise-source, conditioning,
health-threshold and clock policy; register constants are source evidence, not
an authorized execution recipe. Configuration A's certification statement must
not be inferred from reset values, the `NISTC` name, a `CryptoRng` trait, or a
passing output statistic. Raw-noise collection described for validation requires
special certification hardware for these parts, not an ordinary kit.

Current RM48 requires valid data-ready and no pending seed/clock error before
accepting output, plus the documented zero-word race check. Its health tests,
clock detector, auto-reset and tamper event are distinct conditions. A central
hardware reset loses configured values; conditioning reset has different scope.
A policy must restore the qualified configuration before release of output,
bound all waits/retries and invalidate a partial destination on error. Disabling
the peripheral does not itself empty every conditioned/output word. Power-mode
transitions have clock sequencing constraints. None establishes physical entropy
quality for a future board by itself.

The NIST-hosted ST [E11 public-use document](https://csrc.nist.gov/CSRC/media/projects/cryptographic-module-validation-program/documents/entropy/E11_PublicUse.docx)
v1.1 and [E116 public-use document](https://csrc.nist.gov/CSRC/media/projects/cryptographic-module-validation-program/documents/entropy/E116_PublicUse.pdf)
v1.2 were read as full extracted text, including operating conditions and
configuration. They describe bit5 as set to detect a slow clock; current
RM§48.7.1 p.1916 explicitly makes CED **active low**. Preserve this discrepancy:
the host requirement enables the clock detector according to the current RM and
AN4230, and any certification reuse claim must reconcile the public-use wording.
E116 v1.2 explicitly corrected its earlier NISTC bit12 setting. The listed
assessment conditions are not an unqualified validation of every board voltage,
temperature or clock. Their `RNG_VERR` identification statement also does not add
a register to RM48's public register map.

The complete pinned [Embassy RNG source](https://github.com/embassy-rs/embassy/blob/69006a4158aa6d605ad8506ade0f2f79159131e3/embassy-stm32/src/rng.rs)
was read. This is a candidate implementation assessment, not a built nSealr bug:

- `RngConfig` has no NSCR field; `reset_with_config` does not program NSCR.
  Its generic `Recommended`/PAC values are not demonstrated to match the
  distinct AN4230 product tuples. Exact PAC generation/features still need
  correspondence. Custom initialization alone is insufficient: `reset()` and
  `recover_seed_error()` return to defaults, and suspend/resume reconstructs
  only part of the policy.
- `MAX_RESET_RETRIES=3` bounds retries, **not polling time**. Conditioning,
  `poll_word`, and recovery wait loops have no deadline. Async `fill_bytes`
  can call blocking recovery, so merely wrapping that future in a timeout does
  not establish a time bound. Startup has the same issue.
- Async filling checks a zero data word and reports errors, but may already have
  filled earlier chunks. The generic blocking path accepts `poll_word`'s word
  without that zero check; the separate crypto driver checks zero but unwraps
  errors. Trait adapters include nominally fallible methods that always return
  success after the blocking operation. Review the **actually linked** adapter
  and error/panic policy; the trait name is not a fail-closed contract.

For the previously reviewed ESP-IDF source, explicitly require
`CONFIG_ESP_BRINGUP_BYPASS_RANDOM_SETTING` to be disabled/absent in the effective
build: that branch returns `0x5A5A5A5A`. A manifest-level preference is insufficient;
retain effective configuration and linked-path evidence. Existing SAR source
ownership/health/failure gaps remain. No source was physically faulted here.

## Reset, clocks and U585 revision constraints

Current RM§11.3 distinguishes power, system and backup-domain reset. Backup and
reset-cause state can survive other reset classes; consent/secret clearing cannot
be inferred from the word “reset.” HSI48 readiness is distinct from USB frequency
accuracy; CRS source/calibration and Stop behavior need the proposed clock policy.
RCC clock enable is followed by a two-peripheral-clock access delay. Autonomous
and retained domains do not all stop together.

The author now read ES0499 Rev12 core/system bodies pp.7–16, including all
§§2.2.1–2.2.27, with the current X/W/U summary. Additional explicit constraints:

| Condition | Applicability in ES0499 | Consequence for the proposal |
| --- | --- | --- |
| §2.2.15 OTG_FS/DCMI-PSSI reset coupling | X; W/U marked not applicable | Review combined peripheral/core reset and simultaneous users. Do not port a single reset-bit assumption to X. |
| §2.2.22 reset while Stop2/LDO and any SRAM powered down | W; X/U marked not applicable | Keep the listed SRAM domains powered in that mode or exclude the mode; ordinary watchdog/NRST/BOR reset is not a guaranteed recovery. |
| §2.2.26 low-power entry with flash reads/prefetch | X/W; U marked not applicable | Bound every active flash-reading master; the documented prefetch/latency/entry restrictions apply. |
| §2.2.27 MSI PLL false unlock | X/W/U, partial workaround | Re-lock is not instantaneous; clock-dependent service must tolerate the documented recovery interval. |
| §2.2.1 PC13/LSE interaction in LQFP/UFQFPN | X/W/U | A proposed button/expansion allocation cannot toggle PC13 while using the affected crystal path. Bypass and BGA cases differ. |

Other read system rows include X-only cache/backup-reset/retention limits,
all-revision separate-supply backup-domain reset, DBP not protecting PWR_BDCR1,
EXTI privilege locking, RTC-trigger wiring, and debug/Stop faults. These are not
all solved by choosing U. This is an allowed-configuration requirement matrix,
not a final silicon choice. Actual received identity is still H02 work.

**One earlier USB wording question is closed by the current manual:**
RM§72.15.1 p.3164 defines `GOTGCTL.CURMOD` bit21, so ES0499§2.25.5's reference is
supported. It coexists with `GINTSTS.CMOD`; a driver header was not sufficient to
infer its absence. The separate hidden-interrupt “single write” wording across
two registers remains unresolved. OTG_FS FIFO flush/reset now has read normative
preconditions and completion/synchronization requirements; this is not yet a
complete driver-to-errata correspondence or device-subset sign-off.

## S3 actual device driver, not just global helpers

The Espressif registry's **tinyusb0.21.0~2** entry identifies commit
[`894ea01409e0407a7dbe0ee29b2d58a4691f9046`](https://github.com/espressif/tinyusb/tree/894ea01409e0407a7dbe0ee29b2d58a4691f9046).
This is a pinned candidate for analysis; the earlier wrapper's lower-bound
constraint still does not establish a resolved nSealr dependency lock or compatible
build. The actual `dcd_dwc2.c` device initialization, FIFO allocation, endpoint
disable and bus-reset/IRQ paths were read, along with the complete common
implementation/header and the relevant ESP32 port header (exact ranges in the
register). Unused host and isochronous/DMA algorithms are not claimed reviewed.

`dcd_init` calls `dwc2_core_init`, which calls the actual common reset/flush
helpers. Bus-reset IRQ handling also flushes FIFOs while holding the USB spin
lock. Endpoint disable waits for NAK-effective/disabled status; these waits and
FIFO/reset completion polls have **no software deadline**. This closes the
question whether the formerly inspected global helper behavior actually appears
in a candidate device path. It does not prove a hardware hang or exploit.
Interpacket timeout calibration is a different mechanism. Recovery must have a
bounded policy that works from the actual execution/interrupt context and
invalidates outstanding consent and transport state; a task timer alone cannot
preempt an ISR-held wait.

The S3 port declares seven bidirectional endpoint slots, five concurrent IN
endpoints and 256 FIFO words. Its CPU-FIFO allocation formula reserves 62 words
for RX with 64-byte maximum packets and seven slots, plus 16 words for EP0 IN.
Each additional single-buffered 64-byte IN endpoint needs another16 words in
this source. These are software-budget calculations, not an approved descriptor
set or proof of the undocumented IP limits. `CFG_TUD_DWC2_DMA_ENABLE=0` makes the
selected DMA predicate false; proof must include the effective configuration,
reset state and linked image. The public TRM§32.5 NDA boundary still applies.
No missing master-protection specification is replaced by this source trace.

## U5G9 practical package and display consequences

UM3223 Rev2 §§1–2 and7.5–8.6, pp.2–3/14–23, are now direct author reading.
DK2's exact `STM32U5G9ZJT6Q` LQFP144 is a 3.3V RGB800×480 reference. Its
MB1860 display is connected through a **50-pin RGB connector**, with separate
backlight supply/control, I2C2 touch and reset/input signals; it is not DK1's
DSI connection or Safe7's custom DSI FPC. MCU pads10/11 for I2C2 and the wider RGB bus
already consume real resources. The expansion connectors do not make its I/Os
5V compatible. The documented HSE/LSE, reset sources, boot switch and power
selection are relevant reference constraints, not custom-board wiring approval.
UM§7.6.1 uses an LSE crystal and§8.4 puts the blue button on PC13.
ES0595§2.2.1 warns that PC13 transitions disturb LSE on LQFP. Do not inherit
that combination as a qualified input/clock design; a proposal must avoid it or
use a documented unaffected clock/package/input alternative.

Native DS14102 Rev5 outline drawings were visually inspected at printed
p.329 (physical330), Figure85, and printedp.333 (physical334), Figure87;
mechanical tables and notes at pp.330–331/334–335 were read. LQFP144 has a
20mm body and0.5mm lead pitch; UFBGA144 has a10mm body and0.8mm ball pitch.
Top/bottom orientation and pin1/A1 marks are explicit. This closes the previous
**outline-visibility** gap, not exact electrical pad/AF allocation or a footprint
review. The two rendered-image hashes are recorded privately/publicly as metadata.

RM§2.1 now directly establishes the additional G9 LTDC/GPU2D/GFXMMU/OTG_HS
master paths; GPU2D has two ports, one through DCACHE2. LPDMA1 is limited to
SRAM4, unlike the main masters. Larger RAM helps a larger review/recovery UI,
but buffer placement, GTZC attributes, cache maintenance, rail/package pad
allocation and graphics driver/license requirements still decide promotion.
No extra U5G9 bench port or automatic component preference follows from DK2.

## Exact next work

The retrieval gate is closed. Current **content review** remains open: used
security/boot/update/owner/flash/option transitions, GTZC/RAM/ECC/GPIO/DMA/PWR
and the remainder of the selected U585 USB/SPI/I2C/watchdog paths, with exact
package/electrical/AF tables and a proposed clock/driver/configuration tuple.
The Rev7 revision-history index cannot stand in for those body sections.

For S3, remaining work is the proposed kit/module electrical/schematic match,
selected GPIO/SPI transaction/error/driver path, actual dependency/build/endpoint
and error-policy closure, and boot/update/flash/clear policy. The now-traced
unbounded device waits and fixed-pattern RNG build option are explicit review
items. For G9, remaining document-level work is pad/AF/rail allocation, GTZC
and graphics/cache ownership and driver/license/workload closure. SE051 access,
TROPIC remediation and USB normative/power/panel gates remain separate.
No owned kit is required to finish these documentary proposals; no physical
result or H01 completion is claimed by this advance.
