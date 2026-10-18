# Practical probe and measurement coverage

This is a preparation plan, not an admitted wiring procedure. H01's current
manual/configuration gates in [review-coverage.md](review-coverage.md) must close
for the affected host. H02S selected-SE gates remain independent. No physical
resource or operator is confirmed. No measurements, purchases, fuse writes,
production secrets or fabrication actions occurred in H01.

## Admission packet

First complete H01's documentary proposal: exact OPN/package, allowed revision
and configuration, current manuals/errata and bounded wiring requirements. This
work does not depend on owning a kit. The received-unit identification below is
an H02 check before execution, distinct from that documentary sign-off.

For each later U5/S3 setup record one exact board and revision, MCU/module OPN and
marking/DBG/eFuse-derived silicon revision, schematic and jumper state, panel
module/controller/FPC, input devices, source/sink supplies and all connected debug
or host paths. Identify expected default state before the CPU starts. Bind that
packet to current source IDs, selected errata and a completed pin/power/master
ownership table. A kit whose MCU package/rail differs from the custom candidate
must document what the probe can and cannot represent.

Pin compiler/target/HAL/PAC/vendor SDK/USB component and crypto versions, build
flags, linker/memory regions, lockfiles, binary/map hashes and boot image policy.
Begin with public fixtures and a build that cannot silently enable permanent
security provisioning. S02's accepted maintained crypto is reused within its
contract; no duplicate portable benchmark campaign is needed. Identify each
actual target call, fallible entropy source and adapter ABI before benchmarking.

The [follow-up notes](host-subset-notes.md) supply concrete prerequisites: the
S3 device stack needs its underlying TinyUSB lock and actual CPU-FIFO/DMA
configuration; current U585 USB/SPI errata need chosen-driver correspondence.
S3 sleep callers must prevent ANALOG-160's damaging condition. That condition
is prohibited, never a proposed physical negative test. An unused touch or
host-USB path must be explicitly excluded from the proposal rather than marked
reviewed. Headers and software tests do not close missing normative IP semantics.

Record operator, equipment model/ID, calibration or accuracy limitations, supply
current limit, ambient conditions, test wiring and measurement point. Scope/logic
analyzer voltage compatibility and debugger backpower must be checked. Missing
equipment is a resource gate; an estimated waveform is not evidence. Coordinate
any concrete purchase or irreversible provisioning separately when a reviewable
procedure and exact item exist.

## H02 host work, without an SE prerequisite

| Pass | Positive workload | Negative/interruption coverage | Evidence required |
| --- | --- | --- | --- |
| Identity/startup | Read actual part/revision/configuration; bounded USB enumeration; clocks, reset and panel initialization. | Wrong expected revision, held strap, missing panel, debugger disconnected, plug/unplug and brownout. | Board/photos/markings, register/config snapshots, exact limits and rail/reset captures. No secret input yet. |
| Review/consent/input | Same bounded request and inspectable review content on both hosts; scroll through complete allowed data and local recovery-entry flow. | Oversized/malformed input, rapid repeated requests, new request while reviewing, button bounce/stuck input, timeout, cancellation and reset at each consent transition. | Public fixture IDs, display/input trace, latency and rejected-action logs; no host-supplied “approved” state. Expected behavior comes from P01. |
| Memory/scheduling | USB + render + physical input + maintained crypto concurrently; record peak stacks, arenas, queues and remaining margin. | Maximum allowed text/message, allocator/queue exhaustion, stale/out-of-bounds DMA descriptors, core/cache contention and peripheral reset during transfer. | Linker map plus measured high-water marks, ownership checks and trace. Separate internal secret arena from display/external RAM; no hidden fallback/truncation. |
| Entropy/crypto | Qualified source startup and reseed policy; public signature/ECDH/decryption fixtures using actual target adapter. | Source absent/stalled, health failure, SAR/RF conflict, sleep/wake, backend error and short/failed read. | Actual call/link evidence and failure path; secret operations refuse when entropy contract fails. Statistical streams are supporting diagnostics only. |
| Boot/update/owner | Development update first; later explicitly authorized owner-secured procedure on identified sacrificial hardware. | Unsigned/wrong-root/old image, corrupt metadata, incompatible data, interruption at every persisted transition, revoked root and recovery credential loss. | Exact allowed state transitions, surviving/erased state, version counters and recovery demonstration. App A/B is not proof of bootloader/data atomicity. |
| Retention/power | Idle/active/review/update states and bounded suspend behavior. | CPU/system/watchdog reset, incomplete power loss, retained RTC state, USB suspend/detach and return with stale consent. | Current and voltage traces, measurement conditions; pending consent invalidated and intended secret buffers cleared. |

Initial comparisons may use a modest common SPI/physical-control workload while
U5G9's larger UI remains document-level. Do not turn H01 into three full ports.
If representative evidence shows a resource failure, record the exact failure and
promotion decision before expanding the host matrix. Quantitative pass thresholds
must be the accepted product/workload bounds or a reviewed probe specification;
they cannot be chosen after observing a result.

## H02S command/custody work

Start only the selected-service subset whose exact API/errata/update access is
available. Pin OPN, silicon/applet/firmware/configuration and host-library version.
Use vendor bridges for command exploration with public keys and fixtures; do not
report them as isolated custody devices. Preserve mandatory unresolved gates for
SE051 and applicable TROPIC advisory scope.

For each proposed service observe supported curve/algorithm, import/export policy,
channel binding, authorization lifetime, persistent counter/attempt behavior and
reset/update state. Include wrong PIN, default/wrong pairing, replay, wrong object
policy, malformed/oversized command, bus timeout/stuck line, SE-only power cycle,
host-only reset, complete/partial power loss and update interruption. Record
which plaintext/key/shared-secret bytes reach MCU memory. A successful ECDSA
signature is not BIP340; a generic ECDH API is not automatically the required
non-exportable secp256k1 operation.

Enrollment, PIN change, recovery, replacement and secure erase each need a
persisted-state transition table with cuts before/during/after every write. The
host's own rollback behavior is part of the construction. No timed delay,
non-resettable attempts or independent two-SE protection is assumed from a part
name. Vendor applet update authority and owner MCU firmware authority stay
separate in the evidence.

## H03 power/interface work

Use the two retained power candidates only after exact chemistry/OPNs and safe
setup are reviewed. Measure USB default-current startup before firmware, both
connector orientations, charger disable/reset/watchdog state, no-battery operation,
cell voltage extremes, full backlight/CPU/USB load, hot plug, shutdown and reverse
current/backfeed. Derive worst-case dissipation and L/C effective values from
component data, then check representative temperature and transients. A nominal
regulator rating or battery capacity does not establish usable runtime.

USB normative clauses must govern current entitlement, attach/suspend/detach and
inrush. Check the CC-controller/MCU-UCPD path against exact straps, dead-battery
behavior and supply domains. Measure VBUS sensing and pull-up disconnect, including
self-powered battery operation. Do not copy a one-Rd plug fixture into a
two-orientation receptacle design.

For the panel, verify module revision/contact orientation/rail sequencing before
connecting. Capture display transfers and input events while USB is flooded;
test blank/frozen/partial-screen and input failure behavior. For expansion, test
unpowered accessory backdrive, excessive load within the reviewed safe test
limits, stuck SDA/SCL, conflicting GPIO drive and reset/disconnect state. Never
use production secrets as fault-test fixtures. Camera/NFC require separate
admission and budgets if later promoted.

## Evidence handoff and later gates

Each result records claim ID, setup/binary/source hashes, expected and observed
outcomes, raw trace location, operator, date, uncertainty and remaining failures.
Keep “documented,” “calculated,” “implemented” and “measured” separate. An unavailable
test is an unresolved row, not a pass. Distinct review samples actual source
sections and every blocking claim, then checks the concrete procedure/results.

H04 combines current selected manuals, feasible package/AF/power/memory ownership,
representative H02/H02S/H03 evidence and manufacturing/recovery constraints before
any design selection. H08/H09 repeat applicable claims on actual assemblies; a
devkit result does not qualify a custom layout. The coordinator owns task-state
updates and resource acceptance.
