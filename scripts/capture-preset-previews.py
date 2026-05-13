#!/usr/bin/env python3
"""Capture one static PNG per generated preset deck (first slide / cover).

Requires Google Chrome or Chromium with headless support. Override binary:

  CHROME_PATH=/path/to/chrome python3 scripts/capture-preset-previews.py

Output: docs/preset-previews/<slug>-cover.png
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
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


def capture(chrome: str, html_path: Path, out_png: Path) -> None:
    uri = html_path.resolve().as_uri()
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
    subprocess.run(
        cmd,
        check=True,
        capture_output=True,
        text=True,
        timeout=PREVIEW_TIMEOUT_SECONDS,
    )


def main() -> int:
    chrome = find_chrome()
    if not chrome:
        print("No Chrome/Chromium found. Set CHROME_PATH or install Chrome.", file=sys.stderr)
        return 1
    if not PRESETS_DIR.is_dir():
        print(f"Missing presets dir: {PRESETS_DIR}", file=sys.stderr)
        return 1

    files = sorted(PRESETS_DIR.glob("*.html"))
    if not files:
        print(f"No HTML under {PRESETS_DIR}", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ok = 0
    for html_path in files:
        slug = html_path.stem
        out_png = OUT_DIR / f"{slug}-cover.png"
        try:
            print(f"Capturing {slug}...", flush=True)
            capture(chrome, html_path, out_png)
            print(out_png.relative_to(ROOT), flush=True)
            ok += 1
        except subprocess.CalledProcessError as e:
            print(f"FAIL {slug}: {e.stderr or e}", file=sys.stderr, flush=True)
        except subprocess.TimeoutExpired:
            print(
                f"FAIL {slug}: timed out after {PREVIEW_TIMEOUT_SECONDS}s",
                file=sys.stderr,
                flush=True,
            )
    print(f"Captured {ok}/{len(files)} previews using {chrome}", flush=True)
    return 0 if ok == len(files) else 2


if __name__ == "__main__":
    raise SystemExit(main())
