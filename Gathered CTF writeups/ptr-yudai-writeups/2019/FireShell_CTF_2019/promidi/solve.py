from ptrlib import *
from pwn import *
import sys
import hashlib
import string
import random
import struct
import mido

def ascii85decode(data):
    n = b = 0
    out = b''
    for c in data:
        if b'!' <= c and c <= b'u':
            n += 1
            b = b*85+(ord(c)-33)
            if n == 5:
                out += struct.pack('>L', b)
                n = b = 0
        elif c == b'z':
            assert n == 0
            out += b'\0\0\0\0'
        elif c == b'~':
            if n:
                for _ in range(5-n):
                    b = b*85+84
                out += struct.pack('>L', b)[:n-1]
            break
    return out

sock = remote("35.231.144.202", 2007)

sock.recvuntil(":]: ")
ans = sock.recv(6)
while True:
    text = ''.join([random.choice(string.printable[:-6]) for i in range(8)])
    if hashlib.sha256(text).hexdigest()[-6:] == ans:
        break
print(text)
sock.sendline(text)
sock.sendline("start")
while True:
    try:
        print(sock.recvuntil("Here:: "))
    except:
        break
    midi = sock.recvline().decode("base64")
    print(midi)
    open("temp.mid", "wb").write(midi)
    mid = mido.MidiFile("temp.mid")
    answer = ""
    for track in mid.tracks:
        for msg in track:
            if msg.time > 0:
                answer += chr(msg.note)
    print(answer)
    try:
        answer = base85decode(answer[2:answer.index("~>")])
    except:
        answer = ascii85decode(answer[2:answer.index("~>")])
    print(answer)
    sock.send(answer)

sock.interactive()
