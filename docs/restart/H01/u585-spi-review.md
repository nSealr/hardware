# U585 SPI display-path correspondence

Author `/root/h01_sol`, 20 October 2026; selected-source continuation from
`c90dcbc`. No display/module/controller, wiring or driver is admitted. This
advances the SPI1 part of [the U585 manifest](u585-peripheral-manifest.json),
without completing the host's interface row or selecting a panel.

## Current hardware contract

RM0456 Rev7 §68.3 Table696 p2903 gives SPI1 a16-byte FIFO and configurable
4–32-bit frames. SPI3 is a different, limited instance; its limits are not
interchangeable. The current paper proposal can use SPI1 as a single controller,
simplex transmitter, 8-bit MSB-first frames, software-controlled display CS,
no receive pin, no CRC/DMA/RDY/autonomous trigger. The exact clock phase and
frequency remain tied to the eventual panel's actual controller/electrical
specification. PE12 is GPIO for software CS; its possible SPI1 NSS AF does not
make it a hardware-selected output in this proposal.

The following is a source-backed design contract, not a firmware write recipe:

| Control | Proposed requirement |
| --- | --- |
| `SPI_CFG1` | `DSIZE=7` (8 bits), `FTHLV=0` (one frame), `CRCEN=0`, `TXDMAEN=RXDMAEN=0`. Preserve the reset CRC-size value7 even though receive/CRC is excluded. Pick a real supported prescaler; its resulting SCK must satisfy the panel. |
| `SPI_CFG2` | `MASTER=1`, `COMM=01` (simplex TX), `SP=000` (Motorola), `LSBFRST=0`, `IOSWP=0`, `RDIOM=0`. Bind SSM/SSI/internal NSS to the selected inactive polarity; configure CS separately as GPIO. `AFCNTR` must have an explicit pad-idle policy. |
| `SPI_AUTOCR` | Keep `TRIGEN=0`; no DMA/EXTI/timer-triggered start. GPIO and RCC exclusions still apply. |
| Transfer bounds | For the finite-count alternative, use nonzero `TSIZE` within SPI1's16-bit count and exactly match software writes. Zero-length writes perform no transfer. Large display writes need bounded chunks consistent with complete panel pixels/commands. |
| FIFO access | With an8-bit single-frame threshold, use byte writes and recheck `TXP` per byte. Larger packed accesses require a separately matched threshold and accounting. A ready flag does not authorize arbitrary-width writes. |
| Completion | Track software byte count and a fresh transfer; `TXP` means space and `TXTF` means all data were submitted. They do not mean the last bit reached the wire. For nonzero `TSIZE`, use EOT/TXC completion with a deadline, then preserve required final SCK/data/CS hold before disabling or changing pins. |
| Errors and abort | Poll MODF during waits, keep interrupts disabled for this polling proposal, and invalidate the whole pending render/request/consent on any fault or deadline. Forced abort can truncate a frame and is failure, never successful screen completion. |

Manual §§68.4.10–68.4.14 pp2918–2926 explain startup, data flow and mandatory
disable handling. Clearing `SPE` while active can truncate a frame and loses
FIFO contents. In the finite-count case EOT/TXC still does not authorize an
immediate disable: ES0499 Rev12 §2.23.7 p37 requires delay and/or a reduced
PCLK/SCK ratio to avoid truncating the last output pulse. The manual also
requires sufficient last-bit hold time (§68.4.13 p2925). Neither source gives
a universal numeric delay covering an unselected panel. That value remains an
explicit configuration/calculation and H02 timing gate.

`SPI_CR1.IOLOCK` locks CFG2 only and is cleared whenever `SPE` changes1→0,
including hardware disable. It is not a persistent lock across the recommended
disable/re-enable transaction sequence. GPIO configuration locks, GTZC ownership
and this transient SPI lock have different scopes. No lock stops arbitrary
code already running in the trusted secure privileged image.

ES0499 §§2.23.1–2.23.7 pp35–37 were reread with the current body. The existing
ledger keeps the revision/configuration limits: poll MODF because its interrupt
can be blocked; the receive CRC-size issue is avoided only by retaining its
specified setting; the extra slave/RDY/multimaster/autonomous conditions are
excluded here, with their actual enable controls clear. RevisionU does not
remove the applicable completion/mode-fault conditions.

## Exact software source and differences

The already pinned Embassy STM32 Cargo file at commit
`69006a4158aa6d605ad8506ade0f2f79159131e3` depends on generated-data tag
`stm32-data-37a22f31552ba1fd29b3ef192c4578b84abee6e1`. That annotated tag was
resolved to object `2fa06fc0f7223a4b5d193e43972cc10dcb6ee49c`, then generated
commit `b99bf17d58e6a8d385faf4b87b5f310ca2c057a0`. Its exact STM32U585VI SPI1
metadata identifies `spi` version`v6`, PCLK2, CCIPR1.SPI1SEL and the APB2
SPI1 clock/reset fields; its PE13/PE15 AF5 entries correspond to the proposed
signals. This is software metadata correspondence, not package-electrical
evidence or an actual build. The inspected build-script lines1–89 turn the
selected peripheral kind/version into `spi_v6` conditional compilation.

The exact candidate `spi/mod.rs` enhanced-instance branch differs from the
finite/simplex proposal:

* `new_blocking_txonly` omits the MISO pin and DMA handles, but shared
  initialization still chooses full-duplex operation and `TSIZE=0`.
* It uses an all-ones IFCR write, including fields the current manual reserves.
  The current register contract requires named valid clear bits.
* `blocking_write` cycles SPE, drains RX, writes the caller's slice and waits
  on TXC. Its per-word ready wait, RX flush and final TXC wait have no deadline.
  Write-only operation intentionally ignores receive overrun in its shared
  full-duplex path; it is not the same configuration as `COMM=01`.
* The embedded-hal `flush` method returns immediately; actual completion is
  handled inside the write path. Drop only disables the RCC clock and is not
  an explicit peripheral abort, pad/CS hold or secret-erasure procedure.
* Its baud selection may choose a result above a requested frequency when the
  ratio is between supported dividers. Use the actual kernel/divider result,
  not the requested API value, as the panel timing bound.

The continuous-transfer (`TSIZE=0`) driver does not exercise the finite-count
EOT condition in the same way. Do not mechanically attach that erratum to its
different completion path. It still needs its own bounded stop/error/hold
correspondence, initial internal-NSS validation and source-to-build review.
The code source is not a qualified adapter and no upstream bug report or
hardware failure is asserted by these differences.

## Preserved source discrepancy and outcome

The SPI_SR introduction p2943 says flags require explicit IFCR clearing and
do not clear automatically on re-enable. Several per-flag definitions on
pp2944–2945 say that CRCE/OVR/UDR/EOT clear on re-enable, and EOT's prose itself
mixes re-enable with transfer completion. Preserve that discrepancy. The
proposal explicitly clears only documented valid flags, verifies fresh state
and tracks its transfer count; it does not rely on a stale flag or an automatic
clear assumption. Exact driver/state-machine correspondence remains required.

The current source supports a bounded CPU-SPI adapter proposal, but the
unmodified candidate Rust API does not establish the proposed finite/simplex
configuration or its deadlines. A narrow reviewed adapter, or a fully specified
continuous-transfer alternative, remains necessary before selection. A failed
or interrupted display write never grants local consent; the whole screen must
be rendered and bound to the operation before a fresh press is accepted.

Fresh extracted-text reading: RM0456 pp2903–2927, p2928 before §68.5,
pp2929–2931, pp2933–2947 and p2948 before §68.8.11. Encountered functional
tables were read; diagrams were text-extracted, not visually reviewed. CRC
algorithm/TI-mode bodies and unused register-map summaries are outside this
selection. ES0499 §2.23 body pp35–37 and applicability Table3 p5 were reread.
Fresh source reading: `spi/mod.rs` selected lines1–116,150–265,366–550,
790–868,955–1035,1895–1935,2020–2175,2260–2400; build.rs lines1–89;
Cargo.toml dependency lines219–224 and the STM32U585VI SPI1 metadata object.
The other SPI async/DMA/slave algorithms and remaining generated chip metadata
are unread. No target build, physical test, full driver review or source-wide
license audit occurred. Original hashes/URLs and reading scopes are registered.
