# S3 SPI, controls and finite source decisions

This completes the selected C07 SPI/input source table for the retained
WROOM-1-N8R8/DevKitC-1v1.1 paper tuple. It does not select a USB transport,
driver, display, received board or supported operation. The
[clock reference condition remains false](s3-clock-proposal.json), the
[display prerequisite remains unsatisfied](panel-subset-review.md), and the
[memory caps remain unmeasured](memory-ownership-contract.md).
The maintainer's reported S3/two-button inventory is not identification of this
proposed six-contact module/kit tuple.

## One proposed SPI path

| Item | Exact requirement / source correspondence |
| --- | --- |
| Signals | SPI2 SCLK GPIO12/J1.18 and MOSI GPIO11/J1.17 use their function4 IO_MUX route. GPIO10/J1.16 is software CS, GPIO13/J1.19 D/C, GPIO14/J1.20 reset and GPIO9/J1.15 external blanking control. Controls use GPIO function, not their FSPI/UART alternatives. No MISO, hardware CS output, WP/HD/DQS, SPI3, flash-SPI reassignment or new peripheral. Exact pad/rail/reset and fixture obligations remain C01/C02/C09. |
| Clock | Conditional PLL_F80M source, MST_CLK_SEL1, with fixed C03 CPU160/APB80/PLL480. Proposed predivider0, N31/H15/L31, EQU_SYSCLK0 gives2.5 MHz and50% nominal duty. Under the still-unmet±100 ppm reference condition,2,499,750–2,500,250 Hz is below the conditional panel5 MHz ceiling. Source accuracy, actual edges and timing are not qualified by that calculation. |
| Format | Master, mode0: CK_IDLE_EDGE0/CK_OUT_EDGE0; one-bit SDR; WR_BIT_ORDER0 means MSB first according to Table30.5-5/register30.6 and the pinned LL. Preserve the opposite footnotes in Tables30.5-9/10; do not invert the register setting to follow them. Bytes are explicitly ordered in memory; RGB565 high/low byte order is not CPU-endianness inference. |
| Phases | Software D/C distinguishes an opcode byte from parameters/pixels; these are MOSI data, not the controller's separate command/address engine. Disable automatic CMD/ADDR/DUMMY/MISO, DOUTDIN, SIO, QPI/OPI/multiline/DTR, segmented/slave and RX/TX-DMA paths. Enable MOSI low-part data buffer only; no high-part wrap or external RAM. |
| Capacity | SPI_W0–W15 hold64 bytes. Each transaction is1–64 whole bytes; MS_DATA_BITLEN=8n−1, maximum511. Above64 the CPU buffer can repeat/overwrite; a larger length field is not capacity. Every command/tail uses an aligned, initialized, owned backing allocation rounded up to four bytes. LL `write_buffer` copies four bytes per word even for a short last word. A one-byte borrowed object is not sufficient backing. No reproduced out-of-bounds incident is claimed. |
| Secret/public rows | C05's public and private512-byte row slots remain distinct, four-byte aligned, with480 active bytes and initialized padding. Command scratch is separately counted in its owning public/secret partition. Recovery pixel bytes never stage through a public/USB slot. No full framebuffer or queued-transfer API is selected. |
| Select/completion | Keep software CS and D/C stable across every chunk of one command/data phase; all hardware CS pins disabled/unmapped. Clear captured TRANS_DONE before starting; apply configuration only idle, request UPDATE, then finite completion check, then USR. Completion requires fresh TRANS_DONE and USR0, followed by proposed minimum1 µs final/setup/hold guards using qualified C03 time before changing CS/D/C. Internal controller completion does not assert that the software CS pin went high or that a panel accepted pixels. |
| Finite caps | Proposed one transaction≤1 ms and8,192 polls, whichever first, including fresh time reads/config UPDATE/start/completion/error handling; one480-byte row≤10 ms including eight chunks/header/guards. These are finite refusal/qualification caps, not measured normal latency. At the conditional minimum clock,64-byte wire payload alone takes about204.821 µs; budgets must also include all software/IRQ overhead. No vendor call outside the absolute budget. |
| Events | Polling only: SPI interrupt enables0. CPU transfer still uses TRANS_DONE in the register named DMA_INT_RAW; that name does not enable GDMA. Check fresh done and unexpected master/DMA errors; clear captured applicable events through CLR, never all ones or RAW/status RMW. Named master checks are done12, RX-AFIFO-full17, TX-AFIFO-empty18; unexpected DMA-FIFO0/1 also faults. C05 keeps GDMA/EDMA reset/gated and all requester permissions denied. |
| Failure | Timeout/config-update failure/clock or source change/unexpected event aborts the row and entire review, blanks through the qualified default-off interface, stops clocks/CS through the reviewed reset policy, clears owned software/FIFO storage and leaves display/source unqualified. No “partial row is fine,” retry-until-success, saved consent or hidden display readback guarantee. Peripheral reset/zero overwrite is not complete physical remanence erasure. |

## What the retained vendor code actually establishes

IDFfff9895's selected `spi_master.c` copies the mode and TX/RX-LSBFIRST flags,
chooses one data line absent explicit multiline flags, and uses a CPU buffer path
when `dma_enabled` is false. A null RX buffer with half-duplex TX avoids the
full-duplex default RX-length assignment. The LL assigns WR_BIT_ORDER directly
from the LSB-first boolean and sets the mode0 bits above. This is selected
source correspondence; the intervening HAL, bus/pin initialization, clock
calculator, interrupt allocator and effective binary are not fully reviewed.

The same source prevents accepting the stock call path as bounded:

* `spi_device_polling_start` accepts only `portMAX_DELAY`, including bus-lock or
  background waits; its wrapper passes that value to start **and** end.
* `polling_end` busy-waits with the RTOS tick. On timeout it returns before
  post-transfer cleanup, buffer release, polling-state clear or bus unlock.
* LL `apply_config` waits for CMD.UPDATE without a deadline. A task timeout
  outside that synchronous wait cannot preempt it.
* Device creation allocates driver/queue state and enables a source clock using
  cached frequency information. No per-transaction allocation is needed in the
  selected non-DMA private-descriptor branch, but startup allocation, lock and
  call/feature ownership still require proof. Single ownership alone does not
  make an unbounded call finite. Require queue_size1 for the allocated driver
  state, no queue API calls, and count both allocated queues/runtime metadata
  within C05 even though no logical transfer backlog is allowed.

The retained path therefore needs scoped finite remedies using the existing
C03 time contract, fixed memory/ownership, explicit no-DMA/pin/clock readback and
fallible abort propagation. No alternative driver or direct-register new port is
selected to bypass those requirements. Stock code and headers do not qualify
normal operation, panel timing, actual byte/bit order or completion on a board.

## Physical controls and interrupt ownership

GPIO4/5/6/7 on J1.4–7 are directional contacts; GPIO17/J1.10 selects locally;
GPIO18/J1.11 is separate consent. Use normally-open dry contacts to target
ground and the C01 external target-rail pull network. Enable digital input,
disable output/open-drain/internal pulls/unused peripheral routes and release
applicable RTC/digital holds before accepting a level. The LL explicitly warns
that a pin without input enabled reads0; zero is not evidence of a held contact.
GPIO0/3/45/46 straps, CHIP_PU, UART auto-programming, GPIO19/20 USB and GPIO35–37
N8R8 memory are excluded as contacts. GPIO8/J1.12 remains reserved solely for
the conditional attach fixture; it is not another confirmation input.

The proposal uses a bounded any-edge latch for the six controls, CPU0 only,
ordinary level1 interrupt, no GPIO NMI/wake/sleep/filter feature. Exact CPU-line
reservation and all system/fault/watchdog priorities are part of C03. Snapshot
only the selected bits, acknowledge captured W1TC source bits and record an
invalidation/change flag; no display/USB/crypto/logging, allocation or approval
inside the ISR. Proposed limits are one snapshot, at most six callbacks and50 µs.
A flood is coalesced/masked into failed review state, never an unbounded ISR loop.
GPIO edge hardware is a latch, not an exact edge counter. Missing/coalesced
edges or disabled/misrouted IRQ cannot grant consent.

The selected GPIO driver drains finite captured status words and clears an
edge before its callback. S3's CPU interrupt-enable bit/status is shared between
cores in the LL; the core argument is ignored there. CPU0 interrupt allocation
and CPU1 reset/gating are both required, not two independent GPIO owners.
`gpio_config` warns about a reservation conflict but continues and returns
success; it also remuxes to GPIO and may deinitialize an RTC pad. Treat conflict,
unexpected route or readback mismatch as failed startup. A warning or ESP_OK is
not ownership proof. ISR allocation/callback storage must be internal/IRAM as
required by the actual cache/flash policy; effective CONFIG_FREERTOS_UNICORE and
all callsites remain H02 checks.

Proposed debounce requires20 ms continuously stable release after boot/reset/
fault/cancel/reconnection, followed by20 ms continuously stable press for a
new consent event. The expected press is evaluated by the trusted post-render
debounce state; the ISR only flags a change. Level scans/edge processing during idle/render have a proposed
≤1 ms interval; this is unmeasured. IRQs only invalidate/notify: the trusted flow
alone authorizes the fully rendered exact operation. Any edge/cancellation or
attach/source change during an opaque backend call is latched and rechecked
before committing/releasing its output. No callback grants a signature and no
held key, stable low at startup, bounce, reset or old result becomes new consent.
Actual latency, stuck inputs and usable local recovery remain H02 gates.

## C07 transport disposition remains finite

The OTG alternative stays deferred because the required comprehensive IP
semantics are NDA-bound. The fixed USB Serial/JTAG CDC alternative retains its
[public byte/IRQ/reset/writer contract](s3-usj-contract.md), but is **unselected**.
The exact fixed descriptor/current/self-power/GET_STATUS fields remain the
independent received-capture/refusal gate in
[s3-attach-contract.md](s3-attach-contract.md). Neither the unmeasured whole-kit
bus-powered route nor the conditional external fixture is selected by this SPI
reading. No GPIO/SOF/timeout/bus-reset event proves physical unplug, and no
fixture rewrites hardwired descriptors or missing OTG semantics. Effective
console/boot logging and owner-secured debug/whole-CDC fuse policy remain C04.

H02 tests the actual pinned/modified path and effective map/features with public
fixtures after **all** prerequisite stops permit that operation. Expected
negatives are refusal/blanking/no authority or output for oversize/partial/padded-
tail violations, stale done/update, no clock, endpoint or GPIO flood, conflicts,
missed edges, held consent and reset/source changes. No target build, library
call, waveform, injection, entropy/identity generation or physical test ran here.
Exact primary identities/read scopes are in [manual-register.json](manual-register.json).
