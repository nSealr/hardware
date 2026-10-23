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
