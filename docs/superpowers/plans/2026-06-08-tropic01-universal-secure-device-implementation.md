# TROPIC01 Universal Secure Device Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the current custom-hardware mockup with a coherent single-product TROPIC01 universal secure device source set: validated docs, frozen BOM, real KiCad schematic/netlist, compact portrait placement, and guarded PCBWay export.

**Architecture:** Treat `docs/superpowers/specs/2026-06-08-tropic01-universal-secure-device-design.md` as the source of truth. First update the repository contracts and validation tests, then update docs/BOM, then rebuild KiCad from schematic-driven nets instead of polishing the current footprint-only mockup. Production exports stay blocked until ERC, DRC, BOM, position, and antenna notes are truthful.

**Tech Stack:** KiCad 10.0.3, KiCad CLI, KiPilot MCP, Python validation scripts, `unittest`, CSV BOM, JSON requirements, Markdown design notes.

---

## File Structure

- `docs/superpowers/specs/2026-06-08-tropic01-universal-secure-device-design.md`: approved product design, already committed.
- `docs/superpowers/plans/2026-06-08-tropic01-universal-secure-device-implementation.md`: this implementation plan.
- `pcb/tropic01-universal-secure-device/requirements.json`: machine-readable custom hardware contract.
- `bom/tropic01-universal-secure-device.csv`: single-product component table with chosen, alternate, and rejected rows.
- `docs/tropic01-universal-secure-device-rev-a.md`: human-facing Rev A hardware description.
- `docs/tropic01-open-hardware-inventory.md`: inventory entry that must point only to this custom hardware direction.
- `README.md`, `docs/architecture.md`, `docs/roadmap.md`, `docs/testing.md`, `docs/audit-checklist.md`: repository-level documentation that must stop referencing stale custom-wallet narratives.
- `scripts/validate_hardware.py`: repository contract validator.
- `tests/test_validate_hardware.py`: tests that pin requirements, BOM, KiCad source shape, placement, and export behavior.
- `scripts/export_tropic01_universal_pcbway.py`: PCBWay BOM/position/export guard logic.
- `scripts/materialize_tropic01_universal_placement.py`: existing mockup generator; either convert it into a placement helper or retire its production authority.
- `pcb/tropic01-universal-secure-device/kicad/`: KiCad project directory.
- `pcb/tropic01-universal-secure-device/kicad/sheets/*.kicad_sch`: schematic sheets.
- `pcb/tropic01-universal-secure-device/kicad/lib/`: project-local symbols, footprints, and models for parts not safely covered by stock KiCad libraries.
- `pcb/tropic01-universal-secure-device/production/`: generated outputs; must be deleted or clearly marked invalid until regenerated from a connected/routed design.

## Implementation Tasks

### Task 1: Pin the Final Product Contract in Tests

**Files:**
- Modify: `tests/test_validate_hardware.py`

- [ ] **Step 1: Update requirements tests for the final single-product decision**

Replace the current TROPIC01 requirement expectations with assertions that the second secure element is mounted by default, microSD is excluded, NFC and battery stay core, and pogo/test pads are hidden production/debug pads.

Add this test near the existing TROPIC01 universal requirements tests:

```python
    def test_tropic01_universal_secure_device_is_single_product_with_second_se_and_no_microsd(self) -> None:
        value = json.loads(TROPIC01_UNIVERSAL_REQUIREMENTS.read_text(encoding="utf-8"))
        flattened = json.dumps(value, sort_keys=True).lower()

        self.assertEqual(value["device_class"], "tropic01_universal_secure_device")
        self.assertIn("second_secure_element_i2c", value["mandatory_interfaces"])
        self.assertIn("hidden_pogo_test_pads", value["mandatory_interfaces"])
        self.assertIn("no_microsd_slot", value["mandatory_interfaces"])
        self.assertNotIn("second_secure_element_dnp", value["optional_interfaces"])
        self.assertNotIn("microsd_dnp", [item.lower() for item in value["optional_interfaces"]])
        self.assertIn("optiga", flattened)
        self.assertIn("pogo", flattened)
        self.assertIn("covered by the enclosure", flattened)
        self.assertIn("do not include microsd", flattened)
```

- [ ] **Step 2: Update the component decision test**

Extend `test_tropic01_universal_secure_device_pins_rev_a0_component_decisions` with:

```python
        self.assertIn("OPTIGA", decisions["second_secure_element"])
        self.assertIn("Trust M", decisions["second_secure_element"])
        self.assertIn("no microSD", decisions["removable_storage_policy"])
```

- [ ] **Step 3: Update BOM frozen MPN expectations**

In `test_tropic01_universal_secure_device_bom_freezes_core_mpns`, change the expected USB connector and add the second secure element:

```python
            "J1": "USB4105-GF-A",
            "U11": "OPTIGA-TRUST-M-SLS32AIA",
```

Keep these expected rows present:

```python
            "U2": "TR01-C2P-T301",
            "U2_ALT": "TR01-C2P-T310",
            "U9": "ST25R3916B-AQET",
            "U10": "BQ24074RGTR",
```

- [ ] **Step 4: Update PCBWay export expectations**

In `test_tropic01_universal_secure_device_pcbway_bom_export_excludes_dnp_rows`, assert that the final product exports the second secure element and the GCT USB-C receptacle:

```python
        self.assertEqual(by_designator["J1"]["Manufacturer Part Number"], "USB4105-GF-A")
        self.assertEqual(by_designator["U11"]["Manufacturer Part Number"], "OPTIGA-TRUST-M-SLS32AIA")
```

Remove the old assertion that `U11` is excluded from the PCBWay rows.

- [ ] **Step 5: Update placement expectations**

In `test_tropic01_universal_secure_device_placement_plan_is_portrait_and_includes_critical_parts`, require the final product components:

```python
            "U11",
            "TP_SWDIO",
            "TP_SWCLK",
            "TP_NRST",
            "TP_BOOT0",
```

Replace the USB footprint assertion with:

```python
        self.assertIn("USB4105", by_ref["J1"].footprint)
```

- [ ] **Step 6: Update antenna drawing expectations**

In `test_tropic01_universal_secure_device_board_drawings_include_display_and_nfc_features`, replace the old decorative antenna expectation:

```python
        self.assertIn("ANT1 TOP EDGE NFC ANTENNA FPC OR TUNED KEEP-OUT", drawings)
        self.assertNotIn("PCB NFC LOOP", drawings)
```

- [ ] **Step 7: Run the targeted tests and confirm failure before implementation**

Run:

```bash
python3 -m unittest tests.test_validate_hardware.HardwareValidationTests.test_tropic01_universal_secure_device_is_single_product_with_second_se_and_no_microsd tests.test_validate_hardware.HardwareValidationTests.test_tropic01_universal_secure_device_bom_freezes_core_mpns tests.test_validate_hardware.HardwareValidationTests.test_tropic01_universal_secure_device_pcbway_bom_export_excludes_dnp_rows tests.test_validate_hardware.HardwareValidationTests.test_tropic01_universal_secure_device_placement_plan_is_portrait_and_includes_critical_parts -v
```

Expected: failures mentioning missing `second_secure_element_i2c`, old USB MPN, missing `U11`, or outdated placement.

- [ ] **Step 8: Commit the failing contract tests**

Run:

```bash
git add tests/test_validate_hardware.py
git commit -m "test: pin final tropic01 product contract"
```

### Task 2: Update Requirements and Validator Contracts

**Files:**
- Modify: `scripts/validate_hardware.py`
- Modify: `pcb/tropic01-universal-secure-device/requirements.json`
- Test: `tests/test_validate_hardware.py`

- [ ] **Step 1: Update required interfaces in the validator**

In `scripts/validate_hardware.py`, update `REQUIRED_TROPIC01_UNIVERSAL_INTERFACES` so it includes:

```python
    "second_secure_element_i2c",
    "hidden_pogo_test_pads",
    "no_microsd_slot",
```

Keep these existing mandatory interfaces:

```python
    "usb_c_receptacle_only",
    "touch_display",
    "side_physical_buttons",
    "tropic01_spi",
    "tropic01_power_cycle_control",
    "external_host_spi_selectable",
    "lipo_power_path",
    "lipo_battery_connector",
    "nfc_power_gated",
    "qspi_flash",
```

- [ ] **Step 2: Update required MPNs in the validator**

In `REQUIRED_TROPIC01_UNIVERSAL_CORE_MPNS`, use this final mapping for changed rows:

```python
    "J1": "USB4105-GF-A",
    "U11": "OPTIGA-TRUST-M-SLS32AIA",
```

Keep the existing TROPIC01, STM32U5, display, NFC, battery, and flash MPNs until the BOM task changes a row with a test in the same commit.

- [ ] **Step 3: Update requirement text rules**

In `validate_tropic01_universal_secure_device`, remove `"second secure element"` from the list of surfaces that must be unmounted in the core profile. Replace:

```python
    for forbidden in ("radio", "second secure element", "microsd"):
```

with:

```python
    for forbidden in ("radio", "microsd"):
```

Add this required term set entry:

```python
        "second secure element",
        "optiga",
        "pogo",
        "no microsd",
```

- [ ] **Step 4: Update BOM optional-surface validation**

In `validate_tropic01_universal_bom_rows`, replace:

```python
    for optional_surface in ("second secure element", "radio", "microsd"):
```

with:

```python
    for optional_surface in ("radio", "microsd"):
```

Add a required-row check for the second secure element:

```python
    has_second_secure_element = any(
        row.get("required", "").strip().lower() == "true"
        and "optiga" in " ".join(row.values()).lower()
        and "i2c" in " ".join(row.values()).lower()
        for row in rows
    )
    if not has_second_secure_element:
        raise ValueError(f"{path}: universal BOM must include a required OPTIGA-class I2C second secure element")
```

- [ ] **Step 5: Update `requirements.json` mandatory and optional interfaces**

In `pcb/tropic01-universal-secure-device/requirements.json`, add these mandatory entries:

```json
    "second_secure_element_i2c",
    "hidden_pogo_test_pads",
    "no_microsd_slot"
```

Remove these optional entries:

```json
    "second_secure_element_dnp",
    "microSD_dnp"
```

- [ ] **Step 6: Update `requirements.json` component decisions**

Add these keys under `rev_a0_component_decisions`:

```json
    "second_secure_element": "Infineon OPTIGA Trust M family, BOM MPN OPTIGA-TRUST-M-SLS32AIA, USON-10, I2C shielded-connection secure element used as the independent defense-in-depth trust anchor.",
    "removable_storage_policy": "no microSD slot in the single product; use soldered QSPI flash plus USB, NFC, QR/display, or host workflows for import/export."
```

- [ ] **Step 7: Update board profiles**

In the `core` profile, add:

```json
        "OPTIGA Trust M class I2C second secure element",
        "hidden back-side pogo/test pads covered by the enclosure"
```

Remove `"second secure element"` from the `not_mounted` array.

- [ ] **Step 8: Run targeted validation tests**

Run:

```bash
python3 -m unittest tests.test_validate_hardware.HardwareValidationTests.test_tropic01_universal_secure_device_requirements_are_valid tests.test_validate_hardware.HardwareValidationTests.test_tropic01_universal_secure_device_is_single_product_with_second_se_and_no_microsd -v
```

Expected: the requirements tests pass; BOM and placement tests may still fail until later tasks.

- [ ] **Step 9: Commit requirements and validator**

Run:

```bash
git add scripts/validate_hardware.py pcb/tropic01-universal-secure-device/requirements.json
git commit -m "feat: require second secure element in tropic01 product"
```

### Task 3: Freeze the Single-Product BOM

**Files:**
- Modify: `bom/tropic01-universal-secure-device.csv`
- Modify: `scripts/export_tropic01_universal_pcbway.py`
- Test: `tests/test_validate_hardware.py`

- [ ] **Step 1: Replace the USB-C connector row**

In `bom/tropic01-universal-secure-device.csv`, set `J1` to the GCT receptacle:

```csv
J1,usb,USB-C receptacle female centered on bottom short edge,true,GCT USB4105 USB 2.0 Type-C receptacle; no plug-style board; CC Rd and ESD required,GCT,USB4105-GF-A,USB-C 16P SMT receptacle,Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal,https://gct.co/files/specs/usb4105-spec.pdf,,frozen
```

- [ ] **Step 2: Add the second secure element row**

Add this row:

```csv
U11,secure_element,Second secure element for defense-in-depth attestation and independent trust anchor,true,I2C OPTIGA Trust M family device; TROPIC01 remains the open primary secure element,Infineon,OPTIGA-TRUST-M-SLS32AIA,PG-USON-10 3x3mm,Package_SON:Microchip_USON-10-1EP_3x3mm_P0.5mm_EP1.8x2.5mm,https://www.infineon.com/assets/row/public/documents/30/49/infineon-optiga-trust-m-sls32aia-datasheet-en.pdf,,candidate
```

The footprint is a KiCad stock USON-10 candidate. During schematic implementation, compare the exact Infineon package drawing against the footprint pad dimensions. If the stock footprint does not match, create a project-local footprint and update this row in the same commit as the footprint.

- [ ] **Step 3: Remove microSD from mounted or optional product rows**

Delete any row whose category or description makes `microSD` a DNP feature for this product. Keep the design decision documented in Markdown instead of the BOM.

- [ ] **Step 4: Keep pogo/test pads as non-PCBA rows**

Ensure the test-pad row uses explicit designators:

```csv
TP_SWDIO TP_SWCLK TP_NRST TP_BOOT0 TP_UART_TX TP_UART_RX TP_3V3 TP_GND,programming,Hidden back-side pogo/test pads for production flashing bring-up and rail checks,false,Not PCBWay PCBA components; enclosure covers them in product builds,Generic,TestPad,PCB copper pads,TestPoint:TestPoint_Pad_D1.0mm,,,
```

- [ ] **Step 5: Update PCBWay exporter to include U11 and exclude test pads**

In `scripts/export_tropic01_universal_pcbway.py`, keep the rule that rows with `required != "true"` are excluded. Confirm `U11` is included because it is `required,true`, while `TP_*` pads are excluded because they are not PCBA placements.

Add this test helper if not present:

```python
def is_pcba_row(row: dict[str, str]) -> bool:
    if row.get("required", "").strip().lower() != "true":
        return False
    designator = row.get("designator", "")
    return not designator.startswith("TP_")
```

- [ ] **Step 6: Run BOM/export tests**

Run:

```bash
python3 -m unittest tests.test_validate_hardware.HardwareValidationTests.test_tropic01_universal_secure_device_bom_is_valid tests.test_validate_hardware.HardwareValidationTests.test_tropic01_universal_secure_device_bom_freezes_core_mpns tests.test_validate_hardware.HardwareValidationTests.test_tropic01_universal_secure_device_pcbway_bom_export_excludes_dnp_rows tests.test_validate_hardware.HardwareValidationTests.test_tropic01_universal_secure_device_pcbway_bom_export_excludes_non_pcba_rows -v
```

Expected: all four tests pass.

- [ ] **Step 7: Commit BOM and exporter**

Run:

```bash
git add bom/tropic01-universal-secure-device.csv scripts/export_tropic01_universal_pcbway.py tests/test_validate_hardware.py
git commit -m "feat: freeze final tropic01 product bom"
```

### Task 4: Clean Custom Hardware Documentation

**Files:**
- Modify: `README.md`
- Modify: `docs/architecture.md`
- Modify: `docs/roadmap.md`
- Modify: `docs/testing.md`
- Modify: `docs/audit-checklist.md`
- Modify: `docs/tropic01-open-hardware-inventory.md`
- Modify: `docs/tropic01-universal-secure-device-rev-a.md`
- Delete if still present: `docs/custom-persistent-secret-wallet-rev-a.md`
- Delete if still present: `bom/custom-persistent-secret-wallet.csv`
- Delete if still present: `pcb/custom-persistent-secret-wallet/requirements.json`

- [ ] **Step 1: Search stale custom hardware narratives**

Run:

```bash
rg -n "custom-persistent-secret-wallet|persistent secret wallet|second secure element.*DNP|microSD_dnp|USB-C plug|PCB NFC LOOP|air-gapped.*TROPIC01" README.md docs bom pcb scripts tests
```

Expected: matches show only files to edit in this task or tests intentionally checking rejection.

- [ ] **Step 2: Update `docs/tropic01-universal-secure-device-rev-a.md`**

Make this document state the final single-product architecture:

```markdown
Core mounted hardware:
- TROPIC01 primary open secure element.
- STM32U5 host MCU.
- OPTIGA Trust M class I2C second secure element.
- 2.4 inch portrait capacitive touch display.
- USB-C female receptacle centered on the bottom edge.
- ST25R3916B NFC controller with top-edge antenna FPC or tuned keepout.
- LiPo connector and BQ24074-class power path.
- QSPI NOR flash.
- Two high side-actuated physical buttons.
- Hidden back-side pogo/test pads.

Excluded from this product:
- microSD.
- BLE/WiFi/radio module.
- USB-C male plug variant.
- decorative NFC antenna loops.
```

- [ ] **Step 3: Update `docs/tropic01-open-hardware-inventory.md`**

The inventory must describe `tropic01-universal-secure-device` as the only active custom hardware direction. Keep references to other supported hardware families if they are not custom TROPIC01 board designs.

- [ ] **Step 4: Mark production outputs invalid until regenerated**

In `pcb/tropic01-universal-secure-device/production/README.md`, place this warning at the top:

```markdown
# Production Output Status

The files in this directory are not release manufacturing outputs. They were
generated from an earlier placement/mockup board and must not be uploaded to
PCBWay for fabrication or assembly.

Release outputs are valid only after the schematic has real nets, ERC passes,
the PCB has routed copper, DRC passes, and the PCBWay manifest records the clean
checks.
```

- [ ] **Step 5: Run stale narrative scan**

Run:

```bash
rg -n "custom-persistent-secret-wallet|persistent secret wallet|second secure element.*DNP|microSD_dnp|USB-C plug|PCB NFC LOOP" README.md docs bom pcb scripts tests
```

Expected: no stale product claims remain. Rejection tests may mention forbidden strings only where the surrounding test name or assertion makes the rejection explicit.

- [ ] **Step 6: Run repository validation**

Run:

```bash
python3 scripts/validate_hardware.py
```

Expected: validation passes, except KiCad production output checks may remain blocked if they require routed board outputs that are intentionally invalid. If that happens, update the validator to distinguish source validation from release-output validation in Task 8, then rerun.

- [ ] **Step 7: Commit documentation cleanup**

Run:

```bash
git add README.md docs/architecture.md docs/roadmap.md docs/testing.md docs/audit-checklist.md docs/tropic01-open-hardware-inventory.md docs/tropic01-universal-secure-device-rev-a.md pcb/tropic01-universal-secure-device/production/README.md
git add -u docs/custom-persistent-secret-wallet-rev-a.md bom/custom-persistent-secret-wallet.csv pcb/custom-persistent-secret-wallet/requirements.json
git commit -m "docs: align custom hardware with final tropic01 product"
```

### Task 5: Rebuild KiCad Source as Schematic-Driven Hardware

**Files:**
- Modify: `pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_sch`
- Modify: `pcb/tropic01-universal-secure-device/kicad/sheets/power_usb.kicad_sch`
- Modify: `pcb/tropic01-universal-secure-device/kicad/sheets/stm32u5_host.kicad_sch`
- Modify: `pcb/tropic01-universal-secure-device/kicad/sheets/tropic01.kicad_sch`
- Modify: `pcb/tropic01-universal-secure-device/kicad/sheets/display_controls.kicad_sch`
- Modify: `pcb/tropic01-universal-secure-device/kicad/sheets/storage_expansion.kicad_sch`
- Create: `pcb/tropic01-universal-secure-device/kicad/sheets/secure_element_2.kicad_sch`
- Modify: `pcb/tropic01-universal-secure-device/kicad/sheets/optional_profiles.kicad_sch`
- Modify: `pcb/tropic01-universal-secure-device/kicad/sym-lib-table`
- Create as needed: `pcb/tropic01-universal-secure-device/kicad/lib/footprints/*.kicad_mod`

- [ ] **Step 1: Close KiCad file locks before scripted edits**

Run:

```bash
find pcb/tropic01-universal-secure-device/kicad -name '~*.lck' -print
```

Expected: lock files may appear if KiCad is open. Close KiCad or use KiCad MCP for live-safe changes before editing source files.

- [ ] **Step 2: Remove debug KiCad artifacts from source control**

Delete `_debug_*.kicad_prl`, `_debug_*.kicad_pcb`, and `production/drc/_debug_*.json` artifacts after confirming they are not the active project files.

Run:

```bash
find pcb/tropic01-universal-secure-device -name '_debug_*' -print
```

Expected: only generated debug files are listed. Remove them in the implementation step and stage deletions with `git add -u`.

- [ ] **Step 3: Define schematic sheet responsibilities**

Use these sheet boundaries:

```text
power_usb.kicad_sch:
  USB-C receptacle, CC resistors, ESD, VBUS current limit, BQ24074 power path,
  system buck, load switches, battery connector, rail test points.

stm32u5_host.kicad_sch:
  STM32U585VIT6, crystals if used, boot straps, SWD/pogo, UART pads, USB D+/D-,
  GPIO labels to every peripheral.

tropic01.kicad_sch:
  TROPIC01, decoupling, pull network, SPI, GPO, switched VCC, test visibility.

secure_element_2.kicad_sch:
  OPTIGA Trust M class I2C secure element, decoupling, I2C pullups, reset/enable
  if the selected package requires it.

display_controls.kicad_sch:
  Newhaven 40-pin TFT FFC, 6-pin CTP FFC, ST7789 SPI/control nets, FT5426 I2C,
  backlight power control, side buttons.

storage_expansion.kicad_sch:
  QSPI NOR, Qwiic/STEMMA QT I2C, compact UART/SPI pads, external-host TROPIC01
  selection path.

optional_profiles.kicad_sch:
  NFC controller, crystal, matching network, antenna connector/keepout symbols,
  optional haptic/tamper footprints if retained as non-core unpopulated options.
```

- [ ] **Step 4: Use these global net names**

Apply exact net names consistently:

```text
+VBUS_PROT
+SYS
+3V3
+3V3_TROPIC_SW
+3V3_NFC_SW
+3V3_DISP_SW
+BATT
USB_DP
USB_DM
USB_CC1
USB_CC2
SPI_TROPIC_SCK
SPI_TROPIC_MOSI
SPI_TROPIC_MISO
SPI_TROPIC_CSN
TROPIC_GPO
TROPIC_PWR_EN
I2C_SEC_SCL
I2C_SEC_SDA
I2C_TOUCH_SCL
I2C_TOUCH_SDA
SPI_NFC_SCK
SPI_NFC_MOSI
SPI_NFC_MISO
SPI_NFC_CSN
NFC_IRQ
NFC_EN
QSPI_CLK
QSPI_CS
QSPI_IO0
QSPI_IO1
QSPI_IO2
QSPI_IO3
BTN_LEFT
BTN_RIGHT
SWDIO
SWCLK
NRST
BOOT0
UART_TX
UART_RX
```

- [ ] **Step 5: Generate a schematic netlist**

Run:

```bash
kicad-cli sch export netlist pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_sch -o /tmp/tropic01-universal-secure-device.net
```

Expected: command exits 0 and the netlist includes more than 50 named nets.

- [ ] **Step 6: Add source validation tests for second SE and real nets**

In `tests/test_validate_hardware.py`, add:

```python
    def test_tropic01_universal_secure_device_kicad_sources_include_second_secure_element_sheet(self) -> None:
        base = ROOT / "pcb/tropic01-universal-secure-device/kicad"

        self.assertTrue((base / "sheets" / "secure_element_2.kicad_sch").exists())
        sheet = (base / "sheets" / "secure_element_2.kicad_sch").read_text(encoding="utf-8").lower()
        self.assertIn("optiga", sheet)
        self.assertIn("i2c", sheet)
        self.assertIn("u11", sheet)
```

- [ ] **Step 7: Run KiCad source tests**

Run:

```bash
python3 -m unittest tests.test_validate_hardware.HardwareValidationTests.test_tropic01_universal_secure_device_kicad_sources_exist tests.test_validate_hardware.HardwareValidationTests.test_tropic01_universal_secure_device_kicad_sources_include_second_secure_element_sheet tests.test_validate_hardware.HardwareValidationTests.test_tropic01_universal_secure_device_tropic01_sheet_uses_verified_symbol tests.test_validate_hardware.HardwareValidationTests.test_tropic01_universal_secure_device_stm32u5_sheet_uses_verified_symbol -v
```

Expected: all source-shape tests pass.

- [ ] **Step 8: Commit schematic source rebuild**

Run:

```bash
git add pcb/tropic01-universal-secure-device/kicad tests/test_validate_hardware.py
git add -u pcb/tropic01-universal-secure-device
git commit -m "feat: rebuild tropic01 schematic source"
```

### Task 6: Replace the Placement Mockup With Product Placement Rules

**Files:**
- Modify: `scripts/materialize_tropic01_universal_placement.py`
- Modify: `pcb/tropic01-universal-secure-device/design-notes/placement.md`
- Modify: `pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_pcb`
- Test: `tests/test_validate_hardware.py`

- [ ] **Step 1: Set compact portrait board dimensions**

Update placement constants:

```python
BOARD_WIDTH_MM = 48.0
BOARD_HEIGHT_MM = 68.0
DISPLAY_WIDTH_MM = 42.8
DISPLAY_HEIGHT_MM = 59.91
```

This keeps the board close to the selected display while allowing edge space for USB-C, side buttons, NFC keepout, and assembly tolerances.

- [ ] **Step 2: Set fixed edge placement zones**

Use these product zones:

```python
TOP_NFC_ZONE_Y_MM = 4.0
DISPLAY_CENTER_X_MM = BOARD_WIDTH_MM / 2
DISPLAY_CENTER_Y_MM = 32.0
USB_CENTER_X_MM = BOARD_WIDTH_MM / 2
USB_CENTER_Y_MM = BOARD_HEIGHT_MM - 2.5
LEFT_BUTTON_X_MM = 1.8
RIGHT_BUTTON_X_MM = BOARD_WIDTH_MM - 1.8
SIDE_BUTTON_Y_MM = 20.0
```

- [ ] **Step 3: Update required placements**

Ensure `build_placement_plan()` returns placements for:

```text
J1 bottom-center USB-C receptacle
J2/J2B display FFC connectors behind the display
SW1/SW2 side-actuated buttons on the long edges
U1 STM32U5 on back-center
U2 TROPIC01 close to U1
U11 OPTIGA near U1 but on I2C side
U9 ST25R3916B near top NFC zone
U10 BQ24074 near battery connector
J9 LiPo connector on the back/edge
U5 QSPI flash near U1
TP_SWDIO/TP_SWCLK/TP_NRST/TP_BOOT0 hidden back-side test pads
ANT1 top-edge antenna FPC/keepout marker, not a copper loop
```

- [ ] **Step 4: Remove decorative NFC loop rendering**

Update `render_portrait_drawings()` so it outputs:

```text
ANT1 TOP EDGE NFC ANTENNA FPC OR TUNED KEEP-OUT
```

and no string containing:

```text
PCB NFC LOOP
```

- [ ] **Step 5: Apply placement through KiCad MCP or KiCad source edit**

Use KiCad MCP when KiCad is open:

```text
kicad_move_footprint for each ref in the placement plan
kicad_flip_footprint for back-side parts where required
kicad_save_board
```

If KiCad is closed, use the placement script to materialize positions into
`tropic01-universal-secure-device.kicad_pcb`, then open KiCad and inspect.

- [ ] **Step 6: Confirm board outline with KiCad MCP**

Run MCP calls:

```text
kicad_get_board_outline
kicad_get_footprints
```

Expected:

```text
Board outline approximately 48 mm x 68 mm.
J1 centered on bottom short edge.
U9/ANT1 near top short edge.
SW1/SW2 on upper long edges with side-facing orientation.
U1/U2/U11 on back-side secure island.
Display connectors placed behind display envelope.
```

- [ ] **Step 7: Run placement tests**

Run:

```bash
python3 -m unittest tests.test_validate_hardware.HardwareValidationTests.test_tropic01_universal_secure_device_placement_plan_is_portrait_and_includes_critical_parts tests.test_validate_hardware.HardwareValidationTests.test_tropic01_universal_secure_device_board_drawings_include_display_and_nfc_features tests.test_validate_hardware.HardwareValidationTests.test_tropic01_universal_secure_device_materializer_outputs_no_placeholder_footprints -v
```

Expected: all placement tests pass.

- [ ] **Step 8: Commit placement**

Run:

```bash
git add scripts/materialize_tropic01_universal_placement.py pcb/tropic01-universal-secure-device/design-notes/placement.md pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_pcb tests/test_validate_hardware.py
git commit -m "feat: place final tropic01 portrait board"
```

### Task 7: Route and Validate the Board in KiCad

**Files:**
- Modify: `pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_pcb`
- Modify: `pcb/tropic01-universal-secure-device/design-notes/datasheets.md`
- Modify: `pcb/tropic01-universal-secure-device/design-notes/pinmux.md`
- Modify: `pcb/tropic01-universal-secure-device/design-notes/component-freeze.md`

- [ ] **Step 1: Route power and ground**

Create:

```text
L2 continuous GND plane.
L3 power pours for +3V3, +SYS, +3V3_TROPIC_SW, +3V3_NFC_SW, +3V3_DISP_SW.
Short VBUS path from USB-C to protection/current limit/power path.
Local decoupling at U1, U2, U9, U10, U11, U5, display connectors.
```

- [ ] **Step 2: Route USB**

Route:

```text
USB_DP and USB_DM as short matched pair from J1 through ESD to STM32U5.
CC1 and CC2 to 5.1 kOhm Rd pull-downs.
VBUS through current-limit/protection before system power path.
```

- [ ] **Step 3: Route secure island**

Route:

```text
SPI_TROPIC_SCK/MOSI/MISO/CSN short between STM32U5 and TROPIC01.
TROPIC_GPO to STM32U5 with polling fallback documented.
TROPIC_PWR_EN to the TROPIC01 load switch.
I2C_SEC_SCL/SDA from STM32U5 to OPTIGA with local pullups.
No display traffic on the TROPIC01 SPI nets.
```

- [ ] **Step 4: Route display and touch**

Route:

```text
Display SPI/control nets to J2.
Touch I2C/IRQ/reset nets to J2B.
Backlight power through controlled display power path.
```

- [ ] **Step 5: Route NFC**

Route:

```text
SPI_NFC_* nets from STM32U5 to ST25R3916B.
NFC_IRQ and NFC_EN.
27.12 MHz crystal close to U9.
Matching network between U9 and antenna FPC/keepout.
Top-edge antenna keepout free from ground, battery metal, and display metal according to selected antenna strategy.
```

- [ ] **Step 6: Route storage, buttons, battery, and test**

Route:

```text
QSPI_* nets from STM32U5 to W25Q128JV.
BTN_LEFT and BTN_RIGHT to side switches with pull strategy documented.
BQ24074 status and battery sense to STM32U5.
SWD/UART/rail pogo pads on back side.
Qwiic I2C with power-limited 3V3.
External-host SPI selection path isolated from STM32U5 for hardened builds.
```

- [ ] **Step 7: Run ERC**

Run:

```bash
kicad-cli sch erc pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_sch --output pcb/tropic01-universal-secure-device/production/erc/erc.json --format json
```

Expected: exit 0. If ERC reports warnings, document each accepted warning in `pcb/tropic01-universal-secure-device/production/reports/erc-waivers.md` with the exact rule and reason.

- [ ] **Step 8: Run DRC**

Run:

```bash
kicad-cli pcb drc pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_pcb --output pcb/tropic01-universal-secure-device/production/drc/drc.json --format json
```

Expected: exit 0. If DRC reports warnings, document each accepted warning in `pcb/tropic01-universal-secure-device/production/reports/drc-waivers.md` with the exact rule and reason.

- [ ] **Step 9: Inspect through KiCad MCP**

Run MCP calls:

```text
kicad_get_board_summary
kicad_get_tracks
kicad_get_vias
kicad_get_zones
kicad_get_items_by_net for USB_DP, USB_DM, SPI_TROPIC_SCK, +3V3, GND
```

Expected:

```text
Net count is much greater than 1.
Track count is non-zero.
Via count is non-zero for a 4-layer board unless routing is entirely same-side by design.
Zones include GND and power pours.
Critical nets have connected copper items.
```

- [ ] **Step 10: Commit routed KiCad board**

Run:

```bash
git add pcb/tropic01-universal-secure-device/kicad pcb/tropic01-universal-secure-device/design-notes pcb/tropic01-universal-secure-device/production/erc pcb/tropic01-universal-secure-device/production/drc pcb/tropic01-universal-secure-device/production/reports
git commit -m "feat: route tropic01 universal secure device"
```

### Task 8: Guard and Regenerate PCBWay Outputs

**Files:**
- Modify: `scripts/export_tropic01_universal_pcbway.py`
- Modify: `pcb/tropic01-universal-secure-device/production/README.md`
- Generate: `pcb/tropic01-universal-secure-device/production/gerbers/*`
- Generate: `pcb/tropic01-universal-secure-device/production/drill/*`
- Generate: `pcb/tropic01-universal-secure-device/production/position/pcbway-position.csv`
- Generate: `pcb/tropic01-universal-secure-device/production/bom/pcbway-bom.csv`
- Generate: `pcb/tropic01-universal-secure-device/production/step/tropic01-universal-secure-device.step`
- Generate: `pcb/tropic01-universal-secure-device/production/pcbway-manifest.json`
- Generate: `pcb/tropic01-universal-secure-device/production/pcbway-review-package.zip`

- [ ] **Step 1: Add export guard checks**

In `scripts/export_tropic01_universal_pcbway.py`, block export unless:

```python
required_checks = {
    "erc_json_exists": production_root / "erc" / "erc.json",
    "drc_json_exists": production_root / "drc" / "drc.json",
    "board_has_tracks": kicad_board_path,
    "board_has_more_than_one_net": kicad_board_path,
}
```

The implementation can parse the KiCad PCB text for `(net ` entries and `(segment ` entries. It must raise `ValueError("PCBWay export blocked: board is not routed")` when the board has no tracks or only one net.

- [ ] **Step 2: Add a test for export blocking**

In `tests/test_validate_hardware.py`, add:

```python
    def test_tropic01_universal_secure_device_pcbway_export_rejects_unrouted_board(self) -> None:
        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            board = root / "board.kicad_pcb"
            board.write_text('(kicad_pcb (version 20240108) (net 0 ""))', encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "not routed"):
                export_tropic01_universal_pcbway.validate_board_ready_for_export(board)
```

- [ ] **Step 3: Run exporter tests**

Run:

```bash
python3 -m unittest tests.test_validate_hardware.HardwareValidationTests.test_tropic01_universal_secure_device_pcbway_export_rejects_unrouted_board tests.test_validate_hardware.HardwareValidationTests.test_tropic01_universal_secure_device_pcbway_bom_export_matches_materialized_refs -v
```

Expected: both tests pass.

- [ ] **Step 4: Regenerate fabrication files**

Run the project export script:

```bash
python3 scripts/export_tropic01_universal_pcbway.py
```

Expected: Gerbers, drill, position CSV, PCBWay BOM, STEP, manifest, and ZIP are regenerated from the routed design.

- [ ] **Step 5: Inspect the manifest**

Run:

```bash
python3 -m json.tool pcb/tropic01-universal-secure-device/production/pcbway-manifest.json
```

Expected manifest fields include:

```json
{
  "board": "tropic01-universal-secure-device",
  "usb_connector": "USB4105-GF-A",
  "second_secure_element": "OPTIGA-TRUST-M-SLS32AIA",
  "microsd": "excluded",
  "erc": "pass",
  "drc": "pass"
}
```

- [ ] **Step 6: Commit production export**

Run:

```bash
git add scripts/export_tropic01_universal_pcbway.py tests/test_validate_hardware.py pcb/tropic01-universal-secure-device/production
git commit -m "feat: export guarded tropic01 pcbway package"
```

### Task 9: Final Repository Verification

**Files:**
- All changed files.

- [ ] **Step 1: Run the full hardware test suite**

Run:

```bash
python3 -m unittest tests.test_validate_hardware -v
```

Expected: all tests pass.

- [ ] **Step 2: Run repository validator**

Run:

```bash
python3 scripts/validate_hardware.py
```

Expected: command exits 0.

- [ ] **Step 3: Run stale custom hardware scan**

Run:

```bash
rg -n "custom-persistent-secret-wallet|persistent secret wallet|second secure element.*DNP|microSD_dnp|USB-C plug|PCB NFC LOOP|unrouted.*ready|1 net" README.md docs bom pcb scripts tests
```

Expected: no stale product claims remain. A test may mention rejected strings only if the test is explicitly asserting rejection.

- [ ] **Step 4: Inspect KiCad state via MCP**

Run MCP calls:

```text
ping_kicad
kicad_get_board_summary
kicad_get_board_outline
kicad_get_footprints
kicad_get_tracks
kicad_get_vias
kicad_get_zones
```

Expected:

```text
KiCad connection works.
Board outline is compact portrait.
Footprints include J1, U1, U2, U9, U10, U11, J2, J2B, SW1, SW2.
Tracks, vias, nets, and zones are non-empty.
```

- [ ] **Step 5: Write final implementation note**

Create `pcb/tropic01-universal-secure-device/production/reports/release-readiness.md` with:

```markdown
# Rev A0 Release Readiness

Date: 2026-06-08

## Checks

- Requirements validation: pass
- BOM validation: pass
- KiCad ERC: pass
- KiCad DRC: pass
- PCBWay BOM generated: pass
- PCBWay position generated: pass
- Gerbers generated: pass
- Drill generated: pass
- STEP generated: pass

## Known Manufacturing Notes

- NFC antenna requires measurement and tuning on first articles before security
  or RF performance claims.
- OPTIGA Trust M orderable part number must be confirmed against distributor
  stock before purchase order.
- Display FFC connector footprints must be inspected against Newhaven mechanical
  drawings before purchase order.
- The first PCBWay order is Rev A0 validation hardware, not a certified product.
```

- [ ] **Step 6: Commit final verification note**

Run:

```bash
git add pcb/tropic01-universal-secure-device/production/reports/release-readiness.md
git commit -m "docs: record tropic01 rev a0 readiness"
```

## Self-Review

- Spec coverage: covered product form, TROPIC01, STM32U5, display, USB-C, NFC, battery, OPTIGA second SE, QSPI flash, side buttons, pogo pads, expansion, microSD exclusion, no BLE/WiFi, validation criteria, and PCBWay export gating.
- Placeholder scan: this plan contains no unresolved placeholder markers.
- Type/name consistency: final product terms use `second_secure_element_i2c`, `hidden_pogo_test_pads`, `no_microsd_slot`, `USB4105-GF-A`, `OPTIGA-TRUST-M-SLS32AIA`, and `TR01-C2P-T301` consistently.
- Scope split: implementation is split into contract/tests, validator/requirements, BOM/export, docs, KiCad schematic, placement, routing, PCBWay export, and final verification.
