# gdb -n -q -x solve.py ./chal
import gdb

gdb.execute("set pagination off")
gdb.execute("b *0x55555555494b")
gdb.execute("run")

flag = ""
for _ in range(0x0D):
    eax = gdb.execute("p $eax", to_string=True).strip().split("= ")[1]
    flag += chr(int(eax))
    gdb.execute("set $edx = {}".format(eax), to_string=True)
    gdb.execute("continue", to_string=True)
print(flag)
