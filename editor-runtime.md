# Editable deck runtime — DOM contract & integration

Use this document when generating HTML with **frontend-slides-editable**. The canonical copy-paste implementation lives in [examples/editable-deck-reference.html](examples/editable-deck-reference.html).

**Style vs. runtime:** This file defines **how** objects and chrome behave, not **what** each preset looks like. Generators must still follow [STYLE_PRESETS.md](STYLE_PRESETS.md) **Layout** and **Signature Elements** per preset (same expectation as parent `frontend-slides`). Copy **runtime** from the reference; do **not** clone its sample slide geometry for every aesthetic.

## When to include the runtime

This skill **always** ships presentations with the editable deck (edit mode, sidebar, undo, export). Omit only if the user explicitly asks for a read-only deck (rare); then follow the parent `frontend-slides` skill instead.

## Deck chrome tokens (`--deck-chrome-*`)

Fixed UI (progress bar, nav dots, **edit top bar**, sidebar, RTE, object handles, export bar) must **not** hardcode colors that only match one slide theme. Use CSS variables on `:root`:

| Variable | Typical use |
|----------|-------------|
| `--deck-chrome-bg` | Panels, semi-opaque bars |
| `--deck-chrome-border` | Borders on chrome controls |
| `--deck-chrome-text` | Labels, icon color (`currentColor` in SVG) |
| `--deck-chrome-muted` | Secondary labels |
| `--deck-chrome-accent` | Primary action, selection outline, resize handle |
| `--deck-chrome-shadow` | Drop shadow on floating chrome |
| `--deck-chrome-surface` | Button / input surfaces |

Slide **content** theme uses separate tokens (e.g. `--slide-bg-deep`, `--slide-bg-gradient`, `--text-primary` in the reference). **Phase 3 merge order:** `viewport-base.css` → preset `:root` (slide theme) → map or define `--deck-chrome-*` → runtime chrome CSS (using `var(--deck-chrome-*)` only).

**Surfaces that must not steal object clicks:** Mark chrome containers with `data-deck-chrome-surface` where focus/click routing matters; the reference uses it on `#rteToolbar`, `#deckEditChrome`, and `#deckAddElementMenu` for documentation and optional scripting. `#btnAddElement` is excluded from slide-object hit testing via `isDeckChromeNode()`.

## DOM contract

### Slide root

- Each slide is a `<section class="slide" id="slide-N">` (stable `id` required for persistence).
- `position: relative` is already set by `viewport-base.css` on `.slide`.
- **Deck queries:** Runtime code must list slides only under the deck root (e.g. `.slides-offset` with `:scope > section.slide`). Thumbnail previews clone `<section class="slide">` into the sidebar; a global `querySelectorAll('section.slide')` will include those clones and break navigation, reorder, and refresh (duplicate slides).

### Edit layer

- Direct child of each slide (or after background layers):

```html
<div class="slide-edit-layer" aria-hidden="true"></div>
```

- CSS: `position: absolute; inset: 0; z-index: 5; pointer-events: none;`
- In **edit mode**, children with `pointer-events: auto` receive clicks; the layer itself stays `pointer-events: none` so clicks pass through empty areas to a **slide hit target** (optional full-size transparent child) only if you need “click empty to deselect” — the reference uses the layer with `pointer-events: none` and listens on `section.slide` for background hits.

### Slide objects (`data-slide-object`)

Every independently movable / selectable block **must** include a move handle and a resize handle. The reference injects missing controls via **`ensureObjectControls()`** on load, when entering edit mode, after undo restores objects, and after loading from `localStorage`. That helper adds **`.slide-object-resize`** and **`.slide-object-delete`** (×) when absent.

```html
<div
  class="slide-object"
  data-slide-object
  data-oid="s0-o0"
  data-object-type="text"
  style="position:absolute;left:8%;top:15%;width:80%;min-height:1em;"
>
  <button type="button" class="slide-object-move" aria-label="Move object" title="Drag to move">⠿</button>
  <button type="button" class="slide-object-delete" aria-label="Delete object">×</button>
  <button type="button" class="slide-object-resize" aria-label="Resize"></button>
  <div class="slide-object-text" contenteditable="false">Editable text</div>
</div>
```

| Attribute | Required | Meaning |
|-----------|----------|---------|
| `data-slide-object` | yes | Marker for editor |
| `data-oid` | yes | Unique string in the **whole document** (e.g. `s2-o1`) |
| `data-object-type` | recommended | `text` (inner `.slide-object-text`), `graphic` (CSS/decorative box), `image` (`.slide-object-graphic` with `<img>` — click on media selects only; drag via ⠿), or `video` (`.slide-object-graphic` with `<video controls>` — same interaction) |

**Text reflow:** `.slide-object-text` should use `width: 100%`, `box-sizing: border-box`, `overflow-wrap: anywhere` (and/or `word-break`) so changing the object’s width via resize updates line breaks without inner scroll.

**Graphics / images:**

```html
<div class="slide-object" data-slide-object data-oid="s0-o2" data-object-type="graphic"
     style="position:absolute;left:50%;top:40%;width:200px;height:120px;">
  <button type="button" class="slide-object-move" aria-label="Move object">⠿</button>
  <button type="button" class="slide-object-delete" aria-label="Delete object">×</button>
  <button type="button" class="slide-object-resize" aria-label="Resize"></button>
  <div class="slide-object-graphic">
    <img src="assets/x.png" alt="" style="max-height:min(40vh,300px);width:100%;object-fit:contain;pointer-events:none;">
  </div>
</div>
```

The snippet uses fixed `px` for brevity; when **generating** new decks, prefer **`%` or `clamp(...)`** on the outer `.slide-object` box where practical so layout stays consistent with viewport rules in `SKILL.md`.

- Position with `left` / `top` as **`%` of slide** (reference normalizes on drag end). `width` / `height` may be `%` or `px`; resize writes **`%` of slide** for consistency.

### Top-left control cluster (`#deckLeftHover`)

Controls are grouped in a **fixed top-left** container. **Opacity / pointer-events:** **Edit**, **Pages**, and (in edit mode) **#deckEditChrome** (Undo / Redo / Done) use the same **hover-reveal** pattern: moving the pointer into `#deckLeftHover` adds a `.show` class; `mouseleave` + ~400ms delay removes it (including while edit mode is on), matching the original “corner to reveal” behavior.

- **Edit** — enters edit mode only (label stays **Edit**; do not duplicate **Done** on this button).
- **Add element** — `#btnAddElement` (same hover-reveal row as **Save** in edit mode). Opens `#deckAddElementMenu` to insert **Text**, **Image** (local file, paste, or placeholder), or **Video** (local file) on the **current** slide with undo support.
- **Done** — only on `#deckEditChrome`; exits edit mode.
- **Undo** / **Redo** — icon buttons, `disabled` when stack empty; `HistoryStack` notifies via `onChange` callback.

`z-index` should stay **above** slide decorations so presets with corner marks remain readable.

### Object position for drag / undo (`left` / `top`)

`getComputedStyle(el).left` is usually **px**, not `%`, even when the author set `%` in the `style` attribute. The reference uses **`_positionPct(el, slide, 'left'|'top')`**: read `%` from **inline** `el.style` when present; otherwise derive from `getBoundingClientRect()` vs the slide rect. Using `?? 0` on failed parse causes a jump to the slide’s top-left on drag start.

### Edit mode CSS hooks

- `body.deck-edit-mode` — editor active; reference shows handles, sidebar, disables wheel navigation.
- `.slide-object.is-selected` — selected object (multi-select: multiple elements have this class). **Resize handle** is visible only when selected (`body.deck-edit-mode .slide-object.is-selected .slide-object-resize`). **Delete (×)** shows on hover or when selected (`body.deck-edit-mode .slide-object:hover .slide-object-delete` and `.is-selected`).
- `body.deck-sidebar-open` — reserve `padding-right` on slides container for the filmstrip.

## History command types (undo / redo)

| `type` | Payload (conceptually) | Undo behavior |
|--------|------------------------|---------------|
| `moveGroup` | `{ entries: [{ oid, left, top }] }` before or after snapshot | Restore previous `left`/`top` |
| `patchObject` | `{ oid, html }` or `{ oid, style: { left, top, width, height } }` | Restore prior fragment / dimensions |
| `deleteGroup` | `{ snapshots: [{ parentSelector, index, outerHTML }] }` | Re-insert nodes |
| `reorderSlides` | `{ fromIndex, toIndex }` | Move slide section back |
| `deleteSlide` | `{ index, outerHTML, nextSiblingId }` | Re-insert section |
| `copySlide` | cloned slide inserted after source index | Remove cloned slide |
| `newPage` | blank preset-matched slide inserted after current index | Remove inserted slide |

The reference implementation uses a **command stack** with `undo()` / `redo()` applying inverse operations. **`push()` clears the redo stack** and invokes an `onChange` callback (use it to sync undo/redo button `disabled` state).

## Snap alignment (reference behavior)

- **Snap threshold:** 8px (`SNAP_PX`), skipped when `prefers-reduced-motion: reduce`.
- **Slide guides:** Only **horizontal and vertical center** of the slide (`width/2`, `height/2`). **Slide outer edges are not snap targets** — avoids objects snapping to the viewport boundary when near the edge.
- **Object guides:** Edges and centers of **other** `data-slide-object` on the same slide (excluding the moving selection).
- Snapping adjusts the **drag delta** for the whole group so the **primary dragged element** aligns; siblings get the same delta.

## RTE (rich text toolbar)

- The always-visible row is compact: **Bold**, **Italic**, and three **drawer triggers** (**Font** / **Scale** / **Px**) that expand a **card** below with the detailed buttons. Only one drawer open at a time; click the trigger again to close, **Escape** (when not typing in text) to close drawers, or pointerdown outside `#rteToolbar` to collapse. Triggers show a subtle **hint** outline when the current selection matches an option inside that drawer.
- Toolbar `#rteToolbar` is shown when a `.slide-object-text[contenteditable="true"]` is **focused** or when the selection/caret is inside such an element (including **collapsed** caret — user can bold / change size without pre-selecting text).
- **Font + size controls** use toolbar **buttons**, not a native `<select>`, so `mousedown` can `preventDefault()` and keep the text field focused while formatting applies. Presets: **Body**, **Display**, plus **Serif** / **Sans** / **Mono** stacks; **Scale S–M–L–XL** uses wide-spaced factors and `clamp(...rem ...vw ...rem)` for viewport-safe body copy; **Px** applies fixed **`font-size` in px** (24 / 36 / 48 / 72 / 96); **Custom…** toggles an inline **number input (8–400) + Apply/Cancel** in the Px drawer (no `prompt()`, works in embedded browsers).
- **Inline styling** uses `_applyInlineStyle()` to wrap the current selection (or insert a styled zero-width span at a collapsed caret). If the DOM selection is missing or outside the active text box, the reference **re-anchors** a collapsed range at the **end** of the text field so font/size always applies. `_applyFontSizeFactor()` writes `font-size: clamp(...)`; `_applyFontSizePx()` writes `font-size: Npx`; `_applyFontFamily()` writes `font-family: ...`.
- **Bold / italic** state: toggle `.is-active` via `document.queryCommandState(...)` on `selectionchange` / after commands. Font / size buttons also toggle `.is-active` using computed `font-family` / `font-size` heuristics at the caret.
- **Focus handoff:** `focusout` should not commit/close editing when focus moves into `#rteToolbar`; check `activeElement` / `relatedTarget` against the toolbar before setting `contenteditable="false"`.

## Keyboard & interaction summary

| Action | Binding |
|--------|---------|
| Toggle edit mode | `E` (not while typing in `contenteditable`), or hotzone / **Edit** button |
| Exit edit mode | **Done** in `#deckEditChrome` (top-left, hover-revealed), **Esc** (first Esc blurs focused text; Esc again exits), or **E** to toggle off |
| Multi-select toggle | `Ctrl` + click object (macOS: **Control** key, not Cmd) |
| Single select | Click object without Ctrl |
| Clear selection | Click slide background (empty area) |
| Delete object (button) | **×** on object (hover or when selected); single-object delete, undoable |
| Delete / Backspace | Removes selected objects (confirm if 2+); not while typing in `contenteditable` |
| Add element | **Add element** (edit mode, top-left row) → Text / Image / Video on current slide |
| Undo / Redo | **Buttons** in `#deckEditChrome` (hover top-left cluster); or `Ctrl+Z` / **`Ctrl+Y` or `Ctrl+Shift+Z`** when edit mode and not typing in `contenteditable`; macOS **`Cmd+Z`**, **`Cmd+Shift+Z`**, **`Cmd+Y`** |
| Save | **Save** button in `#deckLeftHover` (row with Edit/Pages, edit mode only, hover-revealed) or `Ctrl+S` / **Cmd+S** |
| Bold / italic / font / size | Floating `#rteToolbar` when text is focused |
| Save to localStorage | `Ctrl+S` saves the full `.slides-offset` structure, not just per-slide inner HTML |
| Export HTML | Sidebar button in reference; export should strip edit-mode / selected-state classes |
| Copy slide | Hover a Pages thumbnail, click **Copy**; insert the duplicate immediately after that slide, regenerate slide ids / duplicate object ids, and make the operation undoable |
| New Page | Sidebar **+New Page** button beside **Export HTML**; insert a blank preset-matched page after the current slide, using the current slide’s background/style skeleton where possible |
| Delete slide | Pages filmstrip **×** — confirms with `Delete slide?`; at least one slide must remain (`Keep at least one slide.`) |

## Text editing `focusout` / history

- Commit text to history when the user **leaves** the `contenteditable` field (deferred `setTimeout(0)` so `relatedTarget` / `activeElement` settle).
- RTE toolbar uses **`mousedown` preventDefault** to reduce spurious blur before formatting clicks.

## Generator checklist (Phase 3)

1. Every slide has unique `id="slide-N"`.
2. Movable content sits in `.slide-edit-layer` as `.slide-object` with unique `data-oid`.
3. Text objects: `.slide-object-move` + `.slide-object-delete` + `.slide-object-resize` + `.slide-object-text` with `contenteditable="false"` until focused (or rely on `ensureObjectControls()` to inject missing chrome controls).
4. Include full `viewport-base.css` in `<style>`.
5. Define **slide theme** and **`--deck-chrome-*`** on `:root`; chrome CSS uses variables only.
6. Copy **deck runtime** from `examples/editable-deck-reference.html` (CSS + JS) or inline equivalent — keep `STORAGE_KEY` / deck id meta consistent if user needs multiple files.
7. After generating, verify at 1280×720: no slide overflow, handles visible only in edit mode.
8. Set `<html data-mobile-adaptation="desktop-default">` unless Phase 1 explicitly selected phone support; for phone support set `enabled` and include portrait + landscape media rules from the reference runtime.

## Files

| File | Role |
|------|------|
| [examples/editable-deck-reference.html](examples/editable-deck-reference.html) | Single-file working reference |
| [html-template.md](html-template.md) | Architecture notes + link to reference |
| [viewport-base.css](viewport-base.css) | Mandatory slide sizing |
