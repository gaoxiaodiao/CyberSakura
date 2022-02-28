// sub_466330
int hash_string(char *data, int key) {
  int i;
  int hash = 0;
  for (i = 0; i < strlen(data); i++) {
    hash = ((filename[i] | 0x20) + ((hash >> 8) | ((hash & 0xff) << 24))) ^ key;
  }
}
