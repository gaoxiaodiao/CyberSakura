_start:
  lea rdi, [rbp+0x10]
  mov rax, 22
  syscall                       ; pipe(&p)

  mov r9, 1
  mov r8, 0x100
  xor r10, r10
  xor edx, edx
  mov edx, [rbp+0x14]
  xor rsi, rsi
  xor edi, edi
  mov edi, [rbp-0x1014]
  mov rax, 275
  syscall                       ; splice(fd, NULL, p[1], NULL, 0x100, 1)

  mov r9, 1
  mov r8, 0x100
  xor r10, r10
  mov rdx, 1
  xor rsi, rsi
  xor edi, edi
  mov edi, [rbp+0x10]
  mov rax, 275
  syscall                       ; splice(p[0], NULL, 1, NULL, 0x100, 1)
