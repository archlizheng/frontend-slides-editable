#!/usr/bin/env python3
"""Regression fixtures for the editable deck static validator.

These are deliberately tiny broken decks. The test proves the public validator
fails for the core regressions it is supposed to catch, without relying on a
large generated preset fixture.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-editable-decks.py"

BASE_HTML = """<!doctype html>
<html data-mobile-adaptation="desktop-default">
<head>
<style>
@media (max-width: 700px) and (orientation: portrait) {{ .slide {{ overflow-x:hidden; }} }}
@media (max-height: 500px) and (orientation: landscape) {{ .slide {{ overflow-x:hidden; }} }}
</style>
</head>
<body>
<aside id="slideSidebar"><button id="btnNewPage">+New Page</button></aside>
<div class="slides-offset" id="deck">
{slides}
</div>
<script>
document.querySelector('.slides-offset').querySelectorAll(':scope > section.slide');
function renumberDeckSlides() {{}}
function renumberDeckObjects() {{}}
function createBlankSlideFromPreset() {{}}
function _copySlide(index) {{}}
function _newPageAfterCurrent() {{}}
function exportHtml() {{}}
function sanitizeExportDocument() {{}}
localStorage.setItem('x','y');
document.createElement('button').setAttribute('data-filmstrip-action', 'copy');
</script>
</body>
</html>
"""

GOOD_SLIDES = """
<section class="slide" id="slide-0">
  <h1 data-edit-slot="s0-title">Editable title</h1>
</section>
"""

FIXTURES = {
    "duplicate_slide_ids": BASE_HTML.format(
        slides="""
<section class="slide" id="slide-0"><h1 data-edit-slot="a">A</h1></section>
<section class="slide" id="slide-0"><h1 data-edit-slot="b">B</h1></section>
"""
    ),
    "duplicate_object_ids": BASE_HTML.format(
        slides="""
<section class="slide" id="slide-0">
  <div data-slide-object data-oid="dup"><div class="slide-object-text">A</div></div>
  <div data-slide-object data-oid="dup"><div class="slide-object-text">B</div></div>
</section>
"""
    ),
    "static_title": BASE_HTML.format(
        slides="""
<section class="slide" id="slide-0">
  <h1>Static title</h1>
  <p data-edit-slot="body">Editable body</p>
</section>
"""
    ),
    "missing_mobile_marker": BASE_HTML.replace(' data-mobile-adaptation="desktop-default"', "").format(slides=GOOD_SLIDES),
}

EXPECTED_MESSAGES = {
    "duplicate_slide_ids": "slide ids are not unique",
    "duplicate_object_ids": "data-oid values are not unique",
    "static_title": "title-like authored text is not editable",
    "missing_mobile_marker": "missing mobile adaptation marker",
}


def run_validator(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--file", str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=15,
    )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="editable-contract-fixtures-") as tmp:
        tmp_dir = Path(tmp)
        errors: list[str] = []
        for name, source in FIXTURES.items():
            path = tmp_dir / f"{name}.html"
            path.write_text(source, encoding="utf-8")
            proc = run_validator(path)
            expected = EXPECTED_MESSAGES[name]
            output = proc.stdout + proc.stderr
            if proc.returncode == 0:
                errors.append(f"{name}: validator unexpectedly passed")
            elif expected not in output:
                errors.append(f"{name}: missing expected message {expected!r}; got {output!r}")
        if errors:
            print("Editable contract fixture tests failed:")
            for error in errors:
                print(f"- {error}")
            return 2
    print(f"Editable contract fixtures failed as expected ({len(FIXTURES)} cases).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
