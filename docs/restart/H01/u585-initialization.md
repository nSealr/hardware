# U585 ownership and clock/reset proposal

Author `/root/h01_sol`, 20 October 2026; source continuation from `e35ee73`.
This is a documentary initialization contract for the two U585 package witnesses
in [configuration-review.md](configuration-review.md). It is not executable
register code, admission, a received-device result or a completed host review.
The [machine-readable manifest](u585-peripheral-manifest.json) records the
derived field correspondence and its unresolved implementation checks.

## Runtime boundary and ordering

The initial proposal runs one trusted secure privileged image, with TZEN active,
all implemented internal SRAM blocks secure and privileged, and no nonsecure
application. UI, USB and crypto buffers remain separate software arenas; this
does not protect secrets against arbitrary execution in that trusted image.
Development can use open debug and disposable keys only. The owner-secured
transition remains a separate, unfinished lifecycle contract.

Before USB attachment or accepting controls, startup must establish the intended
clock/power state, configure attribution, clear retained secret-bearing state,
check the selected SRAM ECC status, establish the fault handlers and initialize
the independent watchdog. Configure all implemented TZSC security/privilege
fields, read them back, then set each controller's `LCK`. Secure configuration
registers require secure access; privilege fields require privileged access.
Read access being permitted does not prove that a write was effective.

The MPCBB has two different locks. `CR.GLOCK` locks its control register;
`CFGLOCKR1/2.SPLCKx` locks each superblock's security and privilege tables.
Setting only `GLOCK` leaves those tables mutable. Conversely, setting only
`SPLCKx` leaves the control policy mutable. Both locks persist until system
reset, so reset startup must reestablish them before servicing requests.

For this all-secure SRAM proposal, keep `SRWILADIS=0` and `INVSECSTATE=0`,
verify each implemented attribution word, lock every implemented superblock,
and then lock its control register. RM0456 Rev7 Table33 p199 gives exactly
12 SRAM1, 4 SRAM2, 32 SRAM3 and 1 SRAM4 superblocks. Thus the U585 lock sets
are SRAM1 bits0–11, SRAM2 bits0–3, SRAM3 bits0–31 in their `CFGLOCKR1`, and
SRAM4 bit0 in GTZC2. Generic SRAM1–3 `CFGLOCKR2` fields and MPCBB5/6 are not
an instruction to configure nonexistent U585 superblocks. This correspondence
does not change the already recorded ECC storage loss or prove erased contents.

## Device-specific peripheral correspondence

The manifest derives the implemented TZSC field sets from current RM0456 Rev7
§§5.6.2–5.6.7 and §§5.9.2–5.9.3, checked against DS13086 Rev10 Table2
pp18–20, its cover/§3.19 and RM0456 Table1 p129. It proposes secure and
privileged access for both used and excluded
implemented peripherals. The derived bit sets are `SECCFGR1/PRIVCFGR1` bits0–19,
`SECCFGR2/PRIVCFGR2` bits0–8, and `SECCFGR3/PRIVCFGR3` bits0–22.
GTZC2 uses bits0–9 and11–12. These are analysis sets, requiring independent
review and exact PAC/device correspondence before generating firmware writes.
Reserved fields retain their reset values.

In particular, U585 uses `GTZC1_TZSC_SECCFGR3.OTGSEC`,
`RCC_AHB2ENR1.OTGEN` and `RCC_AHB2RSTR1.OTGRST`. The similarly named
`LTDCUSBSEC` in TZSC configuration register2 and `USBEN/USBRST` in RCC APB2
are reserved on U575/585. They describe other devices' USB block. A family
register name or an all-ones mask would configure the wrong contract.

U585 has two OCTOSPIs, two SDMMCs, FSMC, AES/SAES/PKA, DMA2D, and the GPDMA/LPDMA
controllers. They do not disappear because the proposal uses software crypto,
internal RAM and CPU-driven SPI. Their exact reset/clock pairs are in the
manifest. GPDMA1, LPDMA1 and DMA2D remain asserted reset and clock-gated; no channel
is released or configured. SDMMC1/2 and external-memory interfaces also remain
reset and clock-gated. The proposal does not claim a running or locked DMA
channel configuration. Adding any such path requires its current body/register
review and a new ownership manifest before release from reset.

DS13086 does not give U585 the larger devices' GPU2D, GFXMMU, DCACHE2,
HSPI1, JPEG, LTDC or DSI; their corresponding family fields remain reserved.
The same applies to USART6 and I2C5/6. Unbonded package pads are a separate
question from whether a silicon peripheral/register exists. The custom
LQFP100 SMPS witness and UFBGA169 kit still need their exact GPIO/AF mapping.

## Clock gating, reset and polling

All selected RCC peripheral reset fields start at zero: zero does not assert
reset. An excluded block's proposed held-reset state is an explicit software
action that must be checked before input is accepted. RCC clock enables are a
different control. Their reset values enable SRAM, flash, backup SRAM and cache
interface clocks in several banks, even when the cache itself is disabled.
Do not infer clock gating from a peripheral's own enable bit.

RM0456 §§11.8.29–11.8.35 expressly do not support peripheral-register accesses
while its interface clock is disabled. Therefore a post-gating peripheral read
of zero cannot prove successful reset, attribution, or cleanup. Verify required
peripheral state while accessible; use RCC readback for the later reset/clock
state. Exclusion is a startup requirement, not proof against an attacker already
executing as the trusted secure privileged owner who can alter RCC.

`RCC_CCIPR1` has separate SPI1 and I2C2 kernel selectors; their reset selections
are PCLK2 and PCLK1. USB's intermediate clock and RNG's clock also have distinct
selectors. This increment fixes field correspondence, not the final frequency,
voltage-scale, flash-latency, USB calibration or I2C timing values. CPU deadlines
cannot be calculated until that tuple is fixed. Sleep/Stop/Standby and LPBAM are
excluded from the first proposal; this does not qualify USB suspend current.

The watchdog remains the proposal in H01-C40: EWI disabled, one progress-based
feed owner, no feed from a continuously firing interrupt. Blocking peripheral
waits must have software deadlines and invalidate partial output/consent on
failure. Watchdog startup and its worst-case LSI interval remain prerequisites
before any candidate unbounded source path can support a recovery argument.

## Source corrections and scope

The current GTZC register text swaps the associated peripheral in the prose for
`SDMMC1SEC/SDMMC2SEC` and their privilege counterparts, while bit names and the
register diagrams distinguish them. Both are assigned the same exclusion and
ownership policy here; no per-instance inference depends on the swapped prose.
The ledger preserves the discrepancy for a later per-instance driver.

Fresh extracted-text review: RM0456 pp213–219 (privilege continuation),
pp220–222 before §5.6.11 (watermark registers), pp256–259 before §5.8.6,
pp260–263 before §5.9.4, pp272–274 before §5.11.5 (MPCBB/TZSC registers),
pp548–569 before §11.8.37, and pp587–595 before §11.8.48. Earlier reset and
security pages were reread. Wide register-map summaries were excluded; this
is not new visual drawing review. DS13086 Table2 pp18–20 was reread directly.
Sources are the registered private originals, with public manufacturer links
and hashes in [manual-register.json](manual-register.json).

Remaining before this manifest can contribute to a complete signed host row:
GTZC/TZIC and NVIC interrupt mask/priority correspondence; selected bus-driver
register behavior; final clock/power/watchdog values; exact kit/pad controls;
the lifecycle/clear contract and source-to-binary configuration. The two complete
host configurations and six documentary signoffs remain outstanding.

The later [two-host memory contract](memory-ownership-contract.md) fixes the
SRAM1/2 address/copy/stack allocation and global HAL init correspondence. Its
limits are conditional H02 qualification caps. The older remaining-work list
above records this manifest's original stage; current finite residual scope is
in [closure-checklist.md](closure-checklist.md), without rebinding past reviews.
