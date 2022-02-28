import subprocess

encrypted = open("eflag.txt", "rb").read()

flag = ""
for i in range(len(encrypted)):
    found = False
    for ci in range(0, 0x100):
        c = chr(ci)
        p = subprocess.Popen(
            ["./encrypt"], stdin=subprocess.PIPE, stdout=subprocess.PIPE
        )
        out, err = p.communicate((flag + c).encode())
        if out == encrypted[: i + 1]:
            flag += c
            print(flag)
            found = True
            break
    if not found:
        print("[+]ERR")
        exec()
