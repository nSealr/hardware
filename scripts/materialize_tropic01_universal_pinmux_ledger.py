#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOARD_NAME = "tropic01-universal-secure-device"
PINMUX_LEDGER_JSON = ROOT / "pcb" / BOARD_NAME / "production" / "pinmux-ledger.json"


def build_pinmux_ledger() -> dict[str, object]:
    return {
        "board": BOARD_NAME,
        "schema_version": 1,
        "status": "partial_evidence_no_mcu_pinmux",
        "sources": {
            "tropic01": {
                "title": "TROPIC01 datasheet ODD_TR01_datasheet_vA_11",
                "url": "https://github.com/tropicsquare/tropic01/blob/main/doc/datasheet/ODD_TR01_datasheet_vA_11.pdf",
                "evidence": "Table 1 TROPIC01 pinout and L1 Layer SPI description",
            },
            "display": {
                "title": "Newhaven NHD-2.4-240320AF-CSXP-CTP datasheet",
                "url": "https://newhavendisplay.com/content/specs/NHD-2.4-240320AF-CSXP-CTP.pdf",
                "evidence": "Pin Description and Interface Selection sections",
            },
            "stm32u5": {
                "title": "STM32U585VI official ST datasheet",
                "url": "https://www.st.com/resource/en/datasheet/stm32u585vi.pdf",
                "evidence": "pending manual alternate-function and package pin review",
            },
            "st25r3916b": {
                "title": "ST25R3916B official ST datasheet",
                "url": "https://www.st.com/resource/en/datasheet/st25r3916b.pdf",
                "evidence": "pending NFC controller pin and antenna matching review",
            },
        },
        "tropic01": {
            "status": "datasheet_pinout_confirmed",
            "pins": {
                "1": "VCC",
                "2": "GND",
                "4": "GPO",
                "5": "SPI_SDI",
                "6": "SPI_SDO",
                "7": "SPI_SCK",
                "8": "SPI_CSN",
                "11": "VCC",
                "12": "GND",
                "23": "GND",
                "24": "VCC",
            },
            "nu_policy": "NU pins must follow the datasheet section 11 connection guidance before routing.",
            "spi_mode": "CPOL=0 CPHA=0 MSB-first",
            "host_policy": "TROPIC01 does not initiate communication; host MCU must wait for readiness or use GPO when configured.",
        },
        "display": {
            "status": "connector_pinout_confirmed_mcu_pinmux_pending",
            "module": "NHD-2.4-240320AF-CSXP-CTP",
            "tft_connector": "Molex 54132-4062",
            "touch_connector": "Molex 52271-0679",
            "driver_ics": ["ST7789VI", "FT5426-003"],
            "tft_4wire_spi_mode_select": {"IM0": "0", "IM1": "1", "IM2": "1"},
            "tft_spi_signals": {
                "SDA": "serial data input",
                "SCL_WRX": "serial clock in 3/4-wire SPI",
                "DCX": "data/command in 4-wire SPI",
                "CSX": "active-low chip select",
                "RESX": "active-low reset",
                "SDO": "serial data output",
            },
            "touch_i2c_signals": ["SCL", "SDA", "/INT", "/RESET"],
            "touch_i2c_pullups": "4.7k",
            "backlight": "LED-A anode 3.0 V / 160 mA max class; LED-K1..K4 cathodes to current driver return",
        },
        "stm32u5": {
            "status": "datasheet_pinmux_review_required",
            "part": "STM32U585VIT6",
            "package": "LQFP100",
            "assignments": {},
            "constraint": "No STM32 GPIO or alternate-function assignment is accepted until checked against official ST documentation/CubeMX.",
        },
        "st25r3916b": {
            "status": "datasheet_rf_review_required",
            "part": "ST25R3916B-AQET",
            "constraint": "No antenna matching component value or MCU pin assignment is accepted until checked against official ST datasheet and final antenna measurement.",
        },
        "release_gates": [
            "no_llm_invented_pin_numbers",
            "stm32_cube_or_datasheet_pinmux_review",
            "st25r3916b_pin_and_matching_review",
            "kicad_schematic_nets_match_this_ledger",
            "erc_clean_before_pcb_update",
        ],
    }


def write_pinmux_ledger(path: Path = PINMUX_LEDGER_JSON) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_pinmux_ledger(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    write_pinmux_ledger()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
