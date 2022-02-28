with open("whitepages.txt", "rb") as f:
    buf = f.read()

buf = buf.replace(b"\xe2\x80\x83", b"0")
buf = buf.replace(b"\x20", b"1")

flag = ""
for i in range(0, len(buf), 8):
    flag += chr(int(buf[i:i+8], 2))
print(flag)
