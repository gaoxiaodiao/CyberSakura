all:
	gcc -shared securalloc.c -o libsalloc.so -fPIC
	gcc main.c -o chall -L./ -lsalloc -pie
	strip --strip-all chall
	cp ./chall ../distfiles/
	cp ./libsalloc.so ../distfiles/

test:
	LD_LIBRARY_PATH=./ ./chall
