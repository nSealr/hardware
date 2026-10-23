"""Record actual generator/tool-environment identities separately from SDK Git."""
import base64
import csv
import hashlib
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[4]
RUN = Path('/home/tux/nsealr/.restart-tools/goal/h01-s3-bod-source-gate-runtime/mode0-first-build-01')
SDK = RUN.parent / 'esp-idf'
BUILD = RUN / 'build'


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    source = json.loads((OUT / 'source-receipt.json').read_text())
    bindings = json.loads((OUT / 'mode0-input-bindings.json').read_text())
    site = RUN.parent / 'python-env/lib/python3.12/site-packages'
    packages = []
    installed_files = {}
    for dist in sorted(importlib.metadata.distributions(path=[str(site)]), key=lambda item: item.metadata['Name'].lower()):
        record_path = Path(dist._path) / 'RECORD'
        assert record_path.is_file()
        count = 0
        no_hash = 0
        for name, field, length in csv.reader(record_path.open(newline='')):
            file = Path(os.path.abspath(dist.locate_file(name)))
            if not field:
                no_hash += 1
                continue
            algorithm, expected = field.split('=', 1)
            data = file.read_bytes()
            actual = base64.urlsafe_b64encode(hashlib.new(algorithm, data).digest()).decode().rstrip('=')
            assert actual == expected and len(data) == int(length), str(file)
            installed_files[str(file)] = {'package': dist.metadata['Name'], 'version': dist.version, 'sha256': hashlib.sha256(data).hexdigest()}
            count += 1
        packages.append({'name': dist.metadata['Name'], 'version': dist.version, 'RECORD_sha256': digest(record_path), 'hashed_files_verified': count, 'unhashed_RECORD_or_cache_entries': no_hash})
    external = []
    for row in bindings['rows']:
        if row['status'] != 'HOST_TOOL_OR_ENVIRONMENT_INPUT_HASH_ONLY':
            continue
        file = Path(row['path'])
        if file.is_relative_to(site):
            installed = installed_files[str(file)]
            assert installed['sha256'] == row['sha256']
            external.append({**row, 'producer_role': 'SDK task Python environment installed before build; matches installed distribution RECORD', 'installed_distribution': installed})
        elif '/r00/tools/baseline/.work/final/.tools/python/' in str(file):
            external.append({**row, 'producer_role': 'Existing R00 Python3.12.15 stdlib; actual file hash, interpreter hash in source-receipt. No new R00 qualification.'})
        elif file.is_relative_to('/usr/share/cmake-3.31'):
            external.append({**row, 'producer_role': 'Existing CMake3.31.6 built-in module; actual file hash, executable hash and emitted version separately bound.'})
        else:
            raise AssertionError(('Unknown host producer input', str(file)))
    # Read the actual v6 logs rather than infer execution from target names.
    logged = {}
    for label, base in [('app', BUILD), ('bootloader', BUILD / 'bootloader')]:
        lines = (base / '.ninja_log').read_text().splitlines()
        assert lines[0] == '# ninja log v6'
        for line in lines[1:]:
            values = line.split('\t')
            assert len(values) == 5
            path = str(Path(os.path.abspath(base / values[3])))
            logged[path] = {'scope': label, 'start': values[0], 'end': values[1], 'mtime': values[2], 'Ninja_command_hash_not_crypto_digest': values[4]}
    generated = []
    for row in bindings['rows']:
        if row['status'] == 'GENERATED_CONFIGURE_OUTPUT_NOT_UPSTREAM_SOURCE':
            generated.append({**row, 'execution_log': logged.get(row['path']), 'producer_role': 'Actual Ninja build recipe' if row['path'] in logged else 'Actual CMake/Kconfig configure generation',
                              'producer_bindings': ['source-receipt.json (exact SDK, official compiler/Ninja, CMake and Python executable)', 'mode0-input-bindings.json (SDK scripts/templates/Kconfig/source/include/link inputs)', 'read-only-command-receipts.json and app/bootloader-ninja-commands.stdout.gz (selected normal recipes)', 'configure/build command receipts and actual app/bootloader Ninja logs (execution, not reproducibility)']})
    spec = importlib.util.spec_from_file_location('historical_preflight', REPO / 'docs/restart/H01/checks/s3-bod-isolated-configure-2026-10-23/preflight-and-configure.py')
    helper = importlib.util.module_from_spec(spec)
    sys.dont_write_bytecode = True
    spec.loader.exec_module(helper)
    pre = json.loads((OUT / 'SDK-preflight.json').read_text())
    children = []
    for link in pre['Gitlinks']:
        child = SDK / link['path']
        if link['state'] == 'pinned':
            check, nested = helper.tree_check(child, link['expected'])
            assert not check['mismatches'] and check['checked_rows_sha256'] == link['actual_tree_check']['checked_rows_sha256']
            extras = subprocess.check_output(['git', '-C', str(child), 'ls-files', '--others', '-z']).decode().strip('\0')
            assert not extras
            children.append({'path': link['path'], **check, 'untracked_including_ignored': [], 'nested_Gitlinks': nested})
    result = {'Python_environment_packages': packages, 'total_installed_hash_rows_verified': sum(row['hashed_files_verified'] for row in packages), 'host_producer_input_rows': external,
              'generated_consumed_file_rows': generated, 'pinned_child_post_build_checks': children,
              'installed_metadata_limit': 'RECORD checks are installed-environment integrity/provenance observations, not new independent PyPI archive authentication. The same admitted environment was read-only during configure/build; original installation command/output remains at2680.',
              'generated_limit': 'File hashes, actual execution logs and exact producer source/tool identities are bound. No binary reproducibility or syscall-complete OS-input trace is claimed.'}
    (OUT / 'producer-bindings.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'packages': len(packages), 'RECORD_hashed_files_verified': result['total_installed_hash_rows_verified'], 'host_rows': len(external), 'generated_rows': len(generated), 'pinned_child_post_checks': len(children)}))


if __name__ == '__main__':
    main()
