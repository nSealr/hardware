#!/usr/bin/env python3
"""Independent exact-snapshot CLI behavior checks; no hardware qualification."""
import datetime,hashlib,io,json,os,pathlib,subprocess,sys,tarfile,tempfile
OWN=pathlib.Path(__file__).resolve().parent
ROOT=OWN.parents[4]
BASE='340697d6713a671e9e01b0dc874ec999ab071601'
CANDIDATE='0f83844a4da43dc79c2befba82e40934858250c5'
SOURCE='d91be514ace9c13fdc75cadeb20e8aba152be1a5'
PYTHON=pathlib.Path('/home/tux/nsealr/.restart-tools/goal/r00/tools/baseline/.work/final/.tools/python/bin/python3')
assert PYTHON.is_file()
FILES=['README.md','LICENSE','Makefile','.pre-commit-config.yaml','docs/architecture.md','docs/testing.md','docs/roadmap.md','docs/audit-checklist.md','.github/workflows/ci.yml']
DIRS=['pcb','kits','bom','enclosures','reports','templates','docs','scripts']
rows=[]
def sha(data):return hashlib.sha256(data).hexdigest()
def run(label,root,expected,marker,script='scripts/verify_repo.py',argv=None):
    argv=argv or [str(PYTHON),'-B',script]
    env=os.environ.copy();env['PATH']=str(PYTHON.parent)+os.pathsep+env['PATH']
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    p=subprocess.run(argv,cwd=root,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (OWN/(label+'.log')).write_bytes(p.stdout)
    rows.append({'label':label,'argv':argv,'cwd':str(root),'started_utc':started,'exit_code':p.returncode,'expected_exit':expected,'required_marker':marker,'log':label+'.log','log_sha256':sha(p.stdout)})
    (OWN/'commands.json').write_text(json.dumps(rows,indent=2)+'\n')
    assert p.returncode==expected and marker.encode() in p.stdout and b'Traceback' not in p.stdout,(label,p.returncode,p.stdout)
def snapshot(commit,name,parent):
    dest=parent/name;dest.mkdir()
    blob=subprocess.check_output(['git','archive',commit],cwd=ROOT)
    with tarfile.open(fileobj=io.BytesIO(blob)) as t:t.extractall(dest,filter='data')
    return dest

# Author evidence and exact source are independently bound before replay.
manifest=json.loads((OWN.parent/'artifact-manifest.json').read_text())
for item in manifest['artifacts']:assert sha((ROOT/item['path']).read_bytes())==item['sha256'],item['path']
assert sha((ROOT/'scripts/verify_repo.py').read_bytes())==manifest['source_file_sha256']
assert subprocess.check_output(['git','show',SOURCE+':scripts/verify_repo.py'],cwd=ROOT)==(ROOT/'scripts/verify_repo.py').read_bytes()
changed=subprocess.check_output(['git','diff','--name-only',BASE,CANDIDATE],cwd=ROOT).decode().splitlines()
assert {x for x in changed if not x.startswith('docs/restart/tooling/checkout-verifier/')}=={'scripts/verify_repo.py','.gitignore'}
with tempfile.TemporaryDirectory(prefix='.snapshots-',dir=OWN) as temp:
    temp=pathlib.Path(temp)
    before=snapshot(BASE,'baseline-misnamed',temp)
    run('baseline-valid-hardware-renamed',before,1,'MIT License')
    (before/'LICENSE').write_text('MIT License\n')
    (before/'kits').rename(before/'.held-kits')
    run('baseline-false-pass-reproduced',before,0,'baseline verification passed')
    for index,name in enumerate(['hardware','specs','firmware','arbitrary checkout Ω']):
        after=snapshot(CANDIDATE,name,temp)
        run(f'candidate-name-{index}',after,0,'nSealr hardware baseline verification passed')
    after=temp/'arbitrary checkout Ω'
    for index,rel in enumerate(FILES):
        path=after/rel;data=path.read_bytes();path.unlink();path.mkdir()
        run(f'file-directory-{index}',after,1,'missing required file: '+rel)
        path.rmdir();path.write_bytes(b' \t\n')
        run(f'file-empty-{index}',after,1,'empty required file: '+rel)
        path.write_bytes(data)
    for index,rel in enumerate(DIRS):
        path=after/rel;held=after/('.held-'+rel);path.rename(held)
        script='.held-scripts/verify_repo.py' if rel=='scripts' else 'scripts/verify_repo.py'
        run(f'directory-missing-{index}',after,1,'missing required directory: '+rel,script=script)
        held.rename(path)
    license_file=after/'LICENSE';data=license_file.read_bytes();license_file.write_text('MIT License\n')
    run('candidate-wrong-license',after,1,'LICENSE does not contain expected marker: CERN Open Hardware Licence')
    (after/'kits').rename(after/'.held-kits')
    run('candidate-wrong-license-and-missing-kit',after,1,'missing required directory: kits')
    (after/'.held-kits').rename(after/'kits');license_file.write_bytes(data)
    readme=after/'README.md';data=readme.read_bytes();readme.write_bytes(data.replace(b'## License',b'## Terms'))
    run('readme-no-license-heading',after,1,'README.md must include a License section')
    readme.write_bytes(data)
    run('restored-positive',after,0,'hardware baseline verification passed')
    run('existing-ci-exact-candidate',after,0,'Ran 43 tests',argv=['make','ci'])
    assert (after/'scripts/__pycache__').is_dir() and (after/'tests/__pycache__').is_dir()
# Ignore rule applies at nested depth and keeps substantive sources visible.
p=subprocess.run(['git','check-ignore','--no-index','-v','scripts/__pycache__/verify_repo.cpython-312.pyc','tests/__pycache__/test_validate_hardware.cpython-312.pyc'],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
assert p.returncode==0 and p.stdout.count(b'__pycache__/')==4,p.stdout
(OWN/'bytecode-ignore.log').write_bytes(p.stdout)
p=subprocess.run(['git','check-ignore','--no-index','scripts/verify_repo.py','tests/test_validate_hardware.py'],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
assert p.returncode==1 and not p.stdout
result={'candidate':CANDIDATE,'source':SOURCE,'base':BASE,'cli_runs':len(rows),'all_expectations_pass':True,'manifest_artifacts_verified':len(manifest['artifacts']),'required_files_exercised':len(FILES),'required_dirs_exercised':len(DIRS),'checkout_names':['hardware','specs','firmware','arbitrary checkout Ω'],'existing_ci_tests':43,'python':subprocess.check_output([str(PYTHON),'--version']).decode().strip(),'python_sha256':sha(PYTHON.resolve().read_bytes()),'git':subprocess.check_output(['git','--version']).decode().strip(),'source_sha256':sha((ROOT/'scripts/verify_repo.py').read_bytes()),'bytecode_rule_verified':True}
(OWN/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,sort_keys=True))
