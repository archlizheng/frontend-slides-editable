#!/usr/bin/env python3
"""Validate generated editable preset decks.

This is intentionally static and fast. It catches the regressions that have
historically broken editable decks before screenshot/browser checks run.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRESETS_DIR = ROOT / "examples" / "generated" / "presets"
LEGACY_PRESET_COUNT = 12
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


def load_builder_ports():
    builder_path = ROOT / "scripts" / "build-template-port-decks.py"
    spec = importlib.util.spec_from_file_location("build_template_port_decks", builder_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Unable to load {builder_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.PORTS


def find_slide_ids(source: str) -> list[str]:
    ids: list[str] = []
    for match in re.finditer(r"<section\b(?=[^>]*\bclass=[\"'][^\"']*\bslide\b)[^>]*>", source, flags=re.I):
        id_match = re.search(r'\bid=["\']([^"\']+)["\']', match.group(0), flags=re.I)
        ids.append(id_match.group(1) if id_match else "")
    return ids


def deck_markup_only(source: str) -> str:
    deck_match = re.search(r'<div\b[^>]*\bid=["\']deck["\'][^>]*>', source, flags=re.I)
    if not deck_match:
        return source
    script_pos = source.find("<script", deck_match.end())
    return source[deck_match.start() :] if script_pos < 0 else source[deck_match.start() : script_pos]


def class_tokens_from_value(value: str | None) -> set[str]:
    return set((value or "").split())


def is_title_like_node(tag: str, classes: set[str]) -> bool:
    tag = tag.lower()
    if tag in {"h1", "h2", "h3", "h4"}:
        return True
    if classes & TITLE_LIKE_CLASSES:
        return True
    return False


class TitleSlotAuditParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[dict] = []
        self.in_deck = False
        self.issues: list[str] = []

    def handle_starttag(self, tag: str, attrs_list) -> None:
        tag = tag.lower()
        attrs = {name.lower(): value for name, value in attrs_list}
        if tag == "div" and attrs.get("id") == "deck":
            self.in_deck = True

        parent_slot_context = any(frame["slot_context"] for frame in self.stack)
        has_slot = "data-edit-slot" in attrs
        if has_slot:
            for frame in self.stack:
                frame["has_slot_descendant"] = True

        classes = class_tokens_from_value(attrs.get("class"))
        frame = {
            "tag": tag,
            "classes": classes,
            "aria_hidden": "aria-hidden" in attrs,
            "slot_context": parent_slot_context or has_slot,
            "has_slot_descendant": False,
            "title_like": self.in_deck and is_title_like_node(tag, classes),
            "text": [],
            "deck_root": self.in_deck and tag == "div" and attrs.get("id") == "deck",
        }
        self.stack.append(frame)

    def handle_data(self, data: str) -> None:
        if not self.in_deck:
            return
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
            if frame["title_like"]:
                text = re.sub(r"\s+", " ", " ".join(frame["text"])).strip()
                if (
                    text
                    and not frame["aria_hidden"]
                    and not frame["slot_context"]
                    and not frame["has_slot_descendant"]
                ):
                    cls = " ".join(sorted(frame["classes"])) or "-"
                    self.issues.append(f"<{frame['tag']} class=\"{cls}\"> {text[:64]}")
            if frame["deck_root"]:
                self.in_deck = False


def find_uneditable_title_like_nodes(source: str) -> list[str]:
    parser = TitleSlotAuditParser()
    parser.feed(deck_markup_only(source))
    return parser.issues


def fail(errors: list[str], rel: str, message: str) -> None:
    errors.append(f"{rel}: {message}")


def validate_common(path: Path, source: str, errors: list[str]) -> None:
    rel = str(path.relative_to(ROOT))
    slide_ids = find_slide_ids(source)
    if not slide_ids:
        fail(errors, rel, "no <section class=\"slide\"> nodes found")
    if any(not slide_id for slide_id in slide_ids):
        fail(errors, rel, "one or more slides are missing stable id attributes")
    if len(slide_ids) != len(set(slide_ids)):
        fail(errors, rel, "slide ids are not unique")
    if "querySelectorAll('section.slide')" in source or 'querySelectorAll("section.slide")' in source:
        fail(errors, rel, "uses global querySelectorAll('section.slide')")
    if ":scope > section.slide" not in source:
        fail(errors, rel, "missing scoped :scope > section.slide deck query")
    if "localStorage.setItem" not in source:
        fail(errors, rel, "missing localStorage save path")
    if "function exportHtml" not in source:
        fail(errors, rel, "missing exportHtml()")
    if "sanitizeEditableState" not in source:
        fail(errors, rel, "missing export cleanup sanitizer")


def validate_port(path: Path, source: str, port, errors: list[str]) -> None:
    rel = str(path.relative_to(ROOT))
    deck_only = deck_markup_only(source)
    slide_ids = find_slide_ids(source)
    if "data-template-source=" not in source or "data-ported-template=" not in source:
        fail(errors, rel, "missing ported-template source metadata")
    slot_count = source.count("data-edit-slot=")
    if slot_count <= 0:
        fail(errors, rel, "ported template has no editable slots")
    if ".filmstrip-thumb-host .slide" not in source:
        fail(errors, rel, "missing filmstrip thumbnail slide visibility override")
    uneditable_titles = find_uneditable_title_like_nodes(source)
    if uneditable_titles:
        sample = "; ".join(uneditable_titles[:4])
        fail(errors, rel, f"title-like authored text is not slot-editable: {sample}")
    if re.search(r'<button\b(?=[^>]*\bclass=["\'][^"\']*\bslide-object-resize\b)(?![^>]*\bdata-resize-handle\b)[^>]*>', deck_only, flags=re.I | re.S):
        fail(errors, rel, "contains bare .slide-object-resize markup; resize handles must be generated by runtime with data-resize-handle")
    if re.search(r"<script\b[^>]*\bsrc=", source, flags=re.I):
        fail(errors, rel, "contains external <script src>; ported decks must be single-file")
    if re.search(r"chart\.js|new\s+Chart\s*\(", source, flags=re.I):
        fail(errors, rel, "contains Chart.js dependency or runtime call")
    if "<canvas" in source.lower():
        fail(errors, rel, "contains canvas chart placeholder; use inline HTML/SVG replacement")
    if re.search(r"<link\b[^>]*(?:href=[\"']https?://|rel=[\"'][^\"']*\bstylesheet\b)", source, flags=re.I):
        fail(errors, rel, "contains external or non-inlined <link>; ported decks must be self-contained")
    if re.search(r"@import\s+(?:url\()?['\"]?https?://", source, flags=re.I):
        fail(errors, rel, "contains remote CSS @import")
    if re.search(r"url\(\s*['\"]?https?://", source, flags=re.I):
        fail(errors, rel, "contains remote CSS url() dependency")
    for index in port.preview_indices:
        if index < 0 or index >= len(slide_ids):
            fail(errors, rel, f"preview index slide-{index} out of bounds for {len(slide_ids)} slides")


def main() -> int:
    if not PRESETS_DIR.is_dir():
        print(f"Missing presets dir: {PRESETS_DIR}", file=sys.stderr)
        return 1

    ports = load_builder_ports()
    port_slugs = {port.out_slug for port in ports}
    ports_by_slug = {port.out_slug: port for port in ports}
    expected_total = LEGACY_PRESET_COUNT + len(port_slugs)
    files = sorted(PRESETS_DIR.glob("*.html"))
    errors: list[str] = []

    if len(files) != expected_total:
        errors.append(f"expected {expected_total} preset HTML files, found {len(files)}")

    missing_ports = sorted(slug for slug in port_slugs if not (PRESETS_DIR / f"{slug}.html").is_file())
    for slug in missing_ports:
        errors.append(f"missing ported preset examples/generated/presets/{slug}.html")

    for path in files:
        source = path.read_text(encoding="utf-8")
        validate_common(path, source, errors)
        if path.stem in port_slugs:
            validate_port(path, source, ports_by_slug[path.stem], errors)

    if errors:
        print("Preset validation failed:")
        for error in errors:
            print(f"- {error}")
        return 2

    print(f"Validated {len(files)} preset decks ({len(port_slugs)} ported, {LEGACY_PRESET_COUNT} legacy).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
