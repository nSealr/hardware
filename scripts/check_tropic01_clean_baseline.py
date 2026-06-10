#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOARD = ROOT / "pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_pcb"

MANDATORY_REFS = {
    "U1",
    "U2",
    "U3",
    "U4",
    "U5",
    "U7",
    "U8",
    "U9",
    "U10",
    "U11",
    "U13",
    "U14",
    "U15",
    "J1",
    "J2",
    "J2B",
    "J6",
    "J9",
    "SW1",
    "LED1",
    "RLED1",
    "MH1",
    "MH2",
    "X1",
    "X3",
    "DISP1",
    "ANT1",
    "BAT1",
    "TP_SWDIO",
    "TP_SWCLK",
    "TP_NRST",
    "TP_BOOT0",
    "TP_UART_TX",
    "TP_UART_RX",
    "TP_3V3",
    "TP_GND",
}

DISPLAY_SIDE_REFS = {"J2", "J2B", "DISP1"}
BOARD_ONLY_REFS = {"DISP1", "ANT1", "BAT1"}
ALLOWED_LOCAL_RENDER_MODELS = {
    "J9": "${KIPRJMOD}/models/nsealr_jst_ph_2p.wrl",
}


def find_matching(text: str, start: int) -> int:
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index + 1
    raise ValueError("unbalanced KiCad s-expression")


def blocks(text: str, token: str) -> list[str]:
    found: list[str] = []
    cursor = 0
    while True:
        start = text.find(token, cursor)
        if start == -1:
            return found
        end = find_matching(text, start)
        found.append(text[start:end])
        cursor = end


def property_value(block: str, name: str) -> str | None:
    match = re.search(rf'\(property "{re.escape(name)}" "([^"]+)"', block)
    return match.group(1) if match else None


def footprint_layer(block: str) -> str:
    match = re.search(r'\n\t\t\(layer "([^"]+)"\)', block)
    return match.group(1) if match else ""


def board_outline(text: str) -> tuple[float, float, float, float] | None:
    for block in blocks(text, "(gr_rect"):
        if '(layer "Edge.Cuts")' not in block:
            continue
        match = re.search(
            r"\(start ([-0-9.]+) ([-0-9.]+)\).*?\(end ([-0-9.]+) ([-0-9.]+)\)",
            block,
            re.S,
        )
        if match is None:
            continue
        return tuple(float(value) for value in match.groups())  # type: ignore[return-value]
    return None


def main() -> int:
    text = BOARD.read_text(encoding="utf-8", errors="replace")
    errors: list[str] = []

    for token in ("(gr_text", "(gr_line", "(gr_poly"):
        for block in blocks(text, token):
            if '(layer "Cmts.User")' in block or '(layer "Dwgs.User")' in block:
                errors.append(f"stale user drawing remains: {token}")
                break
    for block in blocks(text, "(gr_rect"):
        if '(layer "Cmts.User")' in block or '(layer "Dwgs.User")' in block:
            errors.append("stale user drawing remains: (gr_rect")
            break

    outline = board_outline(text)
    if outline != (10.0, 34.0, 54.0, 70.0):
        errors.append(f"unexpected compact PCB outline: {outline}")

    refs_by_layer: dict[str, str] = {}
    for block in blocks(text, "(footprint "):
        ref = property_value(block, "Reference")
        if ref is not None:
            refs_by_layer[ref] = footprint_layer(block)
            for model_path in re.findall(r'\(model "([^"]+)"', block):
                if not model_path.startswith("${KIPRJMOD}/models/nsealr_"):
                    continue
                if ALLOWED_LOCAL_RENDER_MODELS.get(ref) != model_path:
                    errors.append(f"unverified local model on {ref}: {model_path}")

    missing = sorted(MANDATORY_REFS - set(refs_by_layer))
    if missing:
        errors.append(f"missing mandatory refs: {', '.join(missing)}")

    forbidden_back_refs = sorted(
        ref
        for ref, layer in refs_by_layer.items()
        if layer == "B.Cu" and ref not in DISPLAY_SIDE_REFS
    )
    if forbidden_back_refs:
        errors.append(f"B.Cu contains non-display refs: {', '.join(forbidden_back_refs)}")

    front_only_failures = sorted(
        ref
        for ref in MANDATORY_REFS - DISPLAY_SIDE_REFS - BOARD_ONLY_REFS
        if refs_by_layer.get(ref) != "F.Cu"
    )
    if front_only_failures:
        errors.append(f"mandatory electronics refs not on F.Cu: {', '.join(front_only_failures)}")

    if errors:
        print("clean baseline: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("clean baseline: PASS")
    print(f"mandatory refs: {len(MANDATORY_REFS)}")
    print("B.Cu refs allowed:", ", ".join(sorted(DISPLAY_SIDE_REFS)))
    print("PCB outline: 44.0 x 36.0 mm at x=10..54 y=34..70")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
