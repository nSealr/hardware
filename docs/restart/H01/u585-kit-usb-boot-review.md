# U585 kit USB and ROM-boot correspondence

Author `/root/h01_sol`, 20 October 2026, continuing from `2adec7d`.
The maintainer briefly requested a stop and explicitly revoked it before this
checkpoint. H01 is active; no pause handoff or host admission is asserted.
These are selected source findings, awaiting distinct review.

## Corrected USB drawing reading

The initial full-sheet reading suggesting that TCPP03 U8 pins9 and11 were
interchanged is **withdrawn**. A larger native-PDF crop, the native D01
`USB_TYPEC.SchDoc` wire records and selected native PCB pad nets all agree:

| Node | Correspondence in all three sources |
| --- | --- |
| U8 pin9, VBUSc | Full `VBUS_C`, at the input side of R7. |
| U8 pin11, Vsense | R7/R8 divider junction; R7=10kΩ from VBUS, R8=2.4kΩ to ground. |

The apparent mismatch came from my reading of the routing at the full-sheet
scale. No stale-export, board-defect or swapped-pin claim remains. The text
annotation mentioning2.7kΩ differs from the actual R8 value2.4kΩ; the latter
matches the nominal6V row in TCPP03 Table13. This is a source annotation
discrepancy, not a physical-board measurement.

The private official design archive has SHA256
`c48391854b70c934a78971fe6baa3882bf974075eed4c4f2846ba15b4ce14a4b`
(22,018,475bytes). Its readme identifies release2.1; the official kit resource
listing dates that release1August2023. Only its readme, selected D01 schematic
records and selected PCB pad/net objects were examined. The project file was
extracted but not reviewed; no whole-layout, stackup, clearance, fabrication or
assembly audit occurred. Read-only KiCad10.0.7 Altium import was used in memory;
font substitutions do not establish or invalidate physical connectivity. No CAD
project was edited or saved. Native files, parsed records and drawing crops
remain private. Public metadata identifies the exact archive/member hashes.

## TCPP03 control is a state machine

DS13618 Rev5 September2025 pp10–18, especially Figure11 p12, distinguish
register defaults, operating modes and gate controls. The I2C seven-bit address
is `011010x`; with I2C_ADD grounded on this schematic it is **0x34**. The kit
manual's0x68 is the shifted write-address byte, not a seven-bit API address.
This distinction must be explicit in the future I2C adapter.

| Control/status | Selected-source consequence |
| --- | --- |
| EN low | Device off/reset, I2C inactive and registers reset; dead-battery resistors enabled; consumer path can be self-biased from VBUS; provider off. MCU reset alone does not prove EN low: sheet9 draws PB5 directly and no external pull-down. |
| EN high | Initial mode is Hibernate with I2C active. The datasheet requires an EN rise under50µs when dynamically triggered. The circuit and actual transition must satisfy this before relying on a software mode write. |
| PM2:PM1 | `00` Hibernate, `10` Low-power, `01` Normal; `11` unused. Normal transfers CC termination responsibility to a correctly configured MCU/UCPD path before dead-battery termination is removed. |
| Gate bits | GDC=1 opens the consumer gate; GDC=0 closes it. GDP has the opposite sense:1 closes provider,0 opens it. A common generic “enable” interpretation is unsafe. Provider and VCONN remain excluded proposals. |
| FLGn | VBUS-presence indication in Hibernate/Low-power; fault indication in Normal. It cannot serve as a mode-independent physical-unplug signal. |
| VBUS_OK | Register2 bit5; bind its interpretation to EN/mode/I2C validity and the documented voltage threshold. It does not establish a complete disconnect deadline, physical plug state or power-off proof. |

R7/R8 give the nominal6V overvoltage setting, not an exact6V clamp; the Vsense
threshold spans1.1–1.25V before resistor tolerance. The47mΩ current-sense
resistor and35–45mV threshold imply roughly0.745–0.957A before resistor
tolerance. A nominal “0.5A” application label is neither a hard500mA limiter
nor permission to draw that current before USB configuration. Protection fault
recovery must follow the applicable I2C/mode sequence; it is not a blanket
automatic retry policy.

Table5 p7 groups Vsense with a2.7–5.5V recommended range, whereas the
functional divider/OVP threshold uses about1.16V at the nominal trip point.
That source inconsistency remains unresolved; the functional example does not
silently certify the stated recommended-range table or final electrical limits.

The separate PF14 VBUS divider is R5=330kΩ/R6=49.9kΩ. Nominal5V becomes
about0.657V at PF14. DS13086 identifies PF14 as ADC4_IN5. This is an analog
sensing path, not a demonstrated3.3V digital-high signal. The present
peripheral manifest excludes ADC4, so this path is not implemented by the
current proposal. Either admit and fully review its bounded ADC4 configuration,
or specify another complete TCPP/mode-based sensing policy. No alternative has
yet been selected. VBUS thresholds, hysteresis, resistor/tolerance margins,
startup, power-off injection and the normative disconnect time remain open.

## ROM boot is outside application GPIO ownership

AN2606 Rev70 February2026 chapter95 pp501–506 lists U575/U585 ROM resources.
Its SPI1 uses PA7 as an input; PB0 is absent from the selected resource table.
Those facts alone do not prove the proposed PA7/PB0 button arrangement safe
through every boot state. ROM I2C3 uses PC0/PC1, overlapping the proposed Up
input/display D/C; ROM I2C1 uses PB6/PB7, including the proposed backlight pin.
The Bluetooth PC10/PC11 branch also overlaps ROM USART3, despite the different
application UART assignment. Exact entry policy, reset defaults, radio branch
control and powered-off I/O constraints must therefore be checked together.

The chapter's SPI3 pin directions contain prose/function-column disagreement;
that unused interface is not silently used as a wiring authority. General
activation Pattern12 also contains malformed TZEN text. Neither is a basis for
an option-byte recipe; current RM0456 remains the applicable register source.

The U585 table states that ROM maximizes the IWDG prescaler and periodically
services it if the hardware-IWDG option was previously enabled. General §4.8
also discusses prescaler updates for a software-enabled IWDG. A watchdog
therefore does not guarantee recovery from a ROM wait loop. §4.8 describes a prescaler-update
flag problem if ROM attempted an update before IWDG enable; startup must not
add an unbounded PVU wait. Bootloader entry and return need an explicit policy.
Boot model V3_1 makes ROM-required resources nonsecure when TZEN is
active; a ROM `Go` is not equivalent to the application's fresh secure reset
configuration for other resources. No trusted entry/return procedure is selected.

Table3 p46 reports U585 bootloader ID0x93 at0x0BF99EFE. This is a source table
identity, distinct from interface protocol versions, not an observation of any
received unit. H02 still has to match actual silicon, ROM and configuration.

## Reading and limits

Fresh AN2606 extracted-text reading: cover/applicability pp1–2; §§4.1–4.2
pp34–37; selected U585 Table3 row p46; hardware-connection text pp47–48;
§§4.8–4.10 pp57–60; chapter95 pp501–506. Flowchart text was read, without a
new visual flowchart review. The remainder of this553-page manual is unread.

Fresh TCPP03 reading: pp1–2,4,6–8,10–19 and revision history p26; p5 diagram
text encountered without visual review. Native pp2,4,12,19 were visually
inspected. The remaining thermal/package/PCB bodies are not signed. UM2839
§7.5 pp20–21 and Bluetooth Table12 were reread; §§10.2–10.3 pp44–45 product
and board history were read. Native MB1551 D01 sheet9 and its U8 zoom were
visually inspected. DS13086's PF14 pin-function entry was checked; no new
whole electrical/AF table review is claimed. The official OPLA text was read
in full; no manufacturer original is redistributed here.

The kit's UCPD/CC, I2C2 timing/error recovery, source/sink gates, USB controller,
interrupts and complete startup/reset/low-power policy remain unresolved.
This checkpoint does not select a sensing circuit, host configuration, panel,
power topology or driver. No build, physical test, fuse operation or hardware
modification occurred; all six documentary signoff rows remain incomplete.
