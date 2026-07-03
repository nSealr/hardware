# Verification: dfm-pcbway — "Turnkey BOM covers only 16 of 103 footprints"

Verdict: **CONFIRMED** (substance exact; row count off by one — 15 data rows, not 16; recommendation needs correction because the schematic cannot be the BOM source today).

## Claim checked

> production/bom/pcbway-bom.csv has 16 rows (U1-U5, U7-U11, J1, J2, J6, J9, SW1); missing all R/C/L passives, L1, L15, X1 16MHz, X3 27.12MHz, LED1, U13/U14 TPS22917, U15 TPS61165, JP1; PCBWay turnkey requires every placed designator plus DNP marking.

## Evidence

### 1. BOM contents (primary source)

File: `/Users/vincenzo/Documents/GitHub/nSealr/hardware/pcb/tropic01-universal-secure-device/production/bom/pcbway-bom.csv`

- `wc -l` = 16 lines = 1 header + **15 data rows**. The finding's "16 rows" almost certainly counted the header; its designator list (U1-U5, U7-U11, J1, J2, J6, J9, SW1) is 15 designators and matches the CSV **exactly**:
  `J1 J2 J6 J9 SW1 U1 U2 U3 U4 U5 U7 U8 U9 U10 U11`
- Confirmed absent from the CSV: every R (R1-R24), every C (39 caps), RJ1/RJ2, RLED1-3, L1 (DFE201610P-2R2M), L15 (10uH), L30/L31, X1 (16MHz), X3 (FA-238 27.12MHz), LED1 (ASMB-MTB0-0A3A2), D15 (Schottky), U13/U14 (TPS22917DBVR), U15 (TPS61165DBVR), J7 (TC2030), JP1, TP_*, ANT1, DISP1, MH1-4.
- Existing columns: `Designator,Qty,Manufacturer,Manufacturer Part Number,Description,Package,Footprint,Notes` — **no Type (SMD/THT) column**, no DNP column.

### 2. Board footprint count (primary source)

`board-truth.json` placement array = **103 footprints** (verified by script). Breakdown of the 88 missing refs:
- Real PCBA parts missing from BOM: 39 C + 24 R + RJ1/RJ2 + RLED1-3 + L1/L15/L30/L31 + X1/X3 + LED1 + D15 + U13/U14/U15 + J7 ≈ **78 placed, solderable components** with no BOM row.
- Non-PCBA refs: MH1-4 (mounting holes, Value=`M2_CASE_SCREW_CLEARANCE`), TP_UART_GND/TX/RX (bare pads), ANT1 (envelope placeholder), DISP1 (off-board envelope), JP1 (BOOT0 solder jumper, copper-only).

So a turnkey quote covering the pick-and-place file is impossible: the CPL will contain ~93 populated positions while the BOM describes 15. This is the finding's core claim and it is true.

### 3. PCBWay requirement (WebFetch of the cited page)

`https://www.pcbway.com/assembly-file-requirements.html` states turnkey/partial-turnkey BOMs should include:
> "Line#, Quantity Per Part Number, Reference Designator, Part Number, Part Description, Package, **Type (Surface mount, Thru-hole or Hybrid)**, Manufacturers Name, Manufacturers Part Number, Distributors Part Number"

- The Type-column part of the recommendation is directly backed by this page.
- Nuance: the page does **not** literally say "every placed designator plus DNP marking" — the finding slightly over-cites. But BOM/CPL designator consistency and explicit DNP marking are standard assembler requirements (assemblers default to populating everything listed in the CPL; a 15/103 mismatch stalls any quote). This does not weaken the finding.

### 4. The recommendation's flaw: the schematic cannot generate this BOM

Parsed all sheets in `/Users/vincenzo/Documents/GitHub/nSealr/hardware/pcb/tropic01-universal-secure-device/kicad/sheets/`: they contain only **9 symbol instances total** — J1, J2, J9, SW1, U1, U2, U5, U9, U11 (lib_id count per sheet: power_usb 2, display_controls 2, others 1 each). Six of the fifteen parts already in the BOM (U3, U4, U7, U8, U10, J6) **do not exist as schematic symbols** (`grep TPS22917` across all `.kicad_sch` = 0 hits; consistent with `production/schematic-coverage.json` `board_refs_missing_binding` which lists U3/U4/U7/U8/U10/U13/U15/X1/X3/LED1/...). "Regenerate BOM from schematic" would therefore produce a *worse* BOM (9 rows).

The viable source today is the **PCB itself**: all 103 footprints carry populated `Value` properties (verified: C1=10uF, R1=5.1k, L1=DFE201610P-2R2M, X3=FA-238 27.12MHz, U15=TPS61165DBVR, ...). Use `kicad-cli pcb export` / a script over the board file, plus `design-notes/component-decisions.md` for MPNs.

### 5. Additional blockers found while verifying

- **Placeholder values in the board**: L30, L31, C30, C31, C32, C33 = `NFC_TUNE` (ST25R3916B matching network not tuned; ANT1 is an envelope). These cannot get MPNs until NFC tuning is done — the BOM cannot be *finalized* even from the PCB.
- **pcbway-manifest mismatch**: `production/pcbway-manifest.json` `required_non_pcba_rows` = ANT1, DISP1, and 8 testpoints (TP_SWDIO TP_SWCLK TP_NRST TP_BOOT0 TP_UART_TX TP_UART_RX TP_3V3 TP_GND). It does **not** list JP1 (the finding's "JP1 per pcbway-manifest" is a mis-citation — JP1 as DNP is still correct practice, just not manifest-mandated). Also 6 of the 8 required TPs (SWDIO/SWCLK/NRST/BOOT0/3V3/GND) don't exist on the board yet, and the board's TP_UART_GND isn't in the manifest list — the DNP row set must be reconciled with the pending testpoint fix.
- Manifest `status: "blocked"` / `"no routed KiCad PCB copper exists"` is itself stale (board is ~96% routed), so the manifest needs regeneration too.

## Corrected recommendation

Regenerate the BOM **from the PCB** (not the schematic — it holds only 9 symbols): script over the `.kicad_pcb` Value/Footprint fields (or `kicad-cli`), merge MPNs from `design-notes/component-decisions.md`, covering all ~93 populated positions (exclude MH1-4 or list as hardware). Add the PCBWay-required `Type (SMD/THT)` column. Add explicit DNP rows for ANT1, DISP1, JP1, and the testpoints — reconciling with `pcbway-manifest.json` `required_non_pcba_rows` after the 6 missing required TPs (TP_SWDIO/SWCLK/NRST/BOOT0/3V3/GND) are added to the board. Flag L30/L31/C30-C33 (`NFC_TUNE`) and ANT1 as value-TBD pending NFC matching-network tuning; the BOM cannot be finalized before that. Longer term, complete the schematic (only 9 of 103 refs have symbols) so schematic-driven BOM generation becomes possible.

## Sources

- `/Users/vincenzo/Documents/GitHub/nSealr/hardware/pcb/tropic01-universal-secure-device/production/bom/pcbway-bom.csv` (15 data rows)
- `/Users/vincenzo/Documents/GitHub/nSealr/hardware/pcb/tropic01-universal-secure-device/production/pcbway-manifest.json` (`required_non_pcba_rows`)
- `/Users/vincenzo/Documents/GitHub/nSealr/hardware/pcb/tropic01-universal-secure-device/production/schematic-coverage.json` (board_refs_missing_binding)
- `/Users/vincenzo/Documents/GitHub/nSealr/hardware/pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_pcb` (103 footprints, Value fields, NFC_TUNE placeholders)
- `/Users/vincenzo/Documents/GitHub/nSealr/hardware/pcb/tropic01-universal-secure-device/kicad/sheets/*.kicad_sch` (9 symbol instances total)
- PCBWay assembly file requirements: https://www.pcbway.com/assembly-file-requirements.html (BOM field list incl. Type column)
