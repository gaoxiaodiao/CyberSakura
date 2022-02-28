#include <stdio.h>

typedef struct {
  char is_used;
  int id;
  char *buf;
} Karte;

int zfd = -1;
int rfd = -1;
unsigned long lock = -1;
Karte list[4];
unsigned long key;
char name[0x40];

unsigned long getrand() {
  unsigned long val;
  read(rfd, &val, 8);
  return val;
}

__attribute__((constructor)) static void init() {
  setbuf(stdout, NULL);
  zfd = open("/dev/zero", O_RDONLY);
  rfd = open("/dev/urandom", O_RDONLY);
  key = getrand();
  lock = key;
}

int getnline(char *buf, int size) {
  if (buf == NULL || size <= 0) return 0;
  int readSize = read(0, buf, size - 1);
  if (readSize == 0) return -1;
  buf[size - 1] = 0;
  char *ptr = strchr(buf, 0x0A);
  if (ptr) *ptr = 0;
  return 1;
}

int getint() {
  char buf[0x20] = {0};
  getnline(buf, 0x20);
  return atoi(buf);
}

int menu() {
  printf("=== MENU ===\n");
  return getint();
}

void add() {
  int i, size, id, j;
  char *buf;
  for(i = 0; i < 3; i++) {
    if (list[i].is_used == 0) {
      printf("Input size > ");
      size = getint();
      if (size <= 0x800) {
        buf = calloc(1, size);
      } els {
        buf = malloc(size);
      }
      if (buf == NULL) {
        puts("allocation failed...");
        return;
      }
      if (size > 0x800) {
        read(zfd, buf, size);
      }
      
      printf("Input description > ");
      getnline(buf, size);
      id = getrand() & 0xffff;
      for(j = 0; j < 3; j++) {
        if (list[j].id == id && list[j].is_used) {
          id = getrand() & 0xffff;
          j = 0;
        }
      }

      list[i].id = id;
      list[i].buf = buf;
      printf("\nAdded id %d\n", id);
      return;
    }
  }

  puts("karte is full!!");
}

void delete() {
  int id, i;
  printf("Input id > ");
  id = getint();
  for(i = 0; i < 3; i++) {
    if (id == list[i].id && list[i].is_used) {
      list[i].is_used = 0;
      free(list[i].buf);
      printf("\nDeleted id %d\n", id);
      return;
    }
  }

  puts("karte not found...");
}

void modify() {
  int id, i;
  if (key == lock) {
    printf("Input id > ");
    id = getint();
    for(i = 0; i < 3; i++) {
      if (id == list[i].id) {
        key = 0xDeadC0beBeef;
        printf("Input new description > ");
        getnline(list[i].buf, strlen(list[i].buf) + 1);
        printf("\nModified id %d\n", id);
        return;
      }
    }
  } else {
    puts("Hey! You can't modify karte any more!!");
    return;
  }

  puts("karte not found...");
}

int main() {
  if (zfd == -1 || rfd == -1) return -1;
  puts("=== LOGO ===");

  while(1) {
    printf("Input patient name... ");
    getnline(name, 0x40);
    puts("OK");
    
    while(1) {
      int choice = menu();
      if (choice == 0) {
        puts("Bye");
        return 0;
      } else if (choice == 1) {
        add();
      } else if (choice == 2) {
        puts("damedesu");
      } else if (choice == 3) {
        delete();
      } else if (choice == 4) {
        modify();
      } else if (choice == 99) {
        break;
      } else {
        puts("Wrong input.");
      }
    }
  }
  
  return 0;
}
