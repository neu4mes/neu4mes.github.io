#!/usr/bin/env python3
"""Render the first page of a PDF as a PNG thumbnail (posters and presentations)."""
from __future__ import annotations

import argparse
from pathlib import Path

import fitz


def render_first_page(pdf_path: Path, output_path: Path, scale: float | None = None) -> None:
    doc = fitz.open(pdf_path)
    try:
        page = doc[0]
        if scale is None:
            scale = 1.25 if page.rect.width * page.rect.height > 1_000_000 else 1.5
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        pix.save(str(output_path))
    finally:
        doc.close()


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Create listing/preview PNG from the first page of a PDF."
    )
    ap.add_argument("pdf", type=Path, help="Source PDF (poster.pdf or presentation.pdf)")
    ap.add_argument(
        "-o",
        "--output",
        type=Path,
        required=True,
        help="Output PNG path (e.g. poster.png or slide.png)",
    )
    ap.add_argument(
        "--scale",
        type=float,
        default=None,
        help="Render scale (default: 1.25 for large pages, else 1.5)",
    )
    args = ap.parse_args()
    if not args.pdf.is_file():
        raise SystemExit(f"PDF not found: {args.pdf}")
    render_first_page(args.pdf, args.output, args.scale)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
