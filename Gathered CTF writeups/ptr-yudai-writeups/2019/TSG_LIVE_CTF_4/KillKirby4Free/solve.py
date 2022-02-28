from ptrlib import *

def walk_inhale(name):
    sock.sendlineafter("> ", "1")
    sock.sendlineafter("> ", "1")
    sock.sendafter("> ", name)
    return
def walk_kill():
    sock.sendlineafter("> ", "1")
    sock.sendlineafter("> ", "2")
    return
def walk_escape():
    sock.sendlineafter("> ", "1")
    sock.sendlineafter("> ", "3")
    return
def list():
    sock.sendlineafter("> ", "2")
    while True:
        line = sock.recvline()
        if line == b'': break
        print(line)
    return
def rename(index, name):
    sock.sendlineafter("> ", "4")
    sock.sendlineafter("> ", str(index))
    sock.sendafter("> ", name)
    return

sock = Process("./kill_kirby")

for i in range(6):
    walk_inhale(str(i + 1))

sock.interactive()
