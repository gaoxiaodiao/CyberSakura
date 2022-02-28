from ptrlib import *

sock = Socket("54.159.113.26", 19001)

balls = []

# receive x
sock.recvuntil("x: [")
result = sock.recvuntil("]").rstrip(b"]")
x = []
for elm in result.split(b','):
    x.append(int(elm))

# send v
e = 65537
k = -4096
v = x[0] + k**e
sock.recvuntil("v: ")
sock.sendline(str(v))
exit()
sock.recvuntil("m: [")
result = sock.recvuntil("]").rstrip(b"]")
m = []
for elm in result.split(b','):
    m.append(int(elm) - k)

n = 0
candidate_n = set()
for ball in range(4096):
    candidate_n.add(m[0] + (4096 - ball))
for i in range(1, 6):
    possible_n = set()
    for ball in range(4096):
        test_n = m[i] + (4096 - ball)
        if test_n in candidate_n:
            possible_n.add(test_n)
    candidate_n = possible_n
print(candidate_n)
