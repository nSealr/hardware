"""Record real CLI checks in fresh private snapshots; no physical PCB validation."""
import argparse
import datetime
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile

SOURCE_ROOT = Path(__file__).resolve().parents[4]
BASE = "340697d6713a671e9e01b0dc874ec999ab071601"
SOURCE = "d91be514ace9c13fdc75cadeb20e8aba152be1a5"
sha = lambda data: hashlib.sha256(data).hexdigest()
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--destination", type=Path, required=True)
parser.add_argument("--python", type=Path, required=True)
args = parser.parse_args()
output = args.destination.absolute()
assert not output.exists() and not output.is_symlink()
assert output.parent == output.parent.resolve(strict=True)
output.mkdir(mode=0o700)
environment = {"python": subprocess.check_output([str(args.python), "--version"], text=True).strip(),
               "python_sha256": sha(args.python.resolve().read_bytes()),
               "git": subprocess.check_output(["git", "--version"], text=True).strip()}
rows = []

def run(label, directory, expected, marker, command=None):
    command = command or [str(args.python), "-B", "scripts/verify_repo.py"]
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    env = os.environ.copy()
    env["PATH"] = str(args.python.parent) + os.pathsep + env.get("PATH", "")
    result = subprocess.run(command, cwd=directory, env=env, capture_output=True)
    log = result.stdout + result.stderr
    path = output / (label + ".log")
    path.write_bytes(log)
    path.chmod(0o600)
    rows.append({"label": label, "command": command, "cwd": str(directory),
                 "started_utc": started, "exit_code": result.returncode,
                 "log": path.name, "sha256": sha(log), "expected": expected})
    assert result.returncode == expected and marker in log and b"Traceback" not in log, label

def snapshot(commit, name):
    directory = output / name
    directory.mkdir(mode=0o700)
    archive = subprocess.check_output(["git", "-C", str(SOURCE_ROOT), "archive", commit])
    with tarfile.open(fileobj=io.BytesIO(archive)) as tree:
        tree.extractall(directory, filter="data")
    return directory

before = snapshot(BASE, "arbitrary-before")
after = snapshot(SOURCE, "arbitrary-after")
run("before-renamed", before, 1, b"MIT License")
run("after-renamed", after, 0, b"hardware baseline verification passed")

original_license = (before / "LICENSE").read_bytes()
(before / "LICENSE").write_text("MIT License\n")
(before / "kits").rename(before / ".held-kits")
run("before-wrong-license-missing-hardware-dir-accepted", before, 0, b"baseline verification passed")
(before / ".held-kits").rename(before / "kits")
(before / "LICENSE").write_bytes(original_license)

original_license = (after / "LICENSE").read_bytes()
(after / "LICENSE").write_text("MIT License\n")
run("after-wrong-license", after, 1, b"CERN Open Hardware Licence")
(after / "LICENSE").write_bytes(original_license)
(after / "kits").rename(after / ".held-kits")
run("after-missing-hardware-dir", after, 1, b"missing required directory: kits")
(after / ".held-kits").rename(after / "kits")

document = after / "docs/architecture.md"
original_document = document.read_bytes()
document.unlink()
document.mkdir()
run("after-document-is-directory", after, 1, b"missing required file: docs/architecture.md")
document.rmdir()
document.write_bytes(original_document)

license_file = after / "LICENSE"
license_file.unlink()
license_file.mkdir()
run("after-license-is-directory", after, 1, b"missing required file: LICENSE")
license_file.rmdir()
license_file.write_bytes(original_license)
run("after-restored-positive", after, 0, b"hardware baseline verification passed")
run("after-make-ci", after, 0, b"Ran 43 tests", ["make", "ci"])

result = {"source_commit": SOURCE, "baseline": BASE, "environment": environment,
          "checks": rows, "scope": "Actual renamed-checkout CLI and existing 43-test hardware tooling suite only.",
          "limits": "No PCB, component, manual-substance, electrical or physical qualification."}
(output / "result.json").write_text(json.dumps(result, indent=2) + "\n")
(output / "result.json").chmod(0o600)
print("PASS: renamed checkout, reproduced prior false acceptance, six corrected CLI outcomes and existing 43-test CI")
