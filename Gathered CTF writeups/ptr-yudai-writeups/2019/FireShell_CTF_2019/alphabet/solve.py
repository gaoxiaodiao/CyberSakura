import hashlib
import string

f = open("submit_the_flag_that_is_here.txt")
buf = f.read()
hashlist = buf.split(" ")
flag = ""
for h in hashlist:
    for c in string.printable:
        if hashlib.sha256(c).hexdigest() == h:
            flag += c
            break
        elif hashlib.md5(c).hexdigest() == h:
            flag += c
            break
    else:
        break

print(flag)
open("flag", "wb").write(flag)
