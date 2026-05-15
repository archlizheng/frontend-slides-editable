#!/usr/bin/env python3
"""Build slot-editable decks from beautiful-html-templates ports.

The ported decks keep the upstream template's slide classes, CSS, typography,
and decorative DOM. Editable behavior is added as a slot layer: authored
content can be edited in place while layout/decoration remains locked.
"""

from __future__ import annotations

import html
import json
import os
import re
import time
from urllib.parse import unquote, urlparse
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "examples" / "generated" / "presets"
DEFAULT_TEMPLATE_DIR = ROOT / "beautiful-html-templates"
REFERENCE = ROOT / "examples" / "editable-deck-reference.html"
_REFERENCE_EDITOR_PARTS: tuple[str, str, str] | None = None


@dataclass(frozen=True)
class TemplatePort:
    source_slug: str
    out_slug: str
    title: str
    preview_indices: tuple[int, int, int]


LEGACY_PORT_SLUGS = {
    "soft-editorial": "soft-editorial",
    "signal": "signal-gold",
    "studio": "studio-volt",
    "monochrome": "monochrome-ledger",
    "neo-grid-bold": "neo-grid-yellow",
    "vellum": "vellum-navy",
    "cobalt-grid": "cobalt-grid",
}

PORT_MANIFEST = [
    ("8-bit-orbit", "8-Bit Orbit", (0, 5, 9)),
    ("biennale-yellow", "Biennale Yellow", (0, 4, 7)),
    ("block-frame", "BlockFrame", (0, 5, 9)),
    ("blue-professional", "Blue Professional", (0, 5, 9)),
    ("bold-poster", "Bold Poster", (0, 5, 9)),
    ("broadside", "Broadside", (0, 8, 15)),
    ("capsule", "Capsule", (0, 5, 9)),
    ("cartesian", "Cartesian", (0, 5, 9)),
    ("cobalt-grid", "Cobalt Grid", (0, 2, 4)),
    ("coral", "Coral", (0, 5, 9)),
    ("creative-mode", "Creative Mode", (0, 4, 7)),
    ("daisy-days", "Daisy Days", (0, 5, 9)),
    ("editorial-forest", "Editorial Forest", (0, 4, 7)),
    ("editorial-tri-tone", "Editorial Tri-Tone", (0, 4, 7)),
    ("emerald-editorial", "Emerald Editorial", (0, 4, 7)),
    ("grove", "Grove", (0, 6, 11)),
    ("long-table", "Long Table", (0, 4, 7)),
    ("mat", "Mat", (0, 4, 8)),
    ("monochrome", "Monochrome", (0, 3, 11)),
    ("neo-grid-bold", "Neo-Grid Bold", (0, 2, 7)),
    ("peoples-platform", "People's Platform (Block & Bold)", (0, 5, 9)),
    ("pin-and-paper", "Pin & Paper", (0, 5, 10)),
    ("pink-script", "Pink Script - After Hours", (0, 4, 8)),
    ("playful", "Playful", (0, 5, 9)),
    ("raw-grid", "Raw Grid", (0, 5, 9)),
    ("retro-windows", "Retro Windows", (0, 5, 9)),
    ("retro-zine", "Retro Zine", (0, 5, 9)),
    ("sakura-chroma", "Sakura Chroma", (0, 4, 7)),
    ("scatterbrain", "Scatterbrain", (0, 5, 9)),
    ("signal", "Signal", (0, 7, 17)),
    ("soft-editorial", "Soft Editorial", (0, 3, 9)),
    ("stencil-tablet", "Stencil & Tablet", (0, 5, 10)),
    ("studio", "Studio", (0, 3, 7)),
    ("vellum", "Vellum", (0, 3, 7)),
]


SLOT_TAGS = r"(h1|h2|h3|h4|p|li|td|th|figcaption|blockquote|cite|small|span|div)"
BLOCK_TAG_RE = re.compile(r"</?(section|article|main|div|ul|ol|table|tbody|thead|tr|svg|canvas|deck-stage)\b", re.I)
TEXT_RE = re.compile(r"[A-Za-z0-9\u4e00-\u9fff\[\]]")
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


def load_ports() -> list[TemplatePort]:
    ports: list[TemplatePort] = []
    for source_slug, title, preview_indices in PORT_MANIFEST:
        out_slug = LEGACY_PORT_SLUGS.get(source_slug, source_slug)
        ports.append(TemplatePort(source_slug, out_slug, title, preview_indices))
    return ports


PORTS = load_ports()


def normalize_generated_html(source: str) -> str:
    return "\n".join(line.rstrip() for line in source.splitlines()) + "\n"


def template_root() -> Path:
    configured = os.environ.get("BEAUTIFUL_TEMPLATES_DIR")
    root = Path(configured).expanduser() if configured else DEFAULT_TEMPLATE_DIR
    if not root.is_absolute():
        root = (ROOT / root).resolve()
    if not (root / "templates").is_dir():
        raise SystemExit(
            f"Missing beautiful-html-templates checkout at {root}. "
            "Set BEAUTIFUL_TEMPLATES_DIR=./beautiful-html-templates."
        )
    return root


def attr_value(tag: str, name: str) -> str | None:
    match = re.search(rf"\b{name}\s*=\s*([\"'])(.*?)\1", tag, flags=re.I | re.S)
    return html.unescape(match.group(2)) if match else None


def inline_local_stylesheets(head: str, source_dir: Path) -> str:
    def repl(match: re.Match[str]) -> str:
        tag = match.group(0)
        href = attr_value(tag, "href")
        rel = (attr_value(tag, "rel") or "").lower()
        if not href:
            return ""
        parsed = urlparse(href)
        if parsed.scheme in {"http", "https", "data"} or parsed.netloc:
            return ""
        if "stylesheet" not in rel and not href.lower().endswith(".css"):
            return ""
        css_path = (source_dir / unquote(parsed.path)).resolve()
        try:
            css_path.relative_to(source_dir.resolve())
        except ValueError:
            return ""
        if not css_path.is_file():
            return ""
        css = css_path.read_text(encoding="utf-8")
        css = re.sub(r"@import\s+(?:url\()?['\"]?https?://[^;]+;", "", css, flags=re.I)
        return f"\n<style data-inlined-from=\"{html.escape(href, quote=True)}\">\n{css}\n</style>\n"

    return re.sub(r"<link\b[^>]*>", repl, head, flags=re.I | re.S)


def remove_external_deck_runtime(head: str, source_dir: Path) -> str:
    head = re.sub(r'\n?\s*<script\b[^>]*\bsrc=["\'][^"\']+["\'][^>]*>\s*</script>', "", head, flags=re.I)
    head = re.sub(r"\n?\s*<title\b[^>]*>.*?</title>", "", head, flags=re.S | re.I)
    head = inline_local_stylesheets(head, source_dir)
    head = re.sub(r"@import\s+(?:url\()?['\"]?https?://[^;]+;", "", head, flags=re.I)
    head = re.sub(r"\bdeck-stage\b", "#deck.slides-offset", head, flags=re.I)
    return head


def has_class(open_tag: str, class_name: str) -> bool:
    match = re.search(r'class=["\']([^"\']*)["\']', open_tag, flags=re.I)
    return bool(match and class_name in match.group(1).split())


def add_class(open_tag: str, class_name: str) -> str:
    match = re.search(r'class=(["\'])([^"\']*)\1', open_tag, flags=re.I)
    if not match:
        return open_tag[:-1] + f' class="{class_name}">'
    classes = match.group(2).split()
    if class_name not in classes:
        classes.append(class_name)
    quote = match.group(1)
    return open_tag[: match.start()] + f"class={quote}{' '.join(classes)}{quote}" + open_tag[match.end() :]


def extract_elements(source: str, tag: str, class_name: str | None = None) -> list[str]:
    token_re = re.compile(rf"<(/?){tag}\b[^>]*>", flags=re.I)
    elements: list[str] = []
    pos = 0
    while True:
        start = None
        for match in token_re.finditer(source, pos):
            if match.group(1):
                continue
            if class_name and not has_class(match.group(0), class_name):
                continue
            start = match
            break
        if not start:
            break
        depth = 1
        for match in token_re.finditer(source, start.end()):
            if match.group(1):
                depth -= 1
            else:
                depth += 1
            if depth == 0:
                elements.append(source[start.start() : match.end()])
                pos = match.end()
                break
        else:
            raise ValueError(f"unclosed <{tag}> starting near byte {start.start()}")
    return elements


def div_slide_to_section(fragment: str) -> str:
    end = fragment.find(">")
    open_tag = "<section" + fragment[4 : end + 1]
    open_tag = add_class(open_tag, "slide")
    body = fragment[end + 1 :]
    close = body.rfind("</div>")
    if close < 0:
        raise ValueError("div.slide fragment missing closing </div>")
    return open_tag + body[:close] + "</section>" + body[close + len("</div>") :]


def extract_deck_stage_inner(source: str) -> str | None:
    match = re.search(r"<deck-stage\b[^>]*>(.*?)</deck-stage>", source, flags=re.S | re.I)
    return match.group(1) if match else None


def extract_head_and_sections(source: str, source_dir: Path) -> tuple[str, list[str]]:
    head_match = re.search(r"<head\b[^>]*>(.*?)</head>", source, flags=re.S | re.I)
    if not head_match:
        raise ValueError("template missing <head>")
    head = remove_external_deck_runtime(head_match.group(1), source_dir)

    sections = extract_elements(source, "section", "slide")
    if not sections:
        deck_stage = extract_deck_stage_inner(source)
        if deck_stage:
            sections = extract_elements(deck_stage, "section")
    if not sections:
        sections = [div_slide_to_section(fragment) for fragment in extract_elements(source, "div", "slide")]
    if not sections:
        raise ValueError("template has no slide sections")
    return head, sections


def set_attr(open_tag: str, name: str, value: str | None = None) -> str:
    open_tag = re.sub(rf"\s{name}(=(\"[^\"]*\"|'[^']*'|[^\s>]+))?", "", open_tag, flags=re.I)
    insert = f" {name}" if value is None else f' {name}="{html.escape(value, quote=True)}"'
    return open_tag[:-1] + insert + ">"


def ensure_slide_contract(section: str, index: int) -> str:
    end = section.find(">")
    open_tag = section[: end + 1]
    open_tag = add_class(open_tag, "slide")
    open_tag = set_attr(open_tag, "id", f"slide-{index}")
    open_tag = set_attr(open_tag, "data-template-slide-index", str(index + 1))
    section = open_tag + section[end + 1 :]
    return section.replace("</section>", '\n    <div class="slide-edit-layer" aria-hidden="true"></div>\n  </section>', 1)


def static_chart_markup(canvas_id: str, slide_index: int, chart_index: int) -> str:
    label_base = f"s{slide_index}-chart-{chart_index}"
    return f"""
<div class="static-chart-replacement" role="img" aria-label="Static chart replacement for {html.escape(canvas_id)}">
  <div class="static-chart-bars">
    <span class="static-chart-bar" style="--v:72%"><b data-edit-slot="{label_base}-a" data-slot-type="metric" data-slot-label="Chart value A" data-slot-locked-layout="true">72</b></span>
    <span class="static-chart-bar" style="--v:48%"><b data-edit-slot="{label_base}-b" data-slot-type="metric" data-slot-label="Chart value B" data-slot-locked-layout="true">48</b></span>
    <span class="static-chart-bar" style="--v:86%"><b data-edit-slot="{label_base}-c" data-slot-type="metric" data-slot-label="Chart value C" data-slot-locked-layout="true">86</b></span>
    <span class="static-chart-bar" style="--v:63%"><b data-edit-slot="{label_base}-d" data-slot-type="metric" data-slot-label="Chart value D" data-slot-locked-layout="true">63</b></span>
  </div>
  <div class="static-chart-caption" data-edit-slot="{label_base}-caption" data-slot-type="text" data-slot-label="Chart caption" data-slot-locked-layout="true">Editable chart summary</div>
</div>
""".strip()


def replace_canvas_charts(section: str, slide_index: int) -> str:
    count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal count
        tag = match.group(0)
        id_match = re.search(r'id=["\']([^"\']+)["\']', tag, flags=re.I)
        canvas_id = id_match.group(1) if id_match else f"chart-{count + 1}"
        count += 1
        return static_chart_markup(canvas_id, slide_index, count)

    return re.sub(r"<canvas\b[^>]*>\s*</canvas>", repl, section, flags=re.S | re.I)


def slot_type_for(tag: str, attrs: str) -> str:
    cls_match = re.search(r'class=["\']([^"\']+)["\']', attrs, flags=re.I)
    classes = cls_match.group(1).lower() if cls_match else ""
    if tag in {"td", "th"}:
        return "table-cell"
    if any(k in classes for k in ("stat", "num", "value", "metric", "bar-val", "vbig", "amount", "percent")):
        return "metric"
    return "text"


def class_tokens_from_attrs(attrs: str) -> set[str]:
    cls_match = re.search(r'class=["\']([^"\']+)["\']', attrs, flags=re.I)
    return set(cls_match.group(1).split()) if cls_match else set()


def is_title_like_slot_candidate(tag: str, attrs: str) -> bool:
    tag = tag.lower()
    if tag in {"h1", "h2", "h3", "h4"}:
        return True
    return bool(class_tokens_from_attrs(attrs) & TITLE_LIKE_CLASSES)


def slot_label_from_inner(inner: str, fallback: str) -> str:
    text = re.sub(r"<br\s*/?>", " ", inner, flags=re.I)
    label = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", text)).strip()[:48]
    return label or fallback


def should_mark_text_node(tag: str, attrs: str, inner: str) -> bool:
    classes = " ".join(class_tokens_from_attrs(attrs)).lower()
    if "data-edit-slot" in attrs or "aria-hidden" in attrs:
        return False
    if "data-edit-slot" in inner:
        return False
    if any(k in classes for k in ("xaxis", "yaxis", "axis", "ticks", "gridline")):
        return False
    if not TEXT_RE.search(re.sub(r"<[^>]+>", "", inner)):
        return False
    return not BLOCK_TAG_RE.search(inner)


def mark_priority_text_slots(section: str, slide_index: int) -> str:
    """Mark title-like inline nodes before generic slotting sees outer layout divs."""
    slot_count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal slot_count
        full = match.group(0)
        tag = match.group(1).lower()
        attrs = match.group(2) or ""
        inner = match.group(3)
        if not is_title_like_slot_candidate(tag, attrs):
            return full
        if not should_mark_text_node(tag, attrs, inner):
            return full
        slot_count += 1
        slot_id = f"s{slide_index}-title-{slot_count}"
        label = slot_label_from_inner(inner, slot_id)
        return (
            f'<{tag}{attrs} data-edit-slot="{slot_id}" '
            f'data-slot-type="{slot_type_for(tag, attrs)}" '
            f'data-slot-label="{html.escape(label, quote=True)}" '
            'data-slot-locked-layout="true">'
            f"{inner}</{tag}>"
        )

    heading_pattern = re.compile(r"<(h1|h2|h3|h4)\b([^>]*)>(.*?)</\1>", flags=re.S | re.I)
    out = heading_pattern.sub(repl, section)
    class_tokens = "|".join(re.escape(token) for token in sorted(TITLE_LIKE_CLASSES, key=len, reverse=True))
    class_lookahead = (
        rf'(?=[^>]*\bclass=["\']'
        rf'(?:(?:{class_tokens})(?=\s|["\'])|[^"\']*\s(?:{class_tokens})(?=\s|["\'])))'
    )
    class_pattern = re.compile(rf"<(p|div|span)\b{class_lookahead}([^>]*)>(.*?)</\1>", flags=re.S | re.I)
    return class_pattern.sub(repl, out)


def mark_text_slots(section: str, slide_index: int) -> str:
    slot_count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal slot_count
        full = match.group(0)
        tag = match.group(1).lower()
        attrs = match.group(2) or ""
        inner = match.group(3)
        if not should_mark_text_node(tag, attrs, inner):
            return full
        slot_count += 1
        slot_id = f"s{slide_index}-slot-{slot_count}"
        slot_type = slot_type_for(tag, attrs)
        label = slot_label_from_inner(inner, slot_id)
        return (
            f'<{tag}{attrs} data-edit-slot="{slot_id}" '
            f'data-slot-type="{slot_type}" '
            f'data-slot-label="{html.escape(label, quote=True)}" '
            'data-slot-locked-layout="true">'
            f"{inner}</{tag}>"
        )

    pattern = re.compile(rf"<{SLOT_TAGS}\b([^>]*)>(.*?)</\1>", flags=re.S | re.I)
    prev = None
    out = section
    for _ in range(3):
        if out == prev:
            break
        prev = out
        out = pattern.sub(repl, out)
    return out


def mark_image_slots(section: str, slide_index: int) -> str:
    count = 0

    def img_repl(match: re.Match[str]) -> str:
        nonlocal count
        tag = match.group(0)
        if "data-edit-slot" in tag or "aria-hidden" in tag:
            return tag
        count += 1
        return tag[:-1] + (
            f' data-edit-slot="s{slide_index}-image-{count}" '
            'data-slot-type="image" data-slot-label="Image" '
            'data-slot-locked-layout="true">'
        )

    section = re.sub(r"<img\b[^>]*>", img_repl, section, flags=re.I)

    def placeholder_repl(match: re.Match[str]) -> str:
        tag = match.group(0)
        if "data-edit-slot" in tag or "aria-hidden" in tag:
            return tag
        cls = re.search(r'class=["\']([^"\']+)["\']', tag, flags=re.I)
        if not cls:
            return tag
        classes = cls.group(1).lower()
        class_tokens = set(classes.split())
        if not (
            "img-placeholder" in class_tokens
            or "image-placeholder" in class_tokens
            or "ph" in class_tokens
        ):
            return tag
        nonlocal count
        count += 1
        return tag[:-1] + (
            f' data-edit-slot="s{slide_index}-image-{count}" '
            'data-slot-type="image" data-slot-label="Image" '
            'data-slot-locked-layout="true">'
        )

    return re.sub(r"<div\b[^>]*>", placeholder_repl, section, flags=re.I)


def prepare_sections(sections: list[str]) -> str:
    rendered = []
    for i, section in enumerate(sections):
        section = ensure_slide_contract(section, i)
        section = replace_canvas_charts(section, i)
        section = mark_image_slots(section, i)
        section = mark_priority_text_slots(section, i)
        section = mark_text_slots(section, i)
        rendered.append(section)
    return "\n\n".join(rendered)


PORT_BASE_CSS = """
<style id="ported-template-runtime-css">
  :root {
    --body-size: clamp(0.75rem, 1.5vw, 1.125rem);
    --font-body: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    --font-display: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    --slide-bg-deep: #0f172a;
    --deck-chrome-bg: rgba(15, 23, 42, 0.94);
    --deck-chrome-border: rgba(255, 255, 255, 0.14);
    --deck-chrome-text: #e2e8f0;
    --deck-chrome-muted: #94a3b8;
    --deck-chrome-accent: #2563eb;
    --deck-chrome-shadow: 0 12px 40px rgba(0, 0, 0, 0.35);
    --deck-chrome-surface: rgba(30, 41, 59, 0.92);
  }
  html {
    scroll-snap-type: y mandatory;
    scroll-behavior: smooth;
  }
  html, body {
    min-height: 100%;
    overflow-x: hidden !important;
  }
  body.ported-template-deck {
    margin: 0;
  }
  #deck.slides-offset {
    display: block !important;
    position: relative !important;
    height: auto !important;
    width: 100vw !important;
    transform: none !important;
    transition: padding-right 0.28s ease !important;
    overflow: visible !important;
  }
  #deck.slides-offset > section.slide {
    width: 100vw !important;
    height: 100vh !important;
    height: 100dvh !important;
    position: relative !important;
    inset: auto !important;
    opacity: 1 !important;
    visibility: visible !important;
    pointer-events: auto !important;
    scroll-snap-align: start;
    box-sizing: border-box;
    overflow: hidden !important;
  }
  body.deck-edit-mode [data-edit-slot] {
    cursor: text;
    outline: 2px dashed color-mix(in srgb, var(--deck-chrome-accent) 72%, transparent);
    outline-offset: 3px;
    box-shadow: 0 0 0 5px color-mix(in srgb, var(--deck-chrome-accent) 10%, transparent);
  }
  body.deck-edit-mode [data-slot-type="image"] {
    cursor: pointer;
  }
  [data-edit-slot][contenteditable="true"] {
    outline: 2px solid var(--deck-chrome-accent) !important;
    outline-offset: 3px;
    box-shadow: 0 0 0 6px color-mix(in srgb, var(--deck-chrome-accent) 16%, transparent) !important;
  }
  .filmstrip-thumb-host .slide {
    opacity: 1 !important;
    visibility: visible !important;
    pointer-events: none !important;
    position: relative !important;
    inset: auto !important;
  }
  .filmstrip-thumb-host .slide-edit-layer {
    pointer-events: none !important;
  }
  .static-chart-replacement {
    width: 100%;
    min-height: min(42vh, 360px);
    display: grid;
    grid-template-rows: 1fr auto;
    gap: clamp(0.5rem, 1.5vw, 1rem);
  }
  .static-chart-bars {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    align-items: end;
    gap: clamp(0.45rem, 1.2vw, 1rem);
    min-height: min(34vh, 300px);
    border-left: 1px solid currentColor;
    border-bottom: 1px solid currentColor;
    padding: clamp(0.5rem, 1.4vw, 1rem);
  }
  .static-chart-bar {
    min-height: 18%;
    height: var(--v);
    display: flex;
    align-items: start;
    justify-content: center;
    background: currentColor;
    opacity: 0.72;
  }
  .static-chart-bar b {
    display: block;
    transform: translateY(calc(-100% - 0.25rem));
    color: inherit;
    background: inherit;
    font: inherit;
  }
  .static-chart-caption {
    font-size: clamp(0.72rem, 1vw, 0.95rem);
    opacity: 0.72;
  }
  @media print {
    .deck-left-hover-anchor, .deck-add-element-menu, .slide-sidebar, .rte-toolbar, .progress-bar, .nav-dots {
      display: none !important;
    }
    #deck.slides-offset > section.slide {
      break-after: page;
    }
  }
</style>
"""


SLOT_ADAPTER_JS = r"""
  /* ---------- Slot editor: locked native template layout, editable content ---------- */
  class SlotEditor {
    constructor(history, richEditor, onChange) {
      this.history = history;
      this.richEditor = richEditor;
      this.onChange = typeof onChange === 'function' ? onChange : function () {};
      this.imageInput = document.getElementById('slotImageInput');
      this.imageTargetId = null;
    }
    bind() {
      document.addEventListener('click', (e) => this._onClick(e), true);
      document.addEventListener('focusout', (e) => this._onFocusOut(e), true);
      if (this.imageInput) {
        this.imageInput.addEventListener('change', () => this._onImagePicked());
      }
    }
    _slotSelector(id) {
      if (window.CSS && CSS.escape) return '[data-edit-slot="' + CSS.escape(id) + '"]';
      return '[data-edit-slot="' + String(id).replace(/"/g, '\\"') + '"]';
    }
    _slotById(id) {
      const deckRoot = document.getElementById('deck');
      return (deckRoot && deckRoot.querySelector(this._slotSelector(id))) || document.querySelector(this._slotSelector(id));
    }
    _onClick(e) {
      if (!document.body.classList.contains('deck-edit-mode')) return;
      if (isDeckChromeNode(e.target)) return;
      const slot = e.target.closest && e.target.closest('[data-edit-slot]');
      if (!slot) return;
      if (slot.closest('[data-slide-object]')) return;

      if (slot.dataset.slotType === 'image') {
        if (!this.imageInput) return;
        e.preventDefault();
        e.stopPropagation();
        this.imageTargetId = slot.dataset.editSlot;
        this.imageInput.value = '';
        this.imageInput.click();
        return;
      }

      if (slot.isContentEditable) return;
      e.preventDefault();
      e.stopPropagation();
      if (slot.dataset._deckHtmlBefore === undefined) slot.dataset._deckHtmlBefore = slot.innerHTML;
      slot.contentEditable = 'true';
      slot.focus();
      if (this.richEditor && this.richEditor._updateRteToolbar) this.richEditor._updateRteToolbar();
    }
    _onFocusOut(e) {
      const slot = e.target.closest && e.target.closest('[data-edit-slot]');
      if (!slot || !slot.isContentEditable) return;
      setTimeout(() => {
        const ae = document.activeElement;
        const toolbar = document.getElementById('rteToolbar');
        if (ae && (ae === slot || slot.contains(ae) || (toolbar && toolbar.contains(ae)))) return;
        slot.contentEditable = 'false';
        const before = slot.dataset._deckHtmlBefore;
        const after = slot.innerHTML;
        delete slot.dataset._deckHtmlBefore;
        if (before !== undefined && before !== after) {
          const id = slot.dataset.editSlot;
          this.history.push({
            undo: () => {
              const fresh = this._slotById(id);
              if (fresh) fresh.innerHTML = before;
            },
            redo: () => {
              const fresh = this._slotById(id);
              if (fresh) fresh.innerHTML = after;
            }
          });
          this.onChange();
        }
        if (this.richEditor) {
          this.richEditor._closeRteDrawers && this.richEditor._closeRteDrawers();
          if (this.richEditor.toolbar) this.richEditor.toolbar.classList.remove('visible');
        }
      }, 0);
    }
    _onImagePicked() {
      const file = this.imageInput && this.imageInput.files && this.imageInput.files[0];
      const id = this.imageTargetId;
      this.imageTargetId = null;
      if (!file || !id) return;
      const slot = this._slotById(id);
      if (!slot) return;
      const before = slot.outerHTML;
      const reader = new FileReader();
      reader.onload = () => {
        const fresh = this._slotById(id);
        if (!fresh) return;
        const dataUrl = reader.result;
        if (fresh.tagName === 'IMG') fresh.src = dataUrl;
        else {
          fresh.style.backgroundImage = 'url("' + dataUrl + '")';
          fresh.style.backgroundSize = 'cover';
          fresh.style.backgroundPosition = 'center';
          if (!fresh.querySelector('*')) fresh.textContent = '';
        }
        const after = fresh.outerHTML;
        if (before === after) return;
        this.history.push({
          undo: () => {
            const current = this._slotById(id);
            if (current) current.outerHTML = before;
          },
          redo: () => {
            const current = this._slotById(id);
            if (current) current.outerHTML = after;
          }
        });
        this.onChange();
      };
      reader.readAsDataURL(file);
    }
  }
"""


def extract_reference_editor_parts() -> tuple[str, str, str]:
    global _REFERENCE_EDITOR_PARTS
    if _REFERENCE_EDITOR_PARTS is not None:
        return _REFERENCE_EDITOR_PARTS
    reference = REFERENCE.read_text(encoding="utf-8")
    style_match = re.search(r"<style>(.*?)</style>", reference, flags=re.S)
    if not style_match:
        raise SystemExit("Reference runtime missing <style>")
    style = style_match.group(1)
    css_start = style.index("    /* === deck chrome")
    editor_css = style[css_start:]

    chrome_start = reference.index('<div class="deck-left-hover-anchor"')
    chrome_end = reference.index('<div class="slides-offset">', chrome_start)
    chrome = reference[chrome_start:chrome_end]
    chrome = chrome.rstrip() + '\n<input type="file" id="slotImageInput" accept="image/*" hidden data-deck-chrome-surface="">\n'

    script_start = reference.index("<script>\n(function () {", chrome_end)
    script_end = reference.index("</script>", script_start) + len("</script>")
    js = reference[script_start:script_end]
    _REFERENCE_EDITOR_PARTS = (
        f"<style id=\"swiss-edit-runtime-css\">\n{editor_css}\n</style>",
        chrome,
        patch_reference_runtime_js(js),
    )
    return _REFERENCE_EDITOR_PARTS


def patch_reference_runtime_js(js: str) -> str:
    slot_selector = '.slide-object-text[contenteditable="true"], [data-edit-slot][contenteditable="true"]'
    js = js.replace(".slide-object-text[contenteditable=\"true\"]", slot_selector)
    js = js.replace(
        "node.closest('.deck-edit-chrome') || node.closest('[data-deck-chrome-surface]'))",
        "node.closest('.deck-edit-chrome') || node.closest('#slotImageInput') || node.closest('[data-deck-chrome-surface]'))",
    )
    js = js.replace(
        "if (best !== this.current) {\n        this.current = best;\n        this.onSlideChange && this.onSlideChange(best);\n      }\n      this._updateChrome();",
        "if (best !== this.current) {\n        this.current = best;\n        this.onSlideChange && this.onSlideChange(best);\n      }\n      this.slides.forEach((s, i) => s.classList.toggle('is-active', i === best));\n      this._updateChrome();",
    )
    js = js.replace(
        "if (el && el.classList && el.classList.contains('slide-object-text') && el.getAttribute('contenteditable') === 'true') {",
        "if (el && el.getAttribute && (el.classList.contains('slide-object-text') || el.hasAttribute('data-edit-slot')) && el.getAttribute('contenteditable') === 'true') {",
    )
    js = js.replace(
        "const history = new HistoryStack(updateUndoRedoChrome);\n  const deck = new SlideDeck();\n  const editor = new SlideObjectEditor(deck, history);\n  const sidebar = new SlideSidebar(deck, history);",
        "const history = new HistoryStack(updateUndoRedoChrome);\n  const deck = new SlideDeck();\n  const editor = new SlideObjectEditor(deck, history);\n  const sidebar = new SlideSidebar(deck, history);\n  " + SLOT_ADAPTER_JS.strip() + "\n  const slotEditor = new SlotEditor(history, editor, updateUndoRedoChrome);",
    )
    js = js.replace(
        "ensureObjectControls(document);\n  editor.bind();\n  updateUndoRedoChrome();",
        "ensureObjectControls(document);\n  editor.bind();\n  slotEditor.bind();\n  updateUndoRedoChrome();",
    )
    js = js.replace(
        "root.querySelectorAll('.snap-line-v, .snap-line-h').forEach((el) => el.remove());",
        "root.querySelectorAll('[data-edit-slot][contenteditable=\"true\"]').forEach((el) => {\n      el.setAttribute('contenteditable', 'false');\n      delete el.dataset._deckHtmlBefore;\n      el.removeAttribute('data-_deck-html-before');\n    });\n    root.querySelectorAll('.snap-line-v, .snap-line-h').forEach((el) => el.remove());",
    )
    js = js.replace(
        "sanitizeEditableState(docEl);\n    const filmstrip = docEl.querySelector('#filmstripList');",
        "sanitizeEditableState(docEl);\n    docEl.querySelectorAll('.deck-left-hover-anchor, #deckAddElementMenu, #progressBar, #navDots, #slideSidebar, #rteToolbar, #slotImageInput, script').forEach((el) => el.remove());\n    const filmstrip = docEl.querySelector('#filmstripList');",
    )
    return js.replace("<script>", '<script id="swiss-slot-edit-runtime-js">', 1)


def render(port: TemplatePort, head: str, sections_html: str) -> str:
    runtime_css, runtime_chrome, runtime_js = extract_reference_editor_parts()
    return f"""<!doctype html>
<html lang="zh-Hans" data-deck-id="ported-{port.out_slug}" data-template-source="{port.source_slug}" data-mobile-adaptation="desktop-default">
<head>
{head}
<title>{html.escape(port.title)} · Slot Editable Template Port</title>
{PORT_BASE_CSS}
{runtime_css}
</head>
<body class="ported-template-deck">
{runtime_chrome}
<div id="deck" class="slides-offset stage" data-ported-template="{port.source_slug}">
{sections_html}
</div>
{runtime_js}
</body>
</html>
"""


def main() -> int:
    started = time.perf_counter()
    source_root = template_root()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for port in PORTS:
        template_path = source_root / "templates" / port.source_slug / "template.html"
        if not template_path.is_file():
            raise SystemExit(f"Missing template: {template_path}")
        source = template_path.read_text(encoding="utf-8")
        head, sections = extract_head_and_sections(source, template_path.parent)
        sections_html = prepare_sections(sections)
        out = normalize_generated_html(render(port, head, sections_html))
        out_path = OUT_DIR / f"{port.out_slug}.html"
        out_path.write_text(out, encoding="utf-8")
        slot_count = sections_html.count("data-edit-slot=")
        print(f"{out_path.relative_to(ROOT)} slides={len(sections)} slots={slot_count} source={port.source_slug}")
    elapsed = time.perf_counter() - started
    print(f"Built {len(PORTS)} template-port decks in {OUT_DIR} in {elapsed:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
