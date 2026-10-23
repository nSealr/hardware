"""One admitted isolated configure; no build/acquisition or generated-input analyzer."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import time

REPO = Path('/home/tux/nsealr/.restart-tools/goal/h01-s3-bod-source-gate')
RUNTIME = Path('/home/tux/nsealr/.restart-tools/goal/h01-s3-bod-source-gate-runtime')
SDK = RUNTIME / 'esp-idf'
OUT = REPO / 'docs/restart/H01/checks/s3-bod-isolated-configure-2026-10-23'
RUN = RUNTIME / 'isolated-configure-01'
SOURCE = '11047b805039e01dbb73e7c08d4b6a8016090fcd'
SDK_COMMIT = 'fff9895c82d744c7237be8847347bdd1b07c6643'
ADMISSION = 'd84d4de87c0682b207da609aa70d93867378a10f'


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])


def write(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')


def tree_check(repo, commit):
    entries = git(repo, 'ls-tree', '-rz', commit).split(b'\0')
    checked = []
    links = []
    errors = []
    for entry in entries:
        if not entry:
            continue
        metadata, raw_path = entry.split(b'\t', 1)
        mode, kind, oid = metadata.decode().split()
        path = raw_path.decode()
        if kind == 'commit':
            links.append({'path': path, 'expected': oid})
            continue
        file = repo / path
        try:
            st = file.lstat()
            if mode == '120000':
                assert stat.S_ISLNK(st.st_mode)
                data = os.fsencode(os.readlink(file))
                actual_mode = '120000'
            else:
                assert stat.S_ISREG(st.st_mode)
                data = file.read_bytes()
                actual_mode = '100755' if st.st_mode & stat.S_IXUSR else '100644'
            actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            row = {'path': path, 'mode': actual_mode, 'blob': actual,
                   'sha256': hashlib.sha256(data).hexdigest()}
            checked.append(row)
            if actual != oid or actual_mode != mode:
                errors.append({'path': path, 'expected_blob': oid, 'expected_mode': mode, **row})
        except (OSError, AssertionError) as exc:
            errors.append({'path': path, 'error': repr(exc)})
    digest = hashlib.sha256(json.dumps(checked, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    return {'commit': commit, 'tree': git(repo, 'rev-parse', commit + '^{tree}').decode().strip(),
            'tracked_file_count': len(checked), 'checked_rows_sha256': digest,
            'mismatches': errors}, links


def main():
    assert not RUN.exists(), 'One-shot output directory already exists; no configure retry'
    assert git(REPO, 'rev-parse', 'HEAD').decode().strip() == '2680cb7f0dc6950832f4c01ab57bfbb1bdf0a07a'
    assert git(SDK, 'rev-parse', 'HEAD').decode().strip() == SDK_COMMIT
    admission = git(REPO, 'show', ADMISSION + ':docs/restart/H01/s3-bod-isolated-configure-admission.json')
    top, links = tree_check(SDK, SDK_COMMIT)
    assert not top['mismatches'], top
    for row in links:
        child = SDK / row['path']
        if not (child / '.git').exists():
            row['state'] = 'not_initialized'
            continue
        row['actual'] = git(child, 'rev-parse', 'HEAD').decode().strip()
        row['state'] = 'pinned' if row['actual'] == row['expected'] else 'wrong_HEAD'
        row['actual_tree_check'], nested = tree_check(child, row['actual'])
        row['nested_Gitlinks'] = nested
        row['untracked_nonignored'] = git(child, 'ls-files', '--others', '--exclude-standard').decode().splitlines()
    top['Gitlinks'] = links
    top['untracked_nonignored'] = git(SDK, 'ls-files', '--others', '--exclude-standard').decode().splitlines()
    top['admission_commit'] = ADMISSION
    top['admission_sha256'] = hashlib.sha256(admission).hexdigest()
    top['prior_network_namespace_control'] = {
        'argv': ['bwrap', '--unshare-user', '--unshare-net', '--bind', '/', '/', '--', '/bin/true'],
        'exit': 0, 'stdout_bytes': 0, 'stderr_bytes': 0,
    }
    write('preflight.json', top)
    RUN.mkdir()
    project = RUN / 'project'
    input_rows = []
    for relative in ('CMakeLists.txt', 'main/CMakeLists.txt', 'main/main.c', 'sdkconfig.defaults'):
        source_path = 'diagnostics/s3-bod-selector/' + relative
        content = git(REPO, 'show', SOURCE + ':' + source_path)
        assert (REPO / source_path).read_bytes() == content
        target = project / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        target.chmod(0o644)
        input_rows.append({'source_commit': SOURCE, 'path': source_path,
                           'source_blob': git(REPO, 'rev-parse', SOURCE + ':' + source_path).decode().strip(),
                           'export': str(target), 'sha256': hashlib.sha256(content).hexdigest()})
    build = RUN / 'build'
    query = build / '.cmake/api/v1/query'
    query.mkdir(parents=True)
    for request in ('codemodel-v2', 'cmakeFiles-v1', 'cache-v2', 'toolchains-v1'):
        (query / request).touch()
    env = os.environ.copy()
    env.update({
        'IDF_PATH': str(SDK), 'IDF_TOOLS_PATH': str(RUNTIME / 'idf-tools'),
        'IDF_PYTHON_ENV_PATH': str(RUNTIME / 'python-env'), 'IDF_COMPONENT_MANAGER': '0',
        'IDF_SKIP_CHECK_SUBMODULES': '1', 'PYTHONPYCACHEPREFIX': str(RUN / 'pycache'),
        'PATH': ':'.join(str(p) for p in (
            RUNTIME / 'python-env/bin',
            RUNTIME / 'idf-tools/tools/xtensa-esp-elf/esp-15.2.0_20251204/xtensa-esp-elf/bin',
            RUNTIME / 'idf-tools/tools/ninja/1.12.1', Path('/usr/bin'), Path('/bin'))),
    })
    command = [str(RUNTIME / 'python-env/bin/python'), str(SDK / 'tools/idf.py'),
               '-C', str(project), '-B', str(build), '-DIDF_TARGET=esp32s3',
               '-DBOD_RST_SEL=0', '-DSDKCONFIG=' + str(build / 'sdkconfig'), 'reconfigure']
    wrapped = ['bwrap', '--unshare-user', '--unshare-net', '--die-with-parent', '--bind', '/', '/',
               '--ro-bind', str(SDK), str(SDK), '--ro-bind', str(RUNTIME / 'idf-tools'), str(RUNTIME / 'idf-tools'),
               '--ro-bind', str(RUNTIME / 'python-env'), str(RUNTIME / 'python-env'),
               '--ro-bind', str(project), str(project), '--', *command]
    receipt = {'probe_inputs': input_rows, 'SDK_commit': SDK_COMMIT, 'admission_commit': ADMISSION,
               'argv': wrapped, 'environment_overrides': {key: env[key] for key in (
                   'IDF_PATH', 'IDF_TOOLS_PATH', 'IDF_PYTHON_ENV_PATH', 'IDF_COMPONENT_MANAGER',
                   'IDF_SKIP_CHECK_SUBMODULES', 'PYTHONPYCACHEPREFIX', 'PATH')},
               'network': 'Separate network namespace; no host network; SDK/tools/project read-only binds',
               'cmake_file_API_queries': ['codemodel-v2', 'cmakeFiles-v1', 'cache-v2', 'toolchains-v1']}
    write('configure-command.json', receipt)
    start = time.time()
    with (OUT / 'configure.stdout.log').open('wb') as stdout, (OUT / 'configure.stderr.log').open('wb') as stderr:
        completed = subprocess.run(wrapped, env=env, stdout=stdout, stderr=stderr)
    receipt.update({'exit': completed.returncode, 'started_unix': start,
                    'duration_seconds': time.time() - start})
    write('configure-command.json', receipt)
    after, after_links = tree_check(SDK, SDK_COMMIT)
    after['Gitlinks_expected'] = after_links
    after['Gitlink_status'] = git(SDK, 'submodule', 'status').decode().splitlines()
    write('post-configure-source-check.json', after)
    print(json.dumps({'exit': completed.returncode, 'duration_seconds': receipt['duration_seconds'],
                      'SDK_root_files': top['tracked_file_count'], 'Gitlinks': len(links), 'runtime': str(RUN)}))


if __name__ == '__main__':
    main()
