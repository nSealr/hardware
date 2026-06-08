# Component Freeze Notes

Status: Rev A0 contract freeze, schematic not yet generated.

## Frozen Core

- `U2` TROPIC01 `TR01-C2P-T301`: primary open secure element.
- `U2_ALT` TROPIC01 `TR01-C2P-T310`: preferred alternate when obtainable.
- `U1` STM32U5 `STM32U585VIT6`: primary host MCU.
- `U1_ALT` STM32U5 `STM32U575VIT6`: fallback host MCU.
- `DISP1` Newhaven `NHD-2.4-240320AF-CSXP-CTP`: 2.4 inch portrait touch
  display.
- `J1` GCT `USB4105-GF-A`: female USB-C receptacle only.
- `U9` ST `ST25R3916B-AQET`: NFC/RFID controller.
- `U10` TI `BQ24074RGTR`: LiPo charger with real power path.
- `U11` Infineon OPTIGA Trust M class `OPTIGA-TRUST-M-SLS32AIA`: second secure
  element.
- `U5` Winbond `W25Q128JVSIQ`: QSPI NOR flash.

## Footprint Risks

- `J2` Molex `54132-4062` and `J2B` Molex `52271-0679` require exact footprint
  verification against the Newhaven display drawing before PCBWay output.
- `U11` OPTIGA footprint is currently a USON-10 candidate. The exact Infineon
  package drawing must be checked before layout freeze.
- `SW1/SW2` must be side-actuated switch footprints. Front tact-switch
  footprints are not acceptable.
- `ANT1` is not a decorative PCB loop. It is either an antenna FPC connector or
  a tuned antenna keep-out with matching network and measurement notes.

## Excluded

- USB-C male plug variant.
- microSD.
- BLE.
- WiFi.
- Radio module.
- Camera.
