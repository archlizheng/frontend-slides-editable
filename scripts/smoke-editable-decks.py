#!/usr/bin/env python3
"""Run Chrome-headless smoke tests for editable deck interactions.

The default test is intentionally sampled, not a full preset matrix. It verifies
the runtime behavior that static validation cannot prove: edit mode activation,
slot editing for ported templates, Pages copy/new-page workflows, persistence,
export cleanup, and viewport overflow. Set SMOKE_PRESET_MATRIX=ported to run the
lightweight interaction checks against every ported template.
"""

from __future__ import annotations

import json
import os
import platform
import html
import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SAMPLES = [
    ROOT / "examples" / "editable-deck-reference.html",
    ROOT / "examples" / "generated" / "presets" / "bold-signal.html",
    ROOT / "examples" / "generated" / "presets" / "soft-editorial.html",
    ROOT / "examples" / "generated" / "presets" / "monochrome-ledger.html",
]
PORTED_SAMPLE_NAMES = {"soft-editorial.html", "monochrome-ledger.html"}
VIEWPORTS = [
    ("desktop", 1280, 720),
    ("mobile-portrait", 390, 844),
    ("mobile-landscape", 844, 390),
]
try:
    TIMEOUT_SECONDS = int(os.environ.get("SMOKE_TIMEOUT_SECONDS", "35"))
except ValueError as e:
    raise SystemExit("SMOKE_TIMEOUT_SECONDS must be an integer") from e


def find_chrome() -> str | None:
    env = os.environ.get("CHROME_PATH")
    if env and Path(env).is_file():
        return env
    if platform.system() == "Darwin":
        p = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
        if p.is_file():
            return str(p)
    for name in ("google-chrome-stable", "google-chrome", "chromium", "chromium-browser"):
        found = shutil.which(name)
        if found:
            return found
    return None


def load_builder_ports():
    builder_path = ROOT / "scripts" / "build-template-port-decks.py"
    spec = importlib.util.spec_from_file_location("build_template_port_decks", builder_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Unable to load {builder_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.PORTS


def sample_paths() -> list[Path]:
    matrix = os.environ.get("SMOKE_PRESET_MATRIX", "").strip().lower()
    if not matrix:
        return SAMPLES
    if matrix == "ported":
        return [ROOT / "examples" / "generated" / "presets" / f"{port.out_slug}.html" for port in load_builder_ports()]
    if matrix == "components":
        return [
            ROOT / "examples" / "generated" / "presets" / "soft-editorial.html",
            ROOT / "examples" / "generated" / "presets" / "monochrome-ledger.html",
        ]
    if matrix == "all":
        return sorted((ROOT / "examples" / "generated" / "presets").glob("*.html"))
    raise SystemExit("SMOKE_PRESET_MATRIX must be empty, 'ported', 'components', or 'all'")


def chrome_eval(chrome: str, html_path: Path, width: int, height: int, script: str) -> dict:
    with tempfile.TemporaryDirectory(prefix="editable-smoke-") as tmp:
        tmp_dir = Path(tmp)
        harness = tmp_dir / html_path.name
        source = html_path.read_text(encoding="utf-8")
        test_script_json = json.dumps(script)
        timeout_ms = TIMEOUT_SECONDS * 1000 - 1000
        injected = """
<script id="editable-smoke-harness">
const testScript = __TEST_SCRIPT__;
function finish(payload) {{
  document.body.setAttribute('data-result', JSON.stringify(payload));
  document.title = 'RESULT:' + JSON.stringify(payload);
}}
window.addEventListener('load', () => {{
  document.documentElement.setAttribute('data-mobile-adaptation', 'enabled');
  setTimeout(() => {{
    try {{
      const fn = new Function('return (async () => {\\n' + testScript + '\\n})()');
      Promise.resolve(fn()).then((payload) => finish(payload)).catch((err) => finish({ok:false,error:String(err && err.message || err)}));
    }} catch (err) {{
      finish({ok:false,error:String(err && err.message || err)});
    }}
  }}, 250);
}});
setTimeout(() => finish({ok:false,error:'timeout'}), __TIMEOUT_MS__);
</script>
""".replace("__TEST_SCRIPT__", test_script_json).replace("__TIMEOUT_MS__", str(timeout_ms))
        if "</body>" in source:
            source = source.replace("</body>", injected + "\n</body>", 1)
        else:
            source += injected
        harness.write_text(source, encoding="utf-8")
        cmd = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--disable-web-security",
            "--allow-file-access-from-files",
            "--hide-scrollbars",
            f"--window-size={width},{height}",
            "--virtual-time-budget=5000",
            "--dump-dom",
            harness.resolve().as_uri(),
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT_SECONDS)
        dumped = proc.stdout
        attr_match = re.search(r'data-result="([^"]+)"', dumped)
        title_match = re.search(r"<title>RESULT:(.*?)</title>", dumped, flags=re.S)
        raw = attr_match.group(1) if attr_match else (title_match.group(1) if title_match else "")
        if not raw:
            return {"ok": False, "error": (proc.stderr or dumped)[-500:]}
        return json.loads(html.unescape(raw))


EDIT_MODE_SCRIPT = r"""
const edit = document.getElementById('editToggle');
const pages = document.getElementById('pagesToggle');
const hover = document.getElementById('deckLeftHover');
if (!edit) throw new Error('missing Edit button');
if (!pages) throw new Error('missing Pages button');
if (!hover) throw new Error('missing deckLeftHover');
document.body.classList.remove('deck-edit-mode', 'slide-anim-paused');
edit.classList.remove('active', 'show');
pages.classList.remove('active', 'show');
edit.click();
await new Promise((resolve) => setTimeout(resolve, 40));
const clickActivated = document.body.classList.contains('deck-edit-mode') && edit.classList.contains('active');
document.dispatchEvent(new KeyboardEvent('keydown', {key: 'E', bubbles: true, cancelable: true}));
await new Promise((resolve) => setTimeout(resolve, 40));
const keyExited = !document.body.classList.contains('deck-edit-mode');
document.dispatchEvent(new KeyboardEvent('keydown', {key: 'e', bubbles: true, cancelable: true}));
await new Promise((resolve) => setTimeout(resolve, 40));
const keyActivated = document.body.classList.contains('deck-edit-mode') && edit.classList.contains('active');
hover.dispatchEvent(new MouseEvent('mouseenter', {bubbles: true}));
await new Promise((resolve) => setTimeout(resolve, 40));
const hoverShowsControls = edit.classList.contains('show') && pages.classList.contains('show');
return {ok: clickActivated && keyExited && keyActivated && hoverShowsControls, clickActivated, keyExited, keyActivated, hoverShowsControls};
"""


PAGES_SCRIPT = r"""
const sidebar = document.getElementById('slideSidebar');
const pages = document.getElementById('pagesToggle');
if (!pages || !sidebar) throw new Error('missing Pages sidebar');
pages.click();
const root = document.querySelector('.slides-offset');
const before = root.querySelectorAll(':scope > section.slide').length;
const storageKey = 'editable-deck:' + (document.documentElement.getAttribute('data-deck-id') || 'default');
localStorage.removeItem(storageKey);
const firstCopy = document.querySelector('[data-filmstrip-action="copy"]');
if (!firstCopy) throw new Error('missing copy button');
firstCopy.click();
const afterCopy = root.querySelectorAll(':scope > section.slide').length;
const newPage = document.getElementById('btnNewPage');
if (!newPage) throw new Error('missing new page button');
newPage.click();
const afterNew = root.querySelectorAll(':scope > section.slide').length;
const ids = Array.from(root.querySelectorAll(':scope > section.slide')).map((s) => s.id);
const oids = Array.from(root.querySelectorAll('[data-oid]')).map((o) => o.getAttribute('data-oid'));
const uniqueIds = new Set(ids).size === ids.length;
const uniqueOids = new Set(oids).size === oids.length;
const undo = document.getElementById('btnUndo');
if (undo) undo.click();
const afterUndo = root.querySelectorAll(':scope > section.slide').length;
let exportedHtml = '';
const originalCreateObjectURL = URL.createObjectURL;
URL.createObjectURL = (blob) => {
  if (blob && typeof blob.text === 'function') {
    blob.text().then((text) => { exportedHtml = text; });
  }
  return 'blob:editable-smoke';
};
URL.revokeObjectURL = () => {};
const originalClick = HTMLAnchorElement.prototype.click;
HTMLAnchorElement.prototype.click = function () {};
const save = document.getElementById('btnSave');
if (!save) throw new Error('missing Save button');
save.click();
const saved = JSON.parse(localStorage.getItem(storageKey) || '{}');
const savedCount = saved.deckHtml ? (saved.deckHtml.match(/<section\b[^>]*\bclass="[^"]*\bslide\b/g) || []).length : 0;
const exportButton = document.getElementById('btnExport');
if (!exportButton) throw new Error('missing Export button');
exportButton.click();
await new Promise((resolve) => setTimeout(resolve, 80));
URL.createObjectURL = originalCreateObjectURL;
HTMLAnchorElement.prototype.click = originalClick;
const exportedDoc = new DOMParser().parseFromString(exportedHtml, 'text/html');
const exportChecks = {
  hasDoctype: exportedHtml.includes('<!DOCTYPE html>'),
  noEditMode: !exportedDoc.body.classList.contains('deck-edit-mode'),
  noSidebarOpen: !exportedDoc.body.classList.contains('deck-sidebar-open'),
  noSelected: !exportedDoc.querySelector('.slide-object.is-selected'),
  noMediaFileInput: !exportedDoc.querySelector('.slide-object-media-file, input[type="file"]'),
  emptyFilmstrip: !exportedDoc.querySelector('#filmstripList') || exportedDoc.querySelector('#filmstripList').children.length === 0
};
const exportClean = Object.values(exportChecks).every(Boolean);
const originalHtml = root.innerHTML;
root.innerHTML = '<section class="slide" id="temporary-slide"></section>';
root.innerHTML = saved.deckHtml || '';
const afterLoad = root.querySelectorAll(':scope > section.slide').length;
root.innerHTML = originalHtml;
return {
  ok: afterCopy === before + 1 && afterNew === before + 2 && afterUndo === before + 1 &&
    uniqueIds && uniqueOids && savedCount === afterUndo && afterLoad === afterUndo && exportClean,
  before, afterCopy, afterNew, afterUndo, savedCount, afterLoad, uniqueIds, uniqueOids, exportClean, exportChecks
};
"""


SLOT_EDIT_SCRIPT = r"""
const root = document.querySelector('.slides-offset');
if (!root) throw new Error('missing slides root');
const slot = root.querySelector('[data-edit-slot][data-slot-type="text"], [data-edit-slot][data-slot-type="metric"], [data-edit-slot][data-slot-type="table-cell"]');
if (!slot) return {ok: true, skipped: true, reason: 'no editable slot'};
const edit = document.getElementById('editToggle');
if (!edit) throw new Error('missing Edit button');
const storageKey = 'editable-deck:' + (document.documentElement.getAttribute('data-deck-id') || 'default');
localStorage.removeItem(storageKey);
if (!document.body.classList.contains('deck-edit-mode')) {
  edit.click();
  await new Promise((resolve) => setTimeout(resolve, 40));
}
if (!document.body.classList.contains('deck-edit-mode')) throw new Error('edit mode did not activate before slot edit');
const before = slot.innerHTML;
const marker = 'Smoke edited slot text';
slot.click();
await new Promise((resolve) => setTimeout(resolve, 40));
const becameEditable = slot.getAttribute('contenteditable') === 'true' || slot.isContentEditable;
slot.textContent = marker;
slot.dispatchEvent(new InputEvent('input', {bubbles: true, inputType: 'insertText', data: marker}));
const focusSink = document.createElement('button');
focusSink.type = 'button';
focusSink.textContent = 'focus sink';
focusSink.style.cssText = 'position:fixed;left:-9999px;top:-9999px;';
document.body.appendChild(focusSink);
focusSink.focus();
slot.blur();
slot.dispatchEvent(new FocusEvent('focusout', {bubbles: true, relatedTarget: focusSink}));
await new Promise((resolve) => setTimeout(resolve, 80));
focusSink.remove();
const committed = slot.getAttribute('contenteditable') !== 'true' && slot.textContent === marker;
const undo = document.getElementById('btnUndo');
const redo = document.getElementById('btnRedo');
if (!undo || !redo) throw new Error('missing undo/redo buttons');
const undoEnabled = !undo.disabled;
undo.click();
await new Promise((resolve) => setTimeout(resolve, 40));
const undoRestored = slot.innerHTML === before;
redo.click();
await new Promise((resolve) => setTimeout(resolve, 40));
const redoApplied = slot.textContent === marker;
const save = document.getElementById('btnSave');
if (!save) throw new Error('missing Save button');
save.click();
const saved = JSON.parse(localStorage.getItem(storageKey) || '{}');
const savedHasEdit = typeof saved.deckHtml === 'string' && saved.deckHtml.includes(marker);
let exportedHtml = '';
const originalCreateObjectURL = URL.createObjectURL;
URL.createObjectURL = (blob) => {
  if (blob && typeof blob.text === 'function') {
    blob.text().then((text) => { exportedHtml = text; });
  }
  return 'blob:editable-slot-smoke';
};
URL.revokeObjectURL = () => {};
const originalClick = HTMLAnchorElement.prototype.click;
HTMLAnchorElement.prototype.click = function () {};
const exportButton = document.getElementById('btnExport');
if (!exportButton) throw new Error('missing Export button');
exportButton.click();
for (let i = 0; i < 20 && !exportedHtml; i++) {
  await new Promise((resolve) => setTimeout(resolve, 50));
}
URL.createObjectURL = originalCreateObjectURL;
HTMLAnchorElement.prototype.click = originalClick;
const exportedDoc = new DOMParser().parseFromString(exportedHtml, 'text/html');
const exportChecks = {
  noEditableSlot: !exportedDoc.querySelector('[data-edit-slot][contenteditable="true"]'),
  noDeckHtmlBefore: !exportedDoc.querySelector('[data-_deck-html-before]'),
  hasMarker: exportedHtml.includes(marker)
};
const exportClean = Object.values(exportChecks).every(Boolean);
return {ok: becameEditable && committed && undoEnabled && undoRestored && redoApplied && savedHasEdit && exportClean,
  becameEditable, committed, undoEnabled, undoRestored, redoApplied, savedHasEdit, exportClean, exportChecks};
"""


COMPONENT_UNLOCK_SCRIPT = r"""
window.confirm = () => true;
const root = document.querySelector('.slides-offset');
if (!root) throw new Error('missing slides root');
const edit = document.getElementById('editToggle');
const unlock = document.getElementById('btnUnlockLayout');
if (!edit) throw new Error('missing Edit button');
if (!unlock) throw new Error('missing Unlock layout button');
if (!document.body.classList.contains('deck-edit-mode')) {
  edit.click();
  await new Promise((resolve) => setTimeout(resolve, 40));
}
const slide = root.querySelector(':scope > section.slide');
if (!slide) throw new Error('missing slide');
const beforeObjects = slide.querySelectorAll('[data-slide-object]').length;
unlock.click();
await new Promise((resolve) => setTimeout(resolve, 80));
const afterObjects = slide.querySelectorAll('[data-slide-object]').length;
const hasComponentObjects = afterObjects > beforeObjects && !!slide.querySelector('[data-component-source-slot]');
const oids = Array.from(slide.querySelectorAll('[data-oid]')).map((o) => o.getAttribute('data-oid'));
const uniqueOids = new Set(oids).size === oids.length;
const firstObject = slide.querySelector('[data-component-source-slot]');
const selectedOrPresent = !!firstObject;
const undo = document.getElementById('btnUndo');
if (!undo) throw new Error('missing undo button');
const undoEnabled = !undo.disabled;
undo.click();
await new Promise((resolve) => setTimeout(resolve, 60));
const undoDisabledAfter = undo.disabled;
const undoAriaAfter = undo.getAttribute('aria-disabled');
const restoredSlide = root.querySelector(':scope > section.slide');
const restoredObjects = restoredSlide.querySelectorAll('[data-slide-object]').length;
const restoredComponentized = restoredSlide.dataset.componentized === 'true';
const restored = restoredObjects === beforeObjects && !restoredComponentized;
return {ok: hasComponentObjects && uniqueOids && selectedOrPresent && undoEnabled && restored,
  beforeObjects, afterObjects, restoredObjects, restoredComponentized, undoDisabledAfter, undoAriaAfter, hasComponentObjects, uniqueOids, selectedOrPresent, undoEnabled, restored};
"""

OVERFLOW_SCRIPT = r"""
const root = document.querySelector('.slides-offset');
const doc = document.documentElement;
const body = document.body;
const overflow = [
  {id: 'documentElement', scrollWidth: doc.scrollWidth, clientWidth: doc.clientWidth},
  {id: 'body', scrollWidth: body.scrollWidth, clientWidth: body.clientWidth},
  {id: 'slides-offset', scrollWidth: root.scrollWidth, clientWidth: root.clientWidth}
].filter((s) => s.scrollWidth > s.clientWidth + 2);
return {ok: overflow.length === 0, overflow};
"""


def main() -> int:
    chrome = find_chrome()
    if not chrome:
        print("No Chrome/Chromium found. Set CHROME_PATH or install Chrome.", file=sys.stderr)
        return 1
    errors: list[str] = []
    samples = sample_paths()
    for sample in samples:
        if not sample.is_file():
            errors.append(f"missing sample {sample.relative_to(ROOT)}")
            continue
        result = chrome_eval(chrome, sample, 1280, 720, EDIT_MODE_SCRIPT)
        if not result.get("ok"):
            errors.append(f"{sample.relative_to(ROOT)} edit mode failed: {result}")
        matrix_mode = bool(os.environ.get("SMOKE_PRESET_MATRIX"))
        if not matrix_mode:
            result = chrome_eval(chrome, sample, 1280, 720, PAGES_SCRIPT)
            if not result.get("ok"):
                errors.append(f"{sample.relative_to(ROOT)} pages/export interaction failed: {result}")
        source = sample.read_text(encoding="utf-8")
        if "data-edit-slot=" in source or sample.name in PORTED_SAMPLE_NAMES or matrix_mode:
            result = chrome_eval(chrome, sample, 1280, 720, SLOT_EDIT_SCRIPT)
            if not result.get("ok"):
                errors.append(f"{sample.relative_to(ROOT)} slot edit failed: {result}")
        if os.environ.get("SMOKE_PRESET_MATRIX", "").strip().lower() == "components":
            result = chrome_eval(chrome, sample, 1280, 720, COMPONENT_UNLOCK_SCRIPT)
            if not result.get("ok"):
                errors.append(f"{sample.relative_to(ROOT)} component unlock failed: {result}")
        if not matrix_mode:
            for label, width, height in VIEWPORTS:
                result = chrome_eval(chrome, sample, width, height, OVERFLOW_SCRIPT)
                if not result.get("ok"):
                    errors.append(f"{sample.relative_to(ROOT)} {label} overflow: {result}")
    if errors:
        print("Editable deck smoke failed:")
        for error in errors:
            print(f"- {error}")
        return 2
    matrix = os.environ.get("SMOKE_PRESET_MATRIX", "sample") or "sample"
    print(f"Smoke-tested {len(samples)} decks in {matrix} mode using {chrome}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
