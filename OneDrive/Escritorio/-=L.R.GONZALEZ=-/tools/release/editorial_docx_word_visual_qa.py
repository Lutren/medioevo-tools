"""Word-backed visual QA for private editorial DOCX exports.

This script is intentionally local-only. It opens DOCX files through the local
Microsoft Word COM automation surface, exports them to PDF, renders every PDF
page with PyMuPDF, and writes image-metric summaries without printing manuscript
content.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import fitz
from PIL import Image

try:
    import win32com.client
except Exception as exc:  # pragma: no cover - host dependency
    win32com = None
    WIN32COM_IMPORT_ERROR = exc
else:  # pragma: no cover - import branch
    WIN32COM_IMPORT_ERROR = None


WD_EXPORT_FORMAT_PDF = 17
WD_EXPORT_OPTIMIZE_FOR_PRINT = 0
WD_EXPORT_ALL_DOCUMENT = 0
WD_EXPORT_DOCUMENT_CONTENT = 0
WD_EXPORT_CREATE_NO_BOOKMARKS = 0


@dataclass(frozen=True)
class BookSpec:
    package_id: str
    title: str
    docx: Path


def _safe_rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def export_docx_to_pdf(docx_path: Path, pdf_path: Path) -> dict[str, Any]:
    if win32com is None:
        raise RuntimeError(f"pywin32 is not available: {WIN32COM_IMPORT_ERROR}")
    if not docx_path.exists():
        raise FileNotFoundError(docx_path)

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = None
    try:
        doc = word.Documents.Open(str(docx_path.resolve()), ReadOnly=True)
        pages = int(doc.ComputeStatistics(2))
        doc.ExportAsFixedFormat(
            OutputFileName=str(pdf_path.resolve()),
            ExportFormat=WD_EXPORT_FORMAT_PDF,
            OpenAfterExport=False,
            OptimizeFor=WD_EXPORT_OPTIMIZE_FOR_PRINT,
            Range=WD_EXPORT_ALL_DOCUMENT,
            Item=WD_EXPORT_DOCUMENT_CONTENT,
            IncludeDocProps=True,
            KeepIRM=True,
            CreateBookmarks=WD_EXPORT_CREATE_NO_BOOKMARKS,
            DocStructureTags=True,
            BitmapMissingFonts=True,
            UseISO19005_1=False,
        )
        return {"word_reported_pages": pages, "pdf_bytes": pdf_path.stat().st_size}
    finally:
        if doc is not None:
            doc.Close(False)
        word.Quit()


def image_metrics(path: Path, root: Path) -> dict[str, Any]:
    with Image.open(path) as im:
        img = im.convert("L")
        width, height = img.size
        pixels = img.load()
        threshold = 245
        ink = 0
        min_x, min_y = width, height
        max_x, max_y = -1, -1
        edge_ink = 0
        edge_total = 0
        border = max(8, min(width, height) // 80)
        for y in range(height):
            for x in range(width):
                is_edge = x < border or y < border or x >= width - border or y >= height - border
                if is_edge:
                    edge_total += 1
                if pixels[x, y] < threshold:
                    ink += 1
                    if is_edge:
                        edge_ink += 1
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                    max_x = max(max_x, x)
                    max_y = max(max_y, y)

        total = width * height
        ink_ratio = ink / total if total else 0.0
        edge_ink_ratio = edge_ink / edge_total if edge_total else 0.0
        bbox = None if max_x < 0 else [min_x, min_y, max_x, max_y]
        edge_contact = False
        if bbox is not None:
            edge_contact = (
                min_x < border or min_y < border or max_x >= width - border or max_y >= height - border
            )
        return {
            "file": _safe_rel(path, root),
            "width": width,
            "height": height,
            "bytes": path.stat().st_size,
            "ink_ratio": round(ink_ratio, 6),
            "edge_ink_ratio": round(edge_ink_ratio, 6),
            "bbox": bbox,
            "blank_candidate": ink_ratio < 0.001,
            "edge_contact_candidate": bool(edge_contact and edge_ink_ratio > 0.002),
        }


def render_pdf_pages(pdf_path: Path, output_dir: Path, root: Path, zoom: float) -> list[dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    metrics: list[dict[str, Any]] = []
    matrix = fitz.Matrix(zoom, zoom)
    try:
        for idx in range(doc.page_count):
            page_no = idx + 1
            out = output_dir / f"page-{page_no:04d}.png"
            pix = doc.load_page(idx).get_pixmap(matrix=matrix, alpha=False)
            pix.save(out)
            metric = image_metrics(out, root)
            metric["page_number"] = page_no
            metrics.append(metric)
    finally:
        doc.close()
    return metrics


def make_contact_sheets(page_metrics: list[dict[str, Any]], sheet_dir: Path, root: Path, pages_dir: Path) -> list[str]:
    sheet_dir.mkdir(parents=True, exist_ok=True)
    thumb_w, thumb_h = 160, 220
    cols, rows = 5, 4
    margin = 16
    label_h = 20
    per_sheet = cols * rows
    sheets: list[str] = []
    for sheet_idx in range(math.ceil(len(page_metrics) / per_sheet)):
        chunk = page_metrics[sheet_idx * per_sheet : (sheet_idx + 1) * per_sheet]
        canvas = Image.new(
            "RGB",
            (cols * (thumb_w + margin) + margin, rows * (thumb_h + label_h + margin) + margin),
            "white",
        )
        for i, metric in enumerate(chunk):
            page_no = metric["page_number"]
            img_path = pages_dir / f"page-{page_no:04d}.png"
            with Image.open(img_path) as im:
                thumb = im.convert("RGB")
                thumb.thumbnail((thumb_w, thumb_h))
                x = margin + (i % cols) * (thumb_w + margin)
                y = margin + (i // cols) * (thumb_h + label_h + margin)
                canvas.paste(thumb, (x, y + label_h))
        out = sheet_dir / f"contact-sheet-{sheet_idx + 1:03d}.png"
        canvas.save(out)
        sheets.append(_safe_rel(out, root))
    return sheets


def summarize(metrics: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "page_count": len(metrics),
        "blank_candidates": [m["page_number"] for m in metrics if m["blank_candidate"]],
        "edge_contact_candidates": [m["page_number"] for m in metrics if m["edge_contact_candidate"]],
        "min_ink_ratio": min((m["ink_ratio"] for m in metrics), default=None),
        "max_ink_ratio": max((m["ink_ratio"] for m in metrics), default=None),
        "min_edge_ink_ratio": min((m["edge_ink_ratio"] for m in metrics), default=None),
        "max_edge_ink_ratio": max((m["edge_ink_ratio"] for m in metrics), default=None),
        "dimensions": sorted({(m["width"], m["height"]) for m in metrics}),
    }


def run(book: BookSpec, out_root: Path, workspace_root: Path, zoom: float) -> dict[str, Any]:
    book_dir = out_root / book.package_id
    pdf_path = book_dir / f"{book.package_id}_word_export.pdf"
    export_info = export_docx_to_pdf(book.docx, pdf_path)
    pages_dir = book_dir / "pages"
    metrics = render_pdf_pages(pdf_path, pages_dir, workspace_root, zoom)
    sheets = make_contact_sheets(metrics, book_dir / "contact_sheets", workspace_root, pages_dir)
    summary = summarize(metrics)
    status = "PASS_AUTOMATED_FULL_PAGE_COVERAGE"
    if summary["blank_candidates"] or summary["edge_contact_candidates"]:
        status = "REVIEW_AUTOMATED_FLAGS"
    return {
        "package_id": book.package_id,
        "title": book.title,
        "docx": _safe_rel(book.docx, workspace_root),
        "word_export_pdf": _safe_rel(pdf_path, workspace_root),
        "word_reported_pages": export_info["word_reported_pages"],
        "pdf_bytes": export_info["pdf_bytes"],
        "rendered_pages_dir": _safe_rel(pages_dir, workspace_root),
        "contact_sheets": sheets,
        "metrics_summary": summary,
        "status": status,
        "page_metrics": metrics,
    }


def write_report(result: dict[str, Any], out_path: Path) -> None:
    lines = [
        "# Editorial DOCX Word Visual QA - 2026-05-22",
        "",
        f"Status: `{result['overall_status']}`",
        "",
        "Scope: internal private automated full-page coverage. PublicationGate=BLOCK.",
        "",
        "Method: Microsoft Word COM exported the private DOCX files to PDF in invisible read-only mode. PyMuPDF rendered every exported PDF page to PNG. PIL computed image metrics for blank-page and edge-contact candidates. No manuscript text is printed in this report.",
        "",
    ]
    for book in result["books"]:
        summary = book["metrics_summary"]
        lines.extend(
            [
                f"## {book['title']}",
                "",
                f"- Status: `{book['status']}`",
                f"- Word-reported pages: `{book['word_reported_pages']}`",
                f"- Rendered page PNGs: `{summary['page_count']}`",
                f"- Blank candidates: `{len(summary['blank_candidates'])}`",
                f"- Edge-contact candidates: `{len(summary['edge_contact_candidates'])}`",
                f"- Contact sheets: `{len(book['contact_sheets'])}`",
                f"- PDF artifact: `{book['word_export_pdf']}`",
                "",
            ]
        )
        if summary["blank_candidates"] or summary["edge_contact_candidates"]:
            lines.append("Candidate pages require manual visual review before approval.")
            lines.append("")
    lines.extend(
        [
            "## Boundary",
            "",
            "- This is automated visual coverage, not public release approval.",
            "- The generated PNGs/contact sheets contain private editorial material.",
            "- Do not publish, upload, push, deploy, or package these QA artifacts for public use.",
            "",
        ]
    )
    out_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-root", default="qa_artifacts/editorial_docx_word_visual_qa/EDITORIAL_DOCX_WORD_FULL_QA_20260522")
    parser.add_argument("--zoom", type=float, default=1.0)
    parser.add_argument("--pretty", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workspace_root = Path.cwd()
    out_root = workspace_root / args.out_root
    out_root.mkdir(parents=True, exist_ok=True)
    books = [
        BookSpec(
            "FRAGMENTOS_INTERNAL_EXPORT_2026-05-22",
            "Fragmentos",
            workspace_root / "books/editorial/internal_exports/FRAGMENTOS_INTERNAL_EXPORT_2026-05-22/17_fragmentos_integrado_0713.docx",
        ),
        BookSpec(
            "CALIBRACION_INTERNAL_EXPORT_2026-05-22",
            "Calibracion",
            workspace_root / "books/editorial/internal_exports/CALIBRACION_INTERNAL_EXPORT_2026-05-22/17_calibracion_integrado_0713.docx",
        ),
    ]
    result = {
        "schema_version": "medioevo.editorial.docx_word_visual_qa.v1",
        "generated_at": datetime.now().isoformat(),
        "publication_gate": "BLOCK",
        "cloud_provider_called": False,
        "external_actions_performed": False,
        "method": "word_com_export_pdf_then_pymupdf_full_page_render",
        "books": [],
    }
    for book in books:
        result["books"].append(run(book, out_root, workspace_root, args.zoom))
    result["overall_status"] = (
        "PASS_AUTOMATED_FULL_PAGE_COVERAGE"
        if all(book["status"] == "PASS_AUTOMATED_FULL_PAGE_COVERAGE" for book in result["books"])
        else "REVIEW_AUTOMATED_FLAGS"
    )
    summary_path = out_root / "editorial_docx_word_visual_qa_summary.json"
    report_path = out_root / "EDITORIAL_DOCX_WORD_VISUAL_QA_REPORT_2026-05-22.md"
    summary_path.write_text(json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False), encoding="utf-8")
    write_report(result, report_path)
    print(
        json.dumps(
            {
                "overall_status": result["overall_status"],
                "summary": _safe_rel(summary_path, workspace_root),
                "report": _safe_rel(report_path, workspace_root),
                "books": [
                    {
                        "package_id": book["package_id"],
                        "status": book["status"],
                        "word_reported_pages": book["word_reported_pages"],
                        "rendered_pages": book["metrics_summary"]["page_count"],
                        "blank_candidates": len(book["metrics_summary"]["blank_candidates"]),
                        "edge_contact_candidates": len(book["metrics_summary"]["edge_contact_candidates"]),
                        "contact_sheets": len(book["contact_sheets"]),
                    }
                    for book in result["books"]
                ],
            },
            indent=2,
        )
    )
    return 0 if result["overall_status"] == "PASS_AUTOMATED_FULL_PAGE_COVERAGE" else 2


if __name__ == "__main__":
    sys.exit(main())
