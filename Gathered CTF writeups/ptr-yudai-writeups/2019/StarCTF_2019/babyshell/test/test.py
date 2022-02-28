from pwn import *

shellcode = '''
syscall
'''

bytecode = asm(shellcode, arch='amd64', bits=64)
print(disasm(bytecode, arch='amd64', bits=64))
print(repr(bytecode))

message = 'ZZJ loves shell_code,and here is a gift:\x0f\x05 enjoy it!\n

for c in bytecode:
    if c not in message:
        print("Invalid character!!: {} ({})".format(repr(c), hex(ord(c))))
        break
else:
    print("OK!! :)")
