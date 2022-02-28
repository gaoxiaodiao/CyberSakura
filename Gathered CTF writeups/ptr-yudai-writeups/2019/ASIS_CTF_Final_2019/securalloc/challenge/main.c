#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "securalloc.h"

char *ptr = NULL;

int readline(char *buf)
{
  char *ptr = buf;
  
  while(1) {
    if (read(0, ptr, 1) == 0) {
      exit(1);
    }
    if (*ptr == 0x0A) {
      *ptr = 0x00;
      break;
    }
    ptr++;
  }
  
  return (int)(ptr - buf);
}

unsigned int readint(void)
{
  char buf[16];
  memset(buf, 0, 16);
  readline(buf);
  return (unsigned int)atol(buf);
}

void create()
{
  int size;
  
  printf("Size: ");
  size = readint();
  
  ptr = (char*)secure_malloc(size);
  puts("Created!");
}

void edit()
{
  printf("Data: ");
  readline(ptr);
  puts("Updated!");
}

void show()
{
  printf("Data: %s\n", ptr);
}

void delete()
{
  secure_free(ptr);
  ptr = NULL;
  puts("Deleted!");
}

int menu(void)
{
  puts("==========");
  puts("1. Create");
  puts("2. Edit");
  puts("3. Show");
  puts("4. Delete");
  puts("5. Exit");
  puts("==========");
  printf("> ");
  return readint();
}

void setup(void)
{
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);
  alarm(30);

  secure_init();
}

int main(void)
{
  int option;
  setup();
  
  while(1) {
    /*
    if (ptr) {
      int i, j;
      for(j = 0; j < 16; j++) {
        for(i = 0; i < 16; i++) {
          printf("%02x ", (unsigned char)ptr[j * 16 + i - 8]);
        }
        puts("");
      }
    }
    //*/
    option = menu();
    
    switch(option) {
    case 1: create(); break;
    case 2: edit(); break;
    case 3: show(); break;
    case 4: delete(); break;
    case 5: return 0;
    default: puts("Invalid option"); break;
    }

    __heap_chk_fail(ptr);
  }
  return 0;
}
