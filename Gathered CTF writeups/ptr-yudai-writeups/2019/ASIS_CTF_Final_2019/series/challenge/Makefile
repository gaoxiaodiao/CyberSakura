all:
	gcc -Wl,-z,now,-z,relro main.c -o ../distfiles/chall -pie -fstack-protector -O0
	strip --strip-all ../distfiles/chall
