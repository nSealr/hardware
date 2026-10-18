#!/usr/bin/env python3
"""Frozen byte/extraction checks. These do not establish manual or hardware qualification."""
import hashlib
import json
import platform
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[5]
OUT = ROOT / "docs/restart/H01/independent-review-current-manual"
H01 = "docs/restart/H01/"
CANDIDATE = "e39015ae20efd37d509054f4b98ddd68ee7e98c9"
SOURCE = "4d50d155c994e8e770d2b868c371cc04b646ad35"
BEFORE = "6f95cc298c5a8108d5c0bdaedfd53e7b81b130ed"
CACHE = Path("/home/tux/nsealr/.restart-tools/goal/h01-private")
ROOT_ORIGINAL = Path("/home/tux/nsealr/.restart-tools/goal/manual-retrieval-root/curl-experiment/run-02/rm0456.pdf")
ALIASES = {"nist-e11-public-use": "E11_PublicUse.docx",
           "nist-e116-public-use": "E116_PublicUse.pdf",
           "s3-tinyusb-registry": "tinyusb-registry.html"}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def at(commit, path):
    return git("show", commit + ":" + path)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    result = json.loads(at(CANDIDATE, H01 + "result.json"))
    register = json.loads(at(CANDIDATE, H01 + "manual-register.json"))
    before = json.loads(at(BEFORE, H01 + "manual-register.json"))
    docs = {d["id"]: d for d in register["documents"]}
    old = {d["id"]: d for d in before["documents"]}
    checks = []
    for name, expected in [("result.json", "5c10be2874d6eb6eb194f1c71259a95f3197fb7aef79b085064ee8a601b7836e"),
                           ("handoff.md", "2f8d26bdedd671e1d91e47639192bf049c3cfdac5293a4e3c177dc8ac76a5240")]:
        data = at(CANDIDATE, H01 + name)
        checks.append({"path": H01 + name, "sha256": sha(data), "match": sha(data) == expected})
    artifacts = []
    for kind in ["artifacts", "verification_artifacts"]:
        for r in result[kind]:
            data = at(CANDIDATE, r["path"])
            match = sha(data) == r["sha256"] and len(data) == r["bytes"]
            if kind == "artifacts":
                match = match and data == at(SOURCE, r["path"])
            artifacts.append({"kind": kind, "path": r["path"], "bytes": len(data), "sha256": sha(data), "match": match})
    identities = []
    affected = []
    for name, d in docs.items():
        b = old.get(name)
        if b is None:
            affected.append(name)
            continue
        fields = ["id", "manufacturer", "document_id", "revision", "url", "original_sha256", "original_bytes"]
        changed = [f for f in fields if b.get(f) != d.get(f)]
        resolved = b.get("original_sha256") is None and d.get("original_sha256") is not None
        identities.append({"id": name, "changed_fields": changed,
                           "resolved_original": resolved,
                           "match": not changed or (resolved and set(changed) <= {"original_sha256", "original_bytes"})})
        if resolved:
            affected.append(name)
    originals = []
    paths = {}
    for name in affected + ["s3-idf-random"]:
        d = docs[name]
        candidates = ([CACHE / "originals" / ALIASES[name]] if name in ALIASES else
                      [CACHE / "originals" / name] + list((CACHE / "originals").glob(name + ".*")))
        matches = [p for p in candidates if p.is_file() and sha(p.read_bytes()) == d["original_sha256"]]
        match = bool(matches) and matches[0].stat().st_size == d["original_bytes"]
        if match:
            paths[name] = matches[0]
        originals.append({"id": name, "sha256": d["original_sha256"], "bytes": d["original_bytes"], "match": match})
    root_original = ROOT_ORIGINAL.read_bytes()
    checks.append({"path": "private coordinator RM0456 original", "sha256": sha(root_original),
                   "bytes": len(root_original), "match": root_original == paths["u5-rm7"].read_bytes()})
    preserved = []
    for commit, directory in [("5186b7207fa397ceb4cd237d710d8adc163c6eb0", "independent-review/"),
                              ("2f9ea3a18d8fb18e3fbaa8f58b6272102f83b9c2", "independent-review-followup/")]:
        for path in git("ls-tree", "-r", "--name-only", commit, H01 + directory).decode().splitlines():
            data = at(CANDIDATE, path)
            preserved.append({"path": path, "original_review_commit": commit, "sha256": sha(data), "match": data == at(commit, path)})
    extractions = []
    for name, path in paths.items():
        if path.suffix != ".pdf":
            continue
        process = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, check=False)
        prior = (CACHE / "text" / (path.stem + ".txt")).read_bytes()
        extractions.append({"id": name, "method": "fresh pdftotext -layout to memory", "exit_code": process.returncode,
                            "sha256": sha(process.stdout), "bytes": len(process.stdout),
                            "match": process.returncode == 0 and process.stdout == prior})
    with zipfile.ZipFile(paths["nist-e11-public-use"]) as z:
        xml = ElementTree.fromstring(z.read("word/document.xml"))
        native_text = "".join(t.text or "" for t in xml.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"))
    prior_text = (CACHE / "text/E11_PublicUse.txt").read_text()
    normalized = lambda t: re.sub(r"\s+", "", t)
    extractions.append({"id": "nist-e11-public-use", "method": "fresh document.xml w:t in order; whitespace-insensitive correspondence",
                        "normalized_sha256": sha(normalized(native_text).encode()),
                        "match": normalized(native_text) == normalized(prior_text)})
    drawings = []
    with tempfile.TemporaryDirectory(prefix="private-render-", dir=OUT / "logs") as temp:
        for page, name in [(330, "u5g9-lqfp144"), (334, "u5g9-ufbga144")]:
            prefix = Path(temp) / name
            process = subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-singlefile", "-scale-to", "1700", "-png",
                                      str(paths["u5g9-ds"]), str(prefix)], capture_output=True)
            fresh = prefix.with_suffix(".png").read_bytes()
            prior = (CACHE / "drawings" / (name + ".png")).read_bytes()
            drawings.append({"id": name, "pdf_physical_page": page, "sha256": sha(fresh), "exit_code": process.returncode,
                             "match": process.returncode == 0 and fresh == prior,
                             "distribution": "Temporary native render deleted; hashes only retained."})
    claims = json.loads(at(CANDIDATE, H01 + "claims.json"))["claims"]
    ledger = json.loads(at(CANDIDATE, H01 + "pin-errata-ledger.json"))
    dangling = []
    for row in claims + ledger["pins"] + ledger["errata"]:
        ev = row.get("evidence", [])
        if isinstance(ev, dict):
            ev = [ev]
        dangling.extend({"row": row["id"], "document": e["document"]} for e in ev if e["document"] not in docs)
    brief = all(at(CANDIDATE, H01 + p) == at(BEFORE, H01 + p) == at("e10dd2426146e0aa3bbcf04af6a9b1bb59f7e868", H01 + p)
                for p in ["brief.md", "input-notes.json"])
    out = {"scope": "Byte/source/extraction correspondence only; substantive report separate; H01 INCOMPLETE.",
           "candidate": CANDIDATE, "source": SOURCE, "python": platform.python_version(),
           "metadata": checks, "artifact_bindings": artifacts, "prior_source_identity": identities,
           "new_source_ids": sorted(set(docs) - set(old)), "affected_originals": originals,
           "preserved_reviews": preserved, "fresh_extractions": extractions, "fresh_native_renders": drawings,
           "approved_brief_input_unchanged": brief, "unique_source_ids": len(docs) == len(register["documents"]),
           "dangling_references": dangling, "host_admissions": result["host_admissions"], "selected_components": result["selected_components"],
           "counts": {"sources": len(docs), "claims": len(claims), "pins": len(ledger["pins"]),
                      "errata": len(ledger["errata"]), "contradictions": len(ledger["contradictions"])}}
    success = (all(x["match"] for x in checks + artifacts + identities + originals + preserved + extractions + drawings)
               and brief and not dangling and out["unique_source_ids"] and result["source_commit"] == SOURCE)
    out["result"] = "pass" if success else "fail"
    print(json.dumps(out, indent=2))
    return int(not success)


if __name__ == "__main__":
    sys.exit(main())
