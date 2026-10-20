# S3 same-kit USB Serial/JTAG source assessment

Author `/root/h01_sol`, 20 October 2026. Bounded assessment authorized by the
coordinator within the existing ESP32-S3-DevKitC-1-N8R8 v1.1 proposal. This is
the same host, native USB connector and GPIO19/20; it adds no bench port.
**This alternative is not selected or admitted.** The earlier OTG/CPU-FIFO
proposal and its comprehensive-register NDA boundary remain recorded.

## Public hardware contract

ESP32-S3 TRM v1.8 chapter33 pp1243–1254 provides the functional body for a
separate fixed CDC-ACM/JTAG USB full-speed device. It uses APB byte-accessible
serial FIFOs and a direct JTAG path to the CPUs. Its serial endpoints transfer
up to64 bytes per packet. Firmware reads available bytes and writes free FIFO
space, then commits the TX packet; filling64 bytes commits automatically.
Waiting for a host to drain that packet can otherwise wait indefinitely.
The public register body pp1256–1268 describes the FIFO access, status,
interrupt enables/status/clear, bus-reset and link-error events. This is a
different documentary boundary from the OTG IP in §32.5; it does not imply
that any unpublished OTG register semantics were reviewed.

The controller needs its PLL-derived48 MHz PHY clock and at least40 MHz APB
for compliant operation (§33.4.2 p1253). Light/deep sleep and runtime clock
changes therefore remain excluded from an initial active-session proposal.
These limits are requirements, not measured throughput, suspend-current or
timing results. The CDC line-coding settings are dummy requests; selecting a
nominal baud rate does not set the USB data rate.

The hardware also accepts RTS/DTR reset/download controls, and its JTAG command
processor has a system-reset path. The described JTAG `SRST` resets digital
system state without resetting the USB Serial/JTAG controller (§33.3.5 p1249).
Consequently a CPU restart is not proof that the serial hardware FIFO or pending
transport data was cleared. Application startup must begin with no accepted
request or consent and establish a fresh transport state before any byte is
interpreted. Resetting the controller through the documented SYSTEM reset
field is a separate action; its effect on the complete FIFO/host session still
needs the selected initialization procedure and H02 negative-case evidence.

Primary references: [TRM v1.8](https://documentation.espressif.com/esp32-s3_technical_reference_manual_en.pdf),
[versioned USB Serial/JTAG guide](https://docs.espressif.com/projects/esp-idf/en/v6.1/esp32s3/api-guides/usb-serial-jtag-console.html).

## Pinned driver findings

The assessment uses ESP-IDF v6.1 commit
`fff9895c82d744c7237be8847347bdd1b07c6643`. This fixes source identity; no
nSealr build, effective sdkconfig, dependency lock or linked implementation
has been established by this reading.

| Path | Actual source behavior | Required consequence |
| --- | --- | --- |
| Direct read | `usb_serial_jtag_read_bytes` waits on a byte ring buffer with the supplied tick limit and returns a count. It supplies no application-message boundaries. | A single transport owner must apply the accepted bounded frame/parser contract and absolute request deadline; no consent from a partial frame. |
| Direct write | `write_bytes` waits separately for its mutex and ring-buffer space using the same caller tick limit, then returns the enqueued count. | A successful return is not host receipt. The two waits can consume approximately twice the supplied wait interval; use one remaining absolute budget, finite sizes and fail-closed partial-output handling. |
| Completion | `wait_tx_done` adjusts the remaining timeout after taking the mutex. ISR drains queued data and issues a zero-length packet after a full final packet. | Preserve the empty/full-packet termination path and check completion; no success from merely queuing bytes. Actual host delivery remains an H02/protocol check. |
| RX overflow | ISR reads up to64 bytes from the hardware FIFO and ignores the result of `xRingbufferSendFromISR`. | A full software ring can silently discard that packet. The stock driver does not provide the required observable receive-loss/error boundary. |
| Reset/errors | ISR handles only serial RX and TX-empty events; install enables RX and later TX. It installs no bus-reset or PID/CRC/stuff-error callback. | The selected adapter must observe relevant reset/error events and invalidate partial request/render/consent state. Adding an interrupt enable without a handler can create an interrupt storm. |
| Install/uninstall | Install deliberately preserves FIFO interrupt status/data and initially assumes TX idle. Uninstall frees objects/rings but intentionally leaves clock and PHY pads enabled. | Neither API establishes a fresh USB session, FIFO cleanup, data erasure or electrical disconnect. Controller, buffers and output ownership need a separate explicit lifecycle. |
| Console VFS | Reviewed nonblocking TX can drop characters after its timeout while the VFS write returns the requested size; newline conversion and driver-backed infinite-wait paths exist. | Do not use the stock console/VFS as the bounded binary frame transport. |
| Connection helper | Its separate tick hook observes SOF, starts by assuming connected, and permits a few absent-SOF ticks. | This is a bus-activity heuristic, not proof of physical unplug, CDC-open state, VBUS presence or session cancellation. |

Sources: [driver and API](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/esp_driver_usb_serial_jtag/src/usb_serial_jtag.c),
[S3 low-level source](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/esp_hal_usb/esp32s3/include/hal/usb_serial_jtag_ll.h),
[console VFS](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/esp_driver_usb_serial_jtag/src/usb_serial_jtag_vfs.c),
[SOF monitor](https://github.com/espressif/esp-idf/blob/fff9895c82d744c7237be8847347bdd1b07c6643/components/esp_driver_usb_serial_jtag/src/usb_serial_jtag_connection_monitor.c).

An adapter with bounded direct FIFO access or a narrowly corrected driver may
be feasible. That is an engineering proposal, not an implemented remedy. It
must define overflow reporting, request/frame limits, reset/error handling,
FIFO/queue cleanup, exclusive interrupt ownership, progress-qualified watchdog
feeding and a deadline across all waits. Its exact public register fields,
effective build features and source correspondence require review before this
alternative can replace OTG. No whole-controller or undocumented all-ones
interrupt mask is inferred from a vendor helper constant.

## Console, debug and lifecycle conditions

The pinned `esp_stdio/Kconfig` defaults the **secondary** console to USB
Serial/JTAG. Choosing another primary, or merely selecting no primary console,
does not establish exclusive byte-stream ownership. The proposal would require
explicit primary `ESP_CONSOLE_NONE` and secondary `ESP_CONSOLE_SECONDARY_NONE`,
with USJ enabled separately for the chosen transport. Both bootloader and app
configurations need correspondence; no automatic inference from one sdkconfig.
The driver CMake file adds VFS and forces the SOF monitor when the console
feature is enabled, so effective feature/link evidence matters.

The proposed sensitive runtime must have one byte writer. No console REPL,
stdout/stderr, ROM/EARLY logs, panic register dump, GDB stub, core dump or trace
transport may write into application framing or expose secret-bearing state.
The available named choices include `ESP_SYSTEM_PANIC_SILENT_REBOOT`,
`ESP_COREDUMP_ENABLE_TO_NONE`, `ESP_TRACE_LIB_NONE` and
`ESP_TRACE_TRANSPORT_NONE`; runtime GDB and every other writer still need
source/link exclusion. The stock driver itself anticipates interleaved ROM
output. Disabling VFS alone does not remove ROM output channels.

TRM §8.3/Table8.3-2 pp536–537 describes default ROM output to USB as well as
UART, a temporary RTC store control, and `DIS_USB_PRINT`. Temporary retained
state is not a permanent cold-start control. The pinned bootloader's no-console
branch clears both ROM output channels only after ROM boot. Development may
therefore have startup noise, open debug/download and disposable identities;
it cannot carry an owner-secured custody claim. A proposed owner-secured mode
requires verified ROM-print suppression and no uncontrolled writer before
secret loading, plus the already-open signed boot/update/rollback/recovery
contract. Nothing here proves those settings on a received device.

The controls have different scope:

| Documentary field | Required distinction |
| --- | --- |
| `DIS_USB_JTAG` | Disconnects USB Serial/JTAG from CPU JTAG while CDC remains usable. Pad JTAG is a separate path; disabling only USB JTAG does not disable pad debug. |
| `DIS_USB_SERIAL_JTAG` | Disables the whole Serial/JTAG block; it is incompatible with retaining that block as the application CDC transport. |
| `DIS_USB_SERIAL_JTAG_DOWNLOAD_MODE` | Disables the Serial/JTAG ROM download service, independently of whether application CDC remains available. |
| `DIS_USB_OTG_DOWNLOAD_MODE` | Separate OTG ROM-download gate, including lot-dependent default behavior. It is not the Serial/JTAG download gate. |
| `DIS_DOWNLOAD_MODE`, secure-download/boot controls | Wider download/boot policy; their final values and owner recovery remain part of the unfinished lifecycle contract. |

[Espressif's versioned JTAG guide](https://docs.espressif.com/projects/esp-idf/en/v6.1/esp32s3/api-guides/jtag-debugging/configure-other-jtag.html)
directly confirms the first distinction. TRM §8.5/Table8.5-1 p538 independently
separates USB and pad JTAG. Chapter5 p434's `DIS_USB_JTAG` prose calls it an
OTG-to-JTAG function; that wording is retained as a source discrepancy rather
than used to conflate the controllers. These are documentary conditions only;
there is no fuse command, burn, production key or hardware operation here.

## Download advisory and lot correspondence

The full manufacturer AR2022-004 V1.1, 21 December2022, was retrieved and read
(3 pages). It identifies separate bits: OTG download at BLK0 byte19 bit7,
previously named `ERR_RST_ENABLE`, and Serial/JTAG download at byte16 bit4,
previously named `DIS_USB_DOWNLOAD`/`DIS_USB_DOWNLOAD_MODE`. The advisory says
the latter alone disables only Serial/JTAG download. The OTG gate's default
depends on date code/PW number; S3 revision0.2 alone does not settle it.
ES errata v1.3 §3.5 printedp9 cites Serial/JTAG as an alternate download route;
that is not authorization to leave a ROM download service open in owner mode.

[AR2022-004 manufacturer original](https://documentation.espressif.com/AR2022-004%20Security%20Advisory%20for%20USB_OTG%20%26%20USB_Serial_JTAG%20Download%20Functions%20of%20ESP32-S3%20Series%20Products%20EN.pdf),
SHA256 `981e6154380eb184b9c6b0dbdf994f11e0c9b7781f62a3928682494a148fa19e`,
188774 bytes. The original-locator HTTP502 and failed web-reader redirect were
recorded before one bounded successful public redirect-target retrieval. No
restricted-document route was used.

## Outcome and exact scope

The fixed CDC controller has a useful public register path and maintained
vendor source on the existing kit. Stock driver/console behavior does not yet
meet the intended bounded reset/error/framing contract. Keep it as an assessed
alternative; do not silently substitute it, weaken owner/debug requirements,
or call its source availability a completed USB row. The no-J4-VBUS-sense and
power-topology issue from [usb-configuration.md](usb-configuration.md) is
unchanged. A bus reset, timeout or SOF status cannot certify physical unplug.

Fresh reading: TRM functional text/tables pp1243–1254 and register field bodies
pp1256–1268; no visual diagram or complete register-summary bit-layout review.
Selected eFuse definitions pp434–435, boot/output Tables8.3-2/8.5-1 pp537–538,
and SYSTEM USB reset-field body p834 were reread. Fresh source reading: complete
driver/API/LL/HAL/SOF monitor/driver Kconfig/CMake and both boot-console source
files; selected VFS lines142–209,339–373,650–735; complete esp_stdio Kconfig,
GDB and trace Kconfig, system panic choice lines30–64 and coredump selection
lines1–48; both pinned programming-guide source files. Unused VFS/select/termios
paths and unrelated fetched Kconfig bodies remain unread. Native originals,
raw code files and extracted texts remain private; the register records actual
coverage and hashes. No target build or physical test occurred.
