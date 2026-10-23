# Finite two-host supply, startup, watchdog and interrupt contract

Author `/root/h01_sol`, 20 October 2026, after `e589c1e`. This completes a
bounded C03 **source/requirement table**, not an effective startup binary,
qualified clock, implemented watchdog, valid USB transport or admitted host.
The existing clock calculations remain conditional. C04 binds boot/owner/update
authority and retained state; C09 binds the complete power/attach arrangement.
Every prerequisite stop remains in force before dependent H02 operations.

## Fixed operating states and supply limits

Both application proposals use fixed active clocks, one trusted image and no
dynamic frequency change, Sleep/Stop/Standby/Shutdown, light/deep sleep or
tickless power management while an operation/review exists. Idle does not imply
USB suspend-current compliance. A suspend/reset/disconnect invalidates the
operation, parser and consent; the C09 contract governs subsequent power and
reattachment. A sleeping implementation needs another reviewed configuration,
not an inherited wall-clock or memory guarantee.

| Property | U585 kit proposal | S3 kit proposal |
| --- | --- | --- |
| Core/bus clock | Existing MSIS nominal48MHz, calculation45–51MHz, HPRE/PPRE1/2/3 divide1; no PLL or software trim. | Existing40MHz crystal→PLL480→CPU160/APB80; fixed SYSTIMER UNIT1 polling allocation. No new timer or clock lead. |
| Regulator/latency | PWR_CR3.REGSEL0 selects LDO, FSTEN0; VOSR.VOS=`01` range3, BOOSTEN0, wait/read VOSRDY. Flash latency2/non-low-power and SRAM latency0 under the existing envelope. U585-absent HS booster fields stay reserved. | Retained module/kit supply, factory flash/PSRAM voltage and pinned CPU clock policy. Do not change VDD_SPI, trim or voltage fuses to satisfy another module's assumptions. |
| Normal supply | VDD within selected DS conditions; proposed kit3V3 path separately bounded in C09. **VDDUSB3.0–3.6V** before USV1. HSLV remains0. IO2SV0/ASV0 keep unused PG[15:2]/analog paths isolated; do not infer a low isolated input is a physical contact state. | Applicable module/chip input rails3.0–3.6V, rated supply capacity is not USB current permission. DS DC levels are specified at3.3V/25°C/high-impedance load; exact actual rail/load qualification remains. |
| Voltage monitoring | Propose BOR_LEV4, PVDLS6/PVDE1 and UVMEN1. BOR4 falling2.67–2.90V, PVD6 falling2.76–3.00V, UVM threshold1.15–1.28V. These do **not** prove a valid USB3V rail. | TRM brownout default threshold is nominal2.7V, below the normal3.0V minimum. Detector enable alone is not an established reset policy: TRM p576 and register10.51 p623 reverse BROWN_OUT_RST_SEL meanings. No polarity/reset scope or alternate mode is selected by deduction; exact applicable semantics, effective mode/threshold/readback and usable rail remain pre-use gates. |
| Reset input | DS NRST requires ≤0.3VDD low/≥0.7VDD high; source filter/no-filter pulse bounds remain as read. Proposed controlled reset low≥1ms only with known valid rails/fixture and supported pin behavior. | DS Table2-13 requires rail stabilization≥50µs before CHIP_PU release and reset low≥50µs; proposed fixture reset low≥1ms and strap hold≥3ms. Fitted10kΩ/1µF RC/auto-program is not an exact reset waveform or exclusive owner proof. |
| Clock qualification | LSE/CRS reference condition remains false until load/aging/temperature/accuracy/USB jitter conditions close. LSESYSEN/ready needed for CRS distribution. No RTC operation, TAMP route or additional LSECSS feature selected here. | Crystal/reference condition remains false; module±10ppm annotation is not the complete factory/aging/PLL/PHY bound. No RC-derived USB accuracy or latency guarantee. |

USV is a software supply-valid assertion which removes isolation, not a voltage
measurement. UVM's low threshold cannot justify setting it at an invalid rail.
PVD/BOR indications cannot guarantee enough time for a flash write or establish
that independently powered display/USB pins are safe. C09's bounded valid supply
and external fail-off/absence/backfeed obligations remain necessary. No voltage
margin, regulator, external supervisor or physical measurement is invented here.
All quoted U585 Table35/86 characterization/design conditions remain explicit.

The S3 brownout reset-scope property is **unsatisfied**: §10.3.4.4 p576 says
selector0=chip/1=system, while Register10.51 p623 says1=chip/0=system. Do not
repair the text by assuming a naming convention, copy a software value as
normative proof, or select mode1 to evade the question. Register10.63's FIB_SEL
prose does not specify a complete alternative detector contract. H02 must stop
operations requiring the unresolved behavior until corrected applicable source
or separately reviewed, finite, safe diagnostic evidence resolves it. This is
source triage, not a completed power/reset criterion or a diagnostic permission.


## Progress watchdog requirements

Watchdog reload belongs to the trusted foreground progress owner. A verified new
parser step, completed row/chunk, completed bounded wait/state transition or
validated update-journal step may advance a progress token. An interrupt,
poll iteration, host traffic, elapsed wall time, repeated failed retry or idle
callback does not. Feed only after checking source/time/fault/epoch state; normal
progress must return control within250ms. The watchdog is neither a trusted
clock nor hostile-firmware isolation; write protection prevents accidental edits.

| Control | Finite proposal and source meaning | Limits before use |
| --- | --- | --- |
| U585 IWDG | Software mode; LSIPREDIV0, PR3 (divide32), RLR999, WINR0xFFF/no window, EWIE0. Start/configure once, wait PVU/RVU/WVU/EWU clear with500µs **and**8192-iteration proposed refusal limits after a qualified time base; verify/readback, reload through KR and relock. No periodic EWCR or WINR writes. | DS Table86 LSI30.4–33.6kHz across stated conditions is characterization, not measured unit accuracy. Table623 update max6 kernel periods gives197.37µs at30.4kHz;500µs is an engineering allowance, not a successful startup guarantee. Pending status or exhausted guard refuses intake. |
| U585 watchdog interval | A conservative count calculation uses998 prescaled periods for an early bound and1000 plus max refresh delay(2 kernel periods+1 prescaled period) for a late bound: about0.95048–1.05375s under the LSI conditions. | This is a conditional count/delay envelope, not measured reset propagation or security assurance. LSI failure, reset domain, startup initial counter and debugger behavior need qualification. No feed at a late/unknown counter. |
| U585 EWI/debug | EWI/NVIC IWDG IRQ stays disabled; EWCR writing also reloads the counter, so acknowledging a repeated EWI could defeat intended reset. Owner-secured debug freeze is forbidden; developer debug is a different state. | No “clear EWI but do not feed” assumption. Option/software mode and ROM watchdog behavior are C04 conditions; no options are executed here. |
| S3 MWDT0 | APB80MHz / prescale40000 = nominal2000Hz; stage0 hold2000, action3 **main-system/core reset**, stages1–3 off, no watchdog interrupt; reset-width proposal7 uses the TIMG table's3.2µs. Software takes explicit ownership after flash-boot protection handoff. | Nominal1s is conditional on APB/reference. An APB/CPU clock failure can stop this counter. It does not reset RTC/PMU; retained state must be rejected/cleared at startup. Actual IDF task/interrupt WDT and feed callsites must not compete with this owner. |
| S3 RWDT | Separate RTC slow default RC source, selector0 and unchanged default divider. Propose stage0 action4 **main-system+RTC/PMU reset**, stages1–3 off, pause-in-sleep0. Effective stage0 count544000 ticks; read EFUSE_WDT_DELAY_SEL=d and require HOLD=544000 /2^(d+1), d0..3. Preserve/read back reset-length fields; their actual pulse/propagation still needs qualification. | Nominal4s at typical136kHz is **not a guaranteed time range**. No manufacturer min/max bound for that RC source is established here; no clock-loss reset deadline is qualified. This count requirement cannot be advertised as a supported timed recovery guarantee. No fuse change or calibration feature is introduced. |
| S3 protection/super WDT | MWDT/RWDT modifications/feed require their documented key0x50D83AA1, then relock. Clear their flash-boot modes only as part of a reviewed handoff which leaves the selected protection active. Super-WDT auto-feed is not application progress and receives no such credit. | ROM/framework boot feed/disable behavior, actual flags, default reset modes and effective single-owner path remain H02/C04 evidence. No new SWD mode or automatic-feeding workaround is selected. |

Neither foreground feed loop may run inside an IRQ/critical section to keep a
stalled application alive. Failure first invalidates output authority; no extra
identity operation or speculative NV write is attempted. A reset does not prove
secret erasure or successful optical blanking. The external blanking/reset
contract must cover startup, absent/invalid rail and clock loss independently
of a functioning handler; its implementation is still unqualified.

## Interrupt and contact allocation

U585 uses secure VTOR/handlers and the four implemented priority bits, proposed
AIRCR.PRIGROUP3 (four preemption bits, no subpriority), PRIS0/BFHFNMINS0 and
secure fault/reset control. Proposed encoded priorities are multiples of16.
Faults capture only bounded necessary status, invalidate the epoch, stop feeding
and request a secure system reset; they never acknowledge success, log secrets
or continue crypto. ECC corrected errors also fail the operation/reset; no
continued workload depends on leaving an ECCC flag latched. NMI/HardFault/
SecureFault are not ordinary maskable peripheral IRQs.

| U585 source | IRQ / proposed priority | Handler and enable contract |
| --- | --- | --- |
| PVD/PVM, RAMCFG, FLASH_S, GTZC |1/5/7/8, priority0 (0x00) | Enable only source-specific selected fault conditions after ownership/status initialization. PVD uses EXTI16; UVM EXTI19 remains fault-only, not3V-valid proof. Captured flags/reset; no reserved all-ones clear or ordinary recovery. |
| RCC_S and CRS |10/74, priority1 (0x10) | Ready/error/CSS masks are limited to the selected clocks. CRS sync/error/miss invalidates the operation and USB clock qualification; no silent reference switch. Source-first status/clear according to existing field contract, then fail/reset. LSECSS125 stays excluded because its RTCSEL/tamper/EXTI lifetime was not selected. |
| Selection/cancel PE7; separate consent PD15 |18/26, priority2 (0x20) | EXTI7→portE=4, EXTI15→portD=3; EXTICR2/4 top bytes only. Both edges, selected captured RPR/FPR W1C, bounded change/cancel latch, no approval in ISR. Proposed50µs ISR cap and flood→failed review. |
| OTG_FS |73, priority3 (0x30) | Existing C06 masks and bounded4-pop/256-byte/200µs service, no crypto/display/log/allocation. Conditional only; OUT64/68 blocks actual admission. |
| Polling/excluded sources | IWDG27, I2C2_EV57/ER58, SPI1 59, RNG94, UCPD106, ADC4 113, TIM2 45 and other unused masters | Peripheral source enable and NVIC enable both absent for the selected polling/excluded paths. Relevant status is still checked in finite foreground work. No DMA/helper constructor may enable them implicitly. |

EXTI's mux chooses one port per pin number. PC0/PB0 and PA7/PE7 therefore
cannot each supply independent simultaneous same-number EXTI histories. The
proposal polls **all six** contacts at≤1ms during idle/render and uses only
PE7/PD15 edge latches during opaque work. Directions are not interpreted as
approvals and do not promise a complete edge history during that work. Selection
cancels; consent state is frozen/bound after the qualified press and subsequent
unexpected PE7/PD15 changes invalidate pending output. Before every new review,
all controls need a new20ms stable release and20ms stable press qualification.
No old held control or lost/coalesced event grants authority.

Selected EXTI security/privilege bits7/15/16/19 are secure/privileged; set other
implemented GPIO/power/clock routes consistently with the existing exclusion
manifest, preserve reserved fields and lock EXTI_SECCFGR/PRIVCFGR via LOCKR only
after readback. LOCKR does not lock output data or turn pending bits into an edge
counter. During trigger/mux writes an edge can be lost: initialization has no
valid consent; resample/clear while masked, then require release. Do not use
software-triggered events as physical-presence evidence.

For S3, propose CPU0 level1 line0 for GPIO source16, level1 line2 for fixed-USJ
source96, and level3 line23 for selected PMS/cache fault sources56,84–88,93/94/98.
These are **allocation requirements**, not observed allocator results. No
external-source NMI, CPU1 owner, shared transport handler, unreviewed RTOS/timer
or RF interrupt is admitted. CPU1 remains reset/clock-gated. Other unselected
peripheral sources map to an internal-interrupt number such as6 to disconnect
them; writing zero would route to CPU interrupt0, not disable them. Any required
framework/source collision must be resolved in the effective H02 image before
use; a broad IDF default configuration is not selected by this table.

S3 GPIO retains the C07 one-snapshot/six-callback/50µs change-latch contract.
USJ retains its finite FIFO/buffer/error/writer contract and stays unselected.
Fault handlers use a bounded snapshot and fail/reset; first-fault latches and
zero/deadbeaf reads are not successful accesses. The interrupt matrix status is
not a child-peripheral acknowledgement. Effective CPU special-register masks,
vector/call placement, cache-disabled execution, critical sections and allocator
must match the final map. Unread framework callees receive no implicit approval.

## Startup order and finite time policy

1. Begin with no application input/result authority and no secret load. Establish
   trusted vectors, reset cause and C04 boot/lifecycle state, valid normal rails,
   external default-off display and source/attach refusal gates. ROM/download
   behavior is not application control. Before a qualified timer exists, hardware
   waits have finite iteration refusal guards, not claimed wall-time guarantees.
2. Apply the existing memory/master/owner manifest and clear all allocated
   sensitive/retained scratch before accepting input. Do not call a broad global
   HAL initialization and assume unwanted DMA/IRQ/radio paths remain excluded.
   Configure flash/regulator/clock in safe order and check actual readiness and
   frequency-source status before shortening delays or using USB.
3. Establish the existing exclusive polling time base. U585 SysTick has no
   interrupt and must be sampled within200ms, with one qualified active clock;
   an opaque backend must have a demonstrated≤200ms bound before use. A watchdog
   not firing does not prove no24-bit wrap. S3 UNIT1 reads retain64-poll/two-attempt
   refusal guards, not successful latency guarantees. No counter is a wall clock
   across halt/sleep/clock change or unread unknown elapsed time.
4. Configure/read back watchdogs and sole feed ownership. Proposed U585 per-flag
   VOS/MSI/LSI ready refusals10ms, LSE400ms and CRS qualification64ms apply only
   when the corresponding qualified time conversion already exists. Earlier
   bootstrap readiness uses a proposed65536-iteration refusal cap per flag;
   it receives no millisecond guarantee from the later45–51MHz clock. S3 uses
   the already specified bounded PLL/read attempts with total proposed500ms
   startup allowance. These are refusal budgets, not manufacturer lock/startup
   maximums. No chain of retries extends the permitted attach deadline.
5. Set safe GPIO latches before output enable/mux, PH13 UART isolation and
   pre-intake Wi-Fi reset; retain the external-radio limits. Configure input/
   EXTI/IRQ ownership, clear captured stale state, read back and lock the selected
   attributes. No accepted input exists during this sequence.
6. Initialize bounded transport and display only if all independent source,
   descriptor/class/identity/power/startup conditions pass. USB's≤1s attach-ready
   proposal is separate from screen-ready; panel rendering/settling may continue
   with all secret operations and consent disabled. No actual U585 enumeration
   passes the unsatisfied OUT gate, and S3 fixed-CDC remains unselected.
7. Enable fresh framed intake/review only after valid clocks/owners/source state,
   normal supply, complete render/optical qualification and stable release. At
   output, recheck the immutable operation/session/display generation and all
   latched faults/cancellation. Any timer/ref/reset/USB/display/entropy/power
   failure discards the entire operation, never a weaker provider or retrying
   signature. C08 entropy-dependent use still stops before qualification.

Critical sections have a proposed20µs bound and cannot cover a transaction,
backend, delay, loop or flash erase. The stated ISR/service/refusal budgets need
real effective-build timing and flood/priority/clock-failure evidence; no source
reading measures them. Bounded handlers and firmware guards do not prove
availability after physical clock loss. C04/C09 bind update/retention and complete
power behavior; later H02/H03 must test named positive and negative cases with
public fixtures and identified resources. No target code, register write,
watchdog/flash/fuse operation, USB enumeration or physical test occurred.

Fresh/reread scope is finite: DS U585 Table35 pp163–164/LSI Table86 p226;
current RM PWR406–407/449–452 and selected status fields, selected IWDG
pp2563–2573/Table623, EXTI921–924/926–934 and used NVIC entries18/26/125.
S3 RTC source/DC/reset DS30/42/64–65; TRM574–576 brownout (nearby unused supply/
power-state context encountered), RTC607–608/613–616/623 and selected633 field prose, TIMG665–668 selected
watchdog field prose, §13 functional675–677 reread, interrupt source/type/
routing Tables9.3-1/2 pp540–546. No native new figure, whole register-map,
calibration feature or general RTOS/driver audit is claimed. Older exact scope
and source hashes remain in the register; fetched/read are distinct.

## S3 BOD selector: single next-source gate, 23 October 2026

Owner `/root/b01_final_review`, Sol6.1/xhigh. Input hardware
`7645554985259222e606fdda01bb1fdd793804ee`. This is a bounded proposed
source-resolution contract for the existing C03/S3 brownout row, not a new
host, selected polarity, diagnostic permission or H01 closure.

The retained primary TRM1.8 PDF was rehashed to
`4484bf8a69035ec42a731c58c64ada6fbd1f1618c5559409f134d9ea083f444f`
(15,215,232 bytes). Its selected text was reread: §10.3.4.4 p576 maps
0 to Chip Reset and1 to System Reset; Register10.51 p623 reverses that map.
This confirms the existing contradiction, not current corrected semantics.
No manufacturer original is redistributed and no full-manual reread is claimed.

One opening of the same [official public TRM URL](https://documentation.espressif.com/esp32-s3_technical_reference_manual_en.pdf)
returned a web-tool size error: `(400) Content length is too large: 10485761+`.
No new original/revision/hash was obtained. This is an extraction/tool-size
limit, not an observed publisher access denial or a new S04 gate. That first
attempt remains in the existing register and8937e879; no alternate route/model
or request to the manufacturer followed.

The coordinator then explicitly authorized normal file retrieval of this same
already-admitted official URL. One `curl --fail --location --proto '=https'
--max-time 60` download returned HTTP200,15,215,232 bytes, the same SHA256 above,
and `cmp` against the archived primary returned0. Targeted `pdftotext -f576
-l576 -layout` and `-f623 -l623 -layout` extractions confirmed both definitions;
their SHA256 values are recorded with the retrieval. **Current primary bytes
are identical and the polarity remains UNSATISFIED; the source question stops.**
No other document/vendor route is opened and no driver is chosen as authority.

Independent conclusion conditions are fixed now: (a) corrected primary bytes,
revision and applicability explicitly establish one consistent0/1 map across
both locations, allowing only this documentary row to be reassessed; or
(b) contradiction, ambiguous applicability, inaccessible body or absent
correction leaves the row UNSATISFIED with selected_polarity null. Neither
outcome admits a connected host, valid rail, threshold, received revision,
reset waveform or physical reset scope. RAM loss under undervoltage must not
be relabelled proof of a particular reset domain.

### Next diagnostic proposed for review, not executed or admitted

Use a tiny public C probe with the already pinned ESP-IDF
`fff9895c82d744c7237be8847347bdd1b07c6643`, not a general Rust port.
Proposed source is `diagnostics/s3-bod-selector/main.c` with one checked
compile-time selector0 or1; no such source/build is created by this checkpoint.
The future project must bind that value to the actual `BROWN_OUT_RST_SEL`
field, expose raw readback and refuse other values. Proposed compile commands:

```sh
idf.py -C diagnostics/s3-bod-selector -B build/s3-bod-0 -DIDF_TARGET=esp32s3 -DBOD_RST_SEL=0 build
idf.py -C diagnostics/s3-bod-selector -B build/s3-bod-1 -DIDF_TARGET=esp32s3 -DBOD_RST_SEL=1 build
```

These are build-only commands after separate admission and verification of
the pinned SDK/toolchain/configuration; no flash/monitor/erase/fuse/security
transition is implied. No installed toolchain, target binary or safe boot path
is claimed. Both builds use the same source/configuration except selector/test
identity; generated code/map/readback effects and absence of auto-provisioning
need review. No byte-equivalence/reproducibility of the binaries is assumed.

The proposed public marker is **the GPIO46 strap latch**, not SRAM retention.
The same TRM §8.1 p534 specifies sampling at Chip Reset; Reg6.15 p506 maps
GPIO_STRAPPING bit2 to GPIO46 (RO). Table8.2-1 p535 permits SPI Boot with GPIO0=1
and GPIO46 ignored. Preserve all other straps and their electrical owners.
Start with GPIO46 low at a controlled initial boot, verify latched bit2=0,
then apply an external high level and verify live input1 while the latch stays0.
Hold GPIO0 high throughout; no flash-voltage strap or debug/boot configuration
is changed. Read UART_PRINT_CONTROL first: GPIO46-dependent01/10 is a stop
for this witness; require an already fixed00/11 state, without any fuse write.
The probe records selector/readback, live input, latched marker
and raw reset causes before/after, without authorizing a host mode or keys.

Before BOD cases, the witness must distinguish an identified Chip Reset control
from the already bounded RWDT System Reset control at valid rails. TRM7.1.4/
Table7.1-1 pp527–528 identifies those types; a raw BOD cause0x0F alone cannot
distinguish them. Required control outcomes are resampled latch1 for Chip Reset
and retained latch0 for System Reset. If either control fails, stop as
NOT_DISCRIMINATING rather than assigning a polarity.

Only a separately reviewed bench procedure may then apply the same qualified
BOD stimulus to selector0 and1, keeping mode0/other fields fixed and read back.
Independent predictions, before observations: the p576 hypothesis yields
after-latch `[1,0]`; the p623 hypothesis yields `[0,1]`. Any other pair,
unconfirmed BOD cause, unintended power-down/POR/CHIP_PU transition, changed
pad before stimulus or missing capture leaves UNSATISFIED. A matching pair
would support only that exact received silicon/configuration, not all S3s.

Bench admission still requires identified board/module/silicon/ROM/security
state and reviewed startup path; GPIO46 accessibility/load and all straps;
an approved current-limited supply/stimulus and independent rail/CHIP_PU/pad
waveform capture proving the event was not power loss or uncontrolled reset;
safe observation/isolation without presuming USB attach, powered-off I/O or
valid operation during undervoltage. Exact levels/timing/instruments/operator
must be fixed before energizing, not guessed here. Existing access/advisory
gates remain. No RAM-loss inference, alternate detector mode or driver result
can replace these controls. This is the single proposed follow-up experiment.

No source build, board/flash/register/fuse write, energizing, secrets,
purchase/outreach, SDK/Pi/CAD or canonical graph change is part of this packet.
The original43-test `make ci` evidence stays bound to its recorded85c77cc
content; it was not rerun or relabelled for this contract-only checkpoint.
All other C01–C10/access/advisory/physical gates and historical reports remain.
