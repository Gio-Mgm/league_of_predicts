# -*- coding: utf-8 -*-
"""League_of_predict_ocr.ipynb

Original file is located at
    https://colab.research.google.com/drive/1X1_S9SaDq2OTiZlfiEZlesCb_cfs2RLt

#!pip install easyocr
"""

import os
import cv2 # Open Source Computer Vision Library for python
import easyocr # OCR
from PIL import Image


def get_box(im, left, top, width, height, name=None):
    """
        Crop desired part of image
        
        left, top: x y of left corner of image in % 
        width, height: widht, height of image in %

    """
    im_size = im.size
    x = im_size[0]
    y = im_size[1]

    # Define box inside image

    left   *= x
    top    *= y 
    width  *= x
    height *= y

    # Create Box
    box = (left, top, left+width, top+height)

    # Crop Image
    area = im.crop(box)
    area.resize((area.size[0]*3, area.size[1]*3)).show()
    #display(area)

    # Save Image
    area.save(f"/{name}.png", "PNG")


def preprocess_image(image):
    """
      apply preprocessing on an image

      params:
      image(ndarray): image to transform 

      returns: transformed image

    """

    image = cv2.resize(image,None,fx=4,fy=4, interpolation=cv2.INTER_CUBIC)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image = cv2.medianBlur(image, 5, 0)
    image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,1))
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=1)
    
    return image


def get_numeric_boxes(im):
    """
        Extracting numerical datas
    """
    if not os.path.exists("/data"):
      os.mkdir("/data")
    if not os.path.exists("/data/gold"):
      os.mkdir("/data/gold")
    if not os.path.exists("/data/score"):
      os.mkdir("/data/score")
    if not os.path.exists("/data/kda"):
      os.mkdir("/data/kda")
    if not os.path.exists("/data/cs"):
      os.mkdir("/data/cs")
    if not os.path.exists("/data/time"):
      os.mkdir("/data/time")

    time_min     = get_box(im, .49,   .073,  .012,  .02,  "data/time/time_min")
    time_sec     = get_box(im, .503,  .073,  .012,  .02,  "data/time/time_sec")
    blue_golds   = get_box(im, .397,  .018,  .031,  .016, "data/gold/blue_golds")
    red_golds    = get_box(im, .597,  .018,  .032,  .018, "data/gold/red_golds")
    blue_turrets = get_box(im, .351,  .018,  .0105, .017, "data/score/blue_turrets")
    blue_kills   = get_box(im, .474,  .0225, .02,   .029, "data/score/blue_kills")
    red_kills    = get_box(im, .516,  .02,   .02,   .029, "data/score/red_kills")
    red_turrets  = get_box(im, .659,  .018,  .015,  .018, "data/score/red_turrets")
    red_top_kda  = get_box(im, .5515, .803,  .04,  .0138, "data/kda/red_top_kda")
    red_jgl_kda  = get_box(im, .5515, .8435, .04,  .0138, "data/kda/red_jgl_kda")
    red_mid_kda  = get_box(im, .5515, .884,  .04,  .0138, "data/kda/red_mid_kda")
    red_adc_kda  = get_box(im, .5515, .925,  .04,  .0138, "data/kda/red_adc_kda")
    red_sup_kda  = get_box(im, .5515, .966,  .04,  .0138, "data/kda/red_sup_kda")
    blue_top_kda = get_box(im, .418,  .803,  .04,  .0141, "data/kda/blue_top_kda")
    blue_jgl_kda = get_box(im, .418,  .8435, .04,  .0141, "data/kda/blue_jgl_kda")
    blue_mid_kda = get_box(im, .418,  .8845, .04,  .0141, "data/kda/blue_mid_kda")
    blue_adc_kda = get_box(im, .418,  .9252, .04,  .0141, "data/kda/blue_adc_kda")
    blue_sup_kda = get_box(im, .418,  .966,  .04,  .0141, "data/kda/blue_sup_kda")
    red_top_cs   = get_box(im , .533, .803,  .017, .015,  "data/cs/red_top_cs")
    red_jgl_cs   = get_box(im , .533, .8435, .017, .015,  "data/cs/red_jgl_cs")
    red_mid_cs   = get_box(im , .533, .884,  .017, .015,  "data/cs/red_mid_cs")
    red_adc_cs   = get_box(im , .533, .924,  .017, .015,  "data/cs/red_adc_cs")
    red_sup_cs   = get_box(im , .533, .966,  .017, .015,  "data/cs/red_sup_cs")
    blue_top_cs  = get_box(im, .4595, .803,  .017, .015,  "data/cs/blue_top_cs")
    blue_jgl_cs  = get_box(im, .4595, .8435, .017, .015,  "data/cs/blue_jgl_cs")
    blue_mid_cs  = get_box(im, .4595, .884,  .017, .015,  "data/cs/blue_mid_cs")
    blue_adc_cs  = get_box(im, .4595, .925,  .017, .015,  "data/cs/blue_adc_cs")
    blue_sup_cs  = get_box(im, .4595, .966,  .017, .015,  "data/cs/blue_sup_cs")

"""## Extract results from ocr"""

def extract_ocr():
  reader = easyocr.Reader(['en']) # need to run only once to load model into memory
  DIR = "/data/"
  results = {}
  for folder in os.listdir(DIR):
    results[folder] = {}
    sub_path = os.path.join(DIR, folder)
    for filename in os.listdir(sub_path):
      file_path = os.path.join(DIR, folder, filename)
      image = cv2.imread(file_path)
      data = reader.readtext(preprocess_image(image), detail=1)
      if not data:
        data = "missing_value"
        print(data)
      else:
        result = data[0][1]
        proba = data[0][2]
        print(f"{result} - {round(proba*100, 2)}%")
      image = cv2.imread(file_path)
      results[folder][filename[:-4]] = [result, round(proba*100, 2)]
  return results



im   = Image.open("/screenshot_1.png")

get_numeric_boxes
res = extract_ocr()