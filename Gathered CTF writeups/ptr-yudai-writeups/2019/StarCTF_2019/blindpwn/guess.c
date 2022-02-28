#include <stdio.h>

void blindpwn(void)
{
  char buf[40];
  read(0, buf, 0x1000);
}

int main(void)
{
  puts("Welcome to this blind pwn!");
  blindpwn();
  puts("Goodbye!");
  return 0;
}
