# Audit Checklist

Before hardware work is complete:

- [ ] BOM includes substitutes or sourcing notes.
- [ ] Manual hardware reports list exact hardware, firmware commit, procedure,
      expected result, observed result, limitations, and safety flags.
- [ ] Stateless QR vault reports do not claim persistent secrets or TROPIC01
      usage.
- [ ] Custom persistent-secret wallet docs do not call USB data transport
      air-gapped and do not claim current TROPIC01 BIP-340 signing before a
      public/vendor path is verified.
- [ ] Custom wallet Rev A docs keep battery interfaces out of the checked
      requirement set unless a separate portable branch is created.
- [ ] Raspberry OS profile reports record removable boot media, wireless,
      swap, remote-access, RAM-only custody, persistent-secret absence, and
      power-cycle evidence before image acceptance is claimed.
- [ ] Wiring diagrams match tested hardware.
- [ ] Assembly docs are reproducible by an external builder.
- [ ] Security-sensitive debug/provisioning paths are documented.
- [ ] License and source files are present for hardware artifacts.
