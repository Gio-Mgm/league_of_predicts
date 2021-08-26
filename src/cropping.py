""" cropping on the image """

import os

def crop_image(im, left, top, width, height, name=None):
	"""
		Crop desired part of image
		
		left, top: x y of left corner of image in % 
		width, height: widht, height of image in %

	"""
	im_size = im.size
	x = im_size[0]
	y = im_size[1]

	# Define box inside image

	left *= x
	top *= y
	width *= x
	height *= y

	# Create Box
	box = (left, top, left+width, top+height)

	# Crop Image
	area = im.crop(box)
	area.resize((area.size[0]*3, area.size[1]*3)).show()
	#display(area)

	# Save Image
	area.save(f"/{name}.png", "PNG")

def crop_numericals(im):
	"""
		Extracting numerical datas from image,
		then save them in a folder
	"""
	if not os.path.exists("./data"):
		os.mkdir("./data")
	if not os.path.exists("./data/ocr"):
		os.mkdir("./data/ocr")
	if not os.path.exists("./data/ocr/gold"):
		os.mkdir("./data/ocr/gold")
	if not os.path.exists("./data/ocr/score"):
		os.mkdir("./data/ocr/score")
	if not os.path.exists("./data/ocr/kda"):
		os.mkdir("./data/ocr/kda")
	if not os.path.exists("./data/ocr/cs"):
		os.mkdir("./data/ocr/cs")
	if not os.path.exists("./data/ocr/time"):
		os.mkdir("./data/ocr/time")

	crop_image(im, .49,   .073,  .012,  .02,  "./data/ocr/time/time_min")
	crop_image(im, .503,  .073,  .012,  .02,  "./data/ocr/time/time_sec")
	crop_image(im, .397,  .018,  .031,  .016, "./data/ocr/gold/blue_golds")
	crop_image(im, .597,  .018,  .032,  .018, "./data/ocr/gold/red_golds")
	crop_image(im, .351,  .018,  .0105, .017, "./data/ocr/score/blue_turrets")
	crop_image(im, .474,  .0225, .02,   .029, "./data/ocr/score/blue_kills")
	crop_image(im, .516,  .02,   .02,   .029, "./data/ocr/score/red_kills")
	crop_image(im, .659,  .018,  .015,  .018, "./data/ocr/score/red_turrets")
	crop_image(im, .5515, .803,  .04,  .0138, "./data/ocr/kda/red_top_kda")
	crop_image(im, .5515, .8435, .04,  .0138, "./data/ocr/kda/red_jgl_kda")
	crop_image(im, .5515, .884,  .04,  .0138, "./data/ocr/kda/red_mid_kda")
	crop_image(im, .5515, .925,  .04,  .0138, "./data/ocr/kda/red_adc_kda")
	crop_image(im, .5515, .966,  .04,  .0138, "./data/ocr/kda/red_sup_kda")
	crop_image(im, .418,  .803,  .04,  .0141, "./data/ocr/kda/blue_top_kda")
	crop_image(im, .418,  .8435, .04,  .0141, "./data/ocr/kda/blue_jgl_kda")
	crop_image(im, .418,  .8845, .04,  .0141, "./data/ocr/kda/blue_mid_kda")
	crop_image(im, .418,  .9252, .04,  .0141, "./data/ocr/kda/blue_adc_kda")
	crop_image(im, .418,  .966,  .04,  .0141, "./data/ocr/kda/blue_sup_kda")
	crop_image(im, .533, .803,  .017, .015,   "./data/ocr/cs/red_top_cs")
	crop_image(im, .533, .8435, .017, .015,   "./data/ocr/cs/red_jgl_cs")
	crop_image(im, .533, .884,  .017, .015,   "./data/ocr/cs/red_mid_cs")
	crop_image(im, .533, .924,  .017, .015,   "./data/ocr/cs/red_adc_cs")
	crop_image(im, .533, .966,  .017, .015,   "./data/ocr/cs/red_sup_cs")
	crop_image(im, .4595, .803,  .017, .015,  "./data/ocr/cs/blue_top_cs")
	crop_image(im, .4595, .8435, .017, .015,  "./data/ocr/cs/blue_jgl_cs")
	crop_image(im, .4595, .884,  .017, .015,  "./data/ocr/cs/blue_mid_cs")
	crop_image(im, .4595, .925,  .017, .015,  "./data/ocr/cs/blue_adc_cs")
	crop_image(im, .4595, .966,  .017, .015,  "./data/ocr/cs/blue_sup_cs")

	print("Cropping done !")
	
