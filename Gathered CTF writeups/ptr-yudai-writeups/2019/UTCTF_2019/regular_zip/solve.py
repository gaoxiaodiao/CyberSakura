import exrex
import zipfile
import shutil

while True:
    print("[+] New File")
    with open("data/hint.txt", "r") as f:
        reg = f.read().rstrip()
        print("[+] Regex: " + reg)
    if reg == '':
        break
    shutil.copyfile("data/archive.zip", "data/temp.zip")
    with zipfile.ZipFile('data/temp.zip') as z:
        passlist = exrex.generate(reg)
        for password in passlist:
            try:
                z.extractall('data/', pwd=password)
                print("[+] Found password: " + password)
                break
            except:
                pass
