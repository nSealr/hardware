"""Execute only the independently specified selector2 CMake guard rejection."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[4]
RUN = Path('/home/tux/nsealr/.restart-tools/goal/h01-s3-bod-source-gate-runtime/selector2-rejection-01')


def main(stage):
    path = OUT / 'selector2-command.json'
    if stage == 'prepare':
        assert not RUN.exists() and not path.exists()
        source = json.loads((OUT / 'source-receipt.json').read_text())
        old_run = str(RUN.parent / 'mode0-first-build-01')
        argv = [item.replace(old_run, str(RUN)).replace('-DBOD_RST_SEL=0', '-DBOD_RST_SEL=2') for item in source['configure_argv']]
        env = {key: value.replace(old_run, str(RUN)) for key, value in source['environment_overrides'].items()}
        inputs = []
        for item in source['project_inputs']:
            data = subprocess.check_output(['git', '-C', str(REPO), 'show', item['source_commit'] + ':' + item['path']])
            assert hashlib.sha256(data).hexdigest() == item['sha256']
            target = Path(item['export'].replace(old_run, str(RUN)))
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            target.chmod(0o644)
            inputs.append({**item, 'export': str(target)})
        record = {'source_commit': source['source_commit'], 'argv': argv, 'environment_overrides': env, 'project_inputs': inputs,
                  'independent_expectations': 'db1a2fc8a48b40effbcaeed8961dafe9a574cea7:docs/restart/H01/s3-bod-build-expectations.json selectors.other',
                  'expected': {'idf_py_exit': 2, 'guard': 'CMakeLists.txt:4 literal BOD_RST_SEL rejection before SDK project include', 'product_compile_or_link': False}}
        path.write_text(json.dumps(record, indent=2) + '\n')
        print('Prepared immutable selector2 expectation/command only; not executed.')
    else:
        assert stage == 'run'
        record = json.loads(path.read_text())
        assert 'exit' not in record
        for item in record['project_inputs']:
            assert hashlib.sha256(Path(item['export']).read_bytes()).hexdigest() == item['sha256']
        env = os.environ.copy()
        env.update(record['environment_overrides'])
        start = time.time()
        with (OUT / 'selector2.stdout.log').open('wb') as stdout, (OUT / 'selector2.stderr.log').open('wb') as stderr:
            done = subprocess.run(record['argv'], env=env, stdout=stdout, stderr=stderr)
        record.update({'exit': done.returncode, 'started_unix': start, 'duration_seconds': time.time() - start})
        path.write_text(json.dumps(record, indent=2) + '\n')
        assert done.returncode == 2
        stderr = (OUT / 'selector2.stderr.log').read_text()
        assert 'CMake Error at CMakeLists.txt:4 (message):' in stderr
        assert 'BOD_RST_SEL must be explicitly 0 or 1' in stderr
        assert not (RUN / 'build/build.ninja').exists() and not (RUN / 'build/sdkconfig').exists()
        print(json.dumps({'exit': done.returncode, 'expected_CMake_guard_observed': True, 'duration_seconds': record['duration_seconds']}))


if __name__ == '__main__':
    main(sys.argv[1])
