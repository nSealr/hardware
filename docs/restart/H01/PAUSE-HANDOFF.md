# H01 explicit pause handoff — 2026-10-18

**Paused at the user's explicit request. H01 remains incomplete. Resume only
after an explicit root/user instruction.** No host configuration, component,
bench procedure or hardware is admitted. No main branch or canonical graph was
changed, and no further research or testing was started during checkpointing.

## Exact checkpoint and disposition

- Repository: `nSealr/hardware`; branch `restart/h01-manuals`.
- Owned worktree: `/home/tux/nsealr/.restart-tools/goal/h01`.
- Clean HEAD when pause arrived:
  `c8a933f3d11e73b2c6678bf33c915b50985dffff`.
- Preserved source HEAD:
  `136d9ccea3422fa47e530b41c2fb2720a2a090a4`.
  This commits the already-read VIQ package correction, selected current-manual
  coverage, three existing retrieval records and `pause-reading-notes.md`.
- This handoff and `pause-state.json` form a separate metadata commit atop that
  exact source HEAD. Its exact pushed hash is reported to the coordinator and
  recorded privately in `h01-private/pause-git-receipt.json`; the Git commit
  containing this file identifies it without a recursive self-hash.
- Only those metadata files remained to commit when this handoff was written.
  No existing source change, private original or reading note was discarded.
  The author will leave the owned worktree clean after committing/pushing them.

`pause-state.json` pins the source artifacts and selected private reading
receipts. The existing `result.json` and `handoff.md` deliberately remain the
historical `4d50d15` source / `e39015a` handoff evidence; their artifact hashes
are not a manifest for the newer checkpoint. Do not mistake them for current
acceptance. The source count of 124 is an inventory, not 124 fully read manuals.

The accepted brief remains `e10dd2426146e0aa3bbcf04af6a9b1bb59f7e868`;
canonical input remains `7b5553685dac56029a4379be12054154b6b5e0b5` and hardware
baseline `340697d6713a671e9e01b0dc874ec999ab071601`. The coordinator's A02 source
freeze remains in force. This branch does not change that freeze.

## Preserved private evidence

The private root is `/home/tux/nsealr/.restart-tools/goal/h01-private`.
`originals/`, `text/` and `drawings/` contain manufacturer originals, native
extractions and rendered drawings. They are not in public Git history.

`pause-2026-10-18-reading.json` is the latest private note, SHA256
`8919e0cb92dde249ccb47f04a9b63e06af68085a6b5f081484bc568990cca65f`.
It corrects, without overwriting, the misleading SMPS/p100 interpretation in
`after-c8a933f-reading.json` (SHA256
`731c97a62ef8e425db87b5d398455a0389b455c082cc903400d7623245edf4e9`).
The correctly viewed native p99 drawing is
`drawings/u585-lqfp100-smps-actual.png`, SHA256
`56bde0507a434f90f3f45957d54dacb8491bce1af1edefd5b102d35946962bf4`.
The old `u585-lqfp100q.png` filename does **not** identify an SMPS pinout.

`retrieval-extra-bounded.json` binds the Newhaven module, linked ILI9341V and
TCPP03 originals. The latter was retrieved only. The Newhaven breakout remains
a partially read official web lead: no breakout specification or schematic
has been fetched. `configuration-reading-progress.json` is earlier context,
not the latest reading or pin decision. `usb-extracted-members.json` binds the
already available Type-C 2.5 and USB 2.0/ECN originals; each register entry states
the actual body coverage. Do not rerun the non-idempotent
`record_configuration_checkpoint.py` merely to resume.

The current RM0456 Rev7 original is also preserved at the coordinator's private
`/home/tux/nsealr/.restart-tools/goal/manual-retrieval-root/curl-experiment/run-02/rm0456.pdf`,
SHA256 `6edaaaae0c5d57c58ffc3a576d44e7b62e8d9cd0e495e8f61bab688226fc327c`,
with adjacent `rm0456.txt` and retrieval metadata. Current-original retrieval
is closed; unfinished applicable reading is not an access failure.

## Reviews and completion gates still open

The original request-changes review and two follow-up reviews remain byte-exact
under their respective `independent-review*` directories. The latest distinct
review is `9d5ed3baf936157a26b55bf42e51da4ce6d240c2`, imported in `5fae213`.
It reviewed the exact old `e39015a` candidate; its CM-1 wording correction was
committed separately in `90aa59d`. It does not review the new configuration,
package or display findings. A distinct substantive source/manual review of
the eventual exact final candidate is still required.

The six host sign-off rows in `review-coverage.md` remain incomplete. The task
requires two complete proposed documentary configurations, U585 and ESP32-S3,
plus a reasoned U5G9 comparison. Proposed OPN/module/package/revision and
configuration identity belong to H01; received unit identity and measurements
belong to H02. Already owning a kit is not an H01 prerequisite, and admitting
zero hosts cannot pass H01.

The principal remaining work is concrete:

- Finish U585 current GTZC locks, cache/register, GPIO/interrupt, used SPI/I2C,
  watchdog, clock/reset and USB body/errata correspondence. Turn excluded
  DMA/crypto/external-memory blocks into a justified reset/clock/ownership
  manifest. The completed ICACHE functional reading ended at p373; do not claim
  the register continuation or DCACHE chapter was read.
- Close exact kit, header and panel/fixture electrical and reset/load evidence.
  The VIQ PC4/PC5 correction is committed, but PA7/PB0's remaining branch and
  boot implications are not waived. U585 kit power/USB/radio sheets and TCPP03
  body remain useful available sources. No display module is selected.
- Define both hosts' developer, owner-secured and product-qualified roots,
  download/debug/rollback/reuse/reset retention and erasure policy. Pin the
  entropy and software-crypto configuration, bounded timeout/recovery and
  complete partial-buffer/consent invalidation behavior. Source helpers with
  unbounded polling or fixed-pattern RNG bring-up options are not a solution.
- Resolve the used S3 SPI/XTS/USB questions with exact evidence or a justified
  exclusion. Public TRM §32.5 p1242 marks the comprehensive USB IP document
  boundary; headers establish software configuration, not missing normative
  register semantics or DMA isolation. Do not expand unused IP without need.
- Complete applicable USB base/ECN and current controller body reading. Existing
  USB originals are available privately. The S3 kit has no established native
  USB VBUS-sense path under arbitrary external power; power topology must be
  explicit. Current power rules do not grant a generic 500 mA preconfiguration
  allowance.
- Finish the U5G9ZJ package/rail/AF/display-memory/cache/master/GTZC/driver-license
  comparison and the DK2 PC13/LSE conflict, then make a reasoned defer/promote
  comparison decision. No third bench port follows from that comparison.

SE051 restricted mandatory documents, the TROPIC advisory without an established
qualified fix, and actual selected-SE capabilities remain future hard service
gates. They do not justify abandoning otherwise available host reading. All
physical resources/measurements, component selection, H02/H02S and H04 gates
remain outside this paused documentary work.

## Process state and next resume action

No H01 fetch, render, parser, probe, child agent or scheduled automation was
active in the pause process snapshot. No download or file write needed to be
aborted. The final completed research action was the selected ICACHE functional
reading; no continuation was launched after the pause. Unrelated user services
and unrelated repository processes were left untouched. No tests or CI were
started during checkpointing; only the checkpoint diff and Git bookkeeping
were inspected.

After explicit resumption, first verify the branch/HEAD and pinned private
notes, then continue the two host configurations from these exact remaining
sections and fixture identities. Reconcile the new register notes with the
six-row matrix before requesting final review; do not run the old result
manifest as if it covered this checkpoint or repeat the unchanged source
inventory. The bounded Newhaven breakout can be evaluated only within the
already authorized display lead, with actual source correspondence. No new
market sweep, production driver, purchase, fuse operation or hardware work is
authorized by this handoff.
