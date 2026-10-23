# Static review of the S3 BOD diagnostic source

**CHANGES REQUESTED at source/configuration level: F1 below.** Reviewer
`/root/sdk_dependency_probe` is distinct from the diagnostic author. Reviewed
hardware checkpoint `2680cb7f0dc6950832f4c01ab57bfbb1bdf0a07a`, tree
`83af5731421ccf2642bdb3d8f1f6aed679b1740a`; its four project inputs remain
byte-identical to source `11047b805039e01dbb73e7c08d4b6a8016090fcd`.
This review makes no compile, link, generated-configuration, execution or
physical qualification claim.

## F1 — remove an inapplicable TEE default before build

**P2, `diagnostics/s3-bod-selector/sdkconfig.defaults:6`.** The project requests
`CONFIG_SECURE_ENABLE_TEE=n`; the independent expectations also require that
setting at `s3-bod-build-expectations.json:70`. In the exact pinned SDK,
`components/esp_tee/Kconfig.projbuild:1-5` scopes the TEE menu to
ESP32-C6/H2/C5/C61, excluding ESP32-S3. Root additionally reported an isolated
S3 configure exit 0 with this name unrecognized. That warning must remain in the
original configure evidence. A successful configure cannot count the ignored
default as applied or as security assurance.

Before build, remove the inapplicable line from this S3 project and explicitly
amend its current expectation/status to target-specific N/A. Preserve the
original frozen expectation, candidate and configure warning rather than
relabelling them. Review that limited change; do not substitute another SDK,
target or speculative security option. I did not modify the author's source
or inspect/rerun the author's configure.

## Consistent source mappings and bounded conclusions

All ten preselected vendor source hashes and eight additional relevant API/
Kconfig/build files match local ESP-IDF
`fff9895c82d744c7237be8847347bdd1b07c6643`, tree
`e6a5e4865e2027f1f0cef5da09f254d65c5cec22`. This verifies those source files,
not completion or cleanliness of the SDK Gitlink/build closure.

The top-level CMake source requires literal 0 or 1 before including the SDK
project, checks the SDK HEAD pin, and supplies the same value to the main
component. The C guard separately rejects a missing macro or numeric value outside 0/1 and
wrong target. The actual pinned CMake API supports the include → build-property
→ project pattern and `MINIMAL_BUILD`. The declared `soc` dependency exposes
the target include/register directories. These are source checks, not executed
selector/configure negatives or proof of complete header/link closure.

The register source and retained TRM1.8 agree on offset 0xE8 at 0x600080e8,
R/W selector bit 27/mask 0x08000000, RO detector bit 31 and WO counter-clear bit 29.
Bits 3:0 are reserved; there is no W1C field in this word. The separate RTC
interrupt-clear register must not be conflated with the BOD word. The source
helper at `main.c:34-40` actually calls the SDK volatile full-word `REG_WRITE`,
then a `memw` statement and volatile read; `app_main` calls it after its guards.
This is register-writing source, never a read-only probe.

The intended arithmetic changes only bit 27 relative to the captured word.
The bus write still re-emits captured enable/reset/RF/flash/wait fields,
reserved bits and the RO/WO positions. Refusal on an observed WO 1 avoids
deliberately replaying that observed 1; a WO 0 read proves no state or safety.
The capture/write gap is not atomic, no ownership lock is established, and a
readback/XOR cannot prove neutral physical effects. The source's no-arming tag
is only the README-defined software intent, not a hardware statement. The
comment about no enable operation cannot be read as an absence of writes to
the enable field within this full-word operation.

Raw reset capture reads `RTC_CNTL_RESET_STATE_REG`; its CPU cause fields are
RO bits 5:0 and 11:6. It does not clear them or label a reset domain. The retained
TRM Register6.15 maps GPIO46 to latch bit 2 and GPIO0 to bit 3, consistent with
the raw strap report and GPIO0 guard. Live GPIO46 uses GPIO_IN1 bit 14 and is
distinct from its latch. GPIO/strap/eFuse reads are not physical history,
reset-domain or safe-pin evidence. UART_PRINT_CONTROL is the actual RO two-bit
field at bits 7:6; rejecting 01/10 leaves 00/11 without choosing between the
header's GPIO8 comment and the recorded TRM GPIO46 text. No fuse write occurs.

For S3, startup calls `esp_brownout_init` conditionally on
`CONFIG_ESP_BROWNOUT_DET`. With that known option n, the call is suppressed;
this is not a call to disable ROM/hardware state. The optional ISR is under
`CONFIG_ESP_BROWNOUT_USE_INTR`, whose S3 default is n; the brownout source file
can still be included for SOC_BOD_SUPPORTED. Therefore configuration intent is
not proof of linked symbol absence. The inspected ISR clears the interrupt,
may call a callback, sets a BROWNOUT hint and ultimately invokes software reset.
The non-ISR init configures enable/reset/threshold and other controls through
HAL. Its CHIP/SYSTEM enum values are software choices, not authority resolving
the contradictory TRM reset maps. The defaults/source guards do not establish
the effective generated configuration or actual startup behavior.

## Evidence reused and remaining gates

The retained primary TRM1.8 remains 15,215,232 bytes with SHA256
`4484bf8a69035ec42a731c58c64ada6fbd1f1618c5559409f134d9ea083f444f`.
Only existing selected register text was read; no new source/component/polarity
research or native diagram review was performed. The opposing p576/p623 reset
maps remain UNSATISFIED, selected polarity null. No readback, enum, raw cause
or host inspection resolves either physical hypothesis.

I verified all 49 existing blocker-manifest bindings at `2680`, preserving both
configure REDs and the failed acquisition batch in their historical role.
Root's later configure observation is separate; I neither reran nor reviewed
that configure or its generated files. Existing Makefile/workflows/validators/
tests match the historical `85c77cc` source; its 43-test evidence is baseline
validation, not diagnostic compilation or new execution. No tests were rerun.

No build/fetch/test, hosted CI, device, flash, fuse, register execution or
energizing occurred in this review. No ELF, link map, bootloader configuration,
complete header closure, physical safety, Board/H01 or release criterion is
qualified. F1 needs a bounded source/config correction before build; all
physical, source-access and independent bench gates remain intact.
