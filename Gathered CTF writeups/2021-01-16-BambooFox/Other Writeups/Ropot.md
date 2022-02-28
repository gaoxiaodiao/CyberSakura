## Ropot
> **Category:** Pwn
> **Description:** nc chall.ctf.bamboofox.tw 10100
>
> Robot? Ropot?
>
> Create an AI for your ropot.
>
> Note: The real flag is in the /home/ropot/flag, so you need to open the flag file and read it by yourself.
> **Pad Link:** http://34.87.94.220/pad/pwn-ropot
> **Flag:**
---

## References

seccomp-tools dump:

```
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x01 0x00 0xc000003e  if (A == ARCH_X86_64) goto 0003
 0002: 0x06 0x00 0x00 0x00000000  return KILL
 0003: 0x20 0x00 0x00 0x00000000  A = sys_number
 0004: 0x15 0x00 0x01 0x00000000  if (A != read) goto 0006
 0005: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0006: 0x15 0x00 0x01 0x00000001  if (A != write) goto 0008
 0007: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0008: 0x15 0x00 0x01 0x0000000f  if (A != rt_sigreturn) goto 0010
 0009: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0010: 0x15 0x00 0x01 0x0000003c  if (A != exit) goto 0012
 0011: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0012: 0x15 0x00 0x01 0x000000e7  if (A != exit_group) goto 0014
 0013: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0014: 0x06 0x00 0x00 0x00000000  return KILL
```

`read`, `write`, `rt_sigreturn`, `exit`, `exit_group` allowed

Plan:
1. Find `pipefd` so that can read from it
2. Find `dprintf` so that can write to parent
3. Play the game
4. Exfil flag

## Bugs


## Exploit Ideas


## Scripts

