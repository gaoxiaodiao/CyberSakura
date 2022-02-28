#include <stdlib.h>
#include <stdio.h>

int main(int argc, char** argv)
{
  int i;
  if (argc < 3) {
    return 0;
  }
  srand(atoi(argv[1]));
  for(i = 0; i < atoi(argv[2]) - 1; i++) {
    rand();
  }
  printf("%d", rand());
  return 0;
}
