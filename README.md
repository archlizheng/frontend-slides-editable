# Frontend Slides - Editable

一个适用于 Claude Code / Codex 的技能，用来生成惊艳、带动画、单文件的 HTML 演示文稿，并内置浏览器编辑器：可拖拽对象、调整大小、编辑文本、重排页面、本地保存，并导出干净的独立 HTML。

A Claude Code / Codex skill for creating stunning, animation-rich, single-file HTML presentations with a built-in browser editor: drag objects, resize blocks, edit text, reorder slides, save locally, and export a clean standalone HTML.

## 目录 · Table of contents

- [v2.0 更新摘要 · Release 2.0 highlights](#toc-highlights)
- [这个 Skill 是做什么的 · What this does](#toc-what)
- [安装 · Installation](#toc-installation)
- [用法 · Usage](#toc-usage)
- [样式预览图库 · Style preview gallery](#toc-gallery)
- [文档结构 · Documentation map](#toc-docs)
- [依赖要求 · Requirements](#toc-requirements)
- [试用参考 · Try the reference](#toc-try)

<a id="toc-highlights"></a>
## v2.0 更新摘要 · Release 2.0 Highlights

本轮将可编辑运行时与交付体验整体推进到 **2.0**：更强媒体工作流、更顺手的排版工具栏，以及更明确的缩放与导出行为。  
This release bumps the editable runtime and authoring workflow to **2.0**: stronger media workflows, a smoother formatting toolbar, and clearer resize + export behavior.

- **Add element（添加对象）**：编辑模式下可从当前页插入文本 / 图片 / 视频占位，并与撤销栈联动。  
  **Add element**: insert text / image / video placeholders on the current slide from edit mode, wired into undo/redo.

- **图片与视频（Images & video）**：支持本地文件选择、`FileReader` 写入 data URL（单文件自包含）；图片支持剪贴板 **Ctrl+V / ⌘V** 粘贴（非富文本焦点时）；双击已有图/视频可重新选择文件。  
  **Images & video**: pick local files and embed as data URLs (single-file friendly); **paste images** with Ctrl/Cmd+V when not typing in rich text; **double-click** existing media to replace.

- **缩放与媒体框（Resize & media box）**：选中对象后除右下角外，增加**右侧 / 底边**手柄，便于沿单边调整；幻灯片内图片/视频取消不当的 `max-height` 限制，缩放框体时画面会随对象尺寸填满（`object-fit: contain`）。  
  **Resize & media box**: corner handle plus **right and bottom edge** handles; in-slide images/videos no longer clamp to a global `max-height`, so resizing the frame actually scales the visible media (`object-fit: contain`).

- **富文本工具栏（RTE）**：字体 / 字号档位收纳为抽屉；自定义像素字号改为**内联数字输入 + Apply**（避免嵌入环境 `prompt` 不可用）；在工具栏上改字体/字号时会**尽量保留文本选区**。  
  **RTE toolbar**: font / size controls live in drawers; custom px size uses an **inline numeric field + Apply** (no `prompt`); **selection is preserved** when applying font/size from the toolbar where possible.

- **对象与页面（Objects & pages）**：每个对象带删除控件；Pages 删页等有更稳妥的确认与文案；导出 HTML 时会剥离仅编辑器用的上传按钮与 `file` 输入。  
  **Objects & pages**: per-object delete control; safer slide-delete confirmation copy; **export strips** editor-only upload UI and file inputs.

- **预设与构建（Presets & build）**：`STYLE_PRESETS.md` 与 `scripts/build-preset-decks.py` 同步扩展，`examples/generated/presets/` 可由脚本从 `editable-deck-reference.html` 派生自检用整页样例。  
  **Presets & build**: expanded `STYLE_PRESETS.md` + `scripts/build-preset-decks.py`; `examples/generated/presets/` are mechanical smoke-test decks sliced from `examples/editable-deck-reference.html`.

- **与 beautiful-html-templates 已同步的 presets**：自 [beautiful-html-templates](https://github.com/zarazhangrui/beautiful-html-templates) 引入、并在本仓库 **`STYLE_PRESETS.md` 第 13–19 节** 落规格且 **`build-preset-decks.py` 可生成样例** 的共 **7** 套为：**Soft Editorial**、**Signal**、**Studio**、**Monochrome**、**Neo-Grid Bold**、**Vellum**、**Cobalt Grid**（对应 `examples/generated/presets/` 下 `soft-editorial.html`、`signal-gold.html`、`studio-volt.html`、`monochrome-ledger.html`、`neo-grid-yellow.html`、`vellum-navy.html`、`cobalt-grid.html`）。气质与上游模板名对齐；版式与 token 以本仓库文档为准，并非逐文件拷贝 HTML。上游库中**其余**模板尚未在本 skill 内写成预设与构建项。  
  **beautiful-html-templates presets synced here**: **seven** themes from [beautiful-html-templates](https://github.com/zarazhangrui/beautiful-html-templates) are first-class in **`STYLE_PRESETS.md` sections 13–19** and ship as built samples: **Soft Editorial**, **Signal**, **Studio**, **Monochrome**, **Neo-Grid Bold**, **Vellum**, **Cobalt Grid** → `soft-editorial.html`, `signal-gold.html`, `studio-volt.html`, `monochrome-ledger.html`, `neo-grid-yellow.html`, `vellum-navy.html`, `cobalt-grid.html` under `examples/generated/presets/`. Vibes align with upstream template names; layout and tokens are **specified in this repo**, not byte-for-byte copies of upstream HTML. **Other** upstream templates are **not** yet ported as presets here.

参考实现仍以单文件 **`examples/editable-deck-reference.html`** 为契约；生成新 deck 时请继续遵循本仓库 `SKILL.md` 与 `editor-runtime.md`。  
The reference contract remains the single file **`examples/editable-deck-reference.html`**; follow `SKILL.md` and `editor-runtime.md` when generating new decks.

<a id="toc-what"></a>
## 这个 Skill 是做什么的 / What This Does

**Frontend Slides - Editable** 是 **frontend-slides** 的可编辑分支。它保留了原始 skill 的风格探索流程、视口适配规则和 **PPT / PDF** 转换能力，并在此基础上加入完整的浏览器内编辑运行时。**交付用的幻灯片仍应按 `STYLE_PRESETS.md` 实现各预设的布局与签名元素**；可编辑只是增加运行时，不是把多套风格压成同一套版式原型。`examples/generated/presets/` 仅为运行时自检样例。

**Frontend Slides - Editable** is the editable fork of **frontend-slides**. It preserves style discovery, viewport discipline, and **PPT / PDF** conversion from the original skill, then adds a full in-browser editing runtime. **Real decks should still implement each preset’s layout and signature elements from `STYLE_PRESETS.md`** — edit mode is an add-on, not permission to reuse one generic slide prototype for every aesthetic. `examples/generated/presets/` is for runtime smoke tests only.

### 操作演示（1.0 录屏） · Demo screencast (1.0 era)

**中文**：以下为 **1.0 时期**在浏览器中的操作录屏，便于快速感受可编辑运行时；**2.0** 的变更请见上文「v2.0 更新摘要」与下文「样式预览图库」中的静态截图。若 GitHub 页面未内嵌播放视频，请直接打开下方链接在浏览器中观看。  
**English**: This is a **1.0-era** walkthrough (not a full 2.0 feature tour). See **Release 2.0 highlights** above and the **Style preview gallery** screenshots below for **2.0** deltas. If the embedded player does not load, open the URL directly.

https://github.com/user-attachments/assets/dc1db494-5e8c-4bbc-9c4a-d02be74c8e89

它适合“生成后还要继续改”的场景，例如：

It is designed for workflows where the generated output must remain editable:

- 直接在幻灯片上移动对象
- 使用 **Ctrl+点击** 多选
- 调整文本框大小并让文字自动重排
- 对文本进行 **粗体 / 斜体 / 字体 / 字号** 编辑（工具栏抽屉 + 自定义 px；改格式时尽量保留选区）
- 使用 **Undo / Redo**
- 在 **Pages** 侧栏重排或删除页面
- **添加** 文本 / 图片 / 视频对象；图片可本地文件或 **粘贴**；视频可本地文件
- 将完整 deck 结构保存到 `localStorage`
- 导出清理过临时编辑状态的独立 `.html`

- move objects directly on slides
- use **Ctrl+click** multi-select
- resize text blocks with automatic reflow; **edge + corner** handles for media objects
- edit text inline with **bold / italic / font / size** (drawer toolbar + custom px; **selection preserved** when possible)
- use **Undo / Redo**
- reorder and delete slides from the **Pages** sidebar
- **add** text / image / video objects; images via local file or **paste**; video via local file
- persist full deck structure to `localStorage`
- export a sanitized standalone `.html`

如果只需要更轻量的只读输出，请使用父 skill [**frontend-slides**](https://github.com/zarazhangrui/frontend-slides)（仓库见链接）。

If you only need the smallest read-only output, use the parent [**frontend-slides**](https://github.com/zarazhangrui/frontend-slides) skill (repository link).

## Skill 对照表 / Skill Comparison

| 维度 / Dimension | `frontend-slides` | `frontend-slides-editable` |
|------|------|------|
| 核心定位 / Primary job | 生成更轻量的只读 HTML 演示 / Generate lighter read-only HTML decks | 生成可继续编辑的 HTML 演示 / Generate editable HTML decks |
| 输出重量 / Output weight | 更小、更干净 / Smaller and lighter | 更重，但包含完整编辑器 / Heavier, with full editor runtime |
| 样式流程 / Style flow | 依赖父 skill 当前安装版本 / Depends on the installed parent-skill version | 先问样式偏好，再推荐预设，再决定直选或看预览 / Ask style preference first, recommend presets, then choose direct pick or previews |
| 预设表现 / Preset fidelity | 按 `STYLE_PRESETS` 逐套实现版式与签名元素 / Implement layout + signatures per preset | **同上，不得因可编辑而统一成单一首屏模板** / **Same — do not collapse all styles into one title-slide template** |
| 浏览器内编辑 / In-browser editing | 可选文本编辑 / Optional text editing | 默认完整编辑运行时 / Full editing runtime by default |
| 页面管理 / Slide management | 无 Pages 侧栏 / No Pages sidebar | 有缩略图侧栏、重排、删除 / Sidebar with thumbnails, reorder, delete |
| 对象操作 / Object manipulation | 不支持对象级拖拽缩放 / No object-level drag or resize | 支持拖拽、边角/边缘缩放、吸附、多选、添加与删除对象 / Drag, corner/edge resize, snap, multi-select, add & delete objects |
| 历史记录 / Undo and redo | 无完整对象历史 / No full object history | 内置 Undo / Redo / Built-in undo and redo |
| 本地保存 / Local persistence | 仅在启用编辑时保存文本改动 / Save text edits when editing is enabled | 保存完整 deck 结构 / Save full deck structure |
| 适合场景 / Best for | 交付成品、体积敏感、只读展示 / Final delivery, size-sensitive, read-only decks | 评审后继续改稿、团队协作、客户反馈迭代 / Post-review edits, collaboration, iterative feedback |
| 什么时候选它 / When to choose it | 你已经接近定稿 / You are close to final | 你预期还会持续改布局和内容 / You expect continued layout and content changes |

## 核心特性 / Key Features

- **零依赖**：单个 HTML 文件，CSS/JS 内联，无需 npm、构建工具或框架
- **可视化风格探索**：通过预览选风格，而不是抽象描述
- **完整可编辑运行时**：拖拽、多选、边角/边缘缩放、对象删除、**添加**图/文/视频、缩略图侧栏与历史记录
- **PPT / PDF 转换**：将 `.pptx` 或 `.pdf` 抽成与 PPT 相同的中间 JSON（`extracted-slides.json` + `assets/`），再生成可编辑网页幻灯片
- **视口安全**：每一页都要求适配视口，不允许内部滚动
- **持久化与导出**：`Ctrl+S` 保存结构化状态；导出时剥离临时编辑态
- **反模板感**：通过精选风格预设，避免千篇一律

- **Zero dependencies**: Single-file HTML with inline CSS/JS, no npm/build/framework
- **Visual style discovery**: pick by preview, not design jargon
- **Full editable runtime**: drag, multi-select, corner/edge resize, object delete, **add** text/image/video, filmstrip, history
- **PPT / PDF conversion**: extract `.pptx` or `.pdf` to the same intermediate JSON (`extracted-slides.json` + `assets/`), then build editable web slides
- **Viewport-safe output**: every slide must fit the viewport without internal scrolling
- **Persistence + export**: `Ctrl+S` saves structure; export removes transient edit state
- **Anti-generic aesthetics**: curated presets over bland default templates

## 适合什么场景 / When To Use This

适合 **frontend-slides-editable**：

Use **frontend-slides-editable** when you want:

- 生成后仍可在浏览器继续微调
- 支持客户/团队评审后的布局修订
- 单文件、零构建的可交付结果
- PowerPoint / PDF 转网页后继续编辑（PDF 为抽取层 + 再设计版式，非像素级还原）

- a generated deck you can continue refining in browser
- post-generation layout iteration during reviews
- a single-file deliverable with no build step
- PowerPoint- or PDF-to-web conversion with continued editing (PDF: extract-then-redesign, not pixel-perfect layout)

适合 **frontend-slides**：

Use **frontend-slides** when you want:

- 更小更轻的只读输出
- 不需要编辑器界面
- 最轻量的生成文件

- a smaller read-only output
- presentation-only HTML without editor chrome
- the lightest possible generated file

<a id="toc-installation"></a>
## 安装 / Installation

仓库地址：**https://github.com/archlizheng/frontend-slides-editable**

### 方式一：把下面这段话发给 AI（推荐） / Option A: paste this prompt to an AI agent

把下面整段复制给 **Claude Code / Cursor / 任何有 shell 权限的 AI Agent**，由它执行命令完成安装。

Paste the block below to **Claude Code / Cursor / any AI agent with shell access** so it can run the install for you.

```text
帮我安装 frontend-slides-editable 这个 Claude Code / Codex skill。请按下面步骤做：

【Claude Code】
- 确保 ~/.claude/skills/ 目录存在（不存在就创建）
- 若 ~/.claude/skills/frontend-slides-editable 已存在且是旧副本，先删掉该目录或改用 git pull 更新
- 执行：git clone https://github.com/archlizheng/frontend-slides-editable.git ~/.claude/skills/frontend-slides-editable
- 验证：ls ~/.claude/skills/frontend-slides-editable/ 应至少能看到 SKILL.md、examples/、STYLE_PRESETS.md

【Codex】
- 确保 ~/.codex/skills/ 目录存在（不存在就创建）
- 若 ~/.codex/skills/frontend-slides-editable 已存在且是旧副本，先删掉该目录或改用 git pull 更新
- 执行：git clone https://github.com/archlizheng/frontend-slides-editable.git ~/.codex/skills/frontend-slides-editable
- 验证：ls ~/.codex/skills/frontend-slides-editable/ 应至少能看到 SKILL.md、examples/、STYLE_PRESETS.md

只帮我装我实际用的那一套（Claude Code 或 Codex），装好后告诉我已完成；之后我说「做单文件可编辑 HTML 演示」「把 pptx / pdf 转成可继续在浏览器里改的幻灯片」等需求应能触发这个 skill。
```

### 方式二：手动命令行 / Option B: manual shell

**Claude Code**

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/archlizheng/frontend-slides-editable.git ~/.claude/skills/frontend-slides-editable
```

**Codex**

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/archlizheng/frontend-slides-editable.git ~/.codex/skills/frontend-slides-editable
```

若目标目录已存在，请先删除旧目录或进入该目录用 `git pull` 更新，再执行 `git clone`。

If the target folder already exists, remove the old tree or `git pull` inside it before cloning again.

### 本地已有源码时 / When you already have a git clone

在仓库的**父目录**执行（把路径换成你的实际位置）：

From the **parent directory** of your clone (adjust the path):

```bash
cp -r ./frontend-slides-editable ~/.claude/skills/
# 或 / or
cp -r ./frontend-slides-editable ~/.codex/skills/
```

### 调用 / Invoke

安装完成后在对话里使用：

Then invoke with:

```text
/frontend-slides-editable
```

<a id="toc-usage"></a>
## 用法 / Usage

### 新建可编辑演示 / Create a new editable presentation

```text
/frontend-slides-editable

> "帮我做一个关于 AI agents for product teams 的分享"
```

这个 skill 会：

The skill will:

1. **Phase 1（内容发现）— 先集中问齐**：除非用户**同一条消息里**已给齐 **目的、篇幅（页数量级或精确页数）、内容或大纲（非仅主题）、风格偏好方向、是否确认完整可编辑运行时、图片资源意向**，以及需要时的**语言/双语**，否则**一次成组提问**；缺啥就只补问缺失项。**仅调用 `/frontend-slides-editable` 不算答完**。有素材后再做配图评估，并与大纲一起敲定（非「先瞎写页再插图」）。详见 `SKILL.md` 的 **Discovery gate**。
2. **Phase 2（风格发现）— Show, don’t tell**：结合 `STYLE_PRESETS.md` 与仓库内样例（如 `examples/generated/presets/`）缩小范围；推荐 2–4 个预设后，让用户**直选**或**生成预览**再定稿，然后进入生成。
3. 若 Phase 1 确认有图：评估素材并与幻灯片结构共同设计；若无图则跳过图片评估。
4. 产出带编辑运行时的单文件 HTML，并在浏览器中打开。

1. **Phase 1 (content discovery) — batch first:** Unless the user supplies **in one message** **purpose, length band (or exact count), content or outline (not topic-only), style direction, confirmation of full editable runtime vs read-only parent skill, image intent**, and **language/locale** when relevant, send **one grouped Phase 1**; next turn asks **only** missing items. Invoking the skill **does not** satisfy discovery. After assets exist, run image evaluation and **co-design outline ↔ images**. See **Discovery gate** in `SKILL.md`.
2. **Phase 2 (style discovery) — show, don’t tell:** Narrow choices using [STYLE_PRESETS.md](STYLE_PRESETS.md) and repo examples (e.g. `examples/generated/presets/`); recommend presets, then **direct pick** or **HTML previews**, then generate.
3. If Phase 1 says images: evaluate assets and align outline; otherwise skip image evaluation.
4. Build a single-file editable HTML deck and open it in the browser.

### 增强现有 HTML / Enhance an existing HTML deck

```text
/frontend-slides-editable

> "Improve this HTML deck and keep it editable"
```

这个 skill 会：

The skill will:

1. 读取现有演示文稿。
2. 修改前检查内容密度与视口适配。
3. 保护编辑运行时契约（如 `section.slide`、`.slide-edit-layer`、`data-oid`）。
4. 在保持编辑/持久化/导出能力的前提下更新 deck。

1. Read the current deck.
2. Validate density and viewport fit before edits.
3. Preserve runtime contracts (`section.slide`, `.slide-edit-layer`, `data-oid`, etc.).
4. Update content while keeping edit/persist/export intact.

### 转换 PowerPoint / Convert a PowerPoint

```text
/frontend-slides-editable

> "Convert presentation.pptx into an editable web slideshow"
```

这个 skill 会：

The skill will:

1. 运行 `scripts/extract-pptx.py`：提取文字、图片和演讲者备注。
2. 与你确认提取结果（标题、要点、图片数量等）。
3. **Phase 1 补全**：提取结果≠完整 brief；仍需一次性确认或补问 **风格方向、可编辑 vs 只读、语言/地区、是否重组页数目标、提取图片的使用方式** 等缺失项。
4. **Phase 2**：用预设/预览缩小风格（Show, don’t tell），再定预设或混合方向。
5. 生成可编辑 HTML deck 并保留内容与资源。

1. Run `scripts/extract-pptx.py`: extract text, images, and speaker notes.
2. Confirm the extraction (titles, content, image counts).
3. **Phase 1 gap-fill:** extraction is **not** the full brief; batch any missing **style direction, editable vs read-only, locale, restructuring goals, how to use extracted images**, etc.
4. **Phase 2:** narrow style with presets/previews (show, don’t tell), then lock preset or mix.
5. Generate an editable HTML deck with preserved assets.

### 转换 PDF / Convert a PDF

```text
/frontend-slides-editable

> "Convert deck.pdf into an editable web slideshow"
```

**依赖：** Python + **PyMuPDF**（`pip install pymupdf`）。抽取命令：

**Dependency:** Python + **PyMuPDF** (`pip install pymupdf`). Extraction command:

```bash
python3 scripts/extract-pdf.py path/to/file.pdf path/to/output_dir
# 可选：无文字且无内嵌图的页面整页渲染为 PNG / Optional: rasterize empty pages
python3 scripts/extract-pdf.py path/to/file.pdf path/to/output_dir --raster-if-empty
```

与 PPT 相同，输出 **`extracted-slides.json`** 与 **`assets/`**；**每一 PDF 页对应一页「幻灯片」**；PDF 无演讲者备注字段。纯扫描件默认抽不出可选文字，需 `--raster-if-empty` 或外部 OCR。

Same as PPT: writes **`extracted-slides.json`** + **`assets/`**; **one PDF page = one slide**; PDFs have no speaker-notes field. Scanned PDFs need **`--raster-if-empty`** or external OCR for usable text.

然后同样走 Phase 1 补全 → Phase 2 风格 → Phase 3 生成可编辑 HTML（与 pptx 流程一致，并非「单步机械编译」）。

Then follow the same Phase 1 → 2 → 3 pipeline as PPTX (not a one-step mechanical compile).

## 编辑体验 / Editing Experience

生成后的 deck 默认包含：

Generated decks include:

- **编辑模式 / Edit mode**：按 `E` 或从左上角呼出控件
- **Pages 侧栏 / Pages sidebar**：缩略图导航、重排、删除（短英文确认 `Delete slide?`）
- **对象编辑 / Object editing**：用 **⠿** 拖动，角点缩放，吸附线对齐；悬停或选中时 **×** 可删除单个对象
- **添加元素 / Add element**：编辑模式下左上角 **Add element** → Text / Image（本地文件、粘贴或占位）/ Video（本地文件）
- **富文本工具栏 / Rich text toolbar**：首行仅 **B / I** 与 **Font / Scale / Px** 抽屉按钮；点击展开对应卡片（字体族、相对字号、像素字号与其他）；支持光标折叠与选区；点击空白处或 **Esc**（非输入时）收起抽屉
- **历史记录 / History**：`Ctrl+Z`、`Ctrl+Y`、`Ctrl+Shift+Z` 及 macOS 等价键
- **持久化 / Persistence**：`Ctrl+S` 保存完整 `.slides-offset` 到 `localStorage`
- **导出 / Export**：下载不含临时编辑态与选中态类名的干净 `.html`

## 内置风格 / Included Styles

### 深色主题 / Dark Themes
- **Bold Signal** - 自信、高冲击力 / Confident, high-impact
- **Electric Studio** - 干净、专业 / Clean, professional
- **Creative Voltage** - 高能霓虹 / Energetic neon
- **Dark Botanical** - 优雅精致 / Elegant, refined

### 浅色主题 / Light Themes
- **Notebook Tabs** - 编辑感与纸张感 / Editorial paper feel
- **Pastel Geometry** - 友好轻快 / Friendly pastel geometry
- **Split Pastel** - 活泼双色分割 / Playful two-tone split
- **Vintage Editorial** - 杂志感与个性化 / Personality-driven editorial

### 特殊风格 / Specialty
- **Neon Cyber** - 未来感霓虹 / Futuristic neon glow
- **Terminal Green** - 开发者终端风 / Hacker-terminal aesthetic
- **Swiss Modern** - 包豪斯极简 / Bauhaus-inspired minimal
- **Paper & Ink** - 文艺排版 / Literary paper-and-ink

### 扩展画廊 / Extended gallery（见 `STYLE_PRESETS.md` 第 13–19 节）
- **Soft Editorial** - 柔和编辑纸感 / Soft paper editorial
- **Signal** - 深蓝 institutions + 金点缀 / Navy and muted gold
- **Studio** - 黑底电光黄 / Black canvas, electric yellow
- **Monochrome** - 象牙色账本单色 / Ivory ledger, ink only
- **Neo-Grid Bold** - 新粗野网格 + 酸黄 / Neo-brutalist grid, acid yellow
- **Vellum** - 学者风深蓝 + 灰青 / Scholarly navy, dusty teal
- **Cobalt Grid** - 钴蓝网格纸 / Cobalt graph-paper analytical

### 扩展画廊自检 · Extended gallery audit

- **三处一致**：`STYLE_PRESETS.md` 中 **19** 套预设（含第 13–19 节）与 `scripts/build-preset-decks.py` 的 `PRESETS` 数组、`examples/generated/presets/*.html` **一一对应**；改主题或参考 HTML 后请执行 `python3 scripts/build-preset-decks.py` 再打开样例验收。  
- **Triple alignment**: all **19** presets in `STYLE_PRESETS.md` (including sections 13–19) match the `PRESETS` array and **`examples/generated/presets/*.html`**; rerun **`python3 scripts/build-preset-decks.py`** after theme/reference edits before reviewing samples.

- **与上游覆盖范围**：[beautiful-html-templates](https://github.com/zarazhangrui/beautiful-html-templates) 公开库体量更大（常见描述为 **30+** 套独立 HTML 模板）；本仓库扩展轮次已把 **7** 套写入规格并接入构建（下表）。其余名称（如 *Editorial Tri-Tone*、*BlockFrame*、*Capsule* 等）可作为 **下一轮** 候选，每套需补全 `STYLE_PRESETS.md` 条目 + `Preset(...)` 主题块 + 再跑构建。  
- **Upstream coverage**: [beautiful-html-templates](https://github.com/zarazhangrui/beautiful-html-templates) ships a **larger** public set (often cited as **30+** templates). This repo’s wave has **fully specified and built** the **seven** below; additional names remain **future** candidates (each needs a `STYLE_PRESETS` spec, a `Preset(...)` block, and a rebuild).

| 扩展画廊名 / Preset title | 样例文件 / Sample slug |
|---------------------------|-------------------------|
| Soft Editorial | `soft-editorial.html` |
| Signal | `signal-gold.html` |
| Studio | `studio-volt.html` |
| Monochrome | `monochrome-ledger.html` |
| Neo-Grid Bold | `neo-grid-yellow.html` |
| Vellum | `vellum-navy.html` |
| Cobalt Grid | `cobalt-grid.html` |

<a id="toc-gallery"></a>
## 样式预览图库 · Style preview gallery

下列 PNG 为各预设 **自检用 deck 的首页（第 1 页）** 静态截图，存放在 **`docs/preset-previews/`**，思路与 [beautiful-html-templates](https://github.com/zarazhangrui/beautiful-html-templates) 仓库中的 [`screenshots/`](https://github.com/zarazhangrui/beautiful-html-templates/tree/main/screenshots) 一致：便于在 README 里快速扫一眼风格，再点开 HTML 细玩或按 `E` 编辑。

These PNGs are **first-slide screenshots** of each preset smoke deck, kept under **`docs/preset-previews/`** — same role as [`screenshots/`](https://github.com/zarazhangrui/beautiful-html-templates/tree/main/screenshots) upstream: skim the gallery here, then open the linked HTML for the full interactive file (press **`E`** for edit mode).

**重新生成截图 / Regenerate captures**（需本机 **Chrome** 或 **Chromium** 无头模式）:

```bash
python3 scripts/build-preset-decks.py
python3 scripts/capture-preset-previews.py
```

详见 [`docs/preset-previews/README.md`](docs/preset-previews/README.md)。维护说明与 `CHROME_PATH`、`PREVIEW_VIEWPORT` 见该文件。

### 深色主题 · Dark themes

<p>
  <a title="Bold Signal" href="examples/generated/presets/bold-signal.html"><img src="docs/preset-previews/bold-signal-cover.png" width="32%" alt="Bold Signal — first slide" /></a>
  <a title="Electric Studio" href="examples/generated/presets/electric-studio.html"><img src="docs/preset-previews/electric-studio-cover.png" width="32%" alt="Electric Studio — first slide" /></a>
  <a title="Creative Voltage" href="examples/generated/presets/creative-voltage.html"><img src="docs/preset-previews/creative-voltage-cover.png" width="32%" alt="Creative Voltage — first slide" /></a>
</p>
<p>
  <a title="Dark Botanical" href="examples/generated/presets/dark-botanical.html"><img src="docs/preset-previews/dark-botanical-cover.png" width="32%" alt="Dark Botanical — first slide" /></a>
</p>

### 浅色主题 · Light themes

<p>
  <a title="Notebook Tabs" href="examples/generated/presets/notebook-tabs.html"><img src="docs/preset-previews/notebook-tabs-cover.png" width="32%" alt="Notebook Tabs — first slide" /></a>
  <a title="Pastel Geometry" href="examples/generated/presets/pastel-geometry.html"><img src="docs/preset-previews/pastel-geometry-cover.png" width="32%" alt="Pastel Geometry — first slide" /></a>
  <a title="Split Pastel" href="examples/generated/presets/split-pastel.html"><img src="docs/preset-previews/split-pastel-cover.png" width="32%" alt="Split Pastel — first slide" /></a>
</p>
<p>
  <a title="Vintage Editorial" href="examples/generated/presets/vintage-editorial.html"><img src="docs/preset-previews/vintage-editorial-cover.png" width="32%" alt="Vintage Editorial — first slide" /></a>
</p>

### 特殊风格 · Specialty

<p>
  <a title="Neon Cyber" href="examples/generated/presets/neon-cyber.html"><img src="docs/preset-previews/neon-cyber-cover.png" width="32%" alt="Neon Cyber — first slide" /></a>
  <a title="Terminal Green" href="examples/generated/presets/terminal-green.html"><img src="docs/preset-previews/terminal-green-cover.png" width="32%" alt="Terminal Green — first slide" /></a>
  <a title="Swiss Modern" href="examples/generated/presets/swiss-modern.html"><img src="docs/preset-previews/swiss-modern-cover.png" width="32%" alt="Swiss Modern — first slide" /></a>
</p>
<p>
  <a title="Paper &amp; Ink" href="examples/generated/presets/paper-ink.html"><img src="docs/preset-previews/paper-ink-cover.png" width="32%" alt="Paper and Ink — first slide" /></a>
</p>

### 扩展画廊（beautiful-html-templates 对齐）· Extended gallery

<p>
  <a title="Soft Editorial" href="examples/generated/presets/soft-editorial.html"><img src="docs/preset-previews/soft-editorial-cover.png" width="32%" alt="Soft Editorial — first slide" /></a>
  <a title="Signal" href="examples/generated/presets/signal-gold.html"><img src="docs/preset-previews/signal-gold-cover.png" width="32%" alt="Signal — first slide" /></a>
  <a title="Studio" href="examples/generated/presets/studio-volt.html"><img src="docs/preset-previews/studio-volt-cover.png" width="32%" alt="Studio — first slide" /></a>
</p>
<p>
  <a title="Monochrome" href="examples/generated/presets/monochrome-ledger.html"><img src="docs/preset-previews/monochrome-ledger-cover.png" width="32%" alt="Monochrome — first slide" /></a>
  <a title="Neo-Grid Bold" href="examples/generated/presets/neo-grid-yellow.html"><img src="docs/preset-previews/neo-grid-yellow-cover.png" width="32%" alt="Neo-Grid Bold — first slide" /></a>
  <a title="Vellum" href="examples/generated/presets/vellum-navy.html"><img src="docs/preset-previews/vellum-navy-cover.png" width="32%" alt="Vellum — first slide" /></a>
</p>
<p>
  <a title="Cobalt Grid" href="examples/generated/presets/cobalt-grid.html"><img src="docs/preset-previews/cobalt-grid-cover.png" width="32%" alt="Cobalt Grid — first slide" /></a>
</p>

<a id="toc-docs"></a>
## 文档结构 / Documentation Map

| 文件 File | 作用 Purpose |
|------|------|
| `SKILL.md` | 核心流程与交付规则 / Workflow and delivery behavior |
| `editor-runtime.md` | 运行时 DOM 契约与检查项 / Runtime DOM contracts and checklist |
| `examples/editable-deck-reference.html` | 标准参考实现 / Canonical runtime reference |
| `examples/demos/frontend-slides-editable-readme-demo.html` | README 配套演示 deck（手工维护，非构建脚本输出）/ README companion deck (hand-maintained, not from build script) |
| `examples/frontend-slides-editable-skill-intro-bilingual.html` | 双语 Skill 介绍 deck / Bilingual skill intro deck |
| `examples/pitch-deck-readme-editable-fork.html` | 可编辑分支 pitch 样例 / Editable-fork pitch sample |
| `STYLE_PRESETS.md` | 19 个精选风格 / 19 curated style presets |
| `viewport-base.css` | 视口适配基础样式 / Viewport-fit base CSS |
| `html-template.md` | HTML 基础结构说明 / Base HTML integration notes |
| `animation-patterns.md` | 动画参考 / CSS/JS animation reference |
| `scripts/extract-pptx.py` | PPT 内容提取脚本 / PPT extraction script |
| `scripts/extract-pdf.py` | PDF 按页抽取（与 PPT 相同 JSON 形状）/ PDF per-page extraction (same JSON shape as PPT) |
| `examples/generated/presets/*.html` | 19 个单风格可编辑样例（与 STYLE_PRESETS 一一对应） / One editable deck per preset |
| `docs/preset-previews/*.png` | 各预设首页截图（README 图库）/ First-slide PNGs for README gallery |
| `scripts/build-preset-decks.py` | 从参考实现批量生成上述样例 / Build all preset sample files |
| `scripts/capture-preset-previews.py` | 用无头 Chrome 生成 `docs/preset-previews/*-cover.png` / Headless Chrome capture for preview PNGs |

## 架构说明 / Architecture

这个 skill 延续父项目“渐进式披露”策略：

This skill follows the parent project's progressive-disclosure approach:

- `SKILL.md` 承载流程和规则 / `SKILL.md` carries workflow and rules
- 支撑文件按需加载 / supporting docs load on demand
- 可编辑运行时保持唯一参考实现 / one canonical runtime implementation
- 生成结果零依赖且可移植 / generated decks stay dependency-free and portable

运行时有几个不可破坏的约束：

The runtime depends on non-negotiable contracts:

- 每页必须是带稳定 `id` 的 `section.slide`
- 可移动内容位于 `.slide-edit-layer`
- 可编辑块使用 `[data-slide-object][data-oid]`
- 页面枚举必须限定真实 deck 根，不能包含缩略图克隆

- each slide is a `section.slide` with stable `id`
- movable content lives in `.slide-edit-layer`
- editable blocks use `[data-slide-object][data-oid]`
- slide enumeration must stay scoped to the true deck root

## 设计理念 / Philosophy

1. **通过“看见选项”建立审美。** 风格预览比抽象问卷更有效。  
2. **生成不是定稿。** 第一版必须天然可编辑。  
3. **依赖就是债务。** 单文件 HTML 应该多年后仍可用。  
4. **尊重视口。** 放不下就拆页，而不是隐藏溢出。  
5. **有辨识度优先。** 工具应帮助产出可记忆的内容。  

1. **People discover taste by seeing options.** Previews beat abstract questionnaires.  
2. **Generated is not final.** The first draft should remain editable.  
3. **Dependencies are debt.** A single HTML should still work years later.  
4. **Respect the viewport.** Split slides instead of hiding overflow.  
5. **Distinctiveness wins.** Presentation tools should produce memorable output.  

<a id="toc-requirements"></a>
## 依赖要求 / Requirements

- [Claude Code](https://claude.ai/claude-code) 或任意将 skill 安装到 **`~/.claude/skills/`** 的兼容客户端；**OpenAI Codex** 使用 **`~/.codex/skills/`**；**Cursor** 等请按各产品文档中的 skills 目录或技能加载方式配置
- 如需 PPT 转换：Python + `python-pptx`
- 如需 PDF 抽取（转 HTML 前的中间层）：Python + **PyMuPDF**（`pip install pymupdf`）；扫描件/纯图 PDF 默认无可靠文本，见上文「转换 PDF」
- 如需浏览器编辑/导出：现代 Chromium、Safari 或 Firefox

- [Claude Code](https://claude.ai/claude-code) or any runner that loads skills from **`~/.claude/skills/`**; **OpenAI Codex** uses **`~/.codex/skills/`**; **Cursor** and others: follow that product’s documented skills directory or skill-loading flow
- For PPT conversion: Python + `python-pptx`
- For PDF extraction (intermediate step before HTML): Python + **PyMuPDF** (`pip install pymupdf`); scanned/image-only PDFs need raster/OCR — see **Convert a PDF** above
- For editing/export: modern Chromium, Safari, or Firefox-class browser

<a id="toc-try"></a>
## 试用参考 / Try The Reference

打开：

Open:

```text
examples/editable-deck-reference.html
```

**其它手工维护样例（非 `build-preset-decks.py` 产物） / Other hand-maintained samples (not produced by `build-preset-decks.py`):**

```text
examples/demos/frontend-slides-editable-readme-demo.html
examples/frontend-slides-editable-skill-intro-bilingual.html
examples/pitch-deck-readme-editable-fork.html
```

**19 个独立可编辑样例（每种风格一个 HTML）：**

**Nineteen separate editable decks (one file per preset):**

```text
examples/generated/presets/bold-signal.html
examples/generated/presets/electric-studio.html
examples/generated/presets/creative-voltage.html
examples/generated/presets/dark-botanical.html
examples/generated/presets/notebook-tabs.html
examples/generated/presets/pastel-geometry.html
examples/generated/presets/split-pastel.html
examples/generated/presets/vintage-editorial.html
examples/generated/presets/neon-cyber.html
examples/generated/presets/terminal-green.html
examples/generated/presets/swiss-modern.html
examples/generated/presets/paper-ink.html
examples/generated/presets/soft-editorial.html
examples/generated/presets/signal-gold.html
examples/generated/presets/studio-volt.html
examples/generated/presets/monochrome-ledger.html
examples/generated/presets/neo-grid-yellow.html
examples/generated/presets/vellum-navy.html
examples/generated/presets/cobalt-grid.html
```

重新生成上述 HTML 与 README 中的预览图：

Regenerate preset HTML **and** README gallery PNGs:

```bash
python3 scripts/build-preset-decks.py
python3 scripts/capture-preset-previews.py
```

（仅截图、不改 deck 时只跑第二行；需本机 Chrome/Chromium。）  
(Re-run only the second line to refresh screenshots; requires local Chrome/Chromium.)

然后试试：

Then try:

- 按 `E` / press `E`
- 点击文本编辑 / click text to edit
- 使用浮动工具栏 / use the floating toolbar
- 用 **⠿** 拖拽对象 / drag objects with **⠿**
- 缩放选中对象 / resize a selected object
- 在 **Pages** 重排 / reorder in **Pages**
- 用 **×** 删对象或删页（页删除会确认）/ delete objects or slides (slide delete confirms)
- **Add element** 添加文本/图/视频 / use **Add element** for text, image, or video
- 按 `Ctrl+S` 保存 / press `Ctrl+S`
- 导出 deck / export the deck

## 致谢 / Credits

基于 [@zarazhangrui](https://github.com/zarazhangrui/frontend-slides) 的 **frontend-slides** 扩展而来，本分支新增可编辑运行时。扩展风格画廊与 [beautiful-html-templates](https://github.com/zarazhangrui/beautiful-html-templates) 中的模板名称与气质对齐（本仓库内完整规格仍以 `STYLE_PRESETS.md` 为准）。

Based on **frontend-slides** by [@zarazhangrui](https://github.com/zarazhangrui/frontend-slides), with editable runtime added in this fork. Additional preset names/vibes align with [beautiful-html-templates](https://github.com/zarazhangrui/beautiful-html-templates); authoritative specs remain in `STYLE_PRESETS.md`.

## 许可证 / License

MIT（与父项目一致，除非另有说明）。

MIT (same as the parent project unless otherwise noted).
