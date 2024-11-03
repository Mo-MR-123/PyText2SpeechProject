# import torch
import os
import warnings

# Suppress all warnings since this is a GUI app
# Warnings present during debugging only
if not os.getenv("DEBUG_FLAG", default=0):
    warnings.filterwarnings("ignore")

# from pathlib import Path
# from TTS.api import TTS
# from src.text_processors.str_to_sentences import split_into_sentences
# from src.parsers.pypdf_parser import PyPdfParser
# from src.text_processors.pre_processor import PreProcessor
from core.src.ui.tk_window_main import TkWindowMain
# from tkinter import Tk
# from src.parsers.paddle_ocr_parser import PaddleOCRParser

def main() -> None:
    TkWindowMain("test title").run_mainloop()

    # pre_processor = PreProcessor()

    # TXT FROM PDF
    # pdf_parser = PdfParser("path/to/pdf", post_processor=post_processor)
    # result = pdf_parser.extract_txt_from_pdf(12, 14)
    # print(f"{result=}")

    # TXT FROM PaddleOCR
    # ocr = PaddleOCRParser(post_processor=post_processor)
    # result = ocr.local_img_to_txt(Path("test.png"))
    
    # result = """ 
    # """

    # res_sentences_splitted = split_into_sentences(result)
    # print(f"{res_sentences_splitted=}")

    # remove punctuations from sentences so that voice generations
    # is less likely to contain gibberish noise, repeating or unintelligible sound
    # res_sentences_no_punctuations = pre_processor.remove_punctuations(res_sentences_splitted)
    # print(f"{res_sentences_no_punctuations=}")

    # res_sentences = 'asdasdqweqwe'
    # IMG TO TXT
    # ocr = PaddleOCRParser(lang='en', show_log=False)
    # img_path = Path("test.png")
    # cls=False --> images are not expected to be rotated 180 degrees, 
    #               to increase performance cls is set to False
    # result = ocr.local_img_to_txt(img_path, _cls=False)

    # TTS
    # dev = "cuda" if torch.cuda.is_available() else "cpu"
    # print(f"{dev=}")

    # TODO: https://docs.coqui.ai/en/dev/models/xtts.html --> check this site for more info about XTTS_v2
    # tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(dev)
    # tts.tts_to_file(text=res_sentences_no_punctuations, speaker_wav=[
    #     # "audio_cindy_nl_sample1.wav", # TODO: longer samples of voice do not necessarily lead to better output. It also decreases performance.
    #     # "audio_cindy_nl_sample2.wav",
    #     # "audio_cindy_nl_sample3.wav",
    #     # "audio_cindy_nl_sample4.wav",
    #     "audio_cindy_nl_sample5_short.wav",
    #     "audio_cindy_nl_sample6_short.wav",
    #     "audio_cindy_nl_sample7_short.wav",
    #     "audio_cindy_nl_sample8_short.wav",
    # ], language="nl", file_path="test.wav", split_sentences=False)