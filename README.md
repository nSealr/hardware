# nSealr Hardware

Open hardware reference designs, BOMs, validation contracts, and production
notes for nSealr signer and secure-device hardware.

Current requirements and task state live in the canonical
[nSealr restart plan](https://github.com/nSealr/nsealr/tree/main/docs/restart).
The accepted direction separates a general-purpose Board/SDK from the Nostr
Signer. The SDK has no Nostr dependency; its initial model is one trusted
firmware image.

## Current investigation

The four Signer profiles are connected commercial ESP32 without an SE, offline
Pi, offline ESP32-P4, and an initially connected custom Board. They have separate
threat and validation boundaries; these names do not establish a security rank.

The [H01 manual register](docs/restart/H01/manual-register.md),
[bounded comparison](docs/restart/H01/option-comparison.md) and
[review gates](docs/restart/H01/review-coverage.md) record current hardware
research. H01 remains incomplete: no host probe or component selection is
approved by this record, and the current U5 reference-manual gap is explicit.
The [probe plan](docs/restart/H01/probe-plan.md) separates documentation from
future measurements and selected-SE gates.

Existing kit requirements, reports and BOMs remain historical investigation
inputs. Their older five-family or ESP32-S3 QR terminology does not define the
accepted portfolio or select the replacement Board's components.

## Archived Hardware

The legacy TROPIC01 Universal Secure Device board has been retired from this
repository. Its complete design — KiCad project, BOM, production contracts,
docs, and board-specific scripts — was archived with full git history to the
private, read-only repository `nSealr/hardware-legacy-tropic01-universal`. It is
historical evidence. The replacement Board follows the canonical restart
requirements and future hardware gates; the archived design is not its BOM.

## Quality Baseline

Run the repository verification loop with:

```sh
make ci
```

or the hardware validator directly:

```sh
python3 scripts/validate_hardware.py
python3 -m unittest tests.test_validate_hardware -v
```

## Layout

- `pcb/`: requirements and KiCad board design files.
- `kits/`: off-the-shelf kit requirements before custom PCB work.
- `enclosures/`: 3D case designs and mechanical notes.
- `bom/`: component lists and sourcing notes.
- `reports/`: manual hardware validation reports.
- `templates/`: validated report templates for future manual acceptance runs.
- `docs/`: architecture, testing, assembly, and security notes.

## License

Hardware design files, PCB sources, BOMs, enclosure files, and assembly
artifacts are released under CERN-OHL-P-2.0 unless a file says otherwise.
