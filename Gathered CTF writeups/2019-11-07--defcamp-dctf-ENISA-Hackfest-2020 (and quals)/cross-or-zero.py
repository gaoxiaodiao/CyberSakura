import base64

#Encode text and key
enc64 = "dHNkdktTAVUHAABUA1VWVgIHBAlSBAFTBAMFUwECAgcAAAFWAFUFCFMACFFUAwQAVgBSBwQJBVZTAFYGCQYHVQABB1IJTQ=="
key = 0x30

flag = ''
#decode the base64
dec64 = base64.b64decode(enc64).hex()
print("Decoded text in hex: " + dec64  + "\n")

# XOR the decoded text with the key
for i in range(0, len(dec64), 2):
    x = int(dec64[i:i+2],16)
    flag = flag + chr(x ^ key)

print("Flag: " + flag)