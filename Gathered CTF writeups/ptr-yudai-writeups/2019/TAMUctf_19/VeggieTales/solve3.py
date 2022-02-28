from ptrlib import *
import pickletools
import base64

def add_list(num):
    sock.recvuntil("watch list")
    sock.sendline("1")
    sock.recvuntil("list:")
    sock.sendline(str(num))
    
def backup_list():
    sock.recvuntil("watch list")
    sock.sendline("3")
    sock.recvuntil("(Don't lose it!):")
    b64 = sock.recvline()
    return base64.b64decode(b64.rstrip())

def load_list(data):
    sock.recvuntil("watch list")
    sock.sendline("4")
    sock.recvuntil(":")
    sock.sendline(base64.b64encode(data))
    if b"Invalid backup" in sock.recvline():
        return False
    else:
        return True

sock = Socket("pwn.tamuctf.com", 8448)
add_list(39)
a = backup_list()
sock.close()
#a_orig = b"42. MacLarry and the Stinky Cheese Battle"
a_orig = b"37. The Little Drummer Boy"

sock = Socket("pwn.tamuctf.com", 8448)
add_list(37)
b = backup_list()
sock.close()
#b_orig = b"44. Veggies in Space: The Fennel Frontier"
b_orig = b"39. The Penniless Princess"

print(a.hex())
print(b.hex())


diff = b''
for x in zip(a, b):
    diff += bytes([x[0] ^ x[1]])

diff_orig = b''
for x in zip(a_orig, b_orig):
    diff_orig += bytes([x[0] ^ x[1]])

print(diff)
print(diff_orig)
