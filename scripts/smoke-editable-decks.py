#!/usr/bin/env python3
"""Run a small Chrome-headless smoke test for editable deck interactions.

The test is intentionally sampled, not a full preset matrix. It verifies the
canonical runtime behavior that static validation cannot prove: opening Pages,
copying a slide, creating a new page, undoing, and checking mobile viewports for
horizontal overflow.
"""

from __future__ import annotations

import json
import os
import platform
import html
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


INTERACTION_SCRIPT = r"""
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
    for sample in SAMPLES:
        if not sample.is_file():
            errors.append(f"missing sample {sample.relative_to(ROOT)}")
            continue
        result = chrome_eval(chrome, sample, 1280, 720, INTERACTION_SCRIPT)
        if not result.get("ok"):
            errors.append(f"{sample.relative_to(ROOT)} interaction failed: {result}")
        for label, width, height in VIEWPORTS:
            result = chrome_eval(chrome, sample, width, height, OVERFLOW_SCRIPT)
            if not result.get("ok"):
                errors.append(f"{sample.relative_to(ROOT)} {label} overflow: {result}")
    if errors:
        print("Editable deck smoke failed:")
        for error in errors:
            print(f"- {error}")
        return 2
    print(f"Smoke-tested {len(SAMPLES)} decks across {len(VIEWPORTS)} viewports using {chrome}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
