from pathlib import Path

import torch

from src.text_processors.str_to_sentences import split_into_sentences
from TTS.api import TTS
from parsers.pdf_parser import PdfParser
from parsers.paddle_ocr_parser import PaddleOCRParser
from src.text_processors.post_processor import PostProcessor

# TODO: check a way to disable logging centrally
if __name__ == "__main__":
    # post_processor = PostProcessor()

    # TXT FROM PDF
    # pdf_parser = PdfParser("path/to/pdf", post_processor=post_processor)
    # result = pdf_parser.extract_txt_from_pdf(12, 14)
    # print(f"{result=}")

    # TXT FROM PaddleOCR
    # ocr = PaddleOCRParser(post_processor=post_processor)
    # result = ocr.local_img_to_txt(Path("test.png"))
    
    # res_sentences = split_into_sentences(result)
    # print(res_sentences)
    res_sentences = ['asdasdasd', 'asdasdqweqwe']
    # IMG TO TXT
    # ocr = PaddleOCRParser(lang='en', show_log=False)
    # img_path = Path("test.png")
    # cls=False --> images are not expected to be rotated 180 degrees, 
    #               to increase performance cls is set to False
    # result = ocr.local_img_to_txt(img_path, _cls=False)

    # TTS
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"{dev=}")
    # TODO: https://docs.coqui.ai/en/dev/models/xtts.html --> check this site for more info about XTTS_v2
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(dev)
    tts.tts_to_file(text=res_sentences, speaker_wav=[
        "audio_nl_sample1.mp3",
        "audio_nl_sample2.mp3",
        "audio_nl_sample3.mp3",
        "audio_nl_sample4.mp3",
        "audio_nl_sample5.mp3",
        "audio_nl_sample6.mp3",
        "audio_nl_sample7.mp3",
        "audio_nl_sample8.mp3",
    ], language="nl", file_path="test.wav", split_sentences=False)