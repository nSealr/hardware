# H01 proposed USB boundary

This is a documentary configuration, not USB certification, an enabled driver or
a wiring instruction. Both host witnesses use a full-speed USB **device** with
one control endpoint and one bounded data interface. Host, dual-role, isochronous,
high-speed, USB PD, BC1.2, VCONN, accessories and alternate modes are excluded.
The custom Board lead is a 5 V sink; an unnegotiated higher-voltage source is not
an allowed operating mode. Received-kit power topology and currents remain H02
checks. The S3 kit has Micro-B connectors, so Type-C CC requirements apply to a
future Type-C implementation and its cable, not to nonexistent kit CC pins.

The later [S3 USB Serial/JTAG assessment](s3-usb-serial-assessment.md) is an
unselected alternative to this S3 OTG proposal. That fixed composite device
has an additional JTAG interface and separate lifecycle gates; it is not
silently covered by the single-data-interface proposal above. Its public
register availability does not close driver/error, VBUS or power requirements.

## Normative power and connection requirements

The primary source is USB2.0, 27 April 2000, as distributed in USB-IF's
2025-06-03 bundle with its applicable errata/ECNs; the base PDF alone is not the
current rule set. The selected Type-C source is Release2.5, March2026, published
8 April2026. Originals and archive members remain private; identities are in
`manual-register.json`.

| Requirement | Source and implication |
| --- | --- |
| Default USB2 load | USB2 §7.2.1, printed p171: one unit load is a **maximum** 100 mA, not an average. High-power operation up to500 mA requires configuration and an adequate advertised budget. A kit limiter marked500 mA is not that permission. The proposed workload remains within its declared descriptor current; no unmeasured descriptor value is accepted. |
| Voltage range | USB2 §7.2.2 plus the complete VBUS Max Limit ECN: the upper VBUS supply limit is5.50 V, replacing5.25 V. Enumeration at the lower applicable cable-end voltage and regulator/protection tolerance must be checked. This says nothing about applying5.5 V to a3.3 V MCU or display pin. |
| Suspend | USB2 §7.2.3 plus complete Suspend Current ECN: non-ICUSB devices are limited to2.5 mA from VBUS in suspend, including pull-up current; the base PDF's500 µA row is superseded. Any1 s averaging interval, permitted peak and slope constraints still apply. Remote wake is excluded initially. A second supply is not proof of low current on the transport port. |
| Attach/inrush | USB2 §§7.2.4.1–.2 plus Device Capacitance ECN: connector-visible capacitance is1–10 µF in that ECN's specified range; larger downstream capacitance requires limiting so the attach load meets the10 µF/44 Ω model and330 mV droop requirement. Type-C Table4-3 additionally limits exposed capacitance to10 µF when not Attached.SNK. The later5.50 V operating range must also be covered by component voltage/tolerance assessment. |
| Source prohibition | USB2 §7.2.1: a device must not source upstream VBUS and must not power the D+/D− pull-up without VBUS. Type-C §§4.5.2.2.3–.5 likewise forbid sink VBUS/VCONN sourcing. Reverse current and powered-off I/O injection are measurements, not properties established by selecting sink software. |
| Normal connection timing | Connect Timing ECN pp4–6: a powered peripheral must connect and be ready to enumerate within1 s of session-valid VBUS; unit-load preconnect time is bounded to100 ms, and suspend rules apply after the1 s post-connect allowance. The dead/weak-battery redline case is outside the initial kit configuration and is not invoked as a waiver. Its coloured redlines were text-extracted, not visually resolved. |
| Default-power Type-C sink | Type-C §§4.5.2.2.3–.5,4.5.2.3.1 and4.6.2.1: independently terminate both CC pins with Rd. A USB2-only default-power, no-PD/no-accessory sink may attach directly on VBUS; then it must not infer orientation or higher current. No1.5/3 A consumption is proposed. Higher-current support would require CC monitoring and the complete adjustment policy, not just two resistors. |
| CC and disconnect | Type-C Table4-28: nominal5.1 kΩ Rd tolerance depends on whether power capability is detected; total equivalent resistance includes internal paths. Table4-3 and §4.5.2.2.5.2 require leaving Attached.SNK within40 ms below the selected valid disconnect threshold (5 V scope: threshold within0.8–3.67 V). The chosen sensing circuit must establish margins and timing. |

For the U585 kit, CN1's TCPP03-M20, CC protection, VBUS divider and supply-select
jumper must be traced together. No source-role or charger-bypass configuration
is proposed. For the S3 kit, the two USB power paths and auto-programming
circuit must be reconciled with its v1.1 schematic before choosing how the
transport port is powered. Neither kit is assumed to satisfy suspend while
running the full display workload. On suspend/disconnect the application stops
new requests, invalidates pending consent and partial transport buffers, and
requires a new rendered review and fresh released-then-pressed consent after
reconnection. Exact low-power implementation and measured port current are H02
requirements.

The subsequent [U585 kit/boot review](u585-kit-usb-boot-review.md) establishes
the correct TCPP03 seven-bit address0x34 and mode-dependent FLGn/gate behavior.
Its native PDF/SchDoc/PCB check withdraws the apparent pin9/11 conflict. The
separate PF14 divider is an analog ADC4_IN5 path, while ADC4 remains excluded
from the present manifest; a complete sensing/CC/EN/reset policy is still needed.
The [subsequent I2C/CC review](u585-i2c-ucpd-review.md) specifies the counted,
bounded control requirements and checks the candidate source. Its deadline,
early-STOP and recovery gaps prevent selecting the stock adapter as that policy.
UCPD sink trimming and configuration lifetime are revision-specific; source,
PD, FRS, VCONN and DMA remain excluded proposals.

## Controller and software boundary still being closed

The existing TinyUSB source review found unbounded core-reset/FIFO-flush loops,
including loops reached from interrupt context. A task-level timeout cannot
preempt those loops. The proposed CPU-FIFO path excludes controller DMA, but
that requires the actual core/master reset configuration, not merely
`CFG_TUD_DWC2_DMA=0`. S3 TRM1.8 §32.5 p1242 reserves the comprehensive register
description for an NDA supplement. Public software can show its configuration;
it cannot supply missing normative master or FIFO semantics. This remains an
explicit S3 documentary dependency wherever the chosen path needs those
semantics. U585's public RM must be used to complete its own device path;
similar IP naming does not transfer normative guarantees between chips.

Actual new reading: Type-C2.5 pp153,180–184,198–201,210–212,218–219,224–232,
243–246,251–252 (selected body, not visual review of every figure). USB2 base
physical pp198–207 / printed170–179, with unrelated hub context encountered;
Device Capacitance and Suspend Current ECNs complete; VBUS Max Limit ECN
complete; Connect Timing ECN complete extracted text, with the redline caveat
above. Remaining applicable electrical/reset/control-transfer/descriptor
clauses and errata are not claimed read by this checkpoint.
