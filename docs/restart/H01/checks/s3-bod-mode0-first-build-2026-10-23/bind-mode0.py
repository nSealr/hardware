"""Bind actual mode0 dependencies to fixed source/official tool bytes; no build."""
import collections
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import shlex
import stat
import subprocess
import sys
import tarfile
import zipfile

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[4]
RUN = Path('/home/tux/nsealr/.restart-tools/goal/h01-s3-bod-source-gate-runtime/mode0-first-build-01')
SDK = RUN.parent / 'esp-idf'
BUILD = RUN / 'build'
PROJECT = RUN / 'project'
TOOL_ROOT = RUN.parent / 'idf-tools/tools/xtensa-esp-elf/esp-15.2.0_20251204/xtensa-esp-elf'


def digest_file(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')


def main():
    source = json.loads((OUT / 'source-receipt.json').read_text())
    assert json.loads((OUT / 'build-command.json').read_text())['exit'] == 0
    spec = importlib.util.spec_from_file_location('historical_bind', REPO / 'docs/restart/H01/checks/s3-bod-isolated-configure-corrected-2026-10-23/bind-generated-inputs.py')
    helper = importlib.util.module_from_spec(spec)
    sys.dont_write_bytecode = True
    spec.loader.exec_module(helper)
    helper.RUN, helper.SDK, helper.BUILD, helper.PROJECT = RUN, SDK, BUILD, PROJECT
    helper.PREFLIGHT = json.loads((OUT / 'SDK-preflight.json').read_text())
    helper.COMMAND = {'probe_inputs': source['project_inputs']}
    refs = collections.defaultdict(set)
    evidence = {}
    for label, directory in [('app', BUILD), ('bootloader', BUILD / 'bootloader')]:
        commands = json.loads((directory / 'compile_commands.json').read_text())
        # The printed Ninja deps format was inspected before this parser.
        raw = gzip.decompress((OUT / (label + '-ninja-deps.stdout.gz')).read_bytes()).decode()
        blocks = []
        for block in raw.strip().split('\n\n'):
            lines = block.splitlines()
            match = re.fullmatch(r'(.+): #deps (\d+), deps mtime \d+ \(VALID\)', lines[0])
            assert match, lines[0]
            paths = [line[4:] for line in lines[1:]]
            assert all(line.startswith('    ') for line in lines[1:])
            assert len(paths) == int(match[2])
            blocks.append({'object': match[1], 'dependencies': paths})
            for path in paths:
                refs[str(Path(os.path.abspath(path if Path(path).is_absolute() else directory / path)))].add(label + ':actual_compiler_dependency')
        objects = {str(Path(os.path.abspath(directory / row['object']))) for row in blocks}
        expected_objects = {str(Path(os.path.abspath(directory / row['output']))) for row in commands}
        assert objects == expected_objects and len(blocks) == len(commands)
        for row in commands:
            assert (directory / row['output']).is_file()
            refs[row['file']].add(label + ':compiled_source')
        api = directory / '.cmake/api/v1/reply'
        indices = sorted(api.glob('index-*.json'))
        assert len(indices) == 1
        index = json.loads(indices[0].read_text())
        files = json.loads((api / index['reply']['cmakeFiles-v1']['jsonFile']).read_text())
        for row in files['inputs']:
            path = Path(row['path'])
            refs[str(path if path.is_absolute() else Path(files['paths']['source']) / path)].add(label + ':CMake_configure_input')
        env = json.loads((directory / 'config.env').read_text())
        for key in ('COMPONENT_KCONFIGS', 'COMPONENT_KCONFIGS_PROJBUILD', 'COMPONENT_SDKCONFIG_RENAMES'):
            for path in env[key].split(';'):
                if path:
                    refs[path].add(label + ':' + key)
        recipe_lines = gzip.decompress((OUT / (label + '-ninja-commands.stdout.gz')).read_bytes()).decode().splitlines()
        for line in recipe_lines:
            for token in shlex.split(line):
                candidate = token.split('=', 1)[-1]
                if candidate.startswith(str(SDK) + '/') and Path(candidate).is_file():
                    refs[candidate].add(label + ':selected_build_recipe_file')
        map_path = directory / ('s3_bod_selector.map' if label == 'app' else 'bootloader.map')
        loads = [line[5:] for line in map_path.read_text().splitlines() if line.startswith('LOAD ')]
        for path in loads:
            refs[str(Path(os.path.abspath(path if Path(path).is_absolute() else directory / path)))].add(label + ':actual_linker_map_LOAD')
        desc = json.loads((directory / 'project_description.json').read_text())
        evidence[label] = {'compile_commands': len(commands), 'actual_VALID_dependency_blocks': len(blocks), 'every_compiled_object_covered': True,
                          'CMake_input_rows': len(files['inputs']), 'link_map_LOAD_rows': len(loads), 'build_components': len(desc['build_components'])}
    for cached in (RUN / 'pycache').rglob('*.cpython-312.pyc'):
        path = '/' + re.sub(r'\.cpython-312\.pyc$', '.py', cached.relative_to(RUN / 'pycache').as_posix())
        refs[path].add('observed_Python_import_source_subset')
    refs[str(SDK / 'tools/idf.py')].add('actual_IDF_main_script')
    refs[str(SDK / 'components/esp_rom/gen_gdbinit.py')].add('actual_optional_script_warning')
    # Whole SDK tracked root and correctly pinned child trees are independently
    # byte-checked. This also binds their Kconfig/Python sources, not just C files.
    check_spec = importlib.util.spec_from_file_location('historical_preflight', REPO / 'docs/restart/H01/checks/s3-bod-isolated-configure-2026-10-23/preflight-and-configure.py')
    pre = importlib.util.module_from_spec(check_spec)
    check_spec.loader.exec_module(pre)
    post, links = pre.tree_check(SDK, source['SDK_commit'])
    assert not post['mismatches'] and post['checked_rows_sha256'] == helper.PREFLIGHT['checked_rows_sha256']
    post['Gitlink_status'] = subprocess.check_output(['git', '-C', str(SDK), 'submodule', 'status']).decode().splitlines()
    prior_status = json.loads((REPO / 'docs/restart/H01/checks/s3-bod-isolated-configure-corrected-2026-10-23/post-configure-source-check.json').read_text())['Gitlink_status']
    assert post['Gitlink_status'] == prior_status
    post['root_untracked_including_ignored'] = subprocess.check_output(['git', '-C', str(SDK), 'ls-files', '--others', '-z']).decode().strip('\0').split('\0')
    assert all(path.endswith('.pyc') and '/__pycache__/' in path for path in post['root_untracked_including_ignored'])
    post['cache_boundary'] = 'Only two old ignored python_version_checker pyc files exist in SDK. Actual commands redirect Python cache to the fresh task prefix; these old files are not selected by that prefix.'
    write('SDK-post-build.json', post)
    archive_path = Path(source['original_archive_receipts'][0]['argv'][source['original_archive_receipts'][0]['argv'].index('--output') + 1])
    assert digest_file(archive_path) == source['original_archive_receipts'][0]['asset']['sha256']
    expected = {}
    with tarfile.open(archive_path, 'r|xz') as archive:
        for member in archive:
            parts = PurePosixPath(member.name).parts
            assert parts[0] == 'xtensa-esp-elf' and '..' not in parts
            name = '/'.join(parts[1:])
            if member.isfile():
                expected[name] = {'kind': 'file', 'sha256': hashlib.file_digest(archive.extractfile(member), 'sha256').hexdigest(), 'owner_executable': bool(member.mode & 0o100)}
            elif member.issym():
                expected[name] = {'kind': 'symlink', 'target': member.linkname}
            elif member.islnk():
                expected[name] = {'kind': 'hardlink', 'target': '/'.join(PurePosixPath(member.linkname).parts[1:]), 'owner_executable': bool(member.mode & 0o100)}
            else:
                assert member.isdir()
    checked = []
    for name, info in expected.items():
        file = TOOL_ROOT / name
        if info['kind'] == 'symlink':
            assert file.is_symlink() and os.readlink(file) == info['target']
            checked.append({'path': name, **info, 'match': True})
        else:
            target = info
            seen = set()
            while target['kind'] == 'hardlink':
                assert target['target'] not in seen
                seen.add(target['target'])
                target = expected[target['target']]
            assert target['kind'] == 'file'
            actual = digest_file(file)
            assert actual == target['sha256'] and bool(file.stat().st_mode & 0o100) == info['owner_executable'], name
            checked.append({'path': name, 'sha256': actual, 'kind': info['kind'], 'match': True})
    actual_names = {file.relative_to(TOOL_ROOT).as_posix() for file in TOOL_ROOT.rglob('*') if file.is_file() or file.is_symlink()}
    assert actual_names == set(expected)
    (OUT / 'toolchain-file-correspondence.json.gz').write_bytes(gzip.compress(json.dumps({'official_archive_sha256': digest_file(archive_path), 'rows': checked}, separators=(',', ':')).encode(), mtime=0))
    ninja_archive = source['original_archive_receipts'][1]
    zip_path = Path(ninja_archive['argv'][ninja_archive['argv'].index('--output') + 1])
    assert digest_file(zip_path) == ninja_archive['asset']['sha256']
    with zipfile.ZipFile(zip_path) as archive:
        assert hashlib.sha256(archive.read('ninja')).hexdigest() == digest_file(RUN.parent / 'idf-tools/tools/ninja/1.12.1/ninja')
    rows = []
    for path, roles in sorted(refs.items()):
        row = helper.bind(path)
        row['roles'] = sorted(roles)
        file = Path(row['path'])
        if file.is_relative_to(TOOL_ROOT):
            assert file.relative_to(TOOL_ROOT).as_posix() in expected
            row['status'] = 'EXACT_OFFICIAL_TOOLCHAIN_ARCHIVE_FILE'
            row['archive_sha256'] = source['original_archive_receipts'][0]['asset']['sha256']
        if row['path'] == str(SDK / '.git/HEAD'):
            assert file.read_text().strip() == source['SDK_commit']
            row['status'] = 'EXACT_DETACHED_SDK_GIT_METADATA_NOT_SOURCE_BLOB'
        rows.append(row)
    data = {'emitted_format_evidence': evidence, 'rows': rows, 'statuses': dict(collections.Counter(row['status'] for row in rows)),
            'official_toolchain_whole_tree_files': len(checked), 'whole_toolchain_archive_byte_correspondence': True, 'ninja_official_archive_byte_correspondence': True,
            'qualification_limit': 'CMake inputs, every compiled object dependency record, map LOAD files, recipe source arguments and observed Python imports are evidence with different roles. No OS syscall-complete file-read trace or physical qualification is claimed.'}
    write('mode0-input-bindings.json', data)
    print(json.dumps({key: value for key, value in data.items() if key != 'rows'}))


if __name__ == '__main__':
    main()
