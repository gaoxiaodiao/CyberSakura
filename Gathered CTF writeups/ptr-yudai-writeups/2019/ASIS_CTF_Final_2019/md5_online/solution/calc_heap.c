#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/md5.h>

#define BUFFER_SIZE 512

int main(int argc, char **argv) {
  int i;
  unsigned int c1, c2, c3;
  MD5_CTX ctx;
  unsigned char md5[MD5_DIGEST_LENGTH];
  unsigned char data[BUFFER_SIZE + 8];
  char result[33];

  if (argc < 2) {
    printf("Usage: %s md5.hexdigest\n", argv[0]);
    return 1;
  }

  for(i = 0; i < BUFFER_SIZE; i++) {
    data[i] = 'A';
  }
  data[BUFFER_SIZE + 0] = 0x44;
  data[BUFFER_SIZE + 4] = 0x61;
  data[BUFFER_SIZE + 5] = 0x01;
  data[BUFFER_SIZE + 6] = 0x00;
  
  for(c3 = 0x55; c3 <= 0x58; c3++) {
    data[BUFFER_SIZE + 3] = c3;
    for(c1 = 0; c1 < 0x10; c1++) {
      data[BUFFER_SIZE + 1] = c1 << 4;
      for(c2 = 0; c2 < 0x100; c2++) {
        data[BUFFER_SIZE + 2] = c2;

        MD5_Init(&ctx);
        MD5_Update(&ctx, data, strlen(data));
        MD5_Final(md5, &ctx);
        
        for(i = 0; i < 16; i++) {
          sprintf(&result[i * 2], "%02x", (unsigned int)md5[i]);
        }
        
        if (strcmp(result, argv[1]) == 0) {
          printf("0x%08x\n", *(unsigned int*)&data[BUFFER_SIZE]);
          return 0;
        }
     
      }
    }
  }
  
  return 1;
}
