"""Bind emitted build dependencies to explicit SDK/project/archive producers.

Inputs are passed by the controller. This does not import historical proof or
infer execution from a component inventory, and is not an OS file-read tracer.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import tarfile
import zipfile


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def absolute(path, base):
    return Path(os.path.abspath(path if Path(path).is_absolute() else base / path))


def dependency_blocks(text):
    require(bool(text.strip()), 'Empty compiler dependency output')
    result = []
    for block in text.strip().split('\n\n'):
        lines = block.splitlines()
        match = re.fullmatch(r'(.+): #deps (\d+), deps mtime \d+ \(VALID\)', lines[0])
        require(match is not None, 'Malformed/stale Ninja dependency block: ' + lines[0])
        require(all(line.startswith('    ') for line in lines[1:]), 'Malformed dependency path')
        dependencies = [line[4:] for line in lines[1:]]
        require(len(dependencies) == int(match[2]), 'Dependency count differs')
        result.append({'object': match[1], 'dependencies': dependencies})
    require(len({row['object'] for row in result}) == len(result), 'Duplicate dependency object')
    return result


def verify_archive(archive, root):
    """Compare all extracted files, links and owner-exec bits to publisher bytes."""
    rows = {}
    if archive.name.endswith('.zip'):
        with zipfile.ZipFile(archive) as source:
            for item in source.infolist():
                if item.is_dir():
                    continue
                rows[item.filename] = {'kind': 'file', 'sha256': hashlib.sha256(source.read(item)).hexdigest(), 'owner_exec': bool((item.external_attr >> 16) & 0o100)}
    else:
        with tarfile.open(archive, 'r:*') as source:
            for item in source:
                if item.isdir():
                    continue
                if item.isfile():
                    rows[item.name] = {'kind': 'file', 'sha256': hashlib.file_digest(source.extractfile(item), 'sha256').hexdigest(), 'owner_exec': bool(item.mode & 0o100)}
                elif item.issym():
                    rows[item.name] = {'kind': 'symlink', 'target': item.linkname}
                elif item.islnk():
                    rows[item.name] = {'kind': 'hardlink', 'target': item.linkname, 'owner_exec': bool(item.mode & 0o100)}
                else:
                    raise ValueError('Unexpected archive member: ' + item.name)
    actual = {file.relative_to(root).as_posix() for file in root.rglob('*') if file.is_file() or file.is_symlink()}
    require(actual == set(rows), 'Extracted archive has missing/extra files: ' + str(root))
    bound = {}
    for name, row in rows.items():
        file = root / name
        if row['kind'] == 'symlink':
            require(file.is_symlink() and os.readlink(file) == row['target'], 'Archive symlink differs: ' + str(file))
        else:
            target, seen = row, set()
            while target['kind'] == 'hardlink':
                require(target['target'] not in seen, 'Archive hardlink cycle')
                seen.add(target['target'])
                target = rows[target['target']]
            require(not file.is_symlink() and digest(file) == target['sha256'] and bool(file.stat().st_mode & 0o100) == row['owner_exec'], 'Archive file/mode differs: ' + str(file))
        bound[str(file)] = {**row, 'archive_sha256': digest_cached(archive)}
    return bound


_archive_hashes = {}


def digest_cached(path):
    key = str(path)
    if key not in _archive_hashes:
        _archive_hashes[key] = digest(path)
    return _archive_hashes[key]


def verify_wheels(lock, wheels, site, derived):
    """Verify installed library members against actual authenticated wheel bytes.

    Pip-generated RECORD/INSTALLER/direct_url are not publisher library bodies.
    Wheel data scripts are bound with only pip's exact #!python replacement by
    this run's venv interpreter; the transformation is explicitly recorded.
    """
    bound, packages = {}, []
    for package in lock['Python_packages']:
        selected = next((item for item in derived if item['name'] == package['name']), package)
        wheel = wheels / selected['filename']
        require(digest(wheel) == selected['sha256'], 'Staged wheel changed')
        count = 0
        with zipfile.ZipFile(wheel) as archive:
            for name in archive.namelist():
                if name.endswith('/') or name.endswith('.dist-info/RECORD'):
                    continue
                target_name = name
                body = archive.read(name)
                transformation = None
                if '.data/' in name:
                    _, role, rest = name.split('/', 2)
                    if role == 'scripts':
                        require(body.startswith(b'#!python\n'), 'Unknown wheel script transformation')
                        interpreter = site.parents[2] / 'bin/python'
                        target = site.parents[2] / 'bin' / rest
                        body = ('#!' + str(interpreter) + '\n').encode() + body.split(b'\n', 1)[1]
                        transformation = 'Exact pip #!python replacement with this venv interpreter; body otherwise byte-identical'
                    elif role in ('purelib', 'platlib'):
                        target = site / rest
                    else:
                        raise ValueError('Unresolved wheel data role: ' + role)
                else:
                    target = site / target_name
                expected = hashlib.sha256(body).hexdigest()
                require(target.is_file() and digest(target) == expected, 'Installed publisher library/script file differs: ' + str(target))
                require(str(target) not in bound, 'Overlapping wheel library file')
                bound[str(target)] = {'package': package['name'], 'version': package['version'], 'sha256': expected, 'archive_sha256': selected['sha256'], 'wheel_member': name, 'installed_transformation': transformation, 'origin': 'derived_exact_sdist' if package['kind'] == 'sdist' else 'publisher_wheel'}
                count += 1
        packages.append({'name': package['name'], 'version': package['version'], 'wheel_sha256': selected['sha256'], 'library_members_verified': count, 'origin': package['kind']})
    return bound, packages


def bind_mode(mode, lock, paths, work, command, sandbox):
    sdk, project, build = paths['sdk'], work / ('project%d' % mode), work / ('build%d' % mode)
    refs, evidence, executed = defaultdict(set), {}, {}
    for label, directory in [('app', build), ('bootloader', build / 'bootloader')]:
        commands = json.loads((directory / 'compile_commands.json').read_text())
        deps = command(work, 'mode%d-%s-deps' % (mode, label), sandbox([str(paths['ninja'] / 'ninja'), '-C', str(directory), '-t', 'deps']), env=paths['env']).decode()
        recipes = command(work, 'mode%d-%s-recipes' % (mode, label), sandbox([str(paths['ninja'] / 'ninja'), '-C', str(directory), '-t', 'commands', 'all']), env=paths['env']).decode()
        blocks = dependency_blocks(deps)
        objects = {absolute(row['object'], directory) for row in blocks}
        require(objects == {absolute(row['output'], directory) for row in commands} and len(blocks) == len(commands), 'Not every compile command has actual VALID dependencies')
        log = (directory / '.ninja_log').read_text().splitlines()
        require(log[0] == '# ninja log v6', 'Unexpected Ninja execution log format')
        for line in log[1:]:
            fields = line.split('\t')
            require(len(fields) == 5, 'Malformed Ninja execution log')
            executed[str(absolute(fields[3], directory))] = {'scope': label, 'start': fields[0], 'end': fields[1], 'mtime': fields[2], 'command_hash_not_crypto_digest': fields[4]}
        require(all(str(obj) in executed and obj.is_file() for obj in objects), 'Compiler object missing from execution log')
        for row in blocks:
            for path in row['dependencies']:
                refs[str(absolute(path, directory))].add(label + ':actual_compiler_dependency')
        for row in commands:
            refs[str(absolute(row['file'], directory))].add(label + ':compiled_source')
            # Bind response files as inputs rather than silently treating @file as flags.
            for token in shlex.split(row['command']):
                if token.startswith('@'):
                    refs[str(absolute(token[1:], directory))].add(label + ':compiler_response_file')
        api = directory / '.cmake/api/v1/reply'
        indices = list(api.glob('index-*.json'))
        require(len(indices) == 1, 'Expected one fresh CMake file-API index')
        index = json.loads(indices[0].read_text())
        files = json.loads((api / index['reply']['cmakeFiles-v1']['jsonFile']).read_text())
        for row in files['inputs']:
            refs[str(absolute(row['path'], Path(files['paths']['source'])))].add(label + ':CMake_input')
        config = json.loads((directory / 'config.env').read_text())
        for key in ('COMPONENT_KCONFIGS', 'COMPONENT_KCONFIGS_PROJBUILD', 'COMPONENT_SDKCONFIG_RENAMES'):
            for path in config[key].split(';'):
                if path:
                    refs[path].add(label + ':' + key)
        for line in recipes.splitlines():
            for token in shlex.split(line):
                candidate = token.split('=', 1)[-1]
                if candidate.startswith(str(sdk) + '/') and Path(candidate).is_file():
                    refs[candidate].add(label + ':selected_recipe_source')
        loads = [line[5:] for line in (directory / ('s3_bod_selector.map' if label == 'app' else 'bootloader.map')).read_text().splitlines() if line.startswith('LOAD ')]
        for path in loads:
            refs[str(absolute(path, directory))].add(label + ':actual_link_map_LOAD')
        evidence[label] = {'compile_commands': len(commands), 'VALID_actual_dependency_blocks': len(blocks), 'objects_in_execution_log': len(objects), 'CMake_inputs': len(files['inputs']), 'link_map_LOAD_rows': len(loads), 'Ninja_log_sha256': digest(directory / '.ninja_log')}
    for cached in (work / 'build-pycache').rglob('*.cpython-312.pyc'):
        path = '/' + re.sub(r'\.cpython-312\.pyc$', '.py', cached.relative_to(work / 'build-pycache').as_posix())
        refs[path].add('observed_import_source_subset')
    refs[str(sdk / 'tools/idf.py')].add('actual_main_script')
    refs[str(sdk / 'components/esp_rom/gen_gdbinit.py')].add('actual_optional_script_warning')
    git_maps = paths['git_maps']
    rows = []
    for name, roles in sorted(refs.items()):
        file = Path(name)
        require(file.is_file(), 'Missing/non-file input: ' + name)
        row = {'path': name, 'sha256': digest(file), 'bytes': file.stat().st_size, 'roles': sorted(roles)}
        if file.is_relative_to(sdk):
            if name == str(sdk / '.git/HEAD'):
                require(file.read_text().strip() == lock['SDK']['commit'], 'SDK HEAD changed')
                row['status'] = 'EXACT_DETACHED_GIT_METADATA_NOT_SOURCE'
            else:
                origin = next(((root, commit, mapping) for root, commit, mapping in git_maps if file.is_relative_to(root)), None)
                require(origin is not None, 'No pinned SDK source origin: ' + name)
                root, commit, mapping = origin
                entry = mapping.get(file.relative_to(root).as_posix())
                require(entry is not None and entry[1] == 'blob', 'Untracked/unpinned SDK input: ' + name)
                raw = os.fsencode(os.readlink(file)) if file.is_symlink() else file.read_bytes()
                mode_actual = '120000' if file.is_symlink() else ('100755' if file.stat().st_mode & 0o100 else '100644')
                require(hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == entry[2] and mode_actual == entry[0], 'SDK input blob/mode differs: ' + name)
                row.update(status='EXACT_PINNED_GIT_FILE', source_commit=commit, source_path=file.relative_to(root).as_posix(), blob=entry[2], mode=entry[0])
        elif file.is_relative_to(project):
            expected = {str(project / Path(item['path']).relative_to('diagnostics/s3-bod-selector')): item for item in lock['project_inputs']}
            require(name in expected and row['sha256'] == expected[name]['sha256'], 'Unbound diagnostic input')
            row.update(status='EXACT_FROZEN_PROJECT_FILE', original_source=expected[name]['path'])
        elif file.is_relative_to(build):
            row.update(status='GENERATED_NOT_UPSTREAM_SOURCE', execution_log=executed.get(name), producer='actual_Ninja_recipe' if name in executed else 'actual_CMake_Kconfig_configure', producer_receipts=['mode%d-configure' % mode, 'mode%d-build' % mode])
        elif name in paths['archive_bindings']:
            row.update(status='EXACT_PUBLISHER_TOOL_ASSET_FILE', origin=paths['archive_bindings'][name])
        elif name in paths['wheel_bindings']:
            row.update(status='EXACT_INSTALLED_AUTHENTICATED_WHEEL_BODY', origin=paths['wheel_bindings'][name])
        else:
            raise ValueError('Unknown/unbound producer input: ' + name)
        rows.append(row)
    result = {'mode': mode, 'formats': evidence, 'statuses': dict(Counter(row['status'] for row in rows)), 'rows': rows, 'limits': 'Actual compile/header dependencies, file API, Kconfig lists, map LOAD inputs, selected recipes and observed imports with producer identities. No syscall-complete OS read trace, binary reproducibility or physical qualification.'}
    (work / ('mode%d-closure.json' % mode)).write_text(json.dumps(result, indent=2) + '\n')
    return {key: value for key, value in result.items() if key != 'rows'}
