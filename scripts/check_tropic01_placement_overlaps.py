#!/usr/bin/env python3
from __future__ import annotations

import math
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOARD = ROOT / "pcb/tropic01-universal-secure-device/kicad/tropic01-universal-secure-device.kicad_pcb"


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


def sexpr_blocks(text: str, token: str) -> list[str]:
    blocks: list[str] = []
    cursor = 0
    while True:
        start = text.find(token, cursor)
        if start == -1:
            return blocks
        end = find_matching(text, start)
        blocks.append(text[start:end])
        cursor = end


def property_value(block: str, name: str) -> str | None:
    match = re.search(rf'\(property "{re.escape(name)}" "([^"]+)"', block)
    return match.group(1) if match else None


def footprint_at(block: str) -> tuple[float, float, float] | None:
    match = re.search(r"\(at ([-0-9.]+) ([-0-9.]+)(?: ([-0-9.]+))?\)", block)
    if match is None:
        return None
    return float(match.group(1)), float(match.group(2)), float(match.group(3) or 0.0)


def footprint_layer(block: str) -> str:
    match = re.search(r'\(layer "([^"]+)"\)', block)
    return match.group(1) if match else ""


def courtyard_points(block: str) -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = []
    for token in ("(fp_line", "(fp_rect"):
        for child in sexpr_blocks(block, token):
            if ".CrtYd" not in child:
                continue
            match = re.search(
                r"\(start ([-0-9.]+) ([-0-9.]+)\).*?\(end ([-0-9.]+) ([-0-9.]+)\)",
                child,
                re.S,
            )
            if match is None:
                continue
            x1, y1, x2, y2 = (float(value) for value in match.groups())
            points.extend(((x1, y1), (x1, y2), (x2, y1), (x2, y2)))
    for child in sexpr_blocks(block, "(fp_circle"):
        if ".CrtYd" not in child:
            continue
        match = re.search(
            r"\(center ([-0-9.]+) ([-0-9.]+)\).*?\(end ([-0-9.]+) ([-0-9.]+)\)",
            child,
            re.S,
        )
        if match is None:
            continue
        center_x, center_y, end_x, end_y = (float(value) for value in match.groups())
        radius = math.hypot(end_x - center_x, end_y - center_y)
        points.extend(((center_x - radius, center_y - radius), (center_x + radius, center_y + radius)))
    return points


def transform_points(points: list[tuple[float, float]], at: tuple[float, float, float]) -> list[tuple[float, float]]:
    origin_x, origin_y, rotation_degrees = at
    angle = math.radians(rotation_degrees)
    cosine = math.cos(angle)
    sine = math.sin(angle)
    return [
        (origin_x + cosine * x - sine * y, origin_y + sine * x + cosine * y)
        for x, y in points
    ]


def footprint_bounds() -> list[tuple[str, str, float, float, float, float]]:
    text = BOARD.read_text(encoding="utf-8", errors="replace")
    bounds: list[tuple[str, str, float, float, float, float]] = []
    for block in sexpr_blocks(text, "(footprint "):
        reference = property_value(block, "Reference")
        at = footprint_at(block)
        points = courtyard_points(block)
        if reference is None or at is None or not points:
            continue
        world_points = transform_points(points, at)
        xs = [point[0] for point in world_points]
        ys = [point[1] for point in world_points]
        bounds.append((reference, footprint_layer(block), min(xs), min(ys), max(xs), max(ys)))
    return bounds


def overlaps() -> list[tuple[float, float, float, str, str, str]]:
    items = footprint_bounds()
    found: list[tuple[float, float, float, str, str, str]] = []
    for index, first in enumerate(items):
        for second in items[index + 1 :]:
            if first[1] != second[1]:
                continue
            overlap_x = min(first[4], second[4]) - max(first[2], second[2])
            overlap_y = min(first[5], second[5]) - max(first[3], second[3])
            if overlap_x > 0.02 and overlap_y > 0.02:
                found.append((overlap_x * overlap_y, overlap_x, overlap_y, first[0], second[0], first[1]))
    return sorted(found, reverse=True)


def main() -> int:
    found = overlaps()
    print(f"courtyard overlaps: {len(found)}")
    for area, overlap_x, overlap_y, first, second, layer in found[:120]:
        print(f"{first:12s} {second:12s} {layer:5s} {overlap_x:.2f} x {overlap_y:.2f} mm area {area:.2f}")
    return 1 if found else 0


if __name__ == "__main__":
    raise SystemExit(main())
