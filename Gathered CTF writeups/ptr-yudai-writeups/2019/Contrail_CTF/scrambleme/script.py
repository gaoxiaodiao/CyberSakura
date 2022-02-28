# gdb -n -q -x script.py ./ScrambleMeBack
import gdb
import re
import string

gdb.execute("set pagination off")
gdb.execute("b *0x4983a5")
#gdb.execute("b *0x498347")
#gdb.execute("b *0x49837a")
gdb.execute("run < input")

#gdb.execute("i r")
gdb.execute("x/4xg $rdi")
#gdb.execute("quit")


"""
"AAAAAAAABBBBBBBB" --> 0x000000002b3e6935
"AAAAAAAAAAAABBBB" --> 0x000000002c3e6935
"AAAAAAAABBBBAAAA" --> 0x000000003f427452
"AAAAAAAACCCCCCCC" --> 0x000000005f6c2130
"AAAAAAAAAAAACCCC" --> 0x00000000303e6935
"""
