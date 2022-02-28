import subprocess
import time

table = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "

with open("output.orig", "rb") as f:
    output = f.read()

def search(flag):
    print(flag)
    if len(flag) >= 20:
        yield flag
    for c in table:
        with open("flag.txt", "w") as f:
            f.write(flag + c)
        p = subprocess.Popen(["./mystery"], stderr=subprocess.PIPE)
        p.communicate()
        with open("output", "rb") as f:
            result = f.read()
        if len(result) > 1:
            if result[:-1] == output[:len(result) - 1]:
                for x in search(flag + c):
                    yield x
        else:
            for x in search(flag + c):
                yield x

for flag in search(''):
    print("candidate: {}".format(flag))
