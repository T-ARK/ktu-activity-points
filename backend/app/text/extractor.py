"""Stage 2: Native Text Layer Extraction & Quote Grounding (SPEC §7.2 & §7.4)."""

import re

import pymupdf as fitz
from pydantic import BaseModel


class TextWord(BaseModel):
    text: str
    page: int
    bbox: tuple[float, float, float, float]  # (x0, y0, x1, y1)


class ExtractedDocumentText(BaseModel):
    full_text: str
    source: str  # "native" or "ocr"
    page_count: int
    words: list[TextWord]
    has_text_layer: bool


def normalize_text_for_grounding(text: str) -> str:
    """Normalizes whitespace, punctuation, and hyphenation for grounding checks."""
    if not text:
        return ""
    # Collapse multiple whitespaces/newlines to single space
    cleaned = re.sub(r"\s+", " ", text)
    # Remove soft hyphens and normalize dash variations
    cleaned = re.sub(r"[\u00ad\u2010\u2011\u2012\u2013\u2014\u2015-]", "-", cleaned)
    # Collapse spaces around hyphens e.g. "inter - college" -> "inter-college"
    cleaned = re.sub(r"\s*-\s*", "-", cleaned)
    return cleaned.strip().lower()


def is_quote_grounded(quote: str, document_text: str) -> bool:
    """Checks whether a verbatim quote exists in document text (E-02 check)."""
    norm_quote = normalize_text_for_grounding(quote)
    norm_doc = normalize_text_for_grounding(document_text)
    if not norm_quote:
        return False
    return norm_quote in norm_doc


def extract_native_pdf_text(content: bytes) -> ExtractedDocumentText:
    """Extracts native text, word tokens, and bounding boxes using PyMuPDF."""
    doc = fitz.open(stream=content, filetype="pdf")  # type: ignore[no-untyped-call]
    pages_text: list[str] = []
    words_list: list[TextWord] = []

    for page_idx in range(len(doc)):
        page = doc[page_idx]
        text = page.get_text("text") or ""  # type: ignore[no-untyped-call]
        pages_text.append(text)

        # Extract words with bounding boxes: (x0, y0, x1, y1, word, block_no, line_no, word_no)
        raw_words = page.get_text("words") or []  # type: ignore[no-untyped-call]
        for w in raw_words:
            words_list.append(
                TextWord(
                    text=str(w[4]),
                    page=page_idx + 1,
                    bbox=(float(w[0]), float(w[1]), float(w[2]), float(w[3])),
                )
            )

    full_text = "\n".join(pages_text).strip()
    has_layer = len(full_text) >= 20

    return ExtractedDocumentText(
        full_text=full_text,
        source="native",
        page_count=len(doc),
        words=words_list,
        has_text_layer=has_layer,
    )
