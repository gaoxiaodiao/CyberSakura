## Better Than ASM
> **Category:** Reverse
> **Description:** 
> **Pad Link:** http://34.87.94.220/pad/reverse-better-than-asm
> **Flag:** flag{7h15_f14g_15_v3ry_v3ry_l0ng_4nd_1_h0p3_th3r3_4r3_n0_7yp0}
---
You are given a file `task.ll`, upon inspection and some useful googling, you should find that this is [LLVM](https://llvm.org/).

With some basic knowledge of assembly, and quite a bit of time, you should come to the following summary:

```
@flag = "\1DU#hJ7.8\06\16\03rUO=[bg9JmtGt`7U\0BnNjD\01\03\120\19;OVIaM\00\08,qu<g\1D;K\00}Y"
@what = "\17/'\17\1DJy\03,\11\1E&\0AexjONacA-&\01LANH'.&\12>#'Z\0FO\0B%:(&HI\0CJylL'\1EmtdC"
@secret = "B\0A|_\22\06\1Bg7#\5CF\0A)\090Q8_{Y\13\18\0DP"

@check: (translated to python)
def check(inp):
    result = 1
    for i in range(len(what)):
        result &= (inp[i] ^ inp[(i+1) % len(what)]) == what[i]
    return result

@main:
Input should be the same length as @what
label 16: calls @check, if true then branch to label 20, else label 51

label 20, 21, 27, 45:
for i in 0...len(@input)-1: @input[i] ^= @secret[i % len(@secret)]

label 51, 52, 58, 76:
for i in 0...len(@input)-1: @input[i] = @flag[i] ^ @secret[i % len(@secret)]

label 48, 79:
print("flag{%s}" % @input)
```

## References
LLVM Official Reference Manual, found [here](https://llvm.org/docs/LangRef.html).

## Bugs


## Exploit Ideas
After running the loop starting from `label 51`, the string `___7h15_15_4_f4k3_f14g_y0u_w1ll_f41l_1f_y0u_subm17_17___` is printed. Hence we can deduce that we are supposed to let `@check` return 1, and such an input is our flag.

Notice that in order to reverse `@check`, we essentially need to do a series of xor equations. We can use `z3` to solve this. Since there are multiple solutions, we need to iterate through all possible solutions until we get the flag (thanks @tygq13 for this).

Output of the script:

![](https://i.imgur.com/OX2p9z0.png)

## Scripts
```python
sflag = "\\1DU#hJ7.8\\06\\16\\03rUO=[bg9JmtGt`7U\\0BnNjD\\01\\03\\120\\19;OVIaM\\00\\08,qu<g\\1D;K\\00}Y"
swhat = "\\17/'\\17\\1DJy\\03,\\11\\1E&\\0AexjONacA-&\\01LANH'.&\\12>#'Z\\0FO\\0B%:(&HI\\0CJylL'\\1EmtdC"
ssecret = "B\\0A|_\\22\\06\\1Bg7#\\5CF\\0A)\\090Q8_{Y\\13\\18\\0DP"

flag = []
what = []
secret = []

# Change the characters and hex codes to integers
i = 0
while i in range(len(sflag)):
    if sflag[i] == '\\':
        flag.append((int(sflag[i+1:i+3], 16)))
        i += 2
    else:
        flag.append(ord(sflag[i]))
    i += 1

i = 0
while i in range(len(swhat)):
    if swhat[i] == '\\':
        what.append((int(swhat[i+1:i+3], 16)))
        i += 2
    else:
        what.append(ord(swhat[i]))
    i += 1

i = 0
while i in range(len(ssecret)):
    if ssecret[i] == '\\':
        secret.append((int(ssecret[i+1:i+3], 16)))
        i += 2
    else:
        secret.append(ord(ssecret[i]))
    i += 1

# fake flag
# for i in range(len(flag)):
#     print(chr(flag[i] ^ secret[i % len(secret)]), end='')

length = len(what)
from z3 import *
s = Solver()
vec = []
for i in range(length):
    vec.append(BitVec(str(i), 8))
for i in range(length):
    s.add(vec[i] ^ vec[(i+1)%len(what)] == what[i])
    # ensure the answer is the code of a printable character
    s.add(31 < vec[i])
    s.add(vec[i] < 126)

while s.check() == sat:
    result = str(s.model()).replace('[', '{').replace(']', '}').replace('=', ':')
    ans = eval(result)

    for i in range(length):
        print(chr(ans[i] ^ secret[i % len(secret)]),end='')
    print()
```
