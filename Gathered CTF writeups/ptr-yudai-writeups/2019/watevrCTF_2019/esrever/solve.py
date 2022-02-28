# gdb -n -q -x solve.py ./esrever
import gdb
import re

gdb.execute("set disassembly intel")
gdb.execute("set pagination off")
gdb.execute("break *0x555555554ba0")
gdb.execute("run << /dev/null")

flag = ""
while True:
    gdb.execute("nexti")
    line = gdb.execute("x/1i $rip", to_string=True)
    r = re.findall("\t([a-z]+) ", line)
    if r == [] or r[0] != 'cmp':
        continue
    r = re.findall("QWORD PTR \[rbp(.+)\]", line)
    if r == []:
        continue
    ofs = int(r[0], 16)
    line = gdb.execute("x/1bx $rbp+({})".format(ofs), to_string=True)
    c = line.split(":\t")[1]
    flag += chr(int(c, 16))
    print(flag)
    gdb.execute("set $rax={}".format(c))
    
