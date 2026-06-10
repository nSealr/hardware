# ERC Triage

Board: `tropic01-universal-secure-device`
Source report: `erc/erc.json`
Total violations: `0`

This is a blocking fabrication artifact. It explains what must be fixed before the PCBWay package can be treated as a release candidate.

## By Type

| Type | Count | Required action |
| --- | ---: | --- |

## By Sheet


## Release Policy

- Do not upload the PCBWay package while ERC triage total_violations is non-zero.
- Do not add ERC waivers to make the report green unless the waiver is tied to a reviewed datasheet decision.
- Prefer improving the schematic generator and source-backed bindings over editing generated sheets by hand.
