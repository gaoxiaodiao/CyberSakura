#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

void handler(int sig)
{
  if (sig == SIGALRM) {
    puts("\nTimeout");
    exit(1);
  }
}

void setup(void)
{
  setvbuf(stdout, NULL, _IONBF, 0);
  signal(SIGALRM, handler);
  alarm(60);
}

int main(void)
{
  char i, n;
  double arr[0x20];
  double avr = 0.0;
  setup();

  puts("===== Average Calculator Online =====");
  printf("Number of values: ");
  scanf("%hhd", &n);
  for(i = 0; i < n; i++) {
    scanf("%lf", &arr[i]);
  }
  for(i = 0; i < n; i++) {
    avr += arr[i];
  }
  avr /= n;
  printf("Result: %f\n", avr);
  return 0;
}
