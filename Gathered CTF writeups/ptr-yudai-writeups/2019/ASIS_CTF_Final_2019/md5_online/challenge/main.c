#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/md5.h>
#include <time.h>

#define BUFFER_SIZE 512

typedef struct {
  char hexdigest[64];
  char text[BUFFER_SIZE];
  unsigned char *salt;
} CORE;

FILE *fp;
CORE *core;

/**
 * Calculate MD5 hexdigest
 */
void md5(char *in, char *out, int isSalt)
{
  int i;
  MD5_CTX ctx;
  char *target;
  unsigned char digest[MD5_DIGEST_LENGTH];

  if (isSalt == 0) {
    /* Not salted */
    target = in;
  } else {
    /* Salted */
    target = in - 4;
    for(i = 0; i < 4; i++) {
      core->salt[i] = rand() % 0x100;
      if (core->salt[i] == 0) core->salt[i]++;
    }
  }
  
  if (MD5_Init(&ctx) != 1) {
    perror("MD5_Init");
    exit(1);
  }

  if (MD5_Update(&ctx, target, strlen(target)) != 1) {
    perror("MD5_Update");
    exit(1);
  }

  if (MD5_Final(digest, &ctx) != 1) {
    perror("MD5_Final");
    exit(1);
  }

  /* Digest to hexdigest */
  for(i = 0; i < 16; i++) {
    sprintf(&out[i << 1], "%02x", (unsigned int)digest[i]);
  }
}

/**
 * Read a line
 */
void readline(char *buf, int size)
{
  char *ptr;
  int readSize, sum = 0;

  while(sum < size) {
    readSize = read(0, buf + sum, 500);
    if (readSize == 0) {
      perror("read");
      exit(1);
    }
    
    ptr = strchr(buf, '\n');
    if (ptr != NULL) {
      *ptr = 0;
      break;
    }
    
    sum += readSize;
  }
}

/**
 * Say hello
 */
void hello(void)
{
  char banner[0x200];
  
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);
  srand(time(NULL));

  /* Initialize the core */
  core = (CORE*)malloc(sizeof(CORE));
  core->salt = core->text - 4;

  /* Read and show banner */
  fp = fopen("banner.txt", "r");
  if (fp == NULL) {
    perror("fopen");
    exit(1);
  }

  memset(banner, 0, 0x200);
  fread(banner, 1, 0x200, fp);
  printf("%s", banner);
}


/**
 * Say good bye
 */
void bye(void)
{
  fclose(fp);
  free(core);
}

/**
 * Main routine
 */
int main(void)
{
  hello();
  int i;
  char ask_salt;
  
  for(i = 0; i < 3; i++) {
    printf("Text: ");
    readline(core->text, BUFFER_SIZE);

    if (*core->text == 0) break;
    
    printf("With salt? [y/N] ");
    ask_salt = getchar();
    getchar();
    
    if (ask_salt == 'Y' || ask_salt == 'y') {
      /* Salted */
      md5(core->text, core->hexdigest, 1);
      printf("MD5 (salted): %s\n", core->hexdigest);
      printf("Salt: \\x%02x\\x%02x\\x%02x\\x%02x\n",
             core->salt[0],
             core->salt[1],
             core->salt[2],
             core->salt[3]);
    } else {
      /* Not salted */
      md5(core->text, core->hexdigest, 0);
      printf("MD5: %s\n", core->hexdigest);
    }
  }
  
  bye();
}
