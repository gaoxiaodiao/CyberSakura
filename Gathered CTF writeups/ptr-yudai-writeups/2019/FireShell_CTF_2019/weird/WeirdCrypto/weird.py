import random
import pyminizip
from PIL import Image
from gmpy2080 import get_all_names_from_image
#gmpy2080 is the perfect Reverse Image Search API

img = Image.open('names.jpg') #This image contains all characters from this source
namelist = list(img.get_all_names_from_image())
password = random.choice(namelist)

files = "N0.txt UwU.zip XwX.jpg weird_animal"
pyminizip.compress(files, "OwO.zip", password, compression_level)