#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
  srand(time(NULL) + 't' + 't');
  printf("%d", rand());
  return 0;
}
