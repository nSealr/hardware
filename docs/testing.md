# Testing

## Current Baseline

```sh
make ci
```

The baseline runs repository verification, unit tests for hardware validators,
bytecode compilation, and validation of the reference requirements and BOM.

## Implemented Tests

- Reference requirements validation.
- Reference BOM validation.
- Negative requirements test for missing mandatory interfaces.

## Required Tests

- File presence and naming checks.
- KiCad ERC/DRC when KiCad files exist and tooling is available.
- Hardware validation reports for physical builds.

Manual hardware tests must include exact parts, firmware commit, procedure,
result, photos or logs where useful, and known limitations.
