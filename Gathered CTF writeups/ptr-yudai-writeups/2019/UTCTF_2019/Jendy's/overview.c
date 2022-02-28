typedef struct {
  char* first;
  char* last;
  char* name;
  long n;
} st_cart;

void add_name(st_cart *cart)
{
  puts("What is your name?");
  cart->name = malloc(0x20);
  fgets(cart->name, 0x20, stdin);
}

void add_item(st_cart *cart)
{
  int i, n, choice;
  char *item;
  char *first;

  puts("Which item would you like to order from Jendy's?");
  for(i = 0; i <= 4; i++) {
    printf("%d. %s\n", i, options[i]);
  }

  scanf("%d%*c", &choice);

  if (0 <=choice && choice <= 4) {
    item = malloc(0x20);
    strncpy(item, options[choice], strlen(options[choice]));
    first = cart->first;
    cart->n += 1;

    if (first == 0) {
      cart->first = item;
      cart->last = item;
    } else {
      (void*)((unsigned long)(cart->last) + 0x18) = (void*)item;
      cart->last = item;
    }
  } else {
    puts("Not a valid option!");
  }
}

void remove_item(st_cart *cart)
{
  int index;
  char *ptr, *last;
  puts("Please enter the number of the item from your order that you wish to remove");
  scanf("%d%*c", &index);
  if (index >= 0) {
    ptr = cart->first;
    if (ptr != NULL && index == 0) {
      free(ptr);
      cart->first = 0;
      cart->last = 0;
      cart->n -= 1;
    } else {
      for(i = 0; ptr != NULL; i++) {
	if (i == index) break;
	last = ptr;
	ptr = (char*)((unsigned long)ptr + 0x18);
      }
      if (ptr != NULL) {
	if (i == index) {
	  if (index == cart->n - 1) {
	    free(cart->last);
	    cart->last = last;
	  } else {
	    (void*)((unsigned long)last + 0x18) = (void*)((unsigned long)ptr + 0x18)
	    free(ptr);
	  }
	  cart->n -= 1;
	}
      }
    }
  }
}

void view_order(st_cart *cart)
{
  int i:
  char msg[0x28];
  char *item;

  if (cart->name) {
    snprintf(msg, 0x28, "Name: %s\n", cart->name);
    printf("%s", msg);
  }

  item = cart->first;

  for(i = 0; i < cart->n; i++) {
    printf("Item #%d: ", i);
    printf(item);
    putchar(0x0A);
    item = (char*)((unsigned long)item + 0x18);
  }
}

void checkout(st_cart *cart)
{
  puts("Thank you for for ordering at Jendy's!");
}

int main(void)
{
  st_cart *cart;
  int choice;

  setbuf(stdin, 0);
  setbuf(stdout, 0);

  cart = (st_cart)malloc(0x20);

  print_menu();
  scanf("%d%*c", &choice);

  while(1) {
    switch(choice) {
    case 1:
      add_name(cart);
      break;
    case 2:
      add_item(cart);
      break;
    case 3:
      remove_item(cart);
      break;
    case 4:
      view_order(cart);
      break;
    case 5:
      checkout(cart);
      return 0;
    default:
      puts("Not a valid choice!");
      break;
    }
  }
  
  return 0;
}
