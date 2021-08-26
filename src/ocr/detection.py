""" Optical Character Recognition with easyOCR and openCV """

import os
import cv2 # Open Source Computer Vision Library for python
import easyocr # OCR

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


def extract_results():
	"""Extract results from ocr"""
	reader = easyocr.Reader(['en']) # need to run only once to load model into memory
	DIR = "../data/ocr"
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
			else:
				result = data[0][1]
				proba = data[0][2]
				#image = cv2.imread(file_path)
				results[folder][filename[:-4]] = [result, round(proba*100, 2)]
	return results
