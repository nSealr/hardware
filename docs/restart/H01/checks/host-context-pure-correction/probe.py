"""Synthetic pure formatter checks; no observer import/main or host operations."""
import ast
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
SOURCE = REPO / 'diagnostics/s3-bod-selector/tools/observe_host_context.py'
sha = lambda data: hashlib.sha256(data).hexdigest()
body = SOURCE.read_bytes()
tree = ast.parse(body, filename=str(SOURCE))
names = {'AUDIT_LABELS', 'AUDIT_NUMBERS', 'audit_tokens', 'format_audit_record', 'format_kernel_output'}
selected = []
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in names:
        selected.append(node)
    elif isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id in names for target in node.targets):
        selected.append(node)
assert len(selected) == len(names)
namespace = {'hashlib': hashlib, 're': re}
exec(compile(ast.Module(body=selected, type_ignores=[]), str(SOURCE) + ':PURE_ONLY', 'exec'), namespace)
format_record, format_output = namespace['format_audit_record'], namespace['format_kernel_output']
expectations = json.loads((HERE / 'expectations.json').read_text())
public = expectations['public_control_line']
cases = {row['id']: row for row in expectations['cases']}
observed = []

row = format_record(public)
assert row['status'] == 'OBSERVED' and not row['redacted']
assert row['fields'] == {'type': 1400, 'apparmor': 'DENIED', 'operation': 'capable', 'profile': 'unprivileged_userns', 'pid': 123, 'comm': 'bwrap', 'capability': 12, 'capname': 'net_admin'}
observed.append({'id': 'public_control', 'status': row['status'], 'exact_fields': True})
for count, identifier in [(64, '64_control'), (65, '65_sentinel')]:
    result = format_output((public + '\n') * count)
    assert len(result['matching_records']) == 64
    assert result['retained_lines_truncated'] == (count == 65)
    assert result['status'] == ('UNKNOWN' if count == 65 else 'OBSERVED')
    observed.append({'id': identifier, 'status': result['status'], 'retained_records': 64, 'returned_lines': result['returned_lines'], 'truncated': result['retained_lines_truncated']})

row = format_record(cases['quoted_nested_fields']['input'])
assert row['status'] == 'UNKNOWN' and 'capname' not in row['fields'] and 'profile' not in row['fields']
assert row['redacted'] == [{'key_sha256': sha(b'name'), 'value_sha256': sha(b'/private/example capname=confidential profile=confidential')}]
assert '/private' not in json.dumps(row) and 'confidential' not in json.dumps(row)
observed.append({'id': 'quoted_nested_fields', 'status': row['status'], 'no_nested_field_promotion': True, 'exact_independent_redaction_hashes': True})

row = format_record(cases['private_profile_comm']['input'])
assert row['status'] == 'UNKNOWN' and 'profile' not in row['fields'] and 'comm' not in row['fields']
assert row['redacted'] == [{'key_sha256': sha(b'profile'), 'value_sha256': sha(b'/private/example/profile')}, {'key_sha256': sha(b'comm'), 'value_sha256': sha(b'/private/example/worker')}]
assert '/private' not in json.dumps(row) and 'example' not in json.dumps(row)
observed.append({'id': 'private_profile_comm', 'status': row['status'], 'no_private_raw_values': True, 'exact_independent_redaction_hashes': True})

for identifier, text in [('malformed_quote', cases['malformed_quote']['input']), ('duplicate_field', public + ' capname="sys_admin"')]:
    row = format_record(text)
    assert row['status'] == 'UNKNOWN' and row['fields'] == {} and row['redacted'] == []
    assert '/private' not in json.dumps(row)
    observed.append({'id': identifier, 'status': row['status'], 'no_partial_fields_or_raw_values': True})
row = format_record(public.replace(public.split(' ', 1)[0], '/private/prefix', 1))
assert row['status'] == 'UNKNOWN' and row['time_prefix'] is None and '/private' not in json.dumps(row)
observed.append({'id': 'path_prefix', 'status': row['status'], 'no_private_prefix': True})
assert {row['id'] for row in observed} == set(cases)
print(json.dumps({'role': 'PURE_SYNTHETIC_FORMATTER_PROOF_NOT_HOST_OBSERVATION', 'source_sha256': sha(body), 'expectations_sha256': sha((HERE / 'expectations.json').read_bytes()), 'selected_ast_names': sorted(names), 'cases': observed, 'observer_runs': 0, 'host_read_commands': 0, 'namespace_attempts': 0, 'builds': 0}, indent=2))
