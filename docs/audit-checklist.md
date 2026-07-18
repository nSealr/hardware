# Audit Checklist

Before hardware work is complete:

- [ ] BOM includes exact MPNs, alternates, footprint status, datasheet links, and
      sourcing notes.
- [ ] Manual hardware reports list exact hardware, firmware commit, procedure,
      expected result, observed result, limitations, and safety flags.
- [ ] Stateless QR vault reports do not claim persistent secrets or TROPIC01
      usage.
- [ ] Raspberry OS profile reports record removable boot media, wireless, swap,
      remote-access, RAM-only custody, persistent-secret absence, and power-cycle
      evidence before image acceptance is claimed.
- [ ] Wiring diagrams match tested hardware.
- [ ] Assembly docs are reproducible by an external builder.
- [ ] Security-sensitive debug/provisioning paths are documented.
- [ ] License and source files are present for hardware artifacts.
