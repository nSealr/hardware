# U585 OTG device path: selected source correspondence

Author `/root/h01_sol`, 20 October 2026, from `b773eb6`. This advances the
same U585 host proposal, without selecting a USB driver, sensing arrangement
or complete configuration. Host/OTG role negotiation, USB PD, charging detection,
LPM, remote wake, isochronous operation and controller DMA remain excluded.

## Current U585 controller contract

RM0456 Rev7 chapter72 applies to U575/U585. Its functional description uses
CPU32-bit FIFO push/pop accesses through the AHB peripheral interface and
1.25KiB of dedicated FIFO RAM. There are six endpoint slots in each direction,
including EP0; the candidate wrapper's320 FIFO words and six slots correspond
to these selected facts. GAHBCFG bits6:1 are reserved: the HS controller's
DMA-enable field is not an available U585 OTG_FS configuration. Generic
AHB-master wording in GRSTCTL is not evidence of an arbitrary SRAM DMA path.
The reviewed U585 memory-master manifest and its exclusions still apply.

Both the48MHz USB domain and valid AHB clock are required before setup; the
functional text requires AHB above14.2MHz and TRDT follows its actual frequency.
FDMOD forces device role, with a documented wait of at least25ms. HNP/SRP
stay disabled. Mode mismatch and unexpected role changes are failures; host
registers cannot be accessed as device registers. Software clock labels alone
do not establish frequency accuracy, USB supply readiness or current draw.

Masking GAHBCFG.GINTMSK suppresses the interrupt line, not status updates.
FIFO status is read-only and follows actual FIFO accesses; other events have
their specific write-one-to-clear rules. A receive-status pop is allowed only
while RXFLVL is asserted. Its BCNT is eleven bits and EPNUM four bits: validate
both against allocated endpoints and buffer capacity before constructing a
slice or copying data. A legal bulk maximum packet is not a substitute for that
software bound under a peripheral/status fault. No observed malformed-packet
acceptance or memory vulnerability is asserted here.

FIFO allocation must include SETUP/status/NAK space, each enabled IN endpoint,
and the complete OUT/control allocation within320 words. A packet in the FIFO
does not constitute a complete application frame or consent. Bad-CRC OUT
packets are automatically discarded in the reviewed non-isochronous path;
retransmission PID handling avoids duplicate delivery. Global OUT NAK still
admits SETUP packets. More than three back-to-back SETUP packets are possible;
the last successfully received setup must be handled. Interrupt work therefore
needs an explicit service/fault budget, beyond nominal full-speed throughput.

Reset, flush, endpoint disable and power removal are distinct operations.
GRSTCTL.CSRST has retained fields, requires completion, three PHY-clock
synchronization and idle checking. FIFO flush requires documented quiescence
before starting, then successful completion before further operations. The
OUT-stop model p3268 gives an explicit Rx-flush timeout under10ms and at most
one retry; it does not authorize an unlimited loop or continuing after failure.
Actual endpoint disable requires NAK-effective and disabled-state completion.
No such operation by itself establishes software-buffer/secret erasure.

The remaining endpoint register/model body, control requests, bounds, IN/error
completion, exact interrupts/time base and full normative USB correspondence
remain to be read and bound. In particular, the p3269 word-alignment expression
has not been adopted as a qualified transfer/buffer tuple; its correspondence
with the actual endpoint fields and driver remains open.

## Exact Rust driver and its limits

The already examined Embassy STM32 Cargo file at commit
`69006a4158aa6d605ad8506ade0f2f79159131e3` declares the path dependency
`embassy-usb-synopsys-otg0.4.0`. The same immutable commit supplied the STM32
USB wrapper, common setup, dependency manifest and selected device implementation.
This is source correspondence, not a resolved nSealr build or chosen adapter.

The wrapper configures the internal FS PHY, six slots and320 words; its
30-word extra Rx allowance is explicitly described by upstream as empirical.
It is not a measured nSealr throughput or normative sizing proof. The following
differences still prevent selection:

| Path | Actual selected source and required consequence |
| --- | --- |
| Supply/initialization | The U5 common path sets the USB supply-valid/monitor controls and waits for VDDUSBRDY without a deadline. Wrapper AHB-idle and forced-device CMOD waits also have no deadline; CMOD polling does not implement the specified minimum25ms delay. Bound every actual selected wait and clock transition. |
| Optional handshake limit | Flush/abort helpers use10ms only with the USB dependency's own `embassy-time` feature. Without it they loop indefinitely. `embassy-stm32/time` enables STM32 time helpers but does not forward this separate dependency feature. A live backend and effective feature graph are required. |
| Failure result | Those helpers warn on timeout and continue; they do not propagate a failed quiescence/flush/disable result to stop the connection. A finite local wait alone is not successful recovery. Multiple per-helper/per-endpoint limits are not one overall deadline. |
| Interrupt context | SETUP processing can call the Tx-flush helper in the IRQ. Rx drains while RXFLVL stays asserted. Verify an actual IRQ/service bound and timer progress during critical sections; an outer task timeout cannot preempt a synchronous loop. |
| Buffer bounds | Ordinary OUT IRQ copying constructs a raw slice with reported BCNT and trusts the peripheral not to exceed MPSIZ; its endpoint number is asserted. The proposed adapter requires checked capacity/packet/count validation and an explicit fault path before unsafe construction, rather than an unproved hardware-length assumption. |
| Status clear masks | Initialization writes all ones to GINTSTS. The selected current device W1C and reserved fields need an exact valid clear mask; a generic all-bits write is not that proof. |
| API completion | IN `write` waits for prior activity/FIFO space, starts a transfer and copies data; its return does not mean the host received or acknowledged the new packet. Application framing, response completion, cancellation and local-consent lifetime need separate policy. |

The selected reset path in the STM32 wrapper is RCC reset through common
setup. Do not conflate it with the dependency's public `core_soft_reset`
method: that separate method also has unbounded idle/reset loops, but no call
to it was found in the inspected wrapper device path. Its existence alone is
not proof that the wrapper executes a CSRST sequence.

The source positively discards saved SETUP/OUT buffer state during its bus-reset
configuration, wakes endpoint futures as disabled and resets the USB address.
That is useful session separation; it does not clear application consent,
message parsers, secrets or every allocated byte. Current application policy
must invalidate all of those pending operations on reset/suspend/failure.

## Errata and VBUS are still hard requirements

ES0499 Rev12 §2.25.3 p39 applies across X/W/U. Every zero-length IN transfer
requires the documented SNAK/CNAK sequence with20 and15 AHB-cycle delays
around endpoint enable. The pinned `start_in_transfer` sets CNAK and EPENA
together for zero-length transfers too; control `accept` uses such a ZLP.
The required workaround is not established by that path. This is a source
configuration mismatch, not a reproduced hardware failure or upstream bug claim.

For §2.25.2 the one-packet `write` path and protected FIFO copy provide useful
correspondence. The multipacket API and its exact scheduling still need review
against the complete applicable erratum and current registers. The software
comment describing an erratum does not itself sign that whole correspondence.
The existing hidden-interrupt two-register/single-write text discrepancy and
false CIDSCHG handling remain in the ledger; host-only errata are not silently
attached to the device proposal.

RM0456 p3187 gives a writable CID with reset value0x3000. This selects the
wrapper's `config_v2v3` branch under that reset state; it is not immutable
received-silicon attestation. That branch forces B-session valid true whenever
hardware VBUS detection is off, including when the generic configuration's
software-override flag is requested. The default has both VBUS options off.
Neither behavior implements the kit's unresolved PF14 analog/TCPP sensing
policy, and a second kit supply means “VBUS absent implies MCU off” is not an
acceptable assumption. VBUS status, bus reset and physical plug presence are
different claims. No security or connection-policy downgrade is selected.

## Actual reading

Fresh RM text pp3133–3134,3138–3140,3142–3144,3150–3153,3155–3158,
3168–3169,3179–3182,3186–3187 and3267–3271; current pp3170–3175 reread.
Adjacent host/isochronous text was encountered, without admitting those modes
or reviewing their whole algorithms. Tables and extracted figure text were read;
no new native OTG diagram or bit-layout visual review is claimed. The earlier
selected pp3135–3137,3164,3238–3240,3261–3266 remain inherited at their stated
scope. ES0499 §2.25 body pp38–40 and applicability Table3p5 reread.

Fresh source reading: STM32 `usb/otg.rs` lines1–99,273–490,540–640;
`usb/mod.rs` and USB dependency Cargo.toml complete; STM32 Cargo dependency
lines170–171 and time/features lines320–376. Dependency `src/lib.rs` selected
lines1–226,541–588,815–1055,1068–1235,1240–1545,1620–1675,1870–1950,
2010–2143,2195–2245. Remaining allocation/transfer/host bodies and generated
OTG register source are not claimed completely reviewed. No effective build,
driver modification, test, physical operation or completed host row occurred.
