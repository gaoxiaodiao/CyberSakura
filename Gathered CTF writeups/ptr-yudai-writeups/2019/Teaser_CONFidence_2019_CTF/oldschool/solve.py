from pprint import pprint

with open("flag.txt", "rb") as f:
   tmp = f.read()

mem = ""
i = 0
for x in range(0xa2):
   if tmp[i] == ord('\r'):
       i += 2
   mem += chr(tmp[i])
   i += 2
mem = mem[1:]
di = mem.index('E')
print(di)

label = b" p4{krule_ctf}"
arr = []
s = 0
for line in mem.split("\n"):
    w = list(line)
    for i in range(len(w)):
        if ord(w[i]) not in label:
            w[i] = -1
        else:
            w[i] = label.index(ord(w[i]))
    s += sum(w)
    arr.append(w)
print(arr)
print(s)
