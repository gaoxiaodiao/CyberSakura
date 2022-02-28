from pwn import *
import pickle

class Evil(object):
    def __init__(self, name):
        pass

data = {"MIKE": 123}
a = pickle.dumps(data, protocol=0)
sock = remote("misc.hsctf.com", 9977)
sock.recvline()
sock.sendline(a)

sock.interactive()
