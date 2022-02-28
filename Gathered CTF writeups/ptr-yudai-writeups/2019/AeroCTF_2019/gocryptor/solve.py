def decrypt(data, key):
    result = b''
    for i in range(len(data)):
        result += bytes([data[i] ^ key[i % len(key)]])
    return result

with open("example_drawing.enc", "rb") as f:
    data = f.read()

key = b"\x72\xb5\x39\xc7\xa3\xe2\x39\x15\x37\x44\x5b\x2b\x87\x6e\x23\x20"
result = decrypt(data, key)

with open("sample", "wb") as f:
    f.write(result)
