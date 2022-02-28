from pyzbar.pyzbar import decode
from PIL import Image
import glob
from secretsharing import PlaintextToHexSecretSharer
import random

shares = []
for path in glob.glob("*.png"):
    result = decode(Image.open(path))
    shares.append(result[0][0])
    print(result[0][0])

print(PlaintextToHexSecretSharer.recover_secret(
    random.sample(shares, 10)
))
