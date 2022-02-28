import zlib

with open("stream.bin", "rb") as f:
    buf = f.read()[2:]

while True:
    try:
        decoded = zlib.decompress(buf, -15)
        print(decoded)
        break
    except zlib.error as e:
        buf += b'\xff'
        if "incomplete" in str(e):
            continue
        else:
            print(e)
            exit()
