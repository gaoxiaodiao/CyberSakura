#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char **argv)
{
  srand(time(NULL));
  if (argc < 2) return 0;
  int x = atoi(argv[1]);
  int i;
  for(i = 0; i < x;) {
    rand();
    if (rand() % 3 == 0) {
      if (rand() % 5 == 0) {
	printf("free\n");
	rand();
      } else {
	rand();
	printf("malloc\n");
      }
      i++;
    } else {
      printf("nothing\n");
    }
  }
  return 0;
}
