#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <limits.h>

long A = 0, B = 0;
int n = 0;
long *terms = NULL;

__attribute__((constructor)) void setup() {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);
  alarm(30);
}

void stop(char *msg) {
  fprintf(stderr, "[ABORT] %s\n", msg);
  exit(1);
}

void readline(char *buf, int size) {
  int readSize = read(0, buf, size);
  if (readSize <= 0) stop("Broken pipe");
  buf[readSize] = 0;
}

long readlong() {
  char buf[0x10] = {0};
  readline(buf, 0x20);
  return atol(buf);
}

void set_coeffs() {
  printf("A = ");
  A = readlong();
  printf("B = ");
  B = readlong();
}

void set_n() {
  printf("n = ");
  n = (int)readlong();
  terms = (long*)malloc(sizeof(long) * n);
  if (terms == NULL) {
    stop("Could not allocate memory");
  }
}

void set_initial() {
  printf("x0 = ");
  terms[0] = readlong();
  printf("x1 = ");
  terms[1] = readlong();
}

void calculate() {
  int i;
  long a, b;
  for(i = 2; i < n; i++) {
    a = A * terms[i - 2];
    b = B * terms[i - 1];
    if ((a > 0 && b > LONG_MAX - a) ||
        (a < 0 && b < LONG_MAX - a)) {
      stop("Overflow detected");
    } else {
      terms[i] = a + b;
    }
  }
}

void check_term() {
  puts("Calculation Done!");

  int i;
  while(1) {
    printf("i > ");
    i = (int)readlong();
    if (i < 0) break;
    printf("x(%d) = %ld\n", i, terms[i]);
  }
}

int main() {
  char buf[0x1f8];
  FILE *fp;
  fp = fopen("description.txt", "r");
  if (fp == NULL) {
    stop("File not found");
  }
  fread(buf, 1, 0x1f8, fp);
  puts(buf);
  
  set_coeffs();
  set_n();
  set_initial();
  calculate();
  check_term();

  puts("Bye!");
  return 0;
}
