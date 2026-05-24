---
name: frontend-slides-editable
description: Use when the user wants a single-file HTML presentation that stays editable in the browser after generation, or needs object-level layout editing, slide reordering, local save/export, or PPT/PDF-to-web conversion with continued editing.
---

<objective>
Frontend Slides (Editable)

Create zero-dependency, animation-rich HTML presentations that run entirely in the browser **with a built-in editor**: move objects, multi-select with **Ctrl+click**, alignment snapping, simple text formatting with **font family + size controls**, **undo/redo**, a **Pages** sidebar (slide thumbnails, drag to reorder, delete), **Ctrl+S** persistence, and **export HTML**.

This skill is a **copy of the `frontend-slides` skill** extended with the editable deck runtime. For read-only decks without editor weight, use the original **`frontend-slides`** skill instead (same skills directory layout).
</objective>

<preset_fidelity>
Parity with parent `frontend-slides` (style flexibility)

**Adding edit mode must not replace preset authoring.** The parent skill treats each choice in [STYLE_PRESETS.md](STYLE_PRESETS.md) as a **spec**: per preset you implement its **Layout** prose, **Signature Elements**, typography, and colors — title slides and content slides **differ across presets** (e.g. Bold Signal’s card + big numerals vs. Notebook Tabs’ paper + edge tabs vs. Swiss Modern’s grid + red bar).

**Normative behavior in Phase 3:**

1. **Read STYLE_PRESETS for the chosen preset(s)** and reflect **layout + signatures** in HTML/CSS, not only `:root` colors and fonts.
2. **The editable reference** ([examples/editable-deck-reference.html](examples/editable-deck-reference.html)) supplies **JS/CSS patterns** (chrome, sidebar, objects, history) — not a **frozen slide layout** to paste on every deck. Do **not** reuse one generic “title + subtitle + corner rounded rectangle” geometry for every style.
3. **`examples/generated/presets/*.html`** are sample decks, not a layout shortcut. The 12 legacy samples are runtime smoke + visual previews; the 34 ported samples are real-template ports from `beautiful-html-templates` using the shared Swiss/reference runtime plus locked slot editing. For real deliveries, match the chosen preset/template grammar instead of reusing a generic README deck.
4. **Static chrome** (decorations that should not be draggable) may live outside `.slide-edit-layer` (e.g. background pseudo-elements, fixed nav chrome) per preset; **movable** copy and blocks stay as `[data-slide-object]` inside the layer.

If runtime constraints ever conflict with a signature element, **adapt the element** (e.g. implement the same visual with CSS, or split into multiple objects) — do **not** drop preset identity for the sake of a single template.
</preset_fidelity>

<template_ports>
Real-template ports (slot-editable)

For the 34 ported presets from `beautiful-html-templates`, prefer the upstream template's **mood / tone / density** and visual grammar over color-token matching alone.

Interaction baseline: ported decks must use the same Swiss/reference editor chrome and object editor as `examples/editable-deck-reference.html` / `swiss-modern.html`. Native template slots are locked-layout content slots; user-added objects are normal `[data-slide-object][data-oid]` objects.

**Important interaction contract:** `data-edit-slot` is editable content, not a draggable component. In edit mode the user can click slot text/images to change their content with RTE/Undo/Redo/Save/Export, but the upstream template's layout grid, card geometry, decorative layers, and spacing stay locked. Only user-added objects in `.slide-edit-layer` become selectable, draggable, resizable components. Do not promise that every native template child will get object handles unless a separate componentization mode is explicitly requested and implemented.

Template edit modes:

- `data-template-edit-mode="slots"` is the default. It is template-safe: authored content is editable through slots, while layout and decoration remain locked.
- `data-template-edit-mode="components"` is an optional generated mode for semantic blocks that can be represented as `[data-slide-object]`.
- In delivered ported decks, **Unlock layout** componentizes the current slide on demand by creating movable copies of editable slots in `.slide-edit-layer`. The original native template DOM stays in place for fidelity, and the operation is undoable.
- Never componentize every DOM node. Exclude backgrounds, grids, axes, ticks, decorative marks, texture/glitch layers, SVG paths, animation wrappers, and pure layout containers.

When using or extending a ported preset:

1. Treat the matching `beautiful-html-templates/templates/{source_slug}/template.html` as the visual system: preserve fonts, CSS variables, slide-level classes, layout grid, decorative DOM, and component grammar.
2. Edit authored content through slots, not by decomposing the template into draggable boxes. Use:
   - `data-edit-slot`
   - `data-slot-type="text|image|metric|table-cell"`
   - `data-slot-label`
   - `data-slot-locked-layout="true"`
3. Keep decorative elements locked unless the user should naturally change that exact item. Grids, paper texture, hairlines, scan lines, pixel/glitch layers, ornamental marks, and layout containers should not become draggable objects.
4. Preserve `.slide-edit-layer` for user-added freeform objects. Added objects can use `[data-slide-object][data-oid]` and the normal Swiss drag/resize/multi-select runtime; native template slots use the Swiss RTE/Undo/Redo/Save/Export path but do not get move/resize handles.
5. If a needed slide type is missing, design a new slide in the same template system: same fonts, palette, spacing rhythm, chrome, and component grammar. Do not mix in another template's visual language.
</template_ports>

<discovery_gate>
Discovery gate (do not skip)

Models often jump straight to generating HTML. **For Mode A (new deck) and Mode B (PPT or PDF) after extraction, you must finish Phase 1 before Phase 2, and Phase 2 before Phase 3** — unless a narrow exception below applies.

**Hard rule:** Unless the user provides **in one turn** (or one clearly scoped batch) **every** item in the **Phase 1 checklist**, you **must** run **Phase 1 first** as **one grouped message** (or a structured question UI). If the batch is incomplete, send **only** the **missing** checklist items in the next message — **do not** guess slide count, outline depth, preset, or language. **Invoking `/frontend-slides-editable` or attaching this skill does *not* waive discovery.** A one-liner (e.g. “用 skill 介绍它自己”, “做一份某某主题的演示”) is **topic / intent only**, not a brief.

**Phase 1 checklist (complete brief — all required without model inference):**

| # | Dimension | What “done” means |
|---|-------------|-------------------|
| 1 | **Purpose** | Pitch / teaching / conference / internal / meta-role (e.g. skill onboarding), etc. |
| 2 | **Length** | **Slide-count band** (e.g. short 5–10 / medium 10–20 / long 20+) **or** exact count — never inferred from topic alone |
| 3 | **Content** | Pasted outline, bullets, draft copy, **or** named source + extract scope (e.g. “README §X–Y only”); not “a theme” alone |
| 4 | **Style direction** | Phase 1 style preference cluster **or** a **named** preset from [STYLE_PRESETS.md](STYLE_PRESETS.md) **or** explicit delegation (“you choose”) — if only “you choose”, **Phase 2** still runs to narrow via recommendations/previews unless the user also explicitly skips previews |
| 5 | **Editing** | Confirm **full editable runtime** (this skill’s default) **or** explicit switch to parent **read-only** `frontend-slides` |
| 6 | **Images** | No / yes / unsure; if **yes**, files may arrive later, but intent is explicit |
| 7 | **Mobile** | Required answer: **Desktop-first only** (default) or **Adapt for phone portrait + landscape**; do not infer this silently |
| — | **Language / locale** | When prose is audience-facing and not already stated: monolingual / bilingual / per-locale files — **ask in Phase 1** |

**Images vs outline:** **Co-design outline ↔ images** (Step 1.2) only **after** the user has real assets or links to evaluate. Do **not** skip Phase 1 dimensions just because images are pending; capture “yes, will provide” in Phase 1, then run image evaluation when files exist.

**Mode B (PPT / PDF):** After `extract-pptx.py` (`.pptx`) or `extract-pdf.py` (`.pdf`), present titles/summaries/asset counts and **still run Phase 1** for anything extraction does **not** decide: **length goals** if restructuring, **style direction**, **editing** scope, **locale**, and **image** handling notes on extracted assets. **Do not** jump from “here’s the extract” straight to **only** style picking — close Phase 1 gaps first, **then** Phase 2, **then** codegen.

**When Phase 1 and/or Phase 2 may be shortened (narrow exceptions only):**

1. **Explicit opt-out** — User clearly skips discovery and/or previews (e.g. “跳过发现，你全部决定”, “no discovery — just generate”).
2. **Complete written brief** — Same batch already satisfies **every** Phase 1 checklist row **without you guessing**, **and** either (a) a **named preset** is chosen so Phase 2 can be a direct handoff to Phase 3, or (b) the user explicitly allows **no previews** and accepts your single recommended preset.

**Default order:** **Phase 1 (grouped) → Phase 2 (show, don’t tell) → Phase 3.** Never start Phase 3 to “save turns.”

**Partial answers:** Next message = **only** missing Phase 1 items, then resume Phase 2.

**Never infer silence as approval.** **Mode C** (enhance existing HTML): precise change list may skip full Phase 1–2; vague “make it better” → 1–2 clarifying questions first.

**Anti-pattern:** Generating HTML because the skill was attached or because you “already know” a good length or preset — **failure mode**.

Skipping discovery to “save turns” is a failure mode for this skill.
</discovery_gate>

<core_principles>
Core Principles

1. **Zero Dependencies** — Single HTML files with inline CSS/JS. No npm, no build tools.
2. **Show, Don't Tell** — Generate visual previews, not abstract choices. People discover what they want by seeing it.
3. **Distinctive Design** — No generic "AI slop." Every presentation must feel custom-crafted.
4. **Viewport Fitting (NON-NEGOTIABLE)** — Every slide MUST fit exactly within 100vh. No scrolling within slides, ever. Content overflows? Split into multiple slides.
</core_principles>

<design_aesthetics>
Design Aesthetics

You tend to converge toward generic, "on distribution" outputs. In frontend design, this creates what users call the "AI slop" aesthetic. Avoid this: make creative, distinctive frontends that surprise and delight.

Focus on:
- Typography: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics.
- Color & Theme: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw from IDE themes and cultural aesthetics for inspiration.
- Motion: Use **CSS-only** animations and transitions in generated decks (this skill outputs single-file HTML, no React and no Motion library). Focus on high-impact moments: one well-orchestrated load with staggered reveals (`animation-delay`) beats scattered micro-interactions.
- Backgrounds: Create atmosphere and depth rather than defaulting to solid colors. Layer CSS gradients, use geometric patterns, or add contextual effects that match the overall aesthetic.

Avoid generic AI-generated aesthetics:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Cliched color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for the context. Vary between light and dark themes, different fonts, different aesthetics. You still tend to converge on common choices (Space Grotesk, for example) across generations. Avoid this: it is critical that you think outside the box!
</design_aesthetics>

<viewport_fitting_rules>
Viewport Fitting Rules

These invariants apply to EVERY slide in EVERY presentation:

- Every `.slide` must have `height: 100vh; height: 100dvh; overflow: hidden;`
- ALL font sizes and spacing must use `clamp(min, preferred, max)` — never fixed px/rem
- Content containers need `max-height` constraints
- Images: `max-height: min(50vh, 400px)`
- Breakpoints required for heights: 700px, 600px, 500px
- Include `prefers-reduced-motion` support
- Never negate CSS functions directly (`-clamp()`, `-min()`, `-max()` are silently ignored) — use `calc(-1 * clamp(...))` instead

**When generating, read `viewport-base.css` and include its full contents in every presentation.**

Content Density Limits Per Slide

| Slide Type | Maximum Content |
|------------|-----------------|
| Title slide | 1 heading + 1 subtitle + optional tagline |
| Content slide | 1 heading + 4-6 bullet points OR 1 heading + 2 paragraphs |
| Feature grid | 1 heading + 6 cards maximum (2x3 or 3x2) |
| Code slide | 1 heading + 8-10 lines of code |
| Quote slide | 1 quote (max 3 lines) + attribution |
| Image slide | 1 heading + 1 image (max 60vh height) |

**Content exceeds limits? Split into multiple slides. Never cram, never scroll.**
</viewport_fitting_rules>

<quick_start>
<mode_detection>
Phase 0: Detect Mode

Determine what the user wants:

- **Mode A: New Presentation** — Create from scratch. Go to Phase 1.
- **Mode B: PPT / PDF conversion** — Convert a `.pptx` or `.pdf` file. Go to Phase 4.
- **Mode C: Enhancement** — Improve an existing HTML presentation. Read it, understand it, enhance. **Follow Mode C modification rules below.**
</mode_detection>

<mode_c_modification_rules>
Mode C: Modification Rules

When enhancing existing presentations, viewport fitting is the biggest risk:

1. **Before adding content:** Count existing elements, check against density limits
2. **Adding images:** Must have `max-height: min(50vh, 400px)`. If slide already has max content, split into two slides
3. **Adding text:** Max 4-6 bullets per slide. Exceeds limits? Split into continuation slides
4. **After ANY modification, verify:** `.slide` has `overflow: hidden`, new elements use `clamp()`, images have viewport-relative max-height, content fits at 1280x720
5. **Proactively reorganize:** If modifications will cause overflow, automatically split content and inform the user. Don't wait to be asked

**When adding images to existing slides:** Move image to new slide or reduce other content first. Never add images without checking if existing content already fills the viewport.
</mode_c_modification_rules>

<phase_1_content_discovery>
Phase 1: Content Discovery (New deck & PPT/PDF path)

**Centralize Phase 1:** For Mode A and for Mode B **after** extraction, deliver the checklist in **one grouped interaction** (see **Discovery gate** above) — not dribbled across many turns. If the user’s first message is incomplete, **only** ask missing items next.

**Do not** jump to style previews or HTML until Phase 1 is satisfied (exceptions: **Discovery gate**).

**Ask ALL discovery questions (1–6 below) in that grouped interaction** when starting from scratch. Use a structured question tool when available; otherwise one concise message:

**Question 1 — Purpose** (header: "Purpose"):
What is this presentation for? Options: Pitch deck / Teaching-Tutorial / Conference talk / Internal presentation

**Question 2 — Length** (header: "Length"):
Approximately how many slides? Options: Short 5-10 / Medium 10-20 / Long 20+

**Question 3 — Content** (header: "Content"):
Do you have content ready? Options: All content ready / Rough notes / Topic only

**Question 4 — Style preference** (header: "Style Pref"):
What visual direction sounds closest as a starting point? Options:
- "Recommend for me" — infer from audience, topic, and content
- "Clean / Professional" — restrained, polished, trustworthy
- "Bold / Experimental" — high-contrast, energetic, surprising
- "Editorial / Warm" — human, crafted, story-forward
- "Technical / Minimal" — precise, structured, product-like
- "I already know the preset" — skip to a direct preset choice

**Question 5 — Editing scope** (header: "Editing"):
Confirm the user wants the **full editable runtime** (default for this skill): object layout, Pages sidebar, undo/redo. If they explicitly want a **minimal read-only** file only, switch to the parent **frontend-slides** skill instead — do not strip the runtime from this skill arbitrarily.

**Question 6 — Assets / images** (header: "Images"):
Will this deck use image files you will provide (folder, uploads, or links)? Options: **No images** (CSS/graphics only) / **Yes — I will provide images** / **Unsure — recommend**

**Question 7 — Mobile adaptation** (header: "Mobile"):
Should this editable deck be adapted for phone use in both portrait and landscape? Options: **Desktop-first only** (recommended; keeps the deck optimized for presenting/editing on desktop) / **Adapt for phone portrait + landscape** (adds mobile-specific CSS hooks, sidebar behavior, and extra viewport verification). This is a required Phase 1 answer for new decks and for PPT/PDF conversions after extraction.

**Language / locale (include in the same grouped message when relevant):** If the deliverable must be monolingual, bilingual, or localized (e.g. CN/EN on the same slides vs two files), ask once here when the user has not already stated it.

If the user has draft content (bullets, doc, outline), ask them to **paste or attach** it in the same turn or immediately after Phase 1.

<image_evaluation>
Step 1.2: Image Evaluation (if images provided)

If **Question 6** was **No images** or the user has not supplied any image files yet → proceed to **Phase 2** after Phase 1 is otherwise complete (you may still ask them to add images later before Phase 3 if they change their mind).

If user provides an image folder (or links) **after** Phase 1 marked images as yes:
1. **Scan** — List all image files (.png, .jpg, .svg, .webp, etc.)
2. **Inspect each image** — Use the host's available image/file viewing capability
3. **Evaluate** — For each: what it shows, USABLE or NOT USABLE (with reason), what concept it represents, dominant colors
4. **Co-design the outline** — Curated images inform slide structure alongside text. This is NOT "plan slides then add images" — design around both from the start (e.g., 3 screenshots → 3 feature slides, 1 logo → title/closing slide)
5. **Confirm the outline in one grouped follow-up** (structured question UI when available): "Does this slide outline and image selection look right?" Options: Looks good / Adjust images / Adjust outline

**Logo in previews:** If a usable logo was identified, embed it (base64) into each style preview in Phase 2 — the user sees their brand styled three different ways.
</image_evaluation>
</phase_1_content_discovery>

<phase_2_style_discovery>
Phase 2: Style Discovery (Show, don’t tell)

**Start only after Phase 1 is complete** (see **Discovery gate**).

**Purpose:** Narrow the aesthetic **visually** — most people can’t name what they want. Use **HTML previews** (and concrete anchors from [STYLE_PRESETS.md](STYLE_PRESETS.md) + repo examples: [examples/generated/presets/](examples/generated/presets/) smoke decks, [examples/editable-deck-reference.html](examples/editable-deck-reference.html) for runtime chrome) so the user picks **direction**, then **preset** or **mix**.

**This is the "show, don't tell" phase.**

<style_preference_first>
Step 2.0: Style Preference First

Start from the **style preference captured in Phase 1**. Before asking the user how they want to choose, give a short recommendation list of **2-4 presets** that best match their preference, audience, and content. Tie names to **STYLE_PRESETS** rows (and, when helpful, “see generated sample `*.html` for slug X”) so choices are grounded, not abstract.

Use this mapping as the starting point:

| Style preference | Suggested presets |
|------|------|
| Recommend for me | Infer from purpose + audience + content, then recommend 2-4 strongest fits |
| Clean / Professional | Bold Signal, Electric Studio, Swiss Modern |
| Bold / Experimental | Creative Voltage, Neon Cyber, Split Pastel |
| Editorial / Warm | Dark Botanical, Vintage Editorial, Paper & Ink |
| Technical / Minimal | Swiss Modern, Terminal Green, Notebook Tabs |
| I already know the preset | Skip recommendation explanation and go straight to preset picking |

Explain the recommendation briefly in concrete terms, for example: audience fit, energy level, brand tone, or content density.

If the user already chose **"I already know the preset"** in Phase 1, skip Step 2.1 and go straight to the preset picker.
</style_preference_first>

<style_path>
Step 2.1: Style Path

Ask how they want to choose (header: "Style"):
- "Pick from recommendations" (recommended) — Choose directly from the suggested presets (still **show** thumbnails or one-liner visual cues from presets when possible)
- "Show me options" — Generate **3** single-slide HTML previews (Step 2.3) to **shrink** the search space before locking a preset
- "I know what I want" — Pick from the full preset list in [STYLE_PRESETS.md](STYLE_PRESETS.md)

**If direct preset name:** Confirm against STYLE_PRESETS, then Phase 3. **If "you choose" from Phase 1:** Default path = recommendations + offer previews before generating.
</style_path>

<mood_selection>
Step 2.2: Mood Selection (Guided Discovery)

Ask (header: "Vibe", multiSelect: true, max 2):
What feeling should the audience have? Options:
- Impressed/Confident — Professional, trustworthy
- Excited/Energized — Innovative, bold
- Calm/Focused — Clear, thoughtful
- Inspired/Moved — Emotional, memorable

Use the user's style preference and recommended preset cluster to steer this question. If the preference already strongly determines the direction, keep the previews within that neighborhood instead of scattering across unrelated aesthetics.
</mood_selection>

<style_previews>
Step 2.3: Generate 3 Style Previews

Based on mood **and the earlier style preference**, generate 3 distinct single-slide HTML previews showing typography, colors, animation, and overall aesthetic. Read [STYLE_PRESETS.md](STYLE_PRESETS.md) for available presets and their specifications.

| Mood | Suggested Presets |
|------|-------------------|
| Impressed/Confident | Bold Signal, Electric Studio, Dark Botanical |
| Excited/Energized | Creative Voltage, Neon Cyber, Split Pastel |
| Calm/Focused | Notebook Tabs, Paper & Ink, Swiss Modern |
| Inspired/Moved | Dark Botanical, Vintage Editorial, Pastel Geometry |

Save previews under a **project-local** scratch folder (e.g. `.claude-design-slide-previews/` or `.design/slide-previews/`) as `style-a.html`, `style-b.html`, `style-c.html`. Each should be self-contained, ~50-100 lines, showing one animated title slide.

Open each preview in the default browser when possible: **macOS** `open path/to/file.html`; **Linux** `xdg-open path/to/file.html`; **Windows** `start path\to\file.html`.

When possible, keep at least **2 of the 3 previews** within the recommended preset family so the user sees relevant variations before they see outliers.
</style_previews>

<user_picks>
Step 2.4: User Picks

Ask (header: "Style"):
Which style preview do you prefer? Options: Style A: [Name] / Style B: [Name] / Style C: [Name] / Mix elements

If "Mix elements", ask for specifics.
</user_picks>
</phase_2_style_discovery>

<phase_3_generate_presentation>
Phase 3: Generate Presentation

Generate the full presentation using content from Phase 1 (text, or text + curated images) and style from Phase 2.

If images were provided, the slide outline already incorporates them from Step 1.2. If not, CSS-generated visuals (gradients, shapes, patterns) provide visual interest — this is a fully supported first-class path.

**Before generating, read these supporting files:**
- [STYLE_PRESETS.md](STYLE_PRESETS.md) — **Authoritative visual spec** for the chosen preset (layout, signature, fonts, colors) — same role as in parent `frontend-slides`
- [editor-runtime.md](editor-runtime.md) — **DOM contract** (`data-slide-object`, `data-oid`, edit layer), history types, snap rules, generator checklist
- [examples/editable-deck-reference.html](examples/editable-deck-reference.html) — **Copy the deck runtime** (editor + sidebar + history + persistence patterns); **do not** treat its slide markup as the only allowed layout
- [html-template.md](html-template.md) — HTML architecture and integration notes
- [viewport-base.css](viewport-base.css) — Mandatory CSS (include in full)
- [animation-patterns.md](animation-patterns.md) — Animation reference for the chosen feeling
- For ported presets, also read local `beautiful-html-templates/templates/{source_slug}/template.html` and `template.json` when available; use `STYLE_PRESETS.md` as the index, but the upstream template as the detailed design grammar.

**Key requirements:**
- Single self-contained HTML file, all CSS/JS inline
- Include the FULL contents of viewport-base.css in the `&lt;style&gt;` block
- **Preset fidelity:** Implement **Layout** and **Signature Elements** from [STYLE_PRESETS.md](STYLE_PRESETS.md) for the selected style. Vary structure slide-to-slide and preset-to-preset; avoid a **single repeated title-slide prototype** across all aesthetics (parent skill does not do that).
- **Ported preset fidelity:** For the 34 ported presets, preserve the upstream template DOM/CSS/classes and make authored content slot-editable. Prefer locked native layout + editable `data-edit-slot` content over making every native element draggable.
- **Every slide** `section.slide` must have a stable `id`; movable content lives in `.slide-edit-layer` as `[data-slide-object][data-oid]` per [editor-runtime.md](editor-runtime.md)
- **Deck slide list:** Never use a global `querySelectorAll('section.slide')` when a filmstrip clones slides — use only slides under the deck wrapper (e.g. `.slides-offset` + `:scope > section.slide`). See [html-template.md](html-template.md) §Regression guard.
- **Mobile adaptation:** If Phase 1 selected phone support, set `data-mobile-adaptation="enabled"` on `<html>` and include portrait + landscape media rules for the deck chrome, sidebar, and slide objects. If not selected, set `data-mobile-adaptation="desktop-default"` so validation can distinguish an explicit desktop-first choice from an omitted decision.
- Embed the **editable deck runtime** (from the reference example): `SlideDeck`, object editor (select / drag / snap / RTE toolbar), `SlideSidebar`, `HistoryStack`, save/export
- Use fonts from Fontshare or Google Fonts — never system fonts
- Add detailed comments explaining each section
- Every section needs a clear `/* === SECTION NAME === */` comment block
</phase_3_generate_presentation>

<phase_4_ppt_conversion>
Phase 4: PPT / PDF conversion

When converting **PowerPoint** (`.pptx`) or **PDF** (`.pdf`) files:

1. **Extract content**
   - **PPTX:** `python3 scripts/extract-pptx.py &lt;input.pptx&gt; &lt;output_dir&gt;` (install **python-pptx** if needed: `pip install python-pptx`)
   - **PDF:** `python3 scripts/extract-pdf.py &lt;input.pdf&gt; &lt;output_dir&gt;` (install **PyMuPDF** if needed: `pip install pymupdf`). Optional: `--raster-if-empty` renders a page to PNG when that page has no extractable text and no embedded images (e.g. scanned-like pages still need separate OCR; this flag only captures a bitmap of the page).
   - Both writers emit the same intermediate: **`extracted-slides.json`** + **`assets/`** (one record per slide/page; PDF has no speaker notes — use `notes: ""`).
2. **Confirm with user** — Present extracted slide/page titles, content summaries, and image counts
3. **Phase 1 (close gaps)** — Extraction supplies **content**, but you still need explicit answers for anything not fixed by the file: **style direction** (or preset/delegate), **full editable vs read-only**, **locale**, **length** intent if merging/splitting slides, and **image** handling on extracted assets. **One grouped follow-up** for missing items only.
4. **Phase 2** — Style discovery (previews / preset pick); see **Phase 2: Style Discovery** in this skill file
5. **Generate HTML** — Convert to chosen style, preserving all text, images (from assets/), slide order; **PPTX:** speaker notes as HTML comments. **PDF:** no notes in source — omit or leave comment placeholders only if the user supplies them separately.

**PDF caveats:** Text reading order and “title vs body” are heuristic; layout is not object-level like PPTX. Image-only PDFs need `--raster-if-empty` or external OCR for usable text.
</phase_4_ppt_conversion>
</quick_start>

<success_criteria>
Phase 5: Delivery

1. **Clean up** — Delete the temporary slide-previews folder (see Phase 2) if it exists
2. **Smoke check (quick)** — Before handing off: open the file once; confirm **no in-slide scrolling** at ~1280×720; if mobile support was selected, also check ~390×844 portrait and ~844×390 landscape; in edit mode, open **Pages**, reorder one slide, **Copy** one slide, add **+New Page**, and refresh — **no duplicate slides or object ids** (regression guard); **Export HTML** opens and runs standalone
3. **Open** — Launch in default browser: **macOS** `open [filename].html`; **Linux** `xdg-open [filename].html`; **Windows** `start [filename].html`
4. **Summarize** — Tell the user:
   - File location, style name, slide count
   - Navigation: Arrow keys, Space, scroll/wheel (wheel disabled while edit mode on), click nav dots
   - **Edit mode:** `E` enters edit mode. **Hover the top-left** to reveal **Edit**, **Pages**, and (while editing) **Undo** / **Redo** / **Done**; controls hide after the pointer leaves (~400ms). **Done** (same cluster) exits edit mode — the **Edit** button label stays **Edit**. **Esc** blurs text first, then exits edit mode when not typing in a text box
   - **Pages** sidebar for thumbnails, reorder (drag rows), hover **Copy** on a thumbnail to duplicate that page, delete slides, and use **+New Page** beside **Export HTML** to insert a blank style-matched page after the current slide
   - **Objects:** drag **⠿** to move; hover **×** on an object or use **Delete/Backspace** to remove (multi-select confirms in English); drag **corner resize** on selected objects to change width/height (text reflows); **Ctrl+click** multi-select (macOS: **Control** key)
   - **Add element:** **Add element** (top-left with Edit/Pages in edit mode) opens a menu: **Text**, **Image** (URL or placeholder), **Video** (URL + controls)
   - **Snap:** aligns to **slide center** and **other objects** — not to the outer slide edges
   - **Text:** click text to type; floating toolbar: **B/I** plus **Font** · **Scale** · **Px** drawers (click to expand cards for families, scale steps, px presets + custom); **Ctrl+Z** / **Ctrl+Y** or **Ctrl+Shift+Z**; **Cmd+Z** / **Cmd+Y** / **Cmd+Shift+Z** on macOS when not typing in `contenteditable`
   - **Save** (`#btnSave`, top-left next to **Edit** / **Pages** when editing — same hover reveal) or **Ctrl+S** / **Cmd+S** saves the full deck structure to localStorage; **Export HTML** remains in the Pages sidebar and should strip transient edit state
   - How to customize: slide theme `:root` variables, **`--deck-chrome-*`** for edit UI (see [STYLE_PRESETS.md](STYLE_PRESETS.md) §Deck chrome tokens), font link, `.reveal` animations; keep `data-oid` unique when adding objects
</success_criteria>

<supporting_files>
Supporting Files

| File | Purpose | When to Read |
|------|---------|-------------|
| [editor-runtime.md](editor-runtime.md) | DOM contract, undo types, snap rules, generator checklist | Phase 3 (before codegen) |
| [examples/editable-deck-reference.html](examples/editable-deck-reference.html) | Working reference: full runtime in one file | Phase 3 (copy/adapt JS/CSS) |
| [STYLE_PRESETS.md](STYLE_PRESETS.md) | 46 curated visual presets with colors, fonts, and signature elements | Phase 2 (style selection) |
| [viewport-base.css](viewport-base.css) | Mandatory responsive CSS — copy into every presentation | Phase 3 (generation) |
| [html-template.md](html-template.md) | HTML structure, integration with editable runtime | Phase 3 (generation) |
| [animation-patterns.md](animation-patterns.md) | CSS/JS animation snippets and effect-to-feeling guide | Phase 3 (generation) |
| [scripts/extract-pptx.py](scripts/extract-pptx.py) | Python script for PPT content extraction | Phase 4 (PPTX) |
| [scripts/extract-pdf.py](scripts/extract-pdf.py) | Python script for PDF page extraction (same JSON shape as PPTX) | Phase 4 (PDF) |
| [README.md](README.md) | Bilingual extended overview, comparison table, troubleshooting | Optional (users / maintainers) |
</supporting_files>
