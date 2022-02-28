## Flag Checker
> **Category:** Reverse
> **Description:** 
> **Pad Link:** http://34.87.94.220/pad/reverse-flag-checker
> **Flag:** flag{v3ry_v3r1log_f14g_ch3ck3r!}
---

We are given three files, written in what seems like `SystemVerilog`. The file `t_chall.v` seems to yield the main function, and it calls the function in `chall.v` which calls the function in `magic.v`.

Inspecting `t_chall.v`, it appears that it takes each element in `flag` array and passes it into `chall` then compares with `target`.

## References


## Bugs


## Exploit Ideas
```verilog=system
wire[7:0] target[32:0], flag[32:0];
```

This line suggests that target and flag consists of 32 8-bit integers, and since `chall` is always the same, we can bruteforce all possible inputs that leads to the `target`.

Eventually, you'll realise that multiple inputs can have the same output, so we need to store these in an array and iterate through the combinations to get the flag.


## Scripts
```python
def magic(inp, val):
    if val%4 == 0: return (inp >> 3) | (inp << 5) #right cycle 3 times
    if val%4 == 1: return (inp << 2) | (inp >> 6) #left cycle 2 times
    if val%4 == 2: return inp + 55
    else: return inp^55

def chall(inp):
    val0 = inp & 0b11
    val1 = (inp & 0b1100) >> 2
    val2 = (inp & 0b110000) >> 4
    val3 = (inp & 0b11000000) >> 6
    res0 = magic(inp, val0)&255
    res1 = magic(res0, val1)&255
    res2 = magic(res1, val2)&255
    res3 = magic(res2, val3)&255
    return res3

target = [182,199,159,225,210,6,246,8,172,245,6,246,8,245,199,154,225,245,182,245,165,225,245,7,237,246,7,43,246,8,248,215]
d = {}
for i in range(33, 126):
    temp = chall(i)
    if temp not in d: d[temp] = []
    d[temp].append(chr(i))

def print_flags(curr, index):
    if index == len(target):
        print(curr)
    else:
        for c in d[target[index]]:
            print_flags(curr + c, index + 1)

print_flags('', 0)
```
