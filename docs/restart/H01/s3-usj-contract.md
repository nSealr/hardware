# S3 fixed-CDC contract under review

This records C04/C07 source correspondence for the existing S3 kit. It does
**not select USB Serial/JTAG**, establish an effective build, or close the S3
paper configuration. The previous [assessment](s3-usb-serial-assessment.md)
and its stock-driver findings remain applicable. C03/C09 clock, VBUS,
descriptor/current and suspend decisions remain mandatory before selection.

## Finite FIFO and interrupt requirements

TRM1.8 chapter33 pp1243–1254,1256–1268 and the pinned v6.1 register/structure
headers agree on these interrupt positions:

| Bits | Meaning and proposed handling |
| --- | --- |
| 0 | JTAG IN flush; excluded from the application CDC owner. |
| 1 | SOF; record fresh bus activity, never physical VBUS or cable presence. |
| 2 | Serial OUT packet; service at most64 bytes in one invocation. |
| 3 | Serial IN empty; enable only while a bounded TX operation needs service. |
| 4–7 | PID, CRC5, CRC16 and stuffing errors; invalidate the transport epoch, partial request/render state and pending consent. |
| 8 | IN token received; excluded from the proposed event set. A token is not application receipt. |
| 9 | USB bus reset; cancel the old application session. |
| 10 | Serial OUT zero-length packet; no data byte or application frame boundary is inferred. |
| 11 | JTAG OUT zero-length packet; excluded from the application CDC owner. |

The defined-bit union is `0x00000fff`. A reviewable proposed CDC enable set is
`0x000006f6` (bits1,2,4–7,9,10), with bit3 added only during pending TX
(`0x000006fe`). These are calculated field sets, **not executed writes or a
complete ISR**. The LL helper's `0x7ffff` constant includes bits outside this
public field set and must not become an all-bits clear/enable prescription.
The LL enum omits error bits4–7; the public register body and pinned generated
headers define them. Clear only handled, observed defined events through
`INT_CLR`; clearing the CPU interrupt alone does not acknowledge its source.
Do not mix direct ownership with a concurrently installed stock-driver ISR.

Use the FIFO availability/free status for each byte and explicit counts capped
at64. The structure intentionally makes FIFO access32-bit while only the low
byte is valid, avoiding read/modify/write of the data port. OUT pointer/count
fields are7-bit, and the manual's write-address-minus-two prose is not a safe
array length. Do not subtract unchecked pointers into a buffer index. A host
which continually refills the FIFO must not create an unbounded ISR drain.
Mask/defer bounded work with an explicit progress/deadline policy; do not spin
until a hostile host stops sending.

The hardware's full64-byte TX packet commits automatically. A partial packet
requires `WR_DONE`; after a full final packet, the LL/driver's ZLP procedure
requires waiting for free FIFO before the additional flush. Every free/empty
wait needs the same absolute operation budget. Queueing bytes, a USB IN token
or a successful driver return does not establish host receipt. Closed host
ports can leave TX pending indefinitely. RX ring enqueue failure must be
observable and cancel the epoch; the stock driver's ignored enqueue result
cannot satisfy this requirement.

Error flags do not document which FIFO bytes survive an error. Therefore the
adapter must discard partial application state on an observed link error,
rather than claim all exposed bytes were validated. Snapshot/error/clear and
queue ownership must cover races before any completed frame can become a
reviewable request. Finite frame/parser/queue limits and the versioned framing,
replay and completion semantics still bind to P01 and the later transport
contract; CDC packet boundaries, ZLPs and line coding are insufficient.

## Reset, retained bytes and writer ownership

JTAG `SRST` can reset the digital system without resetting this controller.
RTS/DTR host controls can reset or request download independently of application
consent. The LL SYSTEM reset helper is a distinct register-reset operation;
neither a CPU restart, stock install/uninstall nor a memory-power setting is a
published guarantee of FIFO erasure or a fresh host session.

Startup must accept no old request or consent. Bound any stale-byte drain,
clear owned software buffers, and require a new session/epoch before parsing
an actionable request. Retained hardware bytes remain untrusted input; an old
response cannot constitute new approval. Abort on reset, error, overflow,
deadline or lost bus activity and require complete new review plus a newly
released-then-pressed input. Reset during a response must not repeat a secret
operation merely because the host retransmits. No private identity key, seed,
internal secret intermediate or secret-memory diagnostic may enter either USB
FIFO. Bounded outputs explicitly authorized by P01, including an approved
decryption result where its contract permits it, remain distinct from those
internal secrets and require their own reviewed authorization/completion path.
This is a required adapter/protocol behavior, not an implemented handshake or
proof of zeroization.

Native TRMp1258 was visually checked against the pinned header: `MEM_CONF`
bit0 is memory power-down and bit1 is forced memory clock, with reset0/1.
These controls are not used as a zeroization remedy. `DATE` is writable and
does not identify received silicon. Test mode, external PHY and JTAG bridge
routing remain excluded. Exact reset/PHY/pad ordering and negative-case target
evidence remain H02 work after the paper policy closes.

The sensitive runtime has one application writer and one interrupt owner.
Both bootloader and application must explicitly choose primary
`ESP_CONSOLE_NONE` and secondary `ESP_CONSOLE_SECONDARY_NONE`, leaving
`ESP_CONSOLE_USB_SERIAL_JTAG_ENABLED` false while separately retaining
`USJ_ENABLE_USB_SERIAL_JTAG`. No VFS console, REPL, stdout/stderr, ROM/EARLY
print, GDB stub, panic register dump, core dump or trace writer may reach this
stream. Require the reviewed silent-panic/no-coredump/no-trace choices and
source/link exclusions for all other writers. The driver CMake forces VFS and
the monitor under console features; a source file being present does not prove
its feature is disabled or its object absent. H02 must retain both effective
configurations, linked symbols/call paths and output-negative tests before
loading secrets. No actual configuration, link map or binary is claimed here.

## Developer and owner requirements

Development may retain debug/download and cold-ROM startup text, but uses only
disposable identities. Clear application framing and wait for a fresh epoch
after that startup. A no-console bootloader suppresses ROM channels only after
ROM has already run; it cannot prove a clean cold-start CDC stream.

An owner state using CDC requires verified `DIS_USB_JTAG=1`,
`DIS_PAD_JTAG=1` (`HARD_DIS_JTAG` is the same field),
`DIS_USB_SERIAL_JTAG=0`, the required internal-PHY selection, and permanent
USB-ROM-print suppression (`DIS_USB_SERIAL_JTAG_ROM_PRINT=1`, the SDK name
corresponding to TRM output control). USB pin exchange/external-PHY settings
must match GPIO19/20 and the kit. ROM download/secure-download, signed
boot/update/recovery and rollback values remain the complete C04 policy;
JTAG-only disable does not settle them. A received whole-block disable is
incompatible with this CDC proposal, rather than a reason to weaken owner
security or invent a new transport.

The exact S3 secure-boot helper writes USB and pad JTAG disables when
`SECURE_BOOT_ALLOW_JTAG` is false; it also handles secure/disabled ROM download,
direct boot, secure boot enable and read-disable protection. The S3 flash
encryption helper disables download encryption/cache and JTAG under its
selected configuration, then requests shared cache write protection. Neither
selected chip helper writes the whole-block `DIS_USB_SERIAL_JTAG` field. That
limited source fact does not prove an entire linked first-boot procedure or
that a received device already has the required values.

The pinned CSV/header make the shared locks concrete:

| Lock in block0 | Fields relevant here and consequence |
| --- | --- |
| `WR_DIS` bit2 | Includes cache/download-cache, `DIS_FORCE_DOWNLOAD`, OTG, app CPU, pad/USB JTAG, whole Serial/JTAG, PHY selection and other fields. Desired CDC/PHY/debug values must be established and verified before locking the group. |
| `WR_DIS` bit18 | Groups download/direct-boot, USB-ROM-print, Serial/JTAG-download, secure-download, UART-print, rollback-version and flash/configuration fields. A premature blanket lock can prevent the intended later rollback policy. |
| `WR_DIS` bit19 | Includes the separate OTG-download gate and revision-disable controls; it is not the Serial/JTAG-download group. |

The complete selected CSV rows, rather than this abbreviated table, govern any
future ceremony. Provisioning order, interruption/recovery and readback belong
to C04/H02, with explicit separate authorization before irreversible activity.
Some security configuration choices arrange automatic fuse programming on a
first boot; they are not benign runtime flags. No security helper, build,
flash command or fuse operation was executed in this research. No production
key or provisioning procedure is supplied.

## Remaining selection gate

C07 still requires the exact clock/reset/startup tuple and bounded adapter
requirements, plus C09's permissible power/attach/suspend contract. J4 has no
VBUS-sense signal. Fixed descriptors also need an exact public identity/current
contract; the selected TRM body does not list `bMaxPower`. Bus-powered kit
suspend must include its shared-rail bridge, regulator and LEDs; self-power
does not permit a D+ pull-up after upstream VBUS is lost. SOF absence, reset,
timeout or a closed CDC port cannot distinguish those electrical conditions.
Light sleep gates S3 APB/PHY and can leave the pull-up asserted but the device
unresponsive; deep sleep disconnects it. Neither observation is a completed
suspend solution. Do not select this alternative until those mandatory paper
properties close or the coordinator supplies the required bounded scope
decision.

The coordinator permits assessment/specification of **one external attach
fixture** on this retained J4 path if exact whole-kit bus-powered suspend
cannot close. It may provide real bounded VBUS-valid status and fail-off
connection/control using at most a named existing-kit GPIO allocation. This
is documentary scope only: no new host, port, controller, driver, component
market sweep, wiring or energizing permission. Do not declare the kit fails
suspend merely because its whole-kit current remains unmeasured.

The fixture contract must bind thresholds, accuracy, deadlines, signal levels
and edges to the actual USB/kit/chip sources. Autonomous absence-of-VBUS
isolation must cover unpowered, power-rise, reset, boot and clock-loss states;
a GPIO and a correctly running firmware loop cannot cover a default PHY
pull-up while that loop is absent. Include upstream backfeed and data/power
isolation, leaving exact implementation/parts and measurements as H02 gates.
The subsequent [conditional attach contract](s3-attach-contract.md) now makes
one finite proposed external interface reviewable; no implementation or parts
are selected, connected or qualified. Its descriptor/status refusal gate is
independent of its threshold/isolation requirements.

Fixed descriptors remain independent: finish the existing public source
scope, enumerate missing identity/current fields and require exact
received-unit capture before any operation depending on those values. Such
a capture must check the complete device/configuration/interface/endpoint
tree, advertised power/source/remote-wake properties and actual allowed
silicon/ROM/lifecycle correspondence, with a negative result refusing the
proposed configuration. It is neither USB certification nor permission to
exceed the known safe pre-configuration supply limits. Present that finite
gap before final C07 admission; no missing normative IP semantics are waived
by the external fixture.

Sources: [TRM1.8](https://documentation.espressif.com/esp32-s3_technical_reference_manual_en.pdf),
[register header](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/soc/esp32s3/register/soc/usb_serial_jtag_reg.h),
[structure header](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/soc/esp32s3/register/soc/usb_serial_jtag_struct.h),
[S3 secure-boot helper](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/bootloader_support/src/esp32s3/secure_boot_secure_features.c),
[S3 flash-encryption helper](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/bootloader_support/src/esp32s3/flash_encryption_secure_features.c),
[eFuse CSV](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/efuse/esp32s3/esp_efuse_table.csv),
[aliases](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/efuse/esp32s3/include/esp_efuse_table.h),
[versioned sleep/console guide](https://docs.espressif.com/projects/esp-idf/en/v6.1/esp32s3/api-guides/usb-serial-jtag-console.html).
Exact hashes and selected reading ranges are in the register; originals and
the native page render remain private.
