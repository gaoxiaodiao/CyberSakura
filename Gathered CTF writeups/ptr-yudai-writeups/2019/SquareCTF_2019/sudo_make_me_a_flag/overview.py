import re
import hashlib
from ptrlib import *

#b=$(if $(subst y,,$(1)),$(call b,$(patsubst x%,%,$(1)),$(2)y),$(if $(subst x,,$(1)),$(call b,$(patsubst %y,%,$(1)),x$(2)),$(call w,$(2))))
"""
def b(v1, v2):
    if 'x' in v1:
        return b(re.sub(r'\Ax(.*)\Z', r'\1', v1), v2+'y')
    elif 'y' in v1:
        return b(re.sub(r'\A(.*)y\Z', r'\1', v1), 'x'+v2)
    else:
        return w(v2)
"""
def b(v1, v2):
    return 'x' * (v1.count('x') + v2.count('y')) + 'y' * (v1.count('y') + v2.count('x'))

#c=$(call p,$(l),$(q))
def c():
    return p(l(), q())

#d=$(call r,$(l))
def d():
    return r(l())

#e=$(if $(subst y,,$(1)),$(words $(subst x,x ,$(1))),$(if $(subst x,,$(1)),-$(words $(subst y,y ,$(1))),0))
def e(v1):
    if 'x' in v1:
        if 'y' in v1:
            return v1.count('x') + 1
        else:
            return v1.count('x')
    elif 'y' in v1:
        if 'x' in v1:
            return -(v1.count('x') + 1)
        else:
            return -v1.count('x')
    else:
        return 0

#g=$(call j,$(call j,xxxxxxxxxxxxxxx))
def g():
    return j(j('xxxxxxxxxxxxxxx'))

#h=$(call k,$(g),$(z))
def h():
    return k(g(), z())

#i=x$(1)
def i(v1):
    return 'x' + v1

#j=$(subst x,xxxxxxx,$(1))
def j(v1):
    return v1.replace('x', 'xxxxxxx')

#a = $(call k,$(call m,$(1)),$(h))
def a(v1):
    return k(m(v1), h())

#l = $(call n,$(firstword $(subst -, , $@)))
def l():
    return n(ARG.split('-')[0])

#o = $(if $(and $(findstring x,$(1)),$(findstring y,$(1))),$(call o,$(patsubst x%y,%,$(1))),$(1))
"""
def o(v1):
    if 'x' in v1 and 'y' in v1:
        return o(v1[1:-1])
    else:
        return v1
"""
def o(v1):
    if v1.count('x') == v1.count('y'):
        return ''
    elif v1.count('x') > v1.count('y'):
        return 'x' * (v1.count('x') - v1.count('y'))
    else:
        return 'y' * (v1.count('y') - v1.count('x'))
#k = $(if $(subst y,,$(1)),$(call k,$(patsubst x%,%,$(1)),x$(2)),$(if $(subst x,,$(1)),$(call k,$(patsubst %y,%,$(1)),$(2)y),$(2)))
"""
def k(v1, v2):
    if 'x' in v1:
        return k(re.sub(r'\Ax(.*)\Z', r'\1', v1), 'x'+v2)
    elif 'y' in v1:
        return k(re.sub(r'\A(.*)y\Z', r'\1', v1), v2+'y')
    else:
        return v2
"""
def k(v1, v2):
    return 'x' * (v1.count('x') + v2.count('x')) + 'y' * (v1.count('y') + v2.count('y'))

#m=$(call p,$(1),$(1))
def m(v1):
    return p(v1, v1)

#n=$(patsubst %,%,$(subst x ,x, $(filter x,$(subst x,x ,$(1)))))$(patsubst %,%,$(subst y ,y, $(filter y,$(subst y,y ,$(1)))))
#n=$(subst x ,x, $(filter x,$(subst x,x ,$(1)))))$(patsubst %,%,$(subst y ,y, $(filter y,$(subst y,y ,$(1))))
def n(v1):
    # xyxxyy --> x yx x yy  |
    # xyxxyy --> xy xxy y   +--> xxy
    return ''.join(list(filter(lambda x: x == 'x', v1.replace('x', 'x ').split()))) +\
        ''.join(list(filter(lambda y: y == 'y', v1.replace('y', 'y ').split())))

#p=$(if $(subst y,,$(1)),$(call k,$(2),$(call p,$(call o,$(call u,$(1))),$(2))),$(if $(subst x,,$(1)),$(call b,$(2),$(call p,$(call o,$(call i,$(1))),$(2))),))
"""
def p(v1, v2):
    if 'x' in v1:
        return k(v2, p(o(u(v1)), v2))
    elif 'y' in v1:
        return b(v2, p(o(i(v1)), v2))
    else:
        return ''
"""
def p(v1, v2):
    xc = v1.count('x')
    yc = v1.count('y')
    if xc > yc:
        return ''.join(sorted(v2 * (xc - yc)))
    elif xc < yc:
        base = 'x' + 'x' * (len(v1) // 2) + 'y' * ((len(v1) - 1) // 2)
        t = ''
        for c in v2:
            if c == 'x':
                t += base
            else:
                t += base.replace('x', 'w').replace('y', 'x').replace('w', 'y')
        return ''.join(sorted(t))
    else:
        return v1
#"""

#q=$(call n,$(lastword $(subst -, , $@)))
def q():
    return n(ARG.split('-')[-1])

#r=$(call b,$(call a,$(1)),$(call y,$(1)))
def r(v1):
    return b(a(v1), y(v1))

#s=@echo flag-`echo $(call v,$(c)) $(call o,$(c)) | md5sum`
def s():
    print("flag-{}".format(hashlib.md5(v(c()) + " " + o(c) + "\n").hexdigest()))

#t=$(call k,$(z),xxxxxxxxxx)
def t():
    return k(z(), 'xxxxxxxxxx')

#u=$(1)y
def u(v1):
    return v1 + 'y'

#v=$(call e,$(call o,$(1)))
def v(v1):
    return e(o(v1))

#w=$(if $(subst z,,$(subst y,,$(1))),
#    $(call w,$(patsubst x%,%z,$(1))),
#   $(if $(subst z,,$(subst x,,$(1))),
#     $(subst z,y,$(subst y,x,$(1))),
#    $(subst z,y,$(1))))
def w(v1):
    if 'x' in v1:
        return w(re.sub(r'\Ax(.*)\Z', r'\1', v1) + 'z')
    elif 'y' in v1:
        return v1.replace('y', 'x').replace('z', 'y')
    else:
        return v1.replace('z', 'y')

#x=$(call r,$(q))
def x():
    return r(q())

#y=$(call p,$(1),$(t))
def y(v1):
    return p(v1, t())

#z=$(call b,$(call j,$(call j,x)),xx)
def z():
    return b(j(j('x')), 'xx')

#flag = $(if $(or $(call o,$(d)),$(call o,$(x))),@echo nope1,$(if $(call o,$(call b,$(l),$(q))), $(s), @echo nope))
def flag():
    if o(d()) or o(x()):
        print("Nope 1")
    else:
        if o(b(l, q)):
            s()
        else:
            print("Nope 2")

# Solution 1
_l = "x" * 23
_q = "x" + "y" * 336
# Solution 2
_l = "x" * 23
_q = "x" + "y" * 727
# Solution 3 (worked)
_l = "x" * 23
_q = "y" + "x"*10 + "y"*2 + "x" * 28

ARG = _l + "-" + _q
dd = d()
xx = x()
print("o(d()) = '{}'".format(o(d())))
print("o(x()) = '{}'".format(o(x())))
print("o(b(l,q)) = '{}'".format(o(b(_l, _q))))

c = p(_l, _q)
output = "{} {}\n".format(v(c), o(c))
output = "flag-{}".format(hashlib.md5(str2bytes(output)).hexdigest())
print(output)
