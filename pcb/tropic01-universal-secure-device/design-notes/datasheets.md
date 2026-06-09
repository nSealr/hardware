# Datasheet Evidence

Primary references for Rev A0 component selection:

- TROPIC01 docs and part numbers: https://github.com/tropicsquare/tropic01
- TROPIC01 devboards and KiCad references: https://github.com/tropicsquare/devboards
- libtropic SDK: https://github.com/tropicsquare/libtropic
- Trezor Safe 7 hardware reference: https://github.com/trezor/trezor-hardware/tree/master/electronics/trezor_safe_7
- STM32U585VI: https://www.st.com/en/microcontrollers-microprocessors/stm32u585vi.html
- Newhaven display: https://newhavendisplay.com/content/specs/NHD-2.4-240320AF-CSXP-CTP.pdf
- GCT USB4105: https://gct.co/files/specs/usb4105-spec.pdf
- ST25R3916B: https://www.st.com/en/nfc/st25r3916b.html
- BQ24074: https://www.ti.com/product/BQ24074
- TPS62840: https://www.ti.com/product/TPS62840
- TPS22917: https://www.ti.com/product/TPS22917

## Local Review Set

The following PDFs were collected into
`/Users/vincenzo/Downloads/nsealr-datasheets/` during Rev A0 review. They are
not committed to the repository, but their canonical filenames are used by the
pinmux/evidence notes:

- `tropic01-datasheet.pdf`
- `newhaven-nhd-2.4-240320af-csxp-ctp.pdf`
- `stm32u575-u585-datasheet.pdf`
- `stm32u5-reference-manual.pdf`
- `st25r3916b-datasheet.pdf`
- `st25r3916b-antenna-design.pdf`
- `optiga-trust-m-datasheet.pdf`
- `bq24074-datasheet.pdf`
- `usb4105-gf-a-datasheet.pdf`
- `usb4105-gf-a-drawing.pdf`

## Confirmed Design Constraints

- TROPIC01 is a QFN32 secure element controlled by the host over SPI. It is not
  the application processor.
- TROPIC01 Rev A0 integration must use controlled power cycling, not a dedicated
  reset pin.
- TROPIC01 SPI must use 3.3 V logic and polling fallback even when GPO/IRQ is
  connected.
- The Newhaven display uses ST7789VI for display and FT5426 for capacitive touch.
- USB-C is a female receptacle only, configured as USB 2.0 device/sink.
- STM32U585VIT6 LQFP100 Rev A0 pinmux now has a source-backed ledger in
  `production/pinmux-ledger.json`; routing remains blocked until schematic nets
  and KiCad ERC/DRC agree with that ledger.
- ST25R3916B controller SPI pins are confirmed, but the antenna and matching
  network values remain measurement-gated with the final antenna and enclosure.
- OPTIGA Trust M USON-10 pins are confirmed, and the board should keep OPTIGA
  on a dedicated STM32 I2C bus rather than sharing with the touch controller.
- NFC requires a real antenna/matching strategy and first-article tuning.
- The June 3, 2026 TROPIC01 laser fault injection advisory must remain visible
  in the threat model and firmware update policy.
