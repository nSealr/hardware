"""One admitted configure/build, separated by actual configuration inspection."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time

REPO = Path('/home/tux/nsealr/.restart-tools/goal/h01-s3-bod-source-gate')
OUT = Path(__file__).resolve().parent
RUNTIME = Path('/home/tux/nsealr/.restart-tools/goal/h01-s3-bod-source-gate-runtime')
RUN = RUNTIME / 'mode0-first-build-01'
SDK = RUNTIME / 'esp-idf'
SOURCE = 'e9849a8ae2833b96e0d4ce92978ee48e2087f30c'
ADMISSION = 'b8488e00afb35c5e153278bf306fa32f354edfbd'
PRIOR = REPO / 'docs/restart/H01/checks/s3-bod-isolated-configure-corrected-2026-10-23'


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])


def write(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def prepare():
    assert not RUN.exists(), 'Fresh one-shot output required'
    admission_data = git(REPO, 'show', ADMISSION + ':docs/restart/H01/s3-bod-first-real-build-admission.json')
    admission = json.loads(admission_data)
    spec = importlib.util.spec_from_file_location('historical_preflight', REPO / 'docs/restart/H01/checks/s3-bod-isolated-configure-2026-10-23/preflight-and-configure.py')
    helper = importlib.util.module_from_spec(spec)
    sys.dont_write_bytecode = True
    spec.loader.exec_module(helper)
    top, links = helper.tree_check(SDK, admission['SDK'])
    assert not top['mismatches'] and git(SDK, 'rev-parse', 'HEAD').decode().strip() == admission['SDK']
    baseline = json.loads((PRIOR / 'preflight.json').read_text())
    assert top['checked_rows_sha256'] == baseline['checked_rows_sha256']
    for row in links:
        child = SDK / row['path']
        if not (child / '.git').exists():
            row['state'] = 'not_initialized'
            continue
        row['actual'] = git(child, 'rev-parse', 'HEAD').decode().strip()
        row['state'] = 'pinned' if row['actual'] == row['expected'] else 'wrong_HEAD'
        row['actual_tree_check'], row['nested_Gitlinks'] = helper.tree_check(child, row['actual'])
        row['untracked_nonignored'] = git(child, 'ls-files', '--others', '--exclude-standard').decode().splitlines()
    assert links == baseline['Gitlinks']
    top['Gitlinks'] = links
    top['untracked_nonignored'] = git(SDK, 'ls-files', '--others', '--exclude-standard').decode().splitlines()
    assert top['untracked_nonignored'] == baseline['untracked_nonignored']
    write('SDK-preflight.json', top)
    RUN.mkdir()
    inputs = []
    for item in admission['source_inputs']:
        data = git(REPO, 'show', SOURCE + ':' + item['path'])
        assert hashlib.sha256(data).hexdigest() == item['sha256']
        assert (REPO / item['path']).read_bytes() == data
        target = RUN / 'project' / Path(item['path']).relative_to('diagnostics/s3-bod-selector')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        target.chmod(0o644)
        inputs.append({**item, 'source_commit': SOURCE, 'source_blob': git(REPO, 'rev-parse', SOURCE + ':' + item['path']).decode().strip(), 'export': str(target)})
    query = RUN / 'build/.cmake/api/v1/query'
    query.mkdir(parents=True)
    for name in ('codemodel-v2', 'cmakeFiles-v1', 'cache-v2', 'toolchains-v1'):
        (query / name).touch()
    # The bootloader configure will use this query if the normal build creates it.
    boot_query = RUN / 'build/bootloader/.cmake/api/v1/query'
    boot_query.mkdir(parents=True)
    for name in ('codemodel-v2', 'cmakeFiles-v1', 'cache-v2', 'toolchains-v1'):
        (boot_query / name).touch()
    old = json.loads((PRIOR / 'configure-command.json').read_text())
    old_run = str(RUNTIME / 'isolated-configure-02')
    argv = [arg.replace(old_run, str(RUN)) for arg in old['argv']]
    overrides = {key: value.replace(old_run, str(RUN)) for key, value in old['environment_overrides'].items()}
    overrides['IDF_PY_BUILD_JOBS'] = '4'
    archives = json.loads((REPO / 'docs/restart/H01/checks/s3-bod-build-blocker-2026-10-23/tool-downloads.json').read_text())
    for archive in archives:
        path = Path(archive['argv'][archive['argv'].index('--output') + 1])
        assert path.stat().st_size == archive['asset']['size'] and sha(path) == archive['asset']['sha256']
    tool_root = RUNTIME / 'idf-tools/tools/xtensa-esp-elf/esp-15.2.0_20251204/xtensa-esp-elf'
    names = [tool_root / 'bin' / ('xtensa-esp32s3-elf-' + name) for name in ('gcc', 'g++', 'objdump', 'readelf', 'nm', 'ar')]
    names += [RUNTIME / 'idf-tools/tools/ninja/1.12.1/ninja', RUNTIME / 'python-env/bin/python', Path('/usr/bin/cmake'), Path('/usr/bin/git'), Path('/usr/bin/bwrap')]
    tools = [{'path': str(path), 'resolved': str(path.resolve()), 'sha256': sha(path)} for path in names]
    write('source-receipt.json', {'source_commit': SOURCE, 'source_tree': admission['source_tree'], 'admission_commit': ADMISSION, 'admission_sha256': hashlib.sha256(admission_data).hexdigest(),
        'project_inputs': inputs, 'SDK_commit': admission['SDK'], 'SDK_tree': top['tree'], 'tools': tools, 'original_archive_receipts': archives,
        'configure_argv': argv, 'build_argv': argv[:-1] + ['build'], 'environment_overrides': overrides,
        'job_schedule': 'Official IDF_PY_BUILD_JOBS=4 controls concurrent compiler jobs only (pinned tools/idf_py_actions/tools.py:671-681); no source/config/optimization or safety threshold change.',
        'expected_config': {'IDF_TARGET': 'esp32s3', 'ESP_BROWNOUT_DET': False, 'SECURE_BOOT': False, 'SECURE_FLASH_ENC_ENABLED': False, 'FREERTOS_UNICORE': True, 'ESP_DEFAULT_CPU_FREQ_MHZ_160': True},
        'TEE': 'Inapplicable S3 symbol/default removed by F1, no disablement guarantee; old warnings remain historical.',
        'stop': 'One configure then inspected config then one ordinary mode0 build only. First failure stops; no acquisition, key/sign/provision/device, mode1, invalid-selector, CI or physical action. Full consumed-input closure remains unproved until separately analyzed.'})
    print('Prepared source receipt only; no SDK configure or compiler invoked.')


def execute(stage):
    assert stage in ('configure', 'build')
    receipt_path = OUT / (stage + '-command.json')
    assert not receipt_path.exists(), 'One shot; no retry'
    source = json.loads((OUT / 'source-receipt.json').read_text())
    for item in source['project_inputs']:
        assert sha(item['export']) == item['sha256'] and sha(REPO / item['path']) == item['sha256']
    for item in source['tools']:
        assert sha(item['path']) == item['sha256']
    if stage == 'build':
        inspection = json.loads((OUT / 'pre-build-config-inspection.json').read_text())
        assert inspection['status'] == 'EXPECTED_FLAGS_RESOLVED_BEFORE_BUILD'
        assert inspection['sdkconfig_sha256'] == sha(RUN / 'build/sdkconfig')
        assert json.loads((OUT / 'configure-command.json').read_text())['exit'] == 0
    env = os.environ.copy()
    env.update(source['environment_overrides'])
    command = source[stage + '_argv']
    record = {'source_receipt_sha256': sha(OUT / 'source-receipt.json'), 'executed_wrapper_sha256': sha(__file__), 'argv': command, 'environment_overrides': source['environment_overrides']}
    write(stage + '-command.json', record)
    start = time.time()
    with (OUT / (stage + '.stdout.log')).open('wb') as stdout, (OUT / (stage + '.stderr.log')).open('wb') as stderr:
        done = subprocess.run(command, env=env, stdout=stdout, stderr=stderr)
    record.update({'exit': done.returncode, 'started_unix': start, 'duration_seconds': time.time() - start})
    write(stage + '-command.json', record)
    print(json.dumps({'stage': stage, 'exit': done.returncode, 'duration_seconds': record['duration_seconds']}))


if __name__ == '__main__':
    if sys.argv[1] == 'prepare':
        prepare()
    else:
        execute(sys.argv[1])
