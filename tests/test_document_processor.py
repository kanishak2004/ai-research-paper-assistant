
from io import BytesIO

import pytest
from pypdf import PdfWriter

from document_processor import (
    extract_pdf_pages,
    split_pages_into_chunks,
)


def create_test_pdf() -> bytes:
    writer = PdfWriter()
    writer.add_blank_page(width=300, height=300)

    buffer = BytesIO()
    writer.write(buffer)
    return buffer.getvalue()


def test_empty_pdf_text_raises_error():
    with pytest.raises(ValueError, match="No extractable text"):
        extract_pdf_pages(create_test_pdf())


def test_chunking_preserves_page_number():
    pages = [{"page_number": 3, "text": "abcdefghij"}]

    chunks = split_pages_into_chunks(
        pages, chunk_size=6, overlap=2
    )

    assert len(chunks) == 2
    assert chunks[0].text == "abcdef"
    assert chunks[1].text == "efghij"
    assert all(chunk.page_number == 3 for chunk in chunks)


def test_invalid_chunk_settings_raise_error():
    with pytest.raises(ValueError):
        split_pages_into_chunks(
            [{"page_number": 1, "text": "some text"}],
            chunk_size=5,
            overlap=5,
        )
