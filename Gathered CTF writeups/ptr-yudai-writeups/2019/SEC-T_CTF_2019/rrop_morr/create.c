#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
  if (argc < 2) {
    printf("%s seed\n", argv[0]);
    return 1;
  }
  int i;
  int seed = atoi(argv[1]);
  FILE *fp = fopen("gadgets", "wb");
  srand(seed);
  for(i = 0; i < 0x800000; i++) {
    unsigned int rnd = rand();
    fwrite(&rnd, 4, 1, fp);
  }
  fclose(fp);
}
