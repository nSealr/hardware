#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOARD_NAME = "tropic01-universal-secure-device"
BOARD_DIR = ROOT / "pcb" / BOARD_NAME
PCB_FILE = BOARD_DIR / "kicad" / f"{BOARD_NAME}.kicad_pcb"
SCHEMATIC_BINDING_JSON = BOARD_DIR / "production" / "schematic-binding.json"


def quote_kicad_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def find_matching_parenthesis(text: str, open_index: int) -> int:
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_index, len(text)):
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
                return index
    raise ValueError(f"unclosed s-expression at byte {open_index}")


def iter_blocks(text: str, line_pattern: str) -> list[tuple[int, int, str]]:
    blocks: list[tuple[int, int, str]] = []
    for match in re.finditer(line_pattern, text, flags=re.MULTILINE):
        open_index = text.index("(", match.start(), match.end())
        end = find_matching_parenthesis(text, open_index) + 1
        blocks.append((match.start(), end, text[match.start() : end]))
    return blocks


def collect_pad_nets(binding: dict[str, object]) -> dict[str, dict[str, str]]:
    components = binding["components"]
    pad_nets: dict[str, dict[str, str]] = {}
    for ref, component in components.items():
        pins = component["pins"]
        for pin_key, pin in pins.items():
            net_name = pin["net"]
            physical_pin = pin.get("physical_pin")
            pad_name = str(physical_pin if physical_pin is not None else pin_key)
            pad_nets.setdefault(ref, {})[pad_name] = net_name
    return pad_nets


def collect_net_ids(pad_nets: dict[str, dict[str, str]]) -> dict[str, int]:
    net_names = sorted({net_name for pads in pad_nets.values() for net_name in pads.values()})
    return {net_name: index for index, net_name in enumerate(net_names, start=1)}


def replace_net_declarations(board_text: str, net_ids: dict[str, int]) -> str:
    net_line = re.compile(r'\n\t\(net\s+\d+\s+"[^"]*"\)')
    first = net_line.search(board_text)
    if first is None:
        raise ValueError("PCB file has no top-level net declaration")

    end = first.end()
    while True:
        next_match = net_line.match(board_text, end)
        if next_match is None:
            break
        end = next_match.end()

    declarations = ['\n\t(net 0 "")']
    declarations.extend(
        f"\n\t(net {net_id} {quote_kicad_string(net_name)})"
        for net_name, net_id in sorted(net_ids.items(), key=lambda item: item[1])
    )
    return board_text[: first.start()] + "".join(declarations) + board_text[end:]


def reference_for_footprint(footprint_block: str) -> str | None:
    match = re.search(r'\(property "Reference" "([^"]+)"', footprint_block)
    return match.group(1) if match else None


def replace_pad_net(pad_block: str, net_id: int, net_name: str) -> str:
    replacement = f'\n\t\t\t(net {net_id} {quote_kicad_string(net_name)})'
    if re.search(r'\n\t\t\t\(net\s+\d+\s+"[^"]*"\)', pad_block):
        return re.sub(r'\n\t\t\t\(net\s+\d+\s+"[^"]*"\)', replacement, pad_block, count=1)

    insert_at = pad_block.rfind("\n\t\t)")
    if insert_at == -1:
        raise ValueError("pad block has no closing pad line")
    return pad_block[:insert_at] + replacement + pad_block[insert_at:]


def pad_name_for_block(pad_block: str) -> str:
    match = re.match(r'\t\t\(pad "([^"]*)"', pad_block)
    if match is None:
        raise ValueError("pad block has no pad name")
    return match.group(1)


def update_footprint_pads(footprint_block: str, ref: str, pad_nets: dict[str, str], net_ids: dict[str, int]) -> str:
    updated_parts: list[str] = []
    previous_end = 0
    seen_pads: set[str] = set()
    for start, end, pad_block in iter_blocks(footprint_block, r'^\t\t\(pad "[^"]*"'):
        pad_name = pad_name_for_block(pad_block)
        if pad_name in pad_nets:
            net_name = pad_nets[pad_name]
            pad_block = replace_pad_net(pad_block, net_ids[net_name], net_name)
            seen_pads.add(pad_name)
        updated_parts.append(footprint_block[previous_end:start])
        updated_parts.append(pad_block)
        previous_end = end

    missing_pads = sorted(set(pad_nets) - seen_pads, key=lambda value: (not value.isdigit(), value))
    if missing_pads:
        raise ValueError(f"{ref} footprint is missing bound pads: {', '.join(missing_pads)}")

    updated_parts.append(footprint_block[previous_end:])
    return "".join(updated_parts)


def update_footprints(board_text: str, pad_nets_by_ref: dict[str, dict[str, str]], net_ids: dict[str, int]) -> str:
    updated_parts: list[str] = []
    previous_end = 0
    seen_refs: set[str] = set()

    for start, end, footprint_block in iter_blocks(board_text, r'^\t\(footprint "[^"]+"'):
        ref = reference_for_footprint(footprint_block)
        if ref in pad_nets_by_ref:
            footprint_block = update_footprint_pads(footprint_block, ref, pad_nets_by_ref[ref], net_ids)
            seen_refs.add(ref)
        updated_parts.append(board_text[previous_end:start])
        updated_parts.append(footprint_block)
        previous_end = end

    missing_refs = sorted(set(pad_nets_by_ref) - seen_refs)
    if missing_refs:
        raise ValueError(f"PCB file is missing bound footprints: {', '.join(missing_refs)}")

    updated_parts.append(board_text[previous_end:])
    return "".join(updated_parts)


def materialize() -> None:
    binding = json.loads(SCHEMATIC_BINDING_JSON.read_text(encoding="utf-8"))
    pad_nets_by_ref = collect_pad_nets(binding)
    net_ids = collect_net_ids(pad_nets_by_ref)

    board_text = PCB_FILE.read_text(encoding="utf-8")
    board_text = replace_net_declarations(board_text, net_ids)
    board_text = update_footprints(board_text, pad_nets_by_ref, net_ids)
    PCB_FILE.write_text(board_text, encoding="utf-8")


if __name__ == "__main__":
    materialize()
