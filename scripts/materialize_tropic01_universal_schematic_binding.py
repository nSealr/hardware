#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOARD_NAME = "tropic01-universal-secure-device"
PRODUCTION_DIR = ROOT / "pcb" / BOARD_NAME / "production"
PINMUX_LEDGER_JSON = PRODUCTION_DIR / "pinmux-ledger.json"
NETLIST_CONTRACT_JSON = PRODUCTION_DIR / "netlist-contract.json"
SCHEMATIC_BINDING_JSON = PRODUCTION_DIR / "schematic-binding.json"


def binding(
    *,
    net: str,
    pin_name: str,
    source: str,
    review_status: str,
    evidence: str,
    physical_pin: int | None = None,
) -> dict[str, object]:
    value: dict[str, object] = {
        "net": net,
        "pin_name": pin_name,
        "source": source,
        "review_status": review_status,
        "evidence": evidence,
    }
    if physical_pin is not None:
        value["physical_pin"] = physical_pin
    return value


def build_u1_bindings(pinmux: dict[str, object]) -> dict[str, object]:
    assignments = pinmux["stm32u5"]["assignments"]
    return {
        net_name: {
            "net": net_name,
            "pin_name": assignment["pin_name"],
            "physical_pin": assignment["physical_pin"],
            "function": assignment["function"],
            "source": assignment["source"],
            "source_table": assignment["source_table"],
            "review_status": "source_backed",
            "evidence": assignment["evidence"],
        }
        for net_name, assignment in sorted(assignments.items())
    }


def component(role: str, sheet: str, pins: dict[str, dict[str, object]], *, symbol: str = "") -> dict[str, object]:
    value: dict[str, object] = {
        "role": role,
        "sheet": sheet,
        "pins": pins,
    }
    if symbol:
        value["symbol"] = symbol
    return value


def test_point(ref: str, net: str, role: str) -> dict[str, object]:
    return component(
        role,
        "kicad/sheets/optional_profiles.kicad_sch",
        {
            "1": binding(
                net=net,
                pin_name="1",
                physical_pin=1,
                source="Hidden pogo/test pad placement review",
                review_status="source_backed",
                evidence=f"{ref} exposes the {net} net only on the covered back-side pogo fixture area.",
            )
        },
        symbol="Connector:TestPoint",
    )


def build_components(pinmux: dict[str, object]) -> dict[str, object]:
    return {
        "U1": component(
            "host_mcu",
            "kicad/sheets/stm32u5_host.kicad_sch",
            build_u1_bindings(pinmux),
            symbol="MCU_ST_STM32U5:STM32U585VITx",
        ),
        "U2": component(
            "tropic01_secure_element",
            "kicad/sheets/tropic01.kicad_sch",
            {
                "1": binding(
                    net="TROPIC_VCC_SW",
                    pin_name="VCC",
                    physical_pin=1,
                    source="TROPIC01 datasheet ODD_TR01_datasheet_vA_11",
                    review_status="source_backed",
                    evidence="TROPIC01 pin 1 is VCC.",
                ),
                "2": binding(
                    net="GND",
                    pin_name="GND",
                    physical_pin=2,
                    source="TROPIC01 datasheet ODD_TR01_datasheet_vA_11",
                    review_status="source_backed",
                    evidence="TROPIC01 pin 2 is GND.",
                ),
                "4": binding(
                    net="TROPIC_GPO",
                    pin_name="GPO",
                    physical_pin=4,
                    source="TROPIC01 datasheet ODD_TR01_datasheet_vA_11",
                    review_status="source_backed_noncritical",
                    evidence="TROPIC01 pin 4 is GPO; firmware must not depend on it without polling fallback.",
                ),
                "5": binding(
                    net="TROPIC_SPI_MOSI",
                    pin_name="SPI_SDI",
                    physical_pin=5,
                    source="TROPIC01 datasheet ODD_TR01_datasheet_vA_11",
                    review_status="source_backed",
                    evidence="Host MOSI connects to TROPIC01 SPI_SDI.",
                ),
                "6": binding(
                    net="TROPIC_SPI_MISO",
                    pin_name="SPI_SDO",
                    physical_pin=6,
                    source="TROPIC01 datasheet ODD_TR01_datasheet_vA_11",
                    review_status="source_backed",
                    evidence="Host MISO connects to TROPIC01 SPI_SDO.",
                ),
                "7": binding(
                    net="TROPIC_SPI_SCK",
                    pin_name="SPI_SCK",
                    physical_pin=7,
                    source="TROPIC01 datasheet ODD_TR01_datasheet_vA_11",
                    review_status="source_backed",
                    evidence="TROPIC01 pin 7 is SPI_SCK.",
                ),
                "8": binding(
                    net="TROPIC_SPI_CSN",
                    pin_name="SPI_CSN",
                    physical_pin=8,
                    source="TROPIC01 datasheet ODD_TR01_datasheet_vA_11",
                    review_status="source_backed",
                    evidence="TROPIC01 pin 8 is SPI chip select.",
                ),
                "11": binding(
                    net="TROPIC_VCC_SW",
                    pin_name="VCC",
                    physical_pin=11,
                    source="TROPIC01 datasheet ODD_TR01_datasheet_vA_11",
                    review_status="source_backed",
                    evidence="TROPIC01 pin 11 is VCC.",
                ),
                "12": binding(
                    net="GND",
                    pin_name="GND",
                    physical_pin=12,
                    source="TROPIC01 datasheet ODD_TR01_datasheet_vA_11",
                    review_status="source_backed",
                    evidence="TROPIC01 pin 12 is GND.",
                ),
                "23": binding(
                    net="GND",
                    pin_name="GND",
                    physical_pin=23,
                    source="TROPIC01 datasheet ODD_TR01_datasheet_vA_11",
                    review_status="source_backed",
                    evidence="TROPIC01 pin 23 is GND.",
                ),
                "24": binding(
                    net="TROPIC_VCC_SW",
                    pin_name="VCC",
                    physical_pin=24,
                    source="TROPIC01 datasheet ODD_TR01_datasheet_vA_11",
                    review_status="source_backed",
                    evidence="TROPIC01 pin 24 is VCC.",
                ),
            },
            symbol="TROPIC_SQUARE:TR01-P2",
        ),
        "J1": component(
            "usb_c_receptacle",
            "kicad/sheets/power_usb.kicad_sch",
            {
                "A1": binding(net="GND", pin_name="GND", source="GCT USB4105 drawing", review_status="source_backed", evidence="A1 is GND."),
                "B12": binding(net="GND", pin_name="GND", source="GCT USB4105 drawing", review_status="source_backed", evidence="B12 is GND."),
                "A4": binding(net="VBUS", pin_name="VBUS", source="GCT USB4105 drawing", review_status="source_backed", evidence="A4 is VBUS."),
                "B9": binding(net="VBUS", pin_name="VBUS", source="GCT USB4105 drawing", review_status="source_backed", evidence="B9 is VBUS."),
                "A5": binding(net="USB_CC1_RD", pin_name="CC1", source="GCT USB4105 drawing", review_status="source_backed", evidence="A5 is CC1 and must use Rd for USB device mode."),
                "B5": binding(net="USB_CC2_RD", pin_name="CC2", source="GCT USB4105 drawing", review_status="source_backed", evidence="B5 is CC2 and must use Rd for USB device mode."),
                "A6": binding(net="USB_DP", pin_name="Dp1", source="GCT USB4105 drawing", review_status="source_backed", evidence="A6 is USB D+ side 1."),
                "B6": binding(net="USB_DP", pin_name="Dp2", source="GCT USB4105 drawing", review_status="source_backed", evidence="B6 is USB D+ side 2."),
                "A7": binding(net="USB_DM", pin_name="Dn1", source="GCT USB4105 drawing", review_status="source_backed", evidence="A7 is USB D- side 1."),
                "B7": binding(net="USB_DM", pin_name="Dn2", source="GCT USB4105 drawing", review_status="source_backed", evidence="B7 is USB D- side 2."),
                "A9": binding(net="VBUS", pin_name="VBUS", source="GCT USB4105 drawing", review_status="source_backed", evidence="A9 is VBUS."),
                "B4": binding(net="VBUS", pin_name="VBUS", source="GCT USB4105 drawing", review_status="source_backed", evidence="B4 is VBUS."),
                "A12": binding(net="GND", pin_name="GND", source="GCT USB4105 drawing", review_status="source_backed", evidence="A12 is GND."),
                "B1": binding(net="GND", pin_name="GND", source="GCT USB4105 drawing", review_status="source_backed", evidence="B1 is GND."),
            },
            symbol="Connector:USB_C_Receptacle_USB2.0",
        ),
        "J2": component(
            "display_ffc",
            "kicad/sheets/display_controls.kicad_sch",
            {
                "1": binding(net="TFT_BACKLIGHT_A", pin_name="LEDA", physical_pin=1, source="EastRising ER-TFT024IPS-3 datasheet", review_status="backlight_driver_review_required", evidence="FFC pin 1 LEDA backlight anode to the final backlight supply/current path."),
                "2": binding(net="TFT_BACKLIGHT_K", pin_name="LEDK1", physical_pin=2, source="EastRising ER-TFT024IPS-3 datasheet", review_status="backlight_driver_review_required", evidence="FFC pin 2 LEDK1 cathode return to the final current driver."),
                "3": binding(net="TFT_BACKLIGHT_K", pin_name="LEDK2", physical_pin=3, source="EastRising ER-TFT024IPS-3 datasheet", review_status="backlight_driver_review_required", evidence="FFC pin 3 LEDK2 cathode return to the final current driver."),
                "4": binding(net="TFT_BACKLIGHT_K", pin_name="LEDK3", physical_pin=4, source="EastRising ER-TFT024IPS-3 datasheet", review_status="backlight_driver_review_required", evidence="FFC pin 4 LEDK3 cathode return to the final current driver."),
                "5": binding(net="TFT_BACKLIGHT_K", pin_name="LEDK4", physical_pin=5, source="EastRising ER-TFT024IPS-3 datasheet", review_status="backlight_driver_review_required", evidence="FFC pin 5 LEDK4 cathode return to the final current driver."),
                "6": binding(net="GND", pin_name="IM0", physical_pin=6, source="EastRising ER-TFT024IPS-3 datasheet", review_status="source_backed", evidence="4-wire 8-bit Serial Interface II requires IM0=0."),
                "7": binding(net="DISPLAY_VCC_SW", pin_name="IM1", physical_pin=7, source="EastRising ER-TFT024IPS-3 datasheet", review_status="source_backed", evidence="4-wire 8-bit Serial Interface II requires IM1=1."),
                "8": binding(net="DISPLAY_VCC_SW", pin_name="IM2", physical_pin=8, source="EastRising ER-TFT024IPS-3 datasheet", review_status="source_backed", evidence="4-wire 8-bit Serial Interface II requires IM2=1."),
                "9": binding(net="DISPLAY_VCC_SW", pin_name="IM3", physical_pin=9, source="EastRising ER-TFT024IPS-3 datasheet", review_status="source_backed", evidence="4-wire 8-bit Serial Interface II requires IM3=1."),
                "10": binding(net="TFT_RST", pin_name="RESET", physical_pin=10, source="EastRising ER-TFT024IPS-3 datasheet", review_status="source_backed", evidence="FFC pin 10 is RESET."),
                "33": binding(net="TFT_SPI_MISO", pin_name="SDO", physical_pin=33, source="EastRising ER-TFT024IPS-3 datasheet", review_status="source_backed", evidence="FFC pin 33 SDO is serial output (MISO) in Serial Interface II."),
                "34": binding(net="TFT_SPI_MOSI", pin_name="SDI", physical_pin=34, source="EastRising ER-TFT024IPS-3 datasheet", review_status="source_backed", evidence="FFC pin 34 SDI is serial input (MOSI) in Serial Interface II."),
                "36": binding(net="TFT_DC", pin_name="WRX(D/CX)", physical_pin=36, source="EastRising ER-TFT024IPS-3 datasheet", review_status="source_backed", evidence="FFC pin 36 is D/CX (data/command) in serial mode."),
                "37": binding(net="TFT_SPI_SCK", pin_name="D/CX(SCL)", physical_pin=37, source="EastRising ER-TFT024IPS-3 datasheet", review_status="source_backed", evidence="FFC pin 37 is SCL serial clock."),
                "38": binding(net="TFT_CS", pin_name="CSX", physical_pin=38, source="EastRising ER-TFT024IPS-3 datasheet", review_status="source_backed", evidence="FFC pin 38 is CSX chip-select."),
                "40": binding(net="DISPLAY_VCC_SW", pin_name="VDDI", physical_pin=40, source="EastRising ER-TFT024IPS-3 datasheet", review_status="source_backed", evidence="FFC pin 40 VDDI interface rail."),
                "41": binding(net="DISPLAY_VCC_SW", pin_name="VDDI", physical_pin=41, source="EastRising ER-TFT024IPS-3 datasheet", review_status="source_backed", evidence="FFC pin 41 VDDI interface rail."),
                "42": binding(net="DISPLAY_VCC_SW", pin_name="VCI", physical_pin=42, source="EastRising ER-TFT024IPS-3 datasheet", review_status="source_backed", evidence="FFC pin 42 VCI logic rail."),
                "43": binding(net="GND", pin_name="GND", physical_pin=43, source="EastRising ER-TFT024IPS-3 datasheet", review_status="source_backed", evidence="FFC pin 43 is GND."),
                "44": binding(net="TOUCH_I2C_SCL", pin_name="SCL", physical_pin=44, source="EastRising ER-TFT024IPS-3 datasheet", review_status="source_backed", evidence="FFC pin 44 is capacitive touch I2C SCL."),
                "45": binding(net="TOUCH_I2C_SDA", pin_name="SDA", physical_pin=45, source="EastRising ER-TFT024IPS-3 datasheet", review_status="source_backed", evidence="FFC pin 45 is capacitive touch I2C SDA."),
                "46": binding(net="TOUCH_INT", pin_name="INT", physical_pin=46, source="EastRising ER-TFT024IPS-3 datasheet", review_status="source_backed", evidence="FFC pin 46 is capacitive touch interrupt, active low."),
                "47": binding(net="TOUCH_RST", pin_name="RESET", physical_pin=47, source="EastRising ER-TFT024IPS-3 datasheet", review_status="source_backed", evidence="FFC pin 47 is capacitive touch reset, active low."),
                "48": binding(net="GND", pin_name="GND", physical_pin=48, source="EastRising ER-TFT024IPS-3 datasheet", review_status="source_backed", evidence="FFC pin 48 is GND."),
                "49": binding(net="GND", pin_name="GND", physical_pin=49, source="EastRising ER-TFT024IPS-3 datasheet", review_status="source_backed", evidence="FFC pin 49 is GND."),
                "50": binding(net="GND", pin_name="GND", physical_pin=50, source="EastRising ER-TFT024IPS-3 datasheet", review_status="source_backed", evidence="FFC pin 50 is GND."),
            },
            symbol="Connector_Generic:Conn_01x50",
        ),
        "U5": component(
            "qspi_nor_flash",
            "kicad/sheets/storage_expansion.kicad_sch",
            {
                "1": binding(net="QSPI_NCS", pin_name="/CS", physical_pin=1, source="Winbond W25Q128JV datasheet", review_status="source_backed", evidence="Standard W25Q128JV 8-pin SPI/QSPI chip-select pin."),
                "2": binding(net="QSPI_IO1", pin_name="DO/IO1", physical_pin=2, source="Winbond W25Q128JV datasheet", review_status="source_backed", evidence="Standard W25Q128JV 8-pin data output / IO1 pin."),
                "3": binding(net="QSPI_IO2", pin_name="/WP/IO2", physical_pin=3, source="Winbond W25Q128JV datasheet", review_status="source_backed", evidence="Standard W25Q128JV 8-pin write-protect / IO2 pin."),
                "4": binding(net="GND", pin_name="GND", physical_pin=4, source="Winbond W25Q128JV datasheet", review_status="source_backed", evidence="Standard W25Q128JV 8-pin ground pin."),
                "5": binding(net="QSPI_IO0", pin_name="DI/IO0", physical_pin=5, source="Winbond W25Q128JV datasheet", review_status="source_backed", evidence="Standard W25Q128JV 8-pin data input / IO0 pin."),
                "6": binding(net="QSPI_CLK", pin_name="CLK", physical_pin=6, source="Winbond W25Q128JV datasheet", review_status="source_backed", evidence="Standard W25Q128JV 8-pin clock pin."),
                "7": binding(net="QSPI_IO3", pin_name="/HOLD/IO3", physical_pin=7, source="Winbond W25Q128JV datasheet", review_status="source_backed", evidence="Standard W25Q128JV 8-pin hold/reset / IO3 pin."),
                "8": binding(net="SYS_3V3", pin_name="VCC", physical_pin=8, source="Winbond W25Q128JV datasheet", review_status="source_backed", evidence="Standard W25Q128JV 8-pin supply pin."),
            },
            symbol="Memory_Flash:W25Q128JVxIM",
        ),
        "U9": component(
            "nfc_rfid_frontend",
            "kicad/sheets/optional_profiles.kicad_sch",
            {
                "1": binding(net="NFC_VCC_SW", pin_name="VDD_IO", physical_pin=1, source="ST25R3916B datasheet DS13541 Rev 11", review_status="source_backed", evidence="Pin 1 is VDD_IO."),
                "6": binding(net="GND", pin_name="GND_D", physical_pin=6, source="ST25R3916B datasheet DS13541 Rev 11", review_status="source_backed", evidence="Pin 6 is digital ground."),
                "8": binding(net="NFC_VCC_SW", pin_name="VDD", physical_pin=8, source="ST25R3916B datasheet DS13541 Rev 11", review_status="source_backed", evidence="Pin 8 is external positive supply."),
                "10": binding(net="NFC_VCC_SW", pin_name="VDD_TX", physical_pin=10, source="ST25R3916B datasheet DS13541 Rev 11", review_status="source_backed", evidence="Pin 10 is TX positive supply input."),
                "12": binding(net="GND", pin_name="GND_DR1", physical_pin=12, source="ST25R3916B datasheet DS13541 Rev 11", review_status="source_backed", evidence="Pin 12 is antenna driver ground."),
                "16": binding(net="GND", pin_name="GND_DR2", physical_pin=16, source="ST25R3916B datasheet DS13541 Rev 11", review_status="source_backed", evidence="Pin 16 is antenna driver ground."),
                "20": binding(net="GND", pin_name="I2C_EN", physical_pin=20, source="ST25R3916B datasheet DS13541 Rev 11", review_status="source_backed", evidence="I2C_EN must be pulled to GND for SPI operation."),
                "21": binding(net="GND", pin_name="VSS", physical_pin=21, source="ST25R3916B datasheet DS13541 Rev 11", review_status="source_backed", evidence="Pin 21 is die substrate ground."),
                "26": binding(net="GND", pin_name="GND_A", physical_pin=26, source="ST25R3916B datasheet DS13541 Rev 11", review_status="source_backed", evidence="Pin 26 is analog ground."),
                "27": binding(net="NFC_IRQ", pin_name="IRQ", physical_pin=27, source="ST25R3916B datasheet DS13541 Rev 11", review_status="source_backed", evidence="Pin 27 is IRQ."),
                "29": binding(net="NFC_SPI_CSN", pin_name="BSS", physical_pin=29, source="ST25R3916B datasheet DS13541 Rev 11", review_status="source_backed", evidence="Pin 29 is SPI enable active-low."),
                "30": binding(net="NFC_SPI_SCK", pin_name="SCLK", physical_pin=30, source="ST25R3916B datasheet DS13541 Rev 11", review_status="source_backed", evidence="Pin 30 is SPI clock."),
                "31": binding(net="NFC_SPI_MOSI", pin_name="MOSI", physical_pin=31, source="ST25R3916B datasheet DS13541 Rev 11", review_status="source_backed", evidence="Pin 31 is SPI data input."),
                "32": binding(net="NFC_SPI_MISO", pin_name="MISO", physical_pin=32, source="ST25R3916B datasheet DS13541 Rev 11", review_status="source_backed", evidence="Pin 32 is SPI data output."),
                "33": binding(net="GND", pin_name="Thermal pad", physical_pin=33, source="ST25R3916B datasheet DS13541 Rev 11", review_status="source_backed", evidence="Thermal pad is GND."),
            },
            symbol="RFID:ST25R3916B",
        ),
        "U11": component(
            "second_secure_element",
            "kicad/sheets/secure_element_2.kicad_sch",
            {
                "1": binding(net="GND", pin_name="GND", physical_pin=1, source="OPTIGA Trust M datasheet Rev 3.70", review_status="source_backed", evidence="PG-USON-10 pin 1 is GND."),
                "3": binding(net="SE2_I2C_SDA", pin_name="SDA", physical_pin=3, source="OPTIGA Trust M datasheet Rev 3.70", review_status="source_backed", evidence="PG-USON-10 pin 3 is SDA."),
                "8": binding(net="SE2_I2C_SCL", pin_name="SCL", physical_pin=8, source="OPTIGA Trust M datasheet Rev 3.70", review_status="source_backed", evidence="PG-USON-10 pin 8 is SCL."),
                "9": binding(net="SE2_RST", pin_name="RST", physical_pin=9, source="OPTIGA Trust M datasheet Rev 3.70", review_status="source_backed", evidence="PG-USON-10 pin 9 is reset."),
                "10": binding(net="SYS_3V3", pin_name="VCC", physical_pin=10, source="OPTIGA Trust M datasheet Rev 3.70", review_status="source_backed", evidence="PG-USON-10 pin 10 is VCC."),
            },
            symbol="Security:OPTIGA_Trust_M",
        ),
        "SW1": component(
            "left_side_button",
            "kicad/sheets/display_controls.kicad_sch",
            {
                "1": binding(net="BTN_LEFT", pin_name="1", physical_pin=1, source="Panasonic EVQP7J01P package drawing review", review_status="footprint_review_required", evidence="One side of left side-actuated button goes to BTN_LEFT."),
                "2": binding(net="GND", pin_name="2", physical_pin=2, source="Panasonic EVQP7J01P package drawing review", review_status="footprint_review_required", evidence="Other side of left button returns to GND."),
            },
            symbol="Switch:SW_Push",
        ),
        "J9": component(
            "lipo_battery_connector",
            "kicad/sheets/power_usb.kicad_sch",
            {
                "1": binding(net="VBAT", pin_name="BAT+", physical_pin=1, source="JST PH 2-pin footprint review", review_status="footprint_review_required", evidence="Battery positive enters power-path charger."),
                "2": binding(net="GND", pin_name="BAT-", physical_pin=2, source="JST PH 2-pin footprint review", review_status="footprint_review_required", evidence="Battery negative returns to GND."),
            },
            symbol="Connector_Generic:Conn_01x02",
        ),
        "TP_SWDIO": test_point("TP_SWDIO", "SWDIO", "hidden_swdio_pogo_test_pad"),
        "TP_SWCLK": test_point("TP_SWCLK", "SWCLK", "hidden_swclk_pogo_test_pad"),
        "TP_NRST": test_point("TP_NRST", "NRST", "hidden_nrst_pogo_test_pad"),
        "TP_BOOT0": test_point("TP_BOOT0", "BOOT0", "hidden_boot0_pogo_test_pad"),
        "TP_UART_TX": test_point("TP_UART_TX", "EXP_UART_TX", "hidden_uart_tx_pogo_test_pad"),
        "TP_UART_RX": test_point("TP_UART_RX", "EXP_UART_RX", "hidden_uart_rx_pogo_test_pad"),
        "TP_3V3": test_point("TP_3V3", "SYS_3V3", "hidden_3v3_pogo_test_pad"),
        "TP_GND": test_point("TP_GND", "GND", "hidden_gnd_pogo_test_pad"),
    }


def build_review_required_nets(components: dict[str, object], netlist_contract: dict[str, object]) -> dict[str, object]:
    bound_nets = {
        pin["net"]
        for component_value in components.values()
        for pin in component_value["pins"].values()
        if isinstance(pin, dict) and isinstance(pin.get("net"), str) and pin["net"].strip()
    }
    contract_nets = {
        net
        for nets in netlist_contract["required_buses"].values()
        for net in nets
    }
    reasons = {
        "EXP_I2C_SCL": "Expansion I2C pins are intentionally not assigned until the final connector footprint is selected.",
        "EXP_I2C_SDA": "Expansion I2C pins are intentionally not assigned until the final connector footprint is selected.",
        "EXP_SPI_SCK": "Expansion SPI pins are intentionally not assigned until conflict analysis with NFC/display/TROPIC buses is complete.",
        "EXP_SPI_MOSI": "Expansion SPI pins are intentionally not assigned until conflict analysis with NFC/display/TROPIC buses is complete.",
        "EXP_SPI_MISO": "Expansion SPI pins are intentionally not assigned until conflict analysis with NFC/display/TROPIC buses is complete.",
        "EXP_SPI_CSN": "Expansion SPI pins are intentionally not assigned until conflict analysis with NFC/display/TROPIC buses is complete.",
        "NFC_ANT1": "Antenna FPC and matching network must be tuned with final mechanics and enclosure.",
        "NFC_ANT2": "Antenna FPC and matching network must be tuned with final mechanics and enclosure.",
    }
    review_required: dict[str, object] = {}
    for net_name in sorted(contract_nets - bound_nets):
        review_required[net_name] = {
            "review_status": "explicitly_unbound",
            "reason": reasons.get(net_name, "Requires final schematic symbol, footprint, or production test binding before routing."),
        }
    return review_required


def build_schematic_binding() -> dict[str, object]:
    pinmux = json.loads(PINMUX_LEDGER_JSON.read_text(encoding="utf-8"))
    netlist_contract = json.loads(NETLIST_CONTRACT_JSON.read_text(encoding="utf-8"))
    components = build_components(pinmux)
    return {
        "board": BOARD_NAME,
        "schema_version": 1,
        "status": "schematic_binding_pre_routing",
        "scope": "Source-backed KiCad ref/pin/net binding before ERC, PCB update, routing, and PCBWay export.",
        "source_contracts": {
            "pinmux_ledger": "production/pinmux-ledger.json",
            "netlist_contract": "production/netlist-contract.json",
        },
        "kicad_project": "kicad/tropic01-universal-secure-device.kicad_pro",
        "release_gates": [
            "no_llm_invented_pin_numbers",
            "all_bound_nets_match_pinmux_ledger",
            "schematic_symbols_have_verified_pin_numbers",
            "layout_review_required_for_rf_usb_display_power",
            "erc_clean_before_pcb_update",
            "pcbway_export_unblocked_only_after_routing",
        ],
        "components": components,
        "review_required_nets": build_review_required_nets(components, netlist_contract),
        "notes": [
            "This contract is not a PCBWay release artifact; it is a guardrail for generating and reviewing the KiCad schematic.",
            "NFC antenna nets remain explicitly unbound until FPC/antenna matching is designed and measured.",
            "Expansion I2C/SPI nets remain explicitly unbound because Rev A0 must avoid assigning pins without connector and conflict review.",
        ],
    }


def write_schematic_binding(path: Path = SCHEMATIC_BINDING_JSON) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_schematic_binding(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    write_schematic_binding()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
