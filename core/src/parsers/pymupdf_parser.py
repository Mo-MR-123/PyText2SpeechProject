
import pymupdf

from pathlib import Path
from core.src.parsers.base_parser import BaseParser
from core.loggers.log_config import LogConfig

log_config = LogConfig()

"""
TODO: implement functionality for filetype checking to avoid erronous reading of files.
TODO: Multithreading not advisable with PyMuPDF as it is designed without that in mind.
      Alternative would be to use multiprocessing to concurrently process multiple pdf files.
NOTE: PyMuPDF can open many non-pdf files as txt -> https://pymupdf.readthedocs.io/en/latest/how-to-open-a-file.html#opening-files-as-text
Supported filetypes by PyMuPDF: https://pymupdf.readthedocs.io/en/latest/how-to-open-a-file.html#supported-file-types
"""
class PyMuPDFParser(BaseParser):
    def __init__(
        self, 
        pdf_path: Path
    ):
        self._pdf_reader = None
        self._logger = log_config.get_logger(self.__class__.__name__)

        self.pdf_path = str(pdf_path)
    
    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        # Open the source PDF
        self._pdf_reader = pymupdf.open(self.pdf_path)
        # Remove all links from the file stream
        # if self.remove_reference_links:
        #     self.remove_all_links()
                    
    def close(self):
        if self._pdf_reader:
            self._pdf_reader.close()

    def extract_all_text(self) -> str:
        """
        encoding -> https://pymupdf.readthedocs.io/en/latest/textpage.html#TextPage.extractTEXT
        """
        all_text = ""

        # Iterate through each page in the document
        for page in self._pdf_reader:
            # Extract text from the current page
            all_text += page.get_text() + "\n"  # Add a newline after each page's text
            
        return all_text

    def extract_text_from_page(self, page_number: int) -> str:
        """
        encoding -> https://pymupdf.readthedocs.io/en/latest/textpage.html#TextPage.extractTEXT
        """
        if 0 <= page_number < self._pdf_reader.page_count:
            page = self._pdf_reader.load_page(page_number)
            return page.get_text()
        else:
            raise ValueError(f"Page number {page_number=} out of range.")

    def remove_all_links(self) -> None:
        """
        FROM -> https://www.linkedin.com/pulse/streamline-your-pdfs-effortlessly-remove-annotations-targeted-arshad-pyjuc
        """            
        for page in self._pdf_reader:
            # Find the link and remove it
            
            # Get all links on that page
            links = page.get_links()
            for link in links:
                self._logger.debug(f"Link object found: {link=}")
                
                # Remove any link that exists
                if link['kind'] != pymupdf.LINK_NONE:
                    self._logger.info(f'Link found: {link}')                    
                    page.add_redact_annot(link["from"]) # link['from'] contains the Rect
                    page.delete_link(link)
            
            # Apply the redaction (removal)
            page.apply_redactions(pymupdf.PDF_REDACT_IMAGE_NONE)

    def extract_text_between_pages(self, start_page: int, end_page: int) -> str:
        """
        encoding -> https://pymupdf.readthedocs.io/en/latest/textpage.html#TextPage.extractTEXT
        """
        if 0 <= start_page < self._pdf_reader.page_count and \
            0 <= end_page < self._pdf_reader.page_count and \
            end_page > start_page:
            
            # Initialize a variable to hold the extracted text
            extracted_text = ""

            # Loop through the specified page range
            # Adjust for 0-based index
            for page_number in range(start_page - 1, end_page):
                page = self._pdf_reader.load_page(page_number)
                # Extract text and add whitespace for separation
                extracted_text += page.get_text() + " "  

            return extracted_text
        else:
            raise ValueError(f"Page numbers {start_page=}-{end_page=} invalid.")

    

