# Two-host power, attach and write lifetime

Author `/root/h01_sol`, 20 October 2026, after `aa383df`. This finishes the
finite C09 source assessment and requirements table. It does **not** establish
a permissible connected implementation: the U585 autonomous attach/EN properties
and S3 descriptor/status/fixture properties below are unsatisfied. Neither kit,
power chain, USB path, display, battery or physical operation is selected or
qualified by this table. No connection or power application is authorized.

The companion [proposal](power-attach-lifetime-proposal.json) records values and
negative outcomes. Existing [USB requirements](usb-configuration.md),
[system policy](system-runtime-contract.md), [owner/update policy](owner-update-contract.md),
[external display contract](pin-electrical-contract.md) and
[S3 conditional attach assessment](s3-attach-contract.md) remain binding.

## Exact kit supply proposals and exclusions

| Host | Finite supply arrangement assessed | Limits and unresolved implementation |
| --- | --- | --- |
| U585 | One independent regulated 5 V source through the **existing CN8 charger-only input**, JP4[7–8]; CN1 only the native device transport. Proposed source acceptance is 4.75–5.25 V at the board under all declared loads/transients, not the charger's label. JP4 has one fitted selection, JP3 retains the MCU supply link. TCPP Hibernate0x08 opens the consumer path and disables provider/VCONN/discharge. | UM2839 explicitly prohibits a PC at CN8 in this bypass setting. It is a power-only source, with no data-host/debug claim. CN1 VBUS must not feed the system through a closed consumer gate. Native supply/connector/bridge/reverse-current, debugger/reset behavior, temperatures, full load and current-limited source behavior remain H02/H03 gates. Charger naming supplies no BC1.2/PD negotiation or generic PC permission. |
| S3 | **Neither** alternative is selected: (A) J4-only whole-kit bus power, J2 and 5V/3V3 header supplies absent; (B) conditional external fixture keeps upstream VBUS away from J4 pin1/kit power and supplies the kit independently through J1.21 5V/J1.22 ground, J2 empty. Proposed independent-source acceptance is 4.75–5.25 V at that header. | The guide's USB, 5V-header and 3V3-header methods are mutually exclusive; its USB method permits either/both USB sockets, which does not permit header power simultaneously. B uses only the already allowed fixture contract and GPIO8 status allocation. Whole-kit suspend/inrush/reverse current and descriptor/status correspondence are unmeasured. Direct3V3 injection, USB-UART as another transport and parts selection are excluded. |

The U585 source choice is a **paper supply proposal**, not a claim that CN1 may
be attached under all conditions. The default ST-LINK-powered JP4[1–2] route
requires its own enumeration before the target gets power and is not substituted
silently. VIN7–12 V/JP4[3–4] is another existing branch, not this proposal.
JP4[5–6] selects 5V_UCPD, but GDC1 **opens** its consumer switch, so it cannot
simultaneously be claimed as the operating supply in the retained Hibernate0x08
contract. EN low instead makes the consumer driver self-biased from VBUS; a
reset cannot be treated as retaining the software-open gate or avoiding backfeed.
One jumper selection does not prove every other board branch is isolated.

UM2839 p16 calls its Type-C connector CN14. The exact native sheet9 labels it
**CN1**, while CN14 is an expansion header in the same manual. Use native CN1
identity, not that conflicting sentence. The corrected U8 pin9/11 correspondence
remains withdrawn as a conflict: PDF, SchDoc and PCB agree.

For S3, native U2 is **SGM2212-3.3XKC3G/TR**, not an AP2112 inferred from another
board. Its July2023 RevA.2 source specifies normal input2.7–20 V and conditional
3.251–3.349 V output at0–800 mA; no800 mA thermal capability of this PCB follows.
SOT-223 θJA117°C/W is a source condition, not a measured board resistance.
Recommended effective output capacitance is1–10 µF, while the application prose
also discusses larger capacitance favorably. The native kit shows C9 nominal
10 µF and C10 0.1 µF, plus further same-rail decoupling. Their actual effective
sum/ESR/stability cannot be inferred from nominal labels or that prose; retain
the exact normal-capacitance/source correspondence as an unqualified condition,
not a defective-board or observed oscillation claim. Dropout is defined at95%
output and cannot by itself establish a normal rail. Do not substitute a part or
silently change the supply route to escape those conditions.

## U585 CC, EN and attach source result

In TCPP OFF/Hibernate its connector-facing dead-battery resistors remain enabled
and the MCU-facing CC switches are **off**. Table8 gives RDB4.1–5.6 kΩ under its
400 µA condition. That fits the default-power/no-current-detection Rd envelope
4.08–6.12 kΩ; it is not orientation,1.5/3 A or PD negotiation. Normal/Low-power
remove those dead-battery resistors and are not substituted. UCPD, ADC4, source,
FRS, VCONN and accessory behavior remain excluded.

The MCU's PB5 DBCC1 control is also TCPP EN. The exact current register is
PWR_UCPDR.UCPD_DBDIS: propose1 before driving the EN sequence, UCPD_STBY0,
reserved bits retained, with UCPD clock/reset/RX/DMA/interrupt owners excluded.
This disables the MCU's additional dead-battery effect; it is not a claim that
PB5 is physical CC1 or that UCPD now supplies the connector's Rd. At reset its
value is0; it is not reset on Standby exit. The normal workload excludes those
sleep states and must reestablish/read back the whole owner state on reset.
Hibernate's disconnected CC switches distinguish internal MCU pulls from
connector Rd, but do not prove powered-off I/O isolation or arbitrary EN levels.

Two mandatory properties remain **UNSATISFIED**:

* **Valid EN:** TCPP's3.3 V mode requires EN≥2.97 V and a dynamically triggered
  rise<50 µs. The already recorded U19/GPIO source floor is3.2175−0.4=2.8175 V,
  below that required level. Nominal3.3 V, small expected load or a successful
  I2C example does not close the specified margin/rise/lifetime. Without an
  exact applicable safe electrical solution, no dependent mode/status operation
  is permitted. No new level circuit or board rework is selected here.
* **Autonomous VBUS-off data removal:** native CN1 D+/D− connect directly to
  PA12/PA11 through protection. TCPP's switches act on CC/VBUS, not those data
  lines. VBUS_OK needs valid EN, supplies, fresh counted I2C and mode/status
  readback. The proposed10 ms poll+2 ms transaction+1 ms detach=13 ms is only a
  normal-running software budget. It does not prove pull-up removal when the
  clock is lost, reset is held, boot/ROM has different ownership, I2C is stuck
  or firmware is absent. A watchdog nominal count is not that independent
  lifetime guarantee. USB2's10 s maximum and Type-C's40 ms detach condition
  cannot be signed from it. No U585 external fixture expansion is made.

On any invalid/stale/unknown mode/status, software must invalidate consent and
partial data, stop new work and command SDIS/BVAL-invalid under its qualified
normal-running path. That is useful refusal behavior; it does not satisfy either
unsatisfied physical interface property. H02 dependent attachment/enumeration
and operations remain stopped, independently of the existing OUT64/68 blocker.

## Port power and complete lifetime requirements

| Condition | Required behavior and source boundary |
| --- | --- |
| Before configuration | USB2 §7.2.1 permits at most100 mA, an absolute maximum, until a valid configuration/current allocation permits more (up to500 mA for this USB2 scope). A limiter/regulator capacity or CC default alone grants no higher draw. Proposed U585 self-powered descriptors must truthfully state capability and actual GET_STATUS; class/VID/PID remain unselected. S3's corresponding fixed fields remain unknown, with its separate read-only capture/refusal gate. |
| Session timing | Reuse the Connect Timing ECN: session-valid0.8–4.0 V, powered readiness≤1 s,100 ms unit-load preconnect window and1 s postconnect allowance before unconfigured suspend current. Every startup wait must fit the end-to-end bound. No dead/weak-battery exception, unsolicited later bus traffic or chained timeout extends it. |
| Suspend | Reuse USB2 §7.1.7.6 and the Suspend ECN: idle>3 ms triggers suspend, current by10 ms subject to the postconnect allowance;2.5 mA VBUS maximum averaged in **any**1 s interval, including termination contributions, spike≤allocation and rising slope≤100 mA/µs. Preserve required pull-up, clocks and host resume/reset response; remote wake and light/deep/Stop modes are excluded. Blanking or disconnect is not a substitute for compliant suspend. |
| Whole-port current | Include every visible load, leakage and termination in every supply/reset/boot/fault state. MCU sleep numbers, JP3 measurement, an absent J2 cable or a disabled RF driver do not remove the U585 sensors/radio/regulators/LEDs or S3 bridge/LED/regulator loads. Neither complete kit is declared to fail or pass suspend. U585 TCPP's0.7 mA VBUSc maximum row is specified at5 V, not a5.5 V aggregate-port bound. |
| Capacitance/inrush | Device Capacitance ECN requires1–10 µF effective VBUS capacitance across its stated0–5.25 V range, powered or unpowered; the later VBUS ECN raises upper supply limits to5.50 V. Larger visible downstream capacitance must meet USB2's10 µF/44 Ω equivalent attach load and330 mV hub-droop requirement. Type-C not-Attached.SNK exposure≤10 µF remains. Nominal fitted/DNF capacitor labels, a switched-off gate or published kit drawings do not prove effective connector-visible capacitance/inrush over voltage/temperature. No extra capacitor/limiter is added here. |
| Local power absent / VBUS absent | Never source upstream VBUS, power a data pull-up without VBUS, use an I/O clamp as a supply path or claim a floated pin is safe isolation. Include slow/unequal rises, falling rails, external display/contact power, USB protection, programmer, reset/ROM and clock-loss states. U585 independent-data-removal property is unsatisfied; S3 conditional fixture must meet its autonomous fail-off and backfeed contract without firmware. |
| Reset/boot/clock loss | Stop requests and invalidate epochs/approval. External display blank/reset/select safety is autonomous under the already allowed display-interface contract; it is not implemented by the GPIO request alone. Neither watchdog, SOF timeout, bus reset, flag or status read proves physical unplug or complete secret/optical erasure. Reset domains and S3 brownout-selector conflict retain C03/C04 gates. |
| Resume/reconnect | No pending approval/result/session survives. Requalify exact clock/time, transport/state, inputs released, complete display rewrite and local fresh confirmation. Meet protocol recovery timing rather than relabel an arbitrary long reset as readiness. No secret before every source/owner/entropy/display/custody gate. |

S3's conditional fixture remains exactly its existing finite contract: GPIO8
only, rising3.90±0.05 V/falling3.30±0.05 V, independent local-rail validity and
≤1 ms autonomous data isolation, upstream fixture draw≤0.50 mA and isolated
per-line leakage≤1 µA. These are proposed implementation requirements, not
component guarantees. Fixed self-power capability/status or a required standard/
class response mismatch **rejects** that route. The fixture does not waive
unavailable OTG semantics or select CDC; no alternative protocol is opened.

## Nonvolatile writes and interrupted power

Ordinary host sessions allocate no persistent identity/PIN vault or automatic
flash write. A USB request, heartbeat, successful nominal boot or a brownout
flag does not authorize one. Firmware updates belong to C04's dedicated
owner-authorized no-secrets state with bounded image/slot/floor behavior.

Before any later erase/program/floor/option/eFuse procedure, establish the exact
part-specific programming voltage, temperature, timing, current/source and
power-sequencing prerequisites in a reviewed implementation/procedure. On-chip
BOR/PVD/UVM thresholds below3 V do not prove the S3/module/USB normal3.0–3.6 V
rail or enough energy to finish writing. No capacitor hold-up, atomic write or
safe in-progress reset is assumed. A new invalid/unknown rail forbids starting
another write; interruption still requires complete checked page/slot/journal/
counter recovery. Do not automatically repeat an ambiguous irreversible action.
The U585 raised-floor journal and S3 helper/status/fuse ambiguity retain their
strict pre-secret stop; no below-floor fallback or stale persistent approval.

## Two existing H03 power-chain investigations

These concern the future custom Board, not retrofit power for either kit. Keep
exactly the already retained protected1S Li-ion/Li-polymer hypotheses; no cell,
charger configuration, exact OPN or PCB is selected. LiFePO4 and a third chain
are outside this table.

| Chain | Reason to retain and finite decision gates |
| --- | --- |
| BQ24074 + TPS63802 fixed3.3 V | First investigation for simpler hardware control and documented absent-battery path. BQ24074 initially limits the output-short test to100 mA, then reads EN1/EN2/ILIM; USB100 is EN2=0/EN1=0,500 mA EN2=0/EN1=1 only after permission. Suspend requires its actual hardware-safe input state. DPPM prioritizes system over charging; with no battery it cannot supply an unsupported peak from an imaginary buffer. Resolve input-limit tolerances, CE/defaults, charger dissipation, cell protection/cutoff and all actual rail/thermal/transient budgets. The vendor's inrush example is not whole-design USB compliance. |
| BQ25628 + TPS63802 where3.3 V regulation is required | Retain only if measured load/thermal benefit justifies switching/control complexity. It is **BQ25628 ILIM**, not BQ25629 D+/D− detection; initial/adapter-removed IINDPM is3.2 A, not an allowed default USB load. Any I2C write enters host mode/watchdog; expiry returns selected settings to defaults and halves ICHG. Safe hardware current/charge/default policy must survive missing firmware, reset, watchdog and I2C fault. A later software setting or watchdog feed is insufficient. OTG/source/bypass charging modes remain excluded. |

TPS63802 MODE must not float. Its soft start/load dependence, repeated thermal
restarts and reverse-boost energy back toward its input require explicit lifetime
analysis; it is not an isolation diode. PG at95% rising/typically90% falling is
not an authenticated rail-valid/write-hold-up signal or source of user consent.
Exact lower-cell startup, protected cutoff, feedback/inductor/capacitors, ripple,
current/efficiency and complete backfeed/USB-suspend behavior remain H03 gates.

At the existing module's specified3 V/15 mA logic point plus15 mA backlight at
13.6 V, the calculated input-to-load power is45+204=249 mW **before** regulator/
driver losses, MCU, controls and SE loads. It is neither a full display maximum
nor a battery/runtime/USB budget: the backlight's25 mA limit has no corresponding
Vf maximum established here, and the raw module startup/rail prerequisite remains
unsatisfied. A label such as “2 A regulator” cannot close those missing budgets.

## Exact reading, later evidence and outcome

Reused selected USB2/Connect/Suspend/Capacitance/VBUS/Type-C source clauses are
already pinned. This increment rereads USB2 physical199/204–207 selected function
power/suspend/inrush text and complete Capacitance/Suspend ECNs; unrelated hub/
HS table context is not selected. UM2839 pp15–18 and TCPP pp6–8/10–14 plus current
PWR_UCPDR pp458–459 are read/reread for the exact tables above. Existing native
kit sheet9 and S3 sheet2 supply branches are reread; other CAD/assembly variants
are not audited. SGM2212 pp1–6/10–11 text is newly read (other-package context
encountered, no new native-figure/package audit). TI selected prior scopes are
reread: BQ24074 pp19–22, BQ25628 pp21/37–38/46, TPS63802 pp11–12. No market,
power-controller driver, new host or alternative transport reading is opened.

The new installed-part source is the
[official SGM2212 RevA.2 PDF](https://www.sg-micro.com/rect/assets/54089b71-cc25-4f36-af2e-34b07f00a108/SGM2212.pdf).
Exact URLs, original hashes, reading scopes and claims for all retained sources
are in [the register](manual-register.json) and [claims](claims.json).

H02/H03 evidence must name received board/marking/revision/jumpers, source,
cable/port/fixtures/instruments/operator and reviewed procedure, then retain
raw waveforms/current/captures and failure outcomes. Include permitted attach,
no-power, unequal/slow ramps, VBUS-only/local-only, held reset/ROM/clock loss,
suspend/unconfigured activity, resume, flood/stale status, source current limit,
cell absent/empty and every allowed write interruption. No such evidence exists.
User-reported generic kits do not identify this retained S3 or a ready bench.

Finite C09 source assessment is complete with the named unsatisfied interface
properties and later qualification conditions. **The power/interface criteria
are not satisfied and neither connected host configuration is admitted.** C10
must preserve that result in each of the six rows rather than turn a complete
requirements table into a working-system claim.
