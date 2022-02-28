from ptrlib import *

elf = ELF("./vuln")

print(elf.got("exit"))
print(0x80485c6)
