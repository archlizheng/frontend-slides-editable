#!/usr/bin/env python3
"""
Extract slide-oriented content from a PDF for the editable-deck pipeline.

Outputs the same shape as extract-pptx.py: extracted-slides.json + assets/

Usage:
    python3 extract-pdf.py <input.pdf> [output_dir] [--raster-if-empty]

Requires: pip install pymupdf

Notes:
    - One PDF page maps to one "slide". Speaker notes are not present in PDF; notes is "".
    - Scanned PDFs (image-only) have no extractable text unless --raster-if-empty is used
      (then the page is rendered to a PNG under assets/).
"""

from __future__ import annotations

import argparse
import json
import os
import sys


def _import_fitz():
    try:
        import fitz  # PyMuPDF
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Missing dependency: PyMuPDF. Install it with: pip install pymupdf"
        ) from exc
    return fitz


def _block_text_and_max_size(block: dict) -> tuple[str, float]:
    """Return (full_text, max_font_size) for a text block (type 0)."""
    if block.get("type") != 0:
        return "", 0.0
    max_size = 0.0
    line_texts: list[str] = []
    for line in block.get("lines", []):
        parts: list[str] = []
        for span in line.get("spans", []):
            max_size = max(max_size, float(span.get("size") or 0.0))
            parts.append(span.get("text") or "")
        line_texts.append("".join(parts))
    text = "\n".join(line_texts).strip()
    return text, max_size


def _pick_title_and_content(
    text_blocks: list[dict],
) -> tuple[str, list[dict]]:
    """
    Heuristic: if the largest-font block is reasonably short and >= 14pt, use as title;
    remaining blocks become content entries. Otherwise title is empty and all blocks
    become separate text content items.
    """
    if not text_blocks:
        return "", []

    sizes = [b["size"] for b in text_blocks]
    max_sz = max(sizes)
    # Prefer the top-most block among those within 0.5pt of max size
    candidates = [b for b in text_blocks if b["size"] >= max_sz - 0.5]
    candidates.sort(key=lambda b: (b["bbox"][1], b["bbox"][0]))
    title_block = candidates[0]
    title_text = title_block["text"]
    second_max = sorted(sizes, reverse=True)[1] if len(sizes) > 1 else 0.0

    use_as_title = (
        max_sz >= 14.0
        and len(title_text) <= 220
        and (len(sizes) == 1 or max_sz >= second_max + 1.0 or max_sz >= 18.0)
    )

    if use_as_title:
        title = title_text
        rest = [b for b in text_blocks if b is not title_block]
        content = [{"type": "text", "content": b["text"]} for b in rest if b["text"]]
        return title, content

    return "", [{"type": "text", "content": b["text"]} for b in text_blocks if b["text"]]


def extract_pdf(
    file_path: str,
    output_dir: str = ".",
    *,
    raster_if_empty: bool = False,
) -> list[dict]:
    """
    Extract one slide dict per PDF page. Schema matches extract_pptx output:
    number, title, content[], images[{path,width,height}], notes.
    """
    fitz = _import_fitz()
    doc = fitz.open(file_path)
    slides_data: list[dict] = []

    assets_dir = os.path.join(output_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    for page_index in range(len(doc)):
        slide_num = page_index + 1
        page = doc[page_index]

        slide_data: dict = {
            "number": slide_num,
            "title": "",
            "content": [],
            "images": [],
            "notes": "",
        }

        text_dict = page.get_text("dict")
        text_blocks: list[dict] = []
        for block in text_dict.get("blocks", []):
            text, size = _block_text_and_max_size(block)
            if not text:
                continue
            bbox = block.get("bbox") or (0, 0, 0, 0)
            text_blocks.append({"text": text, "size": size, "bbox": bbox})

        text_blocks.sort(key=lambda b: (b["bbox"][1], b["bbox"][0]))
        title, content = _pick_title_and_content(text_blocks)
        slide_data["title"] = title
        slide_data["content"] = content

        # Embedded images (xref-based)
        seen_xrefs: set[int] = set()
        for img in page.get_images(full=True):
            xref = int(img[0])
            if xref in seen_xrefs:
                continue
            seen_xrefs.add(xref)
            try:
                base = doc.extract_image(xref)
            except (ValueError, RuntimeError):
                continue
            image_bytes = base.get("image")
            if not image_bytes:
                continue
            ext = (base.get("ext") or "png").lower()
            if ext == "jpeg":
                ext = "jpg"
            img_idx = len(slide_data["images"]) + 1
            image_name = f"slide{slide_num}_img{img_idx}.{ext}"
            image_path = os.path.join(assets_dir, image_name)
            with open(image_path, "wb") as f:
                f.write(image_bytes)

            w = int(base.get("width") or 0)
            h = int(base.get("height") or 0)
            slide_data["images"].append(
                {
                    "path": f"assets/{image_name}",
                    "width": w,
                    "height": h,
                }
            )

        if (
            raster_if_empty
            and not slide_data["content"]
            and not slide_data["title"]
            and not slide_data["images"]
        ):
            matrix = fitz.Matrix(1.5, 1.5)
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            image_name = f"slide{slide_num}_page.png"
            out_path = os.path.join(assets_dir, image_name)
            pix.save(out_path)
            slide_data["images"].append(
                {
                    "path": f"assets/{image_name}",
                    "width": pix.width,
                    "height": pix.height,
                }
            )

        slides_data.append(slide_data)

    doc.close()
    return slides_data


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract PDF pages to extracted-slides.json + assets/"
    )
    parser.add_argument("input_pdf", help="Path to .pdf")
    parser.add_argument(
        "output_dir",
        nargs="?",
        default=".",
        help="Directory for extracted-slides.json and assets/ (default: .)",
    )
    parser.add_argument(
        "--raster-if-empty",
        action="store_true",
        help="If a page has no text and no embedded images, render the page to PNG",
    )
    args = parser.parse_args()

    input_file = args.input_pdf
    output_dir = args.output_dir

    if not os.path.isfile(input_file):
        print(f"Not a file: {input_file}", file=sys.stderr)
        return 1

    try:
        slides = extract_pdf(
            input_file,
            output_dir,
            raster_if_empty=args.raster_if_empty,
        )
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    output_path = os.path.join(output_dir, "extracted-slides.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(slides, f, indent=2, ensure_ascii=False)

    print(f"Extracted {len(slides)} page(s) to {output_path}")
    for s in slides:
        img_count = len(s["images"])
        text_bits = len(s["content"]) + (1 if s["title"] else 0)
        label = s["title"] or "(no title)"
        print(
            f"  Page {s['number']}: {label[:60]}{'…' if len(str(label)) > 60 else ''} "
            f"— {img_count} image(s), {text_bits} text block(s)"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
