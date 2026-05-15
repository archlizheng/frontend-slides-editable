# Editable Preset Runtime TDD Plan

## Summary

This document is the implementation guide for keeping every generated editable deck usable across presets while adding the Pages copy and new-page workflow. It is written for maintainers and future implementation agents. The post-read action is concrete: implement or review changes to the editable runtime, preset builders, and validation scripts without re-deciding scope.

Baseline before this work: `python3 scripts/validate-template-ports.py` validates the 34 ported template contracts, and the generated preset directory contains 46 decks. The new work adds a broader editable-runtime contract around mobile intent, editable titles/graphics, Pages duplication, blank page insertion, export/persistence safety, and performance measurement.

## Interfaces

- Phase 1 discovery must ask a required `Mobile` question: `Desktop-first only` or `Adapt for phone portrait + landscape`. Generated HTML records the explicit choice with `data-mobile-adaptation="desktop-default"` or `data-mobile-adaptation="enabled"`.
- Pages sidebar exposes two new commands: thumbnail hover/focus `Copy`, and footer `+New Page` beside `Export HTML`.
- Copy inserts a duplicate immediately after the selected thumbnail. New Page inserts a blank style-matched slide after the current slide.
- Runtime normalization must keep `section.slide` ids unique and regenerate only duplicated `data-oid` values. Reorder, delete, copy, new page, save, undo/redo, and export must continue to use root-scoped slide queries.
- Legacy preset decks expose editable content through `[data-slide-object][data-oid]`. Ported decks expose authored native-template content through `data-edit-slot`; titles, body copy, metrics, table text, and intentionally editable image slots must not remain static-only DOM.

## TDD Slices

- **S1 Baseline contract**: add a static validator that fails on missing Pages copy/new-page controls, missing mobile adaptation marker/media rules, global slide queries, duplicate slide ids, duplicate object ids, and missing editable title/content contracts. Make it pass for the reference deck and all generated presets.
- **S2 Discovery mobile question**: add a text/doc assertion or review check that `SKILL.md` Phase 1 requires the mobile question. Update `README`, `SKILL.md`, `editor-runtime.md`, and `html-template.md`.
- **S3 Mobile adaptation output**: add fixture checks for both `desktop-default` and `enabled`. For enabled output, require portrait and landscape media rules for sidebar/chrome/object behavior and browser smoke checks at 390x844 and 844x390.
- **S4 Editable titles and graphics**: create failing fixtures for static title-like nodes and intended editable graphic slots. Update template slot marking or legacy object generation so authored text is editable while decorative layout remains locked.
- **S5 Page copy**: write a browser smoke test that opens Pages, clicks a thumbnail Copy button, verifies slide count increments by one, insertion happens after the source slide, ids stay unique, object ids stay unique, and Undo removes the copied slide.
- **S6 New Page**: extend the browser smoke test to click `+New Page`, verify insertion after the current slide, check the blank page has an editable title object, and confirm it inherits preset background/chrome styling through existing CSS classes or copied background skeleton.
- **S7 Export and persistence**: after copy/new-page operations, save and export. Verify exported HTML strips transient editor state, keeps inserted slides, and does not contain filmstrip clone pollution.
- **S8 Performance**: record baseline timings for legacy build, template-port build, static validation, and sampled browser smoke. Optimize repeated reference-runtime extraction, duplicate file reads, and repeated regex passes only after a green behavioral baseline exists.

## Test Plan

- Static full run: `python3 scripts/validate-template-ports.py` and `python3 scripts/validate-editable-decks.py`.
- Build regression: `python3 scripts/build-preset-decks.py`, `BEAUTIFUL_TEMPLATES_DIR=./beautiful-html-templates python3 scripts/build-template-port-decks.py`, then rerun both static validators.
- Browser smoke: `python3 scripts/smoke-editable-decks.py`, which samples the reference deck, one legacy preset, and two ported presets. It checks desktop 1280x720, phone portrait 390x844, and phone landscape 844x390.
- Manual spot check before release: open one dark legacy preset and one ported template, enable edit mode, open Pages, copy a page, create a new page, save, refresh, and export.

## Assumptions

- The validation strategy is full static coverage plus sampled browser interaction, not a 46-preset browser matrix.
- No npm, package manager, or bundled browser automation dependency is introduced. Chrome/Chromium headless scripts follow the existing preview-capture style.
- Existing user edits in `examples/demos/frontend-slides-editable-readme-demo.html` are not reverted.
- Builder output may be regenerated, but hand-maintained demo decks are not treated as build artifacts.
