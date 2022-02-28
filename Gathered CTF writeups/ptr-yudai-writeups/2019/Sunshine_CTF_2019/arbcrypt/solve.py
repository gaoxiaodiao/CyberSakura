import base64

with open("ciphertext.txt", "rb") as f:
    b64 = f.read()

cipher = base64.b64decode(b64)

key = b"arb"

flag = ""
for i in range(len(cipher)):
    flag += chr(cipher[i] ^ key[i % len(key)])

print(flag)
