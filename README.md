# nSealr Hardware

Open hardware reference designs, BOMs, validation contracts, and production
notes for the programmable nSealr Board and independently qualified Signer kits.

The current [product contract](https://github.com/nSealr/nsealr/blob/main/docs/product/contract.md),
[Board realization requirements](https://github.com/nSealr/nsealr/blob/main/docs/restart/pcb-development.md#product-choice-before-h04)
and [task graph](https://github.com/nSealr/nsealr/blob/main/plan/work-items.json)
define direction and actual acceptance. The Board has standalone developer value;
Nostr Signer is one application. Its [Board SDK](https://github.com/nSealr/board-sdk)
is independent of Nostr. Historical specs and reference files below do not
announce supported hardware or override the current contract.

## Reference artifacts

- ESP32-S3 USB/NIP-46 signer reference requirements.
- Historical ESP32-S3 stateless QR vault requirements and display/camera leads;
  these are not admission of a current offline profile.
- Raspberry/Pi stateless QR vault kit requirements, OS profile, BOM, and smoke
  report templates.

## Programmable Board and historical hardware

There is no frozen replacement PCB or physically qualified Board in this
repository. Compare a quality touchscreen and concrete two-SE configurations
against documented developer and Signer workloads before choosing parts. A
dedicated physical confirmation option needs actual display/input/operation
binding; neither touch nor a button alone establishes security. A third SE needs
a distinct verified benefit. Exact APIs, compromise cases, power/pin/resource
budgets, owner firmware/update/recovery and physical tests remain freeze gates.

The legacy TROPIC01 Universal Secure Device board has been retired from this
repository. Its complete design — KiCad project, BOM, production contracts,
docs, and board-specific scripts — was archived with full git history to the
private, read-only repository `nSealr/hardware-legacy-tropic01-universal`. It is
historical material rather than a selected replacement design. The current
direction is the programmable Board above, with one trusted firmware image
initially and no isolation claim for mutually hostile applications. Pi, P4 and
commercial ESP32 qualification remain independent of the custom PCB.

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
