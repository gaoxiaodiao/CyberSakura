void FLAG(int *field) {
  int i, j;

  char string[] = "~~~";
  int list[0x20];
  for(i = 0; i < 0x10; i++) {
    list[2 * i + 0] = field[i] / 8;
    list[2 * i + 1] = field[i] * 7;
  }

  for(j = 0; j < 0x20; j++) {
    if (list[j] > 0x190) abort();
  }

  for(j = 0; j < 0x20; j++) {
    xored[j] = string[j] ^ list[j];
  }
}

int cnt = 0;
int field[32];

int open_random() {
  srand(time(0));
  rand() & 0xF;
}

void proc() {
 .label_open:
  field[cnt] = wParam;
  cnt++;
  field[cnt] = open_random();
  cnt++;
  Sleep(2);
}
