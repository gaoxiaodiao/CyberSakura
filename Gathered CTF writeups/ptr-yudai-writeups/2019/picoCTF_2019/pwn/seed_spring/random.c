#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main()
{
  int i;
  srand(time(NULL));
  for (i = 0; i < 30; i++) {
    printf("%d\n", rand() & 0xf);
  }
  return 0;
}
