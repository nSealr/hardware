# U585 interrupt and short-deadline source contract

Author `/root/h01_sol`, 20 October 2026, from `cbdfd29`. This records selected
current Cortex-M33 and U585 source reading. It does not select an interrupt/time
backend, enable a new peripheral or complete a host row.

## External IRQs, system exceptions and security are separate

RM0456 Rev7 chapter22 lists the family vector positions and offsets. Its4
implemented priority bits match both exact AI and VI generated-data objects.
The table's sequential “Priority” column is not the configured runtime priority;
IPR fields reset to zero. Use explicit supported priority values and grouping,
with lower numeric values giving higher urgency. Equal group priorities do not
preempt one another. The current manual's family maximum is not an instruction
to enable every listed slot; its footnote reserves absent-device peripherals.

[The selected IRQ correspondence](u585-interrupt-subset.json) maps the relevant
sources to their explicit IRQ numbers, vector offsets, register indices and bit
masks. It is a subset, not the complete final allowlist. In particular, TIM2 and
ADC4 remain excluded in the existing peripheral manifest; their presence in a
source table does not enable them. Polling SPI1/I2C2 and disabled IWDG early
warning do not need their peripheral/NVIC interrupt enables. UCPD, CRS and
fault-source enables still depend on their final mode and source controls.

PM0264 Rev8 §4.2 says the external enable, pending, active and priority registers
are not banked between security states; access is filtered by ITNS. Secure-only
ITNS=0 targets secure execution, ITNS=1 nonsecure. Nonsecure access to secure
interrupt fields is read-as-zero/write-ignored, not a readable secure-state
witness. These controls are separate from GTZC peripheral ownership and from
the core's banked exception masks/SysTick/secure vector selection.

For the single trusted secure-image proposal, initialize the secure handlers,
vector base/alignment, fault policy, security targeting and supported priorities
before unmasking any selected source. Keep all unused sources disabled at both
the peripheral and NVIC as applicable. Verify source ownership while clocks
make the peripheral readable; a gated-register zero is not a valid disable
witness. No untrusted application or hostile-code isolation is established by
these controls inside the trusted privileged image.

Disabling a NVIC line does not clear its pending state. Clearing pending does
not clear active state or acknowledge a held level at its peripheral. A still
asserted source can immediately re-pend. Each handler therefore needs an exact
source read/acknowledgement and a bounded fault path; repeatedly clearing NVIC
pending is not recovery. A default weak handler that loops forever is not the
proposed failure policy. Unknown/unexpected IRQs invalidate pending consent and
enter bounded failure handling without feeding the watchdog.

AIRCR has key-protected writes, field-specific banking and secure-only controls.
The selected secure-extension table distinguishes PRIS, BFHFNMINS, PRIGROUP
and SYSRESETREQS. They are not generic “secure mode” switches. For the current
one-image proposal retain secure fault/NMI targeting, make any nonsecure reset
permission explicit, preserve reserved/debug bits and verify actual values.
The handler table, exact reset/clock CSS behavior and source unmask policy remain
incomplete; source text is not an implemented exception image.

## A high-priority timer is not a universal timeout

PRIMASK_S masks configurable secure exceptions too. Raising a timer's NVIC
priority cannot make its ISR run through such a critical section. BASEPRI,
FAULTMASK, security targeting and priority grouping have different scopes.
Every synchronous USB/SPI/I2C/reset wait must therefore have an actual clock
that progresses in its allowed execution context, including the relevant IRQ
and critical section. The source checks already found loops that an outer task
deadline cannot preempt. Enabling an optional time feature is not a proof that
its backend advances in those loops.

PM0264 §4.4 supplies a bounded same-core alternative for investigation: the
secure 24-bit SysTick can count from an explicit nonzero reload value with
CLKSOURCE=processor-clock and TICKINT=0. Polling CURRENT does not require a
SysTick ISR. This can avoid enabling TIM2, but remains a conditional proposal:

* Reserve one exclusive secure SysTick owner. Initialize reload/current/control
  explicitly; do not depend on unknown reset values or another executor's timer.
* Bind conversion and rounding to the actual fixed processor frequency and its
  tolerance. A nominal calibration constant does not measure that frequency.
* Keep every supported modular deadline and maximum poll gap strictly below
  one 2^24-tick wrap, with an explicit conservative margin. Count elapsed ticks
  by validated modular arithmetic; COUNTFLAG is only a sticky indicator, not
  an unbounded count of wraps, and reading CSR clears it.
* No software can infer elapsed ticks if the clock stopped or multiple wraps
  were missed. Debug halt stops this counter. Sleep/Stop, clock changes and
  reset need explicit restrictions or invalidation/reinitialization; no wall
  clock or low-power elapsed-time claim is made.
* Keep the independently clocked watchdog/progress-owner proposal. Polling a
  clock cannot rescue a stopped clock/CPU; interrupt-only watchdog feeding or
  IWDG EWI service must not keep a stalled operation alive.

This is not a chosen or compiled Embassy time backend. It does not fix the
stock drivers' waits, warning-only continuation or critical-section behavior.
The final deadline values, timer implementation and clock/sleep/reset tuple
remain to be reviewed before the manifest admits a concrete time source.

## Retained source differences and reading scope

RM22 p912 broadly calls NVIC registers banked; PM§4.2 gives the field-specific
nonbanked/filter behavior above. PM§2.4.4 pp32–33 describes VTOR_S/VTOR_NS,
but its p189 VTOR introduction says “not banked”. Preserve that inconsistency;
the current single-image proposal uses only the secure vector base and does not
derive nonsecure isolation from that sentence. Generic vector figures contain
IRQ/exception labels that must not replace the explicit U585 positive IRQ map
and `(IRQ+16)*4` offset correspondence. No new visual figure review is claimed.

PM§4.2.10.1 p182 mentions an enable-register write as a pending cause, whereas
the explicit ISER/ISPR definitions distinguish enabling from forcing pending.
The contract uses their distinct register operations and actual source state.
The generic SysTick calibration defaults do not replace the U585-specific
calibration/clock controls. Remaining implementation placeholders in PM text
are not device-specific evidence of480 implemented U585 IRQs or8 priority bits.

Fresh RM0456 text: full chapter22 pp912–918, including Table186 and its
device/revision footnotes. Fresh PM0264 text: cover/applicability p1; selected
§1 introduction before§1.1; pp15–17; pp31–35; complete§4.2 pp176–182 and
p183 before§4.3; p189 (ICSR tail/VTOR); p190 beforeTable66; Table67 pp191–192
before§4.3.7.1; complete§4.4 pp205–206 and p207 before§4.5. Some nonsecure/
non-security-extension adjacent fields and vector-figure text were encountered;
the instruction set, complete SCB/fault/SAU/MPU and exception-entry/return
bodies remain unread. The first combined pp31–35 extraction truncated vector
text; pp32–33 were then read separately. No diagram/bit-layout visual review.

Exact AI/VI source review additionally read their four-bit priority metadata
and the selected IRQ-name/number records in the JSON subset. No complete PAC,
time driver, target binary, interrupt-flood test or physical waveform result is
claimed. Independent affected review and all six documentary signoffs remain
open.
