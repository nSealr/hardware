# S3 BOD selector — compile-only source checkpoint

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
