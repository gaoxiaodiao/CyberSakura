all:
	nasm -f elf64 -o chall.o main.s
	ld -dynamic-linker /lib64/ld-linux-x86-64.so.2 -o rot13 -lc chall.o -z noexecstack
	strip --strip-all rot13
	mv rot13 ../server/
