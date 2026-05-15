# Preset preview images

PNG files here are screenshots of the editable preset sample decks in `examples/generated/presets/`. They exist so the main [README.md](../../README.md) can show a quick visual gallery without opening every HTML file.

The generated decks are both **runtime smoke tests** and **visual previews**. There are now two build layers:

- `scripts/build-preset-decks.py` builds the 19 legacy preview decks. These still use one shared editable runtime with explicit preset/family archetypes for layout variety; same-name outputs are replaced by ported decks in the final 46-file gallery.
- `scripts/build-template-port-decks.py` builds the 34 ported decks from local `beautiful-html-templates/templates/{source_slug}/template.html`. These preserve upstream CSS, fonts, slide-level classes, and decorative DOM, then inject the shared Swiss/reference editor with a locked slot adapter.

Ported decks use a **Swiss runtime + locked slots** model: text, metric, image, and table-cell slots are editable through the same RTE, Undo/Redo, Save, Pages, Add element, and Export chrome as `swiss-modern.html`; decorative grids, hairlines, paper textures, pixel/glitch treatments, and authored layout containers are not `data-slide-object` boxes. User-added objects still live in `.slide-edit-layer` and can be dragged/resized.

Real generated decks should still use [STYLE_PRESETS.md](../../STYLE_PRESETS.md) as the style index. For the 34 ported presets, the true source of visual grammar is the matching `beautiful-html-templates` template plus its `template.json` mood/tone/density metadata.

## Regenerate

After changing themes or `examples/editable-deck-reference.html`, rebuild decks then re-capture:

```bash
python3 scripts/build-preset-decks.py
python3 scripts/capture-preset-previews.py
BEAUTIFUL_TEMPLATES_DIR=./beautiful-html-templates python3 scripts/build-template-port-decks.py
python3 scripts/capture-template-port-previews.py
python3 scripts/validate-template-ports.py
python3 scripts/validate-editable-decks.py
python3 scripts/test-editable-contract-fixtures.py
python3 scripts/validate-skill-workflow.py
python3 scripts/smoke-editable-decks.py
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

Naming:

- Legacy and all-preset cover captures: `<slug>-cover.png`
- Ported template captures: `<slug>-cover.png`, `<slug>-mid.png`, `<slug>-later.png`

`beautiful-html-templates/` is a local development input and is ignored by git; do not commit the cloned upstream repository into this skill.
