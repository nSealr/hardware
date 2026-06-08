# Rev A0 Pinmux Intent

Status: schematic intent. Final STM32U5 pins must be checked against the
datasheet and generated KiCad symbol before routing.

## Dedicated Interfaces

- TROPIC01 SPI:
  - `SPI_TROPIC_SCK`
  - `SPI_TROPIC_MOSI`
  - `SPI_TROPIC_MISO`
  - `SPI_TROPIC_CSN`
  - `TROPIC_GPO`
  - `TROPIC_PWR_EN`

- Display/touch:
  - `SPI_DISP_SCK`
  - `SPI_DISP_MOSI`
  - `SPI_DISP_CSN`
  - `DISP_DC`
  - `DISP_RST`
  - `DISP_BL_EN`
  - `I2C_TOUCH_SCL`
  - `I2C_TOUCH_SDA`
  - `TOUCH_INT`
  - `TOUCH_RST`

- OPTIGA second secure element:
  - `I2C_SEC_SCL`
  - `I2C_SEC_SDA`
  - optional reset/enable if required by selected package.

- NFC/RFID:
  - `SPI_NFC_SCK`
  - `SPI_NFC_MOSI`
  - `SPI_NFC_MISO`
  - `SPI_NFC_CSN`
  - `NFC_IRQ`
  - `NFC_EN`

- QSPI NOR:
  - `QSPI_CLK`
  - `QSPI_CS`
  - `QSPI_IO0`
  - `QSPI_IO1`
  - `QSPI_IO2`
  - `QSPI_IO3`

- User controls:
  - `BTN_LEFT`
  - `BTN_RIGHT`

- Debug/test:
  - `SWDIO`
  - `SWCLK`
  - `NRST`
  - `BOOT0`
  - `UART_TX`
  - `UART_RX`

## Bus Rules

- Display SPI and TROPIC01 SPI must stay physically separate in Rev A0.
- External-host access to TROPIC01 must be physically selectable and disableable.
- NFC is power-gated and disabled by default in hardened firmware.
- microSD, BLE, WiFi, and radio signals are not allocated in Rev A0.
