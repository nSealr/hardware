# Conditional S3 J4 attach contract

This is the one external attach-fixture assessment allowed by the coordinator
for the retained S3 kit. It is conditional on the independent fixed-descriptor
gate below and does not select CDC, a fixture implementation or parts. No
wiring or energizing permission follows. The unmeasured whole-kit bus-powered
alternative remains open; no source result here declares the kit fails
suspend.

## Exact topology and source limits

The v1.1 schematic's sheet2, dated30 November2022, shows J2 USB-UART VBUS
through D1 and J4 native-USB VBUSB through D7 reaching the same VCC_5V.
U2 powers the shared3.3 V rail; the CP2102N, power LED and RGB LED remain
loads even with J2 empty. The board's C15 on native VBUSB is marked not fitted.
Neither that annotation nor diode direction proves assembled reverse-current,
capacitance or suspend behavior. J4 has no VBUS-valid signal to the S3.

For this **conditional self-powered** assessment, upstream VBUS is confined to
the external fixture's sensing/load circuit and must not feed J4 pin1 or the
kit's VCC_5V/3.3 V rails. The independent permitted kit supply uses the
documented5 V header J1.21 and ground J1.22; J2 remains empty. Exact supply
tolerance/current, shared-rail/bridge/reset behavior and normal kit regulator
limits must still close C01/C03/C09 before this becomes a selected topology.
The display's separate conditional rail/backlight fixture must not backpower
the kit or USB. This does not add a USB port or a second controller.

USB2 §7.1.5.1 requires VBUS-controlled pull-up power; §7.2.1 forbids upstream
VBUS sourcing and gives a10 s maximum pull-up removal time after VBUS is
removed. The proposed fixture imposes a much shorter engineering bound below.
The Connect Timing ECN pp5–6 sets peripheral session-valid threshold within
0.8–4.0 V and powered-peripheral connection/readiness within1 s. It preserves
the100 ms unit-load preconnect limit and adds the1 s postconnect suspend-current
allowance. No weak/dead-battery provision is invoked.
The native redline's revised Δt7 also requires an unconfigured peripheral to
reduce to suspend current after that1 s allowance; ordinary bus traffic is
not a reason to keep an unconfigured unit at its unit-load allowance forever.

USB2 §7.1.7.6 requires suspend transition after more than3 ms constant idle,
with suspend current by10 ms after bus inactivity, subject to the ECN's
postconnect allowance. Suspend preserves the pull-up and permits resume.
Disconnecting, deep sleeping or leaving a nonresponsive light-sleep device
attached is not an equivalent suspend implementation. The Suspend Current ECN
sets2.5 mA for this non-hub device, including pull-up contribution, with the
unchanged1 s averaging/spike rules. The VBUS Max Limit ECN replaces5.25 V
upper supply limits with5.50 V. Those are USB limits, not permission to apply
VBUS to a3.3 V signal.

## Proposed external interface requirements

These are finite acceptance requirements for a future fixture, not measured
limits or claims about an unspecified component. H02 must identify an exact
implementation and prove them before the topology is usable.

| Property | Required behavior |
| --- | --- |
| VBUS detection | Proposed rising threshold3.90 V ±0.05 V and falling threshold3.30 V ±0.05 V, including reference, divider, loading, temperature and supply errors. Thus both thresholds lie within the ECN's0.8–4.0 V range, and the maximum rising threshold3.95 V is below the4.40 V minimum configuration supply at the upstream cable end. Hysteresis must remain positive. These are engineering selections, not an existing detector's specification. |
| Autonomous isolation | Both data paths remain isolated unless real upstream VBUS is valid and the kit I/O rail is within its supported operating range. On falling invalid VBUS or invalid local rail, disconnect within1 ms, independently of S3 code, clocks, reset state or GPIO configuration. Do not rely on the S3's default pull-up or a firmware detach write. No VBUS-valid GPIO can override this hardware condition. |
| Unpowered and startup | Loss of either supply, slow rise, reset, bootloader/download entry and an absent/nonrunning firmware owner must not connect a powered kit pull-up to an upstream port with invalid VBUS, inject into an unpowered S3 pin or source upstream VBUS. With VBUS present and a valid local rail, a reset may remain physically attached; it still cancels all application consent. Clock loss grants no responsiveness or operation claim. The independent VBUS-off isolation remains effective during it. |
| Upstream loading | Fixture VBUS draw ≤0.50 mA in every declared state, independent of enumeration, active firmware or local supply; aggregate port behavior must still meet the actual descriptor allocation,2.5 mA suspend limit and applicable1–10 µF/inrush model. The separate supply carries kit/display load. Measure both paths and reverse current, rather than subtracting an estimated MCU current. |
| Data path | Preserve full-speed12 Mb/s polarity, levels, termination, capacitance,4–20 ns rise/fall, matching, jitter and packet timing over the **complete** fixture/cable/kit path. No external pull-up/down is added without the exact termination analysis. In the isolated state require total upstream leakage ≤1 µA per data line in either permitted power state; with the ECN's24.80 kΩ maximum host pull-down that contribution is at most24.8 mV. This calculation does not establish complete idle/disconnect voltage or actual leakage. |
| Status input | Reserve only GPIO8 on J1.12 / WROOM-1 module pad12 for a local-rail-referenced VBUS-valid input. Chip QFN pad13 is a different numbering space. Configure GPIO input explicitly; SUBSPICS1, touch/ADC and RTC alternate ownership are excluded. It is not one of the four boot straps and is not a consent control. No direct VBUS divider into the pin is presumed safe. |
| Status levels | At a valid local rail require high ≥0.90×localVDD and ≤localVDD, low between0 and0.10×localVDD, within the stated load/temperature conditions. DS2.2 Table5-4 at3.3 V/25°C gives VIH≥0.75×VDD and VIL≤0.25×VDD; those test conditions remain explicit. When local power is absent, the fixture must not drive the pin positively or use its protection diode as a supply path. Source the output and its default from the local rail; actual load, edges, injection and power sequencing remain H02 checks. |
| Firmware status | Poll the qualified input with a source-backed maximum1 ms observation interval; loss invalidates partial request/render/consent. A high sample is only the fixture's declared electrical status, never proof of cable removal, a trusted host or approval. An unavailable/stuck/disagreeing status refuses a fresh operation. The independent hardware data isolation handles loss when firmware cannot poll. |
| Connection/startup | With VBUS/local rail valid, the complete permitted boot/attach path must be ready to enumerate within1 s of session-valid crossing. No secrets load until exact received identity/lifecycle, clocks, exclusive writers, input release and fresh session checks succeed. Do not extend that deadline through a chain of individually bounded waits. |
| Suspend/resume | For the conditional self-powered route retain the compliant fixed controller's required APB/PLL clocks and pull-up during suspend; exclude S3 light/deep sleep and remote-wakeup generation. Stop application requests and invalidate consent after the bounded no-activity policy. Respond to host resume/reset without granting an old request/approval. Port draw remains bounded independently of CPU/LED/display current. Actual bus behavior and timing require H02 evidence; this policy does not prove the controller's descriptor/status is suitable. |

The proposed threshold/error values,1 ms limits,0.50 mA and1 µA allocations
are reviewable engineering requirements. They are deliberately separate from
the manufacturer and USB limits that constrain them. No comparator, switch,
isolator, supply or protection component is selected; no new component-market
search is authorized by this specification. Failure to find an implementation
meeting the contract requires a coordinator decision before any replacement
scope, rather than relaxed margins or a guessed electrical exception.

## Independent fixed-descriptor and status gate

USB2 §9.1.1.2 printedp242 says a configuration reports its power-source
capability and current device status reports the actual source. §9.4.5
pp254–255 defines `GET_STATUS(DEVICE)` bit0: one means currently self-powered.
§9.6.3 pp264–266 defines configuration `bmAttributes` bit6 for self-powered
capability and `bMaxPower` in2 mA units. Merely drawing less than an advertised
bus-current value does not establish that self-power capability/status is
truthful. An external isolation fixture cannot rewrite a fixed descriptor or
its hardware response.

The reviewed public TRM33 functional/register body and pinned fixed-USJ
driver/API/LL/guide do not specify the complete device/configuration tree or
its `bmAttributes`, `bMaxPower` and power-source status values. No absence claim
is made for unreviewed public sources. No captured descriptor is available.
The finite missing received-device contract is:

* Exact VID/PID, USB/device release values, descriptor lengths and number of
  configurations, including any silicon/ROM/lot/lifecycle variation.
* Every complete configuration/interface/class/vendor/endpoint descriptor:
  total lengths, interface association, addresses/directions/types, packet
  maxima/intervals and all reported capabilities.
* Power-source capability, maximum upstream draw and actual
  `GET_STATUS(DEVICE)` self-power/remote-wakeup state in each proposed supply,
  reset and secured/developer condition. Permanent debug disable must not
  silently alter or revive an excluded interface authority.
* Standard/class request, reset, endpoint halt/toggle and suspend/resume
  behavior actually needed by this fixed CDC path, against the public
  normative requirements. The separate OTG NDA semantics cannot be inherited
  or waived through a descriptor capture.

H02's read-only capture procedure first establishes a separately reviewed safe
supply/current/fixture setup with disposable state and known received
marking/ROM/lot/lifecycle. It then records raw complete descriptor bytes,
decoded fields, control-request status responses, tool/OS versions, exact
port/cable/supply state and hashes. Do this after cold boot and each relevant
reset/state change; never infer a device from VID/PID or a terminal name alone.
Issue device-status reads only in a defined addressed/configured state; the
base specification does not define their behavior in Default state.
Retain the raw response tree and status, not only a screen summary. No fuse,
flash or security transition is part of that read-only procedure. Capture is
not authorized until its electrical prerequisites are satisfied.

Reject the conditional self-powered route if capability/status cannot match
its actual supply mode, if maximum power cannot cover the port load, if the
tree contradicts the public controller contract, or if an owner setting
disables required CDC or leaves debug authority. Do not modify hardwired
descriptors, misreport the supply or enable debug/download to obtain a pass.
The whole-kit bus-powered route then remains only its original unqualified
alternative, requiring its own complete suspend/current proof. If neither
route closes, CDC is not admitted and the coordinator must decide scope.

Sources: [USB-IF USB2 bundle](https://www.usb.org/document-library/usb-20-specification),
[S3 DS2.2](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf),
[WROOM-1 DS1.8](https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf),
[exact v1.1 kit schematic](https://dl.espressif.com/dl/schematics/SCH_ESP32-S3-DevKitC-1_V1.1_20221130.pdf),
[S3 fixed-CDC source contract](s3-usj-contract.md).
Selected USB normative text/table reading includes base physical169,178–179,182–184,
198–199,203–210,216,270,282–284 and292–294, with unrelated HS/LS/hub text
encountered. These are selected paragraphs/table bodies rather than complete
review of every listed page. Connect ECN nativepp4–5 and resistor ECN nativep4
were visually checked; remaining USB waveforms/eyes/figures were not newly
visually audited. Resistor ECN Figure7-20/21 labels use14.75 kΩ minimum while
the explicit replacement table/text uses14.25 kΩ; preserve the difference and
budget the wider14.25–24.80 kΩ table range. No USB compliance, physical current, actual fixture
or completed host signoff is claimed.
