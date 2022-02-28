unsigned long encode(unsigned long a)
{
  char i;
  unsigned long mask = 0xffffffffffffffff;
  for(i = 0x20; i != 0; i >> 1) {
    mask ^= (mask << i);
    a >>= i;
    a = ((a >> i) & mask) | (a & ~mask);
  }
  return a;
}

int main(void)
{
  int i, x;
  FILE *fp;
  char cipher[0x1000];
  
  memset(cipher, 0, 0x1000);
  fp = fopen("flag.txt", "r");

  for(i = 0; i < 0x1000; i++) {
    srand(time(NULL));
    int x = rand() ^ fgetc_unlocked(fp);
    x = (((x << 0xB) + x * 2) & 0x22110) | ((x * 0x8020) & 0x88440);
    x = (x * 0x10101) >> 16
    cipher[i] = x & 0xff;
    sleep(1);
  }

  fclose(fp);

  for(i = 0; i < 0x200; i++) {
    *(unsigned long*)cipher[i*8] = encode(*(unsigned long*)cipher[i*8]);
  }

  for(i = 0; i < 0x1000; i++) {
    putchar(cipher[i]);
  }
}
