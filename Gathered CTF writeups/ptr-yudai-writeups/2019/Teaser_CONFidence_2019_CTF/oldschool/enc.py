mem = [0 for i in range(18 * 9)]

si = 0x50
for i in range(9):
   dl = int(input()[0:2], 16)
   for j in range(4):
      if dl & 1 == 0 and si != 0 and si % 0x12 != 0:
         si -= 1
      elif dl & 1 == 1 and si % 0x12 != 0x10:
         si += 1
      if dl & 2 == 0 and si > 0x11:
         si -= 0x12
      elif dl & 2 == 2 and si < 0x8f:
         si += 0x12
      dl >>= 2
      mem[si] += 1

di = si # di = 33
si = 0
label = " p4{krule_ctf}"
for i in range(0xa1):
   if mem[si] > 0x0D:
       bl = 0x5e
   else:
       bl = ord(label[mem[si]])
   mem[si] = bl
   si += 1

mem[di] = 0x45
mem[0x50] = 0x53

si = 0
for i in range(8):
   si += 0x11
   mem[si] = 0x0a
   si += 1
si += 0x11
mem[si] = 0x24
print(mem)
print(''.join(list(map(chr, mem))))
si = 0
