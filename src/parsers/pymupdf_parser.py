
import pymupdf
import threading

from pathlib import Path
from src.parsers.base_parser import BaseParser
from loggers.log_config import LogConfig

log_config = LogConfig()

"""
TODO: implement functionality for filetype checking to avoid erronous reading of files.
TODO: Make resrouce management thread-safe! (needed if we only open pdf for reading and not writing?)
NOTE: PyMuPDF can open many non-pdf files as txt -> https://pymupdf.readthedocs.io/en/latest/how-to-open-a-file.html#opening-files-as-text
Supported filetypes by PyMuPDF: https://pymupdf.readthedocs.io/en/latest/how-to-open-a-file.html#supported-file-types
"""
class PyMuPDFParser(BaseParser):
    def __init__(
        self, 
        pdf_path: Path,
        remove_reference_links: bool = True
    ):
        self.pdf_path = str(pdf_path)
        self.remove_reference_links = remove_reference_links
        
        self._lock = threading.Lock()
        
        # Open the source PDF
        self._pdf_reader = pymupdf.open(self.pdf_path)
        self._logger = log_config.get_logger(self.__class__.__name__)

        # Remove all links from the file stream
        if self.remove_reference_links:
            self.remove_all_links()
    
    def extract_text_from_page(self, page_number: int) -> str:
        """
        encoding -> https://pymupdf.readthedocs.io/en/latest/textpage.html#TextPage.extractTEXT
        """
        with self._lock:
            if 0 <= page_number < self._pdf_reader.page_count:
                page = self._pdf_reader.load_page(page_number)
                return page.get_text()
            else:
                raise ValueError(f"Page number {page_number=} out of range.")

    def remove_all_links(self) -> None:
        """
        FROM -> https://www.linkedin.com/pulse/streamline-your-pdfs-effortlessly-remove-annotations-targeted-arshad-pyjuc
        """
        # raise NotImplementedError("TODO: Implement this method")
            
        for page in self._pdf_reader:
            # Apply two types of removal.
            # Find the text and remove it
            # Find the link and remove it
            
            # Get the list of text instances 
            # text_instances = page.search_for("Text to search")
            # for text in text_instances:
            #     print(f'Rect found: {text}')
            #     # text points to Rect
            #     page.add_redact_annot(text)
            
            # Get all links on that page
            links = page.get_links()
            for link in links:
                print(link)
                # for any specific links to remove, replace
                # if link['uri']:
                if link['kind'] != pymupdf.LINK_NONE:
                    self._logger.info(f'Link found: {link}')                    
                    page.add_redact_annot(link["from"]) # link['from'] contains the Rect
                    page.delete_link(link)
            
            # Apply the redaction (removal)
            page.apply_redactions(pymupdf.PDF_REDACT_IMAGE_NONE)

        # Save the modified PDF
        # self._pdf_reader.save(self.pdf_path) # TODO: do we need to overwrite pdf file to see changes of removal?
        self._logger.info(f"Processed PDF saved as '{self.pdf_path}'.")

    def extract_text_between_pages(self, start_page: int, end_page: int) -> str:
        """
        encoding -> https://pymupdf.readthedocs.io/en/latest/textpage.html#TextPage.extractTEXT
        """
        with self._lock:
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
        # txt = self._pdf_reader[start_page : end_page]
        # self._logger.info(txt)
        # return txt
    
    def close(self):
        with self._lock:
            self._pdf_reader.close()
