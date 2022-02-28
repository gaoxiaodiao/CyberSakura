buf = open("image1.png", "rb").read()
open("file.pdf", "wb").write(buf[5253:])
