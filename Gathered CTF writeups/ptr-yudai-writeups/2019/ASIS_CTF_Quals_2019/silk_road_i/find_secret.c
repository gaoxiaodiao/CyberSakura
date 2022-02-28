#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

void ltoa(long val, char *ptr)
{
  int i;
  int digit = (int)log10((double)val);
  ptr[digit + 1] = 0;
  for(i = digit; i >= 0; i--) {
    ptr[i] = 0x30 + (val % 10);
    val /= 10;
  }
}

int main()
{
  char str_secret[10];
  int x1, x2, y1 ,y2;
  for(long secret = 10000; secret < 999999999; secret++) {
    if (secret % 100000 == 0) {
      printf("%ld\n", secret);
    }
    ltoa(secret, str_secret);
    int l = strlen(str_secret);
    if ((secret % (l + 2) == 0) && (str_secret[4] == '1')) {
      x1 = secret / 100000;
      x2 = secret % 10000;
      if ((((x2 % 100) / 10 + (x2 / 1000) * 10) - ((x1 / 1000) *10 + x1 % 10) == 1) && (((x1 / 100) % 10) * 10 + (x1 / 10) % 10 + ((x2 %1000) / 100 + ((x2 % 100) / 10) * 10) * -2 == 8)) {
	y1 = (x1 % 10) * 10 + (x1 / 100) % 10;
	y2 = ((x2 / 100) % 10) * 10 + x2 % 10;
	if ((y1 / y2 == 3) && (y1 % y2 == 0)) {
	  if (secret % (x1 * x2) == (l + 2) * (l + 2) * (l + 2) + 6) {
	    printf("%ld\n", secret);
	    break;
	  }
	}
      }
    }
  }
  return 0;
}
