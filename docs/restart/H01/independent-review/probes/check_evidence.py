#!/usr/bin/env python3
"""Read-only H01 evidence correspondence; no acceptance or electrical inference."""
import hashlib
import json
import platform
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

BASE = Path(__file__).resolve().parents[5]
H01 = BASE / "docs/restart/H01"
INTEGRATION = Path("/home/tux/nsealr")
RESTART = INTEGRATION / "workspace/docs/restart"
CACHE = INTEGRATION / ".restart-tools/goal/h01-private"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    register = json.loads((H01 / "manual-register.json").read_text())
    result = json.loads((H01 / "result.json").read_text())
    candidates = {}
    for path in (CACHE / "originals").iterdir():
        if path.is_file():
            candidates.setdefault(path.stem, []).append(path)
    for folder, key in [("2026-10-13-round3", "originals_and_attempts"),
                        ("2026-10-13-validation4", "original_requests")]:
        old = json.loads((RESTART / folder / "hardware/source-register.json").read_text())
        for entry in old[key]:
            path = entry.get("local_path", entry.get("path"))
            if path:
                candidates.setdefault(entry["id"], []).append(Path(path))
    references = {"ref-safe7-main": "trezor-hardware/electronics/trezor_safe_7/ts7_main_rev_d_sch.pdf",
                  "ref-ts1303": "devboards/TROPIC01_USB_Devkit/PCB/TS1303/ts1303_schematics.pdf",
                  "ref-ts1401": "devboards/TROPIC01_Arduino_Shield/TS1401/ts1401_schematics.pdf",
                  "ref-ts1501": "devboards/TROPIC01_Raspberry_Pi_Shield/TS1501/ts1501_schematics.pdf",
                  "ref-ts1702": "devboards/TROPIC01_Mini_Board/TS1702/TS1702_schematic.pdf"}
    for name, path in references.items():
        candidates[name] = [RESTART / "2026-10-18-readiness/hardware/sources" / path]
    artifacts = []
    for entry in result["artifacts"]:
        data = (BASE / entry["path"]).read_bytes()
        artifacts.append({"path": entry["path"], "sha256": digest(data), "bytes": len(data),
                          "match": digest(data) == entry["sha256"] and len(data) == entry["bytes"]})
    originals = []
    for entry in register["documents"]:
        expected = entry.get("original_sha256")
        row = {"id": entry["id"], "expected_sha256": expected}
        if expected is None:
            row["result"] = "no validated original claimed; no original hash inferred"
        else:
            matches = [p for p in candidates.get(entry["id"], [])
                       if p.is_file() and digest(p.read_bytes()) == expected]
            row["result"] = "match" if matches else "MISSING OR MISMATCH"
            if matches:
                row["bytes"] = matches[0].stat().st_size
                row["size_match"] = row["bytes"] == entry["original_bytes"]
        originals.append(row)
    extractions = []
    for name in ["s3-module", "s3-trm", "s3-es", "p4-es", "ti-bq24074", "ti-bq25628", "ti-tusb320lai"]:
        pdf = CACHE / "originals" / (name + ".pdf")
        old = (CACHE / "text" / (name + ".txt")).read_bytes()
        process = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, check=False)
        extractions.append({"id": name, "command": "pdftotext -layout ORIGINAL -",
                            "exit_code": process.returncode,
                            "reextracted_sha256": digest(process.stdout),
                            "preserved_extraction_sha256": digest(old),
                            "exact_match": process.returncode == 0 and process.stdout == old})
    ledger = json.loads((H01 / "pin-errata-ledger.json").read_text())
    pin_checks = []
    for part in ["STM32U585VITx", "STM32U585VITxQ"]:
        source_id = "st-pins-" + part
        record = next(d for d in register["documents"] if d["id"] == source_id)
        original = next(p for p in candidates[source_id]
                        if p.is_file() and digest(p.read_bytes()) == record["original_sha256"])
        root = ET.fromstring(original.read_bytes())
        pins = {p.attrib["Position"]: p for p in root.findall("{*}Pin")}
        for row in ledger["pins"]:
            if not row["id"].startswith("P-" + part + "-"):
                continue
            for pad, value in row["package_pads"].items():
                gpio, signal = value.split(" ", 1)
                pin = pins.get(pad)
                matched = (pin is not None and pin.attrib["Name"].split(" ", 1)[0] == gpio
                           and signal in {s.attrib["Name"] for s in pin.findall("{*}Signal")})
                pin_checks.append({"row": row["id"], "source": source_id,
                                   "source_sha256": record["original_sha256"], "pad": pad,
                                   "gpio": gpio, "signal": signal, "match": matched})
    claims = json.loads((H01 / "claims.json").read_text())["claims"]
    ids = {d["id"] for d in register["documents"]}
    dangling = []
    for item in claims + ledger["pins"] + ledger["errata"]:
        entries = item.get("evidence", [])
        if isinstance(entries, dict):
            entries = [entries]
        for entry in entries:
            if entry["document"] not in ids:
                dangling.append({"item": item["id"], "document": entry["document"]})
    out = {"scope": "Record/byte correspondence only. Independent source reading is in report.md; H01 is incomplete.",
           "frozen_candidate": "d5d75306a082215453d329e31ca9c11d6effa80d",
           "source_commit": result["source_commit"], "python": platform.python_version(),
           "artifacts": artifacts, "originals": originals, "extractions": extractions,
           "manufacturer_xml_pin_checks": pin_checks,
           "unique_source_ids": len(ids) == len(register["documents"]), "dangling_references": dangling,
           "counts": {"sources": len(ids), "claims": len(claims), "pin_rows": len(ledger["pins"]), "errata_rows": len(ledger["errata"])}}
    print(json.dumps(out, indent=2))
    return int(not all(a["match"] for a in artifacts)
               or any(a["result"] == "MISSING OR MISMATCH" or a.get("size_match") is False for a in originals)
               or not all(e["exact_match"] for e in extractions) or bool(dangling)
               or len(pin_checks) != 48 or not all(p["match"] for p in pin_checks)
               or len(ids) != len(register["documents"]))


if __name__ == "__main__":
    sys.exit(main())
