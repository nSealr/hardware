# C04 — selected owner/update source pre-read

Reviewer `/root`, author `/root/h01_sol`, exact source
`aa383dfd253171f0d06325aeab1d2a6310cdce39`. This is a bounded source reading
while C09/C10 are being completed, **not final H01 review, host admission,
implementation acceptance or physical qualification**. Only unchanged selected
C04/source bindings may be reused later; other areas remain unreviewed here.

The fixed flash allocations are disjoint and arithmetically consistent. U585's
secure-entry field, 8KiB pages, protected 256KiB boot, two journal pages and
272KiB hidden range agree with the selected current RM fields. Each app reserves
640KiB. The inclusive protection tables support the proposal; the manual's HDP
numerical example is inconsistent and was correctly not used. Root/erase/hide
and recovery remain procedures to implement and qualify, not completed effects.

The S3 paper allocation reserves two 3MiB app slots inside 8MiB; this proves no
linked fit or padding. Selected current TRM fields support the 16-bit floor and
the distinct two XTS and three public-digest purposes. The pinned SDK bodies
independently confirm ignored errors in the version read/update helpers and
uncapped damaged-read retries. The contract correctly retains a complete bounded,
error-preserving path/readback gate. No helper was executed; utility/HAL/caller
effects and actual counter/fault behavior remain unproved.

Two precise distinctions must survive later executable procedures. U585 OEM
lock fields are derived read-only status observations after option loading.
S3 aggressive revocation is specified for failed signature verification after
the structural/digest checks; a bad block or image digest alone is excluded.
Its finite roots and potential permanent retirement are real maintenance costs,
not general owner re-enrollment. Neither paragraph supplies a provisioning
recipe or authorization to perform it.

No blocking contradiction was found in this selected correspondence. Five
original source identities and two output identities were verified; exact
reading scopes and limits are in [readings.json](readings.json). Original bodies
remain in their existing private cache. No broad repeat reading, new verifier,
CI, target build, fuse/flash operation or source finding suppression occurred.
