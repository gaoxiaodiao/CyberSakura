int main(int argc, char **argv) {
  if (argc != 2) goto NG;
  
  char *flag = argv[1];
  if (strlen(flag) != 0x27) goto NG;

  if (memcmp(flag, "TWCTF{", 6) != 0 || flag[0x26] != '}') goto NG;

  int i, j;
  char table[] = "0123456789abcdef";
  int appearCount[0x10];
  int appearCountCorrect[] = {3, 2, 2, 0, 3, 2, 1, 3, 3, 1, 1, 3, 1, 2, 2, 3};
  for(i = 0; i < 0xf; i++) {
    char *flaggg = flag;
    while(1) {
      char *ptr = strchr(flaggg, table[i]);
      if (ptr) {
        flaggg += 1;
        appearCount[i] += 1;
      } else {
        break;
      }
    }
  }

  if (memcmp(appearCount, appearCountCorrect, 0x40) != 0) goto NG;

  int added = 0, xored = 0;
  int sumTable[8];
  int xorTable[8];
  int sumTableCorrect[] = {0x15e, 0xda, 0x12f, 0x131, 0x100, 0x131, 0xfb, 0x102};
  int xorTableCorrect[] = {0x52, 0x0c, 0x01, 0x0f, 0x5c, 0x05, 0x53, 0x58};
  for(j = 0; j <= 7; j++) {
    char *ofs = &flag[6 + j * 4];
    for(l = 0; l <= 3; l++) {
      added += *ofs;
      xored ^= *ofs;
    }
    sumTable[j] = added;
    xorTable[j] = xored;
  }
  if (memcmp(sumTable, sumTableCorrect, 0x20) != 0) goto NG;
  if (memcmp(xorTable, xorTableCorrect, 0x20) != 0) goto NG;

  int sumTableCorrect2[] = {0x129, 0x103, 0x12b, 0x131, 0x135, 0x10b, 0xff, 0xff};
  int xorTableCorrect2[] = {0x01, 0x57, 0x07, 0x0d, 0x0d, 0x53, 0x51, 0x51};
  added = 0;
  xored = 0;
  for(i = 0; i <= 7; i++) {
    for(j = 0; j <= 3; j++) {
      added += flag[6 + i + j * 8];
      xored ^= flag[6 + i + j * 8];
    }
    sumTable[i] = added;
    xorTable[i] = xored;
  }
  if (memcmp(sumTable, sumTableCorrect2, 0x20) != 0) goto NG;
  if (memcmp(xorTable, xorTableCorrect2, 0x20) != 0) goto NG;

  int nazoTable[0x20];
  int nazoTableCorrect[] = {0x80, 0x80, 0xff, 0x80, 0xff, 0xff, 0xff, 0xff, 0x80, 0xff, 0xff, 0x80, 0x80, 0xff, 0xff, 0x80, 0xff, 0xff, 0x80, 0xff, 0x80, 0x80, 0xff, 0xff, 0xff, 0xff, 0x80, 0xff, 0xff, 0xff, 0x80, 0xff};
  for(i = 0; i < 0x20; i++) {
    char c = flag[6 + i];
    if (c >= 0x30 && c <= 0x39) { // 0-9
      nazoTable[i] = 0xff;
    } else if (c >= 0x60 && c <= 0x66) { // a-f
      nazoTable[i] = 0x80;
    } else {
      nazoTable[i] = 0;
    }
  }
  if (memcmp(nazoTable, nazoTableCorrect, 0x80) != 0) goto NG;

  int sum = 0;
  for(i = 0; i < 0x10; i++) {
    sum += flag[(i + 3) * 2]
  }
  if (sum != 0x488) goto NG;
  
  if (flag[0x25] != '5') goto NG;
  if (flag[0x07] != 'f') goto NG;
  if (flag[0x0B] != '8') goto NG;
  if (flag[0x0C] != '7') goto NG;
  if (flag[0x17] != '2') goto NG;
  if (flag[0x1F] != '4') goto NG;

  puts("Correct");
  return 0;
  
 NG:
  puts("incorrect");
  return 1;
}
