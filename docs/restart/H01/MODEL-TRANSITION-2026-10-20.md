# H01 model-transition handoff — 20 October 2026

The maintainer requested the next safe checkpoint to transfer ongoing work to
`gpt-6.1-sol` with `xhigh` reasoning. This is **not a project pause or acceptance**.
The explicit 20 October resumption remains in force. H01 is incomplete; no
host, panel, component, wiring or physical probe is admitted.

Source checkpoint: `edfa379ca9ffd40c58a11698beb8b4a2f9807288`, branch
`restart/h01-manuals`, worktree
`/home/tux/nsealr/.restart-tools/goal/h01`. Its predecessor is
`40cdb6c519285ab81922b382440ef6c02a6fc89a`.
This handoff is a separate metadata commit; the containing commit identifies
its exact version without a recursive hash. The coordinator receives the exact
pushed HEAD. Canonical/hardware mains and the A02 source freeze remain unchanged.

## Preserved increment

[resume-source-notes.md](resume-source-notes.md) is the compact source table
for H01-C36 through H01-C41, with scope, source locators, implications and limits.
The register, claims, contradiction ledger and coverage references are updated.
There are still 124 document entries; that count is not completed reading.

Fresh reading by `/root/h01_resume`:

- RM0456 Rev7 pp374–380 before the ICACHE register-map summary; pp382–399
  before the DCACHE register-map summary; pp622–641 before the GPIO register-map
  summary; pp2562–2574 IWDG functional/register body. Encountered text/tables were
  read; the manual diagrams were not newly visually reviewed. Prior pp540–547
  RCC reset-register text was reread.
- UM2839 Rev4 pp21–29 extracted text.
- MB1551-U585AI-D01 native schematic sheets4,7,13,14 visually inspected;
  sheet8 rechecked. Four new render hashes are in the register.

Material findings: U585 DCACHE1 bypasses internal SRAM; invalidation is not
established data erasure; G9 GPU2D/DCACHE2 is specifically nonsecure without
DCACHE2 TrustZone; GPIO RAZ/analog zero is not an authenticated input sample;
HSLV must stay disabled on the proposed 3.3 V rails; IWDG early-wake writes reload
the counter. The current DCACHE TAG text's `CACHEINV=0` conflicts with the
explicit command/register definition and is retained as a contradiction.

Kit startup remains substantive work. PA7/PB0 use the fitted SB10/SB13 paths,
but complete target-net/ROM-loader correspondence is still open. The STMod
selector pull-ups R10/R11 are DNF despite the UART-default label. Wi-Fi enable
has no drawn external hold-low; Bluetooth's separate supply switch does not
prove unpowered-I/O safety. JP3 measures the target MCU rail rather than all kit
loads. These findings do not justify a new convenient kit or display substitution.

The private root remains
`/home/tux/nsealr/.restart-tools/goal/h01-private`. The new
`resume-2026-10-20-reading.json` binds selected coverage and render hashes.
`resume_source_increment.py` is the private authoring helper. It is idempotent
for its exact existing records, but there is no need to rerun it to continue.
Do not run the older non-idempotent `record_configuration_checkpoint.py`.
All originals, extractions and native renders remain private.

## Checks and continuing review limits

At the source checkpoint, JSON parsing, unique document/claim/ledger IDs,
claim-to-document references, all three affected original hashes and byte
lengths, four new render hashes, and `git diff --check` passed. No source
inventory sweep, target build, physical test or whole-repository CI was repeated
for this documentary checkpoint. Existing earlier CI evidence retains its exact
historical scope; it is not a test of these new hardware conclusions.

The old `result.json` / `handoff.md` remain the historical
`4d50d15` / `e39015a` bindings. The latest distinct review
`9d5ed3baf936157a26b55bf42e51da4ce6d240c2` still covers only that older candidate.
This source increment and the eventual two complete documentary configurations
require distinct substantive review. The six signoff rows remain incomplete.

## Exact next work

Continue from this coverage; do not reread the entire solved source inventory.
The next bounded source work is the current U585 peripheral/clock/ownership
manifest: complete selected GTZC lock and RCC clock-enable correspondence;
remaining SPI1, I2C2, USB and interrupt/timer text; reconcile each used and
excluded master/reset bit to the exact U585 device. Current reset registers
default to zero, not asserted reset; reserved/absent bits cannot be filled with
an all-ones mask. Bind the IWDG feed/startup/deadline policy before using it as a
recovery argument for a candidate blocking USB or RNG loop.

The two proposed host records still need full lifecycle, update/rollback,
entropy/crypto adapter, power/rail and driver correspondence. Complete the
remaining native kit sheets and exact mux/radio shutdown/injection evidence;
do not silently describe a powered, unreviewed radio as disabled. No new
market sweep, third bench port or panel selection is authorized by this transfer.

Retain the preceding pause handoff's other exact outstanding work: S3 public
USB-IP documentation boundary and real J4 disconnect/power proposal; native
USB/ECN body coverage; the bounded Newhaven panel/controller/breakout electrical
review; G9 ZJ pad/rail/master/GTZC/driver comparison and PC13/LSE choice.
Retrieved documents remain unread except for their recorded ranges.

The manufacturer-original retrievals are available. Physical-resource identity
and measurements, selected-SE access/service gates, purchase/fabrication,
production keys and irreversible fuses remain outside H01.

No fetch, render, parser, test, probe, subagent or scheduled H01 task remains
running at this transfer. No tool session handle needs resumption. The author
has stopped starting new research and will end its turn after push and reporting
the exact receipt to the coordinator.
