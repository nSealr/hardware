# Audit Checklist

Before hardware work is complete:

- [ ] BOM includes exact MPNs, alternates, footprint status, datasheet links, and
      sourcing notes.
- [ ] Manual hardware reports list exact hardware, firmware commit, procedure,
      expected result, observed result, limitations, and safety flags.
- [ ] Stateless QR vault reports do not claim persistent secrets or TROPIC01
      usage.
- [ ] TROPIC01 Universal Secure Device docs identify TROPIC01 as primary open
      secure element and OPTIGA-class second secure element as defense in depth.
- [ ] TROPIC01 Universal Secure Device docs keep microSD, BLE, WiFi, and radio
      out of Rev A0.
- [ ] TROPIC01 recovery is modeled as controlled power cycling or load
      switching, not a dedicated reset pin.
- [ ] NFC/RFID is documented as a power-gated contactless attack surface with a
      real antenna tuning requirement.
- [ ] Hidden pogo/debug pads are documented as production/debug features covered
      by the enclosure and lockable in hardened firmware.
- [ ] Raspberry OS profile reports record removable boot media, wireless, swap,
      remote-access, RAM-only custody, persistent-secret absence, and power-cycle
      evidence before image acceptance is claimed.
- [ ] Wiring diagrams match tested hardware.
- [ ] Assembly docs are reproducible by an external builder.
- [ ] Security-sensitive debug/provisioning paths are documented.
- [ ] License and source files are present for hardware artifacts.
