#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOARD_NAME = "tropic01-universal-secure-device"
NETLIST_CONTRACT_JSON = ROOT / "pcb" / BOARD_NAME / "production" / "netlist-contract.json"


def build_netlist_contract() -> dict[str, object]:
    return {
        "board": BOARD_NAME,
        "schema_version": 1,
        "status": "pinmux_review_required",
        "scope": "Rev A0 electrical intent before schematic-driven routing",
        "required_buses": {
            "power": [
                "VBUS",
                "VBAT",
                "SYS_3V3",
                "TROPIC_VCC_SW",
                "NFC_VCC_SW",
                "DISPLAY_VCC_SW",
                "GND",
            ],
            "usb2_device": [
                "USB_DP",
                "USB_DM",
                "USB_CC1_RD",
                "USB_CC2_RD",
                "USB_VBUS_SENSE",
            ],
            "tropic01_spi": [
                "TROPIC_SPI_SCK",
                "TROPIC_SPI_MOSI",
                "TROPIC_SPI_MISO",
                "TROPIC_SPI_CSN",
                "TROPIC_GPO",
                "TROPIC_PWR_EN",
            ],
            "display_tft_spi": [
                "TFT_SPI_SCK",
                "TFT_SPI_MOSI",
                "TFT_CS",
                "TFT_DC",
                "TFT_RST",
                "TFT_BACKLIGHT_PWM",
                "TFT_PWR_EN",
            ],
            "display_touch_i2c": [
                "TOUCH_I2C_SCL",
                "TOUCH_I2C_SDA",
                "TOUCH_INT",
                "TOUCH_RST",
            ],
            "qspi_nor": [
                "QSPI_CLK",
                "QSPI_NCS",
                "QSPI_IO0",
                "QSPI_IO1",
                "QSPI_IO2",
                "QSPI_IO3",
            ],
            "nfc_spi": [
                "NFC_SPI_SCK",
                "NFC_SPI_MOSI",
                "NFC_SPI_MISO",
                "NFC_SPI_CSN",
                "NFC_IRQ",
                "NFC_PWR_EN",
                "NFC_ANT1",
                "NFC_ANT2",
            ],
            "second_secure_element_i2c": [
                "SE2_I2C_SCL",
                "SE2_I2C_SDA",
                "SE2_RST",
            ],
            "side_buttons": [
                "BTN_LEFT",
                "BTN_RIGHT",
            ],
            "expansion": [
                "EXP_I2C_SCL",
                "EXP_I2C_SDA",
                "EXP_UART_TX",
                "EXP_UART_RX",
                "EXP_SPI_SCK",
                "EXP_SPI_MOSI",
                "EXP_SPI_MISO",
                "EXP_SPI_CSN",
            ],
            "manufacturing_test": [
                "TP_VBUS",
                "TP_3V3",
                "TP_GND",
                "TP_USB_DP",
                "TP_USB_DM",
                "TP_SWDIO",
                "TP_SWCLK",
                "TP_NRST",
                "TP_BOOT0",
            ],
        },
        "release_gates": [
            "manual_datasheet_pinmux_review",
            "no_llm_invented_pin_numbers",
            "schematic_symbols_have_verified_pin_numbers",
            "kicad_erc_pass",
            "kicad_drc_pass",
            "usb_differential_pair_length_and_impedance_review",
            "nfc_matching_network_measured_with_final_antenna",
            "pcbway_export_unblocked_only_after_routing",
        ],
        "notes": [
            "This file is an electrical-intent contract, not a routed netlist.",
            "MCU alternate-function pin numbers must be selected from official STM32U585VIT6 documentation before routing.",
            "TROPIC01 SPI pin names are fixed at the TROPIC01 symbol boundary; host MCU pins remain gated by pinmux review.",
            "The production exporter must stay blocked while the KiCad board has only net 0 or zero routed copper.",
        ],
    }


def write_netlist_contract(path: Path = NETLIST_CONTRACT_JSON) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_netlist_contract(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    write_netlist_contract()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
