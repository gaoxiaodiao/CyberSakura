from pwn import *
context.log_level ="critical"
def tryFlagPart(flag_part):
    r = remote('34.89.159.150',32653)
    r.recvuntil(": ")
    r.sendline(flag_part)
    r.recvuntil(flag_part +"\r\n")
    resp = r.recvuntil("\r\n")[:-2]
    r.close()
    return resp.decode().startswith('0'*2* len(flag_part))
alphabet ="0123456789abcdef}"
flag ="ctf{"
while flag[-1] !="}":
    for c in alphabet:
        if tryFlagPart(flag + c):
            flag += c
            print(flag)
            break