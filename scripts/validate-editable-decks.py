#!/usr/bin/env python3
"""Validate editable deck runtime contracts across generated preset decks.

This script is intentionally static and quick. It complements
validate-template-ports.py by checking feature/runtime contracts that are shared
by legacy preset decks, ported template decks, and the canonical reference.
"""

from __future__ import annotations

import re
import sys
import time
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRESETS_DIR = ROOT / "examples" / "generated" / "presets"
REFERENCE = ROOT / "examples" / "editable-deck-reference.html"
EXPECTED_PRESET_COUNT = 46


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


TITLE_LIKE_CLASSES = {
    "title",
    "ttl",
    "headline",
    "heading",
    "deck-title",
    "slide-title",
    "stmt",
    "h",
    "h1",
    "h2",
    "h3",
    "h4",
}


class AttrParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.slide_ids: list[str] = []
        self.object_ids: list[str] = []
        self.slide_count = 0
        self.edit_slot_count = 0
        self.slide_object_count = 0
        self.graphic_editable_count = 0
        self.in_deck = False

    def handle_starttag(self, tag: str, attrs_list) -> None:
        tag = tag.lower()
        attrs = {name.lower(): value for name, value in attrs_list}
        classes = set((attrs.get("class") or "").split())
        if attrs.get("id") == "deck" or "slides-offset" in classes:
            self.in_deck = True
        if tag == "section" and "slide" in classes:
            self.slide_count += 1
            self.slide_ids.append(attrs.get("id") or "")
        if "data-oid" in attrs:
            self.object_ids.append(attrs.get("data-oid") or "")
        has_object = "data-slide-object" in attrs
        has_slot = "data-edit-slot" in attrs
        if has_object:
            self.slide_object_count += 1
        if has_slot:
            self.edit_slot_count += 1
        if attrs.get("data-object-type") in {"graphic", "image", "video"} or attrs.get("data-slot-type") == "image":
            if has_slot or has_object:
                self.graphic_editable_count += 1


class TitleLikeAuditParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[dict] = []
        self.issues: list[str] = []

    def handle_starttag(self, tag: str, attrs_list) -> None:
        tag = tag.lower()
        attrs = {name.lower(): value for name, value in attrs_list}
        classes = set((attrs.get("class") or "").split())
        parent_editable = any(frame["editable_context"] for frame in self.stack)
        own_editable = "data-edit-slot" in attrs or "data-slide-object" in attrs
        title_like = tag in {"h1", "h2", "h3", "h4"} or (tag != "section" and bool(classes & TITLE_LIKE_CLASSES))
        frame = {
            "tag": tag,
            "classes": classes,
            "editable_context": parent_editable or own_editable,
            "title_like": title_like,
            "text": [],
        }
        self.stack.append(frame)

    def handle_data(self, data: str) -> None:
        for frame in self.stack:
            if frame["title_like"]:
                frame["text"].append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if not self.stack:
            return
        index = None
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                index = i
                break
        if index is None:
            return
        closing = self.stack[index:]
        self.stack = self.stack[:index]
        for frame in reversed(closing):
            text = re.sub(r"\s+", " ", " ".join(frame["text"])).strip()
            if frame["title_like"] and text and not frame["editable_context"]:
                cls = " ".join(sorted(frame["classes"])) or "-"
                self.issues.append(f"<{frame['tag']} class=\"{cls}\"> {text[:72]}")


def parse_attrs(source: str) -> AttrParser:
    parser = AttrParser()
    parser.feed(source)
    return parser


def title_like_issues(source: str) -> list[str]:
    parser = TitleLikeAuditParser()
    parser.feed(source)
    return parser.issues


def fail(errors: list[str], rel: str, message: str) -> None:
    errors.append(f"{rel}: {message}")


def validate_source(path: Path, source: str, errors: list[str], *, generated: bool) -> None:
    rel = display_path(path)
    parsed = parse_attrs(source)
    if not parsed.slide_ids:
        fail(errors, rel, "missing section.slide nodes")
    if any(not slide_id for slide_id in parsed.slide_ids):
        fail(errors, rel, "one or more slides are missing id attributes")
    if len(parsed.slide_ids) != len(set(parsed.slide_ids)):
        fail(errors, rel, "slide ids are not unique")
    if parsed.object_ids and len(parsed.object_ids) != len(set(parsed.object_ids)):
        fail(errors, rel, "data-oid values are not unique")
    if "querySelectorAll('section.slide')" in source or 'querySelectorAll("section.slide")' in source:
        fail(errors, rel, "uses global section.slide query")
    if ":scope > section.slide" not in source:
        fail(errors, rel, "missing scoped :scope > section.slide query")

    required_tokens = {
        "sidebar copy button": "data-filmstrip-action",
        "sidebar new page button": "id=\"btnNewPage\"",
        "copy slide method": "_copySlide(index)",
        "new page method": "_newPageAfterCurrent()",
        "slide id normalizer": "renumberDeckSlides",
        "object id normalizer": "renumberDeckObjects",
        "blank slide factory": "createBlankSlideFromPreset",
        "mobile adaptation marker": "data-mobile-adaptation",
        "mobile portrait css": "@media (max-width: 700px) and (orientation: portrait)",
        "mobile landscape css": "@media (max-height: 500px) and (orientation: landscape)",
    }
    for label, token in required_tokens.items():
        if token not in source:
            fail(errors, rel, f"missing {label}")

    if "function exportHtml" not in source:
        fail(errors, rel, "missing exportHtml()")
    if "sanitizeExportDocument" not in source:
        fail(errors, rel, "missing sanitizeExportDocument()")
    if "localStorage.setItem" not in source:
        fail(errors, rel, "missing localStorage save path")
    if generated:
        if parsed.slide_object_count == 0 and parsed.edit_slot_count == 0:
            fail(errors, rel, "deck has no editable objects or slots")
        if parsed.edit_slot_count > 0:
            deck_match = re.search(r'<div\b[^>]*\bid=["\']deck["\'][^>]*>(.*?)(?:</div>\s*<script|<script)', source, flags=re.I | re.S)
            deck_source = deck_match.group(1) if deck_match else source
            issues = title_like_issues(deck_source)
            if issues:
                fail(errors, rel, "title-like authored text is not editable: " + "; ".join(issues[:3]))
        elif parsed.slide_object_count > 0 and ".slide-object-text" not in source:
            fail(errors, rel, "legacy deck has no editable text objects")


def main() -> int:
    started = time.perf_counter()
    errors: list[str] = []
    if len(sys.argv) == 3 and sys.argv[1] == "--file":
        path = Path(sys.argv[2])
        if not path.is_file():
            print(f"missing {path}", file=sys.stderr)
            return 1
        validate_source(path, path.read_text(encoding="utf-8"), errors, generated=True)
        if errors:
            print("Editable deck validation failed:")
            for error in errors:
                print(f"- {error}")
            return 2
        elapsed = time.perf_counter() - started
        print(f"Validated editable runtime contract for {display_path(path)} in {elapsed:.2f}s.")
        return 0
    if len(sys.argv) != 1:
        print("Usage: validate-editable-decks.py [--file path/to/deck.html]", file=sys.stderr)
        return 1
    if not REFERENCE.is_file():
        errors.append(f"missing {REFERENCE.relative_to(ROOT)}")
    else:
        validate_source(REFERENCE, REFERENCE.read_text(encoding="utf-8"), errors, generated=False)

    if not PRESETS_DIR.is_dir():
        errors.append(f"missing {PRESETS_DIR.relative_to(ROOT)}")
    else:
        files = sorted(PRESETS_DIR.glob("*.html"))
        if len(files) != EXPECTED_PRESET_COUNT:
            errors.append(f"expected {EXPECTED_PRESET_COUNT} generated presets, found {len(files)}")
        for path in files:
            validate_source(path, path.read_text(encoding="utf-8"), errors, generated=True)

    if errors:
        print("Editable deck validation failed:")
        for error in errors:
            print(f"- {error}")
        return 2
    elapsed = time.perf_counter() - started
    print(f"Validated editable runtime contracts for {EXPECTED_PRESET_COUNT} presets and reference in {elapsed:.2f}s.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
