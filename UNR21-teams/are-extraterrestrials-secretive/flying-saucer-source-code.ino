int to_num(char c) {
  int res = 0;
  const char *alph = "_{AMUNIEROCLTSPVDBJHGZFXKQWY}";
  const char *p = alph;
  while(c != *p) {
    p++;
    if(*p == 0) p = alph;
    res++;
  }
  return res;
}

void add_round_key(char *buf, char key) {
  int k = to_num(key);
  for(int i=0; i<9; i++) {
    const char *alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ{}_ABCDEFGHIJKLMNOPQRSTUVWXYZ{}";
    const char *p = alph;
    while(buf[i] != *p) {
      p++;
      if(*p == 0) p = alph;
    }
    p += k;
    buf[i] = *p;
  }
}

void sub_bytes(char *buf) {
  for(int i=0; i<9; i++) {
    buf[i] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ{}_"[to_num(buf[i])];
  }
}

void shift_rows(char *buf) {
  char aux;
  aux = buf[3]; buf[3] = buf[4]; buf[4] = buf[5]; buf[5] = aux;
  aux = buf[6]; buf[6] = buf[8]; buf[8] = buf[7]; buf[7] = aux;
}

void ecb_encrypt_block(char *buf) {
  const char *key = "ALIEN";

  add_round_key(buf, key[0]);
  for(int round=1; round<5; round++) {
    sub_bytes(buf);
    shift_rows(buf);
    add_round_key(buf, key[round]);
  }
}

void setup() {
  char flag[73];
  strcpy(flag, "CTF{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}");
  for(int i=0; flag[i] != 0; i += 9) {
    ecb_encrypt_block(&flag[i]);
  }

  delay(10000);

  pinMode(LED_BUILTIN, OUTPUT);

  for(int i=0; flag[i] != 0; i++) {
    int x = to_num(flag[i]);

    for(int j=0; j<5; j++) {
      digitalWrite(LED_BUILTIN, HIGH);
      delay(100);
      if(x % 2 == 0) {
        digitalWrite(LED_BUILTIN, LOW);
      } else {
        digitalWrite(LED_BUILTIN, HIGH);
      }
      delay(200);
      digitalWrite(LED_BUILTIN, LOW);
      delay(100);
      x /= 2;
    }
  }
}

void loop() {}
