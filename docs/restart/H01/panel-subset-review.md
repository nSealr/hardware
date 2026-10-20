# Existing Newhaven panel subset review

Selected documentary work at `ea3122647863100285a712d5cb35a094d6578ab7`,
20 October 2026, author `/root/h01_sol`. C02 remains incomplete. No panel,
fixture, supply, startup sequence or display driver is admitted. This finishes
selected source correspondence for the already authorized Newhaven lead; it
does not open another display/controller search.

## Coordinator milestone allocation, 20 October 2026

After this source checkpoint, the coordinator permitted a **conditional
factory-default-only paper display contract** for the H01 register/host-triage
milestone. It is an interface and qualification specification, not a valid
startup assertion, selected/admitted display or permission to energize it.
Normal external rail, logic-level, current, blanking and contact limits, and
all host decisions, must still close from source in H01. The two complete host
paper configurations must contain the unfulfilled display obligations; they
cannot be described as two proven working systems.

The unsatisfied exact-module prerequisite remains startup, internal-power and
factory-state evidence for this DB assembly. **H02 stops before any operation
requiring that assumption** until exact supplier/module evidence is obtained.
Controlled physical checks may use only known safe supported limits; blind
internal-power experimentation is prohibited. Without the evidence the module
stays unqualified and any replacement needs separate coordinator-approved
scope. No new lead, outreach or H04 selection/freeze follows. This allocates
the documentary question to the proper gate; it changes none of H01's six
acceptances and waives no security or electrical limit.

## Two different assemblies

The raw **NHD-2.4-240320DB-CTXP** specifies ILI9341V and links the retained
249-page V100 controller original. The current **NHD-2.4-CTXP-BREAKOUT**
product instead identifies the integrated NHD-2.4-240320AF-CTXP and ST7789VI.
Its Rev1,19 March2026 specification documents three-wire SPI, defaults to
eight-bit parallel and marks J2.15 BLK no-connect. It specifies3.3–5.5V input
and200mA typical/280mA maximum at5V. These are breakout limits, not the raw
DB panel's limits.

The breakout is **deferred for this common four-wire, separate-D/C proposal**.
The public document does not establish that contract or external backlight
control. This is not a claim that every undocumented mode is physically
impossible. Its integrated logic/backlight circuitry cannot be inherited by
the raw panel, and the raw panel's ILI9341V commands cannot be inherited by
the breakout. No ST7789VI manual/driver or further panel is pursued.

## Raw DB contact and electrical contract

Module physical pp4–6,8 and controller pp11,26 agree on the following source
mapping. It is a paper interface, not a cable, assembled continuity result or
authorization to energize a fixture.

| Function | Raw 45-contact module |
| --- | --- |
| Four-wire serial interface I | IM3:0=`0110`: pin2 IM0 low; pin3 IM1 high; pin4 IM2 high; pin5 IM3 low |
| Reset/select | RESX6; CSX34, both active low |
| Clock/data/command | SCL32; SDI/SDA30; D/CX33 |
| Unused outputs | SDO29 and TE35 remain unconnected; no panel readback or TE interrupt is proposed |
| Unused inputs | DB17:0 pins11–28 low; RDX31 high; RGB inputs7–10 fixed at a valid rail, following controller pin rules |
| Logic/analog module supply | VDD36/37, GND38/39 |
| Separate backlight | LEDA40, LEDK41; no MCU pin drives these directly |
| No-connect | 1,42–45 |

The native mechanical drawing's **rear view** shows pin1 at its left and45
at its right. The contact-side/stiffener detail specifies0.30±0.05mm tail
thickness,0.50±0.05mm pitch and0.35±0.03mm contact width. It recommends
Molex0512964594. The manufacturer's selected product body identifies that
part as45 circuits,0.50mm pitch, bottom contact, right angle, front flip and
1.30mm mated height. Its exact sales drawing/contact orientation and actual
fixture remain unproved; a rear-view left/right is not an installed connector
pin-order rule. No PCB or adapter has been designed or selected.

Module VDD is2.5–3.3V, nominal3.0V, with15mA maximum logic current at3V.
VIH is at least0.7VDD and at mostVDD; VIL is at most0.3VDD. Thus a nominal
3.3V kit rail, without its worst-case tolerance and powered-off behavior,
does not establish supply or signal margin. Controller absolute input
limits of VDDI+0.3V are not normal operating permission aboveVDDI. The module
does not document an independent exposedVDDI supply or an input translator.

The backlight is a separate four-series-LED load:15mA typical,25mA maximum,
10.8–13.6V forward voltage at15mA. It requires controlled current;12V is not
a general voltage-source prescription. A separately controlled, default-off
backlight supply is only an H02 fixture requirement to evaluate, not a chosen
converter, available supply or completed H03 power approach. It does not solve
the logic-rail margin. The old PB6/GPIO9 backlight entries remain conditional
control allocations, not directLED connections or established blanking.

## Four-wire transfer and bounded rendering requirements

Controller pp33–35,40–42,63–64,112–116,129–130,136–138 and247 were read.
Writes are eight-bit, MSB first; the controller samples risingSCL and data
changes on fallingSCL. A proposed adapter must explicitly bind that edge
relationship, first-bit setup, idle clock and actual host phase configuration;
an SPI mode name alone is insufficient. The native timing figure begins with
SCL high. No effective U585/S3 mode/divider is selected here.

Both the raw module's native physical p12 and controller p247 specify a
100ns minimum write cycle,40ns minimum high/low phases,30ns data setup/hold,
10ns D/C setup/hold,40ns CS setup and a40ns CS hold row labelled for reads.
Controller p247 qualifies its table at25°C and specifies rise/fall at most15ns.
A **conditional ceiling of5MHz**, with at least40ns final CS hold also for
writes, leaves nominal half-cycle margin but does not prove the actual clock,
edges, load, voltage, temperature or the U585 final-clock erratum workaround.
The reciprocal10MHz is only the table's cycle limit, not an admitted fixture
rating. Do not use a driver which rounds above the selected ceiling.

The minimal render subset uses explicit MADCTL36h and COLMOD3Ah; a65h
COLMOD value preserves the ignored RGB field's18-bit setting and selects
DBI16-bit RGB565. A55h value also selects DBI16-bit but is not needed for an
unused RGB interface. Pixel transmission is high byte first, with R5/G6/B5
packing; MCU little-endian memory layout is not the wire format. MADCTL's
MY/MX/MV/BGR must agree with the physical orientation and test pattern.
Software reset preserves MADCTL/COLMOD fields; hardware defaults cannot be
assumed after every reset command.

CASET2Ah and PASET2Bh each take four bytes, start/end high byte first,
with ordered inclusive coordinates. WithMV=0 the screen bounds are0–239
and0–319. RAMWR2Ch restarts at the configured origin. One fullRGB565 image
is76,800pixels/153,600payload bytes; one row is480bytes. These are calculated
transfer sizes, not a selected linked RAM budget or peak-memory measurement.
At5MHz the payload alone takes at least245.76ms, before commands, software
and optical settling; this is not a maximum completion time.

CS high before a full byte rejects that partial byte. A partially received
multi-parameter command may already have changed earlier parameters; recovery
must restart the whole command. Pausing after complete bytes is supported,
but proposed pixel chunks must also end on complete RGB565 pixels.3Ch
continuation is unnecessary for the first subset: bounded row/window writes
can repeat explicit2Ah/2Bh/2Ch. Do not resume after a failed transfer using
an assumed retained address. Source FIFO/IRQ completion is not panel readback.

Render completion requires the expected bytes, actual host final-clock
completion and hold, no timeout/error/reset, and a screen generation tied to
the pending operation. This write-only interface cannot authenticate displayed
pixels; orientation, legibility, optical settling, failure blanking and stale
screen behavior remain explicit H02 checks. Local consent stays disabled until
the complete valid screen has been presented and controls have been released.

## Reset, sleep and startup are not erasure

01h software reset preserves GRAM and requires at least5ms before another
command; if issued inSleepOut,11h must wait120ms.10h sleep also retains memory,
requires5ms before another command and takes120ms to enter sleep.11h likewise
requires5ms before the next command and takes120ms to completeSleepOut.
Opposite sleep transitions require the stated120ms separation.28h blanks
output and29h restores it; neither clears GRAM. These are controller commands,
not direct external-backlight shutdown controls.

Hardware RESX requires at least10µs low,5ms command quiet time after release
and120ms before11h. When the previous sleep state is unknown, the proposed
policy must use the conservative120ms recovery interval before continuing.
If reset was unstable/high during power rise, a valid reset after both supplies
are present is required; a stable-low reset must remain low at least10µs after
the supplies are applied. Module p14 diagrams and controllerpp219–220,235
were read; the latter's power-down wording says reset 'released' while the
module diagram names its falling edge. Preserve that discrepancy; do not
derive a shorter shutdown interval from one ambiguous word.

Controllerp116 says hardware reset does not clear image memory, whilep233
calls the hardware-reset entry 'repair data'. Neither supplies a zeroization
guarantee. Power-on memory is random. The engineering requirement is to blank,
rewrite every pixel and explicitly restore format/orientation before enabling
review. Cancel consent on every failure/reset; a reset/off command does not
erase a displayed secret or establish that the visible screen is current.
No module-unpowered I/O tolerance or external reset/blanking circuit is proved.

## Module example correspondence and remaining C02 decision

The module example, physicalpp15–16, is not a qualified initialization recipe:

| Module example | Linked V100 correspondence |
| --- | --- |
|11h followed immediately byCBh |11h requires at least5ms before the next command and120ms to completeSleepOut; the shown example contains no delay |
|CBh five bytes ending34h,02h; CFh three bytes00h,81h,30h | Both commands **are documented** in listp89 and bodiespp197–199. CB's04h Vcore code is1.6V;02h AVDD code is5.8V. The latter conflicts with the at-most5.5V AVDD restrictions inpp181,240; defaults also disagree. No internal-rail safety inference follows |
|C0h26h,04h |p180 and listp86 define one parameter. The extra04h has no established meaning in that command |
|B6h0Ah,A2h |pp166–169 define four parameters; this partial write leaves later values inherited. A known reset/default cannot be omitted from the reasoning |
|21h described as inversion off |pp107–108 define21h as inversion on, already corrected in earlier findings |
|26h01h described as curve3 |p109 defines01h as the supported gamma2.2 curve1 |
|F2h02h |p206 defines disable3G with bit0=0 but its header incorrectly saysF6h; command bits/list agreeF2h |
|Extended B/C/F commands generally |p11 requiresEXTC high; p90 also says factory commands may be disabled before shipment, defaultNOP. The45-contact module map does not exposeEXTC or prove its internal/factory state |

An initial case-sensitive lookup missedCB/CF and led to a private message
suggesting absence. That reading is **withdrawn**: command-list/body reading
proves their presence. It is not a public-document access blocker.

The remaining external documentary decision is finite: resolve normal
logic-rail margin underC03/C09, and specify a compatible default-off backlight/
contact fixture. The factory/module startup/internal-power question remains
the named unsatisfied prerequisite under the coordinator allocation above.
A minimal standard-command-only sequence with factory defaults is a conditional
contract, **not established module operation**. Do not
silently discard required factory settings, copy the contradictory example,
or assert the linked controller alone qualifies the glass assembly. The exact
source blocker is reported to the coordinator; no further panel/controller
lead or manufacturer message is authorized by this finding. Independent clock,
USB, lifecycle and memory work can continue under the fixed checklist.

## Recorded reading and limits

Raw module: reread physicalpp1,3–9,15–16; pp10–14 extracted headings encountered.
Native physicalp4 mechanical andp12 four-wire/p14 reset-power visually reviewed.
Controller: selected cover/contents locators only; fulltextpp11,26,33–35,40–42,
63–64,86–90,92,102–104,106,109–116,129–130,136–138,157–158,166–170,180–185,
197–199,206,219–220,233–235,239–241,247. p65 unused parallel format andp238
NV-flow title encountered, not a used-mode/algorithm review. Extracted figure
text is not a new native controller-figure inspection. Other commands, RGB,
NV programming, backlightCABC and unused interfaces remain outside this subset.
The first combined output truncated afterp102; pp103–116 were reread in smaller
outputs before recording them. No whole manual review is claimed.

Breakout: product identity/features body; nativePDF physicalpp1–7 text including
the unused parallel heading; p4 drawing text encountered, not a native mechanical
audit; native physicalp5 pin/interface table visually inspected. Remaining
breakout controller/timing/example bodies intentionally unread after deferral.
Molex: selected [official product](https://www.molex.com/en-us/products/part-detail/512964594)
identity/physical/electrical body only, not
wholeHTML script or an obtained sales drawing. All originals, extractions and
native renders stay private. No hardware, build or measurement was performed.

The [breakout product](https://newhavendisplay.com/tft-breakout-module-with-2-4-inch-ips-tft-display/)
and its [Rev1 specification](https://newhavendisplay.com/content/specs/NHD-2.4-CTXP-BREAKOUT.pdf)
are separate registered sources from the
[raw DB module](https://newhavendisplay.com/content/specs/NHD-2.4-240320DB-CTXP.pdf)
and its [linked ILI9341V original](https://support.newhavendisplay.com/hc/en-us/article_attachments/26622995372055).
