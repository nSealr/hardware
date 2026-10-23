"""Fail-closed controls for the portable compile gate, separate from original43."""
import builtins
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import build_gate as gate
import verify_build as verify


class GateControls(unittest.TestCase):
    def test_wrong_cached_publisher_hash_is_rejected(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root / 'asset').write_bytes(b'wrong')
            with self.assertRaisesRegex(gate.GateError, 'Frozen asset mismatch'):
                gate.acquire({'filename': 'asset', 'sha256': '0' * 64}, root, root)

    def test_git_owner_execution_matches_real_git(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            for args in (['init', '-q'], ['config', 'user.name', 'Test'], ['config', 'user.email', 'test@example.invalid']):
                subprocess.run(['git', '-C', name, *args], check=True)
            file = root / 'LICENSE'
            file.write_text('public test text\n')
            file.chmod(0o755)
            subprocess.run(['git', '-C', name, 'add', '.'], check=True)
            subprocess.run(['git', '-C', name, 'commit', '-qm', 'test'], check=True)
            commit = subprocess.check_output(['git', '-C', name, 'rev-parse', 'HEAD'], text=True).strip()
            gate.git_tree_check(root, commit)
            file.chmod(0o645)
            subprocess.run(['git', '-C', name, 'add', '.'], check=True)
            staged = subprocess.check_output(['git', '-C', name, 'ls-files', '--stage'], text=True)
            self.assertTrue(staged.startswith('100644 '))
            with self.assertRaisesRegex(gate.GateError, 'file/mode mismatch'):
                gate.git_tree_check(root, commit)
            with self.assertRaisesRegex(gate.GateError, 'Wrong Git HEAD'):
                gate.git_tree_check(root, '0' * 40)

    def test_dependencies_reject_stale_missing_duplicate_and_count(self):
        valid = 'a.obj: #deps 1, deps mtime 100 (VALID)\n    /source.c\n'
        self.assertEqual(verify.dependency_blocks(valid)[0]['dependencies'], ['/source.c'])
        for bad in ('', valid.replace('VALID', 'STALE'), valid.replace('#deps 1', '#deps 2'), valid + '\n' + valid, valid.replace('    /', '  /')):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                verify.dependency_blocks(bad)

    def test_preflight_refuses_no_new_privileges_zero(self):
        # Run the actual preflight body up to its security assertions; no build or
        # namespace success is fabricated. The full gate supplies the real run.
        expected = {'sdk': '/unused', 'pin': 'unused', 'uid': os.getuid(), 'euid': os.geteuid(), 'gid': os.getgid(), 'egid': os.getegid(), 'groups': os.getgroups()}
        original = builtins.open
        def controlled_open(path, *args, **kwargs):
            if path == '/proc/self/status':
                return io.StringIO('CapEff:\t0\nCapPrm:\t0\nNoNewPrivs:\t0\n')
            return original(path, *args, **kwargs)
        with patch('sys.argv', ['preflight', json.dumps(expected)]), patch('builtins.open', controlled_open), self.assertRaisesRegex(RuntimeError, 'Mandatory namespace'):
            exec(compile(gate.PREFLIGHT, 'actual-preflight', 'exec', optimize=1), {})

    def test_namespace_failure_is_not_a_green_skip(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()), self.assertRaisesRegex(gate.GateError, 'exit1'):
                gate.command(root, 'required-sandbox', ['/bin/false'])
            record = json.loads((root / 'receipts/required-sandbox.json').read_text())
            self.assertEqual(record['exit'], 1)
            self.assertFalse((root / 'result.json').exists())

    def test_inherited_optimization_is_refused_before_acquisition(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            env = os.environ.copy()
            env['PYTHONOPTIMIZE'] = '1'
            result = subprocess.run([os.sys.executable, str(Path(gate.__file__)), '--work-dir', str(root / 'work'), '--cache-dir', str(root / 'cache'), '--bwrap', '/bin/false'], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn('Unexpected inherited build overrides', result.stderr)
            self.assertFalse((root / 'work').exists())

    def test_archive_file_extra_and_mode_changes_rejected(self):
        import tarfile
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            source = root / 'source'
            source.mkdir()
            (source / 'tool').write_bytes(b'tool')
            (source / 'tool').chmod(0o755)
            archive = root / 'tool.tar'
            with tarfile.open(archive, 'w') as tar:
                tar.add(source / 'tool', arcname='tool')
            exported = root / 'export'
            gate.extract(archive, exported)
            verify.verify_archive(archive, exported)
            (exported / 'tool').chmod(0o645)
            with self.assertRaisesRegex(ValueError, 'file/mode differs'):
                verify.verify_archive(archive, exported)
            (exported / 'tool').chmod(0o755)
            (exported / 'extra').write_bytes(b'extra')
            with self.assertRaisesRegex(ValueError, 'missing/extra'):
                verify.verify_archive(archive, exported)


if __name__ == '__main__':
    unittest.main()
