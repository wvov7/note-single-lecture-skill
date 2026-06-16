#!/usr/bin/env python3
"""Audit bilingual translation coverage for note-single-lecture outputs.

The script checks two things:
1. translation_units.json has complete source, translation, and explanation fields.
2. Final Markdown notes do not contain English source quote/list blocks without a
   nearby Chinese translation label.

Usage:
  python audit_translations.py translation_units.json notes.md report.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


CHINESE_RE = re.compile(r"[\u4e00-\u9fff]")
ENGLISH_RE = re.compile(r"[A-Za-z]")
FENCE_RE = re.compile(r"^\s*```")
TRANSLATION_LABEL_RE = re.compile(r"(中文翻译|中文参考答案|中文译文|翻译：|翻译:)")


def has_chinese(text: str) -> bool:
    return bool(CHINESE_RE.search(text or ""))


def has_english(text: str) -> bool:
    return bool(ENGLISH_RE.search(text or ""))


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def searchable_markdown(text: str) -> str:
    text = re.sub(r"(?m)^\s*>\s?", "", text or "")
    text = re.sub(r"(?m)^\s*[-*]\s+", "", text)
    return normalize_space(text)


def load_units(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    problems: list[str] = []
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(data, dict):
        units = data.get("units")
    else:
        units = data
    if not isinstance(units, list):
        return [], ["translation_units.json must be a list or an object with a 'units' list."]
    normalized: list[dict[str, Any]] = []
    required = ["id", "slide", "type", "source", "translation", "explanation"]
    for idx, unit in enumerate(units, 1):
        if not isinstance(unit, dict):
            problems.append(f"Unit {idx} is not an object.")
            continue
        normalized.append(unit)
        label = str(unit.get("id") or f"#{idx}")
        for field in required:
            if not str(unit.get(field, "")).strip():
                problems.append(f"{label}: missing required field '{field}'.")
        source = str(unit.get("source", ""))
        translation = str(unit.get("translation", ""))
        explanation = str(unit.get("explanation", ""))
        if source and not has_english(source):
            problems.append(f"{label}: source should preserve English original text.")
        if translation and not has_chinese(translation):
            problems.append(f"{label}: translation must contain Chinese.")
        if explanation and not has_chinese(explanation):
            problems.append(f"{label}: explanation must contain Chinese.")
    return normalized, problems


def iter_note_blocks(text: str) -> list[dict[str, Any]]:
    """Return English-heavy quote/list blocks that should normally be translated."""
    blocks: list[dict[str, Any]] = []
    lines = text.splitlines()
    in_code = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if FENCE_RE.match(line):
            in_code = not in_code
            i += 1
            continue
        if in_code or not line.strip():
            i += 1
            continue

        stripped = line.strip()
        starts_quote = stripped.startswith(">")
        starts_list = bool(re.match(r"^[-*]\s+", stripped))
        if starts_quote or starts_list:
            block_lines = [stripped]
            start = i + 1
            i += 1
            while i < len(lines):
                nxt = lines[i].strip()
                if not nxt:
                    break
                if starts_quote and nxt.startswith(">"):
                    block_lines.append(nxt)
                    i += 1
                    continue
                if starts_list and re.match(r"^[-*]\s+", nxt):
                    block_lines.append(nxt)
                    i += 1
                    continue
                break
            end = i
            raw = "\n".join(block_lines)
            cleaned = re.sub(r"(^|\n)\s*(>|[-*])\s*", " ", raw)
            if has_english(cleaned) and not has_chinese(cleaned):
                blocks.append({"line": start, "end_line": end, "text": normalize_space(cleaned)})
            continue
        i += 1
    return blocks


def has_nearby_translation(lines: list[str], end_line: int, lookahead: int) -> bool:
    begin = end_line
    end = min(len(lines), end_line + lookahead)
    window = "\n".join(lines[begin:end])
    return bool(TRANSLATION_LABEL_RE.search(window) and has_chinese(window))


def audit_notes(notes_path: Path, units: list[dict[str, Any]], lookahead: int) -> list[dict[str, Any]]:
    text = notes_path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    issues: list[dict[str, Any]] = []

    for block in iter_note_blocks(text):
        if not has_nearby_translation(lines, block["end_line"], lookahead):
            issues.append(
                {
                    "kind": "missing_nearby_translation",
                    "line": block["line"],
                    "text": block["text"][:220],
                    "message": "English source block is not followed by a nearby Chinese translation label.",
                }
            )

    normalized_notes = searchable_markdown(text)
    for unit in units:
        source = searchable_markdown(str(unit.get("source", "")))
        if not source:
            continue
        probe = source[:120]
        if len(probe) >= 30 and probe not in normalized_notes:
            issues.append(
                {
                    "kind": "unit_not_found_in_notes",
                    "unit_id": unit.get("id"),
                    "source_preview": probe,
                    "message": "translation_units.json source does not appear in final notes.",
                }
            )
    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("units", type=Path)
    parser.add_argument("notes", type=Path)
    parser.add_argument("report", type=Path)
    parser.add_argument("--lookahead", type=int, default=6)
    parser.add_argument("--warn-only", action="store_true")
    args = parser.parse_args()

    units, unit_problems = load_units(args.units)
    note_issues = audit_notes(args.notes, units, args.lookahead)
    report = {
        "translation_units": str(args.units),
        "notes": str(args.notes),
        "unit_count": len(units),
        "unit_problems": unit_problems,
        "note_issues": note_issues,
        "ok": not unit_problems and not note_issues,
    }
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["ok"] or args.warn_only:
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
