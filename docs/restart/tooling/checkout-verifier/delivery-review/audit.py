#!/usr/bin/env python3
"""Read exact delivery/copy/CI evidence; write only this review directory."""
import datetime
import hashlib
import json
import re
import subprocess
from pathlib import Path

OWN = Path(__file__).resolve().parent
ROOT = OWN.parents[4]
BASE = '340697d6713a671e9e01b0dc874ec999ab071601'
SOURCE = '0f83844a4da43dc79c2befba82e40934858250c5'
REVIEW = '26585a1d640726771f1409625f82f82016bf7c25'
CANDIDATE = 'd407d8ec93d5c43aa0045390c80bfcfcf64c9854'
PREFIX = 'docs/restart/tooling/checkout-verifier/'
COPIES = PREFIX + 'independent-review/'
PYTHON = '/home/tux/nsealr/.restart-tools/goal/r00/tools/baseline/.work/final/.tools/python/bin/python3'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def tree(commit):
    return git('rev-parse', commit + '^{tree}').decode().strip()


def entries(commit):
    result = {}
    for row in git('ls-tree', '-rz', '--full-tree', commit).split(b'\0'):
        if row:
            meta, path = row.split(b'\t'); mode, kind, blob = meta.decode().split()
            result[path.decode()] = {'mode': mode, 'kind': kind, 'blob': blob}
    return result


def read_json(path):
    return json.loads((ROOT / path).read_bytes())


def main():
    git('merge-base', '--is-ancestor', CANDIDATE, 'HEAD')
    own_scope = OWN.relative_to(ROOT).as_posix() + '/'
    assert all(p.startswith(own_scope) for p in
               git('diff', '--name-only', CANDIDATE).decode().splitlines())
    final, source, reviewed = entries(CANDIDATE), entries(SOURCE), entries(REVIEW)
    assert tree(CANDIDATE) == tree(REVIEW)
    tail = [p for p in final if p not in source or source[p] != final[p]]
    assert len(tail) == 44 and set(source) <= set(final)
    assert all(p.startswith(COPIES) and p not in source for p in tail)
    assert {p: v for p, v in final.items() if not p.startswith(COPIES)} == source
    copies = []
    for path in sorted(tail):
        data = git('show', CANDIDATE + ':' + path)
        assert final[path] == reviewed[path]
        assert data == git('show', REVIEW + ':' + path) == (ROOT / path).read_bytes()
        copies.append({'path': path, **final[path], 'bytes': len(data), 'sha256': sha(data)})
    author = read_json(PREFIX + 'artifact-manifest.json')
    manifest = read_json(COPIES + 'artifact-manifest.json')
    assert manifest['candidate_commit'] == SOURCE
    assert {r['path'] for r in manifest['files']} | {COPIES + 'artifact-manifest.json'} == set(tail)
    assert len({r['path'] for r in manifest['files']}) == len(manifest['files']) == 43
    for row in author['artifacts'] + manifest['files']:
        data = (ROOT / row['path']).read_bytes()
        assert sha(data) == row['sha256'] and ('bytes' not in row or len(data) == row['bytes'])
    assert {r['path'] for r in author['artifacts']} | {PREFIX + 'artifact-manifest.json'} == {p for p in source if p.startswith(PREFIX)}
    report = read_json(COPIES + 'report.json')
    assert report['candidate_commit'] == SOURCE and report['base_commit'] == BASE
    assert report['verdict'] == 'PASS_bounded_repository_tooling' and report['findings'] == []
    commands = read_json(COPIES + 'commands.json')
    assert len(commands) == 37
    for row in commands:
        assert row['exit_code'] == row['expected_exit']
        assert sha((ROOT / COPIES / row['log']).read_bytes()) == row['log_sha256']
    for row in read_json(PREFIX + 'result.json')['checks']:
        assert row['exit_code'] == row['expected']
        assert sha((ROOT / PREFIX / row['log']).read_bytes()) == row['sha256']
    for commit in (BASE, SOURCE, author['source_commit']):
        git('merge-base', '--is-ancestor', commit, CANDIDATE)
    verifier = (ROOT / 'scripts/verify_repo.py').read_bytes()
    assert sha(verifier) == author['source_file_sha256'] == 'aad93e5aa6c92fd4cfb231e04f36522f3222be73f6865a4cf38be6fd76958d64'
    assert verifier == git('show', author['source_commit'] + ':scripts/verify_repo.py')
    changed = git('diff', '--name-only', BASE, CANDIDATE).decode().splitlines()
    assert {p for p in changed if not p.startswith(PREFIX)} == {'.gitignore', 'scripts/verify_repo.py'}
    patterns = {'credential_token': rb'(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{24,})',
                'private_key_block': rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
                'private_workspace_path': rb'/home/tux/nsealr/(?:workspace|private)/'}
    for path in changed:
        assert final[path]['kind'] == 'blob' and final[path]['mode'] in {'100644', '100755'}
        data = git('show', CANDIDATE + ':' + path); data.decode('utf-8')
        assert not any(re.search(pattern, data) for pattern in patterns.values()), path
    checks = OWN / 'checks'; checks.mkdir(exist_ok=True)
    jobs = []
    captures = []
    for job_id in (117760762302, 117760749613):
        raw = subprocess.check_output(['gh', 'api', f'repos/nSealr/hardware/actions/jobs/{job_id}'], cwd=ROOT)
        job = json.loads(raw)
        assert job['head_sha'] == CANDIDATE and job['status'] == 'completed' and job['conclusion'] == 'success'
        path = checks / f'job-{job_id}.json'; path.write_bytes(raw)
        captures.append({'path': str(path.relative_to(OWN)), 'bytes': len(raw), 'sha256': sha(raw)})
        raw_run = subprocess.check_output(['gh', 'api', f'repos/nSealr/hardware/actions/runs/{job["run_id"]}'], cwd=ROOT)
        run = json.loads(raw_run)
        assert run['head_sha'] == CANDIDATE and run['status'] == 'completed' and run['conclusion'] == 'success'
        path = checks / f'run-{job["run_id"]}.json'; path.write_bytes(raw_run)
        captures.append({'path': str(path.relative_to(OWN)), 'bytes': len(raw_run), 'sha256': sha(raw_run)})
        jobs.append({k: job[k] for k in ('id', 'run_id', 'head_sha', 'status', 'conclusion', 'html_url', 'completed_at')})
    positive = subprocess.run([PYTHON, '-B', 'scripts/verify_repo.py'], cwd=ROOT, capture_output=True)
    output = positive.stdout + positive.stderr
    (checks / 'final-candidate-positive.log').write_bytes(output)
    assert positive.returncode == 0 and b'nSealr hardware baseline verification passed' in output
    assert git('rev-parse', 'refs/heads/main').decode().strip() == BASE
    result = {'recorded_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'candidate': CANDIDATE, 'candidate_tree': tree(CANDIDATE), 'reviewed_source': SOURCE,
              'original_review': REVIEW, 'original_review_tree_equal': True, 'base': BASE,
              'exact_proof_copies': copies, 'tail_added_files': len(tail),
              'independent_manifest_members': 43, 'author_manifest_members': 12,
              'all_source_manifests_log_hashes_and_dependency_closure_verified': True,
              'original_independent_recorded_executions': len(commands), 'original_existing_CI_tests': 43,
              'unchanged_product_and_author_evidence': True, 'base_diff_only_tooling_and_scoped_evidence': True,
              'privacy': {'all_candidate_changes_UTF8_regular_files': True, 'scanned_categories': list(patterns),
                          'findings': [], 'manual_assessment': 'All additions are public verifier code/probes, JSON evidence, text logs and reports. No private/manual/CAD/runtime-object material appended; local public-tool execution paths are not private source intake.'},
              'final_hosted_jobs': jobs, 'API_captures': captures,
              'new_positive_check': {'command': [PYTHON, '-B', 'scripts/verify_repo.py'], 'cwd': str(ROOT),
                                     'exit_code': positive.returncode, 'log': 'checks/final-candidate-positive.log',
                                     'sha256': sha(output), 'python_sha256': sha(Path(PYTHON).resolve().read_bytes())},
              'inspection_correction': 'An initial read-only JSON summary assumed the author-manifest artifacts key also existed in the independent manifest and raised KeyError: artifacts. Its actual files schema was inspected and all43 entries plus self were validated. No source/evidence change or product/test failure.',
              'not_repeated': 'Unchanged37 recorded CLI/CI executions and43 existing tests; exact source/tree/copy identity plus actual final hosted CI establish delivery continuity.',
              'main_unchanged': True, 'author_branch_not_mutated': True,
              'limits': 'Final delivery review of repository tooling only. No H01/component/manual/electronic/PCB/physical claim, A02 acceptance or merge permission.'}
    (OWN / 'bindings.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'candidate': CANDIDATE, 'tree': tree(CANDIDATE), 'proof_copies': len(copies),
                      'manifests_verified': [12, 43], 'final_jobs_success': [j['id'] for j in jobs],
                      'actual_final_verifier_positive': True}, sort_keys=True))


if __name__ == '__main__':
    main()
