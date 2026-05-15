#!/usr/bin/env python3
"""Validate skill workflow docs for required editable-deck decisions."""

from __future__ import annotations

import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CHECKS = {
    "SKILL.md": [
        "Question 7 — Mobile adaptation",
        "Desktop-first only",
        "Adapt for phone portrait + landscape",
        'data-mobile-adaptation="enabled"',
        'data-mobile-adaptation="desktop-default"',
    ],
    "editor-runtime.md": [
        "Copy slide",
        "New Page",
        'data-mobile-adaptation="desktop-default"',
    ],
    "html-template.md": [
        'data-filmstrip-action="copy"',
        "#btnNewPage",
        'data-mobile-adaptation="desktop-default"',
    ],
    "docs/editable-preset-runtime-tdd-plan.md": [
        "S2 Discovery mobile question",
        "S3 Mobile adaptation output",
        "S7 Export and persistence",
        "S8 Performance",
    ],
}


def main() -> int:
    started = time.perf_counter()
    errors: list[str] = []
    for rel, needles in CHECKS.items():
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"{rel}: missing")
            continue
        source = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in source:
                errors.append(f"{rel}: missing {needle!r}")
    if errors:
        print("Skill workflow validation failed:")
        for error in errors:
            print(f"- {error}")
        return 2
    elapsed = time.perf_counter() - started
    print(f"Validated skill workflow docs in {elapsed:.2f}s.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
