# Two-host entropy and software-crypto contract

This completes a finite C08 source-to-contract table for the retained U585/S3
paper workload. It does not qualify either provider, accept generated entropy,
or remove the source/implementation stops below. The coordinator's U585
allocation permits conditional documentary reading/triage only. The complete
two-host configurations and six-row acceptance still require the other
checklist items and distinct final review.

The authority is the original core input7b5553685dac56029a4379be12054154b6b5e0b5:
[S02 entropy contract](https://github.com/nSealr/nsealr/blob/7b5553685dac56029a4379be12054154b6b5e0b5/docs/restart/implementation/S02/entropy-contract.md),
[software-crypto selection](https://github.com/nSealr/nsealr/blob/7b5553685dac56029a4379be12054154b6b5e0b5/docs/restart/implementation/S02/crypto-selection.md),
[secret flow](https://github.com/nSealr/nsealr/blob/7b5553685dac56029a4379be12054154b6b5e0b5/docs/restart/implementation/S02/secret-flow.md).
Their recorded hashes were rechecked from the pinned Git objects; later core
main changes are not silently substituted. No historical test was rerun.

## Common finite adapter requirements

| Boundary | Required behavior for both hosts |
| --- | --- |
| Intake/return | One fallible, all-or-error fill into caller-owned zeroizing internal memory. Accept only the full requested output after all source/state/status checks. Every error wipes the entire destination, including an already filled prefix. Never expose partial bytes, reuse old bytes, or turn failure into success through a trait adapter. |
| Initial qualification bounds | Proposed H01 probe limits: one32-byte fill, at most100 ms including all its setup/read/cleanup waits and the caller's remaining absolute budget; scalar generation at most8 full draws and200 ms total. These are finite qualification limits, not measured product maxima or guarantees that an unqualified provider will succeed. C05/profile measurement and review must bind final effective limits. |
| Scalar handling | Sample a full32-byte candidate, reject zero/out-of-order secp256k1 scalars, never reduce a random integer modulo the group order. Exhaustion yields `RejectionLimit`. A syntactically valid scalar proves no entropy quality. |
| Purposes | Separate requests/ownership for identity generation, session material, BIP340 auxiliary data and NIP44 nonces. Never replace failed auxiliary randomness with zeros because an algorithm accepts fixed data in a test. No new wire format, RNG, DRBG or backend is introduced. |
| Concurrency | One provider owner, one in-flight fill; S3 owner runs on one fixed core. No ISR, second core, task or framework source reconfigures clocks, SAR/RNG controls or its sampling state concurrently. Explicitly audit the shared analog/clock resources, rather than taking a mutex only around the destination. |
| Failure | Preserve `Unavailable`, `HealthFailure`, `Interrupted`, `ProviderFailure` and `RejectionLimit` operational distinctions without recording random bytes. Any observed source/health/clock fault aborts this operation with **zero recovery retries inside the fill**. Reinitialization belongs to a separate finite recovery state with fresh authority; it cannot salvage a partially generated key or old consent. |
| Reset/sleep | Reset, cancellation, owner/account change, transport fault or any excluded power/clock transition invalidates the fill and pending operation. Start with an empty destination and unqualified provider after reset. No retained RNG/FIFO state is treated as a reseed or a fresh authorization. |
| No fallback | No RC-only SDK shortcut, MAC/clock seed, cached output, fixture flag, weak symbol, infallible unwrap, panic-to-success or unseeded software generator. Public deterministic providers are confined to separate test/probe builds; a custody image cannot switch to them at runtime. |

The named100/200 ms limits require the already bounded host time/IRQ policies
and remaining overhead budget. They do not make an unbounded nested vendor
call finite. H02 must implement the reviewed finite remedy, including startup,
conditioning, sampling, cleanup and every blocking dependency, and demonstrate
normal supported success as well as refusal. Watchdog/reset recovery is not a
successful return or an erasure proof.

## U585: nominal manufacturer reference, conditional only

AN4230 Rev14 §5.1.3 Table3 gives STM32U575/585 nominal48 MHz reference values:
`RNG_CR=0x00f00d00`, `RNG_HTCR=0x0000a2b0`,
`RNG_NSCR=0x00017cbb`. RM48.6.2 points to that product-specific table.
The E11 v1.1 assessment lists CPU/AHB160 MHz,25°C,3.3 V and HSI48 kernel48 MHz.
The current paper CPU/AHB45–51 MHz, real HSI48/CRS envelope and received
silicon/profile conditions are **not demonstrated to conform**. This reference
is not a qualified configuration for that proposal and does not make any RNG
output acceptable.

| Item | Required documentary correspondence / refusal |
| --- | --- |
| Clock and attribution | RNGSEC and its RCC source/reset/gate ownership are in the secure manifest; access is32-bit only. Record actual HSI48 source, HCLK, divider, allowed silicon, voltage and temperature before use. CED checks a too-slow kernel before its internal divider; it does not establish the clock's accuracy or a complete source assessment. |
| Configuration | Program only the product reference fields while disabled, CONDRST asserted and CONFIGLOCK clear; NSCR/HTCR writes have those prerequisites. Preserve reserved bits. Read back the complete intended policy before locking; a later central RCC reset loses it and requires full reinitialization. With nominal reference fields, polling IE0, active-low CED0, ARDIS0 and RNGEN1, the calculated locked control value is0x80f00d04. That is a documentary correspondence, not an executed write or a qualified operating recipe. |
| Detector conflict | E11/E116 prose says set bit5 to detect a slow clock, while current RM1910/1916–1917 makes CED active-low and AN's tuple leaves it0. Preserve the conflict; follow the current register definition for the proposed detector policy and reconcile the assessment wording before any reuse claim. Do not silently invert the bit. |
| Read acceptance | Require no current or latched seed/clock errors and DRDY before each accepted word; check the documented zero-word race and status again before committing the complete destination. A DRDY bit or output while RNGEN0 can reflect buffered data; it does not establish a fresh qualified source. Zero is rejected here because this RM defines that race condition; do not generalize that rule to S3's uniform32-bit API. |
| Health/reset | Startup conditioning/known-answer and raw-noise RCT/APT/transition tests are hardware features under their configured thresholds. Any reported fault aborts the fill. ARDIS0 auto-recovery does not erase the incident or authorize reuse of earlier bytes. Conditioning reset clears FIFOs and preserves configuration; a central reset loses the configuration. Tamper error requires the documented reset/reinitialization path. Disabling RNGEN alone is not FIFO erasure. |
| Disable | Keep the documented two kernel cycles between disabling RNGEN and gating its clock or entering a deactivated power mode. Current-policy recovery/cleanup remains finite; a clock/power transition never preserves old random output or consent. |
| Pinned source | Embassy69006a4's `RngConfig` lacks NSCR, generic/reset/recovery paths can restore defaults, and its waits/zero/panic/trait adapters have the previously recorded gaps. A retry count of3 is not a time bound. Require preservation of the exact chosen tuple and fallible whole-output semantics through every reset/recovery/trait path; stock source is not selected as conformant. |

The coordinator permits this as a **conditional documentary contract only**.
H02 has an explicit STOP **before any entropy-dependent use** until the exact
clock/divider/profile/silicon/voltage/temperature, CED conflict and source
justification are resolved. Frequency measurement and simple output statistics
do not recreate the raw-noise assessment. E11's special raw interface and its
`RNG_VERR` statement do not add facilities to a standard kit/public RM map.
No certificate, entropy, component, clock or H04 selection guarantee is made.
Other probes use public fixture values, not newly generated identities.

CLKDIV1 for additional sampling-frequency margin remains outside the exact AN
tuple and is **unselected/unqualified**. No new clock or DRBG lead is opened.
If the source conditions make the proposed host tuple impossible, that remains
a feasibility blocker for the coordinator; it cannot be relabeled a later
measurement. The current record establishes a qualification stop, not such
an impossibility conclusion.

## S3: documented non-RF source and exact ownership

The versioned SDK requires an enabled main entropy source whenever true random
output is needed. RC_FAST alone and a seeded boot state are insufficient under
that contract. The retained non-RF route calls the documented
`bootloader_random_enable()` API and retains its SAR source through the fill;
Wi-Fi/Bluetooth and every application ADC/ULP user remain excluded. This
reserves internal resources; it is not a new application ADC feature.

| Source/state | Observed pinned source and required boundary |
| --- | --- |
| Startup | The normal second-stage bootloader enables then disables its SAR source before the app. Application startup therefore begins unqualified and must explicitly establish the supported source again before accepting bytes. A bootloader's earlier entropy is not an unlimited pool. |
| Enable writes | The retained S3 helper enables RNG/RC_FAST digital clocking, resets/toggles SAR bus clock, selects APB and controller divisor3 with zero fractional fields, enables internal analog-I2C/reference controls, writes internal channel10 patterns, selects both-unit conversion, digital ADC1 control, non-sleep ADC2 arbitration, SAR divider3, trigger interval70 and continuous trigger. These are observed writes, not a new source-health/readback guarantee. |
| Both SAR units | ADC1 pattern slot0 and ADC2 slot1 are written with channel10/12 dB; each pattern length is set to1. Analog reference helper accepts a unit argument but writes a common reference-enable field. Reserve both units and their shared analog controls even if only one source is required by the documented API. Do not claim every written slot is necessarily sampled or copy those indices into a new ADC driver. |
| Source correspondence limit | Native TRM1471 Figure39.3-4 places cmd0 at bits23:18, agreeing with the LL slot0 write; the example1472 instead calls bits5:0 cmd0. The public selected controller text mainly describes DIG ADC1 and does not resolve the helper's ADC2 slot1/length correspondence. Preserve these differences as qualification questions, rather than declare an SDK defect or guess a fix. The documented API supports the SAR source; exact received source/ownership/readback justification remains a stop before entropy use. |
| Conflicts | No RF, ADC driver, calibration, touch/ULP/temperature service or other analog/clock writer may contend during the source lease. The supported API explicitly warns about concurrent RF/ADC use. Clear labels such as “radio unused” or an absent application ADC call are insufficient without the effective feature/call/ownership evidence. |
| `esp_random` | S3 uses the1778-APB-cycle sampling policy, CPU/APB ratio and a static `last_ccount`. It has no source-health error return. One core/owner and fixed frequency are required; reading a word is not source readiness. Its busy wait and all dependencies need finite failure behavior; silent success from the infallible API is not the S02 adapter. |
| RTC mixing | S3 capability header sets RTC timer support. The selected HAL is a direct alias to the LL, which requests a snapshot and reads its two halves without a polling loop. It adds RTC bits to mixing; that is neither a qualified new entropy source nor a new deadline timer. No RTC alarm, sleep or fallback timing path is selected. |
| Fixed pattern | `CONFIG_ESP_BRINGUP_BYPASS_RANDOM_SETTING` must be absent/false in effective config and the linked call path. Its fixed0x5a5a5a5a branch is not a permissible fallback, even in a source-loss test. Public fixtures belong to separately identified test/probe providers. |
| Disable/recovery | The helper disables the trigger, resets pattern tables, removes internal calibration/reference controls, releases analog-I2C ownership, changes the controller clock fields and returns ADC1 to ULP control. It does not thereby prove hardware RNG state erased. No ADC/ULP/RF service is promoted by that returned state; reset/disable invalidates the lease and partial output. |

The SDK and TRM do not expose a per-read health error through the reviewed RNG
API. Do not fabricate one or claim the real hardware detects every stuck-source
mode. The adapter can refuse known unavailable/changed configuration, observed
conflict, interrupted ownership, timeout and injected provider failures; actual
physical-source quality/failure observability and the retained API/source
correspondence must be qualified separately before entropy use. Ordinary output
statistics, repeated-scalar checks or a successful function call do not close
that gate. No accepted random bytes or real identity were generated here.

## Software backend and later evidence

Retain S02's maintained **k256 0.14.0**, defaults off with `schnorr,ecdh`,
software route; sha2 0.11.0 and zeroize 1.9.1 retain their accepted feature limits.
No SAES/PKA or new hardware-crypto backend is introduced. Its raw BIP340 digest
and unhashed shared-x/HKDF requirements remain; the high-level signing API's
extra hash and libsecp default hashed ECDH are not interchangeable shortcuts.
The C alternative stays deferred with its already documented ABI/temporary-
erasure costs. S02's ARM/RISC-V links do not qualify Xtensa, any board, actual
peak RAM or target timing.

Keys, nonces, auxiliary bytes, shared-x/HKDF/plaintext and backend scratch live
only in the selected internal secret arena/stack. No external RAM, DMA,
console, crash dump or USB diagnostic receives them. The allowed P01 approved
operation outputs remain separate from internal secret state. k256 backend
temporaries lack a universal Drop-wipe guarantee; a wrapper cannot erase scratch
it never owns. K01/actual custody integration must resolve its inventory and
mitigation before real-key admission. Hardware reset, cache invalidation and
zeroizing Rust owners do not establish complete physical erasure.

H02 binds the exact application→Rust/FFI→SDK/HAL path, effective features,
aliases/archives/link order/LTO and binary/map/disassembly; a missing-provider
link must not find a weak default or fixture fallback. It instruments invocation
using disposable public fixtures without capturing real secret bytes, then
tests unavailable, short/partial, interrupted, stuck/repeated, health-error,
clock/SAR conflict and deadline cases. Expected negatives are zero crypto output,
whole-destination/pending-state cleanup and no weaker fallback; recovery needs
fresh authority. These injected outcomes do not prove universal real-hardware
fault detection. No such build, injection or measurement has run in H01.

Primary source identities and read scopes are in the register:
[AN4230Rev14](https://www.st.com/resource/en/application_note/an4230-random-number-generation-validation-using-nist-statistical-test-suite-for-stm32-microcontrollers-stmicroelectronics.pdf),
[E11 public-use](https://csrc.nist.gov/CSRC/media/projects/cryptographic-module-validation-program/documents/entropy/E11_PublicUse.docx),
[current RM0456](https://www.st.com/resource/en/reference_manual/rm0456-stm32u575585-armbased-32bit-mcus-stmicroelectronics.pdf),
[S3 RNG guide](https://docs.espressif.com/projects/esp-idf/en/v6.1/esp32s3/api-reference/system/random.html),
[S3 TRM](https://documentation.espressif.com/esp32-s3_technical_reference_manual_en.pdf),
[pinned sampling source](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/esp_hw_support/hw_random.c),
[S3 enable/disable](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/bootloader_support/src/bootloader_random_esp32s3.c).
