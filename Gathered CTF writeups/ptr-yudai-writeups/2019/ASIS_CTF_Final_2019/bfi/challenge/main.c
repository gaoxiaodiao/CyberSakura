#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "bf.h"
#define MAX_LINE 0x10

__attribute__((constructor)) void setup(void) {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
}

void readline(char *buf, int size) {
  int r = read(0, buf, size);
  if (r == 0) exit(0);
  char *ptr = strchr(buf, 0xA);
  if (ptr) *ptr = 0;
}

int readsize(void) {
  char buf[0x10];
  int value;
  
  memset(buf, 0, 0x10);
  readline(buf, 0x0f);
  value = atoi(buf);
  
  if (value <= 0 || value > 0x200) {
    puts("[-] Invalid size");
    exit(0);
  }
  return value;
}

int main(void) {
  int code_size, buf_size;
  char *buffer;
  char *code;

  while(1) {
    printf("=-=-=-=-=-=-=-=-=-=\ncode size = ");
    code_size = readsize();
    
    printf("code = ");
    code = calloc(code_size, 1);
    readline(code, code_size);
    if (*code == '\0') break;
    
    printf("buffer size = ");
    buf_size = readsize();
    
    puts("[+] Running...");
    if (bf_interpret(code, code_size, buf_size)) {
      puts("[-] Unknown error");
    } else {
      puts("[+] Done!");
    }

    free(code);
    getchar();
  }
  
  return 0;
}
