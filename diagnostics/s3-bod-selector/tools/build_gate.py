#!/usr/bin/env python3
"""Fixed S3 compile diagnostic; host tools only, never a device command."""
from __future__ import annotations

import argparse
import email.parser
import errno
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tarfile
import time
import urllib.parse
import urllib.request
import zipfile

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PROJECT = HERE.parent


class GateError(RuntimeError):
    pass


def sha(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def dump(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + '\n')


def command(work: Path, label: str, args: list[str], *, cwd: Path | None = None,
            env: dict[str, str] | None = None, expected: int = 0) -> bytes:
    receipts = work / 'receipts'
    receipts.mkdir(exist_ok=True)
    record = {'argv': args, 'cwd': str(cwd) if cwd else None, 'expected_exit': expected}
    start = time.monotonic()
    with (receipts / (label + '.stdout')).open('wb') as stdout, (receipts / (label + '.stderr')).open('wb') as stderr:
        result = subprocess.run(args, cwd=cwd, env=env, stdout=stdout, stderr=stderr)
    record.update({'exit': result.returncode, 'seconds': time.monotonic() - start,
                   'stdout_sha256': sha(receipts / (label + '.stdout')),
                   'stderr_sha256': sha(receipts / (label + '.stderr'))})
    dump(receipts / (label + '.json'), record)
    if result.returncode != expected:
        raise GateError('%s exit%d, expected%d; see %s' % (label, result.returncode, expected, receipts))
    return (receipts / (label + '.stdout')).read_bytes()


def acquire(row: dict, cache: Path, work: Path) -> Path:
    path = cache / row['filename']
    if not path.exists():
        temporary = path.with_name(path.name + '.partial')
        if temporary.exists():
            raise GateError('Unresolved partial acquisition: %s' % temporary)
        start = time.monotonic()
        try:
            request = urllib.request.Request(row['url'], headers={'User-Agent': 'nSealr-S3-build-gate/1'})
            with urllib.request.urlopen(request, timeout=180) as response, temporary.open('xb') as stream:
                shutil.copyfileobj(response, stream)
            if sha(temporary) != row['sha256']:
                raise GateError('Publisher asset checksum mismatch: %s' % row['url'])
            temporary.rename(path)
        except Exception as error:
            dump(work / 'acquisition-error.json', {'asset': row, 'error': repr(error), 'seconds': time.monotonic() - start})
            raise
    if sha(path) != row['sha256'] or ('size' in row and path.stat().st_size != row['size']) or ('bytes' in row and path.stat().st_size != row['bytes']):
        raise GateError('Frozen asset mismatch: %s' % path)
    return path


def extract(archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True)
    if archive.name.endswith('.zip'):
        with zipfile.ZipFile(archive) as zipped:
            for entry in zipped.infolist():
                name = Path(entry.filename)
                if name.is_absolute() or '..' in name.parts or entry.is_dir():
                    raise GateError('Unexpected ZIP entry: %s' % entry.filename)
                target = destination / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(zipped.read(entry))
                target.chmod((entry.external_attr >> 16) & 0o777 or 0o755)
    else:
        with tarfile.open(archive, 'r:*') as tar:
            tar.extractall(destination, filter='data')


def git_tree_check(root: Path, revision: str) -> dict:
    def git(*args: str) -> bytes:
        return subprocess.check_output(['git', '-C', str(root), *args])
    actual = git('rev-parse', 'HEAD').decode().strip()
    if actual != revision:
        raise GateError('Wrong Git HEAD at %s: %s' % (root, actual))
    count = 0
    links = []
    for entry in git('ls-tree', '-rz', revision).split(b'\0'):
        if not entry:
            continue
        metadata, name = entry.split(b'\t', 1)
        mode, kind, blob = metadata.decode().split()
        name = name.decode()
        if kind == 'commit':
            links.append({'path': name, 'commit': blob})
            continue
        file = root / name
        data = os.fsencode(os.readlink(file)) if mode == '120000' else file.read_bytes()
        actual_mode = '120000' if file.is_symlink() else ('100755' if file.stat().st_mode & 0o100 else '100644')
        actual_blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if actual_blob != blob or actual_mode != mode:
            raise GateError('Pinned Git file/mode mismatch: %s' % file)
        count += 1
    return {'commit': revision, 'tree': git('rev-parse', revision + '^{tree}').decode().strip(), 'files_verified': count, 'Gitlinks': links}


def namespace(bwrap: str, ro_paths: list[Path], args: list[str]) -> list[str]:
    result = [bwrap, '--unshare-user', '--unshare-net', '--die-with-parent', '--bind', '/', '/']
    for path in ro_paths:
        result += ['--ro-bind', str(path), str(path)]
    return result + ['--dev', '/dev', '--cap-drop', 'ALL', '--', *args]


PREFLIGHT = r'''
import errno,json,os,subprocess,sys
expected=json.loads(sys.argv[1]); sdk,pin=expected['sdk'],expected['pin']
assert os.getuid()==expected['uid'] and os.geteuid()==expected['euid']
assert os.getgid()==expected['gid'] and os.getegid()==expected['egid']
status=dict(line.split(':',1) for line in open('/proc/self/status') if ':' in line)
assert int(status['CapEff'].strip(),16)==0 and int(status['CapPrm'].strip(),16)==0
assert os.readlink('/proc/self/ns/net')!=expected['outer_netns']
interfaces=[line.split(':',1)[0].strip() for line in open('/proc/net/dev').read().splitlines()[2:]]
assert interfaces==['lo'] and not open('/proc/net/route').read().splitlines()[1:]
with open('/dev/null','r+b',buffering=0) as stream: stream.write(b'')
assert subprocess.check_output(['git','-C',sdk,'rev-parse','HEAD'],text=True).strip()==pin
for directory in expected['read_only']:
 assert os.statvfs(directory).f_flag & os.ST_RDONLY
 target=os.path.join(directory,'.nsealr-ro-probe-%d'%os.getpid())
 try:
  with open(target,'xb'): pass
 except OSError as error:
  assert error.errno==errno.EROFS
 else:
  os.unlink(target);raise AssertionError('Unexpected writable input mount')
print(json.dumps({'uid':os.getuid(),'euid':os.geteuid(),'gid':os.getgid(),'egid':os.getegid(),'CapEff':status['CapEff'].strip(),'CapPrm':status['CapPrm'].strip(),'NoNewPrivs':status['NoNewPrivs'].strip(),'uid_map':open('/proc/self/uid_map').read(),'gid_map':open('/proc/self/gid_map').read(),'netns':os.readlink('/proc/self/ns/net'),'outer_netns':expected['outer_netns'],'interfaces':interfaces,'IPv4_routes':0,'dev_null_rw':True,'read_only_verified':expected['read_only']}))
'''


def prepare(lock: dict, work: Path, cache: Path, bwrap: str) -> dict:
    sdk = work / 'sdk'
    sdk.mkdir()
    command(work, 'sdk-init', ['git', 'init', str(sdk)])
    command(work, 'sdk-origin', ['git', '-C', str(sdk), 'remote', 'add', 'origin', lock['SDK']['url']])
    command(work, 'sdk-fetch', ['git', '-C', str(sdk), 'fetch', '--depth=1', 'origin', lock['SDK']['commit']])
    command(work, 'sdk-checkout', ['git', '-C', str(sdk), 'checkout', '--detach', lock['SDK']['commit']])
    for index, link in enumerate(lock['SDK']['Gitlinks']):
        child = sdk / link['path']
        child.mkdir(parents=True, exist_ok=True)
        url = urllib.parse.urljoin(lock['SDK']['url'] + '/', link['url'])
        command(work, 'link%d-init' % index, ['git', 'init', str(child)])
        command(work, 'link%d-origin' % index, ['git', '-C', str(child), 'remote', 'add', 'origin', url])
        command(work, 'link%d-fetch' % index, ['git', '-C', str(child), 'fetch', '--depth=1', 'origin', link['gitlink']])
        command(work, 'link%d-checkout' % index, ['git', '-C', str(child), 'checkout', '--detach', link['gitlink']])
    source_checks = [git_tree_check(sdk, lock['SDK']['commit'])]
    if source_checks[0]['tree'] != lock['SDK']['tree']:
        raise GateError('SDK tree differs from frozen primary input')
    source_checks += [git_tree_check(sdk / link['path'], link['gitlink']) for link in lock['SDK']['Gitlinks']]
    dump(work / 'source-checks-before.json', source_checks)
    tools = work / 'tools'
    tools.mkdir()
    roots = {}
    for asset in lock['assets']:
        archive = acquire(asset, cache, work)
        target = tools / 'python-runtime' if asset['name'] == 'python' else tools / 'tools' / asset['name'] / asset['version']
        extract(archive, target)
        roots[asset['name']] = target
    python = roots['python'] / 'python/bin/python3'
    cmake = roots['cmake'] / 'cmake-3.31.6-linux-x86_64/bin'
    compiler = roots['xtensa-esp-elf'] / 'xtensa-esp-elf/bin'
    ninja = roots['ninja']
    ro = [sdk, tools, PROJECT]
    expected = {'sdk': str(sdk), 'pin': lock['SDK']['commit'], 'outer_netns': os.readlink('/proc/self/ns/net'), 'uid': os.getuid(), 'euid': os.geteuid(), 'gid': os.getgid(), 'egid': os.getegid(), 'read_only': list(map(str, ro))}
    preflight_env = os.environ.copy()
    preflight_env['PYTHONPYCACHEPREFIX'] = str(work / 'preflight-pycache')
    command(work, 'bootstrap-namespace-preflight', namespace(bwrap, ro, [str(python), '-c', PREFLIGHT, json.dumps(expected)]), env=preflight_env)
    wheels = work / 'wheels'
    wheels.mkdir()
    for package in lock['Python_packages']:
        archive = acquire(package, cache, work)
        if package['kind'] == 'bdist_wheel':
            shutil.copyfile(archive, wheels / archive.name)
    constraints = lock['SDK_constraints']
    for field, value in [('upstream_filename', 'upstream_sha256'), ('filename', 'sha256'), ('patch_filename', 'patch_sha256')]:
        if sha(HERE / constraints[field]) != constraints[value]:
            raise GateError('Constraint/patch source mismatch')
    upstream = (HERE / constraints['upstream_filename']).read_bytes()
    if upstream.count(b'cryptography>=2.1.4,<49\n') != 1 or (HERE / constraints['filename']).read_bytes() != upstream.replace(b'cryptography>=2.1.4,<49\n', b'cryptography==50.0.0\n'):
        raise GateError('Constraint patch is not the single admitted line')
    shutil.copyfile(HERE / constraints['filename'], tools / 'espidf.constraints.v6.1.txt')
    venv = tools / 'python-env'
    env = os.environ.copy()
    env.update({'IDF_PATH': str(sdk), 'IDF_TOOLS_PATH': str(tools), 'IDF_PYTHON_ENV_PATH': str(venv),
                'IDF_COMPONENT_MANAGER': '0', 'IDF_SKIP_CHECK_SUBMODULES': '1', 'IDF_PY_BUILD_JOBS': '4',
                'PYTHONPYCACHEPREFIX': str(work / 'pycache'), 'TMPDIR': str(work / 'tmp'),
                'PIP_NO_INDEX': '1', 'PIP_CONFIG_FILE': '/dev/null', 'PIP_DISABLE_PIP_VERSION_CHECK': '1',
                'PIP_CACHE_DIR': str(work / 'pip-cache'), 'XDG_CACHE_HOME': str(work / 'cache'),
                'PIP_FIND_LINKS': str(wheels), 'PIP_CONSTRAINT': str(HERE / 'python-versions.txt'),
                'PATH': ':'.join(map(str, [venv / 'bin', python.parent, compiler, ninja, cmake, Path('/usr/bin'), Path('/bin')]))})
    (work / 'tmp').mkdir()
    command(work, 'python-version', [str(python), '-c', 'import sys; assert sys.version_info[:3]==(3,12,15); print(sys.version)'], env=env)
    command(work, 'venv', [str(python), '-m', 'venv', str(venv)], env=env)
    vp = venv / 'bin/python'
    initial = [row for row in lock['Python_packages'] if row['name'] in ('pip', 'setuptools')]
    bootstrap = work / 'bootstrap.txt'
    bootstrap.write_text(''.join('%s==%s --hash=sha256:%s\n' % (row['name'], row['version'], row['sha256']) for row in initial))
    offline_prefix = lambda args: namespace(bwrap, [sdk, roots['python'], wheels, PROJECT], args)
    command(work, 'bootstrap-pip', offline_prefix([str(vp), '-m', 'pip', 'install', '--no-index', '--no-deps', '--require-hashes', '-r', str(bootstrap)]), env=env)
    derived = []
    for package in lock['Python_packages']:
        if package['kind'] != 'sdist':
            continue
        if package['name'] != 'esptool' or package['version'] != '5.6.0' or package['source_build']['build_system'] != {'requires': ['setuptools>=77'], 'build-backend': 'setuptools.build_meta'}:
            raise GateError('Unadmitted source-build backend/package')
        destination = work / 'derived-wheels'
        destination.mkdir()
        command(work, 'build-esptool-wheel', offline_prefix([str(vp), '-m', 'pip', 'wheel', '--no-index', '--no-deps', '--no-build-isolation', '--wheel-dir', str(destination), str(cache / package['filename'])]), env=env)
        built = list(destination.glob('esptool-5.6.0-*.whl'))
        if len(built) != 1:
            raise GateError('Missing unique derived esptool wheel')
        shutil.copyfile(built[0], wheels / built[0].name)
        derived.append({'name': package['name'], 'filename': built[0].name, 'sha256': sha(built[0]), 'source_archive_sha256': package['sha256'], 'kind': 'locally_built_not_publisher_wheel'})
    requirements = work / 'requirements.txt'
    requirements.write_text(''.join('%s==%s --hash=sha256:%s\n' % (row['name'], row['version'], next((item['sha256'] for item in derived if item['name'] == row['name']), row['sha256'])) for row in lock['Python_packages']))
    command(work, 'install-profile', offline_prefix([str(vp), '-m', 'pip', 'install', '--no-index', '--no-deps', '--require-hashes', '-r', str(requirements)]), env=env)
    command(work, 'idf-python-metadata', offline_prefix([str(vp), str(sdk / 'tools/idf_tools.py'), 'install-python-env', '--features', 'core']), env=env)
    installed = json.loads(command(work, 'installed-profile', offline_prefix([str(vp), '-c', 'import importlib.metadata,json;print(json.dumps({d.metadata["Name"].lower().replace("_","-").replace(".","-"):d.version for d in importlib.metadata.distributions()}))']), env=env))
    expected = {row['name']: row['version'] for row in lock['Python_packages']}
    if installed != expected:
        raise GateError('Installed profile differs from exact63 pins')
    check = [str(vp), str(sdk / 'tools/check_python_dependencies.py'), '-r', str(sdk / 'tools/requirements/requirements.core.txt'), '-c']
    command(work, 'upstream-constraints-negative', offline_prefix(check + [str(HERE / constraints['upstream_filename'])]), env=env, expected=1)
    negative = (work / 'receipts/upstream-constraints-negative.stdout').read_text() + (work / 'receipts/upstream-constraints-negative.stderr').read_text()
    if 'cryptography' not in negative or '50.0.0' not in negative:
        raise GateError('Upstream rejection did not expose the specific50 incompatibility')
    command(work, 'local-constraints-positive', offline_prefix(check + [str(HERE / constraints['filename'])]), env=env)
    command(work, 'pip-check', offline_prefix([str(vp), '-m', 'pip', 'check']), env=env)
    dump(work / 'Python-profile.json', {'installed': installed, 'derived': derived, 'upstream_negative': 'Expected original strict checker rejection', 'local_profile': constraints['source']})
    return {'sdk': sdk, 'tools': tools, 'python': vp, 'compiler': compiler, 'cmake': cmake, 'ninja': ninja, 'env': env}


def build_mode(mode: int, lock: dict, paths: dict, work: Path, bwrap: str) -> dict:
    project = work / ('project%d' % mode)
    build = work / ('build%d' % mode)
    project.mkdir()
    for row in lock['project_inputs']:
        source = REPO / row['path']
        if sha(source) != row['sha256']:
            raise GateError('Frozen e984 project input changed: %s' % source)
        target = project / source.relative_to(PROJECT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    ro = [paths['sdk'], paths['tools'], project]
    expected = {'sdk': str(paths['sdk']), 'pin': lock['SDK']['commit'], 'outer_netns': os.readlink('/proc/self/ns/net'), 'uid': os.getuid(), 'euid': os.geteuid(), 'gid': os.getgid(), 'egid': os.getegid(), 'read_only': list(map(str, ro))}
    command(work, 'mode%d-namespace-preflight' % mode, namespace(bwrap, ro, [str(paths['python']), '-c', PREFLIGHT, json.dumps(expected)]), env=paths['env'])
    for root in (build, build / 'bootloader'):
        query = root / '.cmake/api/v1/query'
        query.mkdir(parents=True)
        for kind in ('codemodel-v2', 'cmakeFiles-v1', 'cache-v2', 'toolchains-v1'):
            (query / kind).touch()
    args = [str(paths['python']), str(paths['sdk'] / 'tools/idf.py'), '-C', str(project), '-B', str(build), '-DIDF_TARGET=esp32s3', '-DBOD_RST_SEL=%d' % mode, '-DSDKCONFIG=' + str(build / 'sdkconfig')]
    command(work, 'mode%d-configure' % mode, namespace(bwrap, ro, args + ['reconfigure']), env=paths['env'])
    config = json.loads((build / 'config/sdkconfig.json').read_text())
    flags = {'IDF_TARGET': 'esp32s3', 'FREERTOS_UNICORE': True, 'ESP_DEFAULT_CPU_FREQ_MHZ_160': True, 'ESP_BROWNOUT_DET': False, 'SECURE_BOOT': False, 'SECURE_FLASH_ENC_ENABLED': False}
    if any(config.get(key) != value for key, value in flags.items()) or 'SECURE_ENABLE_TEE' in config:
        raise GateError('Unexpected diagnostic security/target configuration')
    command(work, 'mode%d-build' % mode, namespace(bwrap, ro, args + ['build']), env=paths['env'])
    artifacts = []
    for relative in ('s3_bod_selector.elf', 's3_bod_selector.bin', 's3_bod_selector.map', 'bootloader/bootloader.elf', 'bootloader/bootloader.bin', 'bootloader/bootloader.map'):
        file = build / relative
        artifacts.append({'path': str(file), 'bytes': file.stat().st_size, 'sha256': sha(file)})
    output = command(work, 'mode%d-writer-disassembly' % mode, namespace(bwrap, ro, [str(paths['compiler'] / 'xtensa-esp32s3-elf-objdump'), '-dr', '--disassemble=bod_probe_apply_selector', str(build / 's3_bod_selector.elf')]), env=paths['env']).decode()
    if '600080e8' not in output or 's32i' not in output or 'l32i' not in output or 'memw' not in output:
        raise GateError('Missing actual writer store/barrier/readback witness')
    if mode == 0 and ('f7ffffff' not in output or '\tand\t' not in output):
        raise GateError('Selector0 clear intent differs')
    if mode == 1 and ('8000000' not in output or '\tor\t' not in output):
        raise GateError('Selector1 set intent differs')
    result = {'mode': mode, 'configure_exit': 0, 'build_exit': 0, 'actual_flags': flags, 'artifacts': artifacts, 'source_correspondence': 'Fresh SDK/project and mandatory namespace checks; complete automatic dependency closure check follows in final gate.'}
    dump(work / ('mode%d-result.json' % mode), result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work-dir', type=Path, required=True)
    parser.add_argument('--cache-dir', type=Path, required=True)
    parser.add_argument('--bwrap', default=shutil.which('bwrap'))
    parser.add_argument('--mode', choices=('smoke', 'full'), default='full')
    args = parser.parse_args()
    work, cache = args.work_dir.resolve(), args.cache_dir.resolve()
    if sys.platform != 'linux' or platform.machine() != 'x86_64':
        raise GateError('BLOCKED: only declared Linux x86_64 compile host is supported')
    if not args.bwrap:
        raise GateError('BLOCKED: required host bubblewrap is absent; no isolation fallback')
    inherited = {key: os.environ[key] for key in ('CC', 'CXX', 'CFLAGS', 'CXXFLAGS', 'CPPFLAGS', 'LDFLAGS', 'CMAKE_PREFIX_PATH', 'PYTHONHOME', 'PYTHONPATH', 'IDF_PYTHON_CHECK_CONSTRAINTS') if os.environ.get(key)}
    if inherited:
        raise GateError('Unexpected inherited build overrides: %s' % inherited)
    if args.mode == 'full':
        raise GateError('Full gate implementation pending early smoke; never a green skip')
    if work.exists():
        raise GateError('Fresh empty work directory required; preserve old runs')
    work.mkdir(parents=True)
    cache.mkdir(parents=True, exist_ok=True)
    lock = json.loads((HERE / 'inputs.json').read_text())
    dump(work / 'invocation.json', {'argv': sys.argv, 'input_lock_sha256': sha(HERE / 'inputs.json'), 'bwrap': {'path': str(Path(args.bwrap).resolve()), 'sha256': sha(Path(args.bwrap)), 'version': subprocess.check_output([args.bwrap, '--version'], text=True).strip()}, 'scope': 'Compile-only; no devices, keys, firmware execution or physical qualification'})
    try:
        paths = prepare(lock, work, cache, args.bwrap)
        result = build_mode(0, lock, paths, work, args.bwrap)
        dump(work / 'result.json', {'status': 'PASS_EARLY_MODE0_COMPILE_LINK_ONLY_FINAL_GATE_PENDING', 'result': result, 'physical_qualification': False})
        print('Actual portable mode0 build passed; final closure/0+1+guard2 gate remains pending.')
    except Exception as error:
        dump(work / 'failure.json', {'status': 'FAIL_OR_BLOCKED_NO_FALLBACK', 'error': repr(error), 'physical_qualification': False})
        raise
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (GateError, OSError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
