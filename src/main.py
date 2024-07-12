from pathlib import Path
import logging

from parsers.paddle_ocr_parser import PaddleOCRParser
from PIL import Image


if __name__ == "__main__":
    ocr = PaddleOCRParser(lang='en', show_log=False)
    img_path = Path("test.png")
    # cls=False --> images are not expected to be rotated 180 degrees, 
    #               to increase performance cls is set to False
    result = ocr.local_img_to_txt(img_path, _cls=False)
    print(result)
    

    # result = result[0]
    # image = Image.open(img_path).convert('RGB')
    # boxes = [line[0] for line in result]
    # txts = [line[1][0] for line in result]
    # scores = [line[1][1] for line in result]
    # im_show = draw_ocr(image, boxes, txts, scores, font_path="./fonts/simfang.ttf")
    # im_show = Image.fromarray(im_show)
    # im_show.save('result.jpg')