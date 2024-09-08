import os
from pathlib import Path

from expert_doc.models import PagedDocParser
from expert_doc.pdf_parser import PdfParser


PARSERS = {
    ".pdf": PdfParser,
}


def get_paged_document_parser(path: Path) -> PagedDocParser:
    _, ext = os.path.splitext(path)
    if ext in PARSERS:
        return PARSERS[ext](path)
    raise Exception(
        f"can't parse a '{ext}' - support extensions are {', '.join(PARSERS.keys())}"
    )
