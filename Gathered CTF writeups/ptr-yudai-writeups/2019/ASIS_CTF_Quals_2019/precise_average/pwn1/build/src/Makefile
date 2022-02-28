all:
	gcc -Wl,-z,now,-z,relro main.c -o chall -fstack-protector-strong -fno-pie
	strip --strip-all chall
