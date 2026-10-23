# Affected review of the F1 default correction

**PASS for the F1 source/config amendment only, no new findings.** Reviewer
`/root/sdk_dependency_probe` is distinct from the diagnostic author. Reviewed
`e9849a8ae2833b96e0d4ce92978ee48e2087f30c`, tree
`3c084479c57b2977eee37a39d1cbd3d8bb171c71`, against parent
`73d574cad6f45e10ab6d34809ea7b5fe3355ec3f`. This resolves F1 for the amended
source, without rewriting the original CHANGES_REQUESTED review on the old input.

The exact delta is two modifications and one new amendment record. The default
change removes only `# CONFIG_SECURE_ENABLE_TEE is not set`; its new SHA256 is
`d3ea9fc5e50ec3f831225e1d9878aefca74a58a0474f43d51b6bdc61c8d8063c`.
The top-level CMake input, main component CMake input and `main.c` remain
byte-identical to `11047b805039e01dbb73e7c08d4b6a8016090fcd`. All 325 other
existing parent postimages retain their modes/blobs.

The current expectation correctly removes TEE=n from required settings and
records it as inapplicable to this S3 configuration. Its role now identifies
the original independent expectation plus this limited amendment; it does not
pretend the amended file predates the diagnostic. All other expectation fields
remain exact. The pinned `fff9895c82d744c7237be8847347bdd1b07c6643`
`components/esp_tee/Kconfig.projbuild:1-7` bytes, blob and SHA256 match the
previous source review: the TEE menu lists C6/H2/C5/C61, excluding S3. Neither
absence of the default nor the old unknown-symbol warning proves disablement
or a hardware security property.

The original default is preserved at11047/73d. The original independent
expectation remains atdb1a2fc8/73d, SHA256
`aca0dc8043669520606835efd48c43decd5ce4348f0201c65a219cf3bca1e8a6`.
The actual unknown-symbol warning remains unchanged at73d's
`configure.stderr.log:8`, SHA256
`5778d0d1acedc3913c71db0c89fc52a6819c253eb3decc0288ee92fdde690703`.
The original F1 review remains qualified by commitb6dba74 and its original
CHANGES_REQUESTED verdict. This affected review is nested separately so both
receipts can be retained together.

The 18 vendor-source, four old-input and 49 blocker bindings retain their prior
historical roles. The old input hashes and configure output are not current
evidence for the changed default. There is **no configure on the amended input**
and no transferred bootloader, generated-header, dependency, compile/link,
variant or disassembly proof. The parent's next-experiment proposal remains
unexecuted and subject to its own admission. No campaign, fetch, configure,
build, test, CI, device operation or author-source edit occurred here.

All prior register/RMW/ROM-state limits and both opposing TRM reset hypotheses
remain unchanged and UNSATISFIED, with selected polarity null. No physical
safety, Board, H01 or release criterion is qualified. This source-only review
does not grant build/device admission. Future final candidates must execute
their normal mandatory checks and CI; the review branch's skip-ci commit marker
is confined to this unintegrated review and must not propagate to a final
candidate to suppress those gates. [review.json](review.json) binds the exact
three changed files and retained source receipts.
