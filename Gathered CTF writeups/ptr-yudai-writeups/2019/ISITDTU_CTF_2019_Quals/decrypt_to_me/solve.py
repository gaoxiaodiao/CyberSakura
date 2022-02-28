import binascii

def generate_prg_bit(n):
    state = n
    while True:
        last_bit = state & 1
        yield last_bit
        middle_bit = state >> len(bin(n)[2:])//2 & 1
        state = (state >> 1) | ((last_bit ^ middle_bit) << (len(bin(n)[2:])-1))

cipher = "OKQI+f9R+tHEJJGcfko7Ahy2AuL9c8hgtYT2k9Ig0QyXUvsj1B9VIGUZVPAP2EVD8VmJBZbF9e17".decode("base64")
n = int(binascii.hexlify(cipher), 16)
cipher_bits = [int(i) for i in bin(n)[2:]]
approx_len = len(bin(n)[2:])
for l in range(approx_len, approx_len + 8):
    prg = generate_prg_bit(l)
    mtext = []
    bits = [0 for i in range(l - approx_len)] + cipher_bits
    for i in range(l):
        mtext.append(bits[i] ^ next(prg))
    flag = int(''.join(map(str, mtext)), 2)
    try:
        print(hex(flag)[2:].rstrip("L").decode("hex"))
    except:
        pass
