from ptrlib import *

sock = Socket("crypto.chal.csaw.io", 1003)
target = sock.recvline()
print(target)

# enc(salt + <input> + pepper)

# find salt length
for salt_len in range(16):
    plaintext  = b'A' * (16 - salt_len)
    plaintext += b'1' * 32
    sock.sendlineafter(": ", plaintext)
    sock.recvline()
    r = sock.recvline()
    if r[32:64] == r[64:96]:
        break
logger.info("len(SALT) = " + str(salt_len))

#pepper = b'flag{y0u_kn0w_h0w_B10cks_Are_n0T_r31iab13..}'
pepper = b''
while True:
    for c in '._{}' + string.printable[:-6]:
        plaintext  = b'A' * (16 - salt_len)
        w = min(len(pepper), 15)
        x = max(0, len(pepper) - 15)
        plaintext += b'1' * (15 - w - (x % 16)) + rol(pepper, x)[:w] + bytes([ord(c)])
        plaintext += b'1' * (15 - (len(pepper) % 16))
        sock.sendlineafter(": ", plaintext)
        sock.recvline()
        r = sock.recvline()
        #q = 0 if len(pepper) < 16 else 32
        q = (len(pepper) // 16) * 32
        if r[64 + q:96 + q] == r[32:64]:
            pepper += bytes([ord(c)])
            print(pepper)
            break
    else:
        break
logger.info(b"PEPPER = " + pepper)
