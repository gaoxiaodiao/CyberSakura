import base64

cipher = base64.b64decode(
    "XUBdTFdScw5XCVRGTglJXEpMSFpOQE5AVVxJBRpLT10aYBpIVwlbCVZATl1WTBpaTkBOQFVcSQdH"
)
key = ":)"

flag = ""
for i, c in enumerate(cipher):
    flag += chr(ord(key[i % 2]) ^ ord(c))

print(flag)
