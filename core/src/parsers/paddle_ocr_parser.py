import logging

from src.parsers.base_parser import BaseParser
from paddleocr import PaddleOCR, draw_ocr
from pathlib import Path
from loggers.log_config import LogConfig
from src.text_processors.post_processor import PostProcessor

log_config = LogConfig(log_level=logging.DEBUG)

"""
PaddleOCR extracts text from images using a Computer Vision Model.
Thus far, this is best model I could find that can extract text
with high accuracy.
"""
class PaddleOCRParser(BaseParser):

    def __init__(
        self, 
        lang: str = "en", 
        show_log: bool =False,
        post_processor: PostProcessor = None, 
    ) -> None:
        """Init paddleOCR with args.

        Args:
            show_log (boolean): whether to show logs of paddleOCR or not. Default is False.
            lang (str, optional): Assumed language of image. Defaults to "en".
        """
        self.lang = lang
        self.show_log = show_log
        self.logger = log_config.get_logger(self.__class__.__name__)
        self.post_processor = post_processor

        # NOTE: we only initialize the paddle instance during txt extraction to save VRAM
        self.paddle = None 
    
    def init_paddle_object(self):
        """Initializes the paddle object 
        """
        self.paddle = PaddleOCR(lang=self.lang, show_log=self.show_log)
        # logging.getLogger('ppocr').handlers = [] # shut off paddle logging completely
        logging.getLogger('ppocr').setLevel(logging.ERROR) # this prevents additional warnings to be printed to stdout

    def set_lang(self, lang: str):
        """Change assumed language of images

        Args:
            lang (str): Assumed language. Supported langs: ['ch', 'en', 'korean', 'japan', 'chinese_cht', 'ta', 'te', 'ka', 'latin', 'arabic', 'cyrillic', 'devanagari']
        """
        assert self.paddle is None, "Paddle object is initialized, which should not be the case."
        self.lang = lang
        self.init_paddle_object()
        self.logger.info(f"PaddleOCR language change to {lang}")

    def local_img_to_txt(self, img_path: Path, conf_val: float = None, _cls: bool = False) -> str:
        """Extract text from local image.

        Args:
            _cls (boolean): whether to rotate text so that it is in a vertical position before OCR. Default: False.
            conf_val (float): value between 0 and 1 indicating confidence level to be acceptable for detecting text on images.
            img_path (Path): Path to the image to extraxt text from.
        """
        assert self.paddle is None, "Paddle object is initialized, which should not be the case."
        assert isinstance(img_path, Path), f"Path to image is not a Path instance. Instead it is {img_path}"
        if conf_val:
            assert (conf_val >= 0 or conf_val <= 1), f"conf_val {conf_val} is not between 0 and 1"
        
        # init paddle for the text extraction
        self.init_paddle_object()

        result = self.paddle.ocr(str(img_path), cls=_cls)
        extacted_txt_lst = []

        for res in result:
            for line in res:
                if conf_val and line[-1][1] >= conf_val: # conf value lies in line[-1][1]
                    extacted_txt_lst.append(line[-1][0]) # line[-1][0] contains extracted txt line
                else:
                    extacted_txt_lst.append(line[-1][0]) # line[-1][0] contains extracted txt line
        
        # post process extracted txt. TODO:
        if self.post_processor:
            extacted_txt_lst = self.post_processor.post_process_txt(extacted_txt_lst)

        # convert list of strings into one string
        extracted_txt = " ".join(extacted_txt_lst)

        # Deleting paddle instance to save VRAM!
        del self.paddle
        self.paddle = None

        return extracted_txt