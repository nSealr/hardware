# TROPIC01 Universal Secure Device Design

Date: 2026-06-08
Status: approved product direction, not yet implementation plan

## Goal

Design one compact open hardware device that can become the reference all-in-one
development and deployment platform for projects that need a TROPIC01-based
secure element.

The device is not only a wallet. It must support many secure-device use cases:
hardware wallet prototypes, FIDO/passkey experiments, PGP/SSH signing,
portable root-of-trust, device identity, secure IoT, attestation, NFC workflows,
offline approval flows, signed logs, and secure firmware/update experiments.

The product must be a single board variant. There will not be separate male/female
USB versions and there will not be separate "dev" and "hardened" PCB shapes.
Security and development behavior will be controlled by firmware configuration,
population choices, and debug lock state.

## Current Repository/KiCad Reality

The existing `tropic01-universal-secure-device` KiCad board is a placement mockup,
not a production-ready PCB. KiCad IPC inspection reported:

- 49 footprints
- 1 net
- 0 tracks
- 0 vias
- 0 zones
- 4 copper layers
- one rectangular board outline around 52 mm x 82 mm

Therefore the current board cannot be treated as electrically connected or
manufacturable. The implementation must regenerate the schematic/netlist and then
place and route the PCB from that source of truth.

## Product Form

The board is portrait-oriented, similar to a small smartphone or compact hardware
wallet.

- Front: dominated by a rectangular touch display.
- Bottom short edge: one centered USB-C receptacle.
- Top short edge: NFC/RFID antenna region or antenna FPC interface.
- Upper left long edge: side-actuated physical button.
- Upper right long edge: side-actuated physical button.
- Back: MCU, secure elements, NFC controller, power, flash, debug pads, and
  compact expansion/test interfaces.

The PCB should follow the display envelope as closely as practical. The target
Rev A0 display has an outline of about 42.8 mm x 59.91 mm, so the PCB should be
designed around that class of footprint instead of preserving the larger mockup
shape unless RF, USB, battery, or assembly constraints justify the extra area.

## Chosen Architecture

```text
USB-C / LiPo
    |
    v
Power path + 3V3 rails
    |
    +--> STM32U5 host MCU
    |       | USB HID/CDC/WebUSB/device protocol
    |       | display + touch UI
    |       | NFC policy and application firmware
    |       | secure boot / firmware update / debug lock
    |       |
    |       +--> TROPIC01 over SPI
    |       +--> OPTIGA-class secure element over I2C
    |       +--> ST25R3916B NFC controller over SPI
    |       +--> QSPI NOR flash
    |       +--> touch controller over I2C
    |       +--> side buttons, LEDs, test pads, compact expansion
    |
    +--> power-gated display backlight / NFC / optional domains
```

TROPIC01 is the main open secure element and root-of-trust. STM32U5 is the
application host. TROPIC01 must not be treated as the application processor: it
is a secure coprocessor controlled by the host over SPI.

## Core Components

### Secure Element 1: TROPIC01

Use TROPIC01 as the main open secure element.

Recommended part:

- Primary: `TR01-C2P-T301`
- Alternative if available and justified: `TR01-C2P-T310`

Design requirements:

- QFN32 package, 4 mm x 4 mm, 0.4 mm pitch.
- SPI mode 0: CPOL = 0, CPHA = 0, MSB first.
- Native 3.3 V-compatible rail, respecting 3.6 V absolute maximum.
- Local decoupling close to all VCC pins.
- Pull pins wired according to the official TROPIC01 reference design.
- GPO connected to MCU/test visibility through a conservative resistor path, but
  firmware must not depend on GPO during early startup because public
  documentation shows availability limitations for some startup states.
- TROPIC01 VCC should be switchable or power-controllable so the host can recover
  it without a dedicated reset pin.

### Secure Element 2: OPTIGA-Class I2C Secure Element

Include a second commercial secure element on the final product. This follows the
defense-in-depth lesson from Trezor Safe 7 while keeping TROPIC01 as the open
secure element at the center of the design.

Recommended family:

- Infineon OPTIGA Trust M / Trust M V3 class device, connected over I2C.

Purpose:

- anti-clone / attestation support;
- second independent trust anchor;
- optional policy counters or authentication material;
- extra barrier if one silicon vendor or one interface is compromised;
- closer alignment with modern hardware-wallet defense-in-depth.

This is not a separate optional variant. It is part of the single product design.

### Host MCU

Use STM32U5 as the application processor.

Recommended part:

- Primary: `STM32U585VIT6`, LQFP100.
- Fallback: `STM32U575VIT6`, LQFP100, if supply or cost makes it preferable.

Reasons:

- mature embedded ecosystem;
- TrustZone and security features;
- USB device support;
- enough pins for SPI display, touch, TROPIC01, NFC, flash, buttons, debug, and
  compact expansion;
- compatible with the Tropic Square STM32/libtropic development path.

If a future 3.5-4.0 inch display requires DSI/RGB/QSPI display bandwidth, MCU and
package must be re-evaluated. Rev A0 is optimized around a compact SPI display.

### Display and Touch

Use a rectangular capacitive touch display as a mandatory component.

Recommended Rev A0 display:

- `Newhaven NHD-2.4-240320AF-CSXP-CTP`
- 2.4 inch IPS TFT
- 240 x 320 portrait
- ST7789VI display controller
- FT5426 capacitive touch controller
- 3.3 V TFT and touch domains
- 40-pin TFT FFC plus 6-pin CTP FFC

Reasons:

- large enough for QR codes, wallet confirmations, passkey prompts, debugging
  screens, and open-source application UIs;
- still compact enough for a small handheld board;
- uses SPI/I2C-class interfaces that fit STM32U5 Rev A0 complexity;
- avoids jumping immediately to a larger DSI/RGB display system.

Display connectors must use verified footprints matching the chosen Newhaven
recommended connectors or exact approved alternatives. Proxy FFC footprints are
not acceptable for production output.

### USB-C

Use one USB-C receptacle only.

Recommended connector:

- `GCT USB4105-GF-A` or exact mechanically/electrically compatible approved
  footprint.

Requirements:

- centered on the bottom short edge;
- USB 2.0 device role;
- CC1 and CC2 Rd pull-down resistors;
- ESD protection close to connector;
- VBUS current limiting/protection;
- short and controlled D+/D- route to the MCU.

Rejected option:

- USB-C male plug version.

Reason for rejection: a male-plug board is mechanically weaker, worse for a
display/battery handheld device, harder to protect in a case, and less universal
than a receptacle.

### NFC/RFID

Include NFC/RFID support as a first-class feature.

Recommended controller:

- `ST25R3916B`

Requirements:

- SPI connection to STM32U5;
- IRQ and enable/control GPIOs;
- 27.12 MHz crystal per controller reference design;
- tunable matching network;
- dedicated top-edge antenna region or antenna FPC connector;
- NFC power domain controllable by firmware/hardware.

The antenna must not be represented by decorative graphics. A production design
needs a real antenna strategy: either a tuned PCB antenna with keepouts and
measured matching, or a tuned antenna FPC/module path. The Trezor Safe 7 hardware
split between main board and antenna FPC is an important reference here.

Default security posture:

- NFC off by default until firmware explicitly enables it;
- no secrets exposed over NFC without user confirmation and protocol-level
  authentication;
- NFC attack surface documented in the threat model.

### Battery and Power Path

Include battery support in the single product.

Recommended charger/power-path class:

- `BQ24074` or equivalent single-cell LiPo charger with true power-path behavior.

Requirements:

- USB VBUS powers the system and charges LiPo;
- system can operate with no battery, bad battery, or depleted battery when USB
  power is present;
- battery connector on the back or edge where the enclosure can support it;
- battery voltage sense to MCU ADC through a controlled divider;
- charge/status pins routed to MCU or test visibility where useful.

Avoid simple charger-only designs that do not manage system load and battery load
cleanly.

### System Rail

Use a 3.3 V system rail sized for MCU, display, TROPIC01, OPTIGA, NFC, flash, and
reasonable expansion current.

Candidate:

- `TPS62840` class ultra-low-power buck.

Constraint:

- current budget must be calculated before freezing. The Newhaven display
  backlight and NFC can dominate current. If the 750 mA class is tight, choose a
  higher-current compatible buck variant instead of forcing the design around an
  undersized regulator.

Power domains:

- system 3V3;
- TROPIC01 switched/filtered VCC;
- display/backlight power control;
- NFC power control;
- optional expansion current limiting.

### Local Storage

Include soldered QSPI NOR flash.

Recommended capacity:

- 16 MB minimum;
- 32-64 MB preferred if package, cost, and availability are acceptable.

Allowed uses:

- firmware assets;
- UI assets;
- signed logs;
- cached public data;
- encrypted non-secret blobs;
- recovery/update staging.

Not allowed:

- treating external flash as secure storage for unprotected secrets.

### microSD Decision

Do not include microSD in the single product.

Reason:

- it consumes valuable board and enclosure space;
- it requires user-accessible mechanical openings;
- it adds untrusted filesystem and parser attack surface;
- it invites misuse as "secure" removable storage;
- its main benefits can be covered by USB, NFC, QR/display workflows, and
  soldered encrypted flash.

Users who need removable storage can attach external hardware through expansion
or use host-side workflows.

### Physical Buttons

Use two side-actuated physical buttons near the upper left and upper right long
edges.

Purpose:

- approve/reject;
- wake/sleep;
- hard confirmation boundary independent of touch;
- recovery and boot interactions.

Requirements:

- buttons actuate toward the sides, not front-facing;
- they must be reachable with the display facing the user;
- footprints must match exact selected part numbers;
- no proxy front tact-switch footprints.

Touch is useful for navigation, but sensitive approval should have a physical
button path.

### Pogo/Test Pads

Include hidden back-side pogo/test pads.

Purpose:

- production test;
- initial flashing;
- recovery during development;
- board bring-up;
- automated rail and interface checks.

Signals:

- SWDIO;
- SWCLK;
- NRST;
- BOOT0;
- UART TX/RX;
- GND;
- 3V3;
- VBUS or protected VBUS;
- selected power rails/test points.

These are not user-facing features. The enclosure can cover them completely. In
the hardened firmware profile, debug must be locked or disabled by option bytes
and firmware policy.

### Expansion

The board should support open-source experimentation without becoming a large
header board.

Include:

- one Qwiic/STEMMA QT I2C connector if space allows;
- compact back-side pads for UART;
- compact back-side pads or solder option for external SPI/TROPIC01 host access;
- power-limited 3V3 expansion output.

Do not include large Arduino/Raspberry Pi-style headers on the main product.
They conflict with the compact display-sized form factor.

External TROPIC01 host access must be physically isolatable from the STM32U5 host
through solder jumpers, zero-ohm options, or bus-switch topology. Hardened builds
must be able to disable this path.

## Explicitly Excluded From Rev A0

- USB-C male plug version.
- microSD slot.
- WiFi.
- BLE.
- Camera.
- Large 3.5-4.0 inch display.
- Consumer enclosure design.
- Certification files for CE/FCC/RED.
- Claiming production readiness before ERC/DRC, routing, antenna validation, and
  board bring-up are complete.

These can be revisited after Rev A0 proves the core architecture.

## Security Model

The board must be useful for development but not careless by default.

Principles:

- TROPIC01 is the open secure element and primary trust anchor.
- OPTIGA-class SE provides independent defense-in-depth.
- STM32U5 owns UI, USB, NFC policy, and application logic.
- User approval requires touch UI plus physical-button path for sensitive
  actions.
- NFC is power-gated or disabled until explicitly enabled.
- Debug pads are hidden and lockable.
- External TROPIC01 host path is useful for developers but must be disableable.
- Soldered QSPI flash is not secure storage unless data is encrypted and
  authenticated by keys protected elsewhere.
- No BLE/WiFi in Rev A0 to avoid unnecessary radio attack surface.

TROPIC01 security advisories must be tracked. The June 3, 2026 advisory about
potential laser fault injection bypass of firmware verification means the board
must not rely on a single physical component as the only security boundary.
Firmware update policy, maintenance-mode restrictions, and defense-in-depth must
be documented.

## Implementation Requirements

Before generating files for PCBWay:

1. Replace the current custom hardware narrative with this product direction.
2. Freeze a real component table with statuses: chosen, alternative, rejected.
3. Build a real KiCad schematic with correct symbols, power domains, and nets.
4. Use verified or custom-created footprints for all connectors and critical
   parts.
5. Regenerate the PCB from the schematic/netlist.
6. Place the PCB according to the approved portrait layout.
7. Route USB, SPI, power, display, NFC, and debug/test paths.
8. Add real NFC antenna strategy and matching network.
9. Run ERC and DRC.
10. Export Gerbers, drill, BOM, CPL, assembly drawings, and fabrication notes only
    after ERC/DRC are clean or explicitly waived.

## Validation Criteria

Rev A0 is successful when these checks pass on real hardware:

- USB-C powers the board safely.
- Battery power-path works with and without battery installed.
- STM32U5 can be flashed through pogo/SWD before lock.
- USB enumerates reliably.
- Display shows UI and touch controller reports coordinates.
- Side buttons actuate correctly from the edges.
- TROPIC01 can be identified through libtropic.
- TROPIC01 TRNG, key generation, and signature examples work.
- OPTIGA-class SE can be detected and used for attestation/basic operations.
- QSPI flash read/write/erase works.
- NFC controller initializes and antenna/matching can be measured/tuned.
- Debug can be locked for hardened mode.
- External TROPIC01 host path can be enabled for development and disabled for
  hardened use.

## Source Evidence

Primary references used for this design:

- Tropic Square devboards: https://github.com/tropicsquare/devboards
- TROPIC01 docs and part numbers: https://github.com/tropicsquare/tropic01
- libtropic SDK: https://github.com/tropicsquare/libtropic
- Trezor Safe 7 hardware: https://github.com/trezor/trezor-hardware/tree/master/electronics/trezor_safe_7
- Newhaven display datasheet: https://newhavendisplay.com/content/specs/NHD-2.4-240320AF-CSXP-CTP.pdf
- GCT USB4105 spec: https://gct.co/files/specs/usb4105-spec.pdf
- TI BQ24074 product/datasheet: https://www.ti.com/product/BQ24074
- TI TPS62840 product/datasheet: https://www.ti.com/product/TPS62840
- ST25R3916B product documentation: https://www.st.com/en/nfc/st25r3916b.html
- STM32U585 product documentation: https://www.st.com/en/microcontrollers-microprocessors/stm32u585vi.html
