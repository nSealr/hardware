# Two-host pin and external electrical contract

Author `/root/h01_sol`, 20 October 2026, source checkpoint
`efc087d0d9bb0c2cd1f9f936e46b565c56d56fe0`. This is a finite C01/C02 source
table and qualification specification. No wire, powered fixture, selected
display, received board or complete host is admitted. C03/C04/C09 still bind
system startup, lifecycle and power. The six acceptance rows remain unsigned.

## Exact proposed identities and numbering

The U585 **host kit** is B-U585I-IOT02A / MB1551-U585AI-D01, U13
STM32U585AII6QU / UFBGA169. The custom-package comparison witness is
STM32U585VIT6Q / LQFP100 SMPS, not a second kit or a completed custom design.
Propose U585 revision U, REV_ID `0x3007`; applicable all-revision errata still
apply. H02 checks ordering/marking, device/revision readback, actual board
revision, bridges, power paths and peripheral ownership before any operation.
An unidentified or different revision is refused pending applicability review.

The S3 host proposal remains ESP32-S3-DevKitC-1-N8R8 PCB v1.1 /
ESP32-S3-WROOM-1-N8R8, with a proposed v0.2 silicon condition. Errata v1.3 §1.2
encodes v0.2 as major0/minor2; this is a read-only identification requirement,
not a fuse operation or a claim that every issue is fixed. H02 identifies the
actual module, silicon, corresponding ROM/boot behavior and effective SDK
minimum/maximum revision settings. No received-ROM allowlist/hash is invented.
The maintainer's unspecified S3 with two buttons does not establish this tuple.

U585 pad columns below are **package** pads/balls; CN/J columns are kit headers.
S3 module pads differ from chip QFN pads. DS13086 Rev10 Table 26 p107 says
ordinary U585 GPIOs reset analog unless noted. S3 GPIO4–7 reset with input
disabled, while GPIO10–13 have a different reset input state; neither gives
the fixture a safe reset/blanking default. Explicit input/mux/hold readback is
required before interpreting a contact.

| Function / owner after qualified startup | U585 net: LQFP100 SMPS pad / UFBGA169 ball; kit header | S3 net: module pad; kit header |
| --- | --- | --- |
| CPU SPI clock | PE13:41/L8; CN13.6, AF5 SPI1_SCK | GPIO12:20; J1.18, IO_MUX4 SPI2 clock |
| CPU SPI MOSI | PE15:43/M9; CN13.4, AF5 SPI1_MOSI | GPIO11:19; J1.17, IO_MUX4 SPI2 MOSI |
| Software display select | PE12:40/N8; CN13.3, GPIO (not hardware NSS) | GPIO10:18; J1.16, GPIO |
| Display D/C | PC1:16/J3; CN13.1, GPIO | GPIO13:21; J1.19, GPIO |
| Display reset | PA8:67/G7; CN13.2, GPIO | GPIO14:22; J1.20, GPIO |
| External default-off blanking request | PB6:92/B5; CN14.7, GPIO | GPIO9:17; J1.15, GPIO |
| Up / down | PC0:15/J2, PC2:17/J4; CN16.1/.2, GPIO inputs | GPIO4:4, GPIO5:5; J1.4/.5, inputs |
| Left / right | PA7:31/J5, PB0:32/K5; CN16.5/.6, GPIO inputs | GPIO6:6, GPIO7:7; J1.6/.7, inputs |
| Selection / dedicated consent | PE7:35/L7, PD15:62/J11; CN14.5/.3, GPIO inputs | GPIO17:10, GPIO18:11; J1.10/.11, inputs |
| Device USB D− / D+ | PA11:70/G13, PA12:71/F13; CN1, USB supply/domain ownership required | GPIO19:13, GPIO20:14; J4, fixed USJ unselected |
| Kit TCPP I2C2 SCL / SDA | PH4:absent/E10, PH5:absent/F9; AF4, shared fitted bus | No new I2C/SE bus selected |
| Kit TCPP EN / fault / current-sense | PB5:91/C6 GPIO; PE8:36/K7 FLGn input; PD13:60/K12 IANA analog path excluded | No TCPP is fitted on this S3 kit |
| Kit CC1 / CC2 | PA15:77/A10, PB15:54/L11, dedicated additional functions via TCPP, not maker GPIO | No new CC controller selected |
| Conditional attach status | TCPP fresh I2C status; no ADC4/UCPD promotion | GPIO8:12; J1.12, reserved input, no fixture selected |

The custom LQFP100 SMPS exposes neither PC4/PC5 nor PH4/PH5. It also omits
PB11. PB10/PB11 therefore cannot be assumed to replace the kit's I2C2 pair.
Table 28 p137 gives AF4 I2C2 on PB13/PB14 (pads52/53), an unselected custom
alternative. PB14 is **DBCC2**, a distinct dead-battery control input; it is not
the kit CC2 net. Native sheet9 connects CC2 to **PB15**, CC1 to PA15. The initial
private draft's PB14/CC2 physical-conflict inference is **withdrawn**. DS p134
note4 states that high PB14 activates Rd on PB15; high PB5 similarly affects
PA15. That additional-function owner still needs explicit exclusion and safe
reset behavior if those GPIOs are reused. RM10.10.12 p458 names the actual
control PWR_UCPDR.UCPD_DBDIS; the UCPD chapter's CR3/USBPD_DIS wording is stale
against this register and FLASH_OPTR.PA15_PUPEN. No fuse or register write is
performed or authorized by documenting that discrepancy.

The kit host uses PH4/PH5. No PB13/14 alternative, complete custom BOM or private
SE/expansion allocation is selected here; actual reset/CC/pin allocation must
close before H04. The initial draft also mistakenly named PB4 as TCPP alert;
**native sheet9 instead proves PE8 FLGn and PD13 IANA**. PB4's NJTRST default is
not that signal. These source/draft corrections carry no defective-board or
hardware-conflict claim.

## Fitted U585 branches and boot lifetime

Native MB1551-D01 sheet8 agrees with UM2839 Table 24: SB10/SB13 connect
PA7/PB0 to CN16.5/.6; SB11/SB12 are DNF alternate I2C1 paths. Require that
exact population and leave other shields, STMod/Pmod and unused header loads
absent. PA7/PB0 are not BOOT0. AN2606's retained ROM table nevertheless uses
PA7 as SPI input; ROM also overlaps PC0/PC1/PB6. No local-control/display
authority exists in ROM/download/recovery. The fixture must blank independently,
allow those pins' documented reset/ROM behavior, and never treat a held contact
or ROM output as consent. Requalify mode/ownership and stable release after
returning to the application.

PE13 also reaches the fitted Q3/R48 Arduino LED branch. PE13/PE15 and unused
PE14 reach U4 STG3692QTR. Sheet7 and DS4909 Rev9 pp1–7 agree: PH13 high selects
the UART/S1 branch and isolates SPI/S2 from the common connector; low selects
SPI. R11 is DNF, so the table's nominal default UART is not a reset bias.
Keep PH13 high before SPI use, qualify its rise/control state, and leave
CN2/CN3/CN4 empty. U4 is supplied by3V3; its signal range is0..VCC and
control range0..4.3V. The disabled-port capacitance is only a typical 5 pF,
not a worst-case total fixture load. No unpowered isolation is specified by
these observations. The actual branch/LED/cable load and edges remain H02
checks; GPIO count and switch selection do not remove them.

### Installed radio correction and limits

Native sheet13 identifies M1 **EMW3080(BP)**, CHIP_EN pin11 connected to PF15
(BGA N6). Official [MXCHIP DS0122CN v2.8](https://docs.mxchip.com/attach/zh/DS0122CN_EMW3080_V2.8.pdf)
pp7–10,19 covers that BP variant separately from V2-P. Enable/reset is active
low; the module contains a nominal 100 kΩ pull-up and 10 nF to ground. The older
inference that the **whole net** simply floats is withdrawn. The board still
has no external hold-low; MCU reset analog does not establish Wi-Fi shutdown.
PF15 low is a pre-intake reset requirement; source VIL≤0.8V versus U585
VOL≤0.4V is compatible only under the specified valid rail/load conditions.
Nominal resistor arithmetic is not a tolerance, shutdown-current or RF bound.
The module supply is3.0–3.6V; its 450mA supply recommendation is not a reset or
USB suspend-current maximum. No power-off, RF-quiet-from-POR or zero-emission
claim follows.

UM2839 Tables 12/13 and sheet13 bind Bluetooth UART to PC10/C9 and PC11/A9,
wake to PG6/H10. B1 BT_NRST is a separate physical button, not a target reset
output. SW3 selects system3V3 or a CN12-fed regulator; it is not an off switch.
The conservative paper condition keeps the module supplied from system3V3,
with no target UART/flow/wake/SWD ownership or radio driver admitted. Do not
claim unpowered-I/O isolation by choosing an unpowered CN12 supply. Physical
reset restraint, POR behavior, RF absence and external isolation remain
unproved; any operation requiring them stops. Neither an unused API nor a
GPIO level proves the separate module inactive. This does not silently qualify
the kit as a radio-free production design.

## Normal external fixture requirements

The allowed display/contact fixture is an **interface specification**, not
selected parts, an available power supply or wiring permission. It cannot cure
the DB module's unsatisfied startup/internal-power/factory-state evidence in
[panel-subset-review.md](panel-subset-review.md). H02 stops before any operation
requiring that evidence. C09 adds complete supply/attach/reset/backfeed lifetime.

| Path | Finite normal contract | Source limit / unresolved implementation |
| --- | --- | --- |
| Host I/O rails | U5853.3V proposal, HSLV disabled; S3 domain3.0–3.6V with effective valid rail established before use. No positive drive into an absent host rail. | U585 VDDUSB separately requires3.0–3.6V; nominal3.3V is not rail measurement. S3 DS2.2 Table 5-4 is at3.3V/25°C with high-impedance output load, not a full load/temperature guarantee. |
| Raw DB VDD36/37 | Propose externally regulated3.00V ±2% total error, i.e.2.94–3.06V, logic current capacity at least 15 mA at the specified3V condition, with transient/current/inrush margin to qualify. | Inside module2.5–3.3V range. This is an engineering fixture requirement, not an existing regulator/temperature/current guarantee. Never join raw VDD directly to an unchecked kit3V3 rail. |
| Host→panel logic | Qualify one-way translation/buffering of SCL/SDI/DC/CS/RESX and fixed interface inputs. At the panel require high0.90..1.00×panelVDD, low0..0.10×panelVDD; never above panelVDD during normal use. | Module requires VIH≥0.7VDD and ≤VDD, VIL≤0.3VDD. No direct3.3V host→3.0V panel margin is inferred; absolute VDDI+0.3V is not normal permission. Unused outputs remain open. |
| Source-facing logic load | U585 receiver must accept host high≥VDDIO−0.4V and low≤0.4V under selected table conditions. S3 receiver must accept high≥0.8VDD and low≤0.1VDD under its stated high-impedance conditions. Account for input leakage, branch/cable capacitance and simultaneous currents. | U585 DS Table 96, S3 Table 5-4. Do not treat a typical current/capacitance or unloaded VOH as a universal drive rating. |
| Clock/data edges | U585 SPI1 OSPEEDR=`01`, HSLV0, total supported pad load≤30pF under Table 98 conditions; panel-facing rise/fall≤15ns and the selected setup/hold/CS limits. S3 drive/source/load must meet those same panel-facing limits. | U585 normal2.7–3.6V Table 98 gives max5.8ns at30pF; slower OSPEED00 max17ns at50pF alone misses panel15ns. Translation/skew/LED/mux/actual load still require H02. No new compensation/HSLV feature selected. |
| Controls | Six independent normally-open dry contacts to target ground. Propose each10 kΩ ±1% pull-up to the same valid host I/O rail, closed path≤100Ω, fixture leakage magnitude≤1µA, high≥0.90VDD, low≤0.10VDD. Internal pulls/output/alternate ownership disabled. | U585 normal selected pad types use conservative0.3/0.7VDD thresholds; S3 uses0.25/0.75 under Table 5-4 conditions. At3.6V,10 kΩ minimum gives≤0.364mA/contact. Actual leakage/load/temperature, bounce/stuck/ESD/cable/ownership remain qualification gates. |
| Blank/reset/select | External circuitry defaults backlight off, panel reset asserted and select inactive during absent/invalid rails, POR, reset, ROM/download, boot, clock loss and failed software. Application may request enable only after full valid render and release qualification; a GPIO alone cannot guarantee that lifetime. | No direct LEDA/LEDK MCU drive. Backlight current 15mA nominal, never above 25 mA; source 10.8–13.6V at15mA, controlled current. Module output-off/reset does not erase GRAM or prove optical blanking. |
| Contact and disconnect | Exact45-contact rear-view mapping, correct bottom-contact FFC orientation and no positive injection/backpower during either side's power loss or disconnect. Other sources and shields absent. | Molex product identity alone does not qualify the received sales drawing/connector/fixture. Actual isolation, edge timing, blanking, reset and optical response require H02/H03. |

Generic U585 VOH≥VDDIO−0.4V also does **not** alone establish TCPP EN's3.3V
±10% minimum at the proposed low rail:3.2175−0.4=2.8175V is below2.97V.
Retain the actual-valid-EN source/readback/supply prerequisite and refuse use
without it; no electrical-margin waiver or new EN driver is selected here.

## Scope and remaining gates

S3 controls avoid straps GPIO0/3/45/46, CHIP_PU, UART auto-program and USB19/20.
GPIO35–37 are unavailable on N8R8; GPIO38 is the fitted v1.1 RGB LED and is not
allocated. The shared CP2102N/reset/rail path remains real with its USB cable
absent. CPU1, RF/MAC, unused GPIO/peripheral/DMA routes and retained holds must
have the C03/C04 effective ownership/exclusion proof. No maker bus is granted
access to secret memory, consent or the trusted display.

The sources close only the listed finite pin/electrical reading and explicit
normal interface requirements. ROM/silicon identity, effective settings and
all later physical outcomes remain unproved. C03/C09 must finish safe system
power/reset/watchdog/attach lifetime; C04 must finish developer/owner/recovery
behavior. Fixed-USJ descriptors/transport remain unselected, U585 OUT64/68
remains an unsatisfied source property, and no host criterion is signed by this
table. The new touchscreen/product priorities are assessed in
[option-comparison.md](option-comparison.md), not waived by this no-touch baseline.

Actual fresh reading: U585 DS pp107,232–238,242; selected used Table27 rows
pp111,114,116–119,121,123–125,129,131–134 and AF rows137/140/143; p99 native
diagram reread. LSI p226 is carried into C03 only. UM2839 Table 12 p24,
Table 13 p25, Table14 p26 and selected STMod Tables 25–27 pp34–35; earlier
Table 24/header reading reused. Existing native kit sheets7/8/13 and S3
schematic sheets1/2 reread; no new whole-CAD audit. STG3692 pp1–7 selected
text including tables, no native test-circuit/package audit. MXCHIP pp1,7–10,19
selected text, no native figure or complete RF/production review. RM selected Table776 p3462/74.4.6 pp3472–3473 and UCPDR p458 read/reread for the
distinct DBCC/CC/control naming; no new UCPD mode selected. S3 module
pp10–14 and DS pp64–65 reread; errata selected revision identification p1.
The raw product's exact identity/touch/technical/price body was read separately;
site navigation/scripts and neighboring models are not technical evidence.
Originals, extractions and native renders remain private.
