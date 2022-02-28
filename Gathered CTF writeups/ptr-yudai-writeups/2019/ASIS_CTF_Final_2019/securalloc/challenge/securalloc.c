#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <malloc.h>

#include "securalloc.h"

unsigned long canary;

void secure_init(void)
{
  int i;
  FILE *fp = fopen("/dev/urandom", "rb");
  if (fp == NULL) exit(1);
  for(i = 0; i < 8; i++) {
    fread(&canary, 8, 1, fp);
  }
  fclose(fp);

  canary &= 0xffffffffffffff00;
}

char *secure_malloc(unsigned int size)
{
  char *ptr = (char*)malloc(size + 16);
  if (ptr == NULL) __abort("Resource depletion (secure_malloc)");
  
  *(unsigned int*)ptr = size;
  *(unsigned int*)(ptr + 4) = size + 1;
  *(unsigned long*)(ptr + 8 + size) = canary;
  
  return ptr + 8;
}

void secure_free(char *ptr)
{
  if (ptr == NULL) return;
  
  unsigned int size1 = *(unsigned int*)(ptr - 8);
  unsigned int size2 = *(unsigned int*)(ptr - 4);
  
  if (size2 - size1 != 1) {
    __abort("*** double free detected ***: <unknown> terminated");
  }
  __heap_chk_fail(ptr);
  
  memset(ptr - 8, 0, size1 + 16);
  free((char*)(ptr - 8));
}

void __heap_chk_fail(char *ptr)
{
  if (ptr == NULL) return;
  
  unsigned int size1 = *(unsigned int*)(ptr - 8);
  unsigned int size2 = *(unsigned int*)(ptr - 4);
  unsigned long local_canary = *(unsigned long*)(ptr + size1);

  if (size2 - size1 == 1 && local_canary != canary) {
    __abort("*** heap smashing detected ***: <unknown> terminated");
  }
}

void __abort(char *msg)
{
  fprintf(stderr, "%s\n", msg);
  exit(1);
}
