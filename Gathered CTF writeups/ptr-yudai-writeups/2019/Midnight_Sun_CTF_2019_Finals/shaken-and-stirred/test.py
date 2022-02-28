from pwn import *

with open("encrypt", "rb") as f:
    binary = f.read()
with open("scrambled_buffer", "rb") as f:
    scrambled = f.read()

doit = asm("""
mov eax, 0x00e00c00
mov [rbx+0x100], eax
""", arch="amd64")
begin, end = 0x10af, 0x1148
ofs = binary.index(b"\x1b\x25\xed\x5f")
binary = binary[:ofs] + scrambled + binary[ofs+len(scrambled):]
binary = binary[:begin] + doit + b"\x90" * (end - begin - len(doit)) + binary[end:]

with open("patched", "wb") as f:
    f.write(binary)
