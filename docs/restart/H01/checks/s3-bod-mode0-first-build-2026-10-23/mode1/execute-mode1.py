"""The original admitted selector1 obligation; reuse the mode0 mechanisms."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

OUT = Path(__file__).resolve().parent
BASE = OUT.parent
RUN = Path('/home/tux/nsealr/.restart-tools/goal/h01-s3-bod-source-gate-runtime/mode1-first-build-01')
sys.dont_write_bytecode = True


def load(name):
    spec = importlib.util.spec_from_file_location('reused_' + name.replace('-', '_'), BASE / name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(stage):
    assert json.loads((BASE / 'mode0-source-closure.json').read_text())['status'] == 'PASS_MODE0_BUILD_INPUT_SOURCE_CORRESPONDENCE_IN_EXACT_RECORDED_TOOL_ENVIRONMENT'
    if stage in ('prepare', 'configure', 'build'):
        module = load('execute.py')
        module.OUT, module.RUN = OUT, RUN
        if stage == 'prepare':
            module.prepare()
            path = OUT / 'source-receipt.json'
            source = json.loads(path.read_text())
            for key in ('configure_argv', 'build_argv'):
                assert source[key].count('-DBOD_RST_SEL=0') == 1
                source[key] = ['-DBOD_RST_SEL=1' if item == '-DBOD_RST_SEL=0' else item for item in source[key]]
            source['selected_mode'] = 1
            source['extension_authority'] = 'Explicit coordinator extension after successful mode0/closure: original9e9 selector1 and true selector2 guard only; no new hardware/source/security/budget scope.'
            source['mode0_closure_sha256'] = hashlib.sha256((BASE / 'mode0-source-closure.json').read_bytes()).hexdigest()
            source['reused_execute_source_sha256'] = hashlib.sha256((BASE / 'execute.py').read_bytes()).hexdigest()
            source['mode1_driver_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
            source['stop'] = 'One mode1 configure/build; source/config identical apart from selector and output paths. First error/unknown source stops; no firmware/CI/physical use.'
            path.write_text(json.dumps(source, indent=2) + '\n')
        else:
            module.execute(stage)
    elif stage == 'capture':
        module = load('capture-output.py')
        module.OUT, module.RUN = OUT, RUN
        module.SOURCE = json.loads((OUT / 'source-receipt.json').read_text())
        module.PREFIX = module.SOURCE['build_argv'][:module.SOURCE['build_argv'].index('--') + 1]
        module.main()
    elif stage == 'bind':
        module = load('bind-mode0.py')
        module.OUT, module.RUN, module.BUILD, module.PROJECT = OUT, RUN, RUN / 'build', RUN / 'project'
        module.main()
        # The reused algorithm's historical basename is not the evidence role.
        # These are freshly collected selector1 paths/bytes, never copied mode0 output.
        path = OUT / 'mode0-input-bindings.json'
        data = json.loads(path.read_text())
        path.rename(OUT / 'mode1-input-bindings.json')
        baseline = json.loads((BASE / 'mode0-input-bindings.json').read_text())
        old_host = {row['path']: row['sha256'] for row in baseline['rows'] if row['status'] == 'HOST_TOOL_OR_ENVIRONMENT_INPUT_HASH_ONLY'}
        host = [row for row in data['rows'] if row['status'] == 'HOST_TOOL_OR_ENVIRONMENT_INPUT_HASH_ONLY']
        assert all(old_host.get(row['path']) == row['sha256'] for row in host)
        reference = {'role': 'Exact existing host producer identities reused by path/hash; fresh mode1 source/header/link and generated file hashes above, actual commands/logs/config under mode1 output tree.',
                     'mode0_producer_bindings_sha256': hashlib.sha256((BASE / 'producer-bindings.json').read_bytes()).hexdigest(),
                     'host_rows_identical_to_mode0': len(host), 'new_host_producers': [],
                     'reused_binder_source_sha256': hashlib.sha256((BASE / 'bind-mode0.py').read_bytes()).hexdigest(),
                     'qualification': 'No copied runtime pass, reproducibility or physical claim. Same admitted read-only Python/CMake environment and official toolchain; actual selector1 dependencies/ELF are separate.'}
        (OUT / 'producer-reference.json').write_text(json.dumps(reference, indent=2) + '\n')
    else:
        raise AssertionError(stage)


if __name__ == '__main__':
    main(sys.argv[1])
