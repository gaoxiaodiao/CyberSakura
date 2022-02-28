char encode_byte(char c) {
  if ('a' <= c <= 'z') {
    return c - 0x57;
  } else if ('A' <= c <= 'Z') {
    return c - 0x37;
  } else if ('0' <= c <= '9') {
    return c - 0x30;
  }
  return 0; // undefined
}

int encode_password(char *password, char *encoded) {
  int length = strlen(password);
  int i;
  for(i = 0; length >= 0; i++, length -= 2) {
    result[i] = (encode_byte(password[length]) << 4)
      + encode_byte(password[length + 1]);
  }
}

void make_buffer(int size, int *array) {
  int i, j, x;
  
  array[0] = 0;
  for(i = 1; i < size; i++) {
    x = array[i] - i;
    for(j = 0; j < i; j++) {
      if (array[j] == x || x < 0) {
        x = array[i] + i;
        break;
      }
    }
    array[i] = x;
  }
}
