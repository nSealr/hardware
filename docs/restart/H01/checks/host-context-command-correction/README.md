# Read-only observer command correction

Source53e2c2e713fd6bc027af3570db9ceb009063719e changes only three literals:
`journalctl -k` and suffix-free absolute window timestamps. The existing child
`TZ=UTC` gives those timestamps the same UTC meaning. The workflow is unchanged.
[Validation](validation.json) binds the source, local primary interfaces, preserved
help output, pure time formatting and unchanged helper ASTs. No help or observer
command was rerun while packaging this evidence. Individual earlier help exit
codes were not separately captured; the receipt states that limit explicitly.
The old eight synthetic formatter cases retain their original source identity.

The original run40033802424/artifact12536560855 is preserved, not rewritten.
It observed the same provider image20261012.334.1 and bwrap binary hash as the
failed build, plus a fresh unconfined UID1001 parent with CapEff/Prm0,
NoNewPrivs0 and Seccomp0. AppArmor and its unprivileged-userns restriction were
enabled; userns_clone1/max63795 were observed. Those are fresh-parent facts,
not the failed VM's executing bwrap state. Missing known profile files do not
prove no profile was loaded. The xattr read remains UNKNOWN/ENODATA. Both kernel
readers failed argument parsing, so no log permission denial was observed.

## Minimum attribution evidence still missing — proposal only

The unresolved property is the real RTM_NEWADDR transaction outcome together
with the executing bwrap PID's effective capabilities and current LSM label at
that point. The printed errno is not a decoded netlink ACK. First prefer any
already retained original PID/time-correlated kernel/audit record. A repeat
fresh-context collection merely to get green readers cannot replace this proof.

If original evidence is unavailable, the next experiment would be ONE explicitly
admitted attribution attempt of the unchanged captured bootstrap sandbox launch
on the same declared ubuntu-24.04 runner/image and installed package/binary.
Keep the complete user/net namespace, UID, capability-drop, NNP, read-only mounts,
fresh-device and payload preflight properties unchanged. Capture the actual
netlink request/reply (or failed syscall) and timestamp/PID-correlated LSM/capability
context. This is observation of the unchanged sandbox, not authorization to
change its policy, flags, privileges, version, runner or implementation.

Whether existing unprivileged tracing can obtain that evidence without changing
credential/namespace semantics is not established. That precise feasibility
must be reviewed before an attempt; denied/unavailable tracing is STOP/UNKNOWN,
not permission for sudo tracing, instrumentation of a replacement binary or
platform-policy modification. No attribution experiment, second dispatch,
observer, kernel-log read, namespace or build was implemented or executed here.
The production PR and both failed required gates remain untouched and mandatory.

## Source-only feasibility decision — STOP/UNKNOWN, 24 October

Unprivileged strace has an upstream decoder for actual `NLMSG_ERROR.error` and
can follow clone children. This establishes a possible observation mechanism,
not its availability, permissions or neutral behavior on the captured runner.
The pinned bwrap0.9 nonsetuid path does not establish a blanket tracing ban:
its root-owned-namespace/anti-ptrace discussion is conditional on setuid mode.
The existing0755/UID1001 observation is a different path. See the exact
[bwrap source](https://github.com/containers/bubblewrap/blob/v0.9.0/bubblewrap.c#L834-L899)
and [netlink decoder](https://github.com/strace/strace/blob/686aa55405a09925a77ea0dea59a292b0fb70243/src/netlink.c#L529-L613).

The ordinary tracer wrapper changes the direct parent, relevant to the existing
`--die-with-parent` lifetime. The documented parent-preserving `-D` is not an
unchanged-policy solution: the inspected
[startup source](https://github.com/strace/strace/blob/686aa55405a09925a77ea0dea59a292b0fb70243/src/strace.c#L1800-L1808)
calls `PR_SET_PTRACER_ANY`, adjusting Yama trace authorization. It must not be
used as a bypass. Ptrace also introduces stops/timing effects and LSM permission
checks; late attach can miss the transaction and is not a neutral replacement.
The [strace manual](https://man7.org/linux/man-pages/man1/strace.1.html),
[ptrace rules](https://man7.org/linux/man-pages/man2/ptrace.2.html) and
[kernel Yama documentation](https://docs.kernel.org/admin-guide/LSM/Yama.html)
describe these separate constraints. No fault injection, credential adjustment,
seccomp filter, ptrace authorization or other mode change is proposed.

The exact missing property is a source-bound, permitted observation of this
runner's failing child request/reply **and** contemporaneous effective capability/
LSM context, while preserving the original caller/lifetime and security semantics.
The sources do not prove that conjunction; no stock strace mode reviewed here
provides an atomic AppArmor-label/capability snapshot at that syscall. The
runner's relevant ptrace permission and tracer identity/version are also unbound.
A decoded reply from a traced attempt would describe that altered observation,
not retrospectively prove the untraced failed VM's errno or equivalent execution.

Therefore STOP/UNKNOWN: no wrapper, `-D`, late attach, alternative platform or
privilege/policy change is authorized as a way to obtain green. Existing original
attribution evidence, if retained, remains preferable. This append contains no
experiment implementation or runnable trace command and grants no retry.
Only primary documentation/source was read; no trace/tool install, host/log read,
namespace/build or dispatch occurred. The older source/proofs and production
required failures remain preserved. [Validation](validation.json) pins the
specific upstream source studied; it does not select/install that tool version.
