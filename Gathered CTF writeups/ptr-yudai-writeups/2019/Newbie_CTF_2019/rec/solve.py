import re
asm = """mov     [esp+30h+var_20], 4Bh
mov     [esp+30h+var_1F], 6Fh
mov     [esp+30h+var_1E], 72h
mov     [esp+30h+var_1D], 4Eh
mov     [esp+30h+var_1C], 65h
mov     [esp+30h+var_1B], 77h
mov     [esp+30h+var_1A], 62h
mov     [esp+30h+var_19], 69h
mov     [esp+30h+var_18], 65h
mov     [esp+30h+var_17], 7Bh
mov     [esp+30h+var_16], 52h
mov     [esp+30h+var_15], 65h
mov     [esp+30h+var_14], 63h
mov     [esp+30h+var_13], 6Fh
mov     [esp+30h+var_12], 76h
mov     [esp+30h+var_11], 65h
mov     [esp+30h+var_10], 72h
mov     [esp+30h+var_F], 5Fh
mov     [esp+30h+var_E], 53h
mov     [esp+30h+var_D], 69h
mov     [esp+30h+var_C], 67h
mov     [esp+30h+var_B], 6Eh
mov     [esp+30h+var_A], 61h
mov     [esp+30h+var_9], 74h
mov     [esp+30h+var_8], 75h
mov     [esp+30h+var_7], 72h
mov     [esp+30h+var_6], 65h
mov     [esp+30h+var_5], 7Dh
mov     [esp+30h+var_4], 0
"""

flag = ""
for line in asm.split("\n"):
    r = re.findall(", ([0-9A-F]+)h", line)
    if r == []: continue
    flag += chr(int(r[0], 16))

print(flag)
