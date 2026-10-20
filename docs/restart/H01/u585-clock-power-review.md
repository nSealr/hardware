# U585 clock, deadline and existing-kit power correspondence

Author `/root/h01_sol`,20 October2026, source checkpoint
`e35d009605173b09a2040f6eeb30c3bd7a744a02`. This is a proposed documentary
tuple under C03/C06/C09, not a complete host configuration, compiled clock
backend, measured rail or admitted fixture. S3's clock/power tuple remains
separate. The [finite checklist](closure-checklist.md) remains the scope.

## One proposed Run tuple

The fixed-frequency proposal below avoids relying on an unfitted kit HSE or
on a debugger's clock. No new oscillator, peripheral or clock input is selected.

| Item | Proposed contract and source |
| --- | --- |
| Core regulator | LDO, VCORE range3, VOS=`01`, BOOSTEN=0. RM10.5.4 permits up to55MHz; source SMPS-capable package identity does not require enabling its converter. Final exact PWR/reset/supply fields still need binding. |
| System/AHB/APB | MSIS range0, nominal48MHz, continuous bias, no MSI PLL mode or software trimming; HPRE and PPRE1/2/3 divide by1. MSIK, HSE and system PLLs remain unnecessary in this proposal. |
| Conservative CPU-clock envelope |45–51MHz for subsequent calculations, derived from DS13086 Table83 initial47.74–48.70MHz and normal-mode temperature/VDD deviations, under its stated continuous-mode supply/junction conditions. This rounded envelope is an engineering calculation from characterized specifications, not a measured accuracy or a USB clock guarantee. |
| Flash/SRAM | FLASH LPM=0, LATENCY=2 before raising frequency, readback required; SRAM WSC=0 at range3. RM Tables54/47 cover55MHz. A one-wait-state flash setting justified by nominal48MHz would not cover the upper envelope. |
| SPI1 kernel | PCLK2, divide by16: nominal3MHz, at most3.1875MHz under the envelope, below the conditional panel ceiling5MHz. Explicit rising-capture/falling-change/first-bit/CS timing and ES0499 final-clock workaround remain mandatory. No stock source gap is waived. |
| I2C2 kernel | PCLK1. A Standard-mode timing candidate is derived below; fixed48MHz must not be silently assumed by a frequency-only calculator. |
| USB48MHz | HSI48 with CRS referenced to the already fitted LSE, not free-running HSI48 and not USB SOF. The reference and acceptance conditions below are required before attachment. ICLKSEL=`00`; unused SDMMC remains reset/clock excluded. |
| Short deadlines | Exclusive secure SysTick, processor clock, TICKINT=0, no ISR dependency. No TIM2 promotion. |
| Power states | The first tuple does not retain active requests through Stop/Standby/Shutdown or dynamic clock changes. Suspend handling must invalidate state and satisfy the chosen port-current arrangement. Keeping the CPU in Run is not proof of USB suspend compliance. |

The source sequence is to establish secure ownership/handlers while USB is
detached, configure VOS and wait for readiness with a bound, configure flash
latency and SRAM waits, read them back, and then change/reread the effective
clock/range/prescalers. Initialize the deadline conversion for the resulting
clock phase. Every readiness/status wait needs a bounded synchronous path;
an interrupt timer cannot preempt PRIMASK_S critical sections. Independent
progress-owned IWDG and the earlier EWI-disabled proposal remain necessary.

RM516–517 say a range above24MHz becomes 'range2 (24MHz)' on Stop wake,
while their own range table defines range1=24MHz and range2=16MHz. Preserve
the disagreement. This proposal uses neither an inherited Stop-wake range nor
an unverified wake-time conversion; a resumed request requires fresh clock
initialization and a new rendered review.

## Clock accuracy and the real CRS acceptance range

DS Table83 says MSI PLL accuracy follows its LSE reference. Its maximum0.8ms
PLL settling row, however, is explicitly to **1%** of final frequency. That
row alone cannot establish USB full-speed accuracy. Free-running HSI48 also
has much wider factory/temperature limits than USB allows. Neither a ready
bit nor an oscillator's '48MHz' name closes the USB clock requirement.

RM12 describes CRS in full for this subset. Its frequency counter compares
HSI48 with the selected divided reference. With automatic trimming:

* Error belowFELIM requires no adjustment.
* Error fromFELIM to below3×FELIM still sets **SYNCOK**, while adjusting one step.
* Error from3×FELIM to below128×FELIM sets SYNCWARN and adjusts two steps.
* Larger error, a missing reference or a trim limit sets the corresponding error.

Thus `SYNCOK` does not mean error belowFELIM. Flags are sticky; a stale flag
is not a fresh reference sample. Configure CFGR only with CEN=0, use32-bit
register access and clear only ICR bits0–3. Secure HSI48/ICLK RCC controls
**and** CRS through GTZC; RCC's HSI48 protection does not own CRS.TRIM.
An error/missed-reference condition invalidates transport/consent and requires
recovery before reattachment, not continued watchdog feeding during a loop.

A bounded arithmetic candidate uses LSE32.768kHz divided by32, giving1024Hz,
RELOAD=46874 and FELIM=29. This follows the DS typical0.12% trim step and the
RM rounding rule; the reset FELIM belongs to a different default assumption.
RELOAD exceeds128×29=3712 as required. Under SYNCOK the captured magnitude
is below87ticks, so an engineering bound allows87/46875=0.1856% relative
frequency error before reference/error allowances. A reference budget of at
most100ppm, plus a separately conservative three-clock comparison allowance,
gives about0.2021% by composition, below0.25%. The three-clock allowance is
an engineering guard, not a newly stated CRS production specification.

USB2 §7.1.11, printed159, requires12Mb/s ±0.25% for a full-speed-only
function, including initial accuracy, loading, voltage, temperature and aging.
Its printed160 jitter limits are separately±2ns for consecutive differential
transitions and±1ns for paired transitions, including the PHY/buffer effects.
A counter frequency calculation alone does not establish those output limits.

This is **not a selected clock qualification or a claim about X2's actual
accuracy**. Before the tuple can use that bound, bind the exact reference/load/
temperature/aging allowance and complete source/PHY clock/jitter binding. The
adapter must discard initial phase-dependent captures, require fresh complete
reference periods and error-free bounded convergence, then monitor reference
age/errors. A flag observed once is not continuous clock qualification.
Stop freezes CRS and stops HSI48; Standby/Shutdown lose CRS configuration.
SOF-only calibration also cannot provide the same independent reference during
USB inactivity. The selected LSE alternative avoids that dependency but still
needs the reference condition to be established.

Native kit sheet4 shows X1/HSE and its capacitors DNF, while X2 is NX1610SE
32.768kHz with3.9pF capacitors. Selected native SchDoc parameters name
**EXS00A-MU01499**; no linked internal-only supplier location was accessed.
The [NDK product](https://www.ndk.com/en/products/lineup/crystal-unit/NX1610SE.html)
and [NDKX01-00011-002](https://www.ndk.com/en/products/upload/lineup/pdf/NDKX01-00011_en.pdf)
give standard6/9/12.5pF variants,±20ppm at25°C excluding aging, turnover20–30°C
and parabolic coefficient−0.04ppm/°C². The PDF tolerance row prints °C where
the product body says ppm. These standard fields do not establish the exact
kit variant, effective load or total error. Its100ppm budget is therefore a
named unsatisfied reference condition, not an assumed board guarantee.

## Short-deadline arithmetic

At a maximum51MHz the24-bit counter wraps no sooner than328.965ms. The
proposal restricts each requested deadline/minimum-delay parameter to at
most200ms and requires every relevant polling interval to remain below one
wrap. COUNTFLAG cannot count missed wraps. Debug halt, clock change, another
SysTick owner, reset or use of Sleep/Stop elapsed time invalidates this basis.

Use the **minimum45MHz** conversion to expire a deadline no later than its
requested real duration; it may expire early. Use the **maximum51MHz**
conversion to satisfy a minimum wait; it may finish late. For example120ms
minimum reset recovery requires6,120,000ticks, while a200ms deadline uses
9,000,000ticks. Both fit within one wrap; a requested200ms minimum wait may
take226.667ms at the lower clock bound. Reversing these conversions can
silently extend a deadline or shorten a required hardware delay.

Longer UI/operation bounds must use explicit finite steps or a separately
proved accumulation policy. A complete153,600-byte image at nominal3MHz
already needs at least409.6ms of payload time and cannot fit into one short
SysTick interval. Bounded row/window operations and fixed row counts avoid
pretending that a single modular subtraction measures that whole interval.
These are calculation requirements, not a linked backend, latency result or
permission to feed the watchdog on mere USB activity.

## I2C2 timing candidate, not a complete electrical bus

Reread RM2694–2697 and UM10204 Rev7 pp43–45/50 with DS13086 pp298–299.
For the45–51MHz kernel envelope, Standard-mode rise≤1000ns/fall≤300ns,
analog filter enabled with the DS50–115ns range, and digital filter0, consider:

`PRESC=5, SCLDEL=10, SDADEL=2, SCLH=39, SCLL=44`, or `TIMINGR=0x50A2272C`.

The minimum programmed LOW/HIGH periods at51MHz are5.294/4.706µs, meeting
the4.7/4.0µs requirements before positive synchronization/filter/edge delays.
Their sum is10µs, so they do not generate more than100kHz. The minimum setup
delay is1.294µs against1.25µs required including worst-case rise. RM's SDADEL
inequalities give a maximum lower bound1.625 and minimum upper bound16.846;
the proposed value2 fits. Data delay itself spans235–267ns before the separately
defined synchronization/additional-clock contribution. This calculation uses
the selected device's115ns filter maximum, not a generic260ns assumption.

This is a timing-field candidate. It does not prove actual PH4/PH5 pull-ups,
capacitance, rise/fall, leakage, TCPP enable-derived I/O voltage or all shared
targets. Exact START/STOP/bus-free sequencing, minimum5µs bus-free policy,
byte counts, finalSTOP, bounded error/recovery and current errata remain part
of the adapter contract. No unused target/SMBus/DMA mode is enabled by incidental
reading. I2C timing/filter changes require PE=0; software PE reset retains the
configuration and does not force another device to release the wires.

## Pinned Rust startup correspondence

The existing Embassy commit is
`69006a4158aa6d605ad8506ade0f2f79159131e3`. Its selected
[`rcc/u5.rs`](https://github.com/embassy-rs/embassy/blob/69006a4158aa6d605ad8506ade0f2f79159131e3/embassy-stm32/src/rcc/u5.rs)
initialization uses HSI as an intermediate source, with unbounded readiness/
switch waits. Its frequency model is nominal. At configured MSIS48/range3 it
selects one flash wait state, which does not implement the proposed drift-aware
two-wait-state requirement. Its final latency write has no explicit readback
in the selected path. Disabling unused PLLs also waits without a deadline.
This source therefore needs the bounded initialization/latency remedy before
the tuple can be implemented; it is not accepted as conformant startup.

[`rcc/hsi48.rs`](https://github.com/embassy-rs/embassy/blob/69006a4158aa6d605ad8506ade0f2f79159131e3/embassy-stm32/src/rcc/hsi48.rs)
offers a USB-SOF synchronization flag and defaults it off. Its optional CRS
setup selects USB with reset reload/limit assumptions and does not wait for
fresh qualified captures. It cannot express this LSE/divider/reload/error
policy. HSI48 readiness is unbounded. A bounded adapter must own the required
configuration and failure handling; choosing that flag is insufficient.

[`rcc/bd.rs`](https://github.com/embassy-rs/embassy/blob/69006a4158aa6d605ad8506ade0f2f79159131e3/embassy-stm32/src/rcc/bd.rs)
defaults to LSI/RTC, while its LSE default leaves peripheral LSE routing off.
DBP, LSE and peripheral-ready waits are unbounded. Its U5 mismatch path skips
backup-domain reset; requesting RTC disabled does not explicitly clear an
inherited RTCEN in that path. Do not infer reset/disable/erasure from returned
clock metadata. Specify fresh-state auditing and explicit permitted recovery
before secrets, and never reset the backup domain around live SRAM2 secrets.

The selected library `init_hw` calls RCC inside a critical section, and RCC
`reinit` does likewise. An outer task timeout or higher-priority configurable
timer interrupt cannot make these synchronous waits finite. The planned secure
polling SysTick must have a valid clock-phase conversion inside each wait;
its final48MHz conversion cannot simply be used during intermediate HSI or
reset MSI phases. Effective features, global initialization side effects and
the reviewed bounded adapter remain H02 implementation gates, specified here
as positive and negative requirements. No new driver or timer is introduced.

## Existing supply branches and USB policy direction

UM2839 pp15–21 and native MB1551 sheet14 show that JP4 selects one5V source;
JP3 separates only VDD_MCU from the common3V3 rail. U19 is the fixed
ST1L05APU33R A-version, with no enable pin; camera LDO and board LEDs also
remain on the5V tree. An MCU Stop instruction cannot turn that tree off.
The [ST1L05 datasheet](https://www.st.com/resource/en/datasheet/st1l05.pdf),
Rev3 May2014, Table7 permits3.2175–3.3825V under its stated4.75–5.25V input,
load and0–125°C junction conditions; separate transient rows reach3.5/3.6V
under specified loads/capacitors. Those bounds prevent inheriting a guaranteed
≤3.3V raw-panel rail. The kit's actual capacitor/load conditions and waveforms
still need qualification. Normal input operation ends at5.5V; the7V absolute
input rating does not extend it.

For C09, the bounded direction is a **self-powered kit** with an independently
specified permitted5V source and CN1 used only for device transport/default
power detection. The exact existing supply selection and all reverse-current,
VBUS-visible capacitance and suspend limits remain to bind before selection.
UM2839 allows charger-only CN8/JP4[7–8] and expressly excludes a PC on that
charger-bypass setting; VIN7–12V/JP4[3–4] is a different existing source path.
The ordinary ST-LINK-powered setting depends on its own enumeration and is
not silently interchangeable. No connection or rework has been performed.

The already assessed TCPP-only **Hibernate** alternative keeps I2C and internal
dead-battery Rd active, its provider off and consumer gate software-controlled.
UCPD/PD/FRS/VCONN/source and ADC4 can remain excluded. A read of valid
register2.bit5 VBUS_OK reports a1.9–2.9V UVLO threshold; Type-C permits a
self-powered/default-power USB2-only non-PD, no-accessory sink to attach from
VBUS and requires disconnect threshold0.8–3.67V with transition within40ms.
The threshold ranges fit; mode/EN/read validity and the complete timing policy
remain necessary. Normal mode changes FLGn's meaning and disables internal
dead-battery Rd, so it cannot be substituted into this policy unnoticed.

USB2 §7.1.5.1 requires that the pull-up not supply data-line current when VBUS
is removed. A fresh status transaction and a bounded poll/failure path must
control actual USB detach; status timeout, old flags, bus reset or a failed I2C
read cannot mean 'still attached'. This is voltage-presence monitoring, not
proof that a physical plug is absent or all rails are unpowered. It does not
transfer to S3's J4, which has no such sensing circuit. Exact EN startup/hold,
gate acknowledgement, fault/reset behavior, poll deadline and power budget
are still required to select this U585 policy.

## Actual reading and remaining scope

Fresh RM: full CRS body/register textpp610–619 andp620 before register-map
summary; p609 wide RCC map encountered and excluded. Rereadpp280,295–297,
410–411,450,488–492,508,516–517,589–591,2694–2697. pp2700–2704 target-mode
text was incidentally read after a locator error; no target-mode review is
claimed or added to the workload. Fresh DS: pp221–225,298–299 before USART
body; p166 current-test conditions reread; pp297 and remaining299 unused SD/
USART context encountered, not selected. No new native RM/DS figures inspected.

Fresh ST1L05: pp1,3–5,7–8,10,16–18 text including unused-version/typical-plot
context; no new native figure audit. NDK: nativePDF pp1–2,8–9 text; product
technical identity/table; no other-part catalogue sweep. Native kit sheet14
visually inspected, sheet4 and S3 v1.1 sheet2 reread; selected X2 native
SchDoc records only. TCPP pp8–14 reread; p9 curves text encountered without
new native plots. USB2 physical169–170,178,187–188 /
printed141–142,150,159–160 newly read;
Type-C153,180–183,198–201 reread including unrelated charge-through context.
UM10204 pp43–44,45 before6.2 and50 newly reread from a rehashed preserved
public original. All originals/records/renders stay private.

Pinned source: U5 RCC declarations/defaults, initialization through clock
publication, range-frequency mapping and PLL-disable helper; initial unused
PLL setup context encountered, remaining PLL calculation/USBHS/DSI algorithms
unreviewed. HSI48 helper complete; backup-domain helper complete with unused
family branches encountered; RCC mod family selection and selected init/reinit/
feature glue only. Existing HAL lib selected `init`/critical-section/RCC-call
sites reread; no claim to all global HAL initialization side effects.

Finish only C03's effective PWR/RCC/supply and exact phase/deadline/source
binding, C06's TCPP/USB/IRQ adapter policy, C09's one actual permitted kit
supply/USB arrangement and the S3 counterparts. The reference budget, external
display obligations and future H02 measurements remain explicit. No new
peripheral, driver, host, physical test or admission follows from this note.
