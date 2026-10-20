# Finite U5G9 comparison for Board UI and SDK

Author `/root/h01_sol`, 20 October 2026, after `4d3fa674`. This is C10's
mandatory document comparison, **not a third host port**, selected MCU/display,
received DK2 or permission to build/connect it. It preserves the two U585/S3
paper contracts and every unsatisfied source/physical gate. The maintainer's
generic Board/SDK, touchscreen and physical-confirmation priorities make the
old no-touch baseline a comparator, not an irrevocable product choice.

## Exact identities and pin/power costs

The retained exact leads are **STM32U5G9ZJT6Q, LQFP144/SMPS**, and the distinct
**STM32U5G9ZJJ6Q, UFBGA144/SMPS**. DS14102 Rev5's ordering table and native
pinouts distinguish them. DK2's MB1918-U5G9ZJQ-C01 uses ZJT6Q/3.3 V with parallel
RGB; DK1 is a different package/1.8 V/DSI reference and is not interchangeable.
These are proposed comparison identities; actual marking/REV_ID/board remains
unknown. Earlier selected ES0595 Rev4 applicability stays binding, not a claim
that a particular revision removes every defect.

| Function / cost | Exact ZJT6Q LQFP144 correspondence | Comparison implication |
| --- | --- | --- |
| Retained CPU SPI subset | PE13 pad59 AF5 SCK; PE15 pad61 AF5 MOSI; PE12 pad58 software CS; PC1 pad30 D/C; PA8 pad102 reset; PB6 pad136 blank request. | The larger part has these pins, but DK2 uses PE13/PE15/PE12 for RGB G6/R2/G5. Its fitted RGB cannot silently coexist with the baseline SPI mapping. More RAM does not change the baseline wire time. |
| Six baseline controls | PC0 pad29, PC2 pad31, PA7 pad45, PB0 pad46, PE7 pad51, PD15 pad80. | PE7/PD15 are RGB B6/B3 on DK2. A complete custom allocation must preserve independent consent, touch/IRQ and private SE paths; this table is not a full map or use of spare kit headers. |
| Native USB | PA11 pad105 D−, PA12 pad106 D+, VDDUSB pad108. | These are not U585 pad numbers or proof of a ready HS/FS/USB driver. The G9 reference's HS/sink architecture and pin/power ownership would need its own exact admission. |
| Parallel RGB reference |24 data pins plus PCLK PD3/119, DE PD6/123, HSYNC PE0/141, VSYNC PD13/78; native CN3 is50 pins. |28 timing/data signals, plus display enable PE4/3, backlight PE6/5 and touch PF0/10+PF1/11 AF4 I2C2 with PE5/4 IRQ: **33 GPIO signals**, plus shared NRST/28. Its touch bus is not automatically a private SE bus. |
| DSI alternative cost | Dedicated D0± pads15/16, clock±18/19, D1±21/22; VDDDSI13, VDD11DSI14/20, VSSDSI17/23. | Fewer display data conductors than parallel RGB, with high-speed PHY/layout/rails, protocol and module costs. DK2 leaves the DSI data pins unconnected; no DSI panel/driver or MIPI source contract is selected here. |
| Other domains | VDDIO2 pad131 supplies PG[15:2]; VDDSMPS65/VLXSMPS64/VSSSMPS66; VDD11 pads67/142. | VDD/VDDSMPS1.71–3.6 V, VDDIO2 1.08–3.6 V, USB3.0–3.6 V. DSI supply must track VDD and its1.0–1.26 V PHY rail connects VDD11. Independent supply/power-down sequencing and the <1 V/+300 mV rule matter. No 5 V GPIO or generic raw-panel rail follows. |

The native DK2 power drawing shows VDD/VDDIO2/VDDA/VDDUSB/VDDDSI ties through
their stated links, VDD11/DSI11 and the2.2 µH SMPS connection. It is evidence
of that reference's connections, not a qualified custom power tree. The LQFP
20×20 mm body and UFBGA10×10 mm body have different fanout/assembly/inspection
costs. Footprint area, trace density, rail sequencing, touch/backlight and a50-pin
connection still require manufacturing/BOM review. No price, yield, stack-up or
power estimate is fabricated from the smaller body or a kit's headline.

## Native DK2 PC13/LSE proof

The exact official MB1918-C01 PDF, hash
`65c90d6af3771e4cd1539598883039f850b794f4c6cc117c7dca5309000f9bd2`, is
newly read at these native sheets:

1. Sheet3: U2B ZJT6Q has PC14/OSC32_IN pad8 and PC15/OSC32_OUT pad9 connected
   to X1 32.768 kHz, with C2/C3 nominal3.3 pF. This is a crystal path, not bypass.
2. Sheet4: U2C PC13 pad7 reaches the hierarchical `PC13-WKUP2` port.
3. Sheet2: the wire joins that MCU port to User Interface `USER_BUTTON`.
4. Sheet9: B2 closes USER_BUTTON to3V3; no external low-hold resistor is drawn
   in that button branch. UM3223 §8.4's low-when-released statement still needs
   the actual GPIO/internal-pull/default configuration, not an invented resistor.

This agrees with UM3223 §§7.6.1/8.4. ES0595 §2.2.1 p5 explicitly covers PC13
input **or** output transitions on LQFP with an LSE crystal; bypass and WLCSP/
UFBGA are excluded from that limitation. There is no workaround listed.
Thus stock DK2 X1 plus B2 activity cannot be inherited as an unaffected clock/
confirmation reference. Merely ignoring B2 in software does not prevent its
physical input transition. A future promoted custom configuration must avoid
that combination and bind another exact permitted control/reference solution
before use; neither a new clock lead nor an additional kit probe is opened.
This is source/circuit correspondence, not a measured LSE failure or defective-
board assertion. The PDF's sheet2 legacy title text does not replace its project,
variant, revision and sheet identity; no other PCB/CAD revision is substituted.

## Memory, masters and private display data

DS14102 §3.5 lists SRAM1/2/3/4/5/6 as768/64/832/16/832/512 KiB. Their sum is
**3024 KiB before the stated ECC reservations**, not a free3 MiB arena. SRAM3
with ECC exposes256 KiB ECC-supported plus512 KiB without ECC (768 KiB total);
the2 KiB backup bank is separate and is not a secret/framebuffer budget. Address,
alias, clock, bank/retention and physical contiguous ranges still matter.
Current RM Table10 gives512-byte MPCBB blocks,32 blocks per lock super-block,
with separate controllers including SRAM5/6. Do not inherit U585's two-bank
manifest, whole-SRAM lock count or C05 linker map onto G9.

Two800×480 RGB565 frames require1,536,000 bytes (**1500 KiB**), compared with
900 KiB for two480×480 frames and150 KiB for one240×320 frame. At a purely
capacity level one750 KiB frame is smaller than SRAM3's768 KiB post-ECC capacity
and SRAM5's832 KiB; this does not allocate either bank, establish contiguity or
prove the complete app/stack/secret/backend/SDK fit. It does establish a material
internal-memory reason to continue the existing G9 comparison under the new
touch/SDK preference. At a hypothetical60 Hz a single800×480 RGB565 scanout
reads at least46.08 MB/s of active pixels, before blanking/arbitration/rendering;
that is required traffic, not a measured or guaranteed rate.

The actual master boundary is essential:

| Resource | Current source result | Consequence before promotion/use |
| --- | --- | --- |
| LTDC | RM2.1.7 p132 is a read master reaching internal memories and GFXMMU; GTZC1 SECCFGR2 bit9 is LTDCUSBSEC on G9, not the U585-reserved USB meaning. | Secure register access is not a completed private scanout/configuration/reset proof. Bind the exact master's attributes, framebuffer ownership, faults and effective source path before any private recovery pixels. No implied DMA/master exclusion once enabled. |
| GPU2D/DCACHE2 | RM9.3 p383 explicitly says GPU2D traffic is nonsecure and DCACHE2 does not support TrustZone; DCACHE2 caches GPU M0 including the configured internal SRAM path. | GPU2DSEC/DCACHE2_REGSEC protect control access; they do not turn that traffic into secure memory access. Keep secrets/private rows out of GPU command/texture/frame buffers and copies. It is not a qualified private-recovery renderer or hostile-app boundary. |
| GFXMMU | Separate GFXMMU register and memory security fields (SECCFGR3 bits25/24) and the programmable buffer/LUT mapping are distinct. | A secure register label or virtual framebuffer is not proof that physical backing/cache is private. Validate physical ranges, all masters, locks, cache maintenance and generation before use. |
| DMA2D/other masters | Additional bus masters are real, not CPU-only graphics helpers. C05's unselected-master exclusions are specific to its hosts. | A future G9 admission needs a new exact **selected** master/address/IRQ/RCC/GTZC manifest, preserving private/public separation and reset/fault clearing. No driver/module declaration authorizes those masters here. |

CPU rendering, full-screen scanout and cache completion also do not prove optical
completion, correct screen generation or operation/consent binding. A readable
touchscreen requires exact module startup/rails/logic, touch ownership/debounce,
bounded error paths, blanking/reset lifetime, complete review and physical
confirmation decision. Its pixels and input events are not automatic authority.

## Maintained source and license comparison

The existing Embassy pin `69006a4158aa6d605ad8506ade0f2f79159131e3` declares
`stm32u5g9zj` and the graphics modules in `embassy-stm32`0.6.0. The crate's
manifest declares MIT OR Apache-2.0. Newly read **selected actual source** narrows
what those declarations mean:

* `ltdc.rs` header says it was tested on H735G-DK/RM0468, not G9 qualification.
  Selected buffer/reload methods accept raw framebuffer addresses, wait for
  controller flags, and return FIFO/transfer errors; the waits contain no
  inherent absolute deadline, and `Drop` does not shut the block down. Their
  API comment about copied pixels is not proof of G9 scanout/optical completion.
* `gpu2d.rs` provides status/interrupt/command-list completion handling, not a
  reviewed command generator/decoder. Its completion wait does not observe its
  separate system error. The NemaGFX cache-hold hook transfers interrupt ownership
  to platform code; the source explicitly keeps that library outside this crate.
  That hook is not a licensed, implemented vector-renderer integration here.
* Selected GFXMMU source initializes interrupts and buffer/LUT configuration;
  its cache flush/invalidate waits have no finite timeout. Actual bounds,
  backing ranges, cache errors and interrupt service still need exact review
  if promoted. A task timeout does not preempt those synchronous loops.

Thus a claim that **no Rust display support exists is unsupported**, while
“maintained module exists” is not a working G9 display/Touch/secure-renderer
claim. No new display driver, NemaGFX integration or vendor binary is selected.
If any vendor graphics middleware is later used, its exact source/ABI/license/
redistribution/maintenance terms must be read separately; Embassy's license
does not transfer to another library. Existing OPLA reading covers source
handling here, not a legal/IP/whole-SDK clearance or permission to republish
manufacturer drawings. A narrow maintained C adapter remains permissible under
the same gates; there is no all-Rust requirement or forced rewrite.

## Finite recommendation and limits

Retain G9 as the **existing higher-UI/memory comparison for H04**, because the
internal bank capacities and RGB/touch reference address a concrete readable/
responsive SDK/recovery question that the no-touch SPI baseline does not answer.
Defer promotion/selection or any port: exact custom pin/SE/expansion allocation,
clock/rails/power/current, private scanout/master isolation, full bounded driver/
license/effective-build fit, module/input/optical quality, PC13/reference choice
and manufacturing/cost evidence are not closed. Do not resolve those by calling
all graphics secure, replacing the baseline silently or expanding this milestone.

The few non-Nostr cases in [the existing comparison](option-comparison.md)
(status/approval console, key-operation agent, provisioning/recovery) remain
the concrete comparison workloads. More RAM and touch can help navigation and
entry; no CPU benchmark, touch latency, animation quality, energy or simultaneous
workload capacity has been measured. One trusted owner image and the separate
Signer gates remain. The two-SE hypotheses and S04/advisory/access constraints
are unchanged; the G9 does not supply their missing services/composition proof.
Exact G9/custom-BOM cost is **not established**; the separately dated raw-panel
module price is not the cost of this larger touch reference or complete Board.
Root's coherent few-configuration comparison and evidence precede H04 freeze.

## Actual scope and sources

New native reads: exact MB1918-C01 sheets2/3/4/5/7/9 and DS14102 Figures9/10
pp101/102 pinouts. Other CAD/BOM/PCB/variant, display-module internals, all native
package drawings and unselected USB/power circuits are not a new full audit.
Selected DS32–35/55–56 supply/graphics and exact used AF rows131–147 are read/
reread with prior SRAM/order/outline scopes reused. Neighboring RNG/SAES/TSC,
other-package or unused AF context encountered is not a promoted feature review.
Current RM132/159, selected GTZC fields205–210 and DCACHE382–384 are read/reread;
figures encountered as text are not newly visually audited. No complete G9
LTDC/GPU/DSI/command ISA or RNG/USB implementation review is claimed.

GPU2D source1–162 is read; selected GFXMMU95–259 and LTDC1–5/640–805 are read,
with source selectors identifying other declarations, not reviewing their bodies.
Cargo1–10/158–227/1990 and library module-gate rows are read/reused. No target
build, register access, benchmark, root/key operation or physical test was run.

Primary links: [DS14102](https://www.st.com/resource/en/datasheet/stm32u5g9nj.pdf),
[ES0595](https://www.st.com/resource/en/errata_sheet/es0595-stm32u5fxxx-and-stm32u5gxxx-device-errata-stmicroelectronics.pdf),
[UM3223](https://www.st.com/resource/en/user_manual/um3223-discovery-kit-with-stm32u5g9zj-mcu-stmicroelectronics.pdf),
[exact MB1918-C01 schematic](https://www.st.com/resource/en/schematic_pack/mb1918-u5g9zjq-c01-schematic.pdf),
[pinned Embassy graphics source](https://github.com/embassy-rs/embassy/tree/69006a4158aa6d605ad8506ade0f2f79159131e3/embassy-stm32/src).
Originals/renders/extractions stay private; register metadata/claim reasoning is
public. Native circuit correspondence closes that reading question, not G9 or
H01 host admission.
