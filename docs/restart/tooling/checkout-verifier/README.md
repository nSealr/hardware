# Hardware repository verification

The previous verifier chose the repository type from the checkout directory name.
A renamed hardware checkout rejected its valid CERN license. It could also accept
an MIT license and a missing hardware directory because it skipped the hardware
requirements entirely. Required document paths could be directories.

Source `d91be514ace9c13fdc75cadeb20e8aba152be1a5` selects this repository's
hardware requirements directly, removes the unrelated repository taxonomy and
checks required document paths as files. License and missing-directory checks
remain enforced in arbitrarily named checkouts.

[The result record](result.json) and [artifact hashes](artifact-manifest.json)
preserve the actual prior failure and false acceptance, corrected positive and
negative CLI runs, and unchanged existing CI with 43 tests. The probe extracts
exact public Git snapshots into a fresh private destination; it does not edit the
canonical checkout. Reproduce with an available Python interpreter:

```sh
python3 docs/restart/tooling/checkout-verifier/check.py --destination /absolute/absent-directory --python /absolute/python3
```

This verifies repository tooling only. It does not close H01 or qualify a part,
manual interpretation, PCB or physical behavior. Distinct review and normal CI
are required before merge. The main branch stays unchanged during A02's frozen
source admission and import.
