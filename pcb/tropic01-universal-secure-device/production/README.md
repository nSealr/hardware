# Production Output Status

This directory does not contain release manufacturing outputs yet.

The TROPIC01 Universal Secure Device currently has requirements, BOM, and design
notes only. Files for PCBWay must not be generated or uploaded until:

- KiCad schematic exists and is generated from real symbols/nets.
- ERC passes or every warning is explicitly waived.
- PCB layout exists and has routed copper, vias, zones, and board outline.
- DRC passes or every warning is explicitly waived.
- NFC antenna/matching strategy is documented for first-article tuning.
- PCBWay BOM and position files are generated from the routed design.
- The manifest records exact pass/fail status.

Rev A0 manufacturing output is validation hardware, not a certified product.
