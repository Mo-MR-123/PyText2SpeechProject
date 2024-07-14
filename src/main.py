from pathlib import Path

import torch

from TTS.api import TTS
from parsers.pdf_parser import PdfParser
from parsers.paddle_ocr_parser import PaddleOCRParser

if __name__ == "__main__":
    # TXT FROM PDF
    pdf_parser = PdfParser("ELEMENTAIRE GEWOONTES. Kleine veranderingen, groot resultaat - James Clear.pdf")
    result = pdf_parser.extract_txt_from_pdf(12, 13)
    print(f"{result=}")
    
    # IMG TO TXT
    # ocr = PaddleOCRParser(lang='en', show_log=False)
    # img_path = Path("test.png")
    # cls=False --> images are not expected to be rotated 180 degrees, 
    #               to increase performance cls is set to False
    # result = ocr.local_img_to_txt(img_path, _cls=False)

    # TTS
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"{dev=}")
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(dev)
    tts.tts_to_file(text=result, speaker_wav="audio.mp3", language="nl", file_path="output.wav")