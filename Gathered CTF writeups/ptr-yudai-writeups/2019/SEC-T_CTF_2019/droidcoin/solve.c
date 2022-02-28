#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char* key_adjust(unsigned char *key) {
  key[0xf] ^= 0x42;
  return key;
}

void decrypt(unsigned char* enc_cnf,
              int cnf_len,
              unsigned char *key,
              int key_len,
              unsigned char* output) {
  int i, j, k;
  char loopKey[0x100];
  char table[0x100];
  
  key = key_adjust(key);
  
  for(k = 0; k < 0x100; k++) {
    table[k] = k;
    loopKey[k] = key[k % key_len];
  }

  int x, y, ofs;
  char tmp;
  x = 0;
  for(j = 0; j < 0x100; j++) {
    x = (x + table[j] + loopKey[j]) & 0xff;
    tmp = table[x];
    table[x] = table[j];
    table[j] = tmp;
  }

  x = 0; y = 0;
  for(i = 0; i < cnf_len; i++) {
    y = (y + 1) & 0xff;
    x = (x + table[y]) & 0xff;
    tmp = table[x];
    table[x] = table[y];
    table[y] = tmp;
    ofs = (table[y] + table[x]) & 0xff;
    output[i] = enc_cnf[i] ^ table[ofs];
  }
}

int main() {
  FILE *fp = fopen("libnative-lib.so", "rb");
  char buf[0xb0];
  char output[0xb0];
  char key[0x11] = "????1STEALCOINZ!\x00";
  
  fseek(fp, 0xd84, SEEK_SET);
  fread(buf, 0x81, 1, fp);
  fclose(fp);

  char a, b, c, d;
  for(a = 'a'; a <= 'z'; a++) {
    key[0] = a;
    for(b = 'a'; b <= 'z'; b++) {
      key[1] = b;
      for(c = 'a'; c <= 'z'; c++) {
        key[2] = c;
        for(d = 'a'; d <= 'z'; d++) {
          key[3] = d;
          decrypt(buf, 0x81, key, 0x10, output);
          if (strstr(output, "flag")) {
            printf("%s\n", key);
            printf("%s\n", output);
            exit(0);
          }
        }
      }
    }
  }
  puts("Not found!");
}
