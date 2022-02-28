#include <stdio.h>
#include <stdlib.h>

int bet = 1;

int main()
{
  int i, num, random, money = 0;
  char name[0x10];
  unsigned int seed = (time() * 0xCCCCCCCD) >> 3;
  printf("What is your name?");
  read(stdin, name, 0x10);
  printf("Welcome ");
  printf(name);
  putchar('\n');
  seed += bet;
  srand(seed);

  for(i = 1; i < 100; i++) {
    random = rand();
    printf("[%d/100] Guess my number: ", i);
    scanf("%d", &num);
    if (num != random) {
      puts("Sorry! It was not my number");
      exit(0);
    }
    puts("Correct!");
    money += bet;
  }

  if (money > 100) {
    puts("Cool! Here's another prize");
    char flag[0x20];
    FILE *fd = fopen("flag.txt", "r");
    fread(fd, 0x1e, 1, flag);
    fclose(fd);
    printf("%s", flag);
  }
}
