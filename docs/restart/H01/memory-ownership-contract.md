# Two-host memory and ownership contract

This finite C05 table proposes one bounded internal-memory layout per retained
host. Addresses and source constraints are distinguished from engineering
capacity limits. No linker, target build, peak measurement, clearing test or
physical isolation has passed. The layouts are requirements for H02 to implement
and reject if they do not fit, not measured product capacities. The
[machine-readable allocation](memory-ownership-proposal.json) gives exclusive
upper addresses and exact arithmetic.

The first image is trusted in its entirety. U585 uses one secure privileged
image with TZEN; S3 uses CPU0/World0 with CPU1 held reset and clock-gated.
Neither layout protects a key against arbitrary execution in that image. No
nonsecure application, World1 application, DMA, hostile-app sandbox, new crypto
backend or external secret RAM is introduced.

## Fixed workload and copy limits

P01 PROD-09 requires finite profile limits before expensive work, while leaving
their measured acceptance to T01/K01 and target qualification. These H01 values
are proposed **qualification caps**, not protocol maxima, current T01 values or
a promise that all inputs below them are renderable. The original pinned P01
contract and S02 secret-flow/backend remain authoritative. Reject an operation
that cannot be parsed, completely reviewed and completed within all its limits;
do not truncate fields or add allocation to admit it.

| Resource | Proposed cap and owner |
| --- | --- |
| Incoming frame | 16,384 bytes including framing; one transport-owned accumulation buffer. Validate advertised length before accepting its body; no unbounded spill or second queued frame. |
| Public result | 16,384 bytes including framing; one result buffer. Only P01-authorized outputs enter it after local authority. A response buffer is not an export route for recovery material or intermediate secrets. |
| Parser/review state | 16,384 bytes cumulative public retained state, including offsets, metadata and copied public strings. Prefer bounded borrowed views; every copy counts. Secret plaintext/review copies count against the secret arena instead. |
| Queue/authority | One pending operation and one active review, with no backlog of approvals/results. Transport epoch, exact operation/identity and review state bind consent; cancellation, reset, timeout, source error or owner change invalidates all three. |
| USB storage | 4,096 bytes total software endpoint/CDC staging, control state and bounded rings. Peripheral FIFO capacity is separate hardware storage, never extra application capacity. C06/C07 fix the exact packet/service/descriptor contract. |
| Rendering | One public 512-byte slot and one **separate secret** 512-byte slot, each with 480 active RGB565 bytes for one 240-pixel row. Padding is not another row. No 153,600-byte full framebuffer, hidden render queue or DMA copy. Recovery/backup rows stay secret and local; transport staging cannot alias them. |
| Secret data | 65,536 bytes total: input/plaintext16,384; output/plaintext16,384; key/source8,192; encoded local recovery8,192; session/entropy4,096; private row512; owned operation scratch11,776. These are aggregate caps, including duplicate encodings, pending ownership and error paths. An unused partition is not permission to grow another. |
| Stack/backend | Separate 65,536 bytes: application stack32,768; exception/ISR stack8,192; owned backend workspace24,576. SDK/background task stacks fit the separate runtime partition and cannot receive secret call frames. Compiler spills, FFI/libc/TLS, k256 temporaries and panic/unwind paths must be inventoried; the allocation does not establish their erasure. |
| Entropy | The [C08 contract](entropy-contract-review.md) reserves the caller's complete32-byte destination within secret storage; proposed fill100 ms, scalar at most8 draws/200 ms total. No entropy-dependent use before its explicit provider qualification stops close. |

The 64 KiB public partition allocates request16,384 + result16,384 + review16,384
+ USB4,096 + normal row512 + control metadata4,096, leaving7,680 bytes explicitly
unallocated. The secret and stack partitions each total exactly64 KiB. No
implicit heap may borrow these partitions. Overflow, stack exhaustion, an
unqualified operation size or an unaccounted copy refuses the operation and
clears owned secret/pending state; it cannot become a smaller blind review.

## U585 allocation and initialization

RM0456 Rev7 Figure4 p142 and §2.3.3 distinguish C-bus/system-bus aliases;
Table33 p199 and the already read SRAM/RAMCFG body determine implemented size,
ECC and lock granularity. Use only the secure system-bus aliases below for
application data. Other aliases denote the same storage, not extra capacity.

| Secure address interval, upper end excluded | Size | Proposed owner |
| --- | --- | --- |
| 0x30000000–0x30010000, SRAM1 | 64 KiB | Secret application/exception stacks and backend workspace. SRAM1 is not claimed to provide SRAM2's ECC protection. |
| 0x30010000–0x30020000, SRAM1 | 64 KiB | Public request/result/review/USB/normal-row partition. “Public” means host-known data, not nonsecure attribution. |
| 0x30020000–0x30030000, SRAM1 | 64 KiB | Runtime, bounded allocator and any required RAM-resident code, with no secret call frames or secret allocation. |
| 0x30030000–0x30040000, SRAM2 | 64 KiB | Secret data partition, with selected ECC/startup initialization and error handling. |

SRAM3, SRAM4 and backup SRAM are outside this initial allocation. Their actual
presence, ECC storage loss, security and clearing obligations do not disappear.
Do not count ECC storage as free RAM or retain secrets in RTC/backup/TAMP.
Flash code/constant and persistent-record allocations belong to C04; no plaintext
key or recovery copy may be placed there accidentally by a section attribute.

The existing [U585 initialization manifest](u585-initialization.md) and
[peripheral correspondence](u585-peripheral-manifest.json) remain the exact
device-specific authority: all implemented SRAM secure/privileged; both MPCBB
superblock locks and control GLOCK; secure/privileged implemented TZSC fields
then LCK; reserved fields preserved. CPU SAU/MPU attributes alone do not constrain
other masters. GPDMA1, LPDMA1, DMA2D, SDMMC1/2, OCTOSPI1/2, FSMC and unused
accelerators remain held reset and clock-gated. SPI/I2C/OTG use CPU service;
there is no selected DMA channel. ICACHE has no remap, DCACHE1 stays disabled,
and internal SRAM bypasses DCACHE1 regardless. Cache invalidation is not erasure.

Startup establishes these exclusions, attribution, clear/ECC/fault policy and
finite clocks/time/watchdog **before** USB attachment or local request intake.
MPCBB/TZSC locks last until system reset; after reset repeat initialization and
invalidate old authority. `SRAM2_RST=0`/`SRAM_RST=0` request documented system-reset
erasure, not universal clearing of backup/debug/cache/register state. Startup
still clears/checks the owned ranges before reuse and handles ECC incidents.

Pinned Embassy69006a4's global `init_hw` calls SYSCFG/PWR/FLASH reset/enable,
GPIO initialization, `dma::init`, RCC initialization and feature-dependent
EXTI/time/RTC initialization inside a critical section. The callsite is not a
held-reset/master-exclusion proof; not every callee or effective cfg is reviewed.
The proposed bounded startup must suppress incompatible automatic initialization
or reestablish and verify this manifest before intake, without an unbounded
critical section or blind late reset of live controls. Existing polling SPI/I2C/
OTG/RNG gaps still need their scoped remedies. No stock global initializer is
accepted as conformant merely because the application never requests DMA.

## S3 allocation, aliases and locks

TRM1.8 pp400–407 distinguishes SRAM0/1/2 and aliases. With the proposed32 KiB
instruction cache and64 KiB data cache, SRAM0/2 are cache storage, not additional
CPU arenas. SRAM1 data0x3fc88000–0x3fcf0000 aliases
instruction0x40378000–0x403e0000 with offset0x006f0000, in the same order.
The pinned IDF linker instead ends its initial static window at0x3fcdb700 /
0x403cb700 to respect bootloader/startup reservations. A total512 KiB label or
`_heap_end=0x40000000` does not prove available application RAM.
Its introductory0x403b9000 startup comment differs from the active end constant.
The directly referenced, same-pin bootloader memory linker explicitly permits
application static storage up to its loader start and asserts that start equals
0x403cb700. This resolves the selected linker-bound correspondence, not actual
fit. ROM download shared buffers start at0x3fcd7e00 and may overlap the runtime
partition only in their separately reset download state; no live application
may invoke a ROM downloader or preserve authority through that transition.

| SRAM1 data interval, upper end excluded | Size | Proposed owner |
| --- | --- | --- |
| 0x3fc88000–0x3fc98000 | 64 KiB | Reserved IRAM code/vector interval, instruction alias0x40378000–0x40388000. Not also data/heap. |
| 0x3fc98000–0x3fca8000 | 64 KiB | Public partition described above. |
| 0x3fca8000–0x3fcb8000 | 64 KiB | Secret data partition. |
| 0x3fcb8000–0x3fcc8000 | 64 KiB | Secret application/exception stacks and backend workspace. |
| 0x3fcc8000–0x3fcd8000 | 64 KiB | SDK/runtime and its bounded allocator/task stacks, with no secret call frames. |
| 0x3fcd8000–0x3fcdb700 | 14,080 bytes | Unallocated static margin; not evidence of a measured free heap. |

Use one fixed CPU0 owner. CPU1 has `SYSTEM_CONTROL_CORE_1_RESETING=1`,
`CLKGATE_EN=0`, with no second-core startup/task/ISR writer. RUNSTALL alone only
waits for an ongoing task to finish and is not the reset/exclusion policy.
The app remains World0; there is no World1 entry or world-switching feature.
CPU permissions are shared for internal SRAM, so this does not create per-core
secret isolation.

The proposed PMS main instruction/data split is data0x3fc98000; both unused
internal instruction splits coincide there. Data splits are0x3fca8000 and
0x3fcc8000. All are256-byte aligned and mapped through the documented per-block
category/address fields, not a guessed linear address write. World0 instruction
regions permit read/execute, not write; its instruction-bus access to data is
denied. World0 data regions permit read/write; data-bus access to instruction
storage is denied. All World1 internal SRAM/ROM permissions are denied; World0
ROM remains read/execute through IBUS and read-only through DBUS. Cache blocks
are not admitted as CPU application storage. This is code/data permission
separation; the three World0 data regions are not mutually secret compartments.

Before locking, read back internal SRAM/cache usage, all five split lines and
both World0/1 permission sets against the effective linker map. Then set the
named usage, split, IRAM and DRAM configuration locks. TRM15.8 says these locks
last until the next CPU reset; do not assume they survive every reset or cover
all RTC/peripheral state. Do not blindly derive writes from the error-prone
summary table. Per-register bodies give a distinct I2S1 permission lock, despite
the table's I2S0 label in that row. Permission-denied internal reads can return0,
external reads0xdeadbeaf, and writes fail; an enabled monitor logs only the first
incident. A read value or lack of a CPU exception is not a successful check.

All six internal SRAM DMA permission fields (instruction/data0–2/cache-block9/10)
are denied for each of the documented SPI2, SPI3, UHCI0, I2S0, I2S1, AES, SHA,
ADC_DAC, RMT, LCD_CAM, USB and SDIO requesters, then each named permission lock
is set. The ADC_DAC DMA denial does not disable the C08 CPU-controlled SAR
entropy route; its exclusive source lease remains separately unqualified.
GDMA and external-memory DMA stay reset/clock-gated. No application PSRAM,
PSRAM BSS/noinit/stack, RTC-retained secret, trace allocation or external secret
cache line is allowed. The N8R8 module's physically present PSRAM is not claimed
removed. Flash caches/SPI0/1 and mandatory boot/security hardware may operate;
they are not application DMA or selected accelerated-crypto backends.

SYSTEM17.3.5/17.4 gives separate reset/clock controls: unused OTG USB, SPI3,
UHCI/I2S, LCD_CAM, SDIO_HOST, RMT and application crypto engines stay reset and
gated; GDMA uses `SYSTEM_DMA_RST`/`DMA_CLK_EN`, external DMA uses its separate
EDMA controls. SPI2 CPU FIFO, fixed-USJ candidate, SYSTIMER and the SAR source
are distinct conditional owners under C03/C07/C08. Never reset/gate SPI0/1 or
the live cache to imitate exclusion. UART/console/log/panic output and the
effective task/IRQ/feature set remain subject to C04/C07; no secret trace,
core dump, panic dump or diagnostic writer is allowed.

The pinned `memory.ld.in` and `sections.ld.in` explicitly skip IRAM's data alias,
account for prefetch padding, assert segment fit, and contain separate noinit,
RTC and optional external-BSS/noinit sections. Their defaults do **not** create
the fixed partitions above. H02 must generate/check the effective linker script
and map, preserve alias/prefetch/ROM reservations, constrain every allocator and
task/ISR stack, and fail link/intake on overlap or excess. A successful default
link would not prove this contract.

## Finite admission evidence

H02 checks the exact binary/map and effective compiler/features/link order/LTO;
enumerates every master, core, allocator, stack, ISR and source writer; and
measures the maximum supported complete workload and failure paths within these
partitions. It must show boundary success and refusal at +1 byte/queued request,
no hidden suffix, no recovery row/secret sent to USB, no external/retained secret
placement, and correct cancellation and owned-range clearing on faults/reset.
It also verifies configured locks and exclusions on the actual silicon without
using denied zero reads as proof. Injected faults, cache invalidation, reset and
Rust zeroizing owners do not establish complete physical remanence erasure.

Source identities/read scopes are in [manual-register.json](manual-register.json):
[RM0456](https://www.st.com/resource/en/reference_manual/rm0456-stm32u575585-armbased-32bit-mcus-stmicroelectronics.pdf),
[S3 TRM](https://documentation.espressif.com/esp32-s3_technical_reference_manual_en.pdf),
[pinned IDF memory linker](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/esp_system/ld/esp32s3/memory.ld.in),
[section linker](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/esp_system/ld/esp32s3/sections.ld.in),
[bootloader memory linker](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/bootloader/subproject/main/ld/esp32s3/bootloader.memory.ld.in),
[pinned HAL initialization](https://github.com/embassy-rs/embassy/blob/69006a4158aa6d605ad8506ade0f2f79159131e3/embassy-stm32/src/lib.rs).
This completes the finite memory allocation/ownership decision table; final
host rows still depend on the other C01–C09 decisions and C10 exact review.
