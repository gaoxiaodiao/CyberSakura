int hash(char *flag)
{
  int i;
  long pon = 0x17;
  for(i = 0; i < length; i++) {
    pon = (flag[i] << i) + (pon << 3) - pon;
  }
  return (int)(pon >> 4);
}

int check_flag(char* flag)
{
  int i, j;
  long w = 0, x = 0, y = 0, z = 0;
  long xored = 0, sum = 0;
  int length = strlen(flag);
  for(i = 0; i < length; i++) {
    if (i & 1 == 0) {
      w ^= flag[i];
    }
    if ((unsigned int)w & 1) {
      x ^= flag[i];
    }
    if (i & 1) {
      y += flag[i];
    }
    if ((unsigned int)y & 1) {
      z ^= flag[i];
    }
  }

  for(j = 0; j < length; j++) {
    xored ^= flag[j];
  }
  for(i = 0; i < lengthl i++) {
    if (i & 1) {
      sum += flag[i];
    }
    if (i & 1 == 0) {
      z ^= flag[i];
    }
  }

  int edx = ((y * 0x66666667) >> 34) - (y >> 31);
  if ((y - ((edx << 2) + edx) * 2) != 8) return 0;

  int edx2 = ((sum * 0x66666667) >> 34) - (sum >> 31);
  if ((sum - ((edx2 << 2) + edx2) * 2 + 3) != (y - ((edx << 2) + edx) * 2)) return 0;

  if (length != 0x19) return 0;
  if (z != 0x19) return 0;
  if (x != 0x10) return 0;
  if (xored != 0x3f) return 0;
  if (w != 9) return 0;

  int ecx = y + sum;
  edx = ((ecx * 0x66666667) >> 34) - (ecx >> 31);
  if (ecx - ((((edx << 2) - (ecx >> 31)) << 2) + edx) * 2 != 3) return 0;

  ecx = y * 3 + sum;
  edx = ((ecx * 0x66666667) >> 34) - (ecx >> 31);
  if ((ecx - ((edx << 2) + edx) * 2) != 9) return 0;

  if (flag[0] != 0x41) return 0;
  if (flag[2] != 0x74) return 0;
  if (flag[0xC] != 0x33) return 0;
  if (flag[0xa] != 0x54) return 0;
  if (hash != 0x22233025) return 0;
  
  return 0;
}
