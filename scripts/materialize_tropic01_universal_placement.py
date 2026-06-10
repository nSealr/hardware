#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOARD_NAME = "tropic01-universal-secure-device"
PLACEMENT_JSON = ROOT / "pcb" / BOARD_NAME / "production" / "placement-plan.json"
KICAD_BOARD = ROOT / "pcb" / BOARD_NAME / "kicad" / f"{BOARD_NAME}.kicad_pcb"

BOARD_ORIGIN_X_MM = 10.0
BOARD_ORIGIN_Y_MM = 10.0
BOARD_WIDTH_MM = 48.0
BOARD_HEIGHT_MM = 68.0
BOARD_END_X_MM = BOARD_ORIGIN_X_MM + BOARD_WIDTH_MM
BOARD_END_Y_MM = BOARD_ORIGIN_Y_MM + BOARD_HEIGHT_MM

DISPLAY_WIDTH_MM = 42.72
DISPLAY_HEIGHT_MM = 59.46
DISPLAY_CENTER_X_MM = BOARD_ORIGIN_X_MM + BOARD_WIDTH_MM / 2.0
DISPLAY_CENTER_Y_MM = BOARD_ORIGIN_Y_MM + 32.0

USB_CENTER_X_MM = BOARD_ORIGIN_X_MM + BOARD_WIDTH_MM / 2.0
USB_CENTER_Y_MM = BOARD_END_Y_MM - 2.4
TOP_NFC_ZONE_Y_MM = BOARD_ORIGIN_Y_MM + 4.0
LEFT_BUTTON_X_MM = BOARD_ORIGIN_X_MM + 0.9
RIGHT_BUTTON_X_MM = BOARD_END_X_MM - 0.9
SIDE_BUTTON_Y_MM = BOARD_ORIGIN_Y_MM + 20.0

BATTERY_WIDTH_MM = 30.0
BATTERY_HEIGHT_MM = 20.0
BATTERY_CENTER_X_MM = BOARD_ORIGIN_X_MM + 23.0
BATTERY_CENTER_Y_MM = BOARD_ORIGIN_Y_MM + 53.0
BATTERY_CABLE_EXIT_X_MM = BATTERY_CENTER_X_MM + BATTERY_WIDTH_MM / 2.0
BATTERY_CABLE_EXIT_Y_MM = BATTERY_CENTER_Y_MM

STALE_VISIBLE_HEADER_REFS = {"J3", "J5", "J7", "J8"}
STALE_TEST_PAD_REFS = {"TP1", "TP2", "TP3", "TP4", "TP9"}
REQUIRED_NAMED_TEST_PAD_REFS = {
    "TP_SWDIO",
    "TP_SWCLK",
    "TP_NRST",
    "TP_BOOT0",
    "TP_UART_TX",
    "TP_UART_RX",
    "TP_3V3",
    "TP_GND",
}
REQUIRED_BOARD_ONLY_REFS = {"DISP1", "ANT1", "BAT1"}


@dataclass(frozen=True)
class Placement:
    ref: str
    value: str
    footprint: str
    x_mm: float
    y_mm: float
    rotation_deg: float = 0.0
    side: str = "top"
    role: str = ""


def build_placement_plan() -> list[Placement]:
    return [
        Placement(
            "DISP1",
            "ER-TFT024IPS-3",
            "Mechanical:Display_Envelope_42.72x59.46mm",
            DISPLAY_CENTER_X_MM,
            DISPLAY_CENTER_Y_MM,
            role="front portrait touch display envelope",
        ),
        Placement(
            "ANT1",
            "13.56MHz_NFC_ANTENNA_ENVELOPE",
            "nSealr_Mechanical:NFC_Antenna_Envelope_42x8mm",
            DISPLAY_CENTER_X_MM,
            TOP_NFC_ZONE_Y_MM + 3.0,
            role="top edge NFC antenna FPC or tuned keepout",
        ),
        Placement(
            "BAT1",
            "LiPo_301020_REAR_ENVELOPE",
            "nSealr_Mechanical:LiPo_301020_Rear_Envelope_30x20mm",
            BATTERY_CENTER_X_MM,
            BATTERY_CENTER_Y_MM,
            side="bottom",
            role="rear LiPo battery envelope with right-side cable path to J9",
        ),
        Placement(
            "J1",
            "USB4105-GF-A",
            "Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal",
            USB_CENTER_X_MM,
            USB_CENTER_Y_MM,
            role="bottom centered USB-C female receptacle",
        ),
        Placement(
            "SW1",
            "EVQP7J01P",
            "Button_Switch_SMD:SW_SPST_EVQP7C",
            LEFT_BUTTON_X_MM,
            SIDE_BUTTON_Y_MM,
            rotation_deg=90.0,
            role="upper left side-actuated physical button",
        ),
        Placement(
            "SW2",
            "EVQP7J01P",
            "Button_Switch_SMD:SW_SPST_EVQP7C",
            RIGHT_BUTTON_X_MM,
            SIDE_BUTTON_Y_MM,
            rotation_deg=270.0,
            role="upper right side-actuated physical button",
        ),
        Placement(
            "U1",
            "STM32U585VIT6",
            "Package_QFP:LQFP-100_14x14mm_P0.5mm",
            BOARD_ORIGIN_X_MM + 20.0,
            BOARD_ORIGIN_Y_MM + 30.0,
            side="bottom",
            role="host MCU center of secure island",
        ),
        Placement(
            "U2",
            "TR01-C2P-T301",
            "Package_DFN_QFN:QFN-32-1EP_4x4mm_P0.4mm_EP2.65x2.65mm",
            BOARD_ORIGIN_X_MM + 33.0,
            BOARD_ORIGIN_Y_MM + 30.0,
            side="bottom",
            role="TROPIC01 primary open secure element next to STM32U5",
        ),
        Placement(
            "U11",
            "OPTIGA-TRUST-M-SLS32AIA",
            "Package_SON:Microchip_USON-10-1EP_3x3mm_P0.5mm_EP1.8x2.5mm",
            BOARD_ORIGIN_X_MM + 33.0,
            BOARD_ORIGIN_Y_MM + 22.0,
            side="bottom",
            role="I2C second secure element in the secure island",
        ),
        Placement(
            "U5",
            "W25Q128JVSIQ",
            "Package_SO:SOIC-8_5.23x5.23mm_P1.27mm",
            BOARD_ORIGIN_X_MM + 6.0,
            BOARD_ORIGIN_Y_MM + 40.0,
            side="bottom",
            role="QSPI NOR close to STM32U5",
        ),
        Placement(
            "U9",
            "ST25R3916B-AQET",
            "Package_DFN_QFN:QFN-32-1EP_5x5mm_P0.5mm_EP3.45x3.45mm",
            BOARD_ORIGIN_X_MM + 31.0,
            BOARD_ORIGIN_Y_MM + 13.0,
            side="bottom",
            role="NFC controller near top matching/antenna region",
        ),
        Placement(
            "J2",
            "ER-TFT024IPS-3 50P FFC",
            "Connector_FFC-FPC:Hirose_FH12-50S-0.5SH_1x50-1MP_P0.50mm_Horizontal",
            BOARD_ORIGIN_X_MM + 22.0,
            BOARD_ORIGIN_Y_MM + 18.0,
            side="bottom",
            role="50-pin FFC behind display carrying display SPI and capacitive touch I2C",
        ),
        Placement(
            "U10",
            "BQ24074RGTR",
            "Package_DFN_QFN:VQFN-16-1EP_3.5x3.5mm_P0.5mm_EP2.1x2.1mm",
            BOARD_END_X_MM - 5.0,
            BATTERY_CABLE_EXIT_Y_MM - 6.0,
            side="bottom",
            role="LiPo charger and power-path near battery connector",
        ),
        Placement(
            "J9",
            "S2B-PH-SM4-TB",
            "Connector_JST:JST_PH_S2B-PH-SM4-TB_1x02-1MP_P2.00mm_Horizontal",
            BOARD_END_X_MM - 3.0,
            BATTERY_CABLE_EXIT_Y_MM,
            rotation_deg=270.0,
            side="bottom",
            role="right-side LiPo connector on back; cable path from BAT1 to J9 stays clear of pogo pads",
        ),
        Placement(
            "U3",
            "TPS62840DLCR",
            "Package_SON:WSON-8-1EP_2x2mm_P0.5mm_EP0.9x1.6mm",
            BOARD_ORIGIN_X_MM + 11.0,
            BOARD_END_Y_MM - 3.8,
            role="3.3 V buck in bottom electronics strip outside display glass",
        ),
        Placement(
            "L1",
            "DFE201610P-2R2M",
            "Inductor_SMD:L_Wuerth_PMFI-201610_PMCI-compatible",
            BOARD_ORIGIN_X_MM + 16.0,
            BOARD_END_Y_MM - 3.8,
            role="buck inductor in bottom electronics strip",
        ),
        Placement(
            "U4",
            "TPS22917DBVR",
            "Package_TO_SOT_SMD:SOT-23-6",
            BOARD_ORIGIN_X_MM + 37.0,
            BOARD_ORIGIN_Y_MM + 37.0,
            side="bottom",
            role="TROPIC01 load switch beside secure island",
        ),
        Placement(
            "U6",
            "TMUX1574RSVR",
            "Package_DFN_QFN:VQFN-16-1EP_3x3mm_P0.5mm_EP1.8x1.8mm",
            BOARD_ORIGIN_X_MM + 7.0,
            BOARD_ORIGIN_Y_MM + 22.0,
            side="bottom",
            role="SPI host mux / isolation near factory pad strip",
        ),
        Placement(
            "U7",
            "TPD4E05U06DQAR",
            "Package_SON:USON-10_2.5x1.0mm_P0.5mm",
            BOARD_ORIGIN_X_MM + 36.0,
            BOARD_END_Y_MM - 4.0,
            role="USB ESD array immediately behind bottom USB-C connector",
        ),
        Placement(
            "U13",
            "TPS22917DBVR",
            "Package_TO_SOT_SMD:SOT-23-6",
            BOARD_ORIGIN_X_MM + 37.0,
            BOARD_ORIGIN_Y_MM + 12.0,
            side="bottom",
            role="NFC power load switch close to NFC controller",
        ),
        Placement(
            "U15",
            "TPS61165DBVR",
            "Package_TO_SOT_SMD:SOT-23-6",
            BOARD_ORIGIN_X_MM + 5.0,
            BOARD_ORIGIN_Y_MM + 17.0,
            side="bottom",
            role="display backlight driver near display FFC",
        ),
        Placement(
            "X3",
            "FA-238 27.12MHz",
            "Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm",
            BOARD_ORIGIN_X_MM + 23.0,
            BOARD_ORIGIN_Y_MM + 12.0,
            side="bottom",
            role="NFC crystal near ST25R3916B",
        ),
        Placement("C30", "NFC_TUNE", "Capacitor_SMD:C_0402_1005Metric", BOARD_ORIGIN_X_MM + 31.0, BOARD_ORIGIN_Y_MM + 8.5, side="bottom", role="NFC tuning capacitor"),
        Placement("C31", "NFC_TUNE", "Capacitor_SMD:C_0402_1005Metric", BOARD_ORIGIN_X_MM + 37.0, BOARD_ORIGIN_Y_MM + 8.5, side="bottom", role="NFC tuning capacitor"),
        Placement("C32", "NFC_TUNE", "Capacitor_SMD:C_0402_1005Metric", BOARD_ORIGIN_X_MM + 31.0, BOARD_ORIGIN_Y_MM + 12.5, side="bottom", role="NFC tuning capacitor"),
        Placement("C33", "NFC_TUNE", "Capacitor_SMD:C_0402_1005Metric", BOARD_ORIGIN_X_MM + 37.0, BOARD_ORIGIN_Y_MM + 12.5, side="bottom", role="NFC tuning capacitor"),
        Placement("L30", "NFC_TUNE", "Inductor_SMD:L_0402_1005Metric", BOARD_ORIGIN_X_MM + 34.0, BOARD_ORIGIN_Y_MM + 10.5, side="bottom", role="NFC tuning inductor"),
        Placement("L31", "NFC_TUNE", "Inductor_SMD:L_0402_1005Metric", BOARD_ORIGIN_X_MM + 40.0, BOARD_ORIGIN_Y_MM + 10.5, side="bottom", role="NFC tuning inductor"),
        Placement("X1", "16MHz", "Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm", BOARD_ORIGIN_X_MM + 7.0, BOARD_ORIGIN_Y_MM + 29.0, side="bottom", role="MCU HSE crystal near STM32U5"),
        Placement("C16", "2.2uF", "Capacitor_SMD:C_0402_1005Metric", BOARD_ORIGIN_X_MM + 10.0, BOARD_ORIGIN_Y_MM + 35.0, side="bottom", role="STM32 local decoupling"),
        Placement("C17", "2.2uF", "Capacitor_SMD:C_0402_1005Metric", BOARD_ORIGIN_X_MM + 10.0, BOARD_ORIGIN_Y_MM + 38.0, side="bottom", role="STM32 local decoupling"),
        Placement("C3", "100nF", "Capacitor_SMD:C_0402_1005Metric", BOARD_ORIGIN_X_MM + 31.0, BOARD_ORIGIN_Y_MM + 37.0, side="bottom", role="secure island decoupling"),
        Placement("C4", "100nF", "Capacitor_SMD:C_0402_1005Metric", BOARD_ORIGIN_X_MM + 35.0, BOARD_ORIGIN_Y_MM + 35.0, side="bottom", role="secure island decoupling"),
        Placement("C5", "100nF", "Capacitor_SMD:C_0402_1005Metric", BOARD_ORIGIN_X_MM + 39.0, BOARD_ORIGIN_Y_MM + 35.0, side="bottom", role="secure island decoupling"),
        Placement("R5", "47k", "Resistor_SMD:R_0402_1005Metric", BOARD_ORIGIN_X_MM + 36.0, BOARD_ORIGIN_Y_MM + 40.0, side="bottom", role="TROPIC/load-switch pull resistor"),
        Placement("R6", "4.7k", "Resistor_SMD:R_0402_1005Metric", BOARD_ORIGIN_X_MM + 40.0, BOARD_ORIGIN_Y_MM + 25.0, side="bottom", role="I2C pull-up"),
        Placement("R7", "4.7k", "Resistor_SMD:R_0402_1005Metric", BOARD_ORIGIN_X_MM + 43.0, BOARD_ORIGIN_Y_MM + 25.0, side="bottom", role="I2C pull-up"),
        Placement("R20", "1M", "Resistor_SMD:R_0402_1005Metric", BOARD_END_X_MM - 4.0, BOARD_END_Y_MM - 8.0, side="bottom", role="battery sense divider high side near J9"),
        Placement("R21", "330k", "Resistor_SMD:R_0402_1005Metric", BOARD_END_X_MM - 4.0, BOARD_END_Y_MM - 5.0, side="bottom", role="battery sense divider low side near J9"),
        Placement(
            "U8",
            "TPS2553DBVR",
            "Package_TO_SOT_SMD:SOT-23-6",
            BOARD_ORIGIN_X_MM + 6.0,
            BOARD_END_Y_MM - 2.5,
            side="bottom",
            role="USB VBUS current-limit switch close to bottom USB-C input",
        ),
        Placement(
            "J6",
            "SM04B-SRSS-TB",
            "Connector_JST:JST_SH_SM04B-SRSS-TB_1x04-1MP_P1.00mm_Horizontal",
            BOARD_ORIGIN_X_MM + 4.0,
            BOARD_END_Y_MM - 12.0,
            side="bottom",
            role="compact Qwiic/STEMMA QT I2C expansion on lower left edge",
        ),
        Placement(
            "LED1",
            "APFA3010LSEEZGKQBKC",
            "LED_SMD:LED_RGB_5050-6",
            BOARD_ORIGIN_X_MM + 8.0,
            BOARD_END_Y_MM - 4.5,
            role="front visible RGB status LED above bottom edge",
        ),
        Placement(
            "R1",
            "5.1k",
            "Resistor_SMD:R_0402_1005Metric",
            BOARD_ORIGIN_X_MM + 19.0,
            BOARD_END_Y_MM - 4.0,
            role="USB-C CC1 Rd resistor near connector",
        ),
        Placement(
            "R2",
            "5.1k",
            "Resistor_SMD:R_0402_1005Metric",
            BOARD_ORIGIN_X_MM + 22.0,
            BOARD_END_Y_MM - 4.0,
            role="USB-C CC2 Rd resistor near connector",
        ),
        Placement(
            "R3",
            "22R",
            "Resistor_SMD:R_0402_1005Metric",
            BOARD_ORIGIN_X_MM + 28.0,
            BOARD_END_Y_MM - 4.0,
            role="USB D+ series resistor near connector",
        ),
        Placement(
            "R4",
            "22R",
            "Resistor_SMD:R_0402_1005Metric",
            BOARD_ORIGIN_X_MM + 30.0,
            BOARD_END_Y_MM - 4.0,
            role="USB D- series resistor near connector",
        ),
        Placement(
            "C1",
            "10uF",
            "Capacitor_SMD:C_0603_1608Metric",
            BOARD_ORIGIN_X_MM + 17.0,
            BOARD_END_Y_MM - 3.0,
            role="USB VBUS local bulk capacitor inside bottom edge",
        ),
        Placement(
            "TP_SWDIO",
            "SWDIO",
            "TestPoint:TestPoint_Pad_D1.0mm",
            BOARD_ORIGIN_X_MM + 5.0,
            BOARD_ORIGIN_Y_MM + 5.0,
            side="bottom",
            role="hidden back-side pogo test pad",
        ),
        Placement(
            "TP_SWCLK",
            "SWCLK",
            "TestPoint:TestPoint_Pad_D1.0mm",
            BOARD_ORIGIN_X_MM + 8.0,
            BOARD_ORIGIN_Y_MM + 5.0,
            side="bottom",
            role="hidden back-side pogo test pad",
        ),
        Placement(
            "TP_NRST",
            "NRST",
            "TestPoint:TestPoint_Pad_D1.0mm",
            BOARD_ORIGIN_X_MM + 11.0,
            BOARD_ORIGIN_Y_MM + 5.0,
            side="bottom",
            role="hidden back-side pogo test pad",
        ),
        Placement(
            "TP_BOOT0",
            "BOOT0",
            "TestPoint:TestPoint_Pad_D1.0mm",
            BOARD_ORIGIN_X_MM + 14.0,
            BOARD_ORIGIN_Y_MM + 5.0,
            side="bottom",
            role="hidden back-side pogo test pad",
        ),
        Placement(
            "TP_UART_TX",
            "UART_TX",
            "TestPoint:TestPoint_Pad_D1.0mm",
            BOARD_ORIGIN_X_MM + 5.0,
            BOARD_ORIGIN_Y_MM + 8.0,
            side="bottom",
            role="hidden back-side pogo test pad",
        ),
        Placement(
            "TP_UART_RX",
            "UART_RX",
            "TestPoint:TestPoint_Pad_D1.0mm",
            BOARD_ORIGIN_X_MM + 8.0,
            BOARD_ORIGIN_Y_MM + 8.0,
            side="bottom",
            role="hidden back-side pogo test pad",
        ),
        Placement(
            "TP_3V3",
            "3V3",
            "TestPoint:TestPoint_Pad_D1.0mm",
            BOARD_ORIGIN_X_MM + 11.0,
            BOARD_ORIGIN_Y_MM + 8.0,
            side="bottom",
            role="hidden back-side pogo test pad",
        ),
        Placement(
            "TP_GND",
            "GND",
            "TestPoint:TestPoint_Pad_D1.0mm",
            BOARD_ORIGIN_X_MM + 14.0,
            BOARD_ORIGIN_Y_MM + 8.0,
            side="bottom",
            role="hidden back-side pogo test pad",
        ),
    ]


def placement_by_ref() -> dict[str, Placement]:
    return {placement.ref: placement for placement in build_placement_plan()}


def render_portrait_drawings() -> list[str]:
    display_left = DISPLAY_CENTER_X_MM - DISPLAY_WIDTH_MM / 2.0
    display_top = DISPLAY_CENTER_Y_MM - DISPLAY_HEIGHT_MM / 2.0
    return [
        f"BOARD OUTLINE {BOARD_WIDTH_MM:.1f} x {BOARD_HEIGHT_MM:.1f} mm",
        f"DISPLAY CENTER {DISPLAY_CENTER_X_MM:.2f},{DISPLAY_CENTER_Y_MM:.2f} mm",
        f"DISPLAY START {display_left:.2f},{display_top:.2f} mm",
        "DISP1 PORTRAIT TOUCH DISPLAY ENVELOPE 42.72 x 59.46 mm",
        "ANT1 TOP EDGE NFC ANTENNA FPC OR TUNED KEEP-OUT",
        "BAT1 REAR LIPO ENVELOPE 30.0 x 20.0 mm WITH RIGHT-SIDE CABLE EXIT TO J9",
        "J1 USB-C FEMALE RECEPTACLE CENTERED ON BOTTOM EDGE",
        "SW1/SW2 HIGH SIDE-ACTUATED BUTTONS ON LONG EDGES",
        "U1/U2/U11 BACK-SIDE SECURE ISLAND",
        "HIDDEN BACK-SIDE POGO TEST PADS COVERED BY ENCLOSURE",
    ]


def write_placement_json(path: Path = PLACEMENT_JSON) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "board": BOARD_NAME,
        "board_width_mm": BOARD_WIDTH_MM,
        "board_height_mm": BOARD_HEIGHT_MM,
        "drawings": render_portrait_drawings(),
        "placements": [asdict(placement) for placement in build_placement_plan()],
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def apply_placement_to_board_text(text: str) -> str:
    text = remove_footprints_by_ref(text, STALE_VISIBLE_HEADER_REFS | STALE_TEST_PAD_REFS)
    text = ensure_required_board_footprints(text)
    text = re.sub(
        r'\(gr_rect\s+\(start 10\.000 10\.000\)\s+\(end [0-9.]+ [0-9.]+\)',
        '(gr_rect\n\t\t(start 10.000 10.000)\n\t\t(end 58.000 78.000)',
        text,
        count=1,
    )
    text = text.replace('(end 57.400 81.910)', '(end 55.400 71.955)')
    text = text.replace('(start 14.600 22.000)', '(start 12.600 12.045)')
    text = text.replace('(at 27.000 90.000 0)', '(at 20.000 76.500 0)')
    for placement in build_placement_plan():
        text = _apply_single_footprint_placement(text, placement)
    return text


def apply_placement_to_board(path: Path = KICAD_BOARD) -> None:
    path.write_text(apply_placement_to_board_text(path.read_text(encoding="utf-8")), encoding="utf-8")


def remove_footprints_by_ref(text: str, refs: set[str]) -> str:
    footprint_re = re.compile(r'\n\t\(footprint "[^"]+"[\s\S]*?(?=\n\t\(footprint |\n\))')

    def patch(match: re.Match[str]) -> str:
        block = match.group(0)
        reference_match = re.search(r'\(property "Reference" "([^"]+)"', block)
        if reference_match and reference_match.group(1) in refs:
            return ""
        return block

    return footprint_re.sub(patch, text)


def ensure_required_board_footprints(text: str) -> str:
    existing_refs = set(re.findall(r'\(property "Reference" "([^"]+)"', text))
    insert_blocks = []
    for placement in build_placement_plan():
        if placement.ref in existing_refs:
            continue
        if placement.ref in REQUIRED_NAMED_TEST_PAD_REFS:
            insert_blocks.append(_test_pad_footprint_block(placement))
        elif placement.ref in REQUIRED_BOARD_ONLY_REFS:
            insert_blocks.append(_board_only_footprint_block(placement))

    if not insert_blocks:
        return text
    insert_at = text.rfind("\n)")
    if insert_at == -1:
        raise ValueError("KiCad board has no top-level closing parenthesis")
    return text[:insert_at] + "\n".join(insert_blocks) + text[insert_at:]


def _apply_single_footprint_placement(text: str, placement: Placement) -> str:
    footprint_re = re.compile(r'\n\t\(footprint "[^"]+"[\s\S]*?(?=\n\t\(footprint |\n\))')

    def patch(match: re.Match[str]) -> str:
        block = match.group(0)
        if f'(property "Reference" "{placement.ref}"' not in block:
            return block
        block = re.sub(
            r'^\n\t\(footprint "[^"]+"',
            f'\n\t(footprint "{placement.footprint}"',
            block,
            count=1,
        )
        block = re.sub(
            r'\n\t\t\(at [-0-9.]+ [-0-9.]+ [-0-9.]+\)',
            f'\n\t\t(at {placement.x_mm:.3f} {placement.y_mm:.3f} {placement.rotation_deg:.3f})',
            block,
            count=1,
        )
        block = re.sub(
            r'\(property "Value" "[^"]+"',
            f'(property "Value" "{placement.value}"',
            block,
            count=1,
        )
        if placement.footprint.endswith("SW_SPST_EVQP7C"):
            block = block.replace("SW_SPST_EVQP7A.step", "SW_SPST_EVQP7C.step")
            block = block.replace("Top-actuated Model", "Side-actuated Model")
        block = _set_footprint_side(block, placement.side)
        return block

    return footprint_re.sub(patch, text)


def _stable_uuid(ref: str, suffix: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"{BOARD_NAME}:{ref}:{suffix}"))


def _property_block(ref: str, value: str) -> str:
    return f"""
\t\t(property "Reference" "{ref}"
\t\t\t(at 0 -1.5 0)
\t\t\t(layer "F.SilkS")
\t\t\t(uuid "{_stable_uuid(ref, "ref")}")
\t\t\t(effects (font (size 0.8 0.8) (thickness 0.12)))
\t\t)
\t\t(property "Value" "{value}"
\t\t\t(at 0 1.5 0)
\t\t\t(layer "F.Fab")
\t\t\t(uuid "{_stable_uuid(ref, "value")}")
\t\t\t(effects (font (size 0.8 0.8) (thickness 0.12)))
\t\t)""".rstrip()


def _test_pad_footprint_block(placement: Placement) -> str:
    return f"""
\t(footprint "{placement.footprint}"
\t\t(version 20260206)
\t\t(generator "nsealr-placement")
\t\t(layer "B.Cu")
\t\t(at {placement.x_mm:.3f} {placement.y_mm:.3f} {placement.rotation_deg:.3f})
\t\t(descr "Hidden back-side pogo/test pad")
\t\t(property "Reference" "{placement.ref}"
\t\t\t(at 0 -1.35 0)
\t\t\t(layer "B.SilkS")
\t\t\t(uuid "{_stable_uuid(placement.ref, "ref")}")
\t\t\t(effects (font (size 0.55 0.55) (thickness 0.08)) (justify mirror))
\t\t)
\t\t(property "Value" "{placement.value}"
\t\t\t(at 0 1.35 0)
\t\t\t(layer "B.Fab")
\t\t\t(uuid "{_stable_uuid(placement.ref, "value")}")
\t\t\t(effects (font (size 0.55 0.55) (thickness 0.08)) (justify mirror))
\t\t)
\t\t(attr smd exclude_from_pos_files exclude_from_bom)
\t\t(fp_circle (center 0 0) (end 0.6 0) (stroke (width 0.05) (type solid)) (fill no) (layer "B.CrtYd") (uuid "{_stable_uuid(placement.ref, "courtyard")}"))
\t\t(pad "1" smd circle
\t\t\t(at 0 0)
\t\t\t(size 1.0 1.0)
\t\t\t(layers "B.Cu" "B.Mask")
\t\t\t(uuid "{_stable_uuid(placement.ref, "pad1")}")
\t\t)
\t)
""".rstrip()


def _board_only_footprint_block(placement: Placement) -> str:
    if placement.ref == "DISP1":
        return _rect_envelope_footprint(
            placement,
            width=DISPLAY_WIDTH_MM,
            height=DISPLAY_HEIGHT_MM,
            layer="F",
            description="Front portrait capacitive touch display envelope",
            model="${KIPRJMOD}/models/nsealr_display_2p4.wrl",
        )
    if placement.ref == "ANT1":
        return _rect_envelope_footprint(
            placement,
            width=42.0,
            height=8.0,
            layer="F",
            description="Top-edge 13.56 MHz NFC antenna keepout/envelope",
            model="${KIPRJMOD}/models/nsealr_nfc_antenna.wrl",
        )
    if placement.ref == "BAT1":
        return _rect_envelope_footprint(
            placement,
            width=BATTERY_WIDTH_MM,
            height=BATTERY_HEIGHT_MM,
            layer="B",
            description="Rear LiPo battery mechanical envelope with cable exit to J9",
            model="${KIPRJMOD}/models/nsealr_lipo_301020.wrl",
            cable_to_j9=True,
        )
    raise ValueError(f"unsupported board-only footprint: {placement.ref}")


def _rect_envelope_footprint(
    placement: Placement,
    *,
    width: float,
    height: float,
    layer: str,
    description: str,
    model: str,
    cable_to_j9: bool = False,
) -> str:
    half_w = width / 2.0
    half_h = height / 2.0
    silk = f"{layer}.SilkS"
    fab = f"{layer}.Fab"
    user = "Dwgs.User"
    cable = ""
    if cable_to_j9:
        cable_dx = (BOARD_END_X_MM - 3.0) - (placement.x_mm + half_w)
        cable = f"""
\t\t(fp_line (start {half_w:.3f} 0) (end {half_w + cable_dx:.3f} 0) (stroke (width 0.35) (type solid)) (layer "{user}") (uuid "{_stable_uuid(placement.ref, "cable")}"))
\t\t(fp_text user "CABLE EXIT TO J9" (at {half_w + cable_dx / 2.0:.3f} -1.2 0) (layer "{user}") (uuid "{_stable_uuid(placement.ref, "cable-text")}") (effects (font (size 0.7 0.7) (thickness 0.1))))"""

    return f"""
\t(footprint "{placement.footprint}"
\t\t(version 20260206)
\t\t(generator "nsealr-placement")
\t\t(layer "{layer}.Cu")
\t\t(at {placement.x_mm:.3f} {placement.y_mm:.3f} {placement.rotation_deg:.3f})
\t\t(descr "{description}")
{_property_block(placement.ref, placement.value)}
\t\t(attr board_only exclude_from_pos_files exclude_from_bom)
\t\t(fp_rect (start {-half_w:.3f} {-half_h:.3f}) (end {half_w:.3f} {half_h:.3f}) (stroke (width 0.12) (type solid)) (fill no) (layer "{silk}") (uuid "{_stable_uuid(placement.ref, "silk")}"))
\t\t(fp_rect (start {-half_w:.3f} {-half_h:.3f}) (end {half_w:.3f} {half_h:.3f}) (stroke (width 0.10) (type dash)) (fill no) (layer "{fab}") (uuid "{_stable_uuid(placement.ref, "fab")}"))
\t\t(fp_text user "{description}" (at 0 0 0) (layer "{user}") (uuid "{_stable_uuid(placement.ref, "user-text")}") (effects (font (size 0.8 0.8) (thickness 0.1))))
{cable}
\t\t(model "{model}"
\t\t\t(offset (xyz 0 0 0))
\t\t\t(scale (xyz 1 1 1))
\t\t\t(rotate (xyz 0 0 0))
\t\t)
\t)
""".rstrip()


def _set_footprint_side(block: str, side: str) -> str:
    layer_prefixes = ("Cu", "Paste", "Mask", "SilkS", "Fab", "CrtYd")
    if side == "bottom":
        for suffix in layer_prefixes:
            block = block.replace(f'"F.{suffix}"', f'"B.{suffix}"')
    elif side == "top":
        for suffix in layer_prefixes:
            block = block.replace(f'"B.{suffix}"', f'"F.{suffix}"')
    else:
        raise ValueError(f"unsupported footprint side: {side}")
    return block


def main() -> int:
    parser = argparse.ArgumentParser(description="Materialize TROPIC01 universal placement preflight files.")
    parser.add_argument(
        "--apply-board",
        action="store_true",
        help="Update the KiCad PCB scaffold outline and key footprint coordinates from the placement contract.",
    )
    args = parser.parse_args()

    write_placement_json()
    if args.apply_board:
        apply_placement_to_board()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
