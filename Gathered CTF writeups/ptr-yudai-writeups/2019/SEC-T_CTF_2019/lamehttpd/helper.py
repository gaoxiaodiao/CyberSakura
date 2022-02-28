#! /usr/bin/env python2

from pwn import *
import binascii
import time
import sys
import re
import os

context.terminal = 'hyper'

cmd = ""
context(arch = 'arm', os = 'linux', endian='little')
context.log_level = 'debug'

env = {'LD_LIBRARY_PATH':'/usr/arm-linux-gnueabi/lib/'}
p = process(["qemu-arm", "-g", "1337", "./lamehttpd"], env=env)
gdb.attach(target=(0, 1337), gdbscript='''
{}
set print pretty on
#continue
'''.format(cmd), exe="./lamehttpd", arch="arm")

sleep(2)
p.interactive()

