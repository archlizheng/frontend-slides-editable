#!/usr/bin/env python3
"""Capture cover/mid/later PNGs for slot-editable template ports.

Requires Google Chrome or Chromium with headless support. Override binary:

  CHROME_PATH=/path/to/chrome python3 scripts/capture-template-port-previews.py

Output:
  docs/preset-previews/<slug>-cover.png
  docs/preset-previews/<slug>-mid.png
  docs/preset-previews/<slug>-later.png
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
import tempfile
import importlib.util
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRESETS_DIR = ROOT / "examples" / "generated" / "presets"
OUT_DIR = ROOT / "docs" / "preset-previews"
VIEWPORT = os.environ.get("PREVIEW_VIEWPORT", "1600,900")
try:
    PREVIEW_TIMEOUT_SECONDS = int(os.environ.get("PREVIEW_TIMEOUT_SECONDS", "45"))
except ValueError as e:
    raise SystemExit("PREVIEW_TIMEOUT_SECONDS must be an integer") from e

if PREVIEW_TIMEOUT_SECONDS <= 0:
    raise SystemExit("PREVIEW_TIMEOUT_SECONDS must be greater than 0")


def load_port_previews():
    builder_path = ROOT / "scripts" / "build-template-port-decks.py"
    spec = importlib.util.spec_from_file_location("build_template_port_decks", builder_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Unable to load {builder_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    previews = []
    for port in module.PORTS:
        captures = tuple(zip(("cover", "mid", "later"), port.preview_indices))
        previews.append((port.out_slug, captures))
    return previews


PORT_PREVIEWS = load_port_previews()


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


def capture(chrome: str, html_path: Path, out_png: Path, slide_index: int) -> None:
    source = html_path.read_text(encoding="utf-8")
    if not re.search(rf'<section\b[^>]*\bid=["\']slide-{slide_index}["\']', source, flags=re.I):
        raise ValueError(f"{html_path.relative_to(ROOT)} has no slide-{slide_index}")
    capture_css = f"""
<style id="ported-capture-target-css">
  [data-port-editor-ui] {{ display: none !important; }}
  #deck.slides-offset {{ overflow: hidden !important; height: 100vh !important; }}
  #deck.slides-offset > section.slide {{
    position: absolute !important;
    inset: 0 !important;
    opacity: 0 !important;
    visibility: hidden !important;
    pointer-events: none !important;
  }}
  #deck.slides-offset > #slide-{slide_index} {{
    position: relative !important;
    inset: auto !important;
    opacity: 1 !important;
    visibility: visible !important;
    pointer-events: auto !important;
    width: 100vw !important;
    height: 100vh !important;
    height: 100dvh !important;
    scroll-snap-align: none !important;
  }}
  #deck.slides-offset > #slide-{slide_index} [data-anim] {{
    opacity: 1 !important;
    animation: none !important;
  }}
</style>
"""
    if "</head>" not in source:
        raise ValueError(f"{html_path} missing </head>")
    with tempfile.NamedTemporaryFile("w", suffix=".html", encoding="utf-8", delete=False) as tmp:
        tmp.write(source.replace("</head>", capture_css + "\n</head>", 1))
        tmp_path = Path(tmp.name)
    uri = tmp_path.resolve().as_uri()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={VIEWPORT}",
        f"--screenshot={out_png}",
        uri,
    ]
    try:
        subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            timeout=PREVIEW_TIMEOUT_SECONDS,
        )
    finally:
        tmp_path.unlink(missing_ok=True)


def main() -> int:
    chrome = find_chrome()
    if not chrome:
        print("No Chrome/Chromium found. Set CHROME_PATH or install Chrome.", file=sys.stderr)
        return 1
    if not PRESETS_DIR.is_dir():
        print(f"Missing presets dir: {PRESETS_DIR}", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ok = 0
    total = sum(len(captures) for _, captures in PORT_PREVIEWS)
    for slug, captures in PORT_PREVIEWS:
        html_path = PRESETS_DIR / f"{slug}.html"
        if not html_path.is_file():
            print(f"FAIL {slug}: missing {html_path.relative_to(ROOT)}", file=sys.stderr, flush=True)
            continue
        for label, index in captures:
            out_png = OUT_DIR / f"{slug}-{label}.png"
            try:
                print(f"Capturing {slug} {label} (slide-{index})...", flush=True)
                capture(chrome, html_path, out_png, index)
                print(out_png.relative_to(ROOT), flush=True)
                ok += 1
            except subprocess.CalledProcessError as e:
                print(f"FAIL {slug} {label}: {e.stderr or e}", file=sys.stderr, flush=True)
            except subprocess.TimeoutExpired:
                print(
                    f"FAIL {slug} {label}: timed out after {PREVIEW_TIMEOUT_SECONDS}s",
                    file=sys.stderr,
                    flush=True,
                )
    print(f"Captured {ok}/{total} ported-template previews using {chrome}", flush=True)
    return 0 if ok == total else 2


if __name__ == "__main__":
    raise SystemExit(main())
