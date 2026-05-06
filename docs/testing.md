# Testing

## Current Baseline

```sh
make ci
```

## Required Tests

- BOM validation.
- File presence and naming checks.
- KiCad ERC/DRC when KiCad files exist and tooling is available.
- Hardware validation reports for physical builds.

Manual hardware tests must include exact parts, firmware commit, procedure,
result, photos or logs where useful, and known limitations.

