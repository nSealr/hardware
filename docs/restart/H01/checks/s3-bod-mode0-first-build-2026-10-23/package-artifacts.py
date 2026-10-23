"""Preserve actual linked images/maps/configs and compare the two fixed modes."""
import gzip
import hashlib
import json
from pathlib import Path
import tarfile

OUT = Path(__file__).resolve().parent
RUNTIME = Path('/home/tux/nsealr/.restart-tools/goal/h01-s3-bod-source-gate-runtime')


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    inventory = []
    artifacts = []
    summaries = []
    configs = {}
    with tarfile.open(OUT / 'linked-artifacts-and-configs.tar.gz', 'w:gz') as archive:
        for mode, proof in [(0, OUT), (1, OUT / 'mode1')]:
            root = RUNTIME / ('mode%d-first-build-01/build' % mode)
            assert json.loads((proof / 'build-command.json').read_text())['exit'] == 0
            rows = []
            for file in sorted(root.rglob('*')):
                if not file.is_file():
                    continue
                assert not file.is_symlink()
                relative = file.relative_to(root).as_posix()
                retained = file.suffix not in ('.a', '.o', '.obj') and file.name != 'a.out'
                item = {'mode': mode, 'path': relative, 'bytes': file.stat().st_size, 'sha256': sha(file), 'preserved_in_archive': retained}
                inventory.append(item)
                if retained:
                    archive.add(file, arcname='mode%d/%s' % (mode, relative), recursive=False)
                if relative in ('s3_bod_selector.elf', 's3_bod_selector.bin', 's3_bod_selector.map', 'bootloader/bootloader.elf', 'bootloader/bootloader.bin', 'bootloader/bootloader.map', 'partition_table/partition-table.bin', 'sdkconfig', 'config/sdkconfig.h', 'config/sdkconfig.json', 'bootloader/config/sdkconfig.json'):
                    artifacts.append({**item, 'runtime_path': str(file), 'archive_member': 'mode%d/%s' % (mode, relative)})
            for target, directory in [('app', root), ('bootloader', root / 'bootloader')]:
                configs[(mode, target)] = json.loads((directory / 'config/sdkconfig.json').read_text())
                nm = gzip.decompress((proof / (target + '-nm.stdout.gz')).read_bytes()).decode().splitlines()
                names = {line.split()[-1] for line in nm if line.split()}
                assert 'esp_brownout_init' not in names and 'rtc_brownout_isr_handler' not in names
                if target == 'app':
                    assert 'bod_probe_apply_selector' in names and 'app_main' in names and '__esp_sys_init_fn_init_brownout' in names
                rows.append({'target': target, 'linked_esp_brownout_init': False, 'linked_optional_rtc_brownout_isr_handler': False, 'linked_startup_init_wrapper': '__esp_sys_init_fn_init_brownout' in names})
            summaries.append({'mode': mode, 'symbols': rows})
    assert configs[(0, 'app')] == configs[(1, 'app')]
    assert configs[(0, 'bootloader')] == configs[(1, 'bootloader')]
    compare = {'app_config_values_identical': len(configs[(0, 'app')]), 'bootloader_config_values_identical': len(configs[(0, 'bootloader')]),
               'selector0': 'Actual linked AND with0xf7ffffff, register0x600080e8, store/memw/readback; called byapp_main.',
               'selector1': 'Actual linked OR with0x08000000, same register/store/memw/readback andactualapp_maincall.',
               'startup': 'The init_brownout callback remains registered, with actual disassembly entry/rsil3/rsil0/return0. Its esp_brownout_init call and optional ISR are not linked. flash_brownout hooks remain. No blanket absence of all brownout/reset code or ROM activity is inferred.',
               'source': 'Pinnedstartup_funcs.c:67-90/configfalse versus actualnm+disassembly, not a physical execution.',
               'summary': summaries, 'binary_equivalence': 'Not claimed; source/config/compiled selector effects and actual separate artifact hashes are recorded.'}
    (OUT / 'mode-comparison.json').write_text(json.dumps(compare, indent=2) + '\n')
    (OUT / 'linked-artifact-bindings.json').write_text(json.dumps({'source_commit': 'e9849a8ae2833b96e0d4ce92978ee48e2087f30c', 'SDK': 'fff9895c82d744c7237be8847347bdd1b07c6643', 'archive': 'linked-artifacts-and-configs.tar.gz', 'archive_sha256': sha(OUT / 'linked-artifacts-and-configs.tar.gz'), 'artifacts': artifacts}, indent=2) + '\n')
    (OUT / 'build-output-inventory.json.gz').write_bytes(gzip.compress(json.dumps({'rows': inventory, 'excluded_from_archive': 'Objects and intermediate static archives retain exact hashes here and remain in owned runtime cache; finalELF/bin/map/config/dependency/compiler-description files are archived.'}, separators=(',', ':')).encode(), mtime=0))
    print(json.dumps({'all_build_files_hashed': len(inventory), 'archive_members': sum(row['preserved_in_archive'] for row in inventory), 'main_artifacts': len(artifacts), 'archive_bytes': (OUT / 'linked-artifacts-and-configs.tar.gz').stat().st_size, 'app_config_values_identical': compare['app_config_values_identical'], 'bootloader_config_values_identical': compare['bootloader_config_values_identical']}))


if __name__ == '__main__':
    main()
