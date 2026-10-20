# U585 generic EP0/bulk source contract and OUT blocker

This finishes finite C06 endpoint/control reading and triage. It does **not**
close the unsatisfied OUT semantic property or admit USB enumeration, a class,
driver or host configuration. The coordinator explicitly requires the64/68
conflict below to remain a blocker, not a supported conditional transfer mode.
The [earlier source review](u585-otg-source-review.md),
[clock tuple](u585-clock-proposal.json), [memory limits](memory-ownership-contract.md)
and [USB power boundary](usb-configuration.md) remain applicable.

## Unsatisfied source property

Native RM0456 Rev7 p3269 requires non-isochronous OUT
`XFRSIZ=n×(MPS+4−(MPS mod4))`, `PKTCNT=n`. For MPS64/n1 this yields68.
Page3270 says completion requires XFRSIZ0 and PKTCNT0, or a short packet;
pp3228–3229 define byte XFRSIZ and packet count. A full64-byte packet with
initial68 leaves4 by the described decrement. Pinned Embassy69006a4 instead
arms MPS×packets, hence64/1. Neither choice is qualified by substituting vendor
code for the model, rounding the formula differently or assuming an early
completion. This reading does not establish that either host is impossible.

**H02 STOP:** no enumeration/operation that assumes this OUT semantic until a
corrected applicable manufacturer source or evaluated diagnostic evidence
resolves it. Any dedicated diagnostic discrimination needs a separately reviewed
finite procedure, identified bench, public data only, actual buffer/FIFO bounds,
abort/interrupt/counter policy and success/refusal criteria. It is not a normal
probe using an assumed conformant driver. No64/68 choice, experiment, new class,
driver or IP lead is authorized here. The relevant H01 interface criterion
remains unsatisfied even though its finite source reading/triage is complete.

## Bounded controller requirements

| Boundary | Source-backed requirement / explicit proposed cap |
| --- | --- |
| Endpoint schema | Generic EP0 IN/OUT MPS64 and one bulk pair EP1 IN0x81/OUT0x01 MPS64; all other slots inactive/masked. This is not CDC or Bridge compatibility. Class/subclass/protocol, VID/PID/release/string identity are **unselected**. H02 chooses a lawful identity and reads its class requirements before enumeration; T01 cannot infer an implemented transport. |
| FIFO budget | Proposed Rx96 words at0, EP0 Tx16 at96, EP1 Tx16 at112:128 of320 words,192 unallocated. RM3155–3156 requires13 SETUP locations, one global-NAK location and data/status/OUT-completion space; the proposal exceeds both its two-active-OUT formula35 and two-max-packet engineering allowance52. Each active IN has its own FIFO and at least one64-byte packet. This is static arithmetic, not measured service margin. |
| OUT storage | A received packet is never a complete application frame or consent. Check fresh RXFLVL before each status pop; endpoint, packet-status, BCNT≤64, destination remaining and complete software count before any slice/copy. Stage storage is at least68 bytes to avoid making the disputed formula an undersized-buffer assumption, but do **not** program/qualify either transfer size from that allocation. C05's total4 KiB USB bound still applies. SNPM0; no snoop/iso/DMA mode. |
| EP0 setup | Eight-byte SETUP, at most three saved slots/24 bytes; a newer valid SETUP supersedes the incomplete control transaction. Global OUT NAK and EP0 STALL do not stop SETUP ACKs. Validate every field, recipient, state and exact length; no append-only setup queue, secret control command or approval. |
| Standard responses | Return at most min(actual descriptor/response length,wLength), with correct short/ZLP termination. Device/configuration descriptors and class details must be complete and fixed before enumeration. Proposed generic control-response cap256 bytes, packet staging64, within C05; a chosen class that exceeds it requires an explicit revised bound. Optional strings may be absent only with zero reference fields. FS USB2 uses bcdUSB0200 per2002 erratum and rejects unsupported device-qualifier/other-speed requests. |
| Request states | Implement the exact Default/Address/Configured rules for GET_DESCRIPTOR/GET_CONFIGURATION/GET_INTERFACE/GET_STATUS, SET_ADDRESS/SET_CONFIGURATION and endpoint halt. Unsupported/malformed/state-inappropriate requests STALL in Data/Status; no permanent EP0 halt. A new SETUP recovers protocol STALL. SET_DESCRIPTOR, remote wake, TEST_MODE and SYNCH_FRAME are not features of this generic FS proposal. |
| Halt/toggle | Bulk halt/status is real state, not a successful flag. ClearFeature(ENDPOINT_HALT) resets DATA0 even if already unhalted; configuration/interface reset does too. For the single default alternate, SET_INTERFACE may STALL as allowed. Do not infer authority from a host-issued feature/configuration command. |
| Address timing | SET_ADDRESS must use the old address through successful status, then accept the new address after its2 ms recovery; complete status within50 ms. The pinned helper writes DAD before `accept`, with a hardware-order comment, and `accept` discards endpoint errors. Its on-wire delayed-address correspondence is **unproven**, not an observed defect. Require an exact applicable hardware explanation and a fallible completion path before use. |
| Other control timing | USB9.2.6 requires no-data standard status≤50 ms, first/subsequent IN data≤500 ms and final status≤50 ms; host-caused delay is distinct. Proposed adapter deadline40 ms for its own active standard-request work, control response≤256 bytes, then bounded refusal/disconnect. This is an engineering cap, not guaranteed normal latency. No five-second nested call or retry chain escapes the absolute budget. |
| Reset/resume recovery | The host grants10 ms recovery after reset/resume; the device must be ready for data at its end. This is distinct from the controller's force-device25 ms initialization wait, the ≥3-PHY-cycle synchronization guard and the2 ms SET_ADDRESS recovery. Clock/reference/state requalification must fit the actual transition before claiming readiness. |
| IN completion | One packet per arm, PKTCNT1; payload0–64 and all bytes in one bounded buffer. Nonzero writes require room for the entire packet in DTXFSTS, counted in32-bit words; ZLP does not require FIFO data space. API enqueue/copy return is not USB completion. XFRC indicates completion on AHB and USB; remaining fields are read only after EPENA clears. Host starvation/timeouts cancel the transfer/epoch rather than rerun signing. |
| IN errata | ES0499Rev12§2.25.2 requires one packet per transfer and no interleaved CSR access during the protected packet push. §2.25.3 applies to every ZLP: SNAK1/CNAK0, wait20 AHB cycles, EPENA1, wait15, CNAK1/SNAK0. With qualified C03 clocks, separate minimum1 µs guards exceed20/15 cycles at45–51 MHz; not a measured waveform. Stock simultaneous CNAK/EPENA does not implement this. |
| Reset/disable | Assert SDIS and invalidate parser/consent/partial input/result first. Stop writes, establish NAK-effective, disable only enabled endpoints, wait EPDISD and then quiescent flush; EP0 OUT cannot be disabled through EPDIS. CSRST retains SDIS/GCCFG/clock fields, requires completion,≥3 PHY cycles and idle check. One minimum1 µs guard is proposed only under qualified clocks. Repeat full application/endpoint initialization; reset/flush is not secret erasure. |
| Finite service | Proposed IRQ/service invocation≤4 status pops/256 payload bytes and≤200 µs, whichever arrives first. Mask/defer the level source and continue within a separate≤1 ms service interval, or fault/disconnect if the budget cannot be met; never drain a hostile continuously nonempty FIFO indefinitely. Do not flush/wait10 ms inside an IRQ or mask the clock supplying its deadline. These are qualification limits, not a guaranteed host bandwidth/latency. Bulk has no service-time guarantee. |
| Recovery | One total20 ms quiescence/disable/flush budget, each Rx flush under10 ms and at most one retry as RM3268 specifies. Failure propagates to disconnected/unqualified state; warning-and-continue is forbidden. Proposed SDIS hold≥2 ms covers the documented suspended minimum1 ms+2.5 µs only with qualified time. No host receipt, physical unplug, application clearing or restored authority is inferred from it. |

## Interrupt acknowledgement and exact exclusions

[u585-usb-proposal.json](u585-usb-proposal.json) records defined W1C bit sets and
separate proposed interrupt masks. Write only captured applicable W1C bits,
never all ones or a status-register RMW. RO FIFO levels clear by servicing the
FIFO. IEPINT/OEPINT summarize DAINT and the corresponding DIEPINT/DOEPINT;
acknowledge the actual endpoint source. DAINT/DAINTMSK use EP0/1 only.
INEPNE/GINAKEFF/GONAKEFF require the documented CNAK/clear-global commands;
their observation does not itself prove a NAK went on the bus.

TXFE is a level and stays masked in the proposed whole-packet polling path.
ITTXFE/OTEPDIS are additionally used during the specific
EP0 overrun phase prescribed by RM3282. Babble, timeout, unexpected role/speed,
source inconsistency or budget exhaustion invalidates the whole epoch. Reset,
suspend/resume and EERR require fresh authority; EERR permits only soft-disconnect
recovery. No isochronous, host-only or LPM status is promoted into a feature.

DOEPMSK defines OUTPKTERRM bit8 while DOEPINT explicitly reserves bit8; do not
enable it or invent a corresponding error flag. CIDSCHGM stays masked in this
forced-device/no-ID proposal. Preserve ES§2.25.4's hidden GOTGINT bit20 and
two-register/“single-write” mismatch, and §2.25.5's CURMOD naming/polarity mismatch
against RM CMOD. These are not guessed register repairs or completed handler
proofs. Any later dependency on those ambiguous semantics needs resolution.

ES§2.25.2's description compares a packet count with MPS bytes, and its device
workaround's literal XFRSIZ=MPS equality does not express a short packet.
Preserve that wording: the proposed single-packet/noninterleaved-push rule is a
conservative requirement, not a correction of the source or proof that every
short/EP0 path is qualified. Applicable source correspondence remains necessary
before dependent use, along with the explicit OUT and address-timing gates.

## TCPP-only control allocation

The finite proposed kit arrangement uses **Hibernate**, EN/PB5 at its valid3.3 V
logic level and rise<50 µs, provider/VCONN/discharges off, consumer gate open.
Register0 proposal0x08 means GDC1/GDP0/PM00; read register1 acknowledgement0x08
and register2 identification/status through seven-bit address0x34. EN low is
OFF/reset/I2C-inactive, not a readable zero status; startup/reset can leave PB5
floating because the native kit has no external pull-down. Do not assume that
MCU reset alone clears TCPP or makes powered-off I/O safe.

Accept VBUS_OK bit5 only with fresh successful counted I2C, correct identity,
mode/gate readback, valid EN/supplies and no reported fault. Its1.9–2.9 V UVLO
range is a voltage-presence threshold, not proof of physical unplug or an
upper-voltage/current contract. Proposed poll interval≤10 ms, complete readback/
status transaction group≤2 ms, and SDIS/BVAL-invalid action≤1 ms yield≤13 ms
normal-software reaction; failure/stale/unknown immediately refuses attachment
and invalidates authority. C03/C09 must still bind default/reset/clock-loss,
independent failure, rail and whole-port current/capacitance/backfeed behavior.

UCPD and ADC4 remain excluded; no normal-mode Rd handoff, PD or automatic fault
recovery is selected. The stock I2C/USB adapters and forced-true BVAL defaults
remain nonconformant with this explicit status-validity policy. A live bounded
adapter must reflect status loss in actual pull-up disconnection, not merely
cancel a task. The final permissible supply/attach arrangement remains C09.

Actual exact source scopes, native register/formula renders and originals are
recorded in [manual-register.json](manual-register.json); originals stay private.
No firmware, helper, diagnostic, enumeration, register write or physical test ran.


C09 now records valid EN level/rise and autonomous VBUS-off data removal as
**unsatisfied mandatory properties** in power-attach-lifetime-contract.md.
Hibernate0x08 opens the consumer switch and cannot be assumed to power the kit
through JP4[5–6]. Its normal13 ms status proposal does not qualify reset/clock-
loss/absent-owner pull-up removal. These stops are independent of OUT64/68;
no enumeration, connection, external-fixture expansion or USB admission follows.
