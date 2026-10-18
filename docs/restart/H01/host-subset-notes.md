# H01 follow-up manual reading

Author: `/root/h01_author`, 2026-10-18. These are documentary findings after
the distinct review of `19362fc9a12bed43070c56642b4a932f1bc6a545` and its
`d5d7530` handoff. The material errata correction is separate at `16a7d4b`.
The newer [current-manual notes](current-manual-notes.md) supersede the old
retrieval gaps and explicitly extend the reading below. No host, wiring,
component selection, target implementation or measurement is
approved here. Exact reading and original hashes are in
[manual-register.json](manual-register.json); proposed configurations still need
the sign-off in [review-coverage.md](review-coverage.md).

## S3 selected GPIO, SPI and watchdog paths

The preserved [TRM v1.8](https://documentation.espressif.com/esp32-s3_technical_reference_manual_en.pdf)
was read further at printed pp.481–482, 493–494, 507–515, 519–520,
613–615, 665–679, 908–918, 1114, 1124–1128, 1141, 1157–1158 and
1237–1242. Register text and tables were read; this is not a visual inspection
of every timing drawing or a full 1531-page review.

- The GPIO10–13 SPI2 witness uses IO_MUX **function 4**. The reset table
  enables inputs on those pins, while the GPIO4–7 control pool starts with
  input disabled. Neither state supplies a panel reset or button pull network.
  GPIO output enable may come from the peripheral or software; pin ownership
  must include both selection and output enable. Hold can preserve an older
  pin state across reset/sleep. A new mux setting alone does not release it.
- The selected GPIO interrupt registers describe edge/level modes, status
  clearing and routing to CPU/NMI. GPIO wake described here is light-sleep
  wake; it is not a blanket deep-sleep promise. Debounce, stuck input,
  authorization lifetime and any electrical filter remain separate work.
- The master SPI state/length and CS timing text is now read. A new manual
  contradiction remains: Tables30.5-9/10 footnotes reverse the bit-order
  meaning given by Table30.5-5 and register30.6. The latter agree on the
  single-bit interpretation. Record and check the maintained driver before
  relying on it; no register recipe or panel clock is approved.
- All chapter13 functional watchdog text was read, together with selected
  MWDT/RWDT register descriptions. MWDT core reset and RWDT system/RTC reset
  affect different domains. Timing depends on the chosen APB/RTC clock,
  prescaling, stage and sleep behavior. The super watchdog's optional automatic
  feeding does not demonstrate application health. Write protection guards
  accidental writes, not hostile firmware. H02 must identify which failure each
  watchdog is intended to detect and which consent/secret state survives reset.

Remaining relevant S3 manual reading is specific: GPIO §§6.6–6.8 and
§§6.11–6.13 beyond the portions above if the selected path uses their
routing/filter functions; SPI selected transaction/error/DMA registers and
maintained driver; exact kit schematic and complete panel electrical/startup
contract. Unused RMT, touch, LCD_CAM, host-USB and autonomous paths do not require
new ports. Their omission must be explicit in the proposed configuration.

## Sleep, entropy and external-memory encryption

The source comparison pins ESP-IDF v6.1 to commit
[`fff9895c82d744c7237be8847347bdd1b07c6643`](https://github.com/espressif/esp-idf/tree/fff9895c82d744c7237be8847347bdd1b07c6643).
Only the functions/lines in the register were read. This does not select IDF as
the Board implementation or qualify an unrelated Rust HAL.

`rtc_sleep_get_default_config` and `rtc_sleep_init`, with the corresponding
`rtc.h` defaults, establish a concrete correspondence for corrected
**ANALOG-160**: the two assertions reject the forbidden conjunction and the
reviewed default branches avoid it. A build that disables assertions still
needs valid configuration at every caller; custom values and other sleep
implementations do not inherit this result. No damaging configuration is a
permitted physical negative test. **TOUCH-100** retains its complete corrected
interrupt workaround; the initial physical-button proposal does not use that
touch interrupt path.

The full `esp_random`/`esp_fill_random` implementation and S3
`bootloader_random_enable/disable` functions were read. The return type provides
no source-health error. Sampling delay and extra mixing are implementation
behavior, not proof of qualified entropy. The boot entropy path configures both
SAR units and internal channels; its use must exclude conflicting ADC ownership
and meet the versioned RNG documentation. A source comment about the secondary
clock is not a substitute for that documented entropy contract. H02 needs an
explicit source-state/failure adapter and the actual linked call path. Effective
configuration must exclude CONFIG_ESP_BRINGUP_BYPASS_RANDOM_SETTING, whose
reviewed source branch returns a fixed pattern.

Chapter23's XTS text and register descriptions are now read. Key-purpose
configuration can select missing/all-zero key material; an encryption-enabled
flag alone is insufficient evidence of provisioned custody. Cache-mediated
RAM encryption and software-driven flash encryption are different paths.
The ciphertext-destroy action does not establish that the separately readable
plaintext register bank has been wiped. The chapter's enable-bit prose also
differs from the precise odd-population-count description of
`SPI_BOOT_CRYPT_CNT` at p.433. Both discrepancies are in the ledger. No fuse
operation, secret provisioning or zeroization guarantee follows from this read.

## USB public documentation and software boundary

S3 TRM **§32.4 pp.1237–1242 is OTG/HNP/SRP material**. The relevant
access-limit statement is **§32.5, printed p.1242**: comprehensive USB-OTG
register specifications are subject to the IP provider's NDA. The public
§32.3 device/FIFO/DMA description remains useful. Its IN/OUT register-name
contradiction is not silently resolved by pretending the complete register
chapter is public.

The versioned IDF `usb_struct.h` distinguishes `diep*` IN and `doep*` OUT fields.
Selected global functions in `usb_dwc_ll.h` expose software DMA/slave selection,
reset, FIFO and interrupt handling, but much of that file concerns USB host
operation. It is not the selected device controller driver. These sources
support observed software semantics; they neither replace normative IP
specifications nor prove bus-master isolation.

The current Espressif device wrapper was read at
[`fc9bead300f82484eace377d5dea2f3e11163206`](https://github.com/espressif/esp-usb/tree/fc9bead300f82484eace377d5dea2f3e11163206/device/esp_tinyusb).
Its manifest reports 2.4.0 but allows TinyUSB **>=0.17.0~2**, so that manifest
alone does not pin the underlying device driver. Its configuration enables
slave/IRQ support and can also enable DMA; the latter takes priority when
supported. The installation function chooses internal PHY, full-speed device
mode for S3, with separate self-powered VBUS handling. This is a candidate
software path, not an actual nSealr build or measured USB configuration.

For a bounded CPU-FIFO device proposal, close the exact TinyUSB dependency,
compile-time configuration, endpoint/FIFO partition, reset/flush/error/timeout
path and buffer ownership. Demonstrate from the selected binary/configuration
that unused DMA/host modes are not enabled. If required semantics remain
undocumented, prepare narrowly scoped manufacturer questions against §32.5:

1. Which public, revision-specific source defines the selected device FIFO
   limits, flush/reset completion and interrupt side effects?
2. What is the correct direction-specific register correspondence for the
   §32.3.6 IN/OUT examples?
3. Only if USB-master DMA is used: which address regions, alignment, protection
   and abort/completion semantics apply to that selected mode?

No external inquiry has been sent. A header or successful traffic test cannot
answer a missing hardware isolation specification. Conversely, an unused DMA
path need not expand the initial probe. Developer access is a selection
criterion for S3 as it is for U5/SE candidates; it does not by itself select or
reject the complete chip family.

## Current U5 and power follow-up

For [DS14102 Rev5](https://www.st.com/resource/en/datasheet/stm32u5g9zj.pdf),
the author read the complete §3.5 SRAM-bank text, §§3.8–3.9.2 power/security
overview, §§3.19–3.20 through p.55, §§3.41–3.42 display features, selected
§6.3 mechanical text/table, §7 ordering and §9 revision history. The larger
RAM is banked, with ECC costs; GPU2D, DMA2D and LTDC introduce bus masters.
The power-sequence constraints and package-specific USB/DSI/core rails must
enter a future exact allocation. Rev5 repairs package information introduced
in Rev4. Exact AF/pad matching, current RM ownership and graphics-driver/license
closure remain open. The attempted web screenshots yielded no usable image:
that earlier visual gap is now closed for the two native outline figures listed
in current-manual-notes.md; no footprint or complete pad review is claimed.

[ES0595 Rev4](https://www.st.com/resource/en/errata_sheet/es0595-stm32u5fxxx-and-stm32u5gxxx-device-errata-stmicroelectronics.pdf)
§§2.9–2.10 pp.19–20 now have body-level reading: DSI automatic clock-lane
control is constrained; the indicated EoT/contention errors can be false;
SAES's specified backup-key transfers require ascending reads. These are
specific configuration constraints, not a general failure of graphics or SAES.

[UM3223 Rev2](https://www.st.com/resource/en/user_manual/um3223-discovery-kit-with-stm32u5g9zj-mcu-stmicroelectronics.pdf)
§§1–2 pp.2–3 were initially inherited from the distinct review. Fresh
author reading of the [manufacturer DK2 feature page](https://estore.st.com/en/stm32u5g9j-dk2-cpn.html)
corroborates ZJT6Q/LQFP144, 3.3 V and 800×480 RGB. That earlier pass had only an indexed §7.5 excerpt. The new native author
reading covers §§7.5–8.6, including power selection and display connector.
The complete schematic/BOM and exact board revision remain unreviewed. DK2 is a closer
package reference than DK1; it is neither a third bench port nor an inherited
custom Board design. An 800×480 RGB565 buffer is **750 KiB**, or **1500 KiB**
for two, calculated before any other allocation.

For [ES0499 Rev12](https://www.st.com/resource/en/errata_sheet/es0499-stm32u575xx-and-stm32u585xx-device-errata-stmicroelectronics.pdf),
current selected U585 bodies are now read: §§2.2.20–2.2.26,
2.15.1, 2.17–2.18, 2.23, 2.25–2.26. USB-device FIFO interleaving and ZLP
sequencing require exact driver checks; SPI completion must preserve the last
clock/data interval. ECC reporting, flash error recovery and watchdog/backup
reset interaction remain implementation requirements. RevX UCPD Rd limits
matter for a sink proposal; they are not inherited by W/U. The new pass has read all current core/system bodies pp.7–16 and selected
RM reset/clock/RNG/USB text. Remaining used bodies and exact driver/configuration
correspondence still prevent qualification of any U585 revision.

[TPS63802 SLVSEU9D](https://www.ti.com/lit/ds/symlink/tps63802.pdf)
§§9.3.3–9.3.10 pp.11–12 now explicitly support the startup/reverse-current
discussion. Reverse energy can raise the input before the device's protection
intervenes; PG is not proof of complete board isolation. Keep the two retained
power chains, and leave cell/OPN/circuit/USB entitlement and physical waveforms
for their stated gates.
