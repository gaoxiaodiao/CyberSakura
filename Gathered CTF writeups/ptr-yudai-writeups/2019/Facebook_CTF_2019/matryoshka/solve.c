#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <byteswap.h>

unsigned char memory[0x100];
unsigned char original[0x30] =
  "\xf6\x2c\x72\x1a\x03\x99\x0e\x78\xbd\x90\xe9\x68\xd0\x69\x37\x29"
  "\xf8\x12\xf4\xe5\xd0\xfb\xf3\x7e\x72\x61\x79\x19\xed\x44\x12\x52"
  "\xf5\xf9\xaa\x14\x36\x0d\x1f\xb2\x52\x6b\xf2\x6a\xda\x9d\xec\x3c";
unsigned char string[0x30];

void scramble_memory(char *password)
{
  unsigned long delta = 0x0808080808080808;
  unsigned long seed = 0x0706050403020100;
  unsigned long *ptr = (unsigned long*)&memory;
  int i;
  for(i = 0; i < 0x20; i++) {
    *ptr = seed;
    seed += delta;
    ptr++;
  }
  unsigned char r9 = 0, r10 = 0;
  for(i = 0; i < 0x100; i++) {
    unsigned char xmm0 = memory[i];
    r9 += xmm0 + password[r10];
    memory[i] = memory[r9];
    memory[r9] = xmm0;
    r10 = (r10 + 1) % 8;
  }
}

void create_string()
{
  int i;
  unsigned char pos0 = 0, pos1 = 0;
  for(i = 0; i < 0x30; i++) {
    pos0 += 1;
    unsigned char xmm2 = memory[pos0];
    pos1 += xmm2;
    unsigned char xmm3 = memory[pos1];
    memory[pos0] = xmm3;
    memory[pos1] = xmm2;
    string[i] ^= memory[(xmm2 + xmm3) & 0xff];
  }
}

int main()
{
  char password[] = "????wT96";
  char c1, c2, c3, c4;
  for(c1 = 0x20; c1 < 0x7f; c1++) {
    printf("c1 = %d\n", c1);
    for(c2 = 0x20; c2 < 0x7f; c2++) {
      for(c3 = 0x20; c3 < 0x7f; c3++) {
	for(c4 = 0x20; c4 < 0x7f; c4++) {
	  password[0] = c1;
	  password[1] = c2;
	  password[2] = c3;
	  password[3] = c4;
	  memcpy(string, original, 0x30);
	  
	  scramble_memory(password);
	  create_string();

	  unsigned long ret = *(unsigned long*)&(string);
	  unsigned char *text = (unsigned char*)((unsigned long)string + 8);

	  int i;
	  for(i = 0; i < 0x28; i++) {
	    if (!(0x20 <= text[i] && text[i] < 0x7f)) {
	      break;
	    }
	  }
	  if (i > 0x20) {
	    printf("password: %s\n", password);
	    printf("ret: %016lx\n", ret);
	    printf("text: %s\n", text);
	      
	    unsigned long d, c, b, a;
	    unsigned long x = __bswap_64(ret);
	    d = 0x115c28da834feffd ^ x;
	    c = 0x665f336b1a566b19 ^ d;
	    b = 0x393b415f5a590044 ^ c;
	    a = 0x3255557376f68 ^ b;
	    printf("%016lx %016lx %016lx %016lx\n", a, b, c, d);
	  }
	}
      }
    }
  }
  return 0;
}
