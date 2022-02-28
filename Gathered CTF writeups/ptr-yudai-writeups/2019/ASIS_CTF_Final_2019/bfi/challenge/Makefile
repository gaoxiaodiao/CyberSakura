all:
	gcc -shared bf.c -o libbf.so -fPIC -O2
	gcc main.c -o chall -L./ -lbf -pie -O2
	strip --strip-all chall
	mv chall ../distfiles/
	mv libbf.so ../distfiles/

test:
	LD_LIBRARY_PATH=../distfiles/ ../distfiles/chall
