# --------------------------------------------------------------------------- #
# Date: 06/07/17; modified 06/09/17
# Authors: Richard Lu and Michael Fermanian
# Description:
#   bootstrap a folder up (or down) to set number of photos
# Runtime: 
# --------------------------------------------------------------------------- #

import glob
import math
import os
import random
import sys
from PIL import Image, ImageColor

# =========================================================================== #
# EXAMPLE USAGE
# =========================================================================== #

# python2 bootstrap_photo_folder.py folder amount
# folder = high_professional
# amount = 1000

# =========================================================================== #
# LOAD ENVIRONMENT
# =========================================================================== #

base_dir = "/home/phd/richard_lu/bulk/wonolo"
photo_dir = os.path.join(base_dir, "0_data_collection", "photos")

folder = sys.argv[1]
amount = int(sys.argv[2])
classname = sys.argv[3]
start_value = int(sys.argv[4])
#folder = "/warmth/train_5.3_5.0_3.8_3.5/high_warmth/"
#amount = 16

specific_folder = photo_dir + folder

original_photos = glob.glob(os.path.join(specific_folder, "*_{}.jpg".format(
	classname)))

counter = start_value 

# =========================================================================== #
# RANDOMLY BOOTSTRAP UP OR DOWN
# =========================================================================== #

random.seed(30)
"""
original_length = len(original_photos)

if original_length < amount:
	diff = amount - original_length
	copies = diff / original_length
    for i in range(amount-original_length):
        tmp_file = random.sample(original_photos,1)[0].split(".jpg")[0]
        os.system("cp {}.jpg {}_b{}.jpg".format(tmp_file, tmp_file, i))
elif original_length > amount:
    for i in range(original_length-amount):
        tmp_file = random.sample(original_photos,1)[0]
        original_photos.pop(original_photos.index(tmp_file))
        os.system("rm {}".format(tmp_file))
else:
    pass
"""

# =========================================================================== #
# ROTATE WITHIN A RANGE OF DEGREES
# =========================================================================== #

def rotate(num_times):
	global counter
	for num in range(num_times):
		for photo in original_photos:
			#the subset which will not be manipulated is the original set of 	
			#if '_b' in photo:
			r = Image.open(photo)
			deg = random.sample(range(-45,45,5),1)[0]
			r = r.rotate(deg)
			tmp = photo.split(".jpg")[0]
			r.save("{}_{}r{}.jpg".format(tmp, counter, deg))
			counter += 1


# =========================================================================== #
# RANDOM CROP
# =========================================================================== #
#cut out the top and bottom 20% of a photo, and the left and right 25%
def crop(num_times):
	global counter
	for num in range(num_times):
		for photo in original_photos:
			#if '_b' in photo:
			im = Image.open(photo)
			w, h = im.size
			p1, p2 = .25*w, .2*h
			p1 = int(math.ceil(p1 + (random.sample(range(-10,10),1)[0]/100.0)*w))
			p2 = int(math.ceil(p2 + (random.sample(range(-10,10),1)[0]/100.0)*h))
			#im = im.crop((p1, p2, w-p1, h-p2))
			for x in range(p1):
				for y in range(h):
					im.putpixel((x,y), ImageColor.getcolor('white', 'RGBA'))
			for x in range(w-p1, w):
				for y in range(h):
					im.putpixel((x,y), ImageColor.getcolor('white', 'RGBA'))
			for y in range(p2):
				for x in range(w):
					im.putpixel((x,y), ImageColor.getcolor('white', 'RGBA'))
			for y in range(h-p2, h):
				for x in range(w):
					im.putpixel((x,y), ImageColor.getcolor('white', 'RGBA'))
			tmp = photo.split(".jpg")[0]
			im.save("{}_{}c_{}_{}.jpg".format(tmp,counter,p1,p2))
			counter += 1


rotate(amount)
crop(amount)
