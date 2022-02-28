from pwn import *
import ctypes
import time

glibc = ctypes.cdll.LoadLibrary('./libc-2.27.so')
glibc.srand(glibc.time(0))

sock = remote("35.198.143.204", 32590)
sock.sendlineafter("\n", "taro")

randList = []
randCnt = 0
def rand(i):
    if i >= len(randList):
        for j in range(i - len(randList) + 1):
            randList.append(glibc.rand())
    return randList[i]

def firewall(option):
    sock.sendlineafter("Enter option:", "2")
    sock.sendlineafter("Option: ", str(option))
    return

def activate(option):
    sock.sendlineafter("Enter option:", "3")
    time.sleep(0.01)
    sock.sendlineafter("Option: ", str(option))

def get_state():
    sock.recvuntil("round : ")
    r = int(sock.recvline())
    sock.recvuntil(": ")
    player_hp = int(sock.recvline())
    sock.recvuntil(": ")
    hacker_hp = int(sock.recvline())
    sock.recvuntil(": ")
    defence = int(sock.recvline())
    return r, player_hp, hacker_hp, defence

#sock = Process("./pwn_honeypot")


while True:
    r, myhp, hp, defence = get_state()
    if hp < 0: break

    print(myhp, hp, defence)

    if rand(randCnt) % 0x1e > 4:
        firewall(1)
        randCnt += 1
    else:
        firewall(2)
    activate(rand(randCnt) & 0b11)
    randCnt += 1

sock.interactive()

