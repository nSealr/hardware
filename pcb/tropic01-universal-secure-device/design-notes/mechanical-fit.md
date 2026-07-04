# Mechanical Feasibility — board + battery vs display footprint (plan + thickness)

Date: 2026-07-04. Scope: verify to the millimetre that (a) board footprint + battery
footprint together fit WITHIN the display footprint in plan, and (b) the whole stack
fits in thickness (Z). Four sub-verdicts, each CONFIRMED / REFUTED / PARTIAL + numbers.

## Sources actually used (and a source caveat)
- **Board measured geometry**: `design-notes/review-2026-07/board-truth.json` (outline
  Edge.Cuts, all placements + bboxes). Used directly.
- **Existing mechanical analysis** (cross-checked, corrections noted):
  `design-notes/review-2026-07/mechanical-display-integration.md`.
- **Display datasheet**: the path given in the task
  (`/Users/vincenzo/Downloads/nsealr-datasheets/er-tft024ips-3-archive.pdf`) **does not
  exist**, and the only local copy `er-tft024ips-3-datasheet.pdf` is a **5.5 KB Cloudflare
  "Just a moment…" HTML stub, NOT a PDF** — so its pages could not be Read. All
  ER-TFT024IPS-3 page citations below are therefore taken from the prior reviewer note
  (`mechanical-display-integration.md`, "verified page by page") and were **independently
  corroborated** against the EastRising ER-TFT024-3 family datasheet
  (buydisplay.com/download/manual/ER-TFT024-3_Datasheet.pdf) via web: that datasheet gives
  "Outline with FPC folded 42.72(W) x 59.46(H)", "Active Area 36.72 x 48.96", "Visual Area
  38.72 x 50.96", and the "BL/CTP 59.26" touch-panel line — all matching the note.
  → Treat the display page numbers as second-hand-but-corroborated, not first-hand.
- **Battery cell**: EEMB LP502030 (eemb.com/product-130, eemb.store/products/lp502030).
- **Battery connector J9**: JST PH-series datasheet ePH.pdf — **Read first-hand**
  (pp.1, 3, 5, 7). Pages cited are the real JST catalog pages.

Board coordinate convention (KiCad front view, +y down): outline centrelines
x=10.64 (left) / 53.36 (right) → **width 42.72 mm**; y=31.0 (top) / 70.8 (bottom) →
current height 39.80 mm. DECIDED design shrinks the top edge to **y=34.0 → H=36.8 mm**.

---

## VERDICT 1 — Display outline & which height governs the budget: CONFIRMED

- **Module envelope = 42.72(W) x 59.46(H) x ~2.3(T) mm** "Outline Dimension with FPC
  folded" (datasheet §2.2, p.5). The **59.46 = backlight (BL) frame**, the largest physical
  layer → **this is the number that governs the board+battery budget.**
- The **59.26** figure is the **CTP touch-glass height only** (p.8 shows BOTH "BL 59.46±0.2"
  and "BL/CTP 59.26±0.2"); the glass is 0.20 mm SHORTER than the BL frame. Width **42.72±0.2**
  on all drawings (p.6 / p.8).
- **Active-area offsets (NOT vertically centred):** height chain 2.90 → AA 48.96 → 7.60
  (= 59.46); i.e. **top margin (away from FPC) = 2.90 mm, bottom margin (FPC/COG ledge) =
  7.60 mm** (p.6). Visual-area chain 1.90 / 50.96 / 6.60. Width AA 36.72 centred (3.00 each
  side). FPC exits the **bottom 42.72-wide edge** (p.6).
- Budget arithmetic: board H (36.8) + battery band (22.66) = **59.46 = the BL height,
  exactly** (zero slack). Board width (42.72) = display width (42.72), zero margin per spec.

> **REFUTED sub-item:** `design-notes/mechanical-architecture.md` (line 13/30) budgets the
> board+battery against **59.26** ("Board + battery ≤ 59.26 → ~22.5 mm"). That is the CTP
> glass, not the module envelope. The correct governing height is **59.46**, giving the
> battery band **22.66 mm** (not "~22.5"). The prior reviewer note already flagged this
> (M3 in the synthesis); confirmed here. Under-budgeting by 0.20 mm is harmless to fit but
> the docs must read 59.46 / 22.66.

Verdict: **CONFIRMED** — 42.72 x 59.46 (BL frame) governs; battery band = 59.46 − 36.8 =
**22.66 mm**; active area offset 2.90 top / 7.60 bottom.

---

## VERDICT 2 — Battery fits in plan (42.72 x 22.66 zone): CONFIRMED

Zone = **42.72 (w, along x) x 22.66 (h, along y)**. Cell **EEMB LP502030 = 20.5 x 32.0 x
5.3 mm** (W x L x H) — dimensions independently confirmed (eemb.com; 250 mAh typ / 230 min).

Orientation: **32.0 mm along the WIDTH (42.72), 20.5 mm along the HEIGHT (22.66)**.
- **Height (y) axis:** 22.66 − 20.5 = **2.16 mm total margin** → ~1.08 mm top + ~1.08 mm
  bottom. Tight but real. FITS.
- **Width (x) axis:** 42.72 − 32.0 = **10.72 mm gross margin**, BUT the J9 mated plug eats
  into it (see below). Net free after the plug band ≈ **4.9 mm**. FITS.

**J9 plug intrusion (the real width constraint):** the cell ships with a mated **JST PHR-2**
plug; confirmed "whole plug width **5.8 mm**", 2 mm pole spacing (eemb). Side-entry J9 has its
mouth facing the battery zone, so this ~5.8 mm plug + wire-bend sits **in-plane inside the
band**, ~5–9 mm of it (JST ePH.pdf p.7 side-entry assembly layout gives **9.0 mm min**
board+mating clearance in the mating direction). Left-justified cell (0.5 mm wall gap) →
x 11.14..43.14; J9 at x≈46.5 → plug band ~43.6..49.4 → **~0.46 mm gap** cell-to-plug. OK.

**Largest real LiPo that fits 42.72 x 22.66 x ~5 mm:**
- **With the JST plug present:** effective clear cell envelope ≈ **20.5 x ~35 x 5.3 mm**.
  → **EEMB LP502030, 250 mAh** is the practical maximum (the DECIDED cell). LP502035
  (20.5 x 37 x 5.3, ~340 mAh) is 37 mm long → leaves only ~5.7 mm for plug + 2 clearances →
  plug band collides / cell hits the wall. **No** to LP502035 with a plugged connector.
- **If the battery is soldered (tabs) or uses a low-profile in-plane BTB** (frees the
  ~5.8 mm plug band): clear length ≈ ~40 mm → **EEMB LP502035 ~340 mAh** fits comfortably;
  LP502040 (42 mm, 400 mAh) is ~1 mm too long (42 > ~41 clear) → borderline no.

Verdict: **CONFIRMED** — LP502030 fits with margins **height 2.16 mm / width ~4.9 mm net**.
Largest = **250 mAh (LP502030) with the JST plug**, or **~340 mAh (LP502035) with solder
tabs**.

---

## VERDICT 3 — Battery/board fit in thickness (Z-stack): CONFIRMED it fits, but J9 makes it needlessly thick

Two INDEPENDENT Z-columns (they are in different in-plane regions, so they do **not** need
equal thickness — this directly answers the user's question):

- **Region L = the board** (y 34..70.8): display module + J2 gap + PCB + tallest F.Cu part.
- **Region T = the battery** (y 11.34..34, above the board, no PCB there): display module +
  battery + ferrite + NFC FPC.

Behind the shared display module (~2.3 mm, §2.2 p.5; the CTP/glass + bezel pushes the front
assembly to ~4.2 mm in the case — display-integration §1.1):

| Region | Stack behind the display module | Depth behind module |
|---|---|---|
| **L (board)** | J2 FFC connector gap **2.0** + PCB **1.6** + tallest F.Cu part **J9 = 6.0** | **9.6 mm** |
| **T (battery)** | battery **5.3** + ferrite **~0.5** + NFC FPC **~0.2** | **6.0 mm** |

- **J9 height = ~6.0 mm above F.Cu.** Verified from JST ePH.pdf: side-entry SMT SM4 body
  (p.5, SM4 side-entry drawing = **6.0 mm** overall height dimension) — corroborated by the
  distributor spec (~6.0 mm height above board) and the series header "7.5 mm in height after
  mounting / 4.5 mm width" (p.1, generic through-hole figure). **J9 is the tallest F.Cu
  part** on the board (next tallest: SW1 button / J1 USB-C ~3.2–3.5 mm, J6 JST-SH ~2.9 mm).
- **The two columns are NOT equal and need not be:** Region L (9.6 mm) is **3.6 mm deeper**
  than Region T (6.0 mm). A flat case-back is set by the **taller** column (L / J9), so the
  device thickness is dominated by J9, not the battery. The battery (5.3 mm) is comfortably
  thinner than board+parts — **battery Z is NOT the limiter; J9 is.**

**Total device thickness (governed by Region L):**
≈ front wall 0.8 + display module 2.3 + [J2 2.0 + PCB 1.6 + J9 6.0 = 9.6] + back wall 0.8
= **~13.5 mm cased** (~11.9 mm bare board+display+J9). This matches the completeness-critic
estimate ("≥~12 mm thick at J9", G8).

> **FLAG (J9 too tall):** the battery region only needs **6.0 mm** behind the display; J9
> forces **9.6 mm**. J9 alone adds **~2.5–3.5 mm** to the whole device for a "small & tidy"
> secure wallet. **Recommendation:** replace J9 (S2B-PH-SM4-TB, 6.0 mm) with **solder tabs /
> pads (~1.5 mm)** or a **low-profile in-plane BTB**. Region L then = 2.0 + 1.6 + ~3.5
> (SW1/USB-C become the tallest) = **~7.1 mm**, total **~11 mm cased** — ~2.5 mm thinner AND
> the two columns become comparable (7.1 vs 6.0). This ALSO removes the in-plane plug band
> that limits the cell length (Verdict 2) and the J9↔MH4 collision (Verdict 4). Strong,
> multi-benefit change.

Verdict: **CONFIRMED it fits** (battery 5.3 mm ≪ board-side 9.6 mm; nothing exceeds the case
back). Total ≈ **13.5 mm cased with J9 / ~11 mm with battery solder tabs.** Board- and
battery-side do **not** need equal thickness (separate columns); the flat case back is set by
the taller J9 column.

---

## VERDICT 4 — The 3 top connectors (J9, J6, J-ANT) fit across the 42.72 top edge: PARTIAL

Top strip after the Option-B shrink (top edge y=34, R2.5 fillets, MH3 (13.1,36.6) / MH4
(50.9,36.6), each Ø3.15 clearance → keep-out ±1.58). Usable inboard x for connector bodies
≈ **15.0 .. 48.5** (after ~1.3 mm edge + the two corner MH keep-outs). Connector x-widths
from board-truth: **J6** SM04B-SRSS-TB = 7.85; **J9** S2B-PH-SM4-TB body ~7.95 (courtyard
9.25); **J-ANT** (Trezor-style BM28B0.6-6DP BTB, per the NFC verdict) ≈ 4 x 3 mm.

Proposed x-layout (all mouths facing up into the battery zone, y-bodies ~35..42):
| Conn | Role | x-centre | Body x-span | Clear of? |
|---|---|---|---|---|
| **J6** | expansion (Qwiic) | **19.0** | 15.1..22.9 | MH3 (hole 11.5..14.7) ✓, R2.5 fillet ✓ |
| **J-ANT** | NFC FPC feed | **32.0** | ~30.0..34.0 | centred, clear both sides ✓ |
| **J9** | battery | **46.5** | 42.5..50.5 | **✗ overlaps MH4 (hole 49.3..52.5)** |

- J6 and J-ANT fit cleanly. The **conflict is J9 vs MH4**: to give the **32 mm** cell its
  clear span the DECIDED design shifts J9 right to **x≈46.5**, but the J9 **body** (±3.98)
  then reaches x=50.5 and **collides with the MH4 clearance hole at 50.9** (starts 49.3). The
  prior note's "still inboard of the MH4 fillet" is true only for the ~5.8 mm **plug band**
  (43.6..49.4), **not** for the full ~8 mm connector body/courtyard.
- Direct trade-off with a side-entry 8 mm-wide J9: at x≈44 the body clears MH4 (gap ~1.3 mm)
  but its plug band (41.1..46.9) only leaves ~30 mm for the cell (11.1..41.1) → **LP502030's
  32 mm no longer fits** (back to Verdict-2's "borderline 30 mm only"). You can have the
  32 mm cell **or** J9 clearing MH4 with this connector — not both.
- **Resolution (same fix as Verdict 3):** battery **solder tabs / low-profile pad pair**
  at the far right removes the 8 mm body AND the plug band → the 32 mm cell fits, MH4 is
  clear, and the device gets thinner. Alternatively accept a ~30 mm / lower-capacity cell,
  or nudge MH4 inboard (breaks the tidy corner-hole symmetry).

Verdict: **PARTIAL** — J6 + J-ANT fit; **J9 as a side-entry JST-PH at x≈46.5 collides with
MH4** and cannot coexist with the 32 mm cell. Fix by soldering the battery (removes body +
plug band) — which also resolves Verdicts 2 and 3.

---

## Bottom line (fit verdicts)
1. **Display outline — CONFIRMED.** 42.72 x **59.46** (BL frame) governs the budget, NOT
   59.26 (CTP glass, 0.20 mm shorter). Board 36.8 + battery 22.66 = 59.46 exactly. AA offset
   2.90 top / 7.60 bottom. (mechanical-architecture.md's 59.26 budget is **REFUTED**.)
2. **Battery in plan — CONFIRMED.** LP502030 (20.5 x 32.0 x 5.3) fits 42.72 x 22.66 with
   **height margin 2.16 mm** and **width margin ~4.9 mm net** (after the ~5.8 mm JST plug
   band). Largest cell = **250 mAh LP502030 with the JST plug**, **~340 mAh LP502035 with
   solder tabs**.
3. **Thickness — CONFIRMED it fits.** Total ≈ **13.5 mm cased** (~11.9 mm bare), **set by the
   J9 column (9.6 mm behind the display), not the battery (6.0 mm).** J9 (JST-PH, **6.0 mm**,
   JST ePH.pdf p.5) is the tallest F.Cu part and makes the device ~2.5–3.5 mm thicker than
   the battery needs → **use battery solder tabs / low-profile connector → ~11 mm.** The two
   sides are separate columns and need not be equal thickness.
4. **Three top connectors — PARTIAL.** J6 (x19) + J-ANT (x32) fit; **J9 at x46.5 collides
   with MH4** and can't coexist with the 32 mm cell using a side-entry JST-PH. Solder-tab the
   battery to fix.

**Single highest-leverage change:** replace the JST-PH battery connector (J9) with solder
tabs / a low-profile pad pair. It simultaneously (a) shrinks the device from ~13.5 to ~11 mm,
(b) lets the full 32 mm (or larger) cell fit in plan, and (c) removes the J9↔MH4 collision.
