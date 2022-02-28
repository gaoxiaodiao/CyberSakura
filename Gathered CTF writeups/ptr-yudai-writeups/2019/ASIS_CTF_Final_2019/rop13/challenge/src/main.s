extern read
extern write
extern exit
extern signal
extern alarm

section .text
global _start
_start:
  call get_args
  call setup
  call main
  call exit
  ret

get_args:
  mov rdi, [rsp + 0x08]
  mov rsi, [rsp + 0x10]
  ret

setup:
  mov rsi, exit
  mov rdi, 0x0E
  call signal
  mov rdi, 10
  call alarm
  ret

rot13:
  push rbp
  mov rbp, rsp
  push rdx

  mov rsi, rdi
  cld

.loop:
  lodsb
.is_upper
  cmp al, 0x40
  jbe .is_lower
  cmp al, 0x5a
  jg .is_lower
  add al, 13
  cmp al, 0x5a
  jbe .done
  sub al, 26
.is_lower
  cmp al, 0x60
  jbe .done
  cmp al, 0x7a
  jg .done
  add al, 13
  cmp al, 0x7a
  jbe .done
  sub al, 26
.done
  test al, al
  stosb
  jnz .loop

  pop rdx
  pop rbp
  ret

main:
  push rbp
  mov rbp, rsp
  sub rsp, 0x40

  mov rdx, 0x100
  lea rsi, [rbp-0x40]
  mov rdi, 0
  call read

  lea rdi, [rbp-0x40]
  mov rdx, rax
  call rot13

  lea rsi, [rbp-0x40]
  mov rdi, 1
  call write

  leave
  ret

