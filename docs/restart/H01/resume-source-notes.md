# H01 resumed source review — 20 October 2026

Author `/root/h01_resume`, continuing the explicit maintainer resumption from
`40cdb6c519285ab81922b382440ef6c02a6fc89a`. These are selected documentary
findings. H01 remains incomplete; no host, wiring, component or physical probe
is admitted. The historical pause records and exact earlier reviews remain
unchanged. The old `result.json` and `handoff.md` do not bind this increment.

## Source-bound requirements

The following table is suitable as an input to the Board SDK contract only
with its applicability and limits intact. It does not establish a generic
service's implemented behavior.

| Claim | Exact primary source | Requirement and limit |
| --- | --- | --- |
| H01-C36 — cache access and cleanup | RM0456 Rev7 §§8.4.9–8.7.7, pp374–380; §§9.3–9.7.10, pp383–399 | U585 DCACHE1 only caches the external-memory region `0x60000000–0xAFFFFFFF`; internal SRAM and peripheral accesses bypass it. Keep DCACHE1 disabled in the internal-memory-only proposal. ICACHE remapping has separate region enables; all four remain disabled for the proposal. Invalidation clears validity, not an established data-erasure operation. Source errors and completion flags need explicit handling; a poll without a deadline is insufficient. |
| H01-C37 — G9 graphics security | RM0456 Rev7 §9.3 p383, contrasted with general §9.4.7 p390 | G9 GPU2D traffic is nonsecure and DCACHE2 does not support TrustZone. A future GPU framebuffer must be deliberately nonsecure and must not overlap the secure secret arena. The generic cache TrustZone statement does not override this implementation exception. This constrains the mandatory comparison; it neither admits nor globally rejects a G9 design. |
| H01-C38 — GPIO ownership and reads | RM0456 Rev7 §§13.3.1–13.3.19, pp624–631; §§13.4.1–13.4.13, pp633–641 | With TZEN, GPIOs reset secure but a nonsecure read can return zero without an illegal-access event. Analog mode also returns zero. An active-low consent input therefore needs validated mode, access context and configuration before its value is interpreted. GPIO lock protects listed configuration, not output data, and is removed by peripheral/system reset. Additional-function owners still require the separate system-security manifest. |
| H01-C39 — 3.3 V I/O constraint | RM0456 Rev7 §13.3.20 pp631–632 and §13.4.12 p640 | Leave HSLV disabled for the proposed 3.3 V rails. Enabling it above 2.7 V may damage the device; the manual provides no hardware protection. HSLV with Fm+ is also forbidden. This is a prohibited configuration, never a proposed destructive negative test. |
| H01-C40 — independent recovery | RM0456 Rev7 §§61.3–61.7.6, pp2562–2574 | Once started, IWDG continues independently of the main clock until its reset, subject to the documented low-power/debug/option controls. Writes to the early-wake register reload the counter; repeatedly acknowledging EWI is not a reliable route to a later reset. The initial proposal leaves EWI disabled and uses a single feed owner that requires actual forward progress. LSI tolerance, startup, debug-freeze setting and reset/secret-clear behavior still need the complete configuration and H02 evidence. |
| H01-C41 — kit startup branches | MB1551-U585AI-D01 native sheets4,7,8,13,14; UM2839 Rev4 §§7.6–7.9, pp22–29 | The proposed PA7/PB0 inputs use fitted SB10/SB13; alternate I2C1 bridges SB11/SB12 are marked DNF. STMod selector pull-ups R10/R11 are DNF even though the tables label UART as default. Wi-Fi CHIP_EN has no drawn external pull-down. Do not infer reset isolation, radio inactivity, or a defined mux state from an unused driver. These findings remain kit-specific. |

All RM rows resolve to [the registered original](https://www.st.com/resource/en/reference_manual/rm0456-stm32u575585-armbased-32bit-mcus-stmicroelectronics.pdf),
SHA256 `6edaaaae0c5d57c58ffc3a576d44e7b62e8d9cd0e495e8f61bab688226fc327c`.
The kit drawing resolves to [MB1551 D01](https://www.st.com/resource/en/schematic_pack/mb1551-u585ai-d01-schematic.pdf),
SHA256 `040d70dc5da0e6ef0d0e5cfe33abfbffdfe4b01cbb9d5348ec20679752ebe221`.
The kit manual resolves to [UM2839 Rev4](https://www.st.com/resource/en/user_manual/um2839-discovery-kit-for-iot-node-with-stm32u5-series-stmicroelectronics.pdf),
SHA256 `00b3650d881649661574b3889062545cb4e74450ef15991c68b2e74fffe8ddf3`.
These hashes identify originals; they are not proof of complete manual reading.

## Cache and input consequences

The U585 proposal uses internal secret and transfer arenas, CPU-driven SPI, and
no external memory. DCACHE1 can therefore remain disabled without pretending
that it secures or clears internal SRAM. The ICACHE configuration needs both
`EN` policy and all four `CRRx.REN` values. Its reset status starts busy while
hardware invalidates the tags; startup must await actual completion with a
bounded failure path before relying on cache state.

For a future configuration that enables DCACHE, a full invalidate or disabling
the cache must not discard dirty data that is still required. Range cleaning
requires exclusion of other writers until command completion. Write-back errors
may appear as the cache's own error flag rather than at the original writer;
error handling belongs to the service boundary. The current internal-memory-only
U585 proposal does not exercise that excluded external-memory path.

There is a source inconsistency: §9.4.3 p385 lists `CACHEINV=0` among ways to
invalidate, while §9.4.8 p390 and §9.7.1 p395 specify writing one and explicitly
say zero has no effect. Preserve this discrepancy. The proposed disabled
DCACHE configuration does not use the conflicting command; any future enabled
driver must follow the explicit command/register contract and retain the
manufacturer clarification as an open item.

Before accepting an input, startup must establish its input mode, rail, pull,
security attribution and intended reader context. Observing a zero bit is
insufficient. The existing requirement for a debounced release followed by a
new press still applies after reset, timeout, transport cancellation or display
failure. The GPIO lock sequence is a configuration guard; it does not establish
isolation from malicious code executing in the same trusted privilege/security
state.

## Kit conditions established by the drawings

Sheet4 shows target BOOT0 on PH3 through R35 and SW1, with its default switch
position grounding the path. PA7/PB0 are distinct target pins. Sheet8 exposes
them only through the proposed Arduino A4/A5 bridge paths; the alternate I2C1
paths must remain open. This is native schematic evidence, not received-board
continuity or a completed ROM-loader pin review.

Sheet7 routes PE13/PE15 to the STMod analog switch as well as the Arduino path.
PH13 selects its SPI/UART branch. Because R11 is DNF, the printed UART-default
label is not proof of an externally biased reset state. Leave CN2/CN3/CN4 empty,
set the selection deliberately before SPI traffic, and account for the connected
switch and the sheet8 Q3/R48 LED branch in the electrical/timing budget. The
switch's own electrical data and the complete target net correspondence remain
open.

Sheet13 powers the Wi-Fi module directly from 3V3 and connects target PF15 to
CHIP_EN. The drawing does not show an external hold-low on that net; target
GPIO reset is analog. No claim of radio inactivity from power-on is supported
by these two sources. The Bluetooth module has a separate SW3 power selection
between system 3V3 and its CN12-fed regulator. Selecting an unpowered CN12
branch does not prove absence of injection through attached UART/debug lines.
Its reset button is a separate BT reset, not an established target-controlled
reset. Source-backed shutdown and powered-off I/O behavior remain required.

Sheet14 shows JP4 selecting the board's 5 V source and JP3 between 3V3 and
VDD_MCU. Measuring JP3 alone excludes other board loads. The camera regulator,
power indicator and radio supplies are real loads on the board supply. The
annotated regulator capacity and the USB-port current permission are separate
quantities. No complete kit suspend or display-current budget follows from
these drawings.

## Actual reading and outstanding work

Fresh current-RM extracted-text reading: pp374–380 before the register-map
summary; pp382–399 before the register-map summary; pp622–641 before the
register-map summary; pp2562–2574. Functional and register body text was read,
including encountered table text. Diagrams were text-extracted, not newly
visually reviewed. The prior pp540–547 RCC reset-register reading was reread
for the excluded-master manifest; reset fields default to zero, so an
all-zero register snapshot does not prove software is holding a block reset.
Absent-device fields remain reserved, not a blanket all-ones reset mask.

Fresh UM2839 extracted-text reading: pp21–29. Fresh native schematic visual
review: sheets4,7,13,14; sheet8 rechecked. Manufacturer drawings and extracts
remain private; render hashes and exact page scope are in the register.

The proposed configurations still require the remaining clock/power/GTZC,
SPI/I2C/USB/interrupt/driver and reset-manifest correspondence, exact panel and
fixture electrical closure, both lifecycle/update/entropy configurations, and
the remaining G9 package/rail/driver comparison. The six documentary signoff
rows therefore remain incomplete. This increment does not convert the S3 NDA
USB boundary, display source contradictions, physical-resource gaps or
selected-SE gates into accepted compromises.

## Subsequent finite pin/electrical and product-priority checkpoint

[pin-electrical-contract.md](pin-electrical-contract.md) and its
[proposal](pin-electrical-proposal.json) record C01's exact two-kit pad/header/AF
and normal external fixture requirements. Claims H01-C91–C94 carry exact source
scope, assumptions and negative cases. Original MXCHIP DS0122CN v2.8, STG3692
DS4909 Rev9 and the exact raw DB product page remain private, with metadata and
hashes public. Existing native sheets7/8/9/13 and S3 pages1/2 are reread, not a
new whole-CAD/assembly audit.

Two corrections are explicit. Installed EMW3080(BP) CHIP_EN has internal nominal
100 kΩ pull-up/10 nF, so the whole-net floating inference is withdrawn; no external
hold-low and no POR radio-quiet proof remain. A private draft also confused
PB14 **DBCC2 control** with the physical CC2 net: kit CC2 is **PB15**, CC1 PA15.
The draft's PB4 alert is likewise withdrawn: native sheet9 gives **PE8 FLGn and
PD13 IANA**. DS p134 note4 and actual PWR_UCPDR ownership resolve the distinction;
no false physical conflict or defective-board claim follows. PB11/PH4/PH5 are
still absent from the LQFP100 SMPS witness, which is not a completed custom BOM.

The maintainer's 20 October priorities make the no-touch baseline comparative.
Existing option-comparison.md now covers generic Board/SDK use, three bounded
non-Nostr workloads, concrete UI bandwidth/memory limits, a physical-confirmation
decision and unselected two-SE composition hypotheses. No chip/panel is selected,
no new market sweep or task tracker is opened, and S04/manufacturing/owner/physical
gates are unchanged. C03/C04/C09 and the final G9/six-row packet remain incomplete;
there is no hardware result or completed H01 acceptance at this checkpoint.


## Subsequent finite C03/C04 system and owner checkpoint

The [system table](system-runtime-contract.md) records active supply/watchdog/IRQ
and finite startup guards; the S3 brownout selector contradiction remains an
unsatisfied source property, and RC-slow min/max/clock-loss timing is unproved.
The [owner/update table](owner-update-contract.md) records exact protections,
root/floor authority and interrupted-update stops for both paper hosts. Newly
registered counter helpers distinguish unbounded/error-losing stock behavior
from required bounded checked commitment; no helper/fuse/flash call executed.
These are documentary proposals, not a persistent vault, qualified transport,
boot chain, clock, entropy provider, protected device or completed H01 row.
C09 and final G9/six-row integration/review remain.
