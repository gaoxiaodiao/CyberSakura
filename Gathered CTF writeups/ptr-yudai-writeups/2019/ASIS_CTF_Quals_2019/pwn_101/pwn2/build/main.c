#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#define MAX_ADDR 10
#define NAME_LEN 32

typedef struct {
  unsigned long phone;
  char *name;
  char *desc;
} t_address;
t_address address[MAX_ADDR];

void handler(int sig)
{
  if (sig == SIGALRM) {
    puts("\nTimeout");
    exit(1);
  }
}

void setup(void)
{
  setvbuf(stdout, NULL, _IONBF, 0);
  signal(SIGALRM, handler);
  alarm(60);
}

int menu(void)
{
  int i;
  puts("========================");
  puts(" 1. Add an address");
  puts(" 2. Show an address");
  puts(" 3. Delete an address");
  puts("========================");
  printf("> ");
  scanf("%d", &i);
  return i;
}

void add(void)
{
  int i;
  int size;

  for(i = 0; i < MAX_ADDR; i++) {
    if (address[i].name == NULL) {
      break;
    }
  }
  if (i == MAX_ADDR) {
    puts("You can't add any more addresses.");
    return;
  }

  printf("Description Length: ");
  scanf("%d", &size);
  if (size < 0 || size > 0x2000) {
    puts("Invalid size.");
    return;
  }
  
  address[i].name = (char*)malloc(NAME_LEN);
  address[i].desc = (char*)malloc(size);
  size++;

  printf("Phone Number: ");
  scanf("%d", &address[i].phone);
  printf("Name: ");
  read(0, address[i].name, NAME_LEN);
  printf("Description: ");
  read(0, address[i].desc, size);
  printf("Added an address: index=%d\n", i);
}

void show(void)
{
  int i;

  printf("Index: ");
  scanf("%d", &i);

  if (i < 0 || i >= MAX_ADDR) {
    puts("Invalid index.");
    return;
  }

  if (address[i].name == NULL) {
    puts("Unused address.");
    return;
  }

  printf("Phone Number: %d\n", address[i].phone);
  printf("Name        : %s\n", address[i].name);
  printf("Description : %s\n", address[i].desc);
}

void delete(void)
{
  int i;

  printf("Index: ");
  scanf("%d", &i);

  if (i < 0 || i >= MAX_ADDR) {
    puts("Invalid index.");
    return;
  }

  if (address[i].name == NULL) {
    puts("Unused address.");
    return;
  }

  free(address[i].name);
  free(address[i].desc);
  
  address[i].phone = 0;
  address[i].name = NULL;
  address[i].desc = NULL;
  puts("OK.");
}

int main()
{
  setup();
  
  while(1) {
    int choice = menu();
    if (choice == 1) {
      add();
    } else if (choice == 2) {
      show();
    } else if (choice == 3) {
      delete();
    } else {
      puts("Bye.");
      break;
    }
  }
  
  return 0;
}
