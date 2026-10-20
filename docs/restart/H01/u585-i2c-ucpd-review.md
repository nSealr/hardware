# U585 kit-control I2C and CC configuration correspondence

Author `/root/h01_sol`, 20 October 2026, from `0672514`. This continues the
[kit/boot review](u585-kit-usb-boot-review.md); no host, driver, sensing path or
wiring is admitted. The bus controls USB protection and is shared with kit
devices. It is not a selected-SE custody channel.

## CPU-driven I2C2 contract

RM0456 Rev7 §§65.3–65.4 and65.9 distinguish interface/kernel clocks, input
filters, transfer counts and actual STOP completion. The documentary proposal
is one trusted controller, seven-bit TCPP03 address0x34, short explicitly
counted register transactions, polling, and no target/SMBus/DMA/autonomous
operation. It requires these controls and failure rules:

| Area | Required behavior before selection |
| --- | --- |
| Clock/pins | Choose a real I2C2 kernel source and TIMINGR tuple including oscillator tolerance, both filters and worst-case rise/fall times. Standard-mode alone does not determine those fields. ES0499§2.20.1 requires at least4MHz I2CCLK for a250ns transmitter setup time; the analogous Fast/Fm+ bounds are10/20MHz. |
| Unused modes | Own-address enables, general call, SMBus/PEC/alert, FMP, wake-up, data DMA and AUTOCR trigger/event-DMA enables stay clear. NOSTRETCH stays0 in controller mode. No unreviewed target or autonomous operation is implied by unused APIs. |
| Transaction | Verify the bus lines are idle before starting a fresh transaction; do not rewrite address/count/direction while START remains set. Bind NBYTES to the exact nonzero short buffer and keep RELOAD=0 for this control subset. Register reads may use a counted write plus repeated START and counted read; success includes the intended final STOP. |
| Receive completion | Read RXDR only for fresh RXNE. Count actual received bytes; a STOP, address event or deadline before the expected byte count is failure. Neither TXE nor TC alone proves a complete transaction and released external bus. |
| Deadline/error | One absolute deadline covers START, every byte, TC and STOP, including recovery. NACK/ARLO/bus error or timeout invalidates the status and pending USB request/consent. Do not retry a power-control write until the actual mode/gates and permitted recovery are established. |
| Reset | Clearing PE releases this MCU's SCL/SDA and resets communication/status while retaining configuration. Keep PE low for at least3APB cycles and check it. This does not release a line held low by another device or prove the TCPP03 state reset. A wedged shared bus is a failed connection, not a reason for unbounded recovery. |

Polling status is still necessary when peripheral interrupt enables are zero.
The manual's hardware SMBus timers are separate from the application's overall
deadline and remain disabled in this proposal. ES0499§2.20.2 permits continuing
after a spurious controller BERR once cleared; choosing to abort instead must
still safely finish/reset the transaction and invalidate its result. Its
target-timeout SDA defect (§2.20.3) is not a reason to enable target mode.

ES0499§2.4.1 is revisionX-only in Table3; W/U are unaffected. For a conditional
revisionX configuration the analog filter can add current in the listed
Stop2/3 conditions; changing
ANFOFF only after GPIO AF configuration does not implement its all-mode
workaround. The documented workaround disables the analog filter before AF
configuration and uses a digital filter, which prevents I2C operation in Stop.
Do not attach that defect or workaround to the current revisionU proposal.
For every revision, I2C2 must be
disabled before a Stop mode it cannot support; its wake support is Stop0/1,
unlike I2C3's Stop2 support. No whole-kit suspend-current claim follows.

## Pinned I2C software correspondence

The existing Embassy candidate commit is
`69006a4158aa6d605ad8506ade0f2f79159131e3`. Its exact generated-data commit
`b99bf17d58e6a8d385faf4b87b5f310ca2c057a0` identifies I2C2 as `i2c_v2`.
The AI kit metadata includes PH4 SCL/PH5 SDA, AF4; the VI package metadata
does not expose those kit pins. Both identify PCLK1, CCIPR1.I2C2SEL and the
APB1ENR1/APB1RSTR1 I2C2 fields. This is selected software metadata; current
DS package/AF/electrical evidence remains separately required.

The blocking constructor does not unmask the event/error NVIC lines or attach
DMA handles. It resets/enables RCC and initializes timing; the seven-bit
address conversion shifts into CR2.SADD, so0x34 is the API value. A single
`Timeout` is shared through a blocking write/read sequence. These are useful
correspondences, with material limits:

* `Timeout` has a real absolute deadline only with the `time` feature and a
  working time backend. Without that feature, checks always succeed. The
  configured default is1000ms when the feature exists; it is not a selected
  USB disconnect or UI-progress budget.
* `soft_reset` waits for PE to clear without a timeout. It is called from
  selected BERR/ARLO error handling; an outer task timeout does not preempt it.
* `wait_rxne` reports an early STOP without RXNE as `StopReceived`, distinct
  from `DataAvailable`. The selected master `read_internal` ignores that enum
  and reads RXDR after any successful helper result. It therefore does not
  prove the required exact byte count under that status condition. No physical
  occurrence, normal-traffic failure or reproduced upstream bug is asserted.
* Timeout exits do not uniformly perform a bounded abort/reset or establish
  that the external bus and TCPP03 are safe. Drop gates the RCC clock; it is
  not the required control/transport failure policy.
* Initialization forces the analog filter on. The timing calculator receives
  kernel and requested bus frequencies, without the full measured/toleranced
  load/filter inputs required by the selected timing equations. Its minimum
  kernel assertions2/8/17MHz do not implement the sampling erratum's4/10/20MHz bounds.

The selected stock API is consequently not admitted as the complete bounded
TCPP03 adapter. A narrow adapter must satisfy the contract above, including
the status distinction, clock/filter policy and every recovery wait.

## UCPD sink-only alternative and reset lifetime

The TCPP03-only Hibernate/dead-battery proposal and a UCPD-assisted sink
proposal remain alternatives. Neither is selected to avoid the unresolved EN,
VBUS sensing, power or lifecycle requirements. USB PD, source, VCONN, FRS,
BMC traffic and UCPD DMA remain excluded in either proposed initial scope.

For the UCPD-assisted alternative RM0456 §§74.4.6–74.5.2 requires setting
sink analog mode and enabling both CC terminations before releasing the
dead-battery behavior. The actual control is PWR_UCPDR.UCPD_DBDIS, not the
chapter74 prose's old PWR_CR3 location. Its register is protected by UCPD1's
GTZC attribution. UCPD_STBY has its documented Stop3/Standby sequencing;
PWR_UCPDR is not reset merely by exiting Standby. The exact allowed low-power
mode therefore has to be part of the chosen configuration.

Disabling UCPDEN immediately ends activity and returns control fields to reset
values. Restoring its RCC clock is not sufficient reinitialization. A no-PD
sink requires explicit RX/TX-DMA=0, PHYRXEN=0, FRS and transmission commands
inactive, no unsolicited packet path, and an explicit IMR/NVIC/EXTI policy.
CC voltage events and UCPD's hardware debounce do not replace VBUS detection
or the full Type-C connection state machine. Both the external TCPP03 and the
MCU termination state have to be valid across reset and mode changes.

Table774 distinguishes U585 revisionX, with automatic trimming and reserved
CFGR3, from later applicable variants that use software trimming. For the
current revisionU proposal the stored Rd values at0x0BFA0544/0x0BFA0546 and
CFGR3 fields correspond to the selected current text. Do not apply that write
to revisionX. ES0499 Table3 marks the Rp/Rd tolerance defects as revisionX
only; it does not attach them to W/U. The PD-underflow erratum remains
applicable across revisions but its DMA remedy does not authorize DMA in a
no-PD configuration.

The native current clock tree, Figure38 p487, was visually inspected, with
particular attention to the direct HSI16→UCPD1 branch. PCLK1 is its register
bus clock. The exact generated AI/VI metadata calls PCLK1 the UCPD kernel
clock; that differs from the current clock tree and the candidate driver's
HSI16 assumption. Retain this discrepancy and verify oscillator enable/ready
and divider behavior against the chosen clock/reset policy. Do not calculate
the UCPD divider from that metadata's PCLK1 value.

The pinned Embassy `Ucpd::new` enables the interrupt and both DMA-request
bits, and enables reception of a Hard Reset ordered set. Its CC interface
does not make this constructor equivalent to the no-PD/no-DMA proposal.
Its U5 trimming addresses agree with the selected revisionU text, but the
family-wide software branch does not itself discriminate revisionX. Effective
features, exact target revision and an explicit configuration remain required.

## Preserved text differences and reading scope

The manual's CFGR2 description allows writes only while UCPDEN=0, whereas
the generic startup steps enable UCPD before asking for the Rx analog filter.
The register constraint must be respected in a proposed sequence. TYPECEVT1's
status prose names TYPECEVT2CF, while the clear-register definition assigns
TYPECEVT1CF to CC1; clear the actual documented per-line bit and check status.
I2C's interrupt table says TCR clears on NBYTES=0, whereas functional/register
text says nonzero; reload is excluded from this small control proposal. The
functional SDADEL expression includes an additional I2CCLK term absent from
the short register expression; the final timing calculation must account for
the full functional path and external transitions, not a register formula alone.

Fresh RM text: pp2687–2699; pp2709–2719; pp2735–2737 (p2737 includes only
the beginning of DMA transmission text); pp2739–2753; pp3459–3463;
pp3472–3475; pp3478–3490 and p3491 before§74.8.8; pp458–459 before§10.10.13.
The beginning of p3472's receiver exception text and p3478's DMA receive text
were encountered, not a full PD review. Native p487 Figure38 was visually
inspected; no other new diagram/bit-layout visual review is claimed. The
selected UCPD1EN definition p565 was reread. ES0499 pp32–33 and§2.4.1p17
were freshly read, UCPD pp40–41/Table3p5 reread; selected I2C applicability
rows p4 and GPIO§2.4.1 row p3 checked. Target/SMBus/autonomous
functional bodies, full DMA paths and PD packet algorithms remain unread.

Fresh source: `i2c/mod.rs` lines1–343; `i2c/v2.rs` lines115–359,400–632,
2657–2810; `i2c/config.rs` lines1–145,158–235; `wait.rs` complete;
`ucpd.rs` lines1–75,120–214,265–310,327–365. AI/VI metadata review is limited
to selected package labels and I2C2/UCPD1 objects. No complete driver/PAC,
effective target build, timing waveform, physical failure or host signoff is
established. All six documentary rows remain incomplete.
