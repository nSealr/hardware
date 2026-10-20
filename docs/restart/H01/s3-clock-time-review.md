# S3 clock and polling-time correspondence

This C03 increment fixes a proposed clock/time tuple for the existing
ESP32-S3-WROOM-1-N8R8 kit workload. It is not an effective build, a measured
clock or a complete host signoff. The descriptor/power refusal gates remain
in [s3-attach-contract.md](s3-attach-contract.md); this tuple cannot select CDC
or make an incompatible self-powered descriptor valid.

## Proposed fixed active tuple

| Item | Documentary choice and limits |
| --- | --- |
| Main reference | Fitted module40 MHz crystal. Module DS1.8 nativep39 Figure8-1 labels40 MHz ±10 ppm in its **reference schematic**, with crystal-dependent capacitors still TBD. This is useful nominal design evidence, not a measured received-module tolerance over load, temperature and aging. No replacement oscillator is proposed. |
| CPU/APB | BBPLL480 MHz, CPU160 MHz, APB80 MHz. TRM7.2 Tables7.2-1/2/4 give SOC_CLK_SEL1, PLL_FREQ_SEL1, CPUPERIOD_SEL1; APB is80 MHz when CPU is PLL-sourced. The pinned S3 CPU Kconfig defaults160 MHz, and XTAL Kconfig supports40 MHz. An effective sdkconfig must state these choices explicitly. |
| USB PHY | Fixed Serial/JTAG needs PLL-derived48 MHz and APB≥40 MHz. Retain PLL/APB throughout an attached/suspended conditional self-powered session. PM dynamic-frequency changes, light/deep sleep and runtime clock switching are excluded from that proposal; a bypass-bringup clock feature is not acceptable. Hardware configuration/PLL-ready status is not a measured USB accuracy or jitter result. |
| Calculation envelope | Require the actual40 MHz reference to remain within±100 ppm for the defined paper-probe operating conditions. This is an engineering acceptance allocation, not a new manufacturer guarantee. It gives39,996,000–40,004,000 Hz; SYSTIMER's corresponding average rate is15,998,400–16,001,600 Hz. Reference/PLL/PHY accuracy, jitter, rail and temperature conditions must be established before using the conversion or USB interface. No received clock has met this condition. |
| Timer | Existing52-bit SYSTIMER UNIT1, exclusive polling owner; no new timer or UNIT1 alarm. Its fixed fractional divider counts alternately with XTAL/3 and XTAL/2 periods, average XTAL/2.5 =16 MHz nominal. APB clocks register accesses. Unit0 and all framework alarms retain their separate owners. |
| Stall/retention | UNIT1_WORK_EN1; UNIT1_CORE0_STALL_EN0 and CORE1_STALL_EN0. Reset defaults leave UNIT1 disabled with its stall enables set. Explicitly establish and read back ownership/configuration. No deadline or consent survives timer reload, reset, clock change, sleep or loss of reference validity. |

The±100 ppm envelope is a required qualification condition. The±10 ppm
reference-schematic annotation does not establish its complete temperature,
load, aging or PLL/PHY error budget. USB2's full-speed-only data-rate tolerance
and separate jitter/edge limits still govern the complete path; no compliance
claim follows from the nominal divider arithmetic.

## Fresh, bounded counter read

TRM11.3–11.5 gives a distinct count clock and APB register clock. `UPDATE`
latches high20/low32 bits and asserts `VALUE_VALID`; latched values remain
unchanged until the next update. Nativep644 defines UNIT1 `VALUE_VALID` bit29
as R/SS/WTC and `UPDATE` bit30 as WT. A stale valid bit or a second owner can
invalidate a supposed fresh timestamp.

The proposed owner must establish a fresh latch with explicit defined writes:
clear the old WTC valid indication, confirm the cleared state within a finite
guard, issue update, then wait for a new valid indication within a finite
guard. Read the latched low32/high20 value without another owner updating or
reloading the unit. A consistency check may fail; it must not retry forever.
Do not write reserved bits, infer timestamp freshness from a prior valid bit,
or depend on incidental compiler read/modify/write of a mixed WT/WTC register.
This strengthens the documented read procedure; it is a proposed adapter
requirement, not a claimed vendor defect or implemented register sequence.

A reviewable initial guard is at most64 status polls per phase and at most
two consistency attempts. It is an engineering failure bound, not a published
normal-latency guarantee. Exhaustion, inconsistent values, no counter progress
or wrong ownership returns a timer fault and invalidates partial work/consent.
The polling guard itself must not call the same possibly stalled timer. Clock-
phase-correct startup bounds and bounded interrupt/critical-section latency
remain necessary; no tick ISR is assumed to run while interrupts are masked.
H02 must establish that the guard succeeds under normal supported conditions
and refuses injected stalls, rather than accepting an always-failing timer.

UNIT1 operation offsets are OP0x08, load-high/low0x14/0x18,
value-high/low0x48/0x4c, load0x60. The counter is52 bits, not the software
API's advertised64-bit width. A system-level timer reset or HAL deinit affects
the shared module and cannot be used to repair UNIT1 after framework timers
have started. Preserve Unit0, comparator, clock and interrupt ownership under
the common register lock; there is no isolated per-unit reset claim.

## Deadline conversion requirements

Use elapsed ticks modulo2^52 with intervals below half range. At the required
maximum rate the full wrap is about8.92 years; this does not make reload,
debugging, clock loss or another owner safe. Recheck valid configuration and
progress before starting a sensitive operation. Longer protocol/profile bounds
remain the separate finite C05 contract; no new wire format or product maximum
is introduced by these short-operation examples.

For a maximum permitted duration, convert with the **minimum** rate and round
down, subtracting the bounded observation/execution overhead. For a required
minimum wait, use the **maximum** rate and round up, adding a conservative
fractional-tick/comparison allowance. The alternating clock periods are50/75 ns
at nominal40 MHz; an average62.5 ns is not an exact per-tick period.

At the conditional±100 ppm envelope,1 ms corresponds to a deadline threshold
of at most15,998 ticks before overhead, and a120 ms minimum wait requires at
least1,920,192 ticks before the comparison allowance. These are arithmetic
examples, not end-to-end polling or display deadlines. The fixture's maximum
1 ms status observation must include scheduling, counter reads and processing;
setting a nominal1 ms timer period alone fails that requirement. The allowed
startup/USB/display/consent policy must use one remaining absolute budget
across every queue, retry, mutex, hardware wait and service step.

## Actual pinned source behavior

All source references use IDF commit
`fff9895c82d744c7237be8847347bdd1b07c6643`.

| Source | Correspondence and remaining remedy |
| --- | --- |
| S3 `rtc_clk.c` | CPU160 maps to PLL480/3; the selected register field values agree with the public clock table. BBPLL calibration waits in an unbounded loop, followed by10 µs delay. The source manages voltage/slave settings around CPU changes; copying only divider writes omits those controls. The mutable consumer count prevents some PLL shutdown paths but is not hardware enforcement. A separate direct set-XTAL/sleep path disables PLL. Exclude runtime transitions and require a bounded startup/failure path before secrets. |
| S3 `clk_tree_ll.h` | Selected PLL enable/config/calibration and CPU-source/divider helpers were read. Analog PLL settings use the chip's internal register-I2C path; the public source establishes those writes, not an independently documented PLL lock-time/accuracy guarantee. The32 MHz and320 MHz branches were encountered but remain excluded. No analog tuning or fuse operation is performed. |
| S3 `rtc_clk_init.c` | Entire source read. It waits for ROM UART TX idle, sets frequency metadata, changes the CPU clock, rescales CPU cycle count, then establishes slow/fast clocks. The latter retains RC_FAST for boot entropy. Neither UART-idle nor nested PLL wait is made finite by an outer application timeout. Do not load secrets before the selected bounded startup and state checks finish. |
| SYSTIMER LL/HAL | Entire files read. LL uses the fixed2.5 divider and separate bus clock/reset helpers. HAL `get_counter_value` waits indefinitely for valid, then retries low/high/low consistency until equal. Its shared deinit gates the module. The source does not supply the proposed fallible finite read/ownership policy. Unused alarm and other-chip branches do not become part of UNIT1 polling. |
| `esp_timer_impl_systimer.c` | Entire source read. `esp_timer` uses UNIT0/alarm2 and returns through that unbounded HAL read. It can set/advance its counter and configures stall behavior for active cores. Its one-handler ISR and multiple-handler retry branch are conditional on effective features; a single application polling owner cannot assume a callback is a hard deadline. Keep UNIT1 separate and require effective system/link ownership evidence before execution. |
| CPU/XTAL Kconfigs | Both complete files read. Desired160/40 MHz choices are available, but defaults and source availability are not an effective configuration. The existing console/PM/bringup/debug/radio/master exclusions remain mandatory. |

This selects no new timer implementation or driver alternative. H02 must
implement the reviewed bounded adapter within the retained source route, pin
the effective features/binary and measure normal and failure behavior. C03
still requires the exact supply/reset/watchdog/IRQ/startup correspondence and
complete host state table; C07 still requires its existing SPI/input and
transport-admission decisions. No critical loop is called during this review.

Sources: [TRM1.8](https://documentation.espressif.com/esp32-s3_technical_reference_manual_en.pdf),
[module DS1.8](https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf),
[clock source](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/esp_hw_support/port/esp32s3/rtc_clk.c),
[clock init](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/esp_hw_support/port/esp32s3/rtc_clk_init.c),
[clock LL](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/esp_hal_clock/esp32s3/include/hal/clk_tree_ll.h),
[SYSTIMER HAL](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/esp_hal_systimer/systimer_hal.c),
[SYSTIMER LL](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/esp_hal_systimer/esp32s3/include/hal/systimer_ll.h),
[esp_timer implementation](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/esp_timer/src/esp_timer_impl_systimer.c).
Source hashes, actual read ranges and three selected native renders are
recorded in the register. The WROOM-1U nativep40 was encountered during the
locator check; only WROOM-1 nativep39 supports the retained module diagram.
