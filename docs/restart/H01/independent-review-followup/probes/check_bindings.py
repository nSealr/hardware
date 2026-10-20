#!/usr/bin/env python3
"""Read-only correspondence checks for a frozen research candidate; no hardware inference."""
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
H01 = "docs/restart/H01/"
CANDIDATE = "6f95cc298c5a8108d5c0bdaedfd53e7b81b130ed"
SOURCE = "6b45f6f79e1888bdf2ec6680d14dd951b7019327"
OLD = "d5d75306a082215453d329e31ca9c11d6effa80d"
REVIEW = "5186b7207fa397ceb4cd237d710d8adc163c6eb0"
CACHE = Path("/home/tux/nsealr/.restart-tools/goal/h01-private")


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def at(commit, path):
    return git("show", commit + ":" + path)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    result = json.loads(at(CANDIDATE, H01 + "result.json"))
    register = json.loads(at(CANDIDATE, H01 + "manual-register.json"))
    before = json.loads(at(OLD, H01 + "manual-register.json"))
    old_ids = {d["id"] for d in before["documents"]}
    docs = {d["id"]: d for d in register["documents"]}
    checks = []
    for key, expected in [("result.json", "63e99a811fc527e0da9b7fb8f3f4bcb67b6ab8a45f74dbb3b2390d6b1bcfa07b"),
                          ("handoff.md", "8475e8fa0c9f33aac01edeb8d9e0ed4556f9f4b97f2e6ef8cca9fd79f7130d78")]:
        actual = digest(at(CANDIDATE, H01 + key))
        checks.append({"path": H01 + key, "sha256": actual, "match": actual == expected})
    artifacts = []
    for kind in ["artifacts", "verification_artifacts"]:
        for record in result[kind]:
            data = at(CANDIDATE, record["path"])
            match = digest(data) == record["sha256"] and len(data) == record["bytes"]
            if kind == "artifacts":
                match = match and at(SOURCE, record["path"]) == data
            artifacts.append({"kind": kind, "path": record["path"], "sha256": digest(data),
                              "bytes": len(data), "match": match})
    originals = []
    for name, record in docs.items():
        if name in old_ids and name not in ["s3-es", "s3-trm", "p4-es", "ti-tps63802"]:
            continue
        if record["original_sha256"] is None:
            originals.append({"id": name, "sha256": None, "match": None,
                              "scope": "Web-only reading; no original hash inferred."})
            continue
        matches = [p for p in (CACHE / "originals").glob(name + ".*")
                   if p.is_file() and digest(p.read_bytes()) == record["original_sha256"]]
        match = bool(matches) and matches[0].stat().st_size == record["original_bytes"]
        originals.append({"id": name, "sha256": record["original_sha256"],
                          "bytes": record["original_bytes"], "match": match})
    identities = []
    for old in before["documents"]:
        fields = ["id", "manufacturer", "document_id", "revision", "url", "original_sha256", "original_bytes"]
        match = all(old.get(k) == docs[old["id"]].get(k) for k in fields)
        identities.append({"id": old["id"], "identity_unchanged": match})
    preserved = []
    for path in git("ls-tree", "-r", "--name-only", REVIEW, H01 + "independent-review/").decode().splitlines():
        data = at(CANDIDATE, path)
        preserved.append({"path": path, "sha256": digest(data), "match": data == at(REVIEW, path)})
    extractions = []
    for name in ["s3-es", "s3-trm", "ti-tps63802"]:
        process = subprocess.run(["pdftotext", "-layout", str(CACHE / "originals" / (name + ".pdf")), "-"],
                                 capture_output=True, check=False)
        prior = (CACHE / "text" / (name + ".txt")).read_bytes()
        extractions.append({"id": name, "command": "pdftotext -layout ORIGINAL -",
                            "exit_code": process.returncode, "sha256": digest(process.stdout),
                            "match": process.returncode == 0 and process.stdout == prior})
    brief = all(at(CANDIDATE, H01 + p) == at(OLD, H01 + p) for p in ["brief.md", "input-notes.json"])
    claims = json.loads(at(CANDIDATE, H01 + "claims.json"))["claims"]
    ledger = json.loads(at(CANDIDATE, H01 + "pin-errata-ledger.json"))
    dangling = []
    for row in claims + ledger["pins"] + ledger["errata"]:
        evidence = row.get("evidence", [])
        if isinstance(evidence, dict):
            evidence = [evidence]
        dangling.extend({"row": row["id"], "document": e["document"]}
                        for e in evidence if e["document"] not in docs)
    out = {"scope": "Byte/reference correspondence only; substantive review is separate; H01 incomplete.",
           "candidate": CANDIDATE, "source": SOURCE, "python": platform.python_version(),
           "metadata": checks, "artifacts": artifacts, "affected_originals": originals,
           "prior_source_identities": identities, "prior_review_preserved": preserved,
           "pdf_text_correspondence": extractions, "brief_input_unchanged": brief,
           "source_unique": len(docs) == len(register["documents"]), "dangling_references": dangling,
           "host_admissions": result["host_admissions"], "selected_components": result["selected_components"],
           "counts": {"sources": len(docs), "claims": len(claims), "pins": len(ledger["pins"]),
                      "errata": len(ledger["errata"]), "contradictions": len(ledger["contradictions"])}}
    print(json.dumps(out, indent=2))
    return int(not all(x["match"] for x in checks + artifacts + preserved + extractions)
               or any(x["match"] is False for x in originals)
               or not all(x["identity_unchanged"] for x in identities)
               or not brief or bool(dangling) or not out["source_unique"]
               or result["source_commit"] != SOURCE)


if __name__ == "__main__":
    sys.exit(main())
