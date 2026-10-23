#!/usr/bin/env python3
"""Research-only fresh-host context; never invoke bwrap or attempt isolation.

This observes a new VM, not the VM that failed RTM_NEWADDR. Errors, inaccessible
logs and truncated data remain UNKNOWN. Exit0 means a bounded record was written,
not that a namespace, permission, build or security property passed.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import shutil
import stat
import subprocess
import time

READ_CAP = 16384
COMMAND_CAP = 16384  # independently per stdout/stderr; exceeding it stops that reader
STATUS_FIELDS = {'Uid', 'Gid', 'Groups', 'CapInh', 'CapPrm', 'CapEff', 'CapBnd',
                 'CapAmb', 'NoNewPrivs', 'Seccomp', 'Seccomp_filters'}
PUBLIC_PROFILE_FILES = (
    '/usr/lib/sysctl.d/50-bubblewrap.conf',
    '/etc/apparmor.d/bwrap', '/etc/apparmor.d/bwrap-userns-restrict',
    '/usr/share/apparmor/extra-profiles/bwrap',
    '/usr/share/apparmor/extra-profiles/bwrap-userns-restrict',
)
PUBLIC_READS = (
    '/proc/self/uid_map', '/proc/self/gid_map',
    '/proc/self/attr/current', '/proc/self/attr/apparmor/current',
    '/sys/kernel/security/lsm', '/sys/module/apparmor/parameters/enabled',
    '/proc/sys/kernel/unprivileged_userns_clone',
    '/proc/sys/kernel/apparmor_restrict_unprivileged_userns',
    '/proc/sys/kernel/apparmor_restrict_unprivileged_unconfined',
    '/proc/sys/kernel/dmesg_restrict', '/proc/sys/user/max_user_namespaces',
)
SAFE_PATH = '/usr/sbin:/usr/bin:/sbin:/bin'


def unknown(error):
    return {'status': 'UNKNOWN', 'error': str(error)[:512]}


def read_public(path, *, status_fields=False):
    try:
        with open(path, 'rb', buffering=0) as stream:
            body = stream.read(READ_CAP + 1)
        if len(body) > READ_CAP:
            return unknown('Read exceeds fixed16384-byte cap; content not retained')
        text = body.decode('utf-8', errors='replace')
        if status_fields:
            values = dict(line.split(':', 1) for line in text.splitlines() if ':' in line)
            return {'status': 'UNKNOWN' if STATUS_FIELDS - values.keys() else 'OBSERVED', 'fields': {key: values[key].strip() for key in sorted(STATUS_FIELDS) if key in values}, 'missing_fields': sorted(STATUS_FIELDS - values.keys())}
        return {'status': 'OBSERVED', 'text': text, 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}
    except OSError as error:
        return unknown(error)


def read_command(argv):
    """Only called with the fixed read-only command allowlist below; no shell.

    Retention is bounded while reading, not after communicate/capture_output.
    Timeout/overflow terminates only this owned reader PID, never a process group.
    """
    resolved = shutil.which(argv[0], path=SAFE_PATH)
    if resolved is None:
        return {'argv': argv, **unknown('Read-only command unavailable')}
    actual = [resolved, *argv[1:]]
    buffers = {'stdout': bytearray(), 'stderr': bytearray()}
    reason = None
    process = None
    selector = selectors.DefaultSelector()
    try:
        process = subprocess.Popen(actual, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, env={'PATH': SAFE_PATH, 'LC_ALL': 'C', 'TZ': 'UTC'})
        for label, stream in (('stdout', process.stdout), ('stderr', process.stderr)):
            os.set_blocking(stream.fileno(), False)
            selector.register(stream, selectors.EVENT_READ, label)
        deadline = time.monotonic() + 5
        while selector.get_map():
            left = deadline - time.monotonic()
            if left <= 0:
                reason = 'Read-only command exceeded5s observation timeout'
                break
            for key, _ in selector.select(min(left, 0.1)):
                body = os.read(key.fd, 4096)
                if not body:
                    selector.unregister(key.fileobj)
                elif len(buffers[key.data]) + len(body) > COMMAND_CAP:
                    reason = 'Read-only command exceeded16384-byte stream cap'
                    break
                else:
                    buffers[key.data].extend(body)
            if reason:
                break
        if reason and process.poll() is None:
            try:
                process.kill()
            except ProcessLookupError:
                pass
        try:
            exit_code = process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            try:
                process.kill()
            except ProcessLookupError:
                pass
            reason = 'Read-only command status unavailable within observation window'
            exit_code = process.wait(timeout=2)
        return {'argv': actual, 'status': 'OBSERVED' if exit_code == 0 and reason is None and not buffers['stderr'] else 'UNKNOWN',
                'exit': exit_code, 'error': reason, 'stdout': buffers['stdout'].decode(errors='replace'),
                'stderr': buffers['stderr'].decode(errors='replace')}
    except (OSError, subprocess.TimeoutExpired) as error:
        return {'argv': actual, **unknown(error)}
    finally:
        if process is not None and process.poll() is None:
            # No broader signal or privilege fallback. An unavailable status is
            # already UNKNOWN; this only terminates the observer's own reader.
            try:
                process.kill()
            except ProcessLookupError:
                pass
        selector.close()
        if process is not None:
            for stream in (process.stdout, process.stderr):
                if stream is not None:
                    stream.close()


def binary_file(path):
    try:
        resolved = Path(path).resolve(strict=True)
        metadata = resolved.stat()
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > 4 * 1024 * 1024:
            return unknown('Installed binary is not a regular file within4MiB cap')
        with resolved.open('rb') as stream:
            body = stream.read(4 * 1024 * 1024 + 1)
        if len(body) > 4 * 1024 * 1024:
            return unknown('Installed binary grew beyond observation cap')
        try:
            capability = {'status': 'OBSERVED', 'security_capability_hex': os.getxattr(resolved, 'security.capability').hex()}
        except OSError as error:
            capability = unknown(error)  # absent xattr is not relabeled as a capability proof
        return {'status': 'OBSERVED', 'path': str(path), 'resolved': str(resolved), 'mode': oct(stat.S_IMODE(metadata.st_mode)),
                'uid': metadata.st_uid, 'gid': metadata.st_gid, 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest(),
                'file_capability_read': capability}
    except OSError as error:
        return unknown(error)


# Only these literal public labels are retained from arbitrary audit records.
AUDIT_LABELS = {
    'apparmor': {'DENIED', 'ALLOWED', 'AUDIT', 'STATUS', 'ERROR'},
    'operation': {'capable', 'userns_create', 'userns'},
    'profile': {'unconfined', 'unprivileged_userns', 'bwrap', 'bwrap-userns', 'bwrap-userns-restrict'},
    'comm': {'bwrap', 'python', 'python3', 'python3.12', 'journalctl', 'dmesg', 'apt-get', 'dpkg', 'dpkg-query'},
    'capname': {'net_admin', 'sys_admin', 'setpcap', 'setuid', 'setgid', 'sys_ptrace', 'sys_chroot'},
    'requested_mask': {'r', 'w', 'rw', 'wr', 'x', 'm', 'create', 'send', 'receive'},
    'denied_mask': {'r', 'w', 'rw', 'wr', 'x', 'm', 'create', 'send', 'receive'},
}
AUDIT_NUMBERS = {'pid': 2147483647, 'type': 65535, 'capability': 63}


def audit_tokens(line):
    """Split only at unquoted whitespace; quoted contents never become fields."""
    tokens, start, quote, i = [], 0, None, 0
    while i < len(line):
        char = line[i]
        if quote is not None:
            if char == '\\':
                if i + 1 == len(line):
                    raise ValueError('Malformed audit quoting')
                i += 2
                continue
            if char == quote:
                quote = None
        elif char in ('"', "'"):
            quote = char
        elif char.isspace():
            if start < i:
                tokens.append(line[start:i])
            start = i + 1
        i += 1
    if quote is not None:
        raise ValueError('Malformed audit quoting')
    if start < i:
        tokens.append(line[start:i])
    return tokens


def format_audit_record(line):
    result = {'status': 'UNKNOWN', 'fields': {}, 'redacted': [], 'time_prefix': None,
              'audit_identifier': None, 'raw_line_sha256': hashlib.sha256(line.encode()).hexdigest()}
    if len(line) > 2048:
        result['reason'] = 'Audit line exceeds2048characters; no raw contents retained'
        return result
    try:
        tokens = audit_tokens(line)
        if tokens and re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:[.,]\d{1,9})?(?:Z|[+-]\d\d:?\d\d)', tokens[0]):
            result['time_prefix'] = tokens[0]
        fields = {}
        in_body = False
        for token in tokens:
            identifier = re.fullmatch(r'audit\(([0-9]+(?:\.[0-9]+)?:[0-9]+)\):?', token)
            if identifier:
                if result['audit_identifier'] is not None:
                    raise ValueError('Duplicate audit identifier')
                result['audit_identifier'] = identifier[1]
                in_body = True
                continue
            match = re.fullmatch(r'([a-z_]{1,64})=(.+)', token)
            if match is None:
                if in_body:
                    raise ValueError('Unsupported top-level audit body token')
                continue  # timestamp/host/kernel prefixes are never retained
            key, value = match.groups()
            if key in fields:
                raise ValueError('Duplicate audit key')
            if value[0] in ('"', "'"):
                if len(value) < 2 or value[-1] != value[0]:
                    raise ValueError('Malformed audit value')
                value = value[1:-1]
            if '"' in value or "'" in value:
                raise ValueError('Unsupported embedded audit quote')
            fields[key] = value
        recognized = result['time_prefix'] is not None and result['audit_identifier'] is not None and bool(fields)
        for key, value in fields.items():
            if key in AUDIT_LABELS and value in AUDIT_LABELS[key]:
                result['fields'][key] = value
            elif key in AUDIT_NUMBERS and re.fullmatch(r'0|[1-9][0-9]{0,9}', value) and int(value) <= AUDIT_NUMBERS[key]:
                result['fields'][key] = int(value)
            else:
                recognized = False
                # Unknown keys and all nonpublic/path-bearing values are hashes,
                # never raw values, key names, argv, names or proctitle bodies.
                result['redacted'].append({'key_sha256': hashlib.sha256(key.encode()).hexdigest(),
                                           'value_sha256': hashlib.sha256(value.encode()).hexdigest()})
        result['status'] = 'OBSERVED' if recognized else 'UNKNOWN'
    except ValueError:
        result.update(fields={}, redacted=[], status='UNKNOWN', reason='Malformed or duplicate top-level audit record')
    return result


def format_kernel_output(raw):
    # Count the upstream65 sentinel BEFORE filtering/retaining64. Multiline
    # events can conservatively reach UNKNOWN earlier; they never hide a cap.
    lines = raw.splitlines()
    truncated = len(lines) > 64
    matches = [line for line in lines if re.search(r'DENIED|audit\(', line)]
    records = [format_audit_record(line) for line in matches[:64]]
    return {'status': 'UNKNOWN' if truncated or not records or any(row['status'] == 'UNKNOWN' for row in records) else 'OBSERVED',
            'matching_records': records, 'retained_lines_truncated': truncated,
            'returned_lines': len(lines),
            'retention_role': 'Top-level audit metadata with literal public value/numeric allowlists; unknown/private data hashed, no raw argv/path/proctitle',
            'no_matching_lines_is_not_permission_or_denial_absence_proof': True}



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    now = datetime.now(timezone.utc)
    since = (now - timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')
    until = now.strftime('%Y-%m-%d %H:%M:%S')
    result = {
        'role': 'freshhostobservation_notproof_of_failedVM/isolation',
        'observed_at_utc': now.isoformat(),
        'namespace_attempts': 0, 'build_attempts': 0, 'provision_attempts': 0, 'bwrap_executions': 0,
        'kernel': list(os.uname()),
        'image': {name: os.environ.get(name, 'UNKNOWN')[:256] for name in ('ImageOS', 'ImageVersion')},
        'identity': {'uid': os.getuid(), 'euid': os.geteuid(), 'gid': os.getgid(), 'egid': os.getegid(), 'groups': os.getgroups()},
        'process_status': read_public('/proc/self/status', status_fields=True),
        'public_reads': {path: read_public(path) for path in PUBLIC_READS},
        'bubblewrap_package': read_command(['dpkg-query', '-W', '-f=${binary:Package}\t${Version}\t${Architecture}\t${db:Status-Abbrev}\n', 'bubblewrap']),
        'bubblewrap_provider': read_command(['dpkg-query', '-S', '/usr/bin/bwrap']),
        'bubblewrap_apt_policy': read_command(['apt-cache', 'policy', 'bubblewrap']),
        'bubblewrap_binary': binary_file('/usr/bin/bwrap'),
        'public_package_profile_files': {path: {'read': read_public(path), 'provider': read_command(['dpkg-query', '-S', path])} for path in PUBLIC_PROFILE_FILES},
    }
    logs = {}
    for label, argv in (
        ('journal', ['journalctl', '--no-pager', '-k', '--output=short-iso', '--since=' + since, '--until=' + until, '--lines=65', '--grep=DENIED|audit\\(']),
        ('dmesg', ['dmesg', '--time-format=iso', '--since', since, '--until', until]),
    ):
        record = read_command(argv)
        raw = record.pop('stdout', '')
        formatted = format_kernel_output(raw)
        if formatted.pop('status') == 'UNKNOWN':
            record['status'] = 'UNKNOWN'
        record.update(formatted)
        record['window'] = {'since': since, 'until': until, 'role': 'fresh_host_only'}
        logs[label] = record
    result['unprivileged_timestamp_filtered_kernel_observations'] = logs
    result['limits'] = [
        'No bwrap, namespace, netlink, build, SDK, firmware or provisioning operation is executed.',
        'The workflow prerequisite APT setup precedes this read-only observer; this is post-setup state, not pristine-host state.',
        'This is a fresh VM, not the failed VM; no RTM_NEWADDR/kernel errno/LSM causal attribution follows by itself.',
        'Missing, denied, truncated or timed-out observations remain UNKNOWN; no sudo/log escalation, retry or fallback.',
        'No isolation/security PASS or hardware/host admission is produced; existing required PR gates remain unchanged and failed.',
    ]
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print('Fresh-host observation written; no namespace/build attempted and no isolation verdict.')


if __name__ == '__main__':
    main()
