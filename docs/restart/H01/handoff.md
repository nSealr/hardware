# H01 source candidate handoff

Substantive source commit:
**19362fc9a12bed43070c56642b4a932f1bc6a545**, branch
[`restart/h01-manuals`](https://github.com/nSealr/hardware/tree/restart/h01-manuals).
The companion [result record](result.json) binds the exact artifact hashes.
The approved brief remains the unchanged `e10dd24` candidate, with coordinator
approval cherry-picked as `837fa28`.

**H01 remains running/incomplete; no host or part is admitted.** In particular,
acceptances 1 and 5 cannot be passed by admitting zero hosts. Publication and 43
existing repository tests do not establish current-manual completeness,
electrical correctness or measurement. The coordinator owns task-state changes.

The candidate contributes 70 source records, 24 claims, 25 pin witness rows and
20 errata rows, plus eight explicit source contradictions. These counts describe
the record, not a quality score. The meaningful changes are selected current S3
TRM/SDK/errata and TI reading; current ST security bulletin applicability; U5G9
DS14102 Rev5/package/toolchain triage; P4 revision/algorithm-specific boot gates;
verified bounded reuse of SE documents/reference drawings; and practical probe
coverage that keeps physical and selected-SE gates separate.

## Next actionable reading

The ST retrieval gap is specific: current **RM0456 Rev7 March2026** could not be
obtained through the bounded routes recorded in the register. Rev6's preserved
original is not the current delta. Root independently found no usable current
original; the Arm Keil pack index now points to ST manuals instead of embedding
them. Repeat an old route only when there is new evidence it can succeed. Do not
use this access failure to choose S3 for the custom Board or stop unrelated work.

Available-source work remains and can continue after distinct review:

| Work | Exact starting locators and deliverable |
| --- | --- |
| S3 concrete pin/input configuration | Module1.8 p.31 PSRAM limits, remaining application/dimension diagrams; exact DevKitC-1 board schematic/header/RGB conflicts. TRM1.8 §§6.10–6.13 pp.481–496, GPIO_PINn details around pp.507–520. Complete pad/function-number/reset/pull/input-interrupt map for the modest chosen panel/physical controls. A chosen candidate is not a frozen part. |
| S3 SPI configuration | CPU/DMA master setup pp.1115–1117,1128–1130 and clock/interrupt pp.1142–1150 have been read. Still reconcile the chosen mode with §30.5.8.2 state table, §30.6 CS timing p.1141, selected timing-compensation and actual register definitions/driver. Panel clock and electrical limits remain separate. |
| S3 USB and master bounds | §32.3 selected device paths read; finish the selected §32.4 register/FIFO configuration and pin exact TinyUSB/esp-usb implementation. Resolve direction-specific DMA register-name contradictions and explicitly select CPU FIFO or bounded DMA. Verify every enabled master; GDMA permissions do not automatically prove USB AHB-master bounds. |
| S3 watchdog/reset/flash lifecycle | Read chapter13 pp.672–679 and its referenced MWDT/RWDT register definitions for the chosen watchdog. Complete selected boot/eFuse/XTS chapter23 pp.908–918 correspondence, ROM download allowlist and SDK bootloader-update discrepancy. Use the actual selected provision/update path, not a raw fuse procedure. |
| S3 entropy/crypto integration | TRM25 and RNG SDK source preconditions are reviewed. Inspect the pinned actual startup/source-selection/health-failure adapter and target backend invocation/ABI. Determine whether any hardware AES/RSA/HMAC service is actually used before adding its full chapter; portable software crypto does not imply those peripherals are needed. |
| U585 available datasheet/errata work | DS13086 Rev10 exact VI/VIQ pad/AF/electrical and ES0499 Rev12 selected bodies remain actionable through lawful current extraction/original access. Current RM remains a distinct gate. Retain exact received silicon as unknown. |
| U5G9 document triage | Complete DS14102 Rev5 §3.5 memory banks, power/supply, graphics/DSI, exact ZJT6Q/ZJJ6Q pin/package tables and ES0595 Rev4 DSI/SAES/selected interfaces. Current Embassy declarations prevent unsupported “no driver” claims; exact configuration, dependency/license and ownership still need checking. No full new port required. |
| SE and power | Complete accessible selected OPTIGA object/channel/reset/counter/update and TROPIC transport/PIN-state reading where useful. Keep SE051 restricted API/errata and TROPIC remediation gates. TI exact pin/supply/application/thermal/reset-current details, exact cell/protection and USB normative clauses remain open; two retained chains only. |

No S3-only clearance is claimed from these partial readings. Each admitted later
probe needs a concrete selected subset; conditional camera/NFC/large graphics or
hostile-app isolation must not expand that subset silently.

## Verification and review request

JSON parsing, unique source IDs and claim/pin/errata source references passed.
Original source hashes were checked when downloaded or reused; this is separate
from the source reading. `git diff --check` passed before the source commit.

`make ci` in the author worktree failed because the legacy verifier derives the
repository type from its directory basename `h01` and therefore expects MIT.
The exact source commit was checked out without edits at
`/home/tux/nsealr/.restart-tools/goal/h01-ci/hardware`; unchanged `make ci` then
passed baseline verification, all **43** existing tests, compile checks and
hardware validation. This verifies the existing repository tooling only. No new
prose-matching tests, target builds or measurements were added.

The canonical plan validator ran read-only against main
`f2ef70f522af4977e15f81554a8c6eadcdbe8097`, graph revision13, and passed its
47-task structural check. It is reconciliation evidence, not a replacement for
the pinned H01 requirements input `7b5553685dac56029a4379be12054154b6b5e0b5`.

Requested distinct review: verify actual selected manual sections, sample source
identity/hash correspondence, inspect **every blocking claim**, assess exact
part/revision and adverse evidence, and identify unsupported conclusions or
missing useful coverage. Review the known incomplete status rather than issuing
an H01 PASS from schema/test counts. Further available-source review should
follow the findings. No PCB/layout, part freeze, fabrication, purchase, physical
measurement, permanent provisioning or production-secret use is included.
