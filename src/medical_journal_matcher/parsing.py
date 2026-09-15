from __future__ import annotations

from pathlib import Path

from docx import Document
from pypdf import PdfReader


def parse_manuscript(path: Path) -> str:
    """Extract local text without making any external request."""
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md"}:
        return path.read_text(encoding="utf-8")
    if suffix == ".pdf":
        return "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
    if suffix == ".docx":
        return "\n".join(paragraph.text for paragraph in Document(path).paragraphs)
    raise ValueError("Supported manuscript formats are .txt, .md, .pdf, and .docx")
