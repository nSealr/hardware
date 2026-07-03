# Verification: dfm-pcbway — "69 open connections and stale production artifacts block any gerber release"

Verdict: **CONFIRMED** (every evidence point reproduced from primary files; recommendation needs corrections — the existing export gate would NOT catch the 69 opens even after regeneration).

## Evidence check, point by point

### 1. "69 unrouted connections" — CONFIRMED by fresh DRC run
Ran `kicad-cli pcb drc --schematic-parity` (KiCad 10, `/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli`) on
`/Users/vincenzo/Documents/GitHub/nSealr/hardware/pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_pcb` (2026-07-03):

```
Found 0 violations
Found 69 unconnected items
```

Breakdown by net (from the fresh report, saved at `/private/tmp/claude-501/-Users-vincenzo-Documents-GitHub-nSealr/f269fbe4-0fc9-430f-b7c1-0e1284a83512/scratchpad/pcb-review/drc-fresh.json`):
40 GND, 4 TROPIC_VCC, 3 VBUS, 2 NRST, and 1 each of USB_DM_CONN, NFC_XTO, NFC_XTI, NFC_VDD_A, NFC_VCC, NFC_SPI_CSN/SCK/MOSI, TROPIC_GPO, TROPIC_SPI_MOSI/MISO/SCK/CSN, SYS_3V3, SE2_I2C_SCL, CHARGER_PGOOD_N, CHARGER_ILIM, TFT_BACKLIGHT_PWM, QSPI_CLK, QSPI_IO2.

Note: many of the 40 GND opens are F.Cu GND zone islands (e.g., first item: `Zone [GND] on F.Cu, priority 0` at (14.74, 31.6)) — these close with stitching vias to the In1 GND plane, not trace routing.

Caveat: the fresh run also reports **301 schematic parity issues, all severity "warning"** (199 `net_conflict`, 88 `extra_footprint`, 9 field mismatches, 5 footprint mismatches). Ground truth claimed "parity 0" — that number evidently counted only errors. Worth triaging before release, but not part of this finding.

### 2. "pcbway-manifest.json still says 'no routed KiCad PCB copper exists'" — CONFIRMED verbatim
`/Users/vincenzo/Documents/GitHub/nSealr/hardware/pcb/tropic01-universal-secure-device/production/pcbway-manifest.json` (mtime Jun 10 17:57):
```json
"blocked_reasons": ["PCBWay export blocked: no routed KiCad PCB copper exists; board is not routed"],
"status": "blocked", "release_outputs_valid": false, "erc": "blocked", "drc": "blocked"
```
This is provably stale: the current board file (mtime Jun 20 12:01, 1,044,255 bytes) contains **926 `(segment` and 129 `(via ` items** (exact grep counts), which the generating script itself (`validate_board_ready_for_export`) would now count as routed copper.

### 3. "drc.json dated 2026-06-11 with 262 unconnected" — CONFIRMED
`/Users/vincenzo/Documents/GitHub/nSealr/hardware/pcb/tropic01-universal-secure-device/production/drc/drc.json`:
`"date": "2026-06-11T11:36:44"`, `unconnected_items`: **262**, `violations`: **4**, `schematic_parity`: 0. File mtime Jun 11 11:37. The board has been re-routed since (262 → 69 opens; 4 → 0 violations), so the checked-in report is 22 days stale.

Also stale and part of the same gate: `production/erc/erc.json` (`"date": "2026-06-10T18:40:28"`) contains **212 sheet-level violations** — the export gate reads it (`require_clean_kicad_report`) and would stay blocked on ERC even after a DRC refresh.

### 4. "926 segments + 129 vias" — CONFIRMED
`grep -c "(segment"` → 926; `grep -c "(via$\|(via "` → 129 (the 130th match of the loose pattern is the `(vias` DRC-rule token in board setup).

## Why the given recommendation is insufficient (gate defect found)

The proposed gate ("re-run DRC, regenerate manifest") has a hole. In
`/Users/vincenzo/Documents/GitHub/nSealr/hardware/scripts/export_tropic01_universal_pcbway.py`,
`count_kicad_report_violations()` (lines 87-101) sums only `report["violations"]` and per-sheet `violations`. **It never reads `unconnected_items`.** Since fresh DRC yields 0 violations + 69 unconnected, the sequence "regenerate drc.json + erc.json (assuming ERC now clean) → run export script" would flip the manifest to `status: ready_for_fabrication_review` / `release_outputs_valid: true` **while 69 connections are still open**. The gate must be extended to fail on `len(unconnected_items) > 0` before it can serve as a fab-export gate.

Two more required lockstep changes:
- `/Users/vincenzo/Documents/GitHub/nSealr/hardware/tests/test_validate_hardware.py:347-361` (`test_..._pcbway_manifest_is_blocked_until_kicad_release_checks_pass`) hard-asserts `status: blocked` and the "no routed KiCad PCB" reason string; it must be rewritten to assert the *gate logic* (blocked while opens/violations exist, ready when clean) or it will go red the moment the manifest is legitimately regenerated.
- Staleness guard: neither the script nor CI compares drc.json/erc.json `date`/`source` against the board/schematic mtime or hash — that is exactly how a 22-day-stale report survived in-tree. Add a freshness check (e.g., embed board file SHA in the report filename/manifest and verify).

## Verdict
CONFIRMED. All four evidence points are factually accurate against primary sources (fresh kicad-cli DRC, the checked-in JSON artifacts, the board file itself). The recommendation is directionally correct but must be amended: regeneration alone is not a gate, because the export script ignores `unconnected_items` and the CI test pins the blocked state.
