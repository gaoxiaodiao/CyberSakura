typedef struct {
  char str_id[13];
  char nickname[19]; // 0xd
  short flag; // 0x20
} st_box;

st_box* initialize(char *nickname, char *str_id)
{
  st_box *box = malloc(0x23);
  box->flag = 0;
  strcpy(box->str_id, str_id);
  strcpy(box->nickname, nickname);
  return box;
}

void check(st_box *box)
{
  char command[0x40];
  if (box->flag == 0x7a69 && strncmp("DreadPirateRoberts", box->nickname, 0x12) == 0) {
    puts("FBI detected Silkroad, enter the commadns to delete evidence and run Silkroad!");
    fgets(command, 0x80, stdin);
    strcpy(id, box->str_id);
  } else {
    puts("Not Silkroad admin!");
  }
}

char check_id(char *str_id)
{
  /*
  int id = strtol(str_id);
  if (id % strlen(str_id) + 2 == 0) {
    if (str_id[4] == '1') {
      x1 = ((id * 0x14f8b589) >> 45) - (((id * 0x14f8b589) & 0xffffffff) >> 0x1f);
      id - (((id * 0x68db8bad) >> 44) - (((id * 0x68db8bad) & 0xffffffff) >> 0x1f)) * 0x2710;
      // この辺
      if ((strlen(str_id) + 2) * (strlen(str_id) + 2)    * (strlen(str_id) + 2) + 6) {
	return 0;
      }
    }
  }
  return 1;
  */
}

void silk_road()
{
  char str_id[10];
  puts("Hello, guest!");
  printf("Enter your secret ID: ");
  scanf("%9s", str_id);
  if (check_id(str_id) == 1) {
    puts("The secret ID is not correct!");
  } else {
    // ここまで来れば解ける
    printf("Enter your nick: ");
    scanf("%22s", nickname);
    st_box *box = initialize(nickname, str_id);
    check(box);
  }
}

int main()
{
  setvbuf(stdout, NULL, 2, 0);
  srand(time());
  silk_road();
  return 0;
}
