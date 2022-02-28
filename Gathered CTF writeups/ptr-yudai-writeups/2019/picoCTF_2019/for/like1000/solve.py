import tarfile
import os

x = 1000

while x > 0:
    print(x)
    if not tarfile.is_tarfile("{}.tar".format(x)):
        break
    with tarfile.open("{}.tar".format(x)) as tar:
        tar.extractall('./')
    if x < 1000:
        os.unlink("{}.tar".format(x))
    x -= 1
