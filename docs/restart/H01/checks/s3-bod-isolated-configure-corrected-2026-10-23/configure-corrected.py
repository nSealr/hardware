"""One configure with only the separately admitted /dev mount correction."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time

REPO = Path('/home/tux/nsealr/.restart-tools/goal/h01-s3-bod-source-gate')
OLD = REPO / 'docs/restart/H01/checks/s3-bod-isolated-configure-2026-10-23'
OUT = Path(__file__).resolve().parent
OLD_RUN = Path('/home/tux/nsealr/.restart-tools/goal/h01-s3-bod-source-gate-runtime/isolated-configure-01')
RUN = OLD_RUN.parent / 'isolated-configure-02'
ADMISSION = 'bd65d37366f6c128af43d257116cced2733fe192'
SDK = OLD_RUN.parent / 'esp-idf'


def write(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')


def main():
    assert not RUN.exists(), 'One-shot directory exists; no configure retry'
    assert subprocess.check_output(['git', '-C', str(REPO), 'rev-parse', 'HEAD']).decode().strip() == '59ceb746ff5e30f350453ce302f6699a487e65d8'
    spec = importlib.util.spec_from_file_location('historical_preflight', OLD / 'preflight-and-configure.py')
    helper = importlib.util.module_from_spec(spec)
    sys.dont_write_bytecode = True
    spec.loader.exec_module(helper)
    old_command = json.loads((OLD / 'configure-command.json').read_text())
    baseline = json.loads((OLD / 'preflight.json').read_text())
    source, links = helper.tree_check(SDK, helper.SDK_COMMIT)
    assert helper.git(SDK, 'rev-parse', 'HEAD').decode().strip() == helper.SDK_COMMIT
    assert not source['mismatches'] and source['checked_rows_sha256'] == baseline['checked_rows_sha256']
    for row in links:
        child = SDK / row['path']
        if not (child / '.git').exists():
            row['state'] = 'not_initialized'
            continue
        row['actual'] = helper.git(child, 'rev-parse', 'HEAD').decode().strip()
        row['state'] = 'pinned' if row['actual'] == row['expected'] else 'wrong_HEAD'
        row['actual_tree_check'], row['nested_Gitlinks'] = helper.tree_check(child, row['actual'])
        row['untracked_nonignored'] = helper.git(child, 'ls-files', '--others', '--exclude-standard').decode().splitlines()
    assert links == baseline['Gitlinks'], 'SDK Gitlink state changed since original attempt'
    source['Gitlinks'] = links
    source['untracked_nonignored'] = helper.git(SDK, 'ls-files', '--others', '--exclude-standard').decode().splitlines()
    assert source['untracked_nonignored'] == baseline['untracked_nonignored']
    admission = helper.git(REPO, 'show', ADMISSION + ':docs/restart/H01/s3-bod-isolated-configure-wrapper-correction.json')
    source['admission_commit'] = ADMISSION
    source['admission_sha256'] = hashlib.sha256(admission).hexdigest()
    source['historical_preflight_source_sha256'] = hashlib.sha256((OLD / 'preflight-and-configure.py').read_bytes()).hexdigest()
    write('preflight.json', source)
    RUN.mkdir()
    rows = []
    for old_row in old_command['probe_inputs']:
        row = dict(old_row)
        data = helper.git(REPO, 'show', row['source_commit'] + ':' + row['path'])
        assert hashlib.sha256(data).hexdigest() == row['sha256']
        target = Path(row['export'].replace(str(OLD_RUN), str(RUN)))
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        target.chmod(0o644)
        row['export'] = str(target)
        rows.append(row)
    query = RUN / 'build/.cmake/api/v1/query'
    query.mkdir(parents=True)
    for name in old_command['cmake_file_API_queries']:
        (query / name).touch()
    argv = [arg.replace(str(OLD_RUN), str(RUN)) for arg in old_command['argv']]
    at = argv.index('--')
    argv[at:at] = ['--dev', '/dev']
    changes = {key: value.replace(str(OLD_RUN), str(RUN)) for key, value in old_command['environment_overrides'].items()}
    env = os.environ.copy()
    env.update(changes)
    receipt = {'admission_commit': ADMISSION, 'admission_sha256': source['admission_sha256'],
               'historical_failed_command_sha256': hashlib.sha256((OLD / 'configure-command.json').read_bytes()).hexdigest(),
               'change': 'Only --dev /dev added; fresh project/build/pycache paths. No A/B preflight repeated.',
               'argv': argv, 'environment_overrides': changes, 'probe_inputs': rows,
               'cmake_file_API_queries': old_command['cmake_file_API_queries']}
    write('configure-command.json', receipt)
    start = time.time()
    with (OUT / 'configure.stdout.log').open('wb') as stdout, (OUT / 'configure.stderr.log').open('wb') as stderr:
        completed = subprocess.run(argv, env=env, stdout=stdout, stderr=stderr)
    receipt.update({'exit': completed.returncode, 'started_unix': start, 'duration_seconds': time.time() - start})
    write('configure-command.json', receipt)
    after, after_links = helper.tree_check(SDK, helper.SDK_COMMIT)
    after['Gitlinks_expected'] = after_links
    after['Gitlink_status'] = helper.git(SDK, 'submodule', 'status').decode().splitlines()
    write('post-configure-source-check.json', after)
    print(json.dumps({'exit': completed.returncode, 'duration_seconds': receipt['duration_seconds'], 'runtime': str(RUN)}))


if __name__ == '__main__':
    main()
