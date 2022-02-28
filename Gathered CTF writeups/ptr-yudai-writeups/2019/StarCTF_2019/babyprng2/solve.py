from ptrlib import *
from hashlib import sha256

table = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPRSTUVWXYZ0123456789"

# PoW
sock = Socket("34.92.185.118", 10003)
sock.recvuntil("+")
tmp = sock.recvuntil(")")[:-1]
print("[+] tmp : {}".format(tmp.decode()))
sock.recvuntil(" == ")
ans = sock.recvline().strip()
print("[+] ans : {}".format(ans.decode()))

# attack
for attack in brute_force_attack(4, table_len = len(table)):
    xxxx = brute_force_pattern(attack, table=table)
    h = sha256(xxxx.encode() + tmp).hexdigest()
    if h == ans.decode():
        print("[!] Correct : {}".format(xxxx))
        break
else:
    raise Exception("Something is wrong......")
sock.recvuntil(":")
sock.sendline(xxxx)

sock.recvuntil("(hex):")
sock.sendline("0732011411360536000112133805360035")
sock.interactive()
