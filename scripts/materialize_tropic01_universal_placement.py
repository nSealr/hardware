#!/usr/bin/env python3
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOARD_NAME = "tropic01-universal-secure-device"
PLACEMENT_JSON = ROOT / "pcb" / BOARD_NAME / "production" / "placement-plan.json"

BOARD_ORIGIN_X_MM = 10.0
BOARD_ORIGIN_Y_MM = 10.0
BOARD_WIDTH_MM = 48.0
BOARD_HEIGHT_MM = 68.0
BOARD_END_X_MM = BOARD_ORIGIN_X_MM + BOARD_WIDTH_MM
BOARD_END_Y_MM = BOARD_ORIGIN_Y_MM + BOARD_HEIGHT_MM

DISPLAY_WIDTH_MM = 42.8
DISPLAY_HEIGHT_MM = 59.91
DISPLAY_CENTER_X_MM = BOARD_ORIGIN_X_MM + BOARD_WIDTH_MM / 2.0
DISPLAY_CENTER_Y_MM = BOARD_ORIGIN_Y_MM + 32.0

USB_CENTER_X_MM = BOARD_ORIGIN_X_MM + BOARD_WIDTH_MM / 2.0
USB_CENTER_Y_MM = BOARD_END_Y_MM - 2.4
TOP_NFC_ZONE_Y_MM = BOARD_ORIGIN_Y_MM + 4.0
LEFT_BUTTON_X_MM = BOARD_ORIGIN_X_MM + 0.9
RIGHT_BUTTON_X_MM = BOARD_END_X_MM - 0.9
SIDE_BUTTON_Y_MM = BOARD_ORIGIN_Y_MM + 20.0


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
            "NHD-2.4-240320AF-CSXP-CTP",
            "Mechanical:Display_Envelope_42.8x59.91mm",
            DISPLAY_CENTER_X_MM,
            DISPLAY_CENTER_Y_MM,
            role="front portrait touch display envelope",
        ),
        Placement(
            "ANT1",
            "ANT-FPC-TUNED",
            "Connector_Generic:Conn_01x02",
            DISPLAY_CENTER_X_MM,
            TOP_NFC_ZONE_Y_MM + 3.0,
            role="top edge NFC antenna FPC or tuned keepout",
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
            "Button_Switch_SMD:SW_SPST_EVQP7A",
            LEFT_BUTTON_X_MM,
            SIDE_BUTTON_Y_MM,
            rotation_deg=90.0,
            role="upper left side-actuated physical button",
        ),
        Placement(
            "SW2",
            "EVQP7J01P",
            "Button_Switch_SMD:SW_SPST_EVQP7A",
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
            BOARD_ORIGIN_Y_MM + 36.0,
            side="bottom",
            role="host MCU center of secure island",
        ),
        Placement(
            "U2",
            "TR01-C2P-T301",
            "Package_DFN_QFN:QFN-32-1EP_4x4mm_P0.4mm_EP2.65x2.65mm",
            BOARD_ORIGIN_X_MM + 33.0,
            BOARD_ORIGIN_Y_MM + 36.0,
            side="bottom",
            role="TROPIC01 primary open secure element next to STM32U5",
        ),
        Placement(
            "U11",
            "OPTIGA-TRUST-M-SLS32AIA",
            "Package_SON:Microchip_USON-10-1EP_3x3mm_P0.5mm_EP1.8x2.5mm",
            BOARD_ORIGIN_X_MM + 33.0,
            BOARD_ORIGIN_Y_MM + 28.0,
            side="bottom",
            role="I2C second secure element in the secure island",
        ),
        Placement(
            "U5",
            "W25Q128JVSIQ",
            "Package_SO:SOIC-8_5.23x5.23mm_P1.27mm",
            BOARD_ORIGIN_X_MM + 18.0,
            BOARD_ORIGIN_Y_MM + 48.0,
            side="bottom",
            role="QSPI NOR close to STM32U5",
        ),
        Placement(
            "U9",
            "ST25R3916B-AQET",
            "Package_DFN_QFN:QFN-32-1EP_5x5mm_P0.5mm_EP3.45x3.45mm",
            BOARD_ORIGIN_X_MM + 24.0,
            BOARD_ORIGIN_Y_MM + 13.0,
            side="bottom",
            role="NFC controller near top matching/antenna region",
        ),
        Placement(
            "J2",
            "54132-4062",
            "Connector_FFC-FPC:Molex_54132-4062_1x40-1MP_P0.50mm_Horizontal",
            BOARD_ORIGIN_X_MM + 24.0,
            BOARD_ORIGIN_Y_MM + 23.5,
            side="bottom",
            role="40-pin TFT FFC behind display",
        ),
        Placement(
            "J2B",
            "52271-0679",
            "Connector_FFC-FPC:Molex_52271-0679_1x06-1MP_P1.00mm_Horizontal",
            BOARD_ORIGIN_X_MM + 39.0,
            BOARD_ORIGIN_Y_MM + 23.5,
            side="bottom",
            role="6-pin capacitive touch FFC behind display",
        ),
        Placement(
            "U10",
            "BQ24074RGTR",
            "Package_DFN_QFN:VQFN-16-1EP_3.5x3.5mm_P0.5mm_EP2.1x2.1mm",
            BOARD_ORIGIN_X_MM + 25.0,
            BOARD_END_Y_MM - 9.0,
            side="bottom",
            role="LiPo charger and power-path near battery connector",
        ),
        Placement(
            "J9",
            "S2B-PH-SM4-TB",
            "Connector_JST:JST_PH_S2B-PH-SM4-TB_1x02-1MP_P2.00mm_Horizontal",
            BOARD_ORIGIN_X_MM + 39.0,
            BOARD_END_Y_MM - 9.0,
            side="bottom",
            role="LiPo connector on back lower edge",
        ),
        Placement(
            "TP_SWDIO",
            "SWDIO",
            "TestPoint:TestPoint_Pad_D1.0mm",
            BOARD_ORIGIN_X_MM + 13.0,
            BOARD_END_Y_MM - 4.0,
            side="bottom",
            role="hidden back-side pogo test pad",
        ),
        Placement(
            "TP_SWCLK",
            "SWCLK",
            "TestPoint:TestPoint_Pad_D1.0mm",
            BOARD_ORIGIN_X_MM + 16.0,
            BOARD_END_Y_MM - 4.0,
            side="bottom",
            role="hidden back-side pogo test pad",
        ),
        Placement(
            "TP_NRST",
            "NRST",
            "TestPoint:TestPoint_Pad_D1.0mm",
            BOARD_ORIGIN_X_MM + 19.0,
            BOARD_END_Y_MM - 4.0,
            side="bottom",
            role="hidden back-side pogo test pad",
        ),
        Placement(
            "TP_BOOT0",
            "BOOT0",
            "TestPoint:TestPoint_Pad_D1.0mm",
            BOARD_ORIGIN_X_MM + 22.0,
            BOARD_END_Y_MM - 4.0,
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
        "DISP1 PORTRAIT TOUCH DISPLAY ENVELOPE 42.8 x 59.91 mm",
        "ANT1 TOP EDGE NFC ANTENNA FPC OR TUNED KEEP-OUT",
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


def main() -> int:
    write_placement_json()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
