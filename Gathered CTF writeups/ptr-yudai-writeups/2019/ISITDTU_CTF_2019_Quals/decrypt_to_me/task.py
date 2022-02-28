import binascii
def generate_prg_bit(n):
    state = n
    while True:
        last_bit = state & 1
        yield last_bit
        middle_bit = state >> len(bin(n)[2:])//2 & 1
        state = (state >> 1) | ((last_bit ^ middle_bit) << (len(bin(n)[2:])-1))
flag = '###########'
enc = "OKQI+f9R+tHEJJGcfko7Ahy2AuL9c8hgtYT2k9Ig0QyXUvsj1B9VIGUZVPAP2EVD8VmJBZbF9e17"
flag_bin_text = bin(int(binascii.hexlify(flag), 16))[2:]
prg =  generate_prg_bit(len(flag_bin_text))
ctext = []
flag_bits = [int(i) for i in flag_bin_text]
for i in range(len(flag_bits)):
    ctext.append(flag_bits[i] ^ next(prg))  
ciphertext = '0b' + ''.join(map(str, ctext))
n = int(ciphertext, 2)
print binascii.unhexlify('%x' % n).encode('base64')

