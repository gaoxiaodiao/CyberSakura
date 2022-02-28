import re
import requests
import time

t = int(time.time())

# t - t * t = v - 1787569 * w
w = t * t // 1784896
v = t - t * t + 1784896 * w

print(w)
x = [1 for i in range(10)]
x[0] = 0 # x0 ** 3
x[1] = 1
x[2] = v
x[3] = 1 # (x3 ** 3) * (x[9] ** 2)
x[4] = 0 # x4 ** x4
x[5] = 0 # x5 ** x5
x[6] = 0
x[7] = 0
x[8] = w # -1784896 * x[8] * x[3]
x[9] = 0
url = "http://heavensdoor-01.play.midnightsunctf.se:10488/knock/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}".format(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9])
r = requests.get(url)
print(url)
print(r.text)
l = re.findall(b"t \((\d+)\) != res \((-?\d+)\)", r.text.encode("ascii"))
t = int(l[0][0])
y = int(l[0][1])

print(y - t * t)
