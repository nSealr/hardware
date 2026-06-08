# Project-Local KiCad Libraries

These files are source dependencies for the Rev A0 KiCad project. They are kept
inside the project so schematic capture and review do not depend on a user-level
KiCad library path or on the external repository cache.

## TROPIC01

- Symbol: `symbols/TROPIC01.kicad_sym`
- 3D model: `3dmodels/TROPIC01.step`
- Source: Tropic Square `devboards/KiCad-lib`
- Upstream note: the official KiCad-lib README recommends the KiCad standard
  `Package_DFN_QFN:QFN-32-1EP_4x4mm_P0.4mm_EP2.65x2.65mm` footprint.

The TROPIC01 footprint is therefore not copied into this library for Rev A0.
Before routing, compare the KiCad 10 standard footprint against the latest
Tropic Square Mini Board layout and the current datasheet land-pattern guidance.
