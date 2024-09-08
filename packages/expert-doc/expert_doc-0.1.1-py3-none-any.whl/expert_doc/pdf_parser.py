from pathlib import Path
from typing import Iterable, NamedTuple

import pikepdf
from pikepdf import PdfImage
import pypdfium2 as pdfium

from expert_doc.models import (
    Image,
    ParsedPage,
    PagedDocParser,
)


class ImageWrapper(Image):
    def __init__(self, raw_img: PdfImage):
        self.raw_img = raw_img
        return

    def dump_to_file(self, name_no_extension: str) -> str:
        return self.raw_img.extract_to(fileprefix=name_no_extension)

    pass


class PdfParser(PagedDocParser):
    def __init__(self, path: Path):
        super(PdfParser, self).__init__(path)
        self.img_pdf = pikepdf.Pdf.open(path)
        self.text_pdf = pdfium.PdfDocument(str(path))
        assert len(self.img_pdf.pages) == len(self.text_pdf)
        return

    def iter_pages(self) -> Iterable[ParsedPage]:
        for text_page, img_page in zip(
            self.text_pdf,
            self.img_pdf.pages,
        ):
            yield ParsedPage(
                images=[
                    ImageWrapper(raw_img=PdfImage(img))
                    for img in img_page.images.values()
                ],
                text=text_page.get_textpage().get_text_range(),
            )
            pass
        return

    pass
