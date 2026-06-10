# Subsystem 7 — Display (ER-TFT024IPS-3, 50-pin FFC) design

Date: 2026-06-10
Status: design captured. The full 50-pin FFC pin map is in
`production/schematic-binding.json` (J2) and `pinmux.md`. Clean rebuild.

## Interfaces (single 50-pin FFC, J2)

- **Display SPI (4-wire Serial Interface II)**: straps `IM3:IM2:IM1:IM0 = 1110`
  (FFC pins 6-9); SCL=pin37→`TFT_SPI_SCK` (PC10), SDI=34→`TFT_SPI_MOSI` (PC12),
  SDO=33→`TFT_SPI_MISO`, D/CX=36→`TFT_DC` (PC8), CSX=38→`TFT_CS` (PC7),
  RESET=10→`TFT_RST` (PC6).
- **Touch I2C (FT6336)**: SCL=44→`TOUCH_I2C_SCL` (PB8), SDA=45→`TOUCH_I2C_SDA`
  (PB9), INT=46→`TOUCH_INT` (PE1), RESET=47→`TOUCH_RST` (PE0). **4.7 kΩ pull-ups**
  on SCL/SDA to +3V3.
- **Power**: VCI(42)/VDDI(40,41)→`DISPLAY_VCC_SW` (switched by `TFT_PWR_EN`=PC9
  load switch or LDO); GND on 43/48-50.
- Unused parallel pins (VSYNC/HSYNC/DOTCLK/DE, DB0-17, RD) → no-connect; TE(39)
  optional to a GPIO.

## Backlight driver (4 LED strings, Vf 3.2 V, 80 mA total)

3.3 V cannot drive 3.2 V LED strings with headroom, so use a small **boost
constant-current LED driver** (TPS61165-class) from `VSYS`: anode `LEDA` (FFC 1)
to the boost output, the four cathodes `LEDK1-4` (FFC 2-5) tied to the driver's
CC sink. PWM dimming via `TFT_BACKLIGHT_PWM` (PA8, TIM1_CH1). Add the boost
inductor + output cap + the driver's feedback per its datasheet.

> This adds one backlight-driver IC + inductor to the BOM (was previously
> unaddressed). Final driver part is a small selection step.

## ERC gate

All bound display/touch/power/backlight nets present; IM straps + pull-ups;
unused FFC pins no-connect; ERC clean before subsystem 8.
