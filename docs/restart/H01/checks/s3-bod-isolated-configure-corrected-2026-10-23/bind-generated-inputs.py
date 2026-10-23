"""Bind the inspected emitted formats; report incomplete closure, never build."""
import collections
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import tarfile

OUT = Path(__file__).resolve().parent
RUN = Path('/home/tux/nsealr/.restart-tools/goal/h01-s3-bod-source-gate-runtime/isolated-configure-02')
SDK = RUN.parent / 'esp-idf'
BUILD = RUN / 'build'
PROJECT = RUN / 'project'
PREFLIGHT = json.loads((OUT / 'preflight.json').read_text())
COMMAND = json.loads((OUT / 'configure-command.json').read_text())
MAPS = {}


def write(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')


def git_map(repo, commit):
    key = (str(repo), commit)
    if key not in MAPS:
        raw = subprocess.check_output(['git', '-C', str(repo), 'ls-tree', '-rz', commit])
        entries = {}
        for item in raw.split(b'\0'):
            if item:
                metadata, path = item.split(b'\t', 1)
                mode, kind, oid = metadata.decode().split()
                entries[path.decode()] = (mode, kind, oid)
        MAPS[key] = entries
    return MAPS[key]


def bind(path):
    path = Path(os.path.abspath(path))
    row = {'path': str(path)}
    if not path.is_file():
        return {**row, 'status': 'NOT_MATERIALIZED_OR_NOT_FILE'}
    data = path.read_bytes()
    row.update({'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    if path.is_relative_to(SDK):
        relative = path.relative_to(SDK).as_posix()
        repo, commit, lookup = SDK, PREFLIGHT['commit'], relative
        for link in PREFLIGHT['Gitlinks']:
            if relative.startswith(link['path'] + '/'):
                row['Gitlink'] = {'path': link['path'], 'expected': link['expected'], 'state': link['state']}
                if link['state'] != 'pinned' or link['actual_tree_check']['mismatches']:
                    return {**row, 'status': 'UNQUALIFIED_GITLINK'}
                repo, commit = SDK / link['path'], link['expected']
                lookup = path.relative_to(repo).as_posix()
                break
        expected = git_map(repo, commit).get(lookup)
        if not expected or expected[1] != 'blob':
            return {**row, 'status': 'SDK_UNTRACKED_INPUT'}
        mode = '120000' if path.is_symlink() else ('100755' if path.stat().st_mode & stat.S_IXUSR else '100644')
        raw = os.fsencode(os.readlink(path)) if path.is_symlink() else data
        actual = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        row.update({'source_commit': commit, 'source_path': lookup, 'expected_blob': expected[2], 'mode': mode})
        row['status'] = 'EXACT_PINNED_GIT_FILE' if actual == expected[2] and mode == expected[0] else 'SOURCE_MISMATCH'
    elif path.is_relative_to(PROJECT):
        matches = [item for item in COMMAND['probe_inputs'] if Path(item['export']) == path]
        row['status'] = 'EXACT_FROZEN_PROJECT_FILE' if len(matches) == 1 and matches[0]['sha256'] == row['sha256'] else 'UNBOUND_PROJECT_FILE'
        if matches:
            row['source'] = matches[0]
    elif path.is_relative_to(BUILD):
        row['status'] = 'GENERATED_CONFIGURE_OUTPUT_NOT_UPSTREAM_SOURCE'
    else:
        row['status'] = 'HOST_TOOL_OR_ENVIRONMENT_INPUT_HASH_ONLY'
    return row


def main():
    assert COMMAND['exit'] == 0
    index_path = next((BUILD / '.cmake/api/v1/reply').glob('index-*.json'))
    index = json.loads(index_path.read_text())
    reply = index_path.parent
    cmake = json.loads((reply / index['reply']['cmakeFiles-v1']['jsonFile']).read_text())
    model = json.loads((reply / index['reply']['codemodel-v2']['jsonFile']).read_text())
    desc = json.loads((BUILD / 'project_description.json').read_text())
    commands = json.loads((BUILD / 'compile_commands.json').read_text())
    env = json.loads((BUILD / 'config.env').read_text())
    config = json.loads((BUILD / 'config/sdkconfig.json').read_text())
    formats = {
        'inspection_before_this_analyzer': 'Actual stdout/stderr, JSON types/keys/samples, Ninja rules and Kconfig source lines were read first. This script was written afterwards.',
        'project_description': {'type': 'object', 'keys': list(desc), 'build_components': len(desc['build_components']), 'build_component_info': len(desc['build_component_info']), 'all_component_info': len(desc['all_component_info']), 'limit': 'all_component_info is a declared registry, not execution evidence'},
        'compile_commands': {'type': 'array', 'rows': len(commands), 'row_keys': list(commands[0]), 'limit': 'Planned compilation commands, not actual product compilation or preprocessor/header dependency evidence'},
        'file_API': {'objects': index['objects'], 'CMake_input_rows': len(cmake['inputs']), 'input_field_sets': dict(collections.Counter(','.join(sorted(row)) for row in cmake['inputs']))},
        'config_env': {'keys': list(env), 'Kconfig_lists': 'Semicolon-delimited strings; generated kconfigs*.in use source "absolute-path" lines'},
        'Ninja': {'format': 'CMake Ninja3.31 generated rules; CMakeFiles/rules.ninja included', 'bootloader_configure_lines': [382, 384, 385, 386], 'limit': 'ExternalProject configure is a future custom command; no bootloader configuration was executed'},
        'selected_effective_config': {key: config.get(key, 'ABSENT') for key in ('ESP_BROWNOUT_DET', 'SECURE_BOOT', 'SECURE_FLASH_ENC_ENABLED', 'SECURE_ENABLE_TEE', 'FREERTOS_UNICORE', 'ESP_DEFAULT_CPU_FREQ_MHZ_160')},
    }
    write('generated-format-inspection.json', formats)
    refs = collections.defaultdict(list)
    for row in cmake['inputs']:
        path = Path(row['path'])
        refs[str(path if path.is_absolute() else PROJECT / path)].append('CMake_file_API_input')
    for row in commands:
        refs[row['file']].append('planned_compile_source')
    for key in ('COMPONENT_KCONFIGS', 'COMPONENT_KCONFIGS_PROJBUILD', 'COMPONENT_SDKCONFIG_RENAMES'):
        for path in env[key].split(';'):
            if path:
                refs[path].append(key)
    for target in model['configurations'][0]['targets']:
        obj = json.loads((reply / target['jsonFile']).read_text())
        for group in obj.get('compileGroups', []):
            for row in group.get('includes', []):
                # Search directories do not enumerate headers actually consumed.
                refs[row['path']].append('header_search_directory_not_actual_header_set')
    # A fresh redirected Python cache witnesses only imports that emitted bytecode.
    # It is deliberately not a complete Python/native-extension read trace.
    for cached in (RUN / 'pycache').rglob('*.cpython-312.pyc'):
        relative = cached.relative_to(RUN / 'pycache').as_posix()
        source = '/' + re.sub(r'\.cpython-312\.pyc$', '.py', relative)
        refs[source].append('observed_import_bytecode_source_subset')
    refs[COMMAND['argv'][COMMAND['argv'].index('--') + 2]].append('actual_idf_main_script')
    refs[str(SDK / 'components/esp_rom/gen_gdbinit.py')].append('actual_optional_script_failure_in_stderr')
    rows = []
    directories = []
    for path, roles in sorted(refs.items()):
        if set(roles) == {'header_search_directory_not_actual_header_set'}:
            directories.append({'path': path, 'exists': Path(path).is_dir(), 'role': roles[0], 'closure_verified': False})
            continue
        row = bind(path)
        row['roles'] = sorted(set(roles))
        rows.append(row)
    write('available-input-bindings.json', {'rows': rows, 'statuses': dict(collections.Counter(row['status'] for row in rows)), 'header_search_directories': directories,
        'limits': ['Only emitted CMake inputs, planned sources, explicit Kconfig roots/renames and observed Python bytecode sources are included.', 'Nested Kconfig evaluation, main Python scripts/native extensions and actual preprocessor/header reads are not a fully enumerated trace.', 'No bootloader source graph exists yet; no claim unlisted Gitlinks are unused.']})
    inventory = []
    with tarfile.open(OUT / 'configure-output.tar.gz', 'w:gz') as archive:
        for file in sorted(BUILD.rglob('*')):
            if file.is_file():
                assert not file.is_symlink()
                data = file.read_bytes()
                path = file.relative_to(BUILD).as_posix()
                inventory.append({'path': path, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
                archive.add(file, arcname=path, recursive=False)
    write('configure-output-inventory.json', {'archive': 'configure-output.tar.gz', 'files': len(inventory), 'members': inventory,
        'scope': 'Original emitted app configure files and ordinary compiler-identification probes; no product app/bootloader binary was built.'})
    print(json.dumps({'binding_statuses': dict(collections.Counter(row['status'] for row in rows)), 'header_search_directories': len(directories), 'archive_files': len(inventory), 'archive_bytes': (OUT / 'configure-output.tar.gz').stat().st_size}))


if __name__ == '__main__':
    main()
