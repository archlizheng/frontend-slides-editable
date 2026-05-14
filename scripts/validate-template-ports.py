#!/usr/bin/env python3
"""Validate generated editable preset decks.

This is intentionally static and fast. It catches the regressions that have
historically broken editable decks before screenshot/browser checks run.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRESETS_DIR = ROOT / "examples" / "generated" / "presets"
LEGACY_PRESET_COUNT = 12


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
    slide_ids = find_slide_ids(source)
    if "data-template-source=" not in source or "data-ported-template=" not in source:
        fail(errors, rel, "missing ported-template source metadata")
    slot_count = source.count("data-edit-slot=")
    if slot_count <= 0:
        fail(errors, rel, "ported template has no editable slots")
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
