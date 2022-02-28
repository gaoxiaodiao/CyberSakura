from pwn import *

io = process("./pwn_baby_rop")

io.recvuntil("black magic.\n")

gdb.attach(io)

payload = b""
payload += cyclic(1024, n=8).encode()

io.sendline(payload)
io.interactive()
