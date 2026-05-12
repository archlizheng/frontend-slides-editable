# Preset preview images

PNG files here are **first-slide screenshots** of the editable smoke-test decks in `examples/generated/presets/`. They exist so the main [README.md](../../README.md) can show a quick visual gallery without opening every HTML file.

On each preset’s **cover** slide, decorative shapes that are not part of the editable object layer are drawn with **`.slide-cover > .slide-bg::after`** (pure CSS), not a `data-slide-object` box.

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

Optional viewport (default `1600,900`):

```bash
PREVIEW_VIEWPORT=1920,1080 python3 scripts/capture-preset-previews.py
```

Naming: `<slug>-cover.png` matches `examples/generated/presets/<slug>.html`.
