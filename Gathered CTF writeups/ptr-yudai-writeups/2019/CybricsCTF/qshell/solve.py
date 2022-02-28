from PIL import Image
from pyzbar.pyzbar import decode
import qrcode
from time import sleep
from ptrlib import *

def receive():
    qr = [[]]
    data = sock.recvuntil("\n\n.").rstrip(b'.').rstrip()
    sock.recvline()
    data += b'#'
    offset = 0
    while offset < len(data):
        if data[offset] == 0xe2:
            qr[-1].append(255)
            offset += 3
        elif data[offset] == 0x20:
            qr[-1].append(0)
            offset += 1
        elif data[offset] == 0x0a:
            qr.append([])
            offset += 1
        else:
            break

    image = Image.new('RGB', (len(qr), len(qr[0])), (255, 255, 255))
    size = len(qr)
    for y, line in enumerate(qr):
        for x, c in enumerate(line):
            c = qr[y][x]
            image.putpixel((x, y), (c, c, c))
    image = image.resize((size * 3, size * 3))
    image.save("last.png")

    result = decode(image)
    return result[0][0]

def send(cmd):
    qr = qrcode.QRCode(box_size=1, border=4, version=20)
    qr.add_data(cmd)
    qr.make()
    img = qr.make_image(fill_color="white", back_color="black")

    data = b''
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r = img.getpixel((x, y))
            if r == (0, 0, 0):
                data += b'\xe2\x96\x88'
            else:
                data += b' '
        data += b'\n'
    data += b'\n.'

    sock.sendline(data)
    return

if __name__ == '__main__':
    sock = Socket("spbctf.ppctf.net", 37338)

    while True:
        print(bytes2str(receive()), end="")
        cmd = input()
        send(cmd)
        
    sock.interactive()
