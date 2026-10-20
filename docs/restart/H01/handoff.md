# H01 current-manual candidate handoff

**H01 remains incomplete; no host or component is admitted.** The current
RM0456 Rev7 original retrieval is closed. Remaining current body/configuration
review still blocks completion; the mandatory U5/S3 comparison is retained.

The substantive source commit is
`4d50d155c994e8e770d2b868c371cc04b646ad35` on `restart/h01-manuals`, hardware
baseline `340697d6713a671e9e01b0dc874ec999ab071601`. Canonical input remains
`7b5553685dac56029a4379be12054154b6b5e0b5`; approved brief remains
`e10dd2426146e0aa3bbcf04af6a9b1bb59f7e868`. No canonical graph was edited.

`result.json` binds **26 source artifacts**, including the unchanged brief/input,
new analysis and both preserved reviews. Its SHA256 is
`5c10be2874d6eb6eb194f1c71259a95f3197fb7aef79b085064ee8a601b7836e`.
The result and verification logs are committed separately from the substantive
source. The handoff commit is not self-described as already independently reviewed.

## Review provenance

The old `19362fc`/`d5d7530` request-changes review remains in
`independent-review/`, original `5186b7207fa397ceb4cd237d710d8adc163c6eb0`.
The material ANALOG-160/TOUCH-100/documentary-signoff correction remains separate
at `16a7d4bfaa9b144581ae06fb67424718ffb10482`.

The distinct follow-up review of `6f95cc298c5a8108d5c0bdaedfd53e7b81b130ed`
is preserved in `independent-review-followup/`, original
`2f9ea3a18d8fb18e3fbaa8f58b6272102f83b9c2`, imported by `88a8c09` **before**
new source changes. Its limited PASS closes R1/R2/R3 wording and checked bounded
claims at that candidate, while explicitly leaving H01 incomplete. All eleven
files across both reviews were independently compared byte for byte to their
original review commits. Neither report was rewritten.

## New substantive evidence

Read [current-manual-notes.md](current-manual-notes.md) with the exact source
ranges in [manual-register.json](manual-register.json), rather than treating the
register's ninety entries as ninety fully reviewed manuals.

- RM0456 **Rev7,30 March2026,3651 pages** native original independently rehashed
  to `6edaaaae0c5d57c58ffc3a576d44e7b62e8d9cd0e495e8f61bab688226fc327c`.
  Read current masters/reset/selected clock text, all RNG chapter functional and
  register text, selected OTG_FS device/FIFO/reset/interrupt text and revision
  history. The changed-chapter list does not establish the full relevant delta.
- Native DS13086Rev10, ES0499Rev12, DS14102Rev5, ES0595Rev4 and UM3223Rev2
  now have original hashes. ES0499 core/system bodies pp.7–16 were read with
  X/W/U applicability. Current RM supports `GOTGCTL.CURMOD`, closing that one
  earlier USB-name question; other USB erratum wording remains separate.
- AN4230 **Rev14 July2026**, plus NIST-hosted E11v1.1/E116v1.2 public-use
  documents, establish distinct entropy configuration evidence. Their bit5 CED
  prose conflicts with active-low CED in the current RM. Reset/default values,
  ordinary-kit statistics and a library trait do not establish configuration or
  certification reuse. Exact source scope and the conflict are recorded.
- Complete pinned Embassy RNG source was read. NSCR configuration, custom-policy
  preservation, bounded waits and the actual fallible adapter need explicit
  correspondence. Bounded retries do not bound polling; async filling can call
  blocking recovery. This is a candidate source finding, not a built target defect.
- The S3 build must exclude `CONFIG_ESP_BRINGUP_BYPASS_RANDOM_SETTING`. The
  pinned registry-linked TinyUSB candidate now has an actual device-path trace:
  initialization, FIFO allocation, endpoint disable and bus-reset IRQ handling
  reach unbounded waits. Exact dependency lock/configuration/recovery and the
  public TRM§32.5 normative IP boundary remain open.
- Direct UM3223 power/clock/input/RGB/expansion reading and native G9 outline
  inspection close earlier access/visibility gaps. DK2 uses50-pin RGB; its PC13
  button and LSE crystal intersect ES0595§2.2.1. LQFP144/UFBGA144 mechanical
  differences are read, but pad/AF/rail/GTZC/driver/license allocation remains.
  No additional G9 bench port, custom footprint or wiring was approved.

The new current source material is primary and privately preserved. No original
manufacturer PDF, private history, production secret or generated CAD was added
to the public repository.

## Verification and its limits

At the exact source commit, existing `make ci` passed in the owned isolated
`h01-ci/hardware` worktree:43 tests, compile/verification and hardware data
validation. The earlier basename-sensitive author-worktree failure remains
recorded; the verifier was not weakened. No target firmware was built.

`checks/current-manual-integrity.json` records26 exact source bindings,75 unchanged
old source identities,6 previously null original hashes now resolved,9 new
source identities and15 matching retained originals. Approved brief/input hashes
and all source references were checked. These checks prove record consistency,
not correct electronics, complete manual reading or qualified entropy.

## Next required work

1. Complete the current U585 used security/boot/update/owner/flash/options,
   GTZC/RAM/ECC/GPIO/DMA/PWR and remaining USB/SPI/I2C/watchdog/crypto paths.
   Bind exact proposed OPN/package, allowed silicon/ROM revision, clock,
   electrical/AF and driver configuration. No new retrieval attempt is needed
   for already recovered manuals.
2. Finish S3 proposed kit/module electrical/schematic match, selected
   GPIO/SPI transaction/error/driver and boot/update/flash/clear policy. Resolve
   actual device stack/configuration, descriptors and a bounded error policy.
   Read only the IP semantics required by that proposal; unused host/DMA paths
   need not expand the probe. Headers do not replace missing normative semantics.
3. Finish G9 document-level pad/AF/rail/GTZC/cache/master, graphics software/license
   and workload conditions, including the PC13/LSE choice. The native outline
   and DK2 reference do not select a part or require a third port.
4. Preserve independent selected-SE API/errata/update/advisory gates and remaining
   USB normative/power/panel/expansion work. All sixteen physical resource entries
   remain unknown. A received unit is required before H02 execution, not before
   completing an H01 documentary proposal.
5. Obtain a distinct affected review of this exact source and handoff. Focus on
   actual current-manual/driver substance and implications, not schema counts or
   transferring the earlier limited PASS to new content.

No measurement, purchase, fabrication, fuse operation, secret provisioning or
whole-H01 acceptance occurred. The author worktree is frozen for that review.
