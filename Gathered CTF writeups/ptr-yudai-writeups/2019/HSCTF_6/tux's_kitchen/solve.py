from ptrlib import *

candidate = [
    [chr(j) for j in range(1, 0x100)]
    for i in range(71)
]

while True:
    sock = Socket("crypto.hsctf.com", 8112)
    sock.recvuntil("[")
    l = list(map(lambda x: int(x.rstrip(b"L")), sock.recv().rstrip().rstrip(b"]").split(b", ")))
    # original treasure
    index = 0
    for c in l:
        pre = list(candidate[index])
        candidate[index] = []
        for i in range(ord(" "), ord("~")):
            x = c ^ 29486316
            if x % i == 0 and chr(i) in pre:
                candidate[index].append(chr(i))
        index += 1
    for w in candidate:
        if len(w) != 1:
            break
    else:
        print(candidate)
        print(''.join(candidate))
        break
    print(candidate)
    print("Trying...")

# hsctf{thiii111iiiss_isssss_yo0ur_b1rthd4y_s0ng_it_isnt_very_long_6621}
