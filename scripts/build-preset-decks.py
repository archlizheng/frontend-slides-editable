#!/usr/bin/env python3
"""Build README-driven editable preset decks.

These outputs are full editable decks that summarize the current README in a
Chinese-first voice while preserving preset-specific layout identity.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "examples" / "editable-deck-reference.html"
OUT_DIR = ROOT / "examples" / "generated" / "presets"

DARK_CHROME = """
      --deck-chrome-bg: rgba(15, 23, 42, 0.94);
      --deck-chrome-border: rgba(255, 255, 255, 0.14);
      --deck-chrome-text: #e2e8f0;
      --deck-chrome-muted: #94a3b8;
      --deck-chrome-accent: {accent};
      --deck-chrome-shadow: 0 12px 40px rgba(0, 0, 0, 0.45);
      --deck-chrome-surface: rgba(30, 41, 59, 0.92);
"""

LIGHT_CHROME = """
      --deck-chrome-bg: rgba(255, 255, 255, 0.92);
      --deck-chrome-border: rgba(15, 23, 42, 0.12);
      --deck-chrome-text: #0f172a;
      --deck-chrome-muted: #64748b;
      --deck-chrome-accent: {accent};
      --deck-chrome-shadow: 0 12px 40px rgba(15, 23, 42, 0.12);
      --deck-chrome-surface: rgba(241, 245, 249, 0.95);
"""

ROOT_NEEDLE_START = "      --font-display: 'Clash Display', sans-serif;"
ROOT_NEEDLE_END = "      --deck-chrome-surface: rgba(30, 41, 59, 0.92);\n"

HEAD_FONTSHARE = """  <link rel="preconnect" href="https://api.fontshare.com" crossorigin>
  <link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,700&f[]=clash-display@600&display=swap" rel="stylesheet">"""


def normalize_generated_html(source: str) -> str:
    return "\n".join(line.rstrip() for line in source.splitlines()) + "\n"

THEME_NEEDLE_OLD = """    /* === theme === */
    body {
      margin: 0;
      font-family: var(--font-body);
      background: var(--slide-bg-deep);
      color: var(--text-primary);
    }
    .slide { background: var(--slide-bg-gradient); }"""

COVER_METRICS = [
    ("Preset", "每套版式都保留自己的布局和签名元素"),
    ("Edit", "拖拽 缩放 多选 Pages Undo / Redo"),
    ("Ship", "Ctrl+S 保存结构，Export HTML 清理导出"),
]

VALUE_CARDS = [
    ("Parent", "只读更轻", "接近定稿、体积敏感、只需要展示时，更适合父 skill。"),
    ("Editable", "继续改布局", "客户反馈、团队评审、内容常变时，更适合这个分支。"),
    ("Runtime", "对象级编辑", "拖拽、缩放、富文本、Pages、历史记录都保留在文件里。"),
    ("Delivery", "保存与导出", "localStorage 持久化迭代状态，导出时再生成干净的独立 HTML。"),
]

WORKFLOW_CARDS = [
    ("01", "成组 discovery", "目标、页数、内容、风格、编辑范围、图片素材一次问清。"),
    ("02", "先缩小风格范围", "根据 style preference、受众和内容先收敛 2-4 个 preset。"),
    ("03", "直选或看预览", "可以直接挑 preset，也可以先看预览再决定。"),
    ("04", "生成可编辑 deck", "单文件 HTML 交付时仍然保留 Pages、save/export 与 history。"),
]

ARCH_CARDS = [
    ("DOM", "运行时契约", "`section.slide#id`、`.slide-edit-layer`、`[data-slide-object][data-oid]` 需要稳定。"),
    ("Deck root", "只枚举真实 slides", "查 slide 时必须限定 deck root，不能把 filmstrip clones 算进去。"),
    ("Viewport", "不滚动，放不下就拆页", "`100vh / 100dvh`、`clamp()`、内容过密就分拆到新 slide。"),
    ("Docs", "支撑文件按需读取", "`SKILL.md`、`STYLE_PRESETS.md`、`editor-runtime.md`、`html-template.md`。"),
]

COMMON_COMPONENT_CSS = """
    .slide > .slide-bg {
      position: absolute;
      inset: 0;
      z-index: 0;
      pointer-events: none;
      overflow: hidden;
    }
    .slides-offset { background: var(--slide-bg-deep); }
    .slide {
      background: transparent;
      color: var(--text-primary);
    }
    .slide > * { position: relative; }
    .slide-static {
      position: absolute;
      z-index: 1;
      pointer-events: none;
    }
    .reveal {
      opacity: 0;
      transform: translateY(18px);
      transition: opacity 0.55s ease, transform 0.55s ease;
    }
    .slide.visible .reveal {
      opacity: 1;
      transform: translateY(0);
    }
    .slide.visible .reveal:nth-child(1) { transition-delay: 0.05s; }
    .slide.visible .reveal:nth-child(2) { transition-delay: 0.12s; }
    .slide.visible .reveal:nth-child(3) { transition-delay: 0.18s; }
    .slide.visible .reveal:nth-child(4) { transition-delay: 0.24s; }
    .slide.visible .reveal:nth-child(5) { transition-delay: 0.3s; }
    .slide-object {
      transition: transform 0.25s ease, box-shadow 0.25s ease, outline-color 0.25s ease;
    }
    .slide-object-text {
      color: var(--text-primary);
    }
    .eyebrow .slide-object-text,
    .section-number .slide-object-text {
      font-size: clamp(0.68rem, 0.95vw, 0.86rem);
      text-transform: uppercase;
      letter-spacing: 0.16em;
      font-weight: 700;
      color: var(--text-muted);
    }
    .hero-title .slide-object-text,
    .section-title .slide-object-text {
      font-family: var(--font-display);
      font-weight: 800;
      letter-spacing: -0.055em;
      line-height: 0.94;
    }
    .hero-title .slide-object-text {
      font-size: clamp(2.5rem, 7vw, 5.8rem);
    }
    .section-title .slide-object-text {
      font-size: clamp(1.7rem, 4vw, 3.7rem);
    }
    .hero-subtitle .slide-object-text,
    .section-copy .slide-object-text,
    .closing-note .slide-object-text {
      font-size: clamp(0.92rem, 1.26vw, 1.08rem);
      line-height: 1.55;
      color: var(--text-secondary);
    }
    .metric-box .slide-object-text {
      padding: clamp(0.9rem, 1.3vw, 1.2rem);
      border-radius: clamp(12px, 1.2vw, 18px);
      background: var(--surface);
      border: 1px solid var(--line);
      box-shadow: var(--panel-shadow);
    }
    .metric-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: clamp(0.55rem, 0.9vw, 0.95rem);
    }
    .metric {
      display: flex;
      flex-direction: column;
      gap: clamp(0.2rem, 0.4vw, 0.38rem);
      padding-top: clamp(0.45rem, 0.7vw, 0.6rem);
      border-top: 3px solid var(--accent);
    }
    .metric-value {
      font-family: var(--font-display);
      font-size: clamp(1.05rem, 1.8vw, 1.55rem);
      letter-spacing: -0.04em;
      color: var(--text-primary);
    }
    .metric-note {
      font-size: clamp(0.74rem, 0.95vw, 0.88rem);
      line-height: 1.42;
      color: var(--text-secondary);
    }
    .panel-card .slide-object-text,
    .workflow-card .slide-object-text,
    .arch-card .slide-object-text,
    .note-card .slide-object-text {
      display: flex;
      flex-direction: column;
      gap: clamp(0.38rem, 0.7vw, 0.68rem);
      height: 100%;
      box-sizing: border-box;
      padding: clamp(0.92rem, 1.3vw, 1.16rem);
      border-radius: clamp(12px, 1.2vw, 20px);
      background: var(--surface);
      border: 1px solid var(--line);
      box-shadow: var(--panel-shadow);
      backdrop-filter: blur(6px);
    }
    .accent-card .slide-object-text {
      background: var(--accent);
      border-color: color-mix(in srgb, var(--accent) 70%, black);
      color: var(--text-on-accent);
    }
    .label {
      font-size: clamp(0.64rem, 0.86vw, 0.76rem);
      text-transform: uppercase;
      letter-spacing: 0.14em;
      font-weight: 700;
      color: var(--text-muted);
    }
    .accent-card .label {
      color: color-mix(in srgb, var(--text-on-accent) 74%, transparent);
    }
    .title {
      font-family: var(--font-display);
      font-size: clamp(1.05rem, 1.7vw, 1.55rem);
      line-height: 1;
      letter-spacing: -0.04em;
    }
    .body {
      font-size: clamp(0.82rem, 1vw, 0.96rem);
      line-height: 1.48;
      color: var(--text-secondary);
    }
    .body strong {
      color: var(--text-primary);
    }
    .accent-card .body,
    .accent-card .body strong {
      color: var(--text-on-accent);
    }
    .workflow-card .step-index {
      font-family: var(--font-display);
      font-size: clamp(1.5rem, 2.5vw, 2rem);
      line-height: 1;
      color: var(--accent);
      letter-spacing: -0.06em;
    }
    .note-card .title {
      font-size: clamp(1rem, 1.45vw, 1.25rem);
    }
    .pill-row {
      display: flex;
      flex-wrap: wrap;
      gap: clamp(0.45rem, 0.65vw, 0.65rem);
      margin-top: auto;
    }
    .pill {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 0.35rem 0.7rem;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: var(--surface-strong);
      font-size: clamp(0.68rem, 0.82vw, 0.78rem);
      line-height: 1;
      font-weight: 700;
      color: var(--text-primary);
    }
    .closing-note .slide-object-text {
      border-top: 4px solid var(--accent);
      background: var(--surface);
    }
    .layout-bold .section-number .slide-object-text {
      font-size: clamp(2.8rem, 8vw, 6.8rem);
      line-height: 0.8;
      color: var(--accent);
      opacity: 0.96;
    }
    .layout-bold .panel-card .slide-object-text,
    .layout-bold .workflow-card .slide-object-text {
      border-radius: 2px;
      border-width: 2px;
      border-color: color-mix(in srgb, var(--accent) 38%, var(--line));
      transform: rotate(var(--card-tilt, 0deg));
    }
    .layout-split .section-title .slide-object-text {
      max-width: 11ch;
    }
    .layout-split .panel-card .slide-object-text,
    .layout-split .workflow-card .slide-object-text {
      border-radius: 0;
      border-left: 6px solid var(--accent);
      box-shadow: none;
    }
    .layout-editorial .section-title .slide-object-text {
      font-size: clamp(2.1rem, 5.8vw, 5.2rem);
      line-height: 0.9;
      font-style: italic;
    }
    .layout-editorial .panel-card .slide-object-text,
    .layout-editorial .workflow-card .slide-object-text,
    .layout-editorial .arch-card .slide-object-text {
      background: transparent;
      box-shadow: none;
      border-width: 0 0 1px 0;
      border-radius: 0;
      padding-left: 0;
      padding-right: 0;
    }
    .layout-notebook .panel-card .slide-object-text,
    .layout-notebook .workflow-card .slide-object-text,
    .layout-soft .panel-card .slide-object-text,
    .layout-soft .workflow-card .slide-object-text {
      border-radius: clamp(18px, 2vw, 30px);
    }
    .layout-notebook .section-number .slide-object-text,
    .layout-soft .section-number .slide-object-text {
      display: inline-flex;
      width: auto;
      padding: 0.42rem 0.76rem;
      border-radius: 999px;
      background: var(--surface-strong);
      border: 1px solid var(--line);
    }
    .layout-cyber .panel-card .slide-object-text,
    .layout-cyber .workflow-card .slide-object-text,
    .layout-cyber .arch-card .slide-object-text {
      border-radius: 0;
      border-color: color-mix(in srgb, var(--accent) 44%, transparent);
      box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--accent) 18%, transparent), var(--panel-shadow);
    }
    .layout-cyber .label::before {
      content: "// ";
      color: var(--accent);
    }
    .layout-minimal .panel-card .slide-object-text,
    .layout-minimal .workflow-card .slide-object-text,
    .layout-minimal .arch-card .slide-object-text,
    .layout-minimal .metric-box .slide-object-text {
      border-radius: 0;
      box-shadow: none;
      border: 1px solid var(--text-primary);
    }
    .layout-minimal .section-title .slide-object-text {
      line-height: 0.86;
      text-transform: uppercase;
    }
    @media (max-width: 820px) {
      .metric-grid {
        grid-template-columns: 1fr;
      }
    }
"""


@dataclass(frozen=True)
class Preset:
    slug: str
    title: str
    family: str
    cover_archetype: str
    content_archetype: str
    light_chrome: bool
    accent: str
    root_lines: str
    theme_css: str
    google_url: Optional[str]


def box(left: str, top: str, width: str, height: Optional[str] = None) -> str:
    parts = [f"left:{left};", f"top:{top};", f"width:{width};"]
    if height:
        parts.append(f"height:{height};")
    return "".join(parts)


class SlideBuilder:
    def __init__(self, slide_index: int, slide_class: str) -> None:
        self.slide_index = slide_index
        self.slide_class = slide_class
        self.objects: list[str] = []
        self._count = 0

    def text(self, cls: str, style: str, html: str) -> None:
        oid = f"s{self.slide_index}-o{self._count}"
        self._count += 1
        self.objects.append(
            f'''    <div class="slide-object reveal {cls}" data-slide-object data-oid="{oid}" data-object-type="text" style="{style}">
      <button type="button" class="slide-object-move" aria-label="Move">⠿</button>
      <button type="button" class="slide-object-delete" aria-label="Delete object">×</button>
      <button type="button" class="slide-object-resize" aria-label="Resize"></button>
      <div class="slide-object-text" contenteditable="false">{html}</div>
    </div>'''
        )

    def render(self, static: str = "") -> str:
        static_block = f"\n{static}" if static else ""
        objects_html = "\n".join(self.objects)
        return (
            f'<section class="slide {self.slide_class}" id="slide-{self.slide_index}">\n'
            '  <div class="slide-bg" aria-hidden="true"></div>'
            f"{static_block}\n"
            '  <div class="slide-edit-layer">\n'
            f"{objects_html}\n"
            "  </div>\n"
            "</section>"
        )


def metric_html() -> str:
    chunks = []
    for label, note in COVER_METRICS:
        chunks.append(
            f'<div class="metric"><span class="metric-value">{label}</span><span class="metric-note">{note}</span></div>'
        )
    return '<div class="metric-grid">' + "".join(chunks) + "</div>"


def card_html(label: str, title: str, body: str) -> str:
    return f'<span class="label">{label}</span><span class="title">{title}</span><span class="body">{body}</span>'


def workflow_card_html(step: str, title: str, body: str) -> str:
    return (
        f'<span class="step-index">{step}</span>'
        f'<span class="title">{title}</span>'
        f'<span class="body">{body}</span>'
    )


def note_card_html(title: str, body: str, pills: list[str]) -> str:
    pill_html = "".join(f'<span class="pill">{pill}</span>' for pill in pills)
    return f'<span class="title">{title}</span><span class="body">{body}</span><div class="pill-row">{pill_html}</div>'


def arch_note_html(preset_title: str) -> str:
    return (
        '<span class="title">Remember / 记住</span>'
        '<span class="body">可编辑 runtime 是附加层，不是把所有 preset 压成一种模板。'
        f'当前文件展示的是 <strong>{preset_title}</strong> 版本的 README deck，按 <strong>E</strong> 可继续编辑。</span>'
    )


def strip_preset_cover_decor(css: str) -> str:
    """Remove legacy cover pseudo-elements so family-specific decor can be injected once."""
    patterns = (
        r"\n    \.slide-cover::after \{.*?\n    \}",
        r"\n    \.slide-cover > \.slide-bg::after \{.*?\n    \}",
    )
    for pat in patterns:
        css = re.sub(pat, "", css, flags=re.DOTALL)
    return css


COVER_DECOR_CSS_BY_FAMILY: dict[str, str] = {
    "bold": """
    .slide-cover::after {
      content: "";
      position: absolute;
      right: 6%;
      top: 12%;
      width: min(26vw, 300px);
      height: min(48vh, 380px);
      background: var(--accent);
      border-radius: clamp(14px, 1.4vw, 22px);
      transform: rotate(-2.5deg);
      opacity: 0.9;
      z-index: 0;
      pointer-events: none;
      box-shadow: 0 24px 48px rgba(0, 0, 0, 0.22);
    }
""",
    "split": """
    .slide-cover > .slide-bg::after {
      content: "";
      position: absolute;
      left: var(--cover-decor-left, 10%);
      right: var(--cover-decor-right, 10%);
      bottom: var(--cover-decor-bottom, 7%);
      height: var(--cover-decor-height, 3px);
      border-radius: 999px;
      background: var(--cover-decor-background, linear-gradient(90deg, transparent, var(--accent), transparent));
      opacity: var(--cover-decor-opacity, 0.88);
      z-index: 0;
      pointer-events: none;
    }
""",
    "editorial": """
    .slide-cover > .slide-bg::after {
      content: "";
      position: absolute;
      left: var(--cover-decor-left, 7%);
      top: var(--cover-decor-top, 14%);
      bottom: var(--cover-decor-bottom, 16%);
      width: var(--cover-decor-width, 2px);
      border-radius: 2px;
      background: var(--cover-decor-background, linear-gradient(
        180deg,
        transparent,
        color-mix(in srgb, var(--accent) 55%, transparent) 35%,
        color-mix(in srgb, var(--accent) 85%, transparent) 50%,
        color-mix(in srgb, var(--accent) 55%, transparent) 65%,
        transparent
      ));
      opacity: var(--cover-decor-opacity, 0.95);
      z-index: 0;
      pointer-events: none;
      box-shadow: var(--cover-decor-shadow-x, 18px) 0 0 0 color-mix(in srgb, var(--accent) 35%, transparent);
    }
""",
    "notebook": """
    .slide-cover > .slide-bg::after {
      content: "";
      position: absolute;
      right: 0;
      top: 18%;
      width: clamp(8px, 1vw, 12px);
      height: 52%;
      border-radius: 10px 0 0 10px;
      background: linear-gradient(180deg, #98d4bb 0%, #c7b8ea 34%, #f4b8c5 66%, #a8d8ea 100%);
      opacity: 0.92;
      z-index: 0;
      pointer-events: none;
      box-shadow: -6px 0 18px rgba(0, 0, 0, 0.12);
    }
""",
    "soft": """
    .slide-cover > .slide-bg::after {
      content: "";
      position: absolute;
      right: -18%;
      top: -12%;
      width: min(62vw, 720px);
      height: min(62vw, 720px);
      border-radius: 50%;
      background: radial-gradient(
        circle at 35% 35%,
        color-mix(in srgb, var(--accent) 22%, transparent) 0%,
        transparent 58%
      );
      z-index: 0;
      pointer-events: none;
    }
""",
    "cyber": """
    .slide-cover > .slide-bg::after {
      content: "";
      position: absolute;
      right: var(--cover-decor-right, 6%);
      top: var(--cover-decor-top, 9%);
      bottom: var(--cover-decor-bottom, auto);
      width: var(--cover-decor-width, clamp(56px, 7vw, 92px));
      height: var(--cover-decor-height, clamp(56px, 7vw, 92px));
      border: 2px solid color-mix(in srgb, var(--accent) 75%, transparent);
      border-top: var(--cover-decor-border-top, 2px solid color-mix(in srgb, var(--accent) 75%, transparent));
      border-right: var(--cover-decor-border-right, 2px solid color-mix(in srgb, var(--accent) 75%, transparent));
      border-bottom: var(--cover-decor-border-bottom, none);
      border-left: var(--cover-decor-border-left, none);
      border-radius: var(--cover-decor-radius, 0 clamp(10px, 1vw, 14px) 0 0);
      opacity: var(--cover-decor-opacity, 0.9);
      z-index: 0;
      pointer-events: none;
      box-shadow: var(--cover-decor-shadow, 0 0 22px color-mix(in srgb, var(--accent) 35%, transparent));
    }
""",
    "minimal": """
    .slide-cover > .slide-bg::after {
      content: "";
      position: absolute;
      left: 0;
      top: 11%;
      bottom: 13%;
      width: 4px;
      border-radius: 0 4px 4px 0;
      background: linear-gradient(
        180deg,
        transparent,
        var(--accent) 45%,
        transparent
      );
      opacity: 0.85;
      z-index: 0;
      pointer-events: none;
    }
""",
}


COVER_DECOR_VARIABLES_BY_SLUG: dict[str, str] = {
    "electric-studio": """
    .slide-cover {
      --cover-decor-left: 12%;
      --cover-decor-right: 55%;
      --cover-decor-bottom: 9%;
      --cover-decor-height: 4px;
      --cover-decor-opacity: 0.72;
    }
""",
    "split-pastel": """
    .slide-cover {
      --cover-decor-left: 46%;
      --cover-decor-right: 11%;
      --cover-decor-bottom: 8%;
      --cover-decor-height: 3px;
      --cover-decor-opacity: 0.68;
      --cover-decor-background: linear-gradient(90deg, transparent, color-mix(in srgb, var(--accent) 65%, #f0b4d4), transparent);
    }
""",
    "dark-botanical": """
    .slide-cover {
      --cover-decor-left: 7%;
      --cover-decor-top: 16%;
      --cover-decor-bottom: 18%;
      --cover-decor-opacity: 0.8;
    }
""",
    "vintage-editorial": """
    .slide-cover {
      --cover-decor-left: 86%;
      --cover-decor-top: 17%;
      --cover-decor-bottom: 20%;
      --cover-decor-shadow-x: -18px;
      --cover-decor-opacity: 0.58;
    }
""",
    "paper-ink": """
    .slide-cover {
      --cover-decor-left: 10%;
      --cover-decor-top: 18%;
      --cover-decor-bottom: 20%;
      --cover-decor-width: 3px;
      --cover-decor-shadow-x: 14px;
      --cover-decor-opacity: 0.72;
    }
""",
    "vellum-navy": """
    .slide-cover {
      --cover-decor-left: 82%;
      --cover-decor-top: 13%;
      --cover-decor-bottom: 17%;
      --cover-decor-width: 3px;
      --cover-decor-opacity: 0.7;
    }
""",
    "terminal-green": """
    .slide-cover {
      --cover-decor-right: 8%;
      --cover-decor-top: auto;
      --cover-decor-bottom: 12%;
      --cover-decor-width: clamp(72px, 9vw, 128px);
      --cover-decor-height: clamp(34px, 4vw, 56px);
      --cover-decor-border-top: none;
      --cover-decor-border-left: 2px solid color-mix(in srgb, var(--accent) 75%, transparent);
      --cover-decor-border-bottom: 2px solid color-mix(in srgb, var(--accent) 75%, transparent);
      --cover-decor-radius: 0 0 0 clamp(10px, 1vw, 14px);
      --cover-decor-opacity: 0.74;
    }
""",
    "studio-volt": """
    .slide-cover {
      --cover-decor-right: 5%;
      --cover-decor-top: 62%;
      --cover-decor-width: clamp(84px, 10vw, 140px);
      --cover-decor-height: clamp(42px, 5vw, 66px);
      --cover-decor-border-left: 2px solid color-mix(in srgb, var(--accent) 75%, transparent);
      --cover-decor-border-bottom: 2px solid color-mix(in srgb, var(--accent) 75%, transparent);
      --cover-decor-radius: 0 clamp(10px, 1vw, 14px) 0 clamp(10px, 1vw, 14px);
      --cover-decor-opacity: 0.76;
    }
""",
    "cobalt-grid": """
    .slide-cover {
      --cover-decor-right: 7%;
      --cover-decor-top: 11%;
      --cover-decor-width: clamp(76px, 8vw, 112px);
      --cover-decor-height: clamp(76px, 8vw, 112px);
      --cover-decor-opacity: 0.66;
      --cover-decor-shadow: 0 0 0 1px color-mix(in srgb, var(--accent) 18%, transparent), 0 0 22px color-mix(in srgb, var(--accent) 24%, transparent);
    }
""",
}


COVER_LAYOUTS_BY_ARCHETYPE = {
    "slab": {"eyebrow": box("7%", "9%", "22%"), "title": box("7%", "24%", "32%"), "subtitle": box("7%", "63%", "27%"), "metrics": box("50%", "69%", "38%", "15%")},
    "horizon": {"eyebrow": box("8%", "10%", "24%"), "title": box("8%", "17%", "43%"), "subtitle": box("56%", "57%", "27%"), "metrics": box("8%", "72%", "40%", "14%")},
    "voltage": {"eyebrow": box("48%", "12%", "28%"), "title": box("8%", "22%", "42%"), "subtitle": box("52%", "25%", "29%"), "metrics": box("52%", "62%", "34%", "17%")},
    "botanical": {"eyebrow": box("13%", "12%", "22%"), "title": box("30%", "24%", "32%"), "subtitle": box("13%", "61%", "26%"), "metrics": box("47%", "66%", "33%", "15%")},
    "notebook": {"eyebrow": box("18%", "13%", "22%"), "title": box("18%", "23%", "28%"), "subtitle": box("50%", "29%", "21%"), "metrics": box("18%", "72%", "43%", "13%")},
    "pastel-card": {"eyebrow": box("13%", "14%", "22%"), "title": box("13%", "22%", "30%"), "subtitle": box("50%", "23%", "24%"), "metrics": box("31%", "70%", "42%", "13%")},
    "diptych": {"eyebrow": box("9%", "12%", "23%"), "title": box("9%", "23%", "35%"), "subtitle": box("57%", "23%", "25%"), "metrics": box("57%", "61%", "30%", "17%")},
    "masthead": {"eyebrow": box("11%", "10%", "70%"), "title": box("11%", "24%", "36%"), "subtitle": box("55%", "31%", "22%"), "metrics": box("11%", "72%", "56%", "12%")},
    "neon-frame": {"eyebrow": box("8%", "11%", "26%"), "title": box("8%", "21%", "34%"), "subtitle": box("8%", "61%", "27%"), "metrics": box("50%", "17%", "34%", "18%")},
    "terminal": {"eyebrow": box("7%", "12%", "34%"), "title": box("7%", "25%", "42%"), "subtitle": box("7%", "58%", "35%"), "metrics": box("54%", "61%", "33%", "17%")},
    "swiss": {"eyebrow": box("12%", "11%", "20%"), "title": box("32%", "16%", "28%"), "subtitle": box("12%", "57%", "22%"), "metrics": box("58%", "57%", "27%", "18%")},
    "paper-rule": {"eyebrow": box("10%", "15%", "24%"), "title": box("10%", "23%", "31%"), "subtitle": box("50%", "28%", "24%"), "metrics": box("10%", "72%", "44%", "13%")},
    "soft-wash": {"eyebrow": box("14%", "13%", "22%"), "title": box("14%", "23%", "31%"), "subtitle": box("47%", "29%", "26%"), "metrics": box("14%", "70%", "46%", "14%")},
    "signal-spine": {"eyebrow": box("12%", "12%", "22%"), "title": box("12%", "25%", "32%"), "subtitle": box("50%", "19%", "25%"), "metrics": box("50%", "59%", "34%", "17%")},
    "studio-scan": {"eyebrow": box("7%", "12%", "24%"), "title": box("7%", "21%", "40%"), "subtitle": box("52%", "18%", "29%"), "metrics": box("52%", "63%", "35%", "15%")},
    "ledger": {"eyebrow": box("11%", "12%", "22%"), "title": box("11%", "23%", "28%"), "subtitle": box("46%", "24%", "23%"), "metrics": box("46%", "61%", "37%", "15%")},
    "neo-brutal": {"eyebrow": box("9%", "9%", "22%"), "title": box("9%", "18%", "35%"), "subtitle": box("58%", "18%", "25%"), "metrics": box("9%", "70%", "50%", "14%")},
    "vellum": {"eyebrow": box("13%", "12%", "23%"), "title": box("13%", "26%", "34%"), "subtitle": box("53%", "30%", "24%"), "metrics": box("13%", "72%", "42%", "13%")},
    "cobalt": {"eyebrow": box("8%", "12%", "22%"), "title": box("8%", "24%", "34%"), "subtitle": box("52%", "23%", "28%"), "metrics": box("52%", "68%", "34%", "14%")},
}


CONTENT_LAYOUTS = {
    "bold": {
        "value": {"number": box("6%", "8%", "24%"), "title": box("8%", "22%", "36%"), "copy": box("8%", "58%", "30%"), "cards": [box("50%", "11%", "16%", "28%"), box("70%", "15%", "18%", "20%"), box("47%", "49%", "22%", "28%"), box("73%", "51%", "16%", "22%")]},
        "workflow": {"number": box("6%", "8%", "22%"), "title": box("31%", "12%", "38%"), "cards": [box("9%", "43%", "18%", "31%"), box("31%", "39%", "18%", "31%"), box("53%", "43%", "18%", "31%"), box("75%", "39%", "16%", "31%")], "note": box("31%", "76%", "38%", "11%")},
        "arch": {"number": box("6%", "8%", "24%"), "title": box("8%", "22%", "40%"), "cards": [box("51%", "14%", "18%", "18%"), box("71%", "14%", "18%", "18%"), box("51%", "39%", "18%", "18%"), box("71%", "39%", "18%", "18%")], "note": box("8%", "72%", "80%", "12%")},
    },
    "split": {
        "value": {"number": box("8%", "9%", "18%"), "title": box("8%", "18%", "32%"), "copy": box("8%", "52%", "27%"), "cards": [box("45%", "14%", "20%", "24%"), box("68%", "14%", "20%", "24%"), box("45%", "47%", "20%", "24%"), box("68%", "47%", "20%", "24%")]},
        "workflow": {"number": box("8%", "9%", "18%"), "title": box("8%", "18%", "34%"), "cards": [box("42%", "13%", "16%", "18%"), box("60%", "28%", "16%", "18%"), box("42%", "47%", "16%", "18%"), box("60%", "62%", "16%", "18%")], "note": box("8%", "70%", "29%", "13%")},
        "arch": {"number": box("8%", "9%", "20%"), "title": box("8%", "18%", "32%"), "cards": [box("45%", "15%", "42%", "13%"), box("45%", "33%", "42%", "13%"), box("45%", "51%", "42%", "13%"), box("45%", "69%", "42%", "13%")], "note": box("8%", "72%", "30%", "12%")},
    },
    "editorial": {
        "value": {"number": box("11%", "11%", "20%"), "title": box("11%", "22%", "37%"), "copy": box("55%", "21%", "23%"), "cards": [box("11%", "65%", "18%", "16%"), box("32%", "65%", "18%", "16%"), box("53%", "65%", "18%", "16%"), box("74%", "65%", "14%", "16%")]},
        "workflow": {"number": box("11%", "11%", "20%"), "title": box("11%", "22%", "32%"), "cards": [box("50%", "14%", "28%", "13%"), box("50%", "32%", "28%", "13%"), box("50%", "50%", "28%", "13%"), box("50%", "68%", "28%", "13%")], "note": box("11%", "69%", "31%", "13%")},
        "arch": {"number": box("11%", "11%", "18%"), "title": box("11%", "22%", "36%"), "cards": [box("12%", "61%", "17%", "17%"), box("33%", "61%", "17%", "17%"), box("54%", "61%", "17%", "17%"), box("75%", "61%", "13%", "17%")], "note": box("53%", "25%", "28%", "17%")},
    },
    "notebook": {
        "value": {"number": box("18%", "13%", "18%"), "title": box("18%", "22%", "27%"), "copy": box("18%", "51%", "24%"), "cards": [box("48%", "18%", "17%", "20%"), box("67%", "18%", "17%", "20%"), box("48%", "45%", "17%", "20%"), box("67%", "45%", "17%", "20%")]},
        "workflow": {"number": box("18%", "13%", "18%"), "title": box("18%", "22%", "27%"), "cards": [box("47%", "17%", "37%", "12%"), box("47%", "33%", "37%", "12%"), box("47%", "49%", "37%", "12%"), box("47%", "65%", "37%", "12%")], "note": box("18%", "69%", "25%", "13%")},
        "arch": {"number": box("18%", "13%", "18%"), "title": box("18%", "22%", "27%"), "cards": [box("48%", "18%", "17%", "18%"), box("67%", "18%", "17%", "18%"), box("48%", "43%", "17%", "18%"), box("67%", "43%", "17%", "18%")], "note": box("18%", "70%", "66%", "11%")},
    },
    "soft": {
        "value": {"number": box("13%", "12%", "18%"), "title": box("13%", "22%", "30%"), "copy": box("52%", "20%", "24%"), "cards": [box("13%", "62%", "18%", "17%"), box("34%", "58%", "18%", "21%"), box("55%", "62%", "18%", "17%"), box("76%", "58%", "12%", "21%")]},
        "workflow": {"number": box("13%", "12%", "18%"), "title": box("13%", "22%", "30%"), "cards": [box("47%", "17%", "17%", "17%"), box("66%", "17%", "17%", "17%"), box("47%", "42%", "17%", "17%"), box("66%", "42%", "17%", "17%")], "note": box("13%", "67%", "31%", "14%")},
        "arch": {"number": box("13%", "12%", "18%"), "title": box("13%", "22%", "31%"), "cards": [box("47%", "16%", "17%", "18%"), box("66%", "16%", "17%", "18%"), box("47%", "41%", "17%", "18%"), box("66%", "41%", "17%", "18%")], "note": box("13%", "69%", "70%", "11%")},
    },
    "cyber": {
        "value": {"number": box("7%", "9%", "22%"), "title": box("7%", "18%", "32%"), "copy": box("7%", "49%", "26%"), "cards": [box("44%", "12%", "20%", "18%"), box("67%", "12%", "20%", "18%"), box("44%", "39%", "20%", "18%"), box("67%", "39%", "20%", "18%")]},
        "workflow": {"number": box("7%", "9%", "22%"), "title": box("7%", "18%", "32%"), "cards": [box("43%", "15%", "44%", "12%"), box("43%", "32%", "44%", "12%"), box("43%", "49%", "44%", "12%"), box("43%", "66%", "44%", "12%")], "note": box("7%", "70%", "31%", "13%")},
        "arch": {"number": box("7%", "9%", "22%"), "title": box("7%", "18%", "32%"), "cards": [box("43%", "14%", "20%", "18%"), box("67%", "14%", "20%", "18%"), box("43%", "41%", "20%", "18%"), box("67%", "41%", "20%", "18%")], "note": box("7%", "70%", "80%", "12%")},
    },
    "minimal": {
        "value": {"number": box("10%", "10%", "17%"), "title": box("10%", "20%", "27%"), "copy": box("10%", "52%", "24%"), "cards": [box("46%", "18%", "14%", "20%"), box("62%", "18%", "14%", "20%"), box("46%", "46%", "14%", "20%"), box("62%", "46%", "14%", "20%")]},
        "workflow": {"number": box("10%", "10%", "17%"), "title": box("10%", "20%", "29%"), "cards": [box("45%", "18%", "38%", "10%"), box("45%", "33%", "38%", "10%"), box("45%", "48%", "38%", "10%"), box("45%", "63%", "38%", "10%")], "note": box("10%", "72%", "29%", "12%")},
        "arch": {"number": box("10%", "10%", "17%"), "title": box("10%", "20%", "30%"), "cards": [box("45%", "18%", "18%", "16%"), box("65%", "18%", "18%", "16%"), box("45%", "43%", "18%", "16%"), box("65%", "43%", "18%", "16%")], "note": box("10%", "70%", "73%", "12%")},
    },
}


def cover_slide(slide_index: int, preset: Preset, layout: dict[str, str]) -> str:
    builder = SlideBuilder(
        slide_index,
        f"slide-cover cover-{preset.cover_archetype} layout-{preset.content_archetype}",
    )
    builder.text("eyebrow", layout["eyebrow"], f"{preset.title} / README deck")
    builder.text("hero-title", layout["title"], "Frontend Slides<br>Editable")
    builder.text(
        "hero-subtitle",
        layout["subtitle"],
        "中文为主，英文做轻量标签。可编辑 runtime 保留在单文件 HTML 里。",
    )
    builder.text("metric-box", layout["metrics"], metric_html())
    return builder.render()


def value_slide(slide_index: int, preset: Preset, layout: dict[str, object]) -> str:
    builder = SlideBuilder(slide_index, f"slide-value layout-{preset.content_archetype}")
    builder.text("section-number", layout["number"], "01 / Fork logic")
    builder.text("section-title", layout["title"], "区别不在能不能生成，而在生成后还要不要继续改")
    builder.text(
        "section-copy",
        layout["copy"],
        "README 把它定义成 <strong>frontend-slides</strong> 的可编辑分支：保留 style discovery、viewport discipline 与 PPT conversion，同时加入完整浏览器编辑 runtime。",
    )
    card_classes = ["panel-card accent-card", "panel-card", "panel-card", "panel-card"]
    for style, card, cls in zip(layout["cards"], VALUE_CARDS, card_classes):
        builder.text(cls, style, card_html(*card))
    return builder.render()


def workflow_slide(slide_index: int, preset: Preset, layout: dict[str, object]) -> str:
    builder = SlideBuilder(slide_index, f"slide-workflow layout-{preset.content_archetype}")
    builder.text("section-number", layout["number"], "02 / Workflow")
    builder.text("section-title", layout["title"], "先做 discovery，再选 preset，再把最后一轮修改留给浏览器")
    for style, card in zip(layout["cards"], WORKFLOW_CARDS):
        builder.text("workflow-card", style, workflow_card_html(*card))
    builder.text(
        "note-card accent-card",
        layout["note"],
        note_card_html(
            "Editing controls",
            "进入编辑后，布局和文字都还可以继续收口，而不是生成后立刻冻结。",
            ["E", "Pages", "Ctrl+click", "Ctrl+S", "Export HTML"],
        ),
    )
    return builder.render()


def arch_slide(slide_index: int, preset: Preset, layout: dict[str, object]) -> str:
    builder = SlideBuilder(slide_index, f"slide-architecture layout-{preset.content_archetype}")
    builder.text("section-number", layout["number"], "03 / Runtime contract")
    builder.text("section-title", layout["title"], "真正不能丢的是结构契约、视口纪律和 preset identity")
    for style, card in zip(layout["cards"], ARCH_CARDS):
        builder.text("arch-card", style, card_html(*card))
    builder.text("closing-note", layout["note"], arch_note_html(preset.title))
    return builder.render()


def render_deck(preset: Preset) -> str:
    cover_layout = COVER_LAYOUTS_BY_ARCHETYPE[preset.cover_archetype]
    layout = CONTENT_LAYOUTS[preset.content_archetype]
    slides = [
        cover_slide(0, preset, cover_layout),
        value_slide(1, preset, layout["value"]),
        workflow_slide(2, preset, layout["workflow"]),
        arch_slide(3, preset, layout["arch"]),
    ]
    return '<div class="slides-offset">\n' + "\n".join(slides) + "\n</div>"


PRESETS = [
    Preset(
        slug="bold-signal",
        title="Bold Signal",
        family="bold",
        cover_archetype="slab",
        content_archetype="bold",
        light_chrome=False,
        accent="#ff5722",
        root_lines="""      --font-display: 'Archivo Black', sans-serif;
      --font-body: 'Space Grotesk', sans-serif;
      --slide-bg-deep: #151515;
      --slide-bg-gradient: linear-gradient(135deg, #151515 0%, #2a2a2a 55%, #151515 100%);
      --text-primary: #fff8f4;
      --text-secondary: #dfd1c7;
      --text-muted: #b89d8f;
      --text-on-accent: #1a1a1a;
      --accent: #ff5722;
      --surface: rgba(18, 18, 18, 0.72);
      --surface-strong: rgba(255, 255, 255, 0.06);
      --line: rgba(255, 255, 255, 0.12);
      --panel-shadow: 0 22px 44px rgba(0, 0, 0, 0.26);
""",
        theme_css="""
    .slide { background: var(--slide-bg-gradient); }
    .slide::before {
      content: "";
      position: absolute;
      inset: 0;
      background-image:
        linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px);
      background-size: clamp(24px, 3vw, 44px) clamp(24px, 3vw, 44px);
      opacity: 0.32;
      z-index: 0;
      pointer-events: none;
    }
    .slide-cover::after {
      content: "";
      position: absolute;
      right: 7%;
      top: 14%;
      width: min(32vw, 380px);
      height: min(58vh, 460px);
      background: var(--accent);
      border-radius: 16px;
      z-index: 1;
      opacity: 0.95;
    }
    .slide-cover > .slide-bg::after {
      content: "";
      position: absolute;
      left: 60%;
      top: 20%;
      width: 24%;
      height: 34%;
      border-radius: clamp(12px, 1.6vw, 24px);
      border: 1px solid rgba(0, 0, 0, 0.08);
      background:
        linear-gradient(180deg, rgba(0,0,0,0.16), rgba(0,0,0,0.04)),
        repeating-linear-gradient(90deg, rgba(0,0,0,0.24), rgba(0,0,0,0.24) 16%, transparent 16%, transparent 31%);
      box-shadow: 0 18px 36px rgba(0, 0, 0, 0.22);
      z-index: 0;
      pointer-events: none;
    }
    .panel-card .slide-object-text,
    .workflow-card .slide-object-text,
    .arch-card .slide-object-text,
    .metric-box .slide-object-text,
    .closing-note .slide-object-text {
      border-top: 4px solid var(--accent);
    }
""",
        google_url="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Space+Grotesk:wght@400;500&display=swap",
    ),
    Preset(
        slug="electric-studio",
        title="Electric Studio",
        family="split",
        cover_archetype="horizon",
        content_archetype="split",
        light_chrome=True,
        accent="#4361ee",
        root_lines="""      --font-display: 'Manrope', sans-serif;
      --font-body: 'Manrope', sans-serif;
      --slide-bg-deep: #ffffff;
      --slide-bg-gradient: linear-gradient(180deg, #ffffff 0%, #ffffff 51%, #4361ee 51%, #4361ee 100%);
      --text-primary: #0a0a0a;
      --text-secondary: #1b2858;
      --text-muted: #5c6fab;
      --text-on-accent: #ffffff;
      --accent: #4361ee;
      --surface: rgba(255, 255, 255, 0.84);
      --surface-strong: rgba(67, 97, 238, 0.08);
      --line: rgba(15, 23, 42, 0.12);
      --panel-shadow: 0 16px 34px rgba(15, 23, 42, 0.08);
""",
        theme_css="""
    .slide { background: var(--slide-bg-gradient); }
    .slide::after {
      content: "";
      position: absolute;
      left: 0;
      right: 0;
      top: 51%;
      height: 2px;
      background: rgba(10, 10, 10, 0.08);
      z-index: 1;
    }
    .slide-cover::before {
      content: "";
      position: absolute;
      top: 7%;
      right: 8%;
      width: clamp(18px, 2.4vw, 28px);
      height: clamp(18px, 2.4vw, 28px);
      border: 3px solid rgba(10, 10, 10, 0.12);
      z-index: 1;
    }
    .slide-cover > .slide-bg::after {
      content: "";
      position: absolute;
      left: 57%;
      top: 14%;
      width: 31%;
      height: 62%;
      background: linear-gradient(180deg, #0a0a0a 0%, #0a0a0a 58%, #4361ee 58%, #4361ee 100%);
      border-radius: 0;
      box-shadow: 0 20px 50px rgba(10, 10, 10, 0.12);
      z-index: 0;
      pointer-events: none;
    }
    .panel-card .slide-object-text,
    .workflow-card .slide-object-text,
    .arch-card .slide-object-text {
      border-left: 5px solid var(--accent);
    }
""",
        google_url="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;800&display=swap",
    ),
    Preset(
        slug="creative-voltage",
        title="Creative Voltage",
        family="split",
        cover_archetype="voltage",
        content_archetype="split",
        light_chrome=False,
        accent="#d4ff00",
        root_lines="""      --font-display: 'Syne', sans-serif;
      --font-body: 'Space Mono', monospace;
      --slide-bg-deep: #1a1a2e;
      --slide-bg-gradient: linear-gradient(90deg, #0066ff 0%, #0066ff 38%, #1a1a2e 38%, #1a1a2e 100%);
      --text-primary: #ffffff;
      --text-secondary: #d4dcff;
      --text-muted: #b2b9ff;
      --text-on-accent: #0f1020;
      --accent: #d4ff00;
      --surface: rgba(12, 16, 44, 0.78);
      --surface-strong: rgba(212, 255, 0, 0.08);
      --line: rgba(255, 255, 255, 0.12);
      --panel-shadow: 0 20px 40px rgba(0, 0, 0, 0.25);
""",
        theme_css="""
    .slide { background: var(--slide-bg-gradient); }
    .slide::before {
      content: "";
      position: absolute;
      inset: 0;
      background-image: radial-gradient(circle, rgba(255,255,255,0.08) 1px, transparent 1px);
      background-size: clamp(10px, 1.5vw, 16px) clamp(10px, 1.5vw, 16px);
      opacity: 0.35;
      z-index: 0;
    }
    .slide-cover > .slide-bg::after {
      content: "";
      position: absolute;
      left: 57%;
      top: 14%;
      width: 31%;
      height: 62%;
      background:
        linear-gradient(135deg, rgba(212,255,0,0.8), rgba(212,255,0,0.22)),
        linear-gradient(180deg, rgba(255,255,255,0.06), transparent);
      border: 1px solid rgba(212,255,0,0.45);
      box-shadow: 0 0 0 1px rgba(212,255,0,0.16), 0 18px 36px rgba(0,0,0,0.22);
      z-index: 0;
      pointer-events: none;
    }
    .panel-card .slide-object-text,
    .workflow-card .slide-object-text,
    .arch-card .slide-object-text,
    .metric-box .slide-object-text {
      border-top: 3px solid var(--accent);
    }
""",
        google_url="https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700&family=Syne:wght@700;800&display=swap",
    ),
    Preset(
        slug="dark-botanical",
        title="Dark Botanical",
        family="editorial",
        cover_archetype="botanical",
        content_archetype="editorial",
        light_chrome=False,
        accent="#d4a574",
        root_lines="""      --font-display: 'Cormorant', serif;
      --font-body: 'IBM Plex Sans', sans-serif;
      --slide-bg-deep: #0f0f0f;
      --slide-bg-gradient: #0f0f0f;
      --text-primary: #e8e4df;
      --text-secondary: #c6bfb8;
      --text-muted: #a99f96;
      --text-on-accent: #181410;
      --accent: #d4a574;
      --surface: rgba(23, 23, 23, 0.76);
      --surface-strong: rgba(212, 165, 116, 0.08);
      --line: rgba(255, 255, 255, 0.1);
      --panel-shadow: 0 22px 40px rgba(0, 0, 0, 0.28);
""",
        theme_css="""
    .slide { background: #0f0f0f; }
    .slide::before,
    .slide::after {
      content: "";
      position: absolute;
      border-radius: 50%;
      filter: blur(70px);
      opacity: 0.52;
      pointer-events: none;
      z-index: 0;
    }
    .slide::before {
      width: 40vw;
      height: 40vw;
      background: rgba(232, 180, 184, 0.9);
      right: -12%;
      top: -8%;
    }
    .slide::after {
      width: 34vw;
      height: 34vw;
      background: rgba(201, 184, 150, 0.9);
      left: -10%;
      bottom: -16%;
    }
    .hero-title .slide-object-text {
      font-style: italic;
    }
    .panel-card .slide-object-text,
    .workflow-card .slide-object-text,
    .arch-card .slide-object-text {
      border-left: 1px solid var(--accent);
    }
    .slide-cover > .slide-bg::after {
      content: "";
      position: absolute;
      left: 62%;
      top: 18%;
      width: 18%;
      height: 56%;
      background: linear-gradient(135deg, rgba(212,165,116,0.16), rgba(232,180,184,0.12));
      border: 1px solid rgba(255,255,255,0.12);
      z-index: 0;
      pointer-events: none;
    }
""",
        google_url="https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Sans:wght@300;400&display=swap",
    ),
    Preset(
        slug="notebook-tabs",
        title="Notebook Tabs",
        family="notebook",
        cover_archetype="notebook",
        content_archetype="notebook",
        light_chrome=True,
        accent="#5a7c6a",
        root_lines="""      --font-display: 'Bodoni Moda', serif;
      --font-body: 'DM Sans', sans-serif;
      --slide-bg-deep: #2d2d2d;
      --slide-bg-gradient: #2d2d2d;
      --text-primary: #1a1a1a;
      --text-secondary: #4f4a44;
      --text-muted: #7e7468;
      --text-on-accent: #ffffff;
      --accent: #5a7c6a;
      --surface: rgba(248, 246, 241, 0.92);
      --surface-strong: rgba(90, 124, 106, 0.08);
      --line: rgba(26, 26, 26, 0.12);
      --panel-shadow: 0 18px 40px rgba(0, 0, 0, 0.12);
""",
        theme_css="""
    .slide { background: #2d2d2d; }
    .slide::before {
      content: "";
      position: absolute;
      left: 50%;
      top: 50%;
      transform: translate(-50%, -50%);
      width: min(76vw, 980px);
      height: min(78vh, 650px);
      background: #f8f6f1;
      border-radius: 16px;
      box-shadow: 0 18px 60px rgba(0, 0, 0, 0.28);
      z-index: 0;
    }
    .slide::after {
      content: "";
      position: absolute;
      right: calc(50% - min(76vw, 980px) / 2 + 10px);
      top: 50%;
      transform: translateY(-50%);
      width: clamp(18px, 2vw, 24px);
      height: min(52vh, 420px);
      border-radius: 8px;
      background: linear-gradient(180deg, #98d4bb, #c7b8ea, #f4b8c5, #a8d8ea, #ffe6a7);
      z-index: 1;
    }
    .slide-cover > .slide-bg::after {
      content: "";
      position: absolute;
      left: 69%;
      top: 18%;
      width: 10%;
      height: 56%;
      background: linear-gradient(180deg, rgba(90,124,106,0.12), rgba(90,124,106,0.02));
      border: 1px dashed rgba(26,26,26,0.2);
      z-index: 0;
      pointer-events: none;
    }
""",
        google_url="https://fonts.googleapis.com/css2?family=Bodoni+Moda:wght@400;700&family=DM+Sans:wght@400;500&display=swap",
    ),
    Preset(
        slug="pastel-geometry",
        title="Pastel Geometry",
        family="soft",
        cover_archetype="pastel-card",
        content_archetype="soft",
        light_chrome=True,
        accent="#7c6aad",
        root_lines="""      --font-display: 'Plus Jakarta Sans', sans-serif;
      --font-body: 'Plus Jakarta Sans', sans-serif;
      --slide-bg-deep: #c8d9e6;
      --slide-bg-gradient: #c8d9e6;
      --text-primary: #1a1a1a;
      --text-secondary: #4f5961;
      --text-muted: #6f7d88;
      --text-on-accent: #ffffff;
      --accent: #7c6aad;
      --surface: rgba(250, 249, 247, 0.92);
      --surface-strong: rgba(124, 106, 173, 0.08);
      --line: rgba(26, 26, 26, 0.1);
      --panel-shadow: 0 18px 40px rgba(38, 53, 67, 0.12);
""",
        theme_css="""
    .slide { background: #c8d9e6; }
    .slide::before {
      content: "";
      position: absolute;
      left: 50%;
      top: 50%;
      transform: translate(-50%, -50%);
      width: min(78vw, 960px);
      height: min(78vh, 640px);
      background: #faf9f7;
      border-radius: 28px;
      box-shadow: 0 18px 48px rgba(38, 53, 67, 0.12);
      z-index: 0;
    }
    .slide::after {
      content: "";
      position: absolute;
      right: calc(50% - min(78vw, 960px) / 2 + 16px);
      top: 50%;
      transform: translateY(-50%);
      width: clamp(16px, 2vw, 24px);
      height: min(52vh, 420px);
      border-radius: 999px;
      background:
        linear-gradient(180deg, #f0b4d4 0%, #f0b4d4 16%, transparent 16%, transparent 22%, #a8d4c4 22%, #a8d4c4 46%, transparent 46%, transparent 54%, #7c6aad 54%, #7c6aad 100%);
      z-index: 1;
    }
    .slide-cover > .slide-bg::after {
      content: "";
      position: absolute;
      left: 70%;
      top: 18%;
      width: 10%;
      height: 56%;
      background: linear-gradient(180deg, rgba(124,106,173,0.16), rgba(168,212,196,0.12));
      border: 1px solid rgba(26,26,26,0.08);
      border-radius: 28px;
      z-index: 0;
      pointer-events: none;
    }
""",
        google_url="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;700;800&display=swap",
    ),
    Preset(
        slug="split-pastel",
        title="Split Pastel",
        family="split",
        cover_archetype="diptych",
        content_archetype="split",
        light_chrome=True,
        accent="#5a7c6a",
        root_lines="""      --font-display: 'Outfit', sans-serif;
      --font-body: 'Outfit', sans-serif;
      --slide-bg-deep: #f5e6dc;
      --slide-bg-gradient: linear-gradient(90deg, #f5e6dc 0%, #f5e6dc 50%, #e4dff0 50%, #e4dff0 100%);
      --text-primary: #1a1a1a;
      --text-secondary: #5b5462;
      --text-muted: #7f7285;
      --text-on-accent: #ffffff;
      --accent: #5a7c6a;
      --surface: rgba(255, 255, 255, 0.78);
      --surface-strong: rgba(90, 124, 106, 0.08);
      --line: rgba(26, 26, 26, 0.1);
      --panel-shadow: 0 16px 36px rgba(68, 61, 74, 0.12);
""",
        theme_css="""
    .slide { background: var(--slide-bg-gradient); }
    .slide::before {
      content: "";
      position: absolute;
      right: 8%;
      top: 18%;
      width: min(30vw, 360px);
      height: min(44vh, 320px);
      background-image:
        linear-gradient(rgba(26,26,26,0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(26,26,26,0.06) 1px, transparent 1px);
      background-size: 18px 18px;
      z-index: 0;
    }
    .slide-cover > .slide-bg::after {
      content: "";
      position: absolute;
      left: 57%;
      top: 14%;
      width: 31%;
      height: 62%;
      background: linear-gradient(135deg, rgba(200,240,216,0.84), rgba(240,212,224,0.6));
      border: 1px solid rgba(26,26,26,0.08);
      box-shadow: 0 16px 30px rgba(68, 61, 74, 0.1);
      z-index: 0;
      pointer-events: none;
    }
""",
        google_url="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;700;800&display=swap",
    ),
    Preset(
        slug="vintage-editorial",
        title="Vintage Editorial",
        family="editorial",
        cover_archetype="masthead",
        content_archetype="editorial",
        light_chrome=True,
        accent="#1a1a1a",
        root_lines="""      --font-display: 'Fraunces', serif;
      --font-body: 'Work Sans', sans-serif;
      --slide-bg-deep: #f5f3ee;
      --slide-bg-gradient: #f5f3ee;
      --text-primary: #1a1a1a;
      --text-secondary: #514b44;
      --text-muted: #7a6f63;
      --text-on-accent: #ffffff;
      --accent: #1a1a1a;
      --surface: rgba(255, 255, 255, 0.74);
      --surface-strong: rgba(26, 26, 26, 0.06);
      --line: rgba(26, 26, 26, 0.14);
      --panel-shadow: 0 18px 34px rgba(26, 26, 26, 0.08);
""",
        theme_css="""
    .slide { background: #f5f3ee; }
    .slide::before {
      content: "";
      position: absolute;
      right: 8%;
      top: 12%;
      width: clamp(88px, 12vw, 140px);
      height: clamp(88px, 12vw, 140px);
      border: 2px solid rgba(26, 26, 26, 0.3);
      border-radius: 50%;
      z-index: 0;
    }
    .slide::after {
      content: "";
      position: absolute;
      left: 12%;
      bottom: 16%;
      width: 20%;
      height: 2px;
      background: rgba(26, 26, 26, 0.28);
      z-index: 0;
    }
    .slide-cover > .slide-bg::after {
      content: "";
      position: absolute;
      left: 62%;
      top: 18%;
      width: 18%;
      height: 56%;
      background: linear-gradient(180deg, rgba(232,212,192,0.62), rgba(255,255,255,0.0));
      border: 2px solid rgba(26, 26, 26, 0.18);
      border-radius: 999px;
      z-index: 0;
      pointer-events: none;
    }
    .panel-card .slide-object-text,
    .workflow-card .slide-object-text,
    .arch-card .slide-object-text {
      border: 2px solid rgba(26, 26, 26, 0.14);
      box-shadow: none;
    }
""",
        google_url="https://fonts.googleapis.com/css2?family=Fraunces:wght@700;900&family=Work+Sans:wght@400;500&display=swap",
    ),
    Preset(
        slug="neon-cyber",
        title="Neon Cyber",
        family="cyber",
        cover_archetype="neon-frame",
        content_archetype="cyber",
        light_chrome=False,
        accent="#00ffcc",
        root_lines="""      --font-display: 'Clash Display', sans-serif;
      --font-body: 'Satoshi', sans-serif;
      --slide-bg-deep: #0a0f1c;
      --slide-bg-gradient: radial-gradient(ellipse 120% 80% at 50% 20%, #122038 0%, #0a0f1c 55%);
      --text-primary: #e2e8f0;
      --text-secondary: #b8c4d8;
      --text-muted: #7a92b8;
      --text-on-accent: #021b18;
      --accent: #00ffcc;
      --surface: rgba(8, 15, 31, 0.74);
      --surface-strong: rgba(0, 255, 204, 0.08);
      --line: rgba(0, 255, 204, 0.22);
      --panel-shadow: 0 20px 42px rgba(0, 0, 0, 0.28);
""",
        theme_css="""
    .slide { background: var(--slide-bg-gradient); }
    .slide::before {
      content: "";
      position: absolute;
      inset: 0;
      background-image:
        linear-gradient(rgba(0,255,204,0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,0,170,0.06) 1px, transparent 1px);
      background-size: clamp(30px, 4vw, 48px) clamp(30px, 4vw, 48px);
      z-index: 0;
      opacity: 0.44;
    }
    .slide-cover > .slide-bg::after {
      content: "";
      position: absolute;
      left: 58%;
      top: 18%;
      width: 28%;
      height: 54%;
      background:
        radial-gradient(circle at 30% 30%, rgba(0,255,204,0.34), transparent 46%),
        linear-gradient(135deg, rgba(255,0,170,0.18), rgba(0,255,204,0.08));
      border: 1px solid rgba(0,255,204,0.35);
      box-shadow: 0 0 30px rgba(0,255,204,0.12);
      z-index: 0;
      pointer-events: none;
    }
    .panel-card .slide-object-text,
    .workflow-card .slide-object-text,
    .arch-card .slide-object-text,
    .metric-box .slide-object-text,
    .closing-note .slide-object-text {
      box-shadow: 0 0 0 1px rgba(0,255,204,0.14), 0 16px 30px rgba(0,0,0,0.26);
    }
""",
        google_url=None,
    ),
    Preset(
        slug="terminal-green",
        title="Terminal Green",
        family="cyber",
        cover_archetype="terminal",
        content_archetype="cyber",
        light_chrome=False,
        accent="#39d353",
        root_lines="""      --font-display: 'JetBrains Mono', monospace;
      --font-body: 'JetBrains Mono', monospace;
      --slide-bg-deep: #0d1117;
      --slide-bg-gradient: #0d1117;
      --text-primary: #39d353;
      --text-secondary: #8be39a;
      --text-muted: #5bc96a;
      --text-on-accent: #07130a;
      --accent: #39d353;
      --surface: rgba(3, 10, 6, 0.8);
      --surface-strong: rgba(57, 211, 83, 0.08);
      --line: rgba(57, 211, 83, 0.18);
      --panel-shadow: 0 18px 34px rgba(0, 0, 0, 0.3);
""",
        theme_css="""
    .slide { background: #0d1117; }
    .slide::before {
      content: "";
      position: absolute;
      inset: 0;
      background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(57, 211, 83, 0.04) 2px,
        rgba(57, 211, 83, 0.04) 3px
      );
      z-index: 0;
    }
    .slide-cover > .slide-bg::after {
      content: "";
      position: absolute;
      left: 58%;
      top: 18%;
      width: 28%;
      height: 54%;
      background:
        linear-gradient(180deg, rgba(57,211,83,0.12), rgba(57,211,83,0.04)),
        linear-gradient(180deg, #101a12 0%, #0d1117 100%);
      border: 1px solid rgba(57, 211, 83, 0.3);
      box-shadow: inset 0 0 0 1px rgba(57, 211, 83, 0.08);
      z-index: 0;
      pointer-events: none;
    }
    .label,
    .section-number .slide-object-text,
    .eyebrow .slide-object-text,
    .metric-note,
    .body {
      letter-spacing: 0;
    }
""",
        google_url="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap",
    ),
    Preset(
        slug="swiss-modern",
        title="Swiss Modern",
        family="minimal",
        cover_archetype="swiss",
        content_archetype="minimal",
        light_chrome=True,
        accent="#ff3300",
        root_lines="""      --font-display: 'Archivo', sans-serif;
      --font-body: 'Nunito', sans-serif;
      --slide-bg-deep: #ffffff;
      --slide-bg-gradient: #ffffff;
      --text-primary: #000000;
      --text-secondary: #404040;
      --text-muted: #6c6c6c;
      --text-on-accent: #ffffff;
      --accent: #ff3300;
      --surface: rgba(255, 255, 255, 0.9);
      --surface-strong: rgba(255, 51, 0, 0.06);
      --line: rgba(0, 0, 0, 0.12);
      --panel-shadow: none;
""",
        theme_css="""
    .slide { background: #ffffff; }
    .slide::before {
      content: "";
      position: absolute;
      inset: 0;
      background-image:
        linear-gradient(rgba(0,0,0,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,0,0,0.05) 1px, transparent 1px);
      background-size: clamp(28px, 4vw, 52px) clamp(28px, 4vw, 52px);
      z-index: 0;
      opacity: 0.6;
    }
    .slide::after {
      content: "";
      position: absolute;
      left: 0;
      top: 0;
      width: clamp(8px, 1vw, 14px);
      height: 100%;
      background: var(--accent);
      z-index: 1;
    }
    .panel-card .slide-object-text,
    .workflow-card .slide-object-text,
    .arch-card .slide-object-text,
    .metric-box .slide-object-text,
    .closing-note .slide-object-text {
      box-shadow: none;
      border-radius: 0;
    }
    .slide-cover > .slide-bg::after {
      content: "";
      position: absolute;
      left: 63%;
      top: 18%;
      width: 14%;
      height: 52%;
      background:
        linear-gradient(90deg, rgba(255,51,0,0.94) 0 14%, transparent 14% 100%),
        linear-gradient(180deg, rgba(0,0,0,0.04), rgba(0,0,0,0.01));
      border-radius: 0;
      border: 1px solid rgba(0, 0, 0, 0.08);
      z-index: 0;
      pointer-events: none;
    }
""",
        google_url="https://fonts.googleapis.com/css2?family=Archivo:wght@800&family=Nunito:wght@400;500&display=swap",
    ),
    Preset(
        slug="paper-ink",
        title="Paper & Ink",
        family="editorial",
        cover_archetype="paper-rule",
        content_archetype="editorial",
        light_chrome=True,
        accent="#c41e3a",
        root_lines="""      --font-display: 'Cormorant Garamond', serif;
      --font-body: 'Source Serif 4', serif;
      --slide-bg-deep: #faf9f7;
      --slide-bg-gradient: #faf9f7;
      --text-primary: #1a1a1a;
      --text-secondary: #544c45;
      --text-muted: #7b7067;
      --text-on-accent: #ffffff;
      --accent: #c41e3a;
      --surface: rgba(255, 255, 255, 0.7);
      --surface-strong: rgba(196, 30, 58, 0.06);
      --line: rgba(26, 26, 26, 0.12);
      --panel-shadow: 0 16px 30px rgba(26, 26, 26, 0.08);
""",
        theme_css="""
    .slide { background: #faf9f7; }
    .slide::before {
      content: "";
      position: absolute;
      left: 10%;
      top: 72%;
      width: 38%;
      height: 3px;
      background: rgba(196, 30, 58, 0.82);
      z-index: 0;
    }
    .slide::after {
      content: "";
      position: absolute;
      right: 10%;
      top: 12%;
      width: 24%;
      height: 1px;
      background: rgba(26, 26, 26, 0.16);
      z-index: 0;
    }
    .hero-title .slide-object-text {
      font-style: italic;
    }
    .slide-cover > .slide-bg::after {
      content: "";
      position: absolute;
      left: 62%;
      top: 18%;
      width: 18%;
      height: 56%;
      background: linear-gradient(180deg, rgba(196,30,58,0.08), transparent);
      border: 1px solid rgba(26,26,26,0.08);
      z-index: 0;
      pointer-events: none;
    }
    .panel-card .slide-object-text,
    .workflow-card .slide-object-text,
    .arch-card .slide-object-text,
    .closing-note .slide-object-text {
      border-top: 3px solid rgba(196, 30, 58, 0.72);
    }
""",
        google_url="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&family=Source+Serif+4:wght@400;600&display=swap",
    ),
    Preset(
        slug="soft-editorial",
        title="Soft Editorial",
        family="soft",
        cover_archetype="soft-wash",
        content_archetype="soft",
        light_chrome=True,
        accent="#7d9b76",
        root_lines="""      --font-display: 'Cormorant Garamond', serif;
      --font-body: 'Nunito Sans', sans-serif;
      --slide-bg-deep: #f4f0e8;
      --slide-bg-gradient: linear-gradient(165deg, #f4f0e8 0%, #ebe4d6 55%, #f7f4ec 100%);
      --text-primary: #2d2822;
      --text-secondary: #4f4a42;
      --text-muted: #7a7268;
      --text-on-accent: #f4f0e8;
      --accent: #7d9b76;
      --surface: rgba(255, 255, 255, 0.78);
      --surface-strong: rgba(125, 155, 118, 0.1);
      --line: rgba(45, 40, 34, 0.1);
      --panel-shadow: 0 14px 36px rgba(45, 40, 34, 0.08);
""",
        theme_css="""
    .slide { background: var(--slide-bg-gradient); }
    .slide::before {
      content: "";
      position: absolute;
      right: 10%;
      top: 12%;
      width: 32%;
      height: 48%;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(232,180,184,0.38), transparent 70%);
      z-index: 0;
    }
    .slide::after {
      content: "";
      position: absolute;
      left: 8%;
      bottom: 16%;
      width: 24%;
      height: 3px;
      background: linear-gradient(90deg, var(--accent), rgba(237, 220, 140, 0.9));
      z-index: 0;
    }
    .slide-cover > .slide-bg::after {
      content: "";
      position: absolute;
      left: 70%;
      top: 18%;
      width: 10%;
      height: 56%;
      background: linear-gradient(135deg, rgba(125,155,118,0.22), rgba(237,220,140,0.16));
      border: 1px solid rgba(45, 40, 34, 0.08);
      z-index: 0;
      pointer-events: none;
    }
    .hero-title .slide-object-text { font-style: italic; }
""",
        google_url="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&family=Nunito+Sans:wght@400;600&display=swap",
    ),
    Preset(
        slug="signal-gold",
        title="Signal",
        family="bold",
        cover_archetype="signal-spine",
        content_archetype="bold",
        light_chrome=False,
        accent="#c9a227",
        root_lines="""      --font-display: 'Libre Baskerville', serif;
      --font-body: 'Source Sans 3', sans-serif;
      --slide-bg-deep: #0b1220;
      --slide-bg-gradient: linear-gradient(155deg, #0f172a 0%, #0b1220 50%, #111827 100%);
      --text-primary: #e8e4dc;
      --text-secondary: #b8b4ac;
      --text-muted: #8a8680;
      --text-on-accent: #0b1220;
      --accent: #c9a227;
      --surface: rgba(15, 23, 42, 0.72);
      --surface-strong: rgba(201, 162, 39, 0.1);
      --line: rgba(232, 228, 220, 0.12);
      --panel-shadow: 0 18px 40px rgba(0, 0, 0, 0.35);
""",
        theme_css="""
    .slide { background: var(--slide-bg-gradient); }
    .slide::before {
      content: "";
      position: absolute;
      left: 0;
      top: 0;
      width: 4px;
      height: 100%;
      background: linear-gradient(180deg, var(--accent), transparent);
      z-index: 1;
      opacity: 0.85;
    }
    .slide-cover > .slide-bg::after {
      content: "";
      position: absolute;
      left: 60%;
      top: 20%;
      width: 24%;
      height: 34%;
      border-radius: clamp(12px, 1.6vw, 24px);
      background:
        radial-gradient(circle at 40% 35%, rgba(201,162,39,0.2), transparent 55%),
        linear-gradient(135deg, rgba(15,23,42,0.9), rgba(11,18,32,0.95));
      border: 1px solid rgba(201, 162, 39, 0.25);
      z-index: 0;
      pointer-events: none;
    }
    .section-number .slide-object-text { color: var(--accent); }
""",
        google_url="https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&family=Source+Sans+3:wght@400;600&display=swap",
    ),
    Preset(
        slug="studio-volt",
        title="Studio",
        family="cyber",
        cover_archetype="studio-scan",
        content_archetype="cyber",
        light_chrome=False,
        accent="#f5e000",
        root_lines="""      --font-display: 'Bebas Neue', sans-serif;
      --font-body: 'Barlow', sans-serif;
      --slide-bg-deep: #050505;
      --slide-bg-gradient: #050505;
      --text-primary: #f5e000;
      --text-secondary: #e8e088;
      --text-muted: #a39e5c;
      --text-on-accent: #050505;
      --accent: #f5e000;
      --surface: rgba(12, 12, 12, 0.88);
      --surface-strong: rgba(245, 224, 0, 0.08);
      --line: rgba(245, 224, 0, 0.2);
      --panel-shadow: 0 0 40px rgba(245, 224, 0, 0.06);
""",
        theme_css="""
    .slide { background: var(--slide-bg-gradient); }
    .slide::before {
      content: "";
      position: absolute;
      inset: 0;
      background-image: linear-gradient(rgba(245,224,0,0.04) 1px, transparent 1px);
      background-size: 100% clamp(28px, 4vh, 44px);
      z-index: 0;
      pointer-events: none;
    }
    .slide-cover > .slide-bg::after {
      content: "";
      position: absolute;
      left: 58%;
      top: 18%;
      width: 28%;
      height: 54%;
      background: linear-gradient(135deg, rgba(245,224,0,0.95), rgba(245,224,0,0.15));
      border: 2px solid rgba(245, 224, 0, 0.5);
      box-shadow: 0 0 30px rgba(245, 224, 0, 0.15);
      z-index: 0;
      pointer-events: none;
    }
    .hero-title .slide-object-text { letter-spacing: 0.02em; }
""",
        google_url="https://fonts.googleapis.com/css2?family=Barlow:wght@400;600&family=Bebas+Neue&display=swap",
    ),
    Preset(
        slug="monochrome-ledger",
        title="Monochrome",
        family="minimal",
        cover_archetype="ledger",
        content_archetype="minimal",
        light_chrome=True,
        accent="#111111",
        root_lines="""      --font-display: 'Lora', serif;
      --font-body: 'Jost', sans-serif;
      --slide-bg-deep: #f5f3eb;
      --slide-bg-gradient: #f5f3eb;
      --text-primary: #111111;
      --text-secondary: #3a3a3a;
      --text-muted: #6b6b6b;
      --text-on-accent: #f5f3eb;
      --accent: #111111;
      --surface: rgba(255, 255, 255, 0.85);
      --surface-strong: rgba(17, 17, 17, 0.04);
      --line: rgba(17, 17, 17, 0.12);
      --panel-shadow: 0 12px 28px rgba(17, 17, 17, 0.06);
""",
        theme_css="""
    .slide { background: var(--slide-bg-gradient); }
    .slide::before {
      content: "";
      position: absolute;
      inset: 0;
      background-image:
        linear-gradient(rgba(17,17,17,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(17,17,17,0.04) 1px, transparent 1px);
      background-size: clamp(24px, 3vw, 40px) clamp(24px, 3vw, 40px);
      z-index: 0;
      opacity: 0.5;
    }
    .slide-cover > .slide-bg::after {
      content: "";
      position: absolute;
      left: 63%;
      top: 18%;
      width: 14%;
      height: 52%;
      background: repeating-linear-gradient(
        -45deg,
        #111,
        #111 2px,
        #f5f3eb 2px,
        #f5f3eb 6px
      );
      border: 2px solid #111;
      z-index: 0;
      pointer-events: none;
    }
""",
        google_url="https://fonts.googleapis.com/css2?family=Jost:wght@400;500&family=Lora:wght@500;700&display=swap",
    ),
    Preset(
        slug="neo-grid-yellow",
        title="Neo-Grid Bold",
        family="minimal",
        cover_archetype="neo-brutal",
        content_archetype="minimal",
        light_chrome=True,
        accent="#d4e817",
        root_lines="""      --font-display: 'Archivo Black', sans-serif;
      --font-body: 'DM Sans', sans-serif;
      --slide-bg-deep: #f7f5f0;
      --slide-bg-gradient: #f7f5f0;
      --text-primary: #0f0f0f;
      --text-secondary: #2d2d2d;
      --text-muted: #5c5c5c;
      --text-on-accent: #0f0f0f;
      --accent: #d4e817;
      --surface: rgba(255, 255, 255, 0.92);
      --surface-strong: rgba(212, 232, 23, 0.2);
      --line: rgba(15, 15, 15, 0.14);
      --panel-shadow: 8px 8px 0 rgba(15, 15, 15, 0.12);
""",
        theme_css="""
    .slide { background: var(--slide-bg-gradient); }
    .slide::after {
      content: "";
      position: absolute;
      right: 8%;
      top: 10%;
      width: 18%;
      height: 8px;
      background: var(--accent);
      z-index: 1;
      box-shadow: 6px 6px 0 #0f0f0f;
    }
    .panel-card .slide-object-text,
    .workflow-card .slide-object-text,
    .arch-card .slide-object-text,
    .metric-box .slide-object-text {
      border: 2px solid #0f0f0f;
      border-radius: 0;
      box-shadow: 6px 6px 0 rgba(15, 15, 15, 0.1);
    }
    .slide-cover > .slide-bg::after {
      content: "";
      position: absolute;
      left: 63%;
      top: 18%;
      width: 14%;
      height: 52%;
      background: linear-gradient(135deg, var(--accent), rgba(212,232,23,0.35));
      border: 3px solid #0f0f0f;
      border-radius: 0;
      z-index: 0;
      pointer-events: none;
    }
""",
        google_url="https://fonts.googleapis.com/css2?family=Archivo+Black&family=DM+Sans:wght@400;500&display=swap",
    ),
    Preset(
        slug="vellum-navy",
        title="Vellum",
        family="editorial",
        cover_archetype="vellum",
        content_archetype="editorial",
        light_chrome=False,
        accent="#5b8f96",
        root_lines="""      --font-display: 'Cormorant', serif;
      --font-body: 'Literata', serif;
      --slide-bg-deep: #0c1526;
      --slide-bg-gradient: linear-gradient(160deg, #0f1c2e 0%, #0c1526 55%, #0a1220 100%);
      --text-primary: #e6e2d8;
      --text-secondary: #c4bfb4;
      --text-muted: #8f8a80;
      --text-on-accent: #0c1526;
      --accent: #5b8f96;
      --surface: rgba(18, 32, 52, 0.75);
      --surface-strong: rgba(91, 143, 150, 0.12);
      --line: rgba(230, 226, 216, 0.12);
      --panel-shadow: 0 20px 44px rgba(0, 0, 0, 0.35);
""",
        theme_css="""
    .slide { background: var(--slide-bg-gradient); }
    .slide::before {
      content: "";
      position: absolute;
      right: 14%;
      bottom: 12%;
      width: 36%;
      height: 1px;
      background: linear-gradient(90deg, transparent, var(--accent), transparent);
      z-index: 0;
    }
    .hero-title .slide-object-text { font-style: italic; color: #f0ead8; }
    .slide-cover > .slide-bg::after {
      content: "";
      position: absolute;
      left: 62%;
      top: 18%;
      width: 18%;
      height: 56%;
      background:
        radial-gradient(ellipse at 30% 40%, rgba(91,143,150,0.25), transparent 60%),
        linear-gradient(145deg, rgba(12,21,38,0.95), rgba(15,28,46,0.85));
      border: 1px solid rgba(91, 143, 150, 0.35);
      z-index: 0;
      pointer-events: none;
    }
""",
        google_url="https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@0,400;0,600;1,400&family=Literata:wght@400;600&display=swap",
    ),
    Preset(
        slug="cobalt-grid",
        title="Cobalt Grid",
        family="cyber",
        cover_archetype="cobalt",
        content_archetype="cyber",
        light_chrome=True,
        accent="#2563eb",
        root_lines="""      --font-display: 'Fraunces', serif;
      --font-body: 'IBM Plex Sans', sans-serif;
      --slide-bg-deep: #f0f4fa;
      --slide-bg-gradient: linear-gradient(180deg, #f8fafc 0%, #e8f0fc 100%);
      --text-primary: #0f172a;
      --text-secondary: #334155;
      --text-muted: #64748b;
      --text-on-accent: #f8fafc;
      --accent: #2563eb;
      --surface: rgba(255, 255, 255, 0.88);
      --surface-strong: rgba(37, 99, 235, 0.08);
      --line: rgba(15, 23, 42, 0.1);
      --panel-shadow: 0 14px 32px rgba(37, 99, 235, 0.08);
""",
        theme_css="""
    .slide { background: var(--slide-bg-gradient); }
    .slide::before {
      content: "";
      position: absolute;
      inset: 0;
      background-image:
        linear-gradient(rgba(37,99,235,0.07) 1px, transparent 1px),
        linear-gradient(90deg, rgba(37,99,235,0.07) 1px, transparent 1px);
      background-size: clamp(22px, 3vw, 36px) clamp(22px, 3vw, 36px);
      z-index: 0;
    }
    .hero-title .slide-object-text { font-style: italic; color: #1e3a8a; }
    .slide-cover > .slide-bg::after {
      content: "";
      position: absolute;
      left: 58%;
      top: 18%;
      width: 28%;
      height: 54%;
      background:
        linear-gradient(135deg, rgba(37,99,235,0.12), rgba(59,130,246,0.06)),
        repeating-linear-gradient(
          -12deg,
          transparent,
          transparent 8px,
          rgba(37,99,235,0.06) 8px,
          rgba(37,99,235,0.06) 9px
        );
      border: 1px solid rgba(37, 99, 235, 0.25);
      z-index: 0;
      pointer-events: none;
    }
""",
        google_url="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Sans:wght@400;600&display=swap",
    ),
]


def patch_root(text: str, preset: Preset) -> str:
    start = text.find(ROOT_NEEDLE_START)
    end = text.find(ROOT_NEEDLE_END)
    if start < 0 or end < 0:
        raise SystemExit("Could not find :root theme block in reference")
    end += len(ROOT_NEEDLE_END)
    chrome = (LIGHT_CHROME if preset.light_chrome else DARK_CHROME).format(accent=preset.accent)
    return text[:start] + preset.root_lines + chrome + text[end:]


def patch_head_fonts(text: str, google_url: Optional[str]) -> str:
    if HEAD_FONTSHARE not in text:
        raise SystemExit("Could not find font block in reference")
    return text.replace(HEAD_FONTSHARE, "", 1)


def patch_theme_section(text: str, preset: Preset) -> str:
    theme_core = strip_preset_cover_decor(preset.theme_css)
    cover_decor = (
        COVER_DECOR_VARIABLES_BY_SLUG.get(preset.slug, "")
        + COVER_DECOR_CSS_BY_FAMILY.get(preset.family, "")
    )
    theme = (
        f"    /* === theme ({preset.title}) === */\n"
        + COMMON_COMPONENT_CSS
        + theme_core
        + cover_decor
        + """
    body {
      margin: 0;
      font-family: var(--font-body);
      background: var(--slide-bg-deep);
      color: var(--text-primary);
    }
    .slide { background: transparent; }
"""
    )
    if THEME_NEEDLE_OLD not in text:
        raise SystemExit("Could not find theme section in reference")
    return text.replace(THEME_NEEDLE_OLD, theme, 1)


def patch_slides(text: str, slides_html: str) -> str:
    start = text.index('<div class="slides-offset">')
    end = text.index("</div>\n\n<script>", start)
    return text[:start] + slides_html + text[end:]


def main() -> None:
    reference = REF.read_text(encoding="utf-8")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for preset in PRESETS:
        html = reference
        html = patch_head_fonts(html, preset.google_url)
        html = patch_root(html, preset)
        html = patch_theme_section(html, preset)
        html = html.replace(
            '<html lang="en" data-deck-id="editable-deck-reference" data-mobile-adaptation="desktop-default">',
            f'<html lang="zh-Hans" data-deck-id="preset-{preset.slug}" data-mobile-adaptation="desktop-default">',
        )
        html = html.replace(
            "<title>Editable Deck Reference</title>",
            f"<title>{preset.title} · README Preset Deck</title>",
        )
        html = normalize_generated_html(patch_slides(html, render_deck(preset)))

        out_path = OUT_DIR / f"{preset.slug}.html"
        out_path.write_text(html, encoding="utf-8")
        print(out_path.name, len(html))

    print(f"Built {len(PRESETS)} preset decks in {OUT_DIR}")


if __name__ == "__main__":
    main()
