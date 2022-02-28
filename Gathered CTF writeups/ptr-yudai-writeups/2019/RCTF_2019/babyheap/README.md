# [pwn ???pts] babyheap - RCTF 2019
64ビットで全部有効です。
```
$ checksec -f babyheap
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   96 Symbols     Yes	0		4	babyheap
```

- seccompでexecve等が禁止されている
- malloptでfastbinが無効化されている
- addするとcallocで領域が確保される
- noteは10個まででそれぞれサイズ0x1000まで

次のように構造体でサイズも記録されています。
```
typedef struct {
    char* ptr;
    int size;
} note_t;
```
editではこのサイズまでしか変更できないです。
deleteではfreeした後にちゃんとptrにNULLを代入しており、一見してUAFはありません。
editした後に `ptr[i][readBytes] = 0` しているのでoff-by-null脆弱性があります。
とりあえずchunk overlapしてlibc leakとfastbin attackをしましょう。
```python

```

# 感想
