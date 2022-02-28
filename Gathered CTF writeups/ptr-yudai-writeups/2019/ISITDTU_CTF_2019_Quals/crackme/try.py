from z3 import *


flag = [BitVec("x%d" % i, 64) for i in range(0x19)]
solver = Solver()


for f in flag:
   solver.add(0x20 <= f, f <= 0x7F)
evensum = 0
evenxor = 0
oddxor = 0
oddsum = 0
allxor = 0
for i, f in enumerate(flag):
   if i % 2 == 0:
       evensum += f
       evenxor = evenxor ^ f
   else:
       oddsum += f
       oddxor = oddxor ^ f
   allxor = allxor ^ f
solver.add(evenxor == 0x10)
solver.add(oddxor == 9)
solver.add(
   (evensum * 3 + oddsum) % 10 == 9,
   (evensum + oddsum) % 10 == 3,
   (oddsum % 10) + 3 == evensum % 10,
)
solver.add(allxor == 0x19)
#
# A = flag[0]
# i = 1
# while i < (0x19 + (0x19 >> 0x1F)) >> 1:
#    A = A ^ flag[i]
#    i += 1
#
# solver.add(A == 0x3F)
solver.add(flag[0] == ord("A"))
solver.add(flag[1] == ord("u"))
solver.add(flag[2] == ord("t"))
solver.add(flag[10] == ord("T"))
solver.add(flag[12] == ord("3"))
solver.add(flag[23] == ord("r"))
solver.add(flag[9] == ord("_"))
solver.add(flag[17] == ord("_"))
solver.add(flag[24] == ord("s"))

r = 0x17
for i in range(len(flag)):
   r = (flag[i] << i) + (r << 3) - r
r = r >> 4
solver.add(r == 0x22233025)

if solver.check() != sat:
   print("unsat")
   exit()

model = solver.model()
flag_str = ""
for f in flag:
   flag_str += chr(model[f].as_long())
print(flag_str)
