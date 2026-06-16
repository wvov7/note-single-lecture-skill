#!/usr/bin/env python3
"""Render a simple left-to-right mind map PNG from a JSON tree.

Usage:
  python render_mindmap.py outline.json output.png
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


PALETTE = [
    "#2563eb",
    "#16a34a",
    "#f97316",
    "#ef4444",
    "#8b5cf6",
    "#06b6d4",
    "#84cc16",
    "#ec4899",
]


@dataclass
class Node:
    title: str
    children: list["Node"] = field(default_factory=list)
    depth: int = 0
    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0
    color: str = "#2563eb"


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


FONT = load_font(28)
FONT_BOLD = load_font(32, bold=True)
FONT_ROOT = load_font(38, bold=True)


def parse(obj: dict[str, Any], depth: int = 0, color: str = "#2563eb") -> Node:
    title = str(obj.get("title", "")).strip()
    children_raw = obj.get("children", []) or []
    node = Node(title=title, depth=depth, color=color)
    for i, child in enumerate(children_raw):
        child_color = PALETTE[i % len(PALETTE)] if depth == 0 else color
        node.children.append(parse(child, depth + 1, child_color))
    return node


def wrap_text(text: str, max_chars: int) -> list[str]:
    if len(text) <= max_chars:
        return [text]
    lines: list[str] = []
    cur = ""
    for ch in text:
        cur += ch
        if len(cur) >= max_chars and ch in " ，、；;：:（）()/-":
            lines.append(cur.strip())
            cur = ""
        elif len(cur) >= max_chars + 4:
            lines.append(cur.strip())
            cur = ""
    if cur.strip():
        lines.append(cur.strip())
    return lines


def text_size(draw: ImageDraw.ImageDraw, lines: list[str], font: ImageFont.ImageFont) -> tuple[int, int]:
    widths = []
    heights = []
    for line in lines:
        box = draw.textbbox((0, 0), line, font=font)
        widths.append(box[2] - box[0])
        heights.append(box[3] - box[1])
    return (max(widths) if widths else 0, sum(heights) + max(0, len(lines) - 1) * 8)


def measure(node: Node, draw: ImageDraw.ImageDraw) -> None:
    max_chars = max(12, 24 - node.depth * 2)
    font = FONT_ROOT if node.depth == 0 else FONT_BOLD if node.depth == 1 else FONT
    lines = wrap_text(node.title, max_chars)
    tw, th = text_size(draw, lines, font)
    node.w = min(max(tw + 34, 140), 520)
    node.h = max(th + 24, 54)
    for child in node.children:
        measure(child, draw)


def subtree_height(node: Node) -> int:
    if not node.children:
        return node.h
    return max(node.h, sum(subtree_height(c) for c in node.children) + (len(node.children) - 1) * 36)


def assign_positions(node: Node, x: int, top: int, level_gap: int) -> None:
    node.x = x
    total = subtree_height(node)
    node.y = top + total // 2
    child_top = top
    for child in node.children:
        h = subtree_height(child)
        assign_positions(child, x + level_gap, child_top, level_gap)
        child_top += h + 36


def max_depth(node: Node) -> int:
    return max([node.depth] + [max_depth(c) for c in node.children])


def iter_nodes(node: Node):
    yield node
    for child in node.children:
        yield from iter_nodes(child)


def draw_curve(draw: ImageDraw.ImageDraw, a: Node, b: Node) -> None:
    x1 = a.x + a.w // 2
    y1 = a.y
    x2 = b.x - b.w // 2
    y2 = b.y
    mx = (x1 + x2) // 2
    points = []
    for i in range(28):
        t = i / 27
        x = (1 - t) ** 3 * x1 + 3 * (1 - t) ** 2 * t * mx + 3 * (1 - t) * t**2 * mx + t**3 * x2
        y = (1 - t) ** 3 * y1 + 3 * (1 - t) ** 2 * t * y1 + 3 * (1 - t) * t**2 * y2 + t**3 * y2
        points.append((x, y))
    draw.line(points, fill=b.color, width=4)
    r = 7
    draw.ellipse((x2 - r, y2 - r, x2 + r, y2 + r), outline=b.color, fill="white", width=3)


def draw_node(draw: ImageDraw.ImageDraw, node: Node) -> None:
    font = FONT_ROOT if node.depth == 0 else FONT_BOLD if node.depth == 1 else FONT
    max_chars = max(12, 24 - node.depth * 2)
    lines = wrap_text(node.title, max_chars)
    x0 = node.x - node.w // 2
    y0 = node.y - node.h // 2
    x1 = node.x + node.w // 2
    y1 = node.y + node.h // 2
    if node.depth == 0:
        draw.rounded_rectangle((x0, y0, x1, y1), radius=18, outline=node.color, fill="white", width=4)
    elif node.depth == 1:
        draw.rounded_rectangle((x0, y0, x1, y1), radius=16, outline=node.color, fill="#ffffff", width=3)
    else:
        draw.line((x0, y1, x1, y1), fill=node.color, width=3)
    tw, th = text_size(draw, lines, font)
    y = node.y - th // 2
    for line in lines:
        box = draw.textbbox((0, 0), line, font=font)
        lw = box[2] - box[0]
        lh = box[3] - box[1]
        draw.text((node.x - lw // 2, y), line, fill="#111827", font=font)
        y += lh + 8


def render(data: dict[str, Any], output: Path) -> None:
    root = parse(data)
    scratch = Image.new("RGB", (10, 10), "white")
    draw = ImageDraw.Draw(scratch)
    measure(root, draw)
    depth = max_depth(root)
    level_gap = 500
    margin_x = 120
    margin_y = 90
    height = subtree_height(root) + margin_y * 2
    width = margin_x * 2 + (depth + 1) * level_gap
    assign_positions(root, margin_x + root.w // 2, margin_y, level_gap)

    # Expand canvas if long labels extend beyond default width.
    max_right = max(n.x + n.w // 2 for n in iter_nodes(root)) + margin_x
    width = max(width, max_right)

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    for node in iter_nodes(root):
        for child in node.children:
            draw_curve(draw, node, child)
    for node in iter_nodes(root):
        draw_node(draw, node)

    output.parent.mkdir(parents=True, exist_ok=True)
    img.save(output)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("Usage: python render_mindmap.py outline.json output.png", file=sys.stderr)
        return 2
    data = json.loads(Path(argv[1]).read_text(encoding="utf-8-sig"))
    render(data, Path(argv[2]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
