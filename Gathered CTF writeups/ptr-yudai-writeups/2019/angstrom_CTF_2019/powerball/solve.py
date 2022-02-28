from ptrlib import *

sock = Socket("54.159.113.26", 19001)

with open('public.txt') as f:
    n = int(f.readline()[3:])
    e = int(f.readline()[3:])

balls = []

sock.recvuntil("x: [")
result = sock.recvuntil("]").rstrip(b"]")
xs = []
for elm in result.split(b','):
    xs.append(int(elm))

v = max(xs)
sock.recvuntil("v: ")
sock.sendline(str(v))

sock.recvuntil("m: [")
result = sock.recvuntil("]").rstrip(b"]")
ms = []
for elm in result.split(b','):
    ms.append(int(elm))

max_x = max(xs)
for m, x in zip(ms, xs):
    for i in range(4096):
        if (max_x - x) == pow(m - i, e, n):
            print('[!]find bull : {}'.format(i))
            balls.append(i)

print(balls)
for i in range(1, 7):
    sock.recvuntil("Ball {}".format(i))
    sock.sendline(str(balls[i - 1]))

sock.interactive()
