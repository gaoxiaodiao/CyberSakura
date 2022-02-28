typedef struct {
  char name[0x20];
  long hp;
  void *kick;
} Pokemon;

void list_pokemons() {
  for(i = 0; i < 10; i++) {
    printf("%d . %s /HP[%d]\n", i, my_pokemons[i].name, my_pokemons[i].hp);
  }
  now_selected = user_input(); // [!] vulnerable (1)
  printf("Go %s !\n", my_pokemons[now_selected]);
}

int attack() {
  my_pokemons[now_selected].kick(&my_pokemons[now_selected]);
  putchar('\n');
  return (is_dead ^= 1);
}

void pokeball() {
  pokeball_art();
  puts("slot : ");
  i = user_input(); // [!] vulnerable (1)
  if (is_dead == 0) {
    my_pokemons[i].hp = 100;
  }
  puts("name: ");
  read(0, my_pokemons[i].name, 0x400);
  pichu();
}

void battle() {
  pichu();
  while(1) {
    switch (menu()) { // [!] vulnerable (1)
    case 1: // fight
      attack();
      break;
    case 2: // poke ball
      list_pokemons();
      break;
    case 4: // pokemons
      pokeball();
      break;
    }
  }
}

int main() {
  Pokemon my_pokemons[10];
  for(i = 0; i < 10; i++) {
    strcpy(my_pokemons[i].name, "empty");
    my_pokemons[i].hp = 0;
    my_pokemons[i].kick = kick;
  }
  battle();
}
