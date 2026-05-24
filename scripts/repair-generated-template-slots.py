#!/usr/bin/env python3
"""Repair editable slots in already-generated beautiful template ports.

This is a deterministic bridge for environments that do not have the upstream
beautiful-html-templates checkout available. It reuses the port builder's slot
marking rules and only touches generated decks that declare data-ported-template.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRESETS_DIR = ROOT / "examples" / "generated" / "presets"


def load_builder():
    builder_path = ROOT / "scripts" / "build-template-port-decks.py"
    spec = importlib.util.spec_from_file_location("build_template_port_decks", builder_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Unable to load {builder_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def deck_bounds(source: str) -> tuple[int, int] | None:
    start_match = re.search(r'<div\b[^>]*\bid=["\']deck["\'][^>]*>', source, flags=re.I)
    if not start_match:
        return None
    script_pos = source.find("<script", start_match.end())
    if script_pos < 0:
        script_pos = len(source)
    return start_match.start(), script_pos


def iter_section_spans(source: str) -> list[tuple[int, int]]:
    token_re = re.compile(r"</?section\b[^>]*>", flags=re.I)
    spans: list[tuple[int, int]] = []
    pos = 0
    while True:
        start = None
        for match in token_re.finditer(source, pos):
            if not match.group(0).startswith("</"):
                start = match
                break
        if not start:
            break
        depth = 1
        for match in token_re.finditer(source, start.end()):
            if match.group(0).startswith("</"):
                depth -= 1
            else:
                depth += 1
            if depth == 0:
                spans.append((start.start(), match.end()))
                pos = match.end()
                break
        else:
            break
    return spans


def repair_source(source: str, builder) -> str:
    source = re.sub(
        r'(<html\b(?=[^>]*\bdata-template-source=)(?![^>]*\bdata-template-edit-mode=)[^>]*)>',
        r'\1 data-template-edit-mode="slots">',
        source,
        count=1,
        flags=re.I,
    )
    if "btnUnlockLayout" not in source:
        source = source.replace(
            '<button type="button" class="deck-btn-add" id="btnAddElement" title="Add text, image, or video to current slide">Add element</button>',
            '<button type="button" class="deck-btn-add" id="btnAddElement" title="Add text, image, or video to current slide">Add element</button>\n'
            '    <button type="button" class="deck-btn-add" id="btnUnlockLayout" title="Convert this slide&#x27;s editable content into movable components">Unlock layout</button>',
            1,
        )
    if "node.closest('#btnUnlockLayout')" not in source:
        source = source.replace(
            "node.closest('#deckAddElementMenu') || node.closest('#btnAddElement') ||",
            "node.closest('#deckAddElementMenu') || node.closest('#btnAddElement') || node.closest('#btnUnlockLayout') ||",
            1,
        )
    source = source.replace(
        "['#editToggle', '#pagesToggle', '#btnSave', '#btnAddElement', '#deckEditChrome', '#rteToolbar']",
        "['#editToggle', '#pagesToggle', '#btnSave', '#btnAddElement', '#btnUnlockLayout', '#deckEditChrome', '#rteToolbar']",
        1,
    )
    if "const btnUnlockLayout" not in source:
        source = source.replace(
            "const btnAddElement = document.getElementById('btnAddElement');\n  const deckAddElementMenu = document.getElementById('deckAddElementMenu');",
            "const btnAddElement = document.getElementById('btnAddElement');\n  const btnUnlockLayout = document.getElementById('btnUnlockLayout');\n  const deckAddElementMenu = document.getElementById('deckAddElementMenu');",
            1,
        )
    if "btnUnlockLayout && btnUnlockLayout.contains" not in source:
        source = source.replace(
            "if (btnAddElement && btnAddElement.contains(e.target)) return;",
            "if (btnAddElement && btnAddElement.contains(e.target)) return;\n    if (btnUnlockLayout && btnUnlockLayout.contains(e.target)) return;",
            1,
        )
    unlock_fn = r"""
  function componentizeCurrentSlide() {
    const slide = deck.slides[deck.current] || document.querySelector('.slides-offset > section.slide');
    if (!slide || slide.dataset.componentized === 'true') return;
    if (!window.confirm('Unlock this slide layout? This creates movable copies of editable content while keeping the original template layout intact.')) return;
    const layer = slide.querySelector('.slide-edit-layer');
    if (!layer) return;
    const inserted = [];
    const slots = Array.from(slide.querySelectorAll('[data-edit-slot]')).filter((slot) => !slot.closest('[data-slide-object]'));
    slots.slice(0, 12).forEach((slot, index) => {
      const obj = document.createElement('div');
      obj.className = 'slide-object template-component-object';
      obj.setAttribute('data-slide-object', '');
      obj.setAttribute('data-object-type', slot.dataset.slotType === 'image' ? 'image' : 'text');
      obj.setAttribute('data-component-source-slot', slot.dataset.editSlot || '');
      obj.style.cssText = 'left:' + (8 + (index % 3) * 28) + '%;top:' + (12 + Math.floor(index / 3) * 16) + '%;width:24%;min-height:3rem;';
      const move = document.createElement('button');
      move.type = 'button';
      move.className = 'slide-object-move';
      move.setAttribute('aria-label', 'Move object');
      move.textContent = '\u283f';
      const del = document.createElement('button');
      del.type = 'button';
      del.className = 'slide-object-delete';
      del.setAttribute('aria-label', 'Delete object');
      del.textContent = '\u00d7';
      const body = document.createElement('div');
      if (slot.dataset.slotType === 'image') {
        body.className = 'slide-object-graphic';
        body.innerHTML = slot.tagName === 'IMG' ? slot.outerHTML : slot.innerHTML;
      } else {
        body.className = 'slide-object-text';
        body.setAttribute('contenteditable', 'false');
        body.innerHTML = slot.innerHTML;
      }
      obj.appendChild(move);
      obj.appendChild(del);
      obj.appendChild(body);
      layer.appendChild(obj);
      inserted.push(obj);
    });
    slide.dataset.componentized = 'true';
    ensureObjectControls(slide);
    renumberDeckObjects(slide);
    history.push({
      undo: () => {
        inserted.forEach((obj) => {
          if (obj && obj.parentNode) obj.parentNode.removeChild(obj);
        });
        delete slide.dataset.componentized;
        deck.refreshSlides();
        editor.clearSelection();
        ensureObjectControls(document);
      },
      redo: () => {
        inserted.forEach((obj) => {
          if (obj && !obj.parentNode) layer.appendChild(obj);
        });
        slide.dataset.componentized = 'true';
        deck.refreshSlides();
        ensureObjectControls(document);
      }
    });
    updateUndoRedoChrome();
  }

  if (btnUnlockLayout) {
    btnUnlockLayout.addEventListener('click', componentizeCurrentSlide);
  }

"""
    if "function componentizeCurrentSlide()" not in source:
        source = source.replace("\n  document.addEventListener('focusout', (e) => {", unlock_fn + "\n  document.addEventListener('focusout', (e) => {", 1)
    source = source.replace(
        "if (btnAddElement) btnAddElement.classList.remove('show');\n    updateUndoRedoChrome();",
        "if (btnAddElement) btnAddElement.classList.remove('show');\n    if (btnUnlockLayout) btnUnlockLayout.classList.remove('show');\n    updateUndoRedoChrome();",
        1,
    )
    source = source.replace(
        "if (btnAddElement) btnAddElement.classList.add('show');\n      if (deckEditChromeEl)",
        "if (btnAddElement) btnAddElement.classList.add('show');\n      if (btnUnlockLayout) btnUnlockLayout.classList.add('show');\n      if (deckEditChromeEl)",
        1,
    )
    source = source.replace(
        "if (btnAddElement) btnAddElement.classList.remove('show');\n      if (deckEditChromeEl)",
        "if (btnAddElement) btnAddElement.classList.remove('show');\n      if (btnUnlockLayout) btnUnlockLayout.classList.remove('show');\n      if (deckEditChromeEl)",
        1,
    )
    source = source.replace(
        "btnSave.addEventListener('mouseleave', scheduleHide);\n  }",
        "btnSave.addEventListener('mouseleave', scheduleHide);\n  }\n  if (btnUnlockLayout) {\n    btnUnlockLayout.addEventListener('mouseenter', () => clearTimeout(hideT));\n    btnUnlockLayout.addEventListener('mouseleave', scheduleHide);\n  }",
        1,
    )
    bounds = deck_bounds(source)
    if not bounds:
        return source
    deck_start, deck_end = bounds
    deck = source[deck_start:deck_end]
    parts: list[str] = []
    cursor = 0
    for slide_index, (start, end) in enumerate(iter_section_spans(deck)):
        parts.append(deck[cursor:start])
        section = deck[start:end]
        section = builder.mark_image_slots(section, slide_index)
        section = builder.mark_priority_text_slots(section, slide_index)
        section = builder.mark_priority_body_slots(section, slide_index)
        section = builder.mark_text_slots(section, slide_index)
        parts.append(section)
        cursor = end
    parts.append(deck[cursor:])
    repaired_deck = "".join(parts)
    return source[:deck_start] + repaired_deck + source[deck_end:]


def main() -> int:
    builder = load_builder()
    changed = 0
    for path in sorted(PRESETS_DIR.glob("*.html")):
        source = path.read_text(encoding="utf-8")
        if "data-ported-template=" not in source:
            continue
        repaired = repair_source(source, builder)
        if repaired == source:
            continue
        path.write_text(repaired, encoding="utf-8")
        changed += 1
        print(f"repaired {path.relative_to(ROOT)}")
    print(f"Repaired editable slots in {changed} generated template ports.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
