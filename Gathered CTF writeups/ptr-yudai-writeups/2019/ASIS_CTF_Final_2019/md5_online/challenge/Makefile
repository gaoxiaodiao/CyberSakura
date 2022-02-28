all:
	gcc -Wl,-z,now,-z,relro main.c -o chall -fstack-protector -pie -lcrypto -m32
	cp ./chall ../distfiles/
	strip --strip-all ./chall
