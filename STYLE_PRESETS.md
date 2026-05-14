# Style Presets Reference

Curated visual styles for Frontend Slides. Each preset is inspired by real design references — no generic "AI slop" aesthetics. **Abstract shapes only — no illustrations.**

**Viewport CSS:** For mandatory base styles, see [viewport-base.css](viewport-base.css). Include in every presentation.

---

## Dark Themes

### 1. Bold Signal

**Vibe:** Confident, bold, modern, high-impact

**Layout:** Colored card on dark gradient. Number top-left, navigation top-right, title bottom-left.

**Typography:**
- Display: `Archivo Black` (900)
- Body: `Space Grotesk` (400/500)

**Colors:**
```css
:root {
    --bg-primary: #1a1a1a;
    --bg-gradient: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%);
    --card-bg: #FF5722;
    --text-primary: #ffffff;
    --text-on-card: #1a1a1a;
}
```

**Signature Elements:**
- Bold colored card as focal point (orange, coral, or vibrant accent)
- Large section numbers (01, 02, etc.)
- Navigation breadcrumbs with active/inactive opacity states
- Grid-based layout for precise alignment

---

### 2. Electric Studio

**Vibe:** Bold, clean, professional, high contrast

**Layout:** Split panel—white top, blue bottom. Brand marks in corners.

**Typography:**
- Display: `Manrope` (800)
- Body: `Manrope` (400/500)

**Colors:**
```css
:root {
    --bg-dark: #0a0a0a;
    --bg-white: #ffffff;
    --accent-blue: #4361ee;
    --text-dark: #0a0a0a;
    --text-light: #ffffff;
}
```

**Signature Elements:**
- Two-panel vertical split
- Accent bar on panel edge
- Quote typography as hero element
- Minimal, confident spacing

---

### 3. Creative Voltage

**Vibe:** Bold, creative, energetic, retro-modern

**Layout:** Split panels—electric blue left, dark right. Script accents.

**Typography:**
- Display: `Syne` (700/800)
- Mono: `Space Mono` (400/700)

**Colors:**
```css
:root {
    --bg-primary: #0066ff;
    --bg-dark: #1a1a2e;
    --accent-neon: #d4ff00;
    --text-light: #ffffff;
}
```

**Signature Elements:**
- Electric blue + neon yellow contrast
- Halftone texture patterns
- Neon badges/callouts
- Script typography for creative flair

---

### 4. Dark Botanical

**Vibe:** Elegant, sophisticated, artistic, premium

**Layout:** Centered content on dark. Abstract soft shapes in corner.

**Typography:**
- Display: `Cormorant` (400/600) — elegant serif
- Body: `IBM Plex Sans` (300/400)

**Colors:**
```css
:root {
    --bg-primary: #0f0f0f;
    --text-primary: #e8e4df;
    --text-secondary: #9a9590;
    --accent-warm: #d4a574;
    --accent-pink: #e8b4b8;
    --accent-gold: #c9b896;
}
```

**Signature Elements:**
- Abstract soft gradient circles (blurred, overlapping)
- Warm color accents (pink, gold, terracotta)
- Thin vertical accent lines
- Italic signature typography
- **No illustrations—only abstract CSS shapes**

---

## Light Themes

### 5. Notebook Tabs

**Vibe:** Editorial, organized, elegant, tactile

**Layout:** Cream paper card on dark background. Colorful tabs on right edge.

**Typography:**
- Display: `Bodoni Moda` (400/700) — classic editorial
- Body: `DM Sans` (400/500)

**Colors:**
```css
:root {
    --bg-outer: #2d2d2d;
    --bg-page: #f8f6f1;
    --text-primary: #1a1a1a;
    --tab-1: #98d4bb; /* Mint */
    --tab-2: #c7b8ea; /* Lavender */
    --tab-3: #f4b8c5; /* Pink */
    --tab-4: #a8d8ea; /* Sky */
    --tab-5: #ffe6a7; /* Cream */
}
```

**Signature Elements:**
- Paper container with subtle shadow
- Colorful section tabs on right edge (vertical text)
- Binder hole decorations on left
- Tab text must scale with viewport: `font-size: clamp(0.5rem, 1vh, 0.7rem)`

---

### 6. Pastel Geometry

**Vibe:** Friendly, organized, modern, approachable

**Layout:** White card on pastel background. Vertical pills on right edge.

**Typography:**
- Display: `Plus Jakarta Sans` (700/800)
- Body: `Plus Jakarta Sans` (400/500)

**Colors:**
```css
:root {
    --bg-primary: #c8d9e6;
    --card-bg: #faf9f7;
    --pill-pink: #f0b4d4;
    --pill-mint: #a8d4c4;
    --pill-sage: #5a7c6a;
    --pill-lavender: #9b8dc4;
    --pill-violet: #7c6aad;
}
```

**Signature Elements:**
- Rounded card with soft shadow
- **Vertical pills on right edge** with varying heights (like tabs)
- Consistent pill width, heights: short → medium → tall → medium → short
- Download/action icon in corner

---

### 7. Split Pastel

**Vibe:** Playful, modern, friendly, creative

**Layout:** Two-color vertical split (peach left, lavender right).

**Typography:**
- Display: `Outfit` (700/800)
- Body: `Outfit` (400/500)

**Colors:**
```css
:root {
    --bg-peach: #f5e6dc;
    --bg-lavender: #e4dff0;
    --text-dark: #1a1a1a;
    --badge-mint: #c8f0d8;
    --badge-yellow: #f0f0c8;
    --badge-pink: #f0d4e0;
}
```

**Signature Elements:**
- Split background colors
- Playful badge pills with icons
- Grid pattern overlay on right panel
- Rounded CTA buttons

---

### 8. Vintage Editorial

**Vibe:** Witty, confident, editorial, personality-driven

**Layout:** Centered content on cream. Abstract geometric shapes as accent.

**Typography:**
- Display: `Fraunces` (700/900) — distinctive serif
- Body: `Work Sans` (400/500)

**Colors:**
```css
:root {
    --bg-cream: #f5f3ee;
    --text-primary: #1a1a1a;
    --text-secondary: #555;
    --accent-warm: #e8d4c0;
}
```

**Signature Elements:**
- Abstract geometric shapes (circle outline + line + dot)
- Bold bordered CTA boxes
- Witty, conversational copy style
- **No illustrations—only geometric CSS shapes**

---

## Specialty Themes

### 9. Neon Cyber

**Vibe:** Futuristic, techy, confident

**Typography:** `Clash Display` + `Satoshi` (Fontshare)

**Colors:** Deep navy (#0a0f1c), cyan accent (#00ffcc), magenta (#ff00aa)

**Signature:** Particle backgrounds, neon glow, grid patterns

---

### 10. Terminal Green

**Vibe:** Developer-focused, hacker aesthetic

**Typography:** `JetBrains Mono` (monospace only)

**Colors:** GitHub dark (#0d1117), terminal green (#39d353)

**Signature:** Scan lines, blinking cursor, code syntax styling

---

### 11. Swiss Modern

**Vibe:** Clean, precise, Bauhaus-inspired

**Typography:** `Archivo` (800) + `Nunito` (400)

**Colors:** Pure white, pure black, red accent (#ff3300)

**Signature:** Visible grid, asymmetric layouts, geometric shapes

---

### 12. Paper & Ink

**Vibe:** Editorial, literary, thoughtful

**Typography:** `Cormorant Garamond` + `Source Serif 4`

**Colors:** Warm cream (#faf9f7), charcoal (#1a1a1a), crimson accent (#c41e3a)

**Signature:** Drop caps, pull quotes, elegant horizontal rules

---

## Extended gallery (ported from [beautiful-html-templates](https://github.com/zarazhangrui/beautiful-html-templates))

The extended gallery now covers **all 34** local upstream templates as first-class slot-editable presets. They are generated by `scripts/build-template-port-decks.py` from `beautiful-html-templates/templates/{source_slug}/template.html`; output filenames default to the source slug, except the original seven compatibility aliases: `signal-gold`, `studio-volt`, `monochrome-ledger`, `neo-grid-yellow`, and `vellum-navy`.

**Slot-editable contract:** preserve upstream fonts, CSS variables, slide-level classes, decorative DOM, and layout grids. Mark authored content with `data-edit-slot` (`text`, `image`, `metric`, `table-cell`) and keep ornamental systems locked. The generated sample decks use the shared Swiss/reference runtime plus a locked slot adapter: slots get RTE/Undo/Redo/Save/Export behavior without move/resize handles, while `[data-slide-object][data-oid]` is reserved for user-added freeform objects.

### 13. 8-Bit Orbit

**Vibe:** Pixel-art neon arcade aesthetic on a deep navy void.

**Port source:** `beautiful-html-templates/templates/8-bit-orbit`

**Output slug:** `8-bit-orbit`

**Best for:** Anything that should feel like a CRT screen at 2am: cyberpunk, gaming, web3, indie dev tools, hackathon demos. Just as good for a tech talk that wants to lean into nostalgic-digital craft, a synthwave brand deck, or a creative review that wants to feel like a console.

**Avoid for:** Contexts where the dark neon palette would actively work against the message — quiet institutional finance disclosures, healthcare patient-facing materials, traditional luxury.

**Layout:** Preserve the upstream dark medium-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Tektur` + `Chakra Petch` — boxy display sans paired with technical mono, all unmistakably digital and pixel-flavored

**Colors:** deep navy/black void with neon pink, cyan, and yellow pops; pixel art accents and CRT-monitor energy

**Signature Elements:** Pixel-art neon arcade aesthetic on a deep navy void; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 14. Biennale Yellow

**Vibe:** Solar yellow on warm parchment with deep indigo serif and atmospheric sun-glow gradients.

**Port source:** `beautiful-html-templates/templates/biennale-yellow`

**Output slug:** `biennale-yellow`

**Best for:** Anything that should feel like an art-biennale poster or a museum's annual programme: exhibition decks, arts-institution announcements, design conference brochures, curatorial pitches, literary publications, studio retrospectives. Equally good for any deck wanting Dutch-editorial atmosphere with an unmistakable single-color signature.

**Avoid for:** Decks that need visual punch or saturated multi-color energy — the warm-paper canvas and one-yellow palette are intentionally quiet and atmospheric.

**Layout:** Preserve the upstream light medium-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Instrument Serif` + `Archivo` — transitional Didone-flavored display serif paired with a clean grotesk sans for micro-typography and a mono for tabular data

**Colors:** warm parchment ground with a signature solar-yellow accent, deep indigo navy ink, and a soft peach/ember edge that bleeds out of corner gradients

**Signature Elements:** Solar yellow on warm parchment with deep indigo serif and atmospheric sun-glow gradients; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 15. BlockFrame

**Vibe:** Neobrutalist deck with pastel-neon color blocks and chunky black borders.

**Port source:** `beautiful-html-templates/templates/block-frame`

**Output slug:** `block-frame`

**Best for:** Anything that should feel pop-graphic and design-led: indie SaaS launches, agency credentials, creative reviews, brand redesigns. Also a strong unexpected pick for tech, finance, or research when the speaker wants to land as confident and contemporary rather than buttoned-up.

**Avoid for:** Contexts that require quiet institutional restraint or traditional weight (regulated disclosures, formal legal briefs).

**Layout:** Preserve the upstream light high-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Space Grotesk` + `Inter` — geometric sans display + neutral body, used in heavy weights for a poster-like feel

**Colors:** off-white background with neon pastel blocks (hot pink, sky blue, lime green, golden yellow) framed in heavy black borders

**Signature Elements:** Neobrutalist deck with pastel-neon color blocks and chunky black borders; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 16. Blue Professional

**Vibe:** Cream paper background with electric cobalt blue accents; clean modern professional.

**Port source:** `beautiful-html-templates/templates/blue-professional`

**Output slug:** `blue-professional`

**Best for:** Anything that should feel modern-considered and lightly authoritative: B2B SaaS pitches, consulting deliverables, advisory updates, investor reports. Also a clean, tasteful choice whenever you want to read as professional without going stiff — research synthesis, internal reviews, brand work for service businesses.

**Avoid for:** Contexts where the deck should feel hot, playful, or intentionally informal — the cool electric-blue restraint will read as overly polished.

**Layout:** Preserve the upstream light medium-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Space Grotesk` + `Inter` — modern sans pairing; quiet, professional, no decorative flourishes

**Colors:** warm cream paper background with one electric cobalt blue accent; restrained ink black text and soft muted greys

**Signature Elements:** Cream paper background with electric cobalt blue accents; clean modern professional; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 17. Bold Poster

**Vibe:** Editorial poster aesthetic with massive Shrikhand display and a single fire-engine red accent.

**Port source:** `beautiful-html-templates/templates/bold-poster`

**Output slug:** `bold-poster`

**Best for:** Anything that should land like a magazine cover: brand manifestos, founder vision decks, editorial / cultural pitches, creative reviews. Excellent any time you want a few words to feel like a poster — including unexpected fits like a tech keynote or a finance manifesto that wants to be quotable.

**Avoid for:** Decks that need to communicate dense information per slide — the layout is built around a few large statements, not paragraphs of detail.

**Layout:** Preserve the upstream light low-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Shrikhand` + `Space Grotesk` — groovy display + editorial serif + grotesk body; very high typographic contrast

**Colors:** white and warm-cream paper with deep almost-black ink, lifted by a single saturated fire-engine red

**Signature Elements:** Editorial poster aesthetic with massive Shrikhand display and a single fire-engine red accent; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 18. Broadside

**Vibe:** Dark editorial canvas with a single fire orange accent and bilingual Latin/Chinese type stack.

**Port source:** `beautiful-html-templates/templates/broadside`

**Output slug:** `broadside`

**Best for:** Anything that should land like a broadside newspaper headline: brand manifestos, magazine and cultural pitches, design talks, bilingual EN/CN decks, founder vision statements. Also a striking pick for tech, research, or business decks that want a dramatic single-accent editorial feel.

**Avoid for:** Decks that need to feel quiet, warm, or institutionally traditional — the dark canvas with fire-orange accent commits to drama.

**Layout:** Preserve the upstream dark medium-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Barlow` + `Barlow` — broadside-newspaper grotesk pairing with technical mono captions and Simplified Chinese support

**Colors:** near-black newspaper canvas with warm cream text and a single fire-orange headline accent; high typographic contrast, no decorative color

**Signature Elements:** Dark editorial canvas with a single fire orange accent and bilingual Latin/Chinese type stack; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 19. Capsule

**Vibe:** Modular pill-shaped cards on warm bone with a full pastel-pop palette.

**Port source:** `beautiful-html-templates/templates/capsule`

**Output slug:** `capsule`

**Best for:** Anything that should feel modular, modern, and a little Y2K: lifestyle brands, creator portfolios, DTC launches, beauty / wellness, agency credentials. Also fun for a playful tech demo or a research deck that wants pop-art clarity instead of gravitas.

**Avoid for:** Contexts that require traditional institutional weight — the capsule shapes and pastel pops actively soften authority.

**Layout:** Preserve the upstream light medium-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Bodoni Moda` + `Space Grotesk` — high-contrast didone serif paired with a friendly geometric sans

**Colors:** warm bone background, ink-black structure, and a full pastel-pop palette (coral, lime, lavender, sky, violet, yellow, peach, mint) used as flat capsule shapes

**Signature Elements:** Modular pill-shaped cards on warm bone with a full pastel-pop palette; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 20. Cartesian

**Vibe:** Quiet warm-neutral palette with classical Playfair serifs; tasteful and unhurried.

**Port source:** `beautiful-html-templates/templates/cartesian`

**Output slug:** `cartesian`

**Best for:** Anything that should feel quiet, considered, and grown-up: investment theses, white papers, advisory work, longform research, gallery / cultural decks. Also a strong choice for editorial features, founder reflections, or any deck where restraint is the message — including across tech and finance.

**Avoid for:** Decks that need visual heat, multiple accents, or a sense of urgency — the warm-neutral palette is intentionally low-energy.

**Layout:** Preserve the upstream light low-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Playfair Display` + `Inter` — transitional serif headlines paired with a clean grotesk; reads like a Sunday newspaper essay

**Colors:** warm bone and stone neutrals only; no saturated color; the entire system runs on tonal contrast and typography

**Signature Elements:** Quiet warm-neutral palette with classical Playfair serifs; tasteful and unhurried; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 21. Cobalt Grid

**Vibe:** Electric cobalt italic serifs on a graph-paper canvas, anchored by stair-stepped pixel-glitch decorations and slim hairline rules.

**Port source:** `beautiful-html-templates/templates/cobalt-grid`

**Output slug:** `cobalt-grid`

**Best for:** Anything that should feel like a quietly serious design / research bulletin, art publication, or curated trend report. Strong for studio annuals, agency capabilities decks, design-research publications, architecture / art / academic decks, and any deck wanting one strict accent colour and a printed-ledger calmness rather than corporate polish.

**Avoid for:** Decks that need warmth, multi-colour energy, or a casual / playful voice — the strict cobalt + cream + grid palette is intentionally austere.

**Layout:** Preserve the upstream light medium-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Newsreader (italic)` + `Hanken Grotesk` — transitional italic serif for hero type and section heads, paired with a neutral grotesk for body and a clean mono for tabular data and micro-captions; strictly cobalt-on-cream

**Colors:** warm cream / ivory paper canvas with one strict accent of electric cobalt royal blue. The grid is a faint cobalt overlay, and decorations (pixel stair-blocks, QR-style mini-grids, hairline rules) all use the same blue, keeping the deck strictly bichromatic

**Signature Elements:** Electric cobalt italic serifs on a graph-paper canvas, anchored by stair-stepped pixel-glitch decorations and slim hairline rules; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 22. Coral

**Vibe:** Cream and coral on near-black, set in oversized Bebas Neue.

**Port source:** `beautiful-html-templates/templates/coral`

**Output slug:** `coral`

**Best for:** Anything that should feel warm-graphic and editorial: fashion, beauty, fitness, F&B, lifestyle brands, agency credentials. Just as strong for a creator portfolio, a manifesto, or a tech / research deck that wants warmth and a single bold accent instead of corporate cool.

**Avoid for:** Contexts that should feel quiet or institutional — the coral accent and oversized Bebas Neue commit hard to a confident magazine voice.

**Layout:** Preserve the upstream mixed medium-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Bebas Neue` + `Inter` — tall condensed display sans for shouty headlines + neutral body for everything else

**Colors:** near-black canvas, warm cream paper for content, and a saturated coral accent that carries the entire personality

**Signature Elements:** Cream and coral on near-black, set in oversized Bebas Neue; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 23. Creative Mode

**Vibe:** Cream paper canvas with confident multi-color (green, pink, orange, yellow) accents and Archivo Black display.

**Port source:** `beautiful-html-templates/templates/creative-mode`

**Output slug:** `creative-mode`

**Best for:** Anything that should feel design-led and confident: creative agency pitches, design studio decks, ad shop credentials, brand creative reviews, art-direction reviews. Also a great unexpected pick for a tech talk, research findings, or finance review when the speaker wants to lead with taste rather than convention.

**Avoid for:** Contexts that demand institutional restraint and a quiet authority — the saturated multi-accent palette will read as expressive, not formal.

**Layout:** Preserve the upstream light medium-high-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Archivo Black` + `Space Grotesk` — ultra-heavy poster sans + clean grotesk + technical mono

**Colors:** warm cream paper background with a saturated multi-accent palette (forest green, hot pink, orange, mustard yellow) on ink-black structure

**Signature Elements:** Cream paper canvas with confident multi-color (green, pink, orange, yellow) accents and Archivo Black display; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 24. Daisy Days

**Vibe:** Cheerful pastel deck with hand-drawn daisies, stars, and rainbows. Friendly, soft, and warm.

**Port source:** `beautiful-html-templates/templates/daisy-days`

**Output slug:** `daisy-days`

**Best for:** Anything that should feel friendly, soft, and joyful: educational content, kids and family, wellness programs, community workshops, creator portfolios for craft / illustration. Also lovely for an unexpected playful internal kickoff, a wedding planning deck, or any moment where warmth is the message — including across tech or business contexts.

**Avoid for:** Contexts where the audience explicitly expects authority and precision — the hand-drawn pastel SVG decorations are the opposite of buttoned-up.

**Layout:** Preserve the upstream light medium-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Fredoka One` + `Quicksand` — rounded sans display + friendly geometric sans body; warm and informal

**Colors:** warm cream base with a full pastel rainbow (mint, lavender, peach, sky, soft pink, butter, turquoise, coral) and ink-black 3px outlines plus chunky 6px offset shadows

**Signature Elements:** Cheerful pastel deck with hand-drawn daisies, stars, and rainbows. Friendly, soft, and warm; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 25. Editorial Forest

**Vibe:** Forest green, dusty pink, and warm cream meet Source Serif 4 in a quiet, intentional quarterly-review deck.

**Port source:** `beautiful-html-templates/templates/editorial-forest`

**Output slug:** `editorial-forest`

**Best for:** Anything that should feel like a considered editorial — quarterly reviews, internal readouts, studio updates, creative-agency presentations. Equally good for any deck that wants to feel warm and unhurried rather than corporate, including research recaps, book or program announcements, and team retrospectives.

**Avoid for:** Contexts that need to feel urgent, punchy, or sales-driven — the palette and rhythm are intentionally quiet.

**Layout:** Preserve the upstream mixed medium-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Template display font` + `Template body font` — humanist editorial serif with a technical mono for kickers and labels; restrained typographic hierarchy

**Colors:** deep forest green, dusty pink, and warm cream paper; quiet tri-tone that pairs a saturated dark with two soft accents

**Signature Elements:** Forest green, dusty pink, and warm cream meet Source Serif 4 in a quiet, intentional quarterly-review deck; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 26. Editorial Tri-Tone

**Vibe:** Three-color editorial system: dusty pink, mustard cream, and deep burgundy, set in Bricolage + Instrument Serif.

**Port source:** `beautiful-html-templates/templates/editorial-tri-tone`

**Output slug:** `editorial-tri-tone`

**Best for:** Anything that should feel like a fashion-magazine spread: editorial pitches, fashion brand decks, lifestyle media, art direction reviews. Equally good for any deck — including tech, research, or business — that wants tri-tone discipline and serif/sans contrast instead of the usual neutrals.

**Avoid for:** Decks that need to read as soft or comforting — the burgundy/pink/cream tri-tone is intentionally high-contrast and styled.

**Layout:** Preserve the upstream mixed medium-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Bricolage Grotesque` + `Template body font` — expressive variable grotesk + literary serif + technical mono; magazine-page typographic system

**Colors:** dusty pink, mustard cream, and deep burgundy used as full-bleed color blocks; very high contrast tri-tone with no fourth color

**Signature Elements:** Three-color editorial system: dusty pink, mustard cream, and deep burgundy, set in Bricolage + Instrument Serif; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 27. Emerald Editorial

**Vibe:** A magazine-cover business deck: emerald + navy + paper, double-rule masthead ornaments, and a bold Bodoni-style display serif.

**Port source:** `beautiful-html-templates/templates/emerald-editorial`

**Output slug:** `emerald-editorial`

**Best for:** Anything that should feel like the front of a serious magazine, including but not limited to leadership readouts, planning-office reviews, and strategy briefings. The double-rule masthead ornament gives it editorial gravitas without making it stiff — also a great unexpected pick for product launches or research recaps that want to feel considered rather than corporate.

**Avoid for:** Contexts that need to read as quiet, neutral, or institutionally restrained — the emerald field is too saturated to disappear into the background.

**Layout:** Preserve the upstream mixed medium-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Bodoni Moda` + `Template body font` — heavy Bodoni-style display serif paired with a wide geometric sans for chrome and body

**Colors:** vivid emerald green field, deep navy ink, and warm paper cream; high-saturation magazine-cover palette grounded by the navy

**Signature Elements:** A magazine-cover business deck: emerald + navy + paper, double-rule masthead ornaments, and a bold Bodoni-style display serif; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 28. Grove

**Vibe:** Forest-green canvas with cream type, classical Playfair serifs, and a single rust accent.

**Port source:** `beautiful-html-templates/templates/grove`

**Output slug:** `grove`

**Best for:** Anything that should feel organic, considered, and grown-up: sustainability and wellness brands, outdoor / nature products, wineries and restaurants, literary or arts decks, advisory deliverables, bilingual EN/CN reports. Also a calm, distinctive choice for tech, research, or business decks that want patience over urgency.

**Avoid for:** Decks that need neon energy or rapid-fire pop — the forest-green canvas and Playfair serif commit to a slow, classical voice.

**Layout:** Preserve the upstream mixed medium-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Playfair Display` + `Jost` — transitional serif headlines + clean geometric sans body + technical mono; full Chinese serif/sans support

**Colors:** deep forest green canvas with warm bone type and a single rust-red accent; alternate cream-paper mode for breathing room

**Signature Elements:** Forest-green canvas with cream type, classical Playfair serifs, and a single rust accent; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 29. Long Table

**Vibe:** Warm cream and rust-red supper-club aesthetic with bold uppercase grotesk headlines, italic Fraunces, and pill-shaped outlined buttons.

**Port source:** `beautiful-html-templates/templates/long-table`

**Output slug:** `long-table`

**Best for:** Anything that should feel like a warm, intimate, modern hospitality / community brand: supper clubs, dinner series, small restaurants, creative-studio events, membership pitches, lifestyle and wine brands. Equally good for any deck wanting a single warm accent colour, italic-meets-bold typography, and a social-media-aware modern-editorial voice.

**Avoid for:** Decks that need corporate polish, technical density, or a cold / minimalist register — the rust-red palette and bold-italic mix are intentionally warm and people-facing.

**Layout:** Preserve the upstream light medium-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Bricolage Grotesque` + `Fraunces (italic + roman)` — bold uppercase Bricolage Grotesque for hero / chapter titles paired with Fraunces italic for body, captions, button labels, and tagline — a contemporary mix-and-match modern editorial pairing

**Colors:** warm buttery-cream paper with one strict rust-red / terracotta ink used for type, pill borders, and outlined info cards — strictly bichromatic, very social-media friendly

**Signature Elements:** Warm cream and rust-red supper-club aesthetic with bold uppercase grotesk headlines, italic Fraunces, and pill-shaped outlined buttons; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 30. Mat

**Vibe:** Dark sage canvas with bone paper and burnt-orange accent; mid-century modern with wood undertones.

**Port source:** `beautiful-html-templates/templates/mat`

**Output slug:** `mat`

**Best for:** Anything that should feel mid-century, tactile, and intentional: design studio credentials, architecture / interior brands, ceramics / craft / furniture, advisory decks. Also a warm, distinctive choice for tech, research, or business decks that want a considered analog feel instead of digital-cool.

**Avoid for:** Contexts that need fast tech energy or institutional restraint — the muted sage and burnt-orange palette is intentionally warm and slow.

**Layout:** Preserve the upstream mixed medium-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Bricolage Grotesque` + `DM Sans` — expressive variable grotesk display + clean DM body + DM Mono captions

**Colors:** muted sage green canvas with warm bone paper and a saturated burnt-orange accent; an underlying wood tone for tactile detail

**Signature Elements:** Dark sage canvas with bone paper and burnt-orange accent; mid-century modern with wood undertones; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 31. Monochrome

**Vibe:** Ivory ledger paper with all-black type; Lora serif headlines, Jost body, no color at all.

**Port source:** `beautiful-html-templates/templates/monochrome`

**Output slug:** `monochrome-ledger`

**Best for:** Anything that should feel like a hand-typeset ledger: user research synthesis, white papers, longform reports, academic and policy briefs, advisory deliverables, bilingual EN/CN reports. Equally good for tech, design, or brand decks that want their words to be the only thing on the page.

**Avoid for:** Decks that need visual personality or color-led storytelling — the all-ink palette is intentionally austere.

**Layout:** Preserve the upstream light high-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Lora` + `Jost` — literary serif headlines + clean geometric sans body + technical mono; reads like a hand-typeset ledger

**Colors:** ivory and pale-cream paper with deep ink-black type only; no color at all; the system runs on typography, line, and white space

**Signature Elements:** Ivory ledger paper with all-black type; Lora serif headlines, Jost body, no color at all; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 32. Neo-Grid Bold

**Vibe:** Editorial neo-brutalism with a single neon yellow accent on off-white paper.

**Port source:** `beautiful-html-templates/templates/neo-grid-bold`

**Output slug:** `neo-grid-yellow`

**Best for:** Anything that should feel confident and editorial-graphic: design-led pitches, brand work, founder talks, conference keynotes. Excellent for stat-heavy slides, comparisons, and process flows. Just as strong for tech, research, or finance when the speaker wants to read as design-led rather than corporate.

**Avoid for:** Contexts that need to feel quiet, traditional, or warm — the neon-yellow accent and uppercase display commit to a confident editorial voice.

**Layout:** Preserve the upstream light high-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Space Grotesk` + `Space Grotesk` — geometric sans paired with technical mono captions; uppercase display weight

**Colors:** off-white paper background, ink black, signature neon yellow accent used sparingly

**Signature Elements:** Editorial neo-brutalism with a single neon yellow accent on off-white paper; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 33. People's Platform (Block & Bold)

**Vibe:** Activist poster energy: blue, orange, red on cream, with Alfa Slab + Caveat Brush.

**Port source:** `beautiful-html-templates/templates/peoples-platform`

**Output slug:** `peoples-platform`

**Best for:** Anything that should feel honest, loud, and graphic: cultural commentary, manifestos, civic and community decks, design talks, campaign pitches. Excellent for founder-vision moments, mission statements, or any deck — including across industries — that wants protest-poster energy instead of corporate polish.

**Avoid for:** Contexts where institutional restraint is the actual goal — the saturated political-poster palette commits hard to expressive energy.

**Layout:** Preserve the upstream light medium-high-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Alfa Slab One` + `Template body font` — heavy slab display + narrow grotesk + brush script + mono; protest-poster typographic stack

**Colors:** saturated political-poster palette: cobalt blue, signal orange, warning red, on warm cream with deep ink

**Signature Elements:** Activist poster energy: blue, orange, red on cream, with Alfa Slab + Caveat Brush; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 34. Pin & Paper

**Vibe:** Yellow paper with safety-pin illustrations, ink-blue handwritten Caveat, paper-grain texture.

**Port source:** `beautiful-html-templates/templates/pin-and-paper`

**Output slug:** `pin-and-paper`

**Best for:** Anything that should feel hand-crafted, warm, and literary: qualitative research findings, founder reflections, longform brand stories, workshop debriefs. The signature safety-pin illustrations and paper-grain texture make it especially good for any deck — including tech or business — that wants personality and warmth over polish.

**Avoid for:** Decks that need to feel digital-native polished or rigorously data-driven — handwritten Caveat is intentionally informal.

**Layout:** Preserve the upstream light medium-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Caveat` + `Space Grotesk` — handwritten script for warmth + grotesk for legibility + mono for captions; textbook annotation feel

**Colors:** saturated yellow paper, soft cream alternate, deep ink-blue type, plus rust red, kraft, and olive accents; visible paper grain texture

**Signature Elements:** Yellow paper with safety-pin illustrations, ink-blue handwritten Caveat, paper-grain texture; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 35. Pink Script — After Hours

**Vibe:** Black canvas, hot pink accent, pearl-cream paper, Instrument Serif headlines: late-night editorial luxury.

**Port source:** `beautiful-html-templates/templates/pink-script`

**Output slug:** `pink-script`

**Best for:** Anything that should feel nocturnal, intentional, and a little luxe: fashion brand decks, creator personal brands, after-hours / nightlife / spirits launches, luxury product reveals, editorial features. Also a striking unexpected pick for a tech keynote, research synthesis, or business pitch that wants to land with magnetic confidence.

**Avoid for:** Daytime corporate-professional and traditional B2B contexts where the dark canvas with hot-pink accent reads as too styled or too expressive.

**Layout:** Preserve the upstream dark low-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Instrument Serif` + `Inter` — sharp transitional serif headlines + clean sans body + technical mono labels

**Colors:** near-black canvas with one saturated hot pink accent and a pearl-cream paper for content; the whole system runs on a single accent + restraint

**Signature Elements:** Black canvas, hot pink accent, pearl-cream paper, Instrument Serif headlines: late-night editorial luxury; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 36. Playful

**Vibe:** Sun-warm peach background with Syne display: a friendly indie launch deck.

**Port source:** `beautiful-html-templates/templates/playful`

**Output slug:** `playful`

**Best for:** Anything that should feel warm, indie, and approachable: creator portfolios, indie product launches, lifestyle brands, small-business pitches, newsletter / community decks. Also welcoming for any deck — including tech or research — that wants to feel friendly and human rather than corporate.

**Avoid for:** Contexts where institutional credibility matters more than warmth — the peach palette is intentionally informal.

**Layout:** Preserve the upstream light medium-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Syne` + `Space Grotesk` — geometric variable display with personality + clean grotesk body

**Colors:** warm peach / sand backgrounds with ink-black structure and lighter cream cards; single warm temperature throughout

**Signature Elements:** Sun-warm peach background with Syne display: a friendly indie launch deck; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 37. Raw Grid

**Vibe:** Neo-brutalist deck with thick borders, offset shadows, and a pink/sage/ink palette.

**Port source:** `beautiful-html-templates/templates/raw-grid`

**Output slug:** `raw-grid`

**Best for:** Anything that should feel direct and graphic-confident: founder pitches, accelerator demos, brand decks, indie launches, creator portfolios. Strong for stat slides, comparison tables, and process flows. Equally good for tech, research, or finance when the speaker wants the deck to feel scrappy-confident rather than buttoned-up.

**Avoid for:** Contexts that need to feel soft, warm, or intentionally quiet — the brutalist borders and offset shadows commit to a graphic voice.

**Layout:** Preserve the upstream light high-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Segoe UI / system-ui` + `Segoe UI / system-ui` — system sans set in heavy weights with strong uppercase tracking; functional rather than expressive

**Colors:** white background with ink-black structure, soft pink and sage green as flat color blocks, hard 3px borders and 6px offset shadows

**Signature Elements:** Neo-brutalist deck with thick borders, offset shadows, and a pink/sage/ink palette; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 38. Retro Windows

**Vibe:** Windows 95 chrome: gray title bars, MS Sans Serif, pixel typography, full nostalgia.

**Port source:** `beautiful-html-templates/templates/retro-windows`

**Output slug:** `retro-windows`

**Best for:** Anything that should feel knowingly nostalgic: retro gaming, Y2K-aesthetic brands, creator portfolios with a 90s vibe, tech-history talks, deliberately tongue-in-cheek decks. A great choice anywhere a playful retro reference is the entire point.

**Avoid for:** Decks that need to read as modern, elegant, or institutionally credible — the Win95 chrome will always read as a costume.

**Layout:** Preserve the upstream light medium-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Press Start 2P` + `MS Sans Serif` — 8-bit pixel display + Microsoft system sans + DOS terminal mono

**Colors:** Windows 95 system palette: 3D-button gray, navy title bars, pixel-perfect inset/outset borders, no anti-aliasing aesthetic

**Signature Elements:** Windows 95 chrome: gray title bars, MS Sans Serif, pixel typography, full nostalgia; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 39. Retro Zine

**Vibe:** Beige paper with green accent and Bebas Neue + Caveat: a riso-printed zine in HTML form.

**Port source:** `beautiful-html-templates/templates/retro-zine`

**Output slug:** `retro-zine`

**Best for:** Anything that should feel printed, lo-fi, and crafted: indie zines and publications, music / arts brands, creator portfolios, small-batch craft launches, community decks. Also a great underdog choice for tech, research, or business decks that want a riso-print warmth instead of digital polish.

**Avoid for:** Contexts that demand digital-native polish or fast modern-tech energy — the layered zine aesthetic intentionally feels handmade.

**Layout:** Preserve the upstream light medium-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Bebas Neue` + `Space Grotesk` — tall condensed display + handwritten script + clean grotesk body; layered like a printed zine page

**Colors:** warm beige / khaki paper with one saturated forest green; dark ink and off-white cream; reads like a two-color riso print

**Signature Elements:** Beige paper with green accent and Bebas Neue + Caveat: a riso-printed zine in HTML form; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 40. Sakura Chroma

**Vibe:** Vintage Japanese cassette-package aesthetic: cream paper, diagonal rainbow ribbons, condensed bold type, JIS-style spec checkboxes.

**Port source:** `beautiful-html-templates/templates/sakura-chroma`

**Output slug:** `sakura-chroma`

**Best for:** Anything that should feel like a vintage Japanese cassette package or a TDK / Sony / Sakura Color product catalogue: indie hardware brand decks, music-label release schedules, analog studio retrospectives, zine and magazine pitches, kawaii-tech product launches, creative-studio annual reports. Equally good for any deck wanting bold colour, condensed display type, and a tactile printed-product personality.

**Avoid for:** Decks that need restrained, corporate, or quiet typography — the bold condensed lockups, ribbon stripes, and primary-colour palette are intentionally loud and product-page-y.

**Layout:** Preserve the upstream light medium-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Big Shoulders Display` + `Albert Sans` — condensed black grotesk display in red and brown for hero type, paired with a clean modern sans for body and a mono for spec-sheet listings; Japanese kanji used as decorative micro-type

**Colors:** warm cream paper canvas with dark warm-brown ink and a six-colour primary palette (red, pink, orange, yellow, green, blue) used as bold flat blocks, ribbons, and product-strip accents

**Signature Elements:** Vintage Japanese cassette-package aesthetic: cream paper, diagonal rainbow ribbons, condensed bold type, JIS-style spec checkboxes; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 41. Scatterbrain

**Vibe:** Post-it inspired: pastel sticky notes, Caveat handwriting, Shrikhand and Zilla Slab type stack.

**Port source:** `beautiful-html-templates/templates/scatterbrain`

**Output slug:** `scatterbrain`

**Best for:** Anything that should feel like a designer's whiteboard: brainstorms, workshops, creative-agency credentials, design-thinking sessions, ideation pitches, art-direction reviews. Equally fun for any deck — including tech, research, or business — that wants to read as in-progress thinking rather than polished conclusions.

**Avoid for:** Contexts that demand precision and institutional weight — the post-it sticky-note aesthetic intentionally reads as warm and unfinished.

**Layout:** Preserve the upstream light high-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Shrikhand` + `Zilla Slab` — groovy display + handwritten script + warm slab body; reads like a designer's whiteboard

**Colors:** off-white paper with a full pastel sticky-note palette (yellow, blue, pink, green, orange, purple) and ink-brown text; soft drop shadows everywhere

**Signature Elements:** Post-it inspired: pastel sticky notes, Caveat handwriting, Shrikhand and Zilla Slab type stack; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 42. Signal

**Vibe:** Deep navy canvas with bone paper and a single muted-gold accent; institutional with quiet weight.

**Port source:** `beautiful-html-templates/templates/signal`

**Output slug:** `signal-gold`

**Best for:** Anything that should feel weighty, considered, and credibly institutional: investor decks, board presentations, consulting deliverables, legal / policy briefs, advisory pitches. Also a strong choice for tech, research, or brand work that wants to read as quietly authoritative rather than loud.

**Avoid for:** Contexts that should feel hot, fast, or intentionally playful — the navy + gold restraint commits to a sober voice.

**Layout:** Preserve the upstream mixed high-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Source Serif 4` + `DM Sans` — transitional serif headlines + clean sans body + technical mono captions; full Chinese serif/sans support

**Colors:** deep navy primary with warm bone paper alternate and a single muted-gold accent; restrained, institutional, no decorative color

**Signature Elements:** Deep navy canvas with bone paper and a single muted-gold accent; institutional with quiet weight; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 43. Soft Editorial

**Vibe:** Cormorant Garamond serif on warm paper with sage, blush, and lemon accents.

**Port source:** `beautiful-html-templates/templates/soft-editorial`

**Output slug:** `soft-editorial`

**Best for:** Anything that should feel literary, elegant, and unhurried: editorial features, longform brand stories, gallery / museum decks, advisory deliverables, wedding / lifestyle media, founder essays. Equally good for tech, research, or business decks that want a Sunday-supplement warmth instead of corporate polish.

**Avoid for:** Decks that need visual heat or punch — the warm-paper palette and Cormorant serif are intentionally quiet.

**Layout:** Preserve the upstream light low-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Cormorant Garamond` + `Work Sans` — high-contrast garalde serif headlines paired with a clean humanist sans body

**Colors:** warm paper canvas with deep ink type, accented by soft pink, lemon, blush, and sage; reads like a Sunday editorial spread

**Signature Elements:** Cormorant Garamond serif on warm paper with sage, blush, and lemon accents; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 44. Stencil & Tablet

**Vibe:** Bone paper with stencil-cut headlines and a six-color earth palette: archaeology meets brand.

**Port source:** `beautiful-html-templates/templates/stencil-tablet`

**Output slug:** `stencil-tablet`

**Best for:** Anything that should feel archival, tactile, and weighty-graphic: museum and cultural-institution decks, art / architecture brands, longform research, heritage and craft brands, manifestos. A great choice anytime — including across tech and business — when you want the deck to feel like a field manual rather than a slide deck.

**Avoid for:** Contexts that demand digital-native polish or playful pop — the stencil-cut display and earth-tone palette commit to a deliberate analog feel.

**Layout:** Preserve the upstream light medium-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Bowlby One` + `Inter` — ultra-heavy display + stencil + tall condensed + clean body; reads like an archaeological field manual

**Colors:** warm bone and paper neutrals with a saturated earthy palette (sienna, magenta, orange, teal, blue, olive) used in stencil-cut blocks

**Signature Elements:** Bone paper with stencil-cut headlines and a six-color earth palette: archaeology meets brand; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 45. Studio

**Vibe:** Black canvas with electric-yellow type; high-voltage design studio aesthetic.

**Port source:** `beautiful-html-templates/templates/studio`

**Output slug:** `studio-volt`

**Best for:** Anything that should feel electric and design-led: studio credentials, creative agency pitches, brand showcases, art-direction reviews, fashion / sneaker brand work. Also a striking unexpected choice for tech, research, or business decks where the speaker wants the deck to *be* a brand statement.

**Avoid for:** Contexts that should feel quiet or institutional — the black-and-electric-yellow palette is the loudest in the library.

**Layout:** Preserve the upstream dark medium-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Barlow` + `Barlow` — broadcast-grotesk display + technical mono captions; ultra-high-contrast typographic system

**Colors:** near-black canvas with one signature electric-yellow that doubles as foreground type AND accent; reverses to yellow-paper mode for breathing room

**Signature Elements:** Black canvas with electric-yellow type; high-voltage design studio aesthetic; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

### 46. Vellum

**Vibe:** Deep navy canvas with warm-yellow italic Cormorant serifs and a single dusty teal accent. A quiet, scholarly aesthetic.

**Port source:** `beautiful-html-templates/templates/vellum`

**Output slug:** `vellum-navy`

**Best for:** Anything that should feel scholarly, literary, and quietly intelligent: research synthesis, white papers, academic and policy briefs, advisory deliverables, longform editorial pieces, founder reflections. Equally strong for any deck — including tech, business, or creator work — that wants a calm, considered atmosphere instead of energetic visuals.

**Avoid for:** Contexts that need visual heat or pop — the navy + warm-yellow italic-Cormorant aesthetic is intentionally low-tempo.

**Layout:** Preserve the upstream dark low-density slide grammar, native spacing rhythm, and source slide classes; use locked native slots for authored content.

**Typography:** `Cormorant Garamond Italic` + `DM Sans` — italic transitional serif as the structural display face, paired with clean DM Sans body and Courier Prime mono for attributions and labels; bilingual EN/CN support

**Colors:** deep periwinkle navy canvas with warm yellow italic-serif type and one dusty-teal accent for quote marks; a single coherent palette across every slide, no inverted theme

**Signature Elements:** Deep navy canvas with warm-yellow italic Cormorant serifs and a single dusty teal accent. A quiet, scholarly aesthetic; preserve upstream decorative vocabulary and lock non-content structure.

**Deck chrome:** Map `--deck-chrome-*` from the template palette; keep chrome readable over the native slide background and use the strongest template accent for selection.

---

## Font Pairing Quick Reference

| Preset | Output Slug | Display Font | Body Font | Source |
|--------|-------------|--------------|-----------|--------|
| Bold Signal | bold-signal | Archivo Black | Space Grotesk | Google |
| Electric Studio | electric-studio | Manrope | Manrope | Google |
| Creative Voltage | creative-voltage | Syne | Space Mono | Google |
| Dark Botanical | dark-botanical | Cormorant | IBM Plex Sans | Google |
| Notebook Tabs | notebook-tabs | Bodoni Moda | DM Sans | Google |
| Pastel Geometry | pastel-geometry | Plus Jakarta Sans | Plus Jakarta Sans | Google |
| Split Pastel | split-pastel | Outfit | Outfit | Google |
| Vintage Editorial | vintage-editorial | Fraunces | Work Sans | Google |
| Neon Cyber | neon-cyber | Clash Display | Satoshi | Fontshare |
| Terminal Green | terminal-green | JetBrains Mono | JetBrains Mono | Google |
| Swiss Modern | swiss-modern | Archivo | Nunito | Google |
| Paper & Ink | paper-ink | Cormorant Garamond | Source Serif 4 | Google |
| 8-Bit Orbit | `8-bit-orbit` | Tektur | Chakra Petch | Google / inline CSS |
| Biennale Yellow | `biennale-yellow` | Instrument Serif | Archivo | Google / inline CSS |
| BlockFrame | `block-frame` | Space Grotesk | Inter | Google / inline CSS |
| Blue Professional | `blue-professional` | Space Grotesk | Inter | Google / inline CSS |
| Bold Poster | `bold-poster` | Shrikhand | Space Grotesk | Google / inline CSS |
| Broadside | `broadside` | Barlow | Barlow | Google / inline CSS |
| Capsule | `capsule` | Bodoni Moda | Space Grotesk | Google / inline CSS |
| Cartesian | `cartesian` | Playfair Display | Inter | Google / inline CSS |
| Cobalt Grid | `cobalt-grid` | Newsreader (italic) | Hanken Grotesk | Google / inline CSS |
| Coral | `coral` | Bebas Neue | Inter | Google / inline CSS |
| Creative Mode | `creative-mode` | Archivo Black | Space Grotesk | Google / inline CSS |
| Daisy Days | `daisy-days` | Fredoka One | Quicksand | Google / inline CSS |
| Editorial Forest | `editorial-forest` | Template display | Template body | Google / inline CSS |
| Editorial Tri-Tone | `editorial-tri-tone` | Bricolage Grotesque | Template body | Google / inline CSS |
| Emerald Editorial | `emerald-editorial` | Bodoni Moda | Template body | Google / inline CSS |
| Grove | `grove` | Playfair Display | Jost | Google / inline CSS |
| Long Table | `long-table` | Bricolage Grotesque | Fraunces (italic + roman) | Google / inline CSS |
| Mat | `mat` | Bricolage Grotesque | DM Sans | Google / inline CSS |
| Monochrome | `monochrome-ledger` | Lora | Jost | Google / inline CSS |
| Neo-Grid Bold | `neo-grid-yellow` | Space Grotesk | Space Grotesk | Google / inline CSS |
| People's Platform (Block & Bold) | `peoples-platform` | Alfa Slab One | Template body | Google / inline CSS |
| Pin & Paper | `pin-and-paper` | Caveat | Space Grotesk | Google / inline CSS |
| Pink Script — After Hours | `pink-script` | Instrument Serif | Inter | Google / inline CSS |
| Playful | `playful` | Syne | Space Grotesk | Google / inline CSS |
| Raw Grid | `raw-grid` | Segoe UI / system-ui | Segoe UI / system-ui | Google / inline CSS |
| Retro Windows | `retro-windows` | Press Start 2P | MS Sans Serif | Google / inline CSS |
| Retro Zine | `retro-zine` | Bebas Neue | Space Grotesk | Google / inline CSS |
| Sakura Chroma | `sakura-chroma` | Big Shoulders Display | Albert Sans | Google / inline CSS |
| Scatterbrain | `scatterbrain` | Shrikhand | Zilla Slab | Google / inline CSS |
| Signal | `signal-gold` | Source Serif 4 | DM Sans | Google / inline CSS |
| Soft Editorial | `soft-editorial` | Cormorant Garamond | Work Sans | Google / inline CSS |
| Stencil & Tablet | `stencil-tablet` | Bowlby One | Inter | Google / inline CSS |
| Studio | `studio-volt` | Barlow | Barlow | Google / inline CSS |
| Vellum | `vellum-navy` | Cormorant Garamond Italic | DM Sans | Google / inline CSS |

---

## Deck chrome tokens (editable runtime)

When you merge [examples/editable-deck-reference.html](examples/editable-deck-reference.html) into a preset, the **slide** can be light or dark; the **edit UI** (top bar, sidebar, RTE, handles) must stay readable. Define these on `:root` **after** slide colors and map them from the preset’s palette — do not paste a single hardcoded slate theme into every file.

**Dark slide decks** (e.g. Bold Signal, Neon Cyber): often reuse semi-opaque navy panels:

```css
:root {
  --deck-chrome-bg: rgba(15, 23, 42, 0.94);
  --deck-chrome-border: rgba(255, 255, 255, 0.14);
  --deck-chrome-text: #e2e8f0;
  --deck-chrome-muted: #94a3b8;
  --deck-chrome-accent: /* pick a high-contrast accent from the preset, e.g. card or accent token */;
  --deck-chrome-shadow: 0 12px 40px rgba(0, 0, 0, 0.45);
  --deck-chrome-surface: rgba(30, 41, 59, 0.92);
}
```

**Light slide decks** (e.g. Electric Studio white panel, Paper & Ink): invert contrast — **dark text on light frosted bar** so icons stay visible over pale backgrounds:

```css
:root {
  --deck-chrome-bg: rgba(255, 255, 255, 0.92);
  --deck-chrome-border: rgba(15, 23, 42, 0.12);
  --deck-chrome-text: #0f172a;
  --deck-chrome-muted: #64748b;
  --deck-chrome-accent: /* preset primary, e.g. blue */;
  --deck-chrome-shadow: 0 12px 40px rgba(15, 23, 42, 0.12);
  --deck-chrome-surface: rgba(241, 245, 249, 0.95);
}
```

**Rule of thumb:** `--deck-chrome-text` must contrast with `--deck-chrome-bg`; `--deck-chrome-accent` is used for selection outline and **Done** — pick a preset accent, not a random neon. **Undo/Redo** icons use `currentColor` → they follow `--deck-chrome-text`.

---

## DO NOT USE (Generic AI Patterns)

**Fonts:** Inter, Roboto, Arial, system fonts as display

**Colors:** `#6366f1` (generic indigo), purple gradients on white

**Layouts:** Everything centered, generic hero sections, identical card grids

**Decorations:** Realistic illustrations, gratuitous glassmorphism, drop shadows without purpose

---

## CSS Gotchas

### Negating CSS Functions

**WRONG — silently ignored by browsers (no console error):**
```css
right: -clamp(28px, 3.5vw, 44px);   /* Browser ignores this */
margin-left: -min(10vw, 100px);      /* Browser ignores this */
```

**CORRECT — wrap in `calc()`:**
```css
right: calc(-1 * clamp(28px, 3.5vw, 44px));  /* Works */
margin-left: calc(-1 * min(10vw, 100px));     /* Works */
```

CSS does not allow a leading `-` before function names. The browser silently discards the entire declaration — no error, the element just appears in the wrong position. **Always use `calc(-1 * ...)` to negate CSS function values.**
