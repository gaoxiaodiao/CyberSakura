from Crypto.Cipher import AES

q = 412220184797
A = 10717230661382162362098424417014722231813
B = 22043581253918959176184702399480186312
g = (56797798272, 349018778637)
pubkey = (61801292647, 228288385004)
pubkey2 = (196393473219, 35161195210)
share = (130222573707, 242246159397)

with open("captured.enc", "rb") as f:
    enc = f.read()

key = b'130222573707242246159397'
iv = enc[:16]
cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted = cipher.decrypt(enc[16:])

with open("file", "wb") as f:
    f.write(decrypted)
