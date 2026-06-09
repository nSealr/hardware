# Rev A0 Pinmux Ledger Summary

Status: source-backed schematic intent. This is not yet a routed PCB release.
The authoritative machine-readable version is
`production/pinmux-ledger.json`.

Evidence used:

- STM32U585xx datasheet DS13086 Rev 10: LQFP100 pinout, pin definitions, and
  alternate-function tables.
- TROPIC01 datasheet ODD_TR01_datasheet_vA_11: QFN32 pinout and SPI mode.
- ST25R3916B/ST25R3917B/ST25R3919B datasheet DS13541 Rev 11: QFN32 pinout and
  SPI interface selection.
- OPTIGA Trust M datasheet Rev 3.70: PG-USON-10 contact definitions.
- Newhaven NHD-2.4-240320AF-CSXP-CTP datasheet: display, touch, connector, and
  mode-select requirements.

## STM32U585VIT6 LQFP100 Assignments

### USB 2.0 Device

| Net | MCU pin | LQFP100 pin | Function |
| --- | --- | ---: | --- |
| `USB_VBUS_SENSE` | `PA9` | 68 | `OTG_FS_VBUS` |
| `USB_DM` | `PA11` | 70 | `OTG_FS_DM` |
| `USB_DP` | `PA12` | 71 | `OTG_FS_DP` |

USB-C CC pull-downs, ESD, VBUS current limiting, and differential-pair routing
remain schematic/layout gates.

### TROPIC01 SPI

| Net | MCU pin | LQFP100 pin | Function |
| --- | --- | ---: | --- |
| `TROPIC_SPI_CSN` | `PA4` | 29 | `SPI1_NSS` |
| `TROPIC_SPI_SCK` | `PA5` | 30 | `SPI1_SCK` |
| `TROPIC_SPI_MISO` | `PA6` | 31 | `SPI1_MISO` |
| `TROPIC_SPI_MOSI` | `PA7` | 32 | `SPI1_MOSI` |
| `TROPIC_PWR_EN` | `PB0` | 35 | GPIO output |
| `TROPIC_GPO` | `PB2` | 37 | GPIO input / EXTI |

TROPIC01 remains power-cycle controlled; do not add a TROPIC reset pin.

### Display SPI and Touch I2C

| Net | MCU pin | LQFP100 pin | Function |
| --- | --- | ---: | --- |
| `TFT_SPI_SCK` | `PC10` | 78 | `SPI3_SCK` |
| `TFT_SPI_MOSI` | `PC12` | 80 | `SPI3_MOSI` |
| `TFT_CS` | `PC7` | 64 | GPIO output |
| `TFT_DC` | `PC8` | 65 | GPIO output |
| `TFT_RST` | `PC6` | 63 | GPIO output |
| `TFT_BACKLIGHT_PWM` | `PA8` | 67 | `TIM1_CH1` / PWM |
| `TFT_PWR_EN` | `PC9` | 66 | GPIO output |
| `TOUCH_I2C_SCL` | `PB8` | 95 | `I2C1_SCL` |
| `TOUCH_I2C_SDA` | `PB9` | 96 | `I2C1_SDA` |
| `TOUCH_INT` | `PE1` | 98 | GPIO input / EXTI |
| `TOUCH_RST` | `PE0` | 97 | GPIO output |

The Newhaven panel is used in 4-wire SPI mode with `IM0=0`, `IM1=1`,
`IM2=1`. Touch I2C pull-ups are 4.7 kOhm per the display datasheet.

### OPTIGA Trust M I2C

| Net | MCU pin | LQFP100 pin | Function |
| --- | --- | ---: | --- |
| `SE2_I2C_SCL` | `PB6` | 92 | `I2C4_SCL` |
| `SE2_I2C_SDA` | `PB7` | 93 | `I2C4_SDA` |
| `SE2_RST` | `PB5` | 91 | GPIO output |

OPTIGA intentionally uses a dedicated I2C bus rather than sharing the touch
controller bus.

### NFC/RFID Controller

| Net | MCU pin | LQFP100 pin | Function |
| --- | --- | ---: | --- |
| `NFC_SPI_CSN` | `PB12` | 51 | `SPI2_NSS` |
| `NFC_SPI_SCK` | `PB13` | 52 | `SPI2_SCK` |
| `NFC_SPI_MISO` | `PB14` | 53 | `SPI2_MISO` |
| `NFC_SPI_MOSI` | `PB15` | 54 | `SPI2_MOSI` |
| `NFC_IRQ` | `PD0` | 81 | GPIO input / EXTI |
| `NFC_PWR_EN` | `PB1` | 36 | GPIO output |

ST25R3916B uses QFN32 pin 29 `BSS`, pin 30 `SCLK`, pin 31 `MOSI`, pin 32
`MISO`, pin 27 `IRQ`, and pin 20 `I2C_EN`. Pull `I2C_EN` to GND for SPI mode.

The antenna and matching values are not frozen. They must be tuned against the
final top-edge antenna FPC or PCB antenna and enclosure.

### QSPI / OCTOSPI NOR

| Net | MCU pin | LQFP100 pin | Function |
| --- | --- | ---: | --- |
| `QSPI_CLK` | `PE10` | 41 | `OCTOSPIM_P1_CLK` |
| `QSPI_NCS` | `PE11` | 42 | `OCTOSPIM_P1_NCS` |
| `QSPI_IO0` | `PE12` | 43 | `OCTOSPIM_P1_IO0` |
| `QSPI_IO1` | `PE13` | 44 | `OCTOSPIM_P1_IO1` |
| `QSPI_IO2` | `PE14` | 45 | `OCTOSPIM_P1_IO2` |
| `QSPI_IO3` | `PE15` | 46 | `OCTOSPIM_P1_IO3` |

This avoids the PA4-PA7 bank reserved for TROPIC01 SPI.

### Buttons, Debug, and UART

| Net | MCU pin | LQFP100 pin | Function |
| --- | --- | ---: | --- |
| `BTN_LEFT` | `PE2` | 1 | GPIO input / EXTI |
| `BTN_RIGHT` | `PE3` | 2 | GPIO input / EXTI |
| `EXP_UART_TX` | `PD5` | 86 | `USART2_TX` |
| `EXP_UART_RX` | `PD6` | 87 | `USART2_RX` |
| `SWDIO` | `PA13` | 72 | `JTMS/SWDIO` |
| `SWCLK` | `PA14` | 76 | `JTCK/SWCLK` |
| `BOOT0` | `PH3-BOOT0` | 94 | Boot strap |
| `NRST` | `NRST` | 14 | Reset |

SWD, BOOT0, NRST, UART, and power rails should be exposed through hidden
back-side pads only. Hardened firmware must lock debug before any production
security claim.

## Remaining Gates

- Convert this ledger into real KiCad schematic labels and wires.
- Run KiCad ERC after schematic binding.
- Update PCB from schematic and route all nets.
- Verify USB differential pair routing and impedance.
- Tune NFC antenna/matching with the final antenna and enclosure.
- Run KiCad DRC before generating Gerbers/BOM/CPL for PCBWay.
