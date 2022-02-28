  A = arch
  A == ARCH_X86_64 ? next : dead
  A = sys_number
  A >= 0x40000000 ? dead : next
  A == execve ? ok : next
  A == execveat ? ok : next
  A == openat ? ok : next
  A == clone ? ok : next
  A == fork ? ok : next
  A == ptrace ? ok : next
  A == socket ? ok : next
  A == bind ? ok : next
  A == open ? next : ok
  return ERRNO(0)
ok:
  return ALLOW
dead:
  return KILL
