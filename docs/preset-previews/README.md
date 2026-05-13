# Preset preview images

PNG files here are **first-slide screenshots** of the editable smoke-test decks in `examples/generated/presets/`. They exist so the main [README.md](../../README.md) can show a quick visual gallery without opening every HTML file.

On each preset’s **cover** slide, `scripts/build-preset-decks.py` injects **family-specific** static decoration (typically **`.slide-cover::after`** and/or **`.slide-cover > .slide-bg::after`**; some themes keep **`.slide-cover::before`** in the preset block). Shapes are pure CSS, **not** `data-slide-object` boxes, so they stay out of the edit layer.

## Regenerate

After changing themes or `examples/editable-deck-reference.html`, rebuild decks then re-capture:

```bash
python3 scripts/build-preset-decks.py
python3 scripts/capture-preset-previews.py
```

Requires **Chrome** or **Chromium** with headless mode. On macOS, Chrome is auto-detected; elsewhere set:

```bash
export CHROME_PATH=/usr/bin/google-chrome-stable
```

Optional viewport (default `1600,900`) and per-image timeout (default `45` seconds):

```bash
PREVIEW_VIEWPORT=1920,1080 python3 scripts/capture-preset-previews.py
PREVIEW_TIMEOUT_SECONDS=60 python3 scripts/capture-preset-previews.py
```

Naming: `<slug>-cover.png` matches `examples/generated/presets/<slug>.html`.
