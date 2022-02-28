import os
import subprocess
import pickle
import base64
import pickletools

# Exploit that we want the target to unpickle
class Test(object):
    pass
    #def __init__(self):
    #    self.hoge = {"42": "HoggieTalooo"}
    
    #def __reduce__(self):
    #    return (subprocess.Popen, (('/bin/ls',),))


def serialize_exploit():
    shellcode = pickle.dumps(Test())
    return shellcode


def insecure_deserialize(exploit_code):
    pickle.loads(exploit_code)


if __name__ == '__main__':
    shellcode = serialize_exploit()
    print(shellcode)
    #print(base64.b64encode(shellcode))
    insecure_deserialize(shellcode)
