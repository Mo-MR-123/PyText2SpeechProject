import logging

from src.parsers.base_parser import BaseParser
from pypdf import PdfReader
from pathlib import Path
from loggers.log_config import LogConfig
from src.text_processors.post_processor import PostProcessor

log_config = LogConfig(log_level=logging.DEBUG)



class PdfParser(BaseParser):

    def __init__(self, path_to_pdf: Path, post_processor: PostProcessor = None):
        self.logger = log_config.get_logger(self.__class__.__name__)
        self.path_to_pdf = path_to_pdf
        self.pdf_reader = PdfReader(path_to_pdf)
        self.start_page_default = 0
        self.end_page_default = self.pdf_reader.get_num_pages()
        self.post_processor = post_processor

    # TODO: pre/post process txt to remove e.g. weird characters.
    def extract_txt_from_pdf(
        self,
        start_page: int,
        end_page: int
    ) -> str:
        assert isinstance(start_page, int) and isinstance(
            end_page, int), f"Both start and end page must be integers but got {start_page=} and {end_page=}"
        assert start_page < end_page, f"{start_page=} must be less than {end_page=}."
        assert start_page >= 0 and start_page <= self.end_page_default, f"provided start page {start_page} is not between the page range of the pdf {self.start_page_default}-{self.end_page_default}"
        assert end_page >= 0 and end_page <= self.end_page_default, f"provided end page {end_page} is not between the page range of the pdf {self.start_page_default}-{self.end_page_default}"

        pages = self.pdf_reader.pages[start_page: end_page][0]
        self.logger.info(pages)

        extracted_txt = pages.extract_text()

        # TODO: post-process text to remove unneeded chars
        if self.post_processor:
            pass

        return extracted_txt
