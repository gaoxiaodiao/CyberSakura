buf = open("art.png", "rb").read()
open("file.pdf", "wb").write(buf[3408641:])
open("file.zip", "wb").write(buf[3408641 + 22044:])
