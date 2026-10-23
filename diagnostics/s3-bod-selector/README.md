# S3 BOD selector — compile-only source checkpoint

## Portable compile gate, 23 October 2026

Run from a clean Linux x86_64 checkout with Python>=3.11, Git and an available
bubblewrap supporting the mandatory user/network namespaces:

```sh
make s3-bod-compile S3_BOD_WORK_DIR=/tmp/s3-bod-new-run S3_BOD_CACHE_DIR=/tmp/s3-bod-assets
```

The work directory must not exist. The cache may contain only assets matching
[the checked-in exact input hashes](tools/inputs.json); mismatches or interrupted
acquisitions fail. Ordinary official downloads occur only during bootstrap.
Build/configure run in a distinct network namespace (only lo, zero routes), with
fresh `/dev/null`, unchanged UID/GID, zero permitted/effective capabilities,
NoNewPrivs1 and enforced read-only SDK/tools/project mounts. Unsupported/denied
isolation fails; there is no skip, sysctl, AppArmor or privilege workaround.
The recorded actual bubblewrap is a host prerequisite, not part of a binary
reproducibility guarantee. Only the tested host profile is evidenced.

The target prepares exact SDKfff and its three actually consumed Gitlinks,
Xtensa15.2.0_20251204, Ninja1.12.1, CMake3.31.6 and CPython3.12.15 from authenticated
publisher archives. Python63 pins use62 publisher wheels and esptool5.6's exact
publisher sdist, built offline without isolation using pinned setuptools84.2.1;
its derived wheel is identified separately. Installed library bytes are compared
to the actual wheel bodies. Installed RECORD is not publisher authentication.

**Local corrective Python compatibility profile:** the original Espressif
constraints8fd still require cryptography<49. The admitted one-line local patch
pins50.0.0, with every other line and62 versions fixed. The original strict SDK
checker must reject50, the same checker with the explicit local constraints and
`pip check` must pass. The old48.0.1 profile is not installed: its primary metadata
reports advisories, including PKCS7 fixed50; two affected-version tables disagree
with PyPI48.0.1 and that discrepancy remains unresolved. This is not a claim of
upstream support, complete dependency safety, secure signing or provisioning.
Advisory metadata is a dated snapshot, not a fresh mandatory security audit.

Both literal selectors0/1 must produce real app and bootloader ELF/bin/map sets;
selector2 must be rejected at the real CMake guard before SDK/compiler entry.
The gate checks effective security/target flags, all0/1 generated config values,
actual writer/app/startup disassembly and linked init/ISR exclusion. Actual
compiler dependencies for every object, Ninja execution logs, configure/Kconfig
inputs, link-map LOADs and observed Python imports are bound to SDK Git blobs,
frozen project inputs, publisher tool/wheel bytes or separately named generated
producers. These records are not a syscall-complete file-read trace.

`make ci` preserves the original43 controls. `make s3-bod-test` adds finite gate
negative controls; the separate workflow compile job runs the full target and
retains `evidence.tar.gz` (source/raw/config/closure/binaries), including on failure.
The first cold mode0 [checkpoint](../../docs/restart/H01/checks/s3-bod-portable-2026-10-23/early-cold/summary.json)
remains historical; current final-source results/review must be read separately.
Original component [proof](../../docs/restart/H01/checks/s3-bod-mode0-first-build-2026-10-23/README.md)
and distinct review3fb remain bound to their actual sources.

No firmware or device execution occurs. The source performs a real full-word
register write if later run: compile intent is not physical bit preservation.
Disabling SDK `esp_brownout_init`/optional ISR does not disable ROM/hardware;
registered startup wrapper and flash brownout hooks remain. TRM polarity stays
unresolved, no host/Board/H01 criterion is closed, and no binary reproducibility,
boot/reset/safety, threshold/arming, keys, flash/fuse or production qualification
is inferred. Exact sample/startup/strap/rail/reset/operator and independent bench
admission remain required.

## Historical blocked checkpoint2680

The following observations and unexecuted command forms describe the original
blocked source checkpoint; its Git identity and original proof are preserved.

Root admission: `9e9aea04e0c71e089b1fc8af8d488effe8ba3134`.
The independent [expectations](../../docs/restart/H01/s3-bod-build-expectations.json)
were committed before this C source. ESP-IDF must be exactly
`fff9895c82d744c7237be8847347bdd1b07c6643`; selectors other than literal0/1
are rejected by the proposed CMake entrypoint before importing the SDK project.

**Blocked before C compilation/link.** Two actual selector0 configure attempts
failed while the pinned SDK initialized unrelated Gitlinks globally, before
`MINIMAL_BUILD` can narrow the components. The admitted single shallow serial
prefetch also failed with TCP resets. Original logs, SDK states and exact pins
are in the [blocker result](../../docs/restart/H01/checks/s3-bod-build-blocker-2026-10-23/result.json).
No ELF/map/application binary, selector1 build, invalid-selector execution or
automated diagnostic CI target is claimed. No skip flag or version substitution
was used; no retry loop follows the failed batch. Existing43 tests/workflow
remain unchanged, with their original source-specific evidence.

Once exact SDK inputs are available and the failed acquisition is dispositioned,
the admitted direct build forms are (not additional executed commands here):

```sh
idf.py -C diagnostics/s3-bod-selector -B build/s3-bod-0 -DIDF_TARGET=esp32s3 -DBOD_RST_SEL=0 build
idf.py -C diagnostics/s3-bod-selector -B build/s3-bod-1 -DIDF_TARGET=esp32s3 -DBOD_RST_SEL=1 build
```

The source contains a real volatile masked register writer, not read-only
firmware. It intends to change selector bit27 in a captured word and records
raw context/before/after if later executed. Bit31 is RO, bit29 is WO, and an
observed1 on that WO field refuses the write. These facts do not prove neutral
effects on other physical fields, atomicity or a safe voltage/reset state.

The defaults request exclusion of SDK brownout init/ISR; effective generated
configuration and linked exclusion remain unproved because configure stopped.
The optional SDK ISR performs a software reset and is not a polarity witness.
ROM/hardware state is unknown. `not_armed_by_this_probe` means no arming
configuration is requested by this probe, not disabled hardware or safe firmware.
The GPIO46 marker/00-or11 UART print guard and contradictory TRM hypotheses
remain in the existing [contract](../../docs/restart/H01/system-runtime-contract.md).

No flash/erase/fuse/monitor/register execution, energizing, production identity,
threshold/stimulus/alternate-mode selection or physical use is admitted. Exact
sample/ROM/startup/security/strap loads/rails/CHIP_PU/reset controls/instruments/
operator and independent bench review remain mandatory. No host, polarity,
Board, H01 criterion, target or release is qualified by these sources.
