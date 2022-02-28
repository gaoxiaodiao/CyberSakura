from ptrlib import *

chall = "27BDFFF8 2020000A 20210002 AFA10000 20410004 AFA20004 27BD0008"
code = b''
for block in chall.split(" "):
    code += bytes.fromhex(block)[::-1]

print(disasm(code, arch="mips", mode="32", returns=str))

"""
0:      addiu   $sp, $sp, -8
4:      addi    $zero, $at, 0xa
8:      addi    $at, $at, 2
c:      sw      $at, ($sp)
10:     addi    $at, $v0, 4
14:     sw      $v0, 4($sp)
18:     addiu   $sp, $sp, 8
"""

# KorNewbie{16}
