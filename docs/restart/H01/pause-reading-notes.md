# H01 preserved reading at explicit pause

**H01 is incomplete and paused. No host, part or physical configuration is
admitted.** These notes preserve work completed after `c8a933f` and before the
explicit pause. No new research was started to make this checkpoint. The
register now records three already-retrieved originals; retrieval does not close
their remaining reading or configuration requirements.

## Material package correction

DS13086 Rev10, SHA256
`6483871075d4889d39356648a9c1f1fb34f48dce2ce3e8c5a8d73a73f7e935e3`,
native Figure14 p99 is the LQFP100 SMPS pinout. The p100 non-SMPS pinout was
initially rendered under a misleading private filename and misinterpreted in
an intermediate private note. Both diagrams were subsequently viewed and
compared. **PC4/PC5 are not exposed on STM32U585VIT6Q.** The previous private
record is retained unchanged with a separate correction; it must not be used
as current package evidence.

The common U585 paper proposal therefore uses PC0/PC2/PA7/PB0 for the four
direction controls, with the latter two on the kit's CN16.5/.6 default
SB10/SB13 paths. The existing `configuration-review.md` table is corrected.
This does not close other branch loads, reset behavior, ROM-download interaction
or electrical compatibility.

The already-read proposed VIQ pad correspondence is preserved here so it need
not be reconstructed from the erroneous filename:

| Function | VIQ net / pad |
| --- | --- |
| SPI clock / MOSI / select | PE13/41, PE15/43, PE12/40 |
| Display D/C / reset / backlight | PC1/16, PA8/67, PB6/92 |
| Four direction inputs | PC0/15, PC2/17, PA7/31, PB0/32 |
| Local selection / separate consent | PE7/35, PD15/62 |
| USB D− / D+ / supply | PA11/70, PA12/71, VDDUSB/73 |
| Reset / boot / excluded PC13 | NRST/14, PH3/94, PC13/7 |

These pad numbers describe the proposed LQFP package, not the kit's BGA pads.
Exact AF, load, rail, boot and ownership reconciliation remains incomplete.

## Already completed selected reading

RM0456 Rev7 pp540–547 RCC reset-register text was read before the B01 review
time-slice. It provides device-specific reset controls for excluded masters,
crypto and external-memory blocks. It does not establish a live reset/clock
manifest or prove isolation, and reserved/device-absent bits still require care.

RM0456 Rev7 pp366–373 ICACHE functional text was read after resumption. Cache
disable/invalidation clears validity and does not prove data erasure. Region
remapping can remain active while the cache is disabled, so the four region
enable controls require an explicit policy. The proposal must avoid caching
secret SRAM. Reset invalidation/BUSY handling, alias attribution and flash
modification sequencing remain configuration/driver obligations. The following
ICACHE register pages and DCACHE chapter were not read in this increment.

The register records the additional DS13086 pin, AF and electrical page ranges.
BOR4's documented falling range does not by itself ensure the USB supply's
3.0 V operating minimum, and the USB voltage monitor is not such a precision
power-good. Exact supervisor/rail and power-failure behavior remains open.

The authorized bounded Newhaven lead now has actual selected source reading:
`nhd-24-module` identifies NHD-2.4-240320DB-CTXP, its 45-contact interface,
module supply limits and current-driven backlight. Native four-wire timing and
reset/power drawings were viewed, but the mechanical drawing was not. The
linked `nhd-ili9341v` pp33–35 and107–108 were read. Command `0x21` enables
inversion; the module example's opposite comment cannot be treated as normative.
The controller's remaining applicable body and module/fixture compatibility
are unfinished. TCPP03-M20 was retrieved only; its body remains unread.

A manufacturer announcement led to the bounded
[NHD-2.4-CTXP-BREAKOUT product](https://newhavendisplay.com/tft-breakout-module-with-2-4-inch-ips-tft-display/).
The [official announcement](https://support.newhavendisplay.com/hc/en-us/articles/41454163753111-12-02-25-New-2-4-and-2-8-TFT-Breakout-Modules)
was read, while the product page was only partially read. No breakout
specification or schematic was retrieved. Its precise panel, board revision,
power, translation and connector correspondence is an unresolved lead, not a
selected part or an established solution. No fetch follows from this pause.

Private originals, extracted text and rendered manufacturer drawings stay
outside Git. The public register contains their identities and hashes, selected
reading scope and remaining work. The existing `result.json` and `handoff.md`
remain the historical `4d50d15`/`e39015a` candidate evidence; they do not bind or
approve this newer work. See `PAUSE-HANDOFF.md` for the exact paused checkpoint.
