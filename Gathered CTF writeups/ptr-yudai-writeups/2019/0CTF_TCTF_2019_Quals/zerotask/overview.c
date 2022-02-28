char *tasks;

typedef struct {
  char *data; // 0x00
  long size;  // 0x08
  int x0;
  char key[0x20]; // 0x14
  char iv[0x10]; // 0x34
  int x1;
  long x2;
  EVP_CIPHER_CTX *ctx; // 0x58
  long id; // 0x60
  char *next; // 0x68
} st_task;

void handler()
{
  puts("\n[!] bye!");
  exit(1);
}

void setup()
{
  signal(0xE, handler);
  alarm(0x20);
  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);
  tasks = malloc(0x1010);
}

void show_menu()
{
  puts("1. Add task");
  puts("2. Delete task");
  puts("3. Go");
  printf("Choice: ");
}

int read_int()
{
  char str_val[0x18];
  memset(str_val, 0, 8);
  readuntil(str_val, 8, 0xA);
  return atoi(str_val);
}

void add_task()
{
  int id, mode;
  printf("Task id: ");
  id = read_int();
  printf("Encrypt(1) / Decrypt(2): ");
  mode = read_int();
  if (mode == 1 || mode == 2) {
    st_task *task = malloc(0x70);
    if (do_cipher(task, mode) == 0) {
      task->id = id;
      task->next = tasks;
    }
  }
}

void delete_task()
{
  int id;
  st_task *ptr1, *ptr2;
  ptr1 = tasks;
  ptr2 = tasks;
  
  printf("Task id: ");
  id = read_int();
  if (tasks != NULL && id == tasks->id) {
    tasks = tasks->next;
    EVP_CIPHER_CTX_free(ptr1->ctx);
    free(ptr1->data);
    free(ptr1);
  } else {
    for(ptr1 = NULL; ptr1->id != id; ptr1 = ptr1->next) {
      ptr2 = ptr1;
    }
    ptr2->next = ptr1->next;
    EVP_CIPHER_CTX_free(ptr1->ctx);
    free(ptr1->data);
    free(ptr1);
  }
}

void do_cipher(st_task *task, int mode)
{
  printf("Key : ");
  read_str(task->key, 0x20);
  printf("IV : ");
  read_str(task->iv, 0x10);
  printf("Data size : ");
  size = read_int();
  if (0 < size && size <= 0x1000) {
    task->ctx = EVP_CIPHER_CTX_new();
    if (mode == 1) {
      EVP_EncryptInit_ex(task->ctx, EVP_aes_256_cbc(), 0, key, iv);
    } else if (mode == 2) {
      EVP_DecryptInit_ex(task->ctx, EVP_aes_256_cbc(), 0, key, iv);
    }
    task->mode = mode;
    task->data = malloc(task->size);
    printf("Data : ");
    read_str(task->data, task->size);
  }
}

void worker(st_task *task2pass)
{
  int outlen, offset = 0;
  puts("Prepare...");
  sleep(2);
  memset(output, 0, 0x1010);
  if (!EVP_CipherUpdate(task->ctx, output, outlen, task->data, task->size)) {
    pthread_exit(0);
  }
  offset += outlen;
  if (!EVP_CipherFinal_ex(task->ctx, output + offset, outlen)) {
    pthread_exit(0);
  }
  offset += outlen;
  puts("Ciphertext: ");
  print_hex(stdout, output, offset, 0x10, 1);
  pthread_exit(0);
}

void go()
{
  st_task *task2pass;
  long id;
  printf("Task id : ");
  id = read_int();
  task2pass = tasks;
  if (task2pass != NULL) {
    while(task2pass->id != id) {
      task2pass = task2pass->next;
    }
    pthread_create(thread, 0, worker, task2pass);
  }
}

int main(int argc, char **argv)
{
  int n, choice;
  setup();
  while(1) {
    show_menu();
    choice = read_int();
    if (choice == 1) {
      add_task();
    } else if (choice == 2) {
      delete_task();
    } else if (choice == 3) {
      if (n <= 2) {
        go();
        n += 1;
      } else {
        puts("bye");
        exit(1);
      }
    } else {
      puts("bye");
      exit(1);
    }
  }
  return 0;
}
