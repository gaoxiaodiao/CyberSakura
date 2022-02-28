help:
	@echo "usage: make <command|input>"
	@echo
	@echo "command:"
	@echo "  help     Shows this text."
	@echo "  source   Shows the Makefile's source."
	@echo
	@echo "input:"
	@echo "           Correct input reveals the flag."

source:
	@cat Makefile

%:
#	@echo $(call o,$(d))
#	@echo $(call o,$(x))
#	@echo $(call b,$(l),$(q))
#	@echo $(call e,yyyyy)
#	$(s)
	$(flag)
#	sleep 1

b=$(if $(subst y,,$(1)),$(call b,$(patsubst x%,%,$(1)),$(2)y),$(if $(subst x,,$(1)),$(call b,$(patsubst %y,%,$(1)),x$(2)),$(call w,$(2))))
c=$(call p,$(l),$(q))
d=$(call r,$(l))
e=$(if $(subst y,,$(1)),$(words $(subst x,x ,$(1))),$(if $(subst x,,$(1)),-$(words $(subst y,y ,$(1))),0))
g=$(call j,$(call j,xxxxxxxxxxxxxxx))
h=$(call k,$(g),$(z))
i=x$(1)
j=$(subst x,xxxxxxx,$(1))

a = $(call k,$(call m,$(1)),$(h))
l = $(call n,$(firstword $(subst -, , $@)))
o = $(if $(and $(findstring x,$(1)),$(findstring y,$(1))),$(call o,$(patsubst x%y,%,$(1))),$(1))
k = $(if $(subst y,,$(1)),$(call k,$(patsubst x%,%,$(1)),x$(2)),$(if $(subst x,,$(1)),$(call k,$(patsubst %y,%,$(1)),$(2)y),$(2)))

m=$(call p,$(1),$(1))
n=$(patsubst %,%,$(subst x ,x, $(filter x,$(subst x,x ,$(1)))))$(patsubst %,%,$(subst y ,y, $(filter y,$(subst y,y ,$(1)))))
p=$(if $(subst y,,$(1)),$(call k,$(2),$(call p,$(call o,$(call u,$(1))),$(2))),$(if $(subst x,,$(1)),$(call b,$(2),$(call p,$(call o,$(call i,$(1))),$(2))),))
q=$(call n,$(lastword $(subst -, , $@)))
r=$(call b,$(call a,$(1)),$(call y,$(1)))
s=@echo flag-`echo $(call v,$(c)) $(call o,$(c)) | md5sum`
t=$(call k,$(z),xxxxxxxxxx)
u=$(1)y
v=$(call e,$(call o,$(1)))
w=$(if $(subst z,,$(subst y,,$(1))),$(call w,$(patsubst x%,%z,$(1))),$(if $(subst z,,$(subst x,,$(1))),$(subst z,y,$(subst y,x,$(1))),$(subst z,y,$(1))))
x=$(call r,$(q))
y=$(call p,$(1),$(t))
z=$(call b,$(call j,$(call j,x)),xx)

flag = $(if $(or $(call o,$(d)),$(call o,$(x))),@echo nope1,$(if $(call o,$(call b,$(l),$(q))), $(s), @echo nope))
