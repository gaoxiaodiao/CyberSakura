#! /bin/bash

echo "Building env ..."

sudo apt-get install -y qemu gcc-arm-linux-gnueabi gdb-multiarch
sudo cp /usr/arm-linux-gnueabi/lib/ld-linux.so.3 /lib/ld-linux.so.3

echo "If you don't have pwntools, run: pip install --user pwntools"
echo "Now use helper.py to debug the challenge using pwntools"
