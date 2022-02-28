from pwn import *

message = 'ZZJ loves shell_code,and here is a gift:\x0f\x05 enjoy it!\n'

out = ''
for i in range(0x100):
    if chr(i) not in message:
        out += "\\x{:02x}".format(i)
print(out)
