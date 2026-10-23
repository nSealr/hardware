"""Read-only native artifact/dependency inspection after the one mode0 build."""
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

OUT = Path(__file__).resolve().parent
RUN = Path('/home/tux/nsealr/.restart-tools/goal/h01-s3-bod-source-gate-runtime/mode0-first-build-01')
SOURCE = json.loads((OUT / 'source-receipt.json').read_text())
PREFIX = SOURCE['build_argv'][:SOURCE['build_argv'].index('--') + 1]
TOOL = RUN.parent / 'idf-tools/tools/xtensa-esp-elf/esp-15.2.0_20251204/xtensa-esp-elf/bin'
NINJA = RUN.parent / 'idf-tools/tools/ninja/1.12.1/ninja'


def main():
    assert json.loads((OUT / 'build-command.json').read_text())['exit'] == 0
    env = os.environ.copy()
    env.update(SOURCE['environment_overrides'])
    planned = []
    for label, directory, elf in [('app', RUN / 'build', 's3_bod_selector.elf'), ('bootloader', RUN / 'build/bootloader', 'bootloader.elf')]:
        planned.extend([
            (label + '-ninja-deps', [str(NINJA), '-C', str(directory), '-t', 'deps']),
            (label + '-ninja-commands', [str(NINJA), '-C', str(directory), '-t', 'commands', 'all']),
            (label + '-readelf', [str(TOOL / 'xtensa-esp32s3-elf-readelf'), '-h', str(directory / elf)]),
            (label + '-nm', [str(TOOL / 'xtensa-esp32s3-elf-nm'), '-a', str(directory / elf)]),
        ])
    for symbol in ['bod_probe_apply_selector', 'app_main']:
        planned.append(('app-disassembly-' + symbol, [str(TOOL / 'xtensa-esp32s3-elf-objdump'), '-dr', '--disassemble=' + symbol, str(RUN / 'build/s3_bod_selector.elf')]))
    receipts = []
    for name, command in planned:
        target = OUT / (name + '.stdout.gz')
        assert not target.exists(), 'One read-only capture per named command'
        start = time.time()
        done = subprocess.run(PREFIX + command, env=env, capture_output=True)
        target.write_bytes(gzip.compress(done.stdout, mtime=0))
        (OUT / (name + '.stderr.log')).write_bytes(done.stderr)
        receipts.append({'name': name, 'argv': PREFIX + command, 'exit': done.returncode,
                         'duration_seconds': time.time() - start,
                         'stdout_uncompressed_bytes': len(done.stdout), 'stdout_uncompressed_sha256': hashlib.sha256(done.stdout).hexdigest(),
                         'stdout_gzip': target.name, 'stderr': name + '.stderr.log'})
        assert done.returncode == 0, receipts[-1]
    (OUT / 'read-only-command-receipts.json').write_text(json.dumps(receipts, indent=2) + '\n')
    print(json.dumps([{'name': row['name'], 'exit': row['exit'], 'stdout_bytes': row['stdout_uncompressed_bytes']} for row in receipts]))


if __name__ == '__main__':
    main()
