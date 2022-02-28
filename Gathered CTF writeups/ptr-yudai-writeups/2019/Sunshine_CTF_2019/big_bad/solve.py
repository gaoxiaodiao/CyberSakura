from PIL import Image

img = Image.open("BigBad.png")

enc = ""
for x in range(img.size[0]):
    c = img.getpixel((x, 0))
    enc += str(c[0] & 1)

def huffmanDecode(dictionary, text):
    res = ""
    while text:
        for k in dictionary:
            if text.startswith(k):
                res += dictionary[k]
                text = text[len(k):]
                break
        else:
            break
    return res

table = {
    "000": "s",
    "0010": "u",
    "0011": "_",
    "010": "0",
    "0110": "d",
    "0111": "9",
    "1000": "5",
    "10010": "n",
    "10011": "h",
    "10100": "l",
    "10101": "a",
    "10110": "e",
    "10111": "b",
    "1100": "1",
    "11010": "{",
    "11011": "}",
    "11100": "r",
    "11101": "c",
    "11110": "k",
    "11111": "3"
}

print(huffmanDecode(table, enc))
