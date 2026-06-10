#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import uuid
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOARD_NAME = "tropic01-universal-secure-device"
BOARD_DIR = ROOT / "pcb" / BOARD_NAME
KICAD_DIR = BOARD_DIR / "kicad"
SHEET_DIR = KICAD_DIR / "sheets"
SCHEMATIC_BINDING_JSON = BOARD_DIR / "production" / "schematic-binding.json"
KICAD_SYMBOLS = Path("/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols")
PROJECT_NAME = BOARD_NAME
ROOT_SHEET_UUID = "11111111-1111-4111-8111-111111111111"


STOCK_SYMBOL_LIBRARIES = {
    "Connector": KICAD_SYMBOLS / "Connector.kicad_sym",
    "Connector_Generic": KICAD_SYMBOLS / "Connector_Generic.kicad_sym",
    "MCU_ST_STM32U5": KICAD_SYMBOLS / "MCU_ST_STM32U5.kicad_sym",
    "Memory_Flash": KICAD_SYMBOLS / "Memory_Flash.kicad_sym",
    "Switch": KICAD_SYMBOLS / "Switch.kicad_sym",
    "TROPIC_SQUARE": KICAD_DIR / "lib" / "symbols" / "TROPIC01.kicad_sym",
}


@dataclass(frozen=True)
class SymbolSpec:
    ref: str
    value: str
    lib_id: str
    footprint: str
    datasheet: str
    description: str
    sheet: str
    x: float
    y: float


SHEET_UUIDS = {
    "kicad/sheets/power_usb.kicad_sch": "99999999-9999-4999-8999-999999999001",
    "kicad/sheets/stm32u5_host.kicad_sch": "99999999-9999-4999-8999-999999999002",
    "kicad/sheets/tropic01.kicad_sch": "99999999-9999-4999-8999-999999999003",
    "kicad/sheets/display_controls.kicad_sch": "99999999-9999-4999-8999-999999999004",
    "kicad/sheets/storage_expansion.kicad_sch": "99999999-9999-4999-8999-999999999005",
    "kicad/sheets/optional_profiles.kicad_sch": "99999999-9999-4999-8999-999999999006",
    "kicad/sheets/secure_element_2.kicad_sch": "99999999-9999-4999-8999-999999999008",
}

ROOT_CHILD_SHEET_UUIDS = {
    "kicad/sheets/power_usb.kicad_sch": "22222222-2222-4222-8222-222222222222",
    "kicad/sheets/stm32u5_host.kicad_sch": "33333333-3333-4333-8333-333333333333",
    "kicad/sheets/tropic01.kicad_sch": "44444444-4444-4444-8444-444444444444",
    "kicad/sheets/display_controls.kicad_sch": "55555555-5555-4555-8555-555555555555",
    "kicad/sheets/storage_expansion.kicad_sch": "66666666-6666-4666-8666-666666666666",
    "kicad/sheets/optional_profiles.kicad_sch": "77777777-7777-4777-8777-777777777777",
    "kicad/sheets/secure_element_2.kicad_sch": "88888888-8888-4888-8888-777777777777",
}

SHEET_NOTES = {
    "kicad/sheets/power_usb.kicad_sch": [
        "USB-C Rev A0 is USB 2.0 device/sink only.",
        "Use two 5.1 kOhm Rd resistors: CC1 to GND and CC2 to GND.",
        "LiPo connector is present; final charger/power-path implementation remains layout reviewed.",
    ],
    "kicad/sheets/stm32u5_host.kicad_sch": [
        "Primary host candidate: STM32U585VIT6 LQFP100. Fallback: STM32U575VIT6 LQFP100.",
        "Host owns USB, display, controls, policy, QSPI state, expansion policy, and TROPIC01 host-side key protection.",
        "Before production claims: TrustZone/RDP/debug lock/signed firmware and isolated host-key storage.",
    ],
    "kicad/sheets/tropic01.kicad_sch": [
        "TROPIC01 QFN32 secure element. Default part TR01-C2P-T301; preferred part TR01-C2P-T310 when obtainable.",
        "TROPIC01 is 3.0 V to 3.6 V only. External-host SPI is 3.3 V logic only.",
        "GPO is routed, but firmware must support polling fallback.",
        "Recovery is by load-switched VCC power-cycle, not a reset pin.",
    ],
    "kicad/sheets/display_controls.kicad_sch": [
        "Display target: portrait EastRising ER-TFT024IPS-3, ST7789V plus FT6336 capacitive touch on one 50-pin FFC.",
        "Touch is the default navigation surface. Two side buttons are the production approval boundary.",
        "Display SPI remains separate from TROPIC01 SPI in Rev A0.",
    ],
    "kicad/sheets/storage_expansion.kicad_sch": [
        "QSPI target: W25Q128JV-class 128 Mbit NOR. QSPI is not secure storage by itself.",
        "Expansion I2C/SPI connector assignment remains review-gated; UART pins are source-backed.",
    ],
    "kicad/sheets/optional_profiles.kicad_sch": [
        "NFC ST25R3916B-class core surface: power-gated and top-edge antenna keep-out.",
        "Antenna nets remain measurement-gated until FPC/matching/enclosure are finalized.",
        "Removable card slot omitted from this single product; use QSPI, USB, NFC, QR/display, or host workflows.",
    ],
    "kicad/sheets/secure_element_2.kicad_sch": [
        "U11 OPTIGA Trust M class second secure element is mounted in the single product.",
        "U11 connects to STM32U5 over dedicated I2C_SEC_SCL and I2C_SEC_SDA nets with local pullups and decoupling.",
        "TROPIC01 remains the primary open secure element; OPTIGA provides independent defense-in-depth attestation and anti-clone policy.",
        "Footprint candidate must be verified against Infineon PG-USON-10 before layout freeze.",
    ],
}

SYMBOLS = {
    "U1": SymbolSpec(
        ref="U1",
        value="STM32U585VIT6",
        lib_id="MCU_ST_STM32U5:STM32U585VITx",
        footprint="Package_QFP:LQFP-100_14x14mm_P0.5mm",
        datasheet="https://www.st.com/resource/en/datasheet/stm32u585vi.pdf",
        description="STM32U585VIT6 Rev A0 host MCU candidate, LQFP100, 2 MB flash, 786 KB SRAM, TrustZone",
        sheet="kicad/sheets/stm32u5_host.kicad_sch",
        x=119.38,
        y=114.30,
    ),
    "U2": SymbolSpec(
        ref="U2",
        value="TR01-C2P-T301",
        lib_id="TROPIC_SQUARE:TR01-P2",
        footprint="Package_DFN_QFN:QFN-32-1EP_4x4mm_P0.4mm_EP2.65x2.65mm",
        datasheet="https://github.com/tropicsquare/tropic01/blob/main/doc/TR01-C2P-T310/ODD_TR01_datasheet_vA_11.pdf",
        description="TROPIC01 cryptographic coprocessor; Rev A0 default TR01-C2P-T301, preferred TR01-C2P-T310 when available",
        sheet="kicad/sheets/tropic01.kicad_sch",
        x=114.30,
        y=105.41,
    ),
    "J1": SymbolSpec(
        ref="J1",
        value="USB4105-GF-A",
        lib_id="Connector:USB_C_Receptacle_USB2.0_16P",
        footprint="Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal",
        datasheet="https://gct.co/connector/usb4105",
        description="GCT USB4105 USB 2.0 Type-C receptacle, female USB-C only",
        sheet="kicad/sheets/power_usb.kicad_sch",
        x=105.41,
        y=95.25,
    ),
    "J2": SymbolSpec(
        ref="J2",
        value="ER-TFT024IPS-3 50P FFC",
        lib_id="Connector_Generic:Conn_01x50",
        footprint="Connector_FFC-FPC:Hirose_FH12-50S-0.5SH_1x50-1MP_P0.50mm_Horizontal",
        datasheet="https://www.buydisplay.com/download/manual/ER-TFT024IPS-3_Datasheet.pdf",
        description="50-pin 0.5mm FFC carrying display SPI and capacitive touch I2C for EastRising ER-TFT024IPS-3",
        sheet="kicad/sheets/display_controls.kicad_sch",
        x=80.01,
        y=114.30,
    ),
    "U5": SymbolSpec(
        ref="U5",
        value="W25Q128JVSIQ",
        lib_id="Memory_Flash:W25Q32JVSS",
        footprint="Package_SO:SOIC-8_5.3x5.3mm_P1.27mm",
        datasheet="https://www.winbond.com/resource-files/w25q128jv_dtr%20revc%2003272018%20plus.pdf",
        description="128 Mbit SPI/QSPI NOR flash using the KiCad W25Q32JVSS pin-compatible symbol",
        sheet="kicad/sheets/storage_expansion.kicad_sch",
        x=110.49,
        y=95.25,
    ),
    "U9": SymbolSpec(
        ref="U9",
        value="ST25R3916B-AQET",
        lib_id="TROPIC_SQUARE:ST25R3916B_QFN32",
        footprint="Package_DFN_QFN:QFN-32-1EP_5x5mm_P0.5mm_EP3.7x3.7mm",
        datasheet="https://www.st.com/resource/en/datasheet/st25r3916b.pdf",
        description="ST25R3916B NFC/RFID front-end, QFN32",
        sheet="kicad/sheets/optional_profiles.kicad_sch",
        x=114.30,
        y=100.33,
    ),
    "U11": SymbolSpec(
        ref="U11",
        value="OPTIGA-TRUST-M-SLS32AIA",
        lib_id="TROPIC_SQUARE:OPTIGA_TRUST_M_USON10",
        footprint="Package_SON:Microchip_USON-10-1EP_3x3mm_P0.5mm_EP1.8x2.5mm",
        datasheet="https://www.infineon.com/assets/row/public/documents/30/49/infineon-optiga-trust-m-sls32aia-datasheet-en.pdf",
        description="OPTIGA Trust M class second secure element, PG-USON-10 candidate footprint",
        sheet="kicad/sheets/secure_element_2.kicad_sch",
        x=110.49,
        y=90.17,
    ),
    "SW1": SymbolSpec(
        ref="SW1",
        value="LEFT_SIDE_APPROVE",
        lib_id="Switch:SW_Push",
        footprint="Button_Switch_SMD:SW_SPST_EVQP7A",
        datasheet="https://industrial.panasonic.com/ac/e/search_num/index.jsp?c=detail&part_no=EVQP7J01P",
        description="Left side-actuated production approval button",
        sheet="kicad/sheets/display_controls.kicad_sch",
        x=139.70,
        y=105.41,
    ),
    "SW2": SymbolSpec(
        ref="SW2",
        value="RIGHT_SIDE_CANCEL",
        lib_id="Switch:SW_Push",
        footprint="Button_Switch_SMD:SW_SPST_EVQP7A",
        datasheet="https://industrial.panasonic.com/ac/e/search_num/index.jsp?c=detail&part_no=EVQP7J01P",
        description="Right side-actuated production cancel button",
        sheet="kicad/sheets/display_controls.kicad_sch",
        x=139.70,
        y=119.38,
    ),
    "J9": SymbolSpec(
        ref="J9",
        value="LiPo 2-pin JST PH",
        lib_id="Connector_Generic:Conn_01x02",
        footprint="Connector_JST:JST_PH_S2B-PH-SM4-TB_1x02-1MP_P2.00mm_Horizontal",
        datasheet="https://www.jst.com/products/crimp-style-connectors-wire-to-board-type/ph-connector/",
        description="2-pin LiPo battery connector into charger/power path",
        sheet="kicad/sheets/power_usb.kicad_sch",
        x=105.41,
        y=134.62,
    ),
}


def deterministic_uuid(*parts: object) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "nsealr:" + ":".join(str(part) for part in parts)))


def extract_symbol_block(library_text: str, symbol_name: str, lib_id: str) -> str:
    marker = f'\t(symbol "{symbol_name}"'
    start = library_text.find(marker)
    if start == -1:
        marker = f'(symbol "{symbol_name}"'
        start = library_text.index(marker)
    block_start = library_text.index("(symbol", start)
    depth = 0
    for index in range(block_start, len(library_text)):
        if library_text[index] == "(":
            depth += 1
        elif library_text[index] == ")":
            depth -= 1
            if depth == 0:
                block = library_text[block_start : index + 1]
                return block.replace(f'(symbol "{symbol_name}"', f'(symbol "{lib_id}"', 1)
    raise ValueError(f"unterminated symbol block for {symbol_name}")


def stock_symbol_block(lib_id: str) -> str:
    library_name, symbol_name = lib_id.split(":", 1)
    library_path = STOCK_SYMBOL_LIBRARIES[library_name]
    return extract_symbol_block(library_path.read_text(encoding="utf-8"), symbol_name, lib_id)


def custom_st25_symbol() -> str:
    left = [
        ("1", "VDD_IO"),
        ("6", "GND_D"),
        ("8", "VDD"),
        ("10", "VDD_TX"),
        ("12", "GND_DR1"),
        ("16", "GND_DR2"),
        ("20", "I2C_EN"),
        ("21", "VSS"),
        ("26", "GND_A"),
    ]
    right = [
        ("27", "IRQ"),
        ("29", "BSS"),
        ("30", "SCLK"),
        ("31", "MOSI"),
        ("32", "MISO"),
        ("33", "EP_GND"),
    ]
    lines = [
        '\t(symbol "TROPIC_SQUARE:ST25R3916B_QFN32"',
        "\t\t(exclude_from_sim no)",
        "\t\t(in_bom yes)",
        "\t\t(on_board yes)",
        '\t\t(property "Reference" "U" (at 0 22.86 0) (effects (font (size 1.27 1.27))))',
        '\t\t(property "Value" "ST25R3916B_QFN32" (at 0 20.32 0) (effects (font (size 1.27 1.27))))',
        '\t\t(property "Footprint" "Package_DFN_QFN:QFN-32-1EP_5x5mm_P0.5mm_EP3.7x3.7mm" (at 0 -22.86 0) (effects (font (size 1.27 1.27)) (hide yes)))',
        '\t\t(property "Datasheet" "https://www.st.com/resource/en/datasheet/st25r3916b.pdf" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))',
        '\t\t(property "Description" "ST25R3916B NFC/RFID front-end, QFN32 source-backed pin subset" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))',
        '\t\t(symbol "ST25R3916B_QFN32_0_1"',
        "\t\t\t(rectangle (start -12.7 17.78) (end 12.7 -17.78) (stroke (width 0.254) (type default)) (fill (type background)))",
        "\t\t)",
        '\t\t(symbol "ST25R3916B_QFN32_1_1"',
    ]
    for row, (number, name) in enumerate(left):
        y = 15.24 - row * 2.54
        lines.append(
            f'\t\t\t(pin bidirectional line (at -17.78 {y:.2f} 0) (length 5.08) '
            f'(name "{name}" (effects (font (size 1.27 1.27)))) '
            f'(number "{number}" (effects (font (size 1.27 1.27)))))'
        )
    for row, (number, name) in enumerate(right):
        y = 12.70 - row * 2.54
        lines.append(
            f'\t\t\t(pin bidirectional line (at 17.78 {y:.2f} 180) (length 5.08) '
            f'(name "{name}" (effects (font (size 1.27 1.27)))) '
            f'(number "{number}" (effects (font (size 1.27 1.27)))))'
        )
    lines.extend(["\t\t)", "\t)"])
    return "\n".join(lines)


def custom_optiga_symbol() -> str:
    pins = [
        ("1", "GND", -17.78, 7.62, 0),
        ("3", "SDA", -17.78, 2.54, 0),
        ("8", "SCL", -17.78, 0.00, 0),
        ("9", "RST", -17.78, -2.54, 0),
        ("10", "VCC", 17.78, 7.62, 180),
    ]
    lines = [
        '\t(symbol "TROPIC_SQUARE:OPTIGA_TRUST_M_USON10"',
        "\t\t(exclude_from_sim no)",
        "\t\t(in_bom yes)",
        "\t\t(on_board yes)",
        '\t\t(property "Reference" "U" (at 0 12.70 0) (effects (font (size 1.27 1.27))))',
        '\t\t(property "Value" "OPTIGA_TRUST_M_USON10" (at 0 10.16 0) (effects (font (size 1.27 1.27))))',
        '\t\t(property "Footprint" "Package_SON:Microchip_USON-10-1EP_3x3mm_P0.5mm_EP1.8x2.5mm" (at 0 -12.70 0) (effects (font (size 1.27 1.27)) (hide yes)))',
        '\t\t(property "Datasheet" "https://www.infineon.com/assets/row/public/documents/30/49/infineon-optiga-trust-m-sls32aia-datasheet-en.pdf" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))',
        '\t\t(property "Description" "OPTIGA Trust M PG-USON-10 source-backed pin subset" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))',
        '\t\t(symbol "OPTIGA_TRUST_M_USON10_0_1"',
        "\t\t\t(rectangle (start -12.7 10.16) (end 12.7 -7.62) (stroke (width 0.254) (type default)) (fill (type background)))",
        "\t\t)",
        '\t\t(symbol "OPTIGA_TRUST_M_USON10_1_1"',
    ]
    for number, name, x, y, rotation in pins:
        lines.append(
            f'\t\t\t(pin bidirectional line (at {x:.2f} {y:.2f} {rotation}) (length 5.08) '
            f'(name "{name}" (effects (font (size 1.27 1.27)))) '
            f'(number "{number}" (effects (font (size 1.27 1.27)))))'
        )
    lines.extend(["\t\t)", "\t)"])
    return "\n".join(lines)


def symbol_cache(lib_id: str) -> str:
    if lib_id == "TROPIC_SQUARE:ST25R3916B_QFN32":
        return custom_st25_symbol()
    if lib_id == "TROPIC_SQUARE:OPTIGA_TRUST_M_USON10":
        return custom_optiga_symbol()
    return stock_symbol_block(lib_id)


def parse_pin_positions(symbol_block: str) -> dict[str, tuple[float, float, int]]:
    pins: dict[str, tuple[float, float, int]] = {}
    index = 0
    while True:
        pin_pos = symbol_block.find("(pin ", index)
        if pin_pos == -1:
            return pins
        depth = 0
        end = None
        for cursor in range(pin_pos, len(symbol_block)):
            if symbol_block[cursor] == "(":
                depth += 1
            elif symbol_block[cursor] == ")":
                depth -= 1
                if depth == 0:
                    end = cursor + 1
                    break
        if end is None:
            raise ValueError("unterminated pin block")
        block = symbol_block[pin_pos:end]
        number_match = re.search(r'\(number "([^"]+)"', block)
        at_match = re.search(r"\(at ([-0-9.]+) ([-0-9.]+) ([-0-9]+)\)", block)
        if number_match and at_match:
            pins[number_match.group(1)] = (
                float(at_match.group(1)),
                float(at_match.group(2)),
                int(at_match.group(3)),
            )
        index = end


def symbol_instance(spec: SymbolSpec, sheet_uuid: str) -> str:
    symbol_uuid = deterministic_uuid("symbol", spec.ref)
    instance_path = f"/{ROOT_SHEET_UUID}/{ROOT_CHILD_SHEET_UUIDS[spec.sheet]}"
    return f'''\
\t(symbol
\t\t(lib_id "{spec.lib_id}")
\t\t(at {spec.x:.2f} {spec.y:.2f} 0)
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{symbol_uuid}")
\t\t(property "Reference" "{spec.ref}"
\t\t\t(at {spec.x - 10.0:.2f} {spec.y + 12.0:.2f} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t)
\t\t(property "Value" "{spec.value}"
\t\t\t(at {spec.x - 10.0:.2f} {spec.y + 14.5:.2f} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t)
\t\t(property "Footprint" "{spec.footprint}"
\t\t\t(at {spec.x:.2f} {spec.y:.2f} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
\t\t(property "Datasheet" "{spec.datasheet}"
\t\t\t(at {spec.x:.2f} {spec.y:.2f} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
\t\t(property "Description" "{spec.description}"
\t\t\t(at {spec.x:.2f} {spec.y:.2f} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
\t\t(instances
\t\t\t(project "{PROJECT_NAME}"
\t\t\t\t(path "{instance_path}"
\t\t\t\t\t(reference "{spec.ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)'''


def label_endpoint(x: float, y: float, rotation: int, distance: float = 7.62) -> tuple[float, float]:
    if rotation == 0:
        return x - distance, y
    if rotation == 180:
        return x + distance, y
    if rotation == 90:
        return x, y - distance
    if rotation == 270:
        return x, y + distance
    return x + distance, y


def net_label(spec: SymbolSpec, pin_number: str, net_name: str, pin_positions: dict[str, tuple[float, float, int]]) -> str:
    if pin_number not in pin_positions:
        raise ValueError(f"{spec.ref} {spec.lib_id} has no pin {pin_number} for {net_name}")
    rel_x, rel_y, rotation = pin_positions[pin_number]
    x = spec.x + rel_x
    y = spec.y + rel_y
    end_x, end_y = label_endpoint(x, y, rotation)
    wire_uuid = deterministic_uuid("wire", spec.ref, pin_number, net_name)
    label_uuid = deterministic_uuid("global_label", spec.ref, pin_number, net_name)
    return f'''\
\t(wire
\t\t(pts
\t\t\t(xy {x:.2f} {y:.2f}) (xy {end_x:.2f} {end_y:.2f})
\t\t)
\t\t(stroke (width 0) (type default))
\t\t(uuid "{wire_uuid}")
\t)
\t(global_label "{net_name}"
\t\t(shape input)
\t\t(at {end_x:.2f} {end_y:.2f} {rotation})
\t\t(fields_autoplaced)
\t\t(effects (font (size 1.27 1.27)))
\t\t(uuid "{label_uuid}")
\t)'''


def text_note(text: str, x: float, y: float, token: str) -> str:
    return f'''\
\t(text "{text}"
\t\t(exclude_from_sim no)
\t\t(at {x:.2f} {y:.2f} 0)
\t\t(effects (font (size 1.27 1.27)))
\t\t(uuid "{deterministic_uuid("text", token, text)}")
\t)'''


def sheet_text(sheet: str, specs: list[SymbolSpec], binding: dict[str, object]) -> str:
    sheet_uuid = SHEET_UUIDS[sheet]
    caches_by_lib_id = {spec.lib_id: symbol_cache(spec.lib_id) for spec in specs}
    pin_positions_by_lib_id = {lib_id: parse_pin_positions(block) for lib_id, block in caches_by_lib_id.items()}
    lib_symbols = "\n".join(caches_by_lib_id[lib_id] for lib_id in sorted(caches_by_lib_id))
    symbols = [symbol_instance(spec, sheet_uuid) for spec in specs]
    labels = []
    for spec in specs:
        pins = binding["components"][spec.ref]["pins"]
        pin_positions = pin_positions_by_lib_id[spec.lib_id]
        for pin_key, pin in sorted(pins.items(), key=lambda item: str(item[0])):
            pin_number = str(pin.get("physical_pin", pin_key))
            labels.append(net_label(spec, pin_number, pin["net"], pin_positions))
    notes = [text_note(note, 20.0, 20.0 + index * 8.0, sheet) for index, note in enumerate(SHEET_NOTES.get(sheet, []))]
    return f'''\
(kicad_sch
\t(version 20260306)
\t(generator "eeschema")
\t(generator_version "10.0")
\t(uuid "{sheet_uuid}")
\t(paper "A4")
\t(lib_symbols
{lib_symbols}
\t)
{chr(10).join(notes)}
{chr(10).join(symbols)}
{chr(10).join(labels)}
\t(sheet_instances
\t\t(path "/"
\t\t\t(page "1")
\t\t)
\t)
\t(embedded_fonts no)
)
'''


def materialize_schematics() -> None:
    materialize_project_symbol_library()
    binding = json.loads(SCHEMATIC_BINDING_JSON.read_text(encoding="utf-8"))
    specs_by_sheet: dict[str, list[SymbolSpec]] = {}
    for ref in binding["components"]:
        if ref not in SYMBOLS:
            continue
        spec = SYMBOLS[ref]
        specs_by_sheet.setdefault(spec.sheet, []).append(spec)
    for sheet, specs in sorted(specs_by_sheet.items()):
        path = BOARD_DIR / sheet
        path.write_text(sheet_text(sheet, sorted(specs, key=lambda spec: spec.ref), binding), encoding="utf-8")


def materialize_project_symbol_library() -> None:
    library_path = KICAD_DIR / "lib" / "symbols" / "TROPIC01.kicad_sym"
    text = library_path.read_text(encoding="utf-8")
    custom_blocks = [custom_st25_symbol().replace('TROPIC_SQUARE:', ''), custom_optiga_symbol().replace('TROPIC_SQUARE:', '')]
    body = text.rsplit("\n)", 1)[0]
    changed = False
    for block in custom_blocks:
        symbol_name = re.search(r'\(symbol "([^"]+)"', block)
        if symbol_name is None:
            raise ValueError("custom symbol block is malformed")
        if f'(symbol "{symbol_name.group(1)}"' not in text:
            body += "\n" + block
            changed = True
    if changed:
        library_path.write_text(body + "\n)\n", encoding="utf-8")


def main() -> int:
    materialize_schematics()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
