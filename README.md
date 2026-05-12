# Frontend Slides - Editable

一个适用于 Claude Code / Codex 的技能，用来生成惊艳、带动画、单文件的 HTML 演示文稿，并内置浏览器编辑器：可拖拽对象、调整大小、编辑文本、重排页面、本地保存，并导出干净的独立 HTML。

A Claude Code / Codex skill for creating stunning, animation-rich, single-file HTML presentations with a built-in browser editor: drag objects, resize blocks, edit text, reorder slides, save locally, and export a clean standalone HTML.

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

- **与 beautiful-html-templates 已同步的 presets**：自 [beautiful-html-templates](https://github.com/zarazhangrui/beautiful-html-templates) 引入、并在本仓库 **`STYLE_PRESETS.md` §13–19** 落规格且 **`build-preset-decks.py` 可生成样例** 的共 **7** 套为：**Soft Editorial**、**Signal**、**Studio**、**Monochrome**、**Neo-Grid Bold**、**Vellum**、**Cobalt Grid**（对应 `examples/generated/presets/` 下 `soft-editorial.html`、`signal-gold.html`、`studio-volt.html`、`monochrome-ledger.html`、`neo-grid-yellow.html`、`vellum-navy.html`、`cobalt-grid.html`）。气质与上游模板名对齐；版式与 token 以本仓库文档为准，并非逐文件拷贝 HTML。上游库中**其余**模板尚未在本 skill 内写成预设与构建项。  
  **beautiful-html-templates presets synced here**: **seven** themes from [beautiful-html-templates](https://github.com/zarazhangrui/beautiful-html-templates) are first-class in **`STYLE_PRESETS.md` §13–19** and ship as built samples: **Soft Editorial**, **Signal**, **Studio**, **Monochrome**, **Neo-Grid Bold**, **Vellum**, **Cobalt Grid** → `soft-editorial.html`, `signal-gold.html`, `studio-volt.html`, `monochrome-ledger.html`, `neo-grid-yellow.html`, `vellum-navy.html`, `cobalt-grid.html` under `examples/generated/presets/`. Vibes align with upstream template names; layout and tokens are **specified in this repo**, not byte-for-byte copies of upstream HTML. **Other** upstream templates are **not** yet ported as presets here.

参考实现仍以单文件 **`examples/editable-deck-reference.html`** 为契约；生成新 deck 时请继续遵循本仓库 `SKILL.md` 与 `editor-runtime.md`。  
The reference contract remains the single file **`examples/editable-deck-reference.html`**; follow `SKILL.md` and `editor-runtime.md` when generating new decks.

## 这个 Skill 是做什么的 / What This Does

**Frontend Slides - Editable** 是 **frontend-slides** 的可编辑分支。它保留了原始 skill 的风格探索流程、视口适配规则和 PPT 转换能力，并在此基础上加入完整的浏览器内编辑运行时。**交付用的幻灯片仍应按 `STYLE_PRESETS.md` 实现各预设的布局与签名元素**；可编辑只是增加运行时，不是把多套风格压成同一套版式原型。`examples/generated/presets/` 仅为运行时自检样例。

**Frontend Slides - Editable** is the editable fork of **frontend-slides**. It preserves style discovery, viewport discipline, and PPT conversion from the original skill, then adds a full in-browser editing runtime. **Real decks should still implement each preset’s layout and signature elements from `STYLE_PRESETS.md`** — edit mode is an add-on, not permission to reuse one generic slide prototype for every aesthetic. `examples/generated/presets/` is for runtime smoke tests only.


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

如果只需要更轻量的只读输出，请使用父 skill **frontend-slides**。

If you only need the smallest read-only output, use the parent **frontend-slides** skill.

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
- **PPT 转换**：将 `.pptx` 转为可编辑网页幻灯片并保留资源
- **视口安全**：每一页都要求适配视口，不允许内部滚动
- **持久化与导出**：`Ctrl+S` 保存结构化状态；导出时剥离临时编辑态
- **反模板感**：通过精选风格预设，避免千篇一律

- **Zero dependencies**: Single-file HTML with inline CSS/JS, no npm/build/framework
- **Visual style discovery**: pick by preview, not design jargon
- **Full editable runtime**: drag, multi-select, corner/edge resize, object delete, **add** text/image/video, filmstrip, history
- **PPT conversion**: convert `.pptx` into editable web slides with preserved assets
- **Viewport-safe output**: every slide must fit the viewport without internal scrolling
- **Persistence + export**: `Ctrl+S` saves structure; export removes transient edit state
- **Anti-generic aesthetics**: curated presets over bland default templates

## 适合什么场景 / When To Use This

适合 **frontend-slides-editable**：

Use **frontend-slides-editable** when you want:

- 生成后仍可在浏览器继续微调
- 支持客户/团队评审后的布局修订
- 单文件、零构建的可交付结果
- PowerPoint 转网页后继续编辑

- a generated deck you can continue refining in browser
- post-generation layout iteration during reviews
- a single-file deliverable with no build step
- PowerPoint-to-web conversion with continued editing

适合 **frontend-slides**：

Use **frontend-slides** when you want:

- 更小更轻的只读输出
- 不需要编辑器界面
- 最轻量的生成文件

- a smaller read-only output
- presentation-only HTML without editor chrome
- the lightest possible generated file

## 安装 / Installation

把目录复制到你的 skill 目录：

Copy this directory into your skill folder:

### Claude Code 用户 / For Claude Code users

```bash
cp -r frontend-slides-editable ~/.claude/skills/
```

### Codex 用户 / For Codex users

```bash
cp -r frontend-slides-editable ~/.codex/skills/
```

然后调用：

Then invoke it with:

```text
/frontend-slides-editable
```

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

1. 提取 PPT 文字、图片和备注。
2. 与你确认提取结果（标题、要点、图片数量等）。
3. **Phase 1 补全**：提取结果≠完整 brief；仍需一次性确认或补问 **风格方向、可编辑 vs 只读、语言/地区、是否重组页数目标、提取图片的使用方式** 等缺失项。
4. **Phase 2**：用预设/预览缩小风格（Show, don’t tell），再定预设或混合方向。
5. 生成可编辑 HTML deck 并保留内容与资源。

1. Extract text, images, and notes from PPT.
2. Confirm the extraction (titles, content, image counts).
3. **Phase 1 gap-fill:** extraction is **not** the full brief; batch any missing **style direction, editable vs read-only, locale, restructuring goals, how to use extracted images**, etc.
4. **Phase 2:** narrow style with presets/previews (show, don’t tell), then lock preset or mix.
5. Generate an editable HTML deck with preserved assets.

## 编辑体验 / Editing Experience

生成后的 deck 默认包含：

Generated decks include:

- **编辑模式 / Edit mode**：按 `E` 或从左上角呼出控件
- **Pages 侧栏 / Pages sidebar**：缩略图导航、重排、删除（短英文确认 `Delete slide?`）
- **对象编辑 / Object editing**：用 **⠿** 拖动，角点缩放，吸附线对齐；悬停或选中时 **×** 可删除单个对象
- **添加元素 / Add element**：编辑模式下左上角 **Add element** → Text / Image（URL 或占位）/ Video（URL）
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

### 扩展画廊 / Extended gallery（见 `STYLE_PRESETS.md` §13–19）
- **Soft Editorial** - 柔和编辑纸感 / Soft paper editorial
- **Signal** - 深蓝 institutions + 金点缀 / Navy and muted gold
- **Studio** - 黑底电光黄 / Black canvas, electric yellow
- **Monochrome** - 象牙色账本单色 / Ivory ledger, ink only
- **Neo-Grid Bold** - 新粗野网格 + 酸黄 / Neo-brutalist grid, acid yellow
- **Vellum** - 学者风深蓝 + 灰青 / Scholarly navy, dusty teal
- **Cobalt Grid** - 钴蓝网格纸 / Cobalt graph-paper analytical

### 扩展画廊自检 · Extended gallery audit

- **三处一致**：`STYLE_PRESETS.md` 中 **19** 套预设（含 §13–19）与 `scripts/build-preset-decks.py` 的 `PRESETS` 数组、`examples/generated/presets/*.html` **一一对应**；改主题或参考 HTML 后请执行 `python3 scripts/build-preset-decks.py` 再打开样例验收。  
- **Triple alignment**: all **19** presets in `STYLE_PRESETS.md` (including §13–19) match the `PRESETS` array and **`examples/generated/presets/*.html`**; rerun **`python3 scripts/build-preset-decks.py`** after theme/reference edits before reviewing samples.

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

## 文档结构 / Documentation Map

| 文件 File | 作用 Purpose |
|------|------|
| `SKILL.md` | 核心流程与交付规则 / Workflow and delivery behavior |
| `editor-runtime.md` | 运行时 DOM 契约与检查项 / Runtime DOM contracts and checklist |
| `examples/editable-deck-reference.html` | 标准参考实现 / Canonical runtime reference |
| `STYLE_PRESETS.md` | 19 个精选风格 / 19 curated style presets |
| `viewport-base.css` | 视口适配基础样式 / Viewport-fit base CSS |
| `html-template.md` | HTML 基础结构说明 / Base HTML integration notes |
| `animation-patterns.md` | 动画参考 / CSS/JS animation reference |
| `scripts/extract-pptx.py` | PPT 内容提取脚本 / PPT extraction script |
| `examples/generated/presets/*.html` | 19 个单风格可编辑样例（与 STYLE_PRESETS 一一对应） / One editable deck per preset |
| `scripts/build-preset-decks.py` | 从参考实现批量生成上述样例 / Build all preset sample files |

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

## 依赖要求 / Requirements

- [Claude Code](https://claude.ai/claude-code) 或兼容运行器
- 如需 PPT 转换：Python + `python-pptx`
- 如需浏览器编辑/导出：现代 Chromium、Safari 或 Firefox

- [Claude Code](https://claude.ai/claude-code) or a compatible runner
- For PPT conversion: Python + `python-pptx`
- For editing/export: modern Chromium, Safari, or Firefox-class browser

## 试用参考 / Try The Reference

打开：

Open:

```text
examples/editable-deck-reference.html
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

重新生成上述文件：

Regenerate all preset samples:

```bash
python3 scripts/build-preset-decks.py
```

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
