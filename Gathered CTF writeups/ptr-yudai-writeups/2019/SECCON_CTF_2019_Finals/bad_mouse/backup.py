from PIL import Image

s = b"?@aBcDAUiHkJKLMNQPOaS\\UVWXY`kemgoiAqcdEywLyN{P]Mopqrstuvwxyz{|}~OHrQCLEFGHiN[U]W_YqXSTUVWXYZ[\\]^_`}fElGnIpmqklk}QxSzU|w~wxuA}D?FAHEFCDAMIPKRMTQROPMYU\\W^Y`Ua[\\[mc`ibsdcughIjKlK}p@rBstwzY@kBeDCE?@CBERgGaHOJKLINQYS[UYQYWXyakemgoiAgcdelwqys{uM}opw~KwUvO{?F{|IDQIcJUMQLGHgP]T_VaXsYSTSeg`ibkd}e_`cbedcuihkjklmt?yA{C}UEwxuz}E?GAE}ECDAFIQKSMQIQOPqYc\\e^g`y^[\\UeshsjulEmghejmuowqumustS|I@KBMD_E?@?QSLUNWPiQKLORqXCZ}\\[]WXQaodofqhAicdqlyqKr}uytopOxE|G~I@[A{|[DQHSJULgMGHIJ[T~]OXQRSTuYoZ_\\Yk]`_`gb{dEu?hojklMu?xAzC|UzwxYz[|yMa@cBCDELWQYS[Um]OPoXe\\g^i`{a[\\[mohqjslEmghGp}t?vAxSystvFxHWI[|]~?@B"

W = 0
def pon(R22):
    W = 0
    R23 = 9
    while True:
        W = (W & 0xff00) + (((W & 0xff) * 2) & 0xff)
        R23 -= 1
        if R23 == 0: break
        W = ((W & 0xff00) * 2) + (W & 0xff)
    return -1 - (W & 0xff)

def get_next_offset(R22):
    return -pon(R22 ^ (W & 0xff))
"""
def get_next_click():
    W = get_next_offset(6)
    print(W)
    R20 = W >> 8 # Whi: bit offset
    offset = offset_ + (W & 0xff) # Wlo: byte offset
    Z = s[offset]
    while True:
        R20 -= 1
        if R20 < 0: break
        Z >>= 1
    return Z & 1
#"""
w = b''.join([bytes([i]) for i in range(0x3f, 0x7f)])
def get_next_click():
    for i in range((len(s) // 0x40) * 0x40):
        for j in range(8):
            yield (((w[i % 0x40] ^ s[i]) % 0x100) >> j) & 1

img = Image.new('L', (600, 64), 255)

cur = 0
offset_ = 0
x, y, delta = 1, 0, 1
g = get_next_click()
direction = 0
for na in range(16 * 0x40):
    for i in range(8):
        try:
            if next(g) == 1:
                if delta == 1:
                    img.putpixel((x, y*4 + delta), 0)
                    img.putpixel((x, y*4 + delta + 1), 0)
                    img.putpixel((x, y*4 + delta + 2), 0)
                    img.putpixel((x, y*4 + delta + 3), 0)
                else:
                    img.putpixel((x, 60 - y*4 - delta - 1), 0)
                    img.putpixel((x, 60 - y*4 - delta - 2), 0)
                    img.putpixel((x, 60 - y*4 - delta - 3), 0)
                    img.putpixel((x, 60 - y*4 - delta - 4), 0)
        except:
            img.resize((1200, 128)).save("output.png")
            exit()
        y += delta
    if delta == 1:
        x += 1
        direction += 1
        if direction > 11:
            direction = 11
        delta = -1
    else:
        x += 1
        direction -= 1
        if direction < 0:
            direction = 0
        delta = 1

