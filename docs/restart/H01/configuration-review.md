# H01 concrete configuration review

Ongoing author work after the exact `e39015a` review; this is not host admission
or a replacement for the six-row completion gate. The imported review is in
`independent-review-current-manual/`; CM-1 was corrected separately in `90aa59d`.
All identities here are **proposals for documentary analysis**. H02 must identify
received hardware before execution. No kit ownership, fuse change, wiring,
measurement or production firmware is implied.

The 20 October [resumed source increment](resume-source-notes.md) adds current
cache/GPIO/watchdog reading and the native kit startup/power branch findings.
It supersedes the older unread-cache/watchdog scope statements below only for
the exact newly recorded sections. The proposed configurations remain unsigned.

The subsequent [U585 initialization contract](u585-initialization.md) and
[field manifest](u585-peripheral-manifest.json) add the current MPCBB/TZSC lock
and RCC reset/clock correspondence. They account for the real U585 DMA2D master
and distinguish OTG fields from the USB fields reserved on that device. Final
clock values, fault/interrupt masks and selected driver paths remain open.

The later [S3 clock/time correspondence](s3-clock-time-review.md) makes a fixed
CPU160/APB80/PLL480 and separate SYSTIMER UNIT1 polling proposal explicit.
It records unbounded PLL/snapshot loops and required finite remedies, rather
than qualifying stock startup. The [calculation tuple](s3-clock-proposal.json)
keeps reference/PHY and effective-feature conditions unsatisfied; no actual
clock or completed time/host contract is inferred.

[Two-host entropy/crypto correspondence](entropy-contract-review.md) now fixes
the finite all-or-error adapter table, exact U585 manufacturer-reference
conditions and S3 non-RF SAR ownership. U585's coordinator-approved conditional
documentary allocation has a strict H02 stop before entropy-dependent use;
no nominal clock, output statistic, certificate label or successful API call
admits random output. Actual provider/source/backend and binary qualification
remain separate from this completed conditional source table.

The [two-host memory/ownership contract](memory-ownership-contract.md) now binds
fixed internal address partitions, aggregate copies/stacks/queues and separate
public/private row buffers. Its [allocation](memory-ownership-proposal.json)
contains unmeasured qualification caps, no alias double count or claimed free
heap. U585 global HAL init is not an exclusion proof; S3 locks reset with the
CPU, and a trusted World0 image can still read all its data. Effective source/
feature/linker correspondence, complete-workload fit and clearing remain H02
gates; no host row or hostile-app isolation is accepted here.

The same-kit [S3 USB Serial/JTAG source assessment](s3-usb-serial-assessment.md)
examines a fixed CDC alternative under the existing host scope. It is not
selected: stock receive-loss/reset/error, console ownership and lifecycle
behavior still need a bounded adapter and exact configuration. OTG's earlier
NDA boundary is retained; no controller substitution or USB-row signoff occurs.

The later [S3 fixed-CDC contract](s3-usj-contract.md) finishes selected public
IRQ/header and security-helper correspondence, including the different scopes
of JTAG, whole CDC and shared write locks. Its finite stream/reset/writer
requirements remain unimplemented. Clock, descriptor/current and the exact
attach/suspend arrangement still prevent selection. One conditional external
J4 attach-fixture assessment is now within scope. Its later
[conditional contract](s3-attach-contract.md) reserves GPIO8/J1.12 for real
VBUS-valid status and specifies autonomous isolation/defaults. No parts or
implementation are selected or authorized for connection, and fixed-descriptor
source/status correspondence can still reject its self-powered route.

[U585 SPI correspondence](u585-spi-review.md) now adds selected current
functional/register body and errata reading, with the pinned enhanced-SPI
driver and exact U585VI metadata. Completion/hold, transient IOLOCK, flag-clear
wording and unbounded driver waits remain explicit adapter/configuration gates.

The [finite U585 EP0/bulk table](u585-usb-endpoint-contract.md) completes the
selected endpoint/control/IN/error reading and records exact FIFO/IRQ/control
bounds and the TCPP-only mode/readback proposal. The native OUT64/68 conflict
is an **unsatisfied source-semantic blocker**, with neither transfer mode
qualified and no dependent enumeration/normal probe admitted. Class/VID/PID
remain unselected; H02 lawful identity/class-source review and any separately
reviewed diagnostic procedure are explicit gates. This triage does not close
the unsatisfied H01 interface criterion.

The [S3 SPI/input table](s3-spi-input-contract.md) now fixes the selected
CPU64-byte path, bit-order/phase/CS requirements, padded short-tail backing,
finite polling/abort remedies and six-contact change-latch/debounce proposal.
The [allocation](s3-spi-input-proposal.json) leaves clock/reference, effective
binary/IRQ, pin/rail and display conditions unqualified; fixed CDC and both
power arrangements remain unselected. No received kit is inferred from the
maintainer's separate inventory or from a source header mapping.

## Scope and identities

The two comparable workloads use CPU-driven SPI graphics, six physical controls,
USB full-speed device transport, internal secret memory and the accepted S02
maintained software crypto candidate. Camera, touch, NFC, USB host/PD/source,
external-memory secrets and crypto accelerators are outside this proposed subset.
Their exclusion still needs reset/clock/master evidence, not merely absent APIs.
The generic Board SDK remains independent of Nostr; this workload does not freeze
the custom Board or merge the four Signer profiles.

| Identity | Proposed documentary target | Boundary |
| --- | --- | --- |
| U585 custom-package witness | STM32U585VIT6Q, LQFP100, SMPS option, silicon U / REV_ID `0x3007` | Exact DS13086 pad/AF/electrical reconciliation remains in progress. Revision U is not a blanket errata fix. |
| U585 kit witness | B-U585I-IOT02A, MB1551-U585AI-D01; schematic U13 STM32U585AII6QU, UFBGA169 | UM2839 Rev4 calls the target STM32U585AII6Q; schematic adds the `U` suffix. Received marking/REV_ID must match the allowed revision; board ordering alone does not establish it. BGA pads are not LQFP100 pad numbers. |
| S3 kit/module witness | ESP32-S3-DevKitC-1-N8R8 PCB v1.1, ESP32-S3-WROOM-1-N8R8 | Official current guide links the schematic dated 2022-11-30, SHA256 `f116b5d9f1fdce126e9a63d8450388eb11295d8322d831502fbc9729442b72e4`. The older 2022-04-13 file is not silently substituted. Module suffix does not establish received silicon revision. |

The U585 kit has many permanently connected peripherals. Its I2C2 bus is shared
with sensors and the TCPP03-M20 port protection; it is not a private selected-SE
bus. Its external STSAFE is not an H01 custody backend. UM2839 §7.9.7 identifies
PF11 as its enable/shutdown control, but this is not yet an electrical shutdown
proof. Unused radios, memories, sensor interrupts and STMod mux branches still
need their schematic reset/load analysis before signing the kit configuration.

UM2839 §7.2 p16 calls the Type-C connector CN14, while §7.5 pp20–21 and the
schematic identify CN1; CN14 is an Arduino header. The proposal uses CN1 and
retains this documentation discrepancy. The board's nominal 500 mA current limit
is not USB permission to draw 500 mA before configuration.

## Concrete UI wiring witness, still under electrical review

UM2839 Table24 p33 and native schematic MB1551-D01 sheet8 agree on this U585
allocation. Sheet8 was visually inspected; this is connector-to-net evidence,
not an assembled continuity test. All controls are external normally-open dry
contacts to target ground, with a proposed 10 kΩ pull-up to the target I/O supply.
They are not boot/reset buttons. Shared grounds, powered-off injection and
connector orientation must be checked in H02 before energizing a fixture.

| Function | U585 kit net / header | S3 v1.1 net / header |
| --- | --- | --- |
| SPI clock | PE13, CN13.6 / D13 | GPIO12, J1.18 |
| SPI MOSI | PE15, CN13.4 / D11 | GPIO11, J1.17 |
| Display select | PE12, CN13.3 / D10 | GPIO10, J1.16 |
| Display data/command | PC1, CN13.1 / D8 | GPIO13, J1.19 |
| Display reset | PA8, CN13.2 / D9 | GPIO14, J1.20 |
| Backlight control | PB6, CN14.7 / D6 | GPIO9, J1.15 |
| Up / down / left / right | PC0/PC2/PA7/PB0, CN16.1/.2/.5/.6 | GPIO4/5/6/7, J1.4–7 |
| Local selection / separate consent | PE7 / PD15, CN14.5 / CN14.3 | GPIO17 / GPIO18, J1.10 / J1.11 |

The common U585 proposal corrects the earlier PC4/PC5 allocation: DS13086
Rev10 native Figure14 p99 shows that the proposed LQFP100 SMPS package does
**not** expose PC4/PC5. The p100 diagram is the non-SMPS package. PA7/PB0 on
CN16.5/.6 use the kit's documented default SB10/SB13 paths (SB11/SB12 absent),
subject to the still-incomplete branch/reset/electrical checks. This is a
paper-proposal correction, not wiring authorization or a continuity result.
See [pause-reading-notes.md](pause-reading-notes.md) for the preserved correction.

The S3 header mapping is directly read from the manufacturer's v1.1 guide;
both native schematic pages now visually agree. Module pads, reset states
and selected conflicts still require their exact-chip checks. GPIO35–37 are unavailable on N8R8 due to octal PSRAM. GPIO38
drives the v1.1 RGB LED; v1.0 instead uses GPIO48. Neither is allocated here.
GPIO19/20 remain USB D−/D+. Boot straps and UART auto-program pins are not controls.

On the U585 kit, PE13 also drives the Arduino LED through Q3/R48, and SPI1
branches to the STMod mux. These loads are real even with no shield attached;
the fixture must leave expansion connectors empty and evaluate the selected
mux state/load. Merely listing the pin AF cannot erase those branches.

The proposed input policy requires debounced release after boot, reset, USB
disconnect, timeout, screen fault or cancelled request before a fresh consent
press can be accepted. A held button is not a new authorization. The review
screen must be fully rendered and bound to the pending operation; any transport,
entropy, rendering or power failure invalidates that pending operation. Exact
debounce/timing limits and local recovery usability remain H02 measured gates.

## Display source contradiction and bounded alternative

The subsequent [existing Newhaven panel review](panel-subset-review.md) keeps
the raw DB/ILI9341V module distinct from the current AF/ST7789VI breakout.
The latter is deferred for the common four-wire/DC/backlight proposal.
The raw panel's selected command, mechanical and timing sources are now read,
but module startup/internal-power contradictions, normal rail margin and a
compatible default-off backlight/contact fixture remain open. The backlight
control row above is conditional; it is not a direct connection to LEDA/LEDK.
No panel, driver or complete screen/consent policy is admitted by that reading.

Waveshare SKU17344 was examined as the modest SPI lead. Its product page names
ST7789VW, its documentation names ST7789V, and the linked module drawing names
ST7789V2-G4. The board schematic (SHA256
`9d18b8eeec61bbc9294a075ce96fbf7bf4f800caebc73ca384b2de1cd36d2d00`)
directly joins external VCC, LCD VDD and LEDA: it shows no voltage regulator or
logic translator. The linked module specification §7.1 limits operation to
2.6–3.3 V. Therefore the product's generic 5 V claim is **not supported by this
document set**. No 5 V connection is admitted.

The schematic's J1 numbering is VCC/GND/DIN/SCK/CS/DC/RST/BL on pins1–8;
J2 reverses that numbering. Internal 12-contact display flex is a different
interface. Cable colour/order and an arbitrary FPC are not substitutes for this
mapping. The backlight transistor has a pull-up, so reset does not imply blanking.

One bounded alternative is Adafruit PID4311, EYESPI revision introduced in
February2023, source commit `9804ed3f84ab9b4547706bc13a467492435a60f4`.
Its actual Eagle schematic was read as XML and correlated with the native
revC image dated2023-02-20: AP2127K-3.3 regulator, 74HC4050D
buffer, reset supervisor, BSS138 backlight switch and microSD socket. The source
and guide do not justify assuming direct equivalence with Waveshare. Its linked
panel is QT020HLCG00, revision A, 2017-06-01, but that specification again names
ST7789V in the table and ST7789V2-G4 in the drawing. Exact controller-document
correspondence and worst-case rail margin still require resolution. Neither
module is selected or documentary-admitted by these observations.

No extra display market sweep or third host port follows from this. Remaining
questions are concrete: which controller revision is supplied in the proposed
module, which controller command/timing document applies, and how do the module's
regulator tolerance and I/O levels meet the actual panel's limits? The public
source contradictions are retained; no manufacturer message has been sent.

## Current U585 security, memory and lifecycle conclusions

The following are current RM0456 Rev7 requirements, replacing reliance on the
historical Rev6 excerpts. These are documentary requirements, not provisioning
instructions or claims about a running binary.

* **Reset is not an established security partition.** §§3.5.4–3.5.7 and
  §§5.4–5.6: with TZEN active the CPU/SAU, SRAM and GPIOs start secure, but
  securable peripherals and DMA channels start nonsecure; TZIC events start
  masked. SAU/MPU settings affect the CPU, not other masters. The initialization
  manifest must establish each used and excluded peripheral/channel's ownership
  before accepting USB input, lock the intended TZSC/MPCBB configuration, and
  enable the relevant illegal-access handling. Reserved device-specific bits
  must remain at reset values; a family-wide all-ones mask is invalid.
* **GPIO security alone is insufficient.** §3.5.5 Tables12–14 pp165–167 lists
  DAC, USB VBUS, UCPD, TAMP, RTC, PWR, RCC and EXTI functions which may affect or
  observe a secure pin. Their ownership must agree with the UI/consent allocation
  even if the associated application feature is unused. Privilege violations
  can silently return zero/ignore writes (§3.6.3); lack of an exception is not
  evidence that an access was permitted or a buffer contains valid data.
* **Exact SRAM budget.** §5.3 Table33 p199 and §6.3 Tables45–47: U585 has
  SRAM1 192 KiB, SRAM2 64 KiB, SRAM3 512 KiB, SRAM4 16 KiB and backup SRAM2 KiB.
  SRAM3 ECC protects its first256 KiB and consumes its last64 KiB, leaving192 KiB
  without ECC. MPCBB units are512 bytes, locking32-block /16 KiB groups.
  A planned secret arena in SRAM2 and separate UI/USB arenas must be enforced by
  the link map and runtime ownership checks; these totals are not peak-RAM proof.
* **ECC handling is part of the configuration.** §6.3.2 and §§6.6.1–6.6.6:
  single/double errors stop being newly detected while their respective flags
  remain set. Enable the appropriate interrupt/NMI and address-latch policy,
  accounting for ES0499's interrupt-dependent flag/address correction. Any
  double error invalidates pending crypto and review state. Flash ECC (§7.3.2)
  also requires prompt corrected-error handling; a set ECCC can prevent a later
  double error from generating NMI. Cached data and erased-line limitations
  prevent treating a repeat read as an independent clean result.
* **Erase and retain are explicit.** §§6.3.1,3.7.3 and7.9.13: SRAM2_RST=0 and
  SRAM_RST=0 request system-reset erasure of their respective SRAM groups;
  value1 means retention. Backup SRAM is outside SRAM_RST. SRAM2_ECC=0 and
  SRAM3_ECC=0 enable ECC (the polarity must not be inverted). A system reset
  alone is not a universal key/backup-register erase. The proposal excludes
  secret retention in backup SRAM/RTC/TAMP and requires startup clearing before
  accepting requests. Actual erased/retained contents are H02 evidence.
* **Owner root requirements.** §§3.3,3.10 and7.4–7.6: BOOT_LOCK with TZEN pins
  SECBOOTADD0; WRP by itself is mutable, whereas the area's UNLOCK=0 prevents
  changing its boundaries until RDP regression to0. HDP prevents read/write,
  erase and execution after closure until system reset, and also freezes the
  corresponding secure/HDP boundary options. This permits a proposal with an
  owner-installed immutable boot verifier and a boot-only version journal.
  The exact flash allocation, signed-update format and interrupted-journal
  policy still need binding; a feature label is not a bootloader implementation.
* **Lifecycle distinctions.** Development uses disposable identities and open
  debug; DHUK is identical across devices at RDP0 (§3.8.1), so it cannot be
  presented as device-unique custody in that state. Owner-secured operation
  requires a specific owner root, debug/download restrictions, rollback policy
  and recovery credentials. OEM1 gates full RDP1→0 regression; OEM2 gates
  RDP1→0.5 and may allow RDP2→1. The latter does not erase application code.
  Full RDP1→0 erases main flash, SRAMs and listed device secrets but retains OTP;
  RDP1→0.5 retains secure-watermark flash while erasing nonsecure flash and
  volatile secrets (§§7.6.2,3.10.1). No secret belongs in OTP. A root/owner
  replacement must explicitly account for retained counters and destruction of
  the old custody state. Product qualification is a separate future gate, not
  another spelling of RDP1/2.
* **Interrupted writes are not atomic.** §§7.3.5–7.3.12 pp298–305: writes and
  erases stall accesses to the same bank; interrupted locations are not
  guaranteed. FLASH_OPSR must be examined after system reset before another
  operation. Recovery needs a validated redundant record and a full affected
  page recovery policy, not continuation from a possibly partial quad-word.
  OTP interruption loses that quad-word. BOOT_LOCK/TZEN also prohibit bank
  swapping, so an update design cannot casually assume the swap-bank example.

The first firmware remains one trusted image. Hardware attribution and a second
software component do not establish hostile-application isolation. The final
configuration must state its actual runtime boundary, including what a memory
corruption in trusted firmware could still access; the above mechanisms cannot
be advertised as an already implemented partition.

## Actual reading and remaining work in this checkpoint

Later [U585 kit/boot correspondence](u585-kit-usb-boot-review.md) records
selected AN2606 ROM resource/watchdog, TCPP03 mode/control and sheet9/native-CAD
reading. ROM PC0/PC1/PB6 ownership overlaps the proposal; PA7/PB0 remains
conditional. PF14 analog VBUS sensing needs an explicitly reviewed ADC4 policy
or another complete alternative. The initial apparent U8 pin9/11 mismatch is
withdrawn: enlarged PDF, native schematic and PCB agree. No host, sensing path
or wiring admission results.
The [subsequent I2C/CC review](u585-i2c-ucpd-review.md) adds selected current
register/body and exact source/metadata correspondence. Native clock-tree
inspection confirms the HSI16 UCPD branch; the metadata's PCLK1 kernel label
is retained as a discrepancy. The blocking I2C API needs explicit byte-count,
deadline-feature and bounded recovery correspondence before selection.
The [U585 OTG source review](u585-otg-source-review.md) subsequently adds
selected CPU-FIFO/state/reset and actual Rust path correspondence. Its ZLP,
deadline/failure, buffer-bound and VBUS requirements remain unmet; no USB
adapter or complete host configuration is selected by that source increment.
The [U585 interrupt/core-time review](u585-interrupt-review.md) adds a selected
IRQ map and secure masking/SysTick limits. It promotes no excluded peripheral.
The [finite closure checklist](closure-checklist.md) is the remaining H01 work
list; later received-unit, adapter execution and design measurements stay separate.
The [clock/power correspondence](u585-clock-power-review.md) and
[calculation tuple](u585-clock-proposal.json) add a conditional MSIS48/VOS3,
drift-aware latency/SPI/I2C/short-deadline proposal and the already fitted
LSE/CRS alternative. The pinned Rust startup does not implement its bounded
waits, flash margin or LSE-CRS policy. Exact reference, supply/TCPP/USB and S3
counterparts remain open; this is not a complete configuration or working kit.

New current-RM reading: pp150–194 (§§2.3.4,3,4); pp195–212 (GTZC introduction,
implementation, functional body and selected secure configuration registers);
pp276–286 and p287 before Table50 (RAMCFG body/registers); pp291–305,307–330
(flash body/options/protection/access tables),342–350 (option/boot/watermark/WRP
registers); pp401–415 (supplies, startup, regulation, supervision and beginning power
modes);483–486,488,493–496,497–500,505–508 (reset, selected clock body and RCC
security/privilege). Figure38 p487 extraction was truncated and is not a complete
visual clock-tree review. This does **not** claim the
giant register-map tables or all diagrams were visually reviewed. The garbled
text of lifecycle Figures25/26 is not a visual review; the readable normative
transition tables and body were read.

UM2839 Rev4: pp1–5,12–21,29–34; schematic sheet8 visually correlated with
Table24. Other kit schematic sheets are not yet signed. Waveshare schematic
page1 was visually reviewed; linked module specification pp1–9 were read for
identity/electrical contradictions. Adafruit XML parts/nets and the complete native revC schematic image were
reviewed; linked controller command correspondence remains pending. Its reset
and select pull-ups are on VIN before the buffer, so5 V VIN does not by itself
make the exposed control lines safe for3.3 V S3 pins.

Current USB-IF Type-C2.5 and the June2025 USB2.0/ECN bundle are available as
private originals. The Device Capacitance and Suspend Current ECNs were read in
full: the former requires1–10 µF exposed connector capacitance in its scope;
the latter changes non-ICUSB device suspend current to2.5 mA, including pull-up
current, while preserving averaging rules. Selected current base/Type-C clauses plus VBUS Max Limit and Connect Timing
ECNs are now read as scoped in [usb-configuration.md](usb-configuration.md);
remaining applicable clauses and ECNs are still being read. Downloading those bundles does not close
the USB row.

Still required: remaining selected U585 power/reset/clock/cache/GPIO/AF/peripheral
body and exclusions, current-manual delta correspondence, exact driver deadlines
and reset policies; S3 lifecycle/XTS/SPI/USB normative and software boundary
resolution; complete proposed kit and display identities/electrical wiring;
G9 ZJ pad/rail/AF/graphics ownership and driver/license comparison. The existing
six-row sign-off remains open while this work proceeds.
