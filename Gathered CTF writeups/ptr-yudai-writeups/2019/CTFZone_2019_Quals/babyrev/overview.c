int main(int argc, char **argv) {
  short c;
  int i, j;
  FILE *fp;
  char key[0x50*6];

  if (argc < 2) {
    printf("usage: %s <key_file>\n", argv[0]);
    return 1;
  }

  fp = fopen(argv[1], "rb");
  if (fp == NULL) {
    printf("cannot open file %s\n", argv[1]);
    return 1;
  }

  for(i = 0; i < 6; i++) {
    for(j = 0; j < 0x50; j++) {
      c = fgetc(fp);
      if (c != EOF) {
        buffer[i*0x50+j] = c;
      }
    }
  }

  if (check01(key) == 0 || ... || check08(key) == 0) {
    printf("Incorrect flag\n");
  } else {
    for(i = 0; i < 6; i++) {
      for(j = 0; j < 0x50; j++) {
        printf("%c", key[i * 0x50 + j]);
      }
    }
  }
}
