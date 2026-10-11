
from dataclasses import dataclass
from io import BytesIO

from pypdf import PdfReader

from config import CHUNK_OVERLAP, CHUNK_SIZE


@dataclass
class DocumentChunk:
    text: str
    page_number: int
    chunk_number: int


def extract_pdf_pages(pdf_bytes: bytes) -> list[dict]:
    """Extract non-empty text from each PDF page."""
    reader = PdfReader(BytesIO(pdf_bytes))

    if reader.is_encrypted:
        raise ValueError("Password-protected PDFs are not supported.")

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()

        if text:
            pages.append({
                "page_number": page_number,
                "text": text,
            })

    if not pages:
        raise ValueError(
            "No extractable text found. The PDF may be scanned; OCR is not included."
        )

    return pages


def split_pages_into_chunks(
    pages: list[dict],
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[DocumentChunk]:
    """Split page text into chunks while preserving page numbers."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be non-negative and smaller than chunk_size.")

    chunks = []
    chunk_number = 0
    step = chunk_size - overlap

    for page in pages:
        text = page["text"].strip()

        for start in range(0, len(text), step):
            piece = text[start:start + chunk_size].strip()

            if piece:
                chunks.append(
                    DocumentChunk(
                        text=piece,
                        page_number=page["page_number"],
                        chunk_number=chunk_number,
                    )
                )
                chunk_number += 1

    return chunks


def process_pdf(pdf_bytes: bytes) -> list[DocumentChunk]:
    """Extract and chunk a PDF in one call."""
    pages = extract_pdf_pages(pdf_bytes)
    return split_pages_into_chunks(pages)
