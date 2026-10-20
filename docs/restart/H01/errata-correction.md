# Material correction to the first H01 source candidate

The distinct review of source `19362fc9a12bed43070c56642b4a932f1bc6a545`
(handoff `d5d75306a082215453d329e31ca9c11d6effa80d`) found two incorrect
mitigation summaries. Those commits remain immutable review evidence; the
current [pin/errata ledger](pin-errata-ledger.json) corrects the affected rows.
The issue is tracked in
[issue20's review blocker](https://github.com/nSealr/nsealr/issues/20#issuecomment-6253470640).

The author re-read the preserved original
[ESP32-S3 errata v1.3](https://documentation.espressif.com/esp-chip-errata/en/latest/esp32s3/esp-chip-errata-en-master-esp32s3.pdf),
SHA256 `8f349bdd0b4e9bca24e49d777ac3b416ff2d2c48253a49653162e84f4b484500`,
628997 bytes. The original hash was recomputed before this correction.

- **E-S3-ANALOG160, §3.3 printed p.7:** `BIAS_SLEEP=0 AND PD_CUR=1` is the
  damaging condition, not the mitigation. The documentation requires avoiding
  that conjunction in sleep software. The cited IDF workaround disables it.
- **E-S3-TOUCH100, §3.7 printed p.10:** skipping the first two
  `TOUCH_SCAN_DONE_INT` interrupts is only the first step; the workaround then
  disables and stops using those interrupts. Discarding two samples alone does
  not express the required behavior.

These are documentation corrections, not instructions to exercise the damaging
condition or write hardware registers. No physical operation, qualified driver,
host admission, component choice or completed H01 acceptance follows. The
selected sleep/touch implementation still needs source correspondence, and the
fresh affected candidate needs distinct review.

H01's proposal requirements are also clarified: exact proposed part/package,
allowed revision and configuration can be reviewed before hardware is owned.
H02 must identify the actual received unit before a probe. This distinction does
not waive missing current manuals or the mandatory U5/S3 comparison.
