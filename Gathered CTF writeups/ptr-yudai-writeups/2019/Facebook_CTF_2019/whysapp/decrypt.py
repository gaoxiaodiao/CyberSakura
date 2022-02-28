from Crypto.Cipher import AES
import base64
import sys

# math
#cipher = "iwGfhu+ibZJE7zyqY/I2w6KwA3MjvmDjnEEwjlJG5Wg="

# ping
#cipher = "EGL+3TD6pfPmF9tdXXaclcvPJHM6kkYqcPQVqMuTv5w="

# msg
#cipher = "IvhfXZYSXnHqnOAxyXR27oAKiSpSVkXj7BaUkJLpHIka2AirTj2MEDuNrN8jPGkY+kzu436Zcd8xp1ZkPNH1Ga9ZiH4MvF4Vg7zxFdi41P4+w7mLMsxf/CaTF8KzQ/My"
#cipher = "Dbj9p4oOLib1PRUq+AM8HYy2MiMubu7i/FeRF/l5oQYbc7m/7ffoQ01d4AtVSL/L"
cipher = sys.argv[1]

key = "yeetyeetyeetyeet"
crypto = AES.new(key, AES.MODE_ECB)
plain = crypto.decrypt(base64.b64decode(cipher)).rstrip(b"\x00")
print(plain)
