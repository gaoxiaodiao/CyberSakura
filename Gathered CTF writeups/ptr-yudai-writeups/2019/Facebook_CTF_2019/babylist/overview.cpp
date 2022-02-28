#include <iostream>
#include <stdlib.h>
#include <string.h>

void handler()
{
  std::cout << "Timeout" << std::endl;
}
void setup()
{
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);
  alarm(0x8c);
  sgnal(0xe, handler);
}

void welcome()
{
  std::cout << "Welcome to babylist!" << std::endl;
}

void create_list()
{
  int i;
  for(i = 0; i <= 9; i++) {
    if (lists[i] == NULL) {
      break;
    }
  }
  if (i == 10) {
    std::cout << "Sorry, no empty spot available :(" << std::endl;
    return;
  }
  lists[i] = new List(); // 0x88
  std::cout << "Enter name for list:" << std::endl;
  std::getline(std::cin, (char*)list[i]);
  std::cout << "List has been created!" << std::endl;
}

int read_index()
{
  std::cout << "Enter index of list:" << std::endl;
  if (index < -1 || index > 9 || list[index] == NULL) {
    std::cout << "Error: Invalid index" << std::endl;
    exit(-1);
  }
  return index;
}

void add_element()
{
  int index = read_index();
  int number;
  std::cout << "Enter number to add:" << std::endl;
  std::cin >> number;
  lists[index].add(number);
  std::cout << "Number successfully added to list!" << std::endl;
}

void view_element()
{
  int index = read_index();
  int target;
  std::cout << "Enter index into list:" << std::endl;
  std::cin >> target;
  std::cout << "[" << target << "] = " << lists[index].get(target) << std::endl;
}

void dup_list()
{
  int index;
  for(index = 0; index <= 9; index++) {
    if (lists[index] == NULL) {
      break;
    }
  }
  if (index == 10) {
    std::cout << "Sorry, no empty spot available :(" << std::endl;
    return;
  }
  int from = read_index();
  lists[index] = new List(); // 0x88
  memcpy(lists[index], lists[from], sizeof(List)); // 0x88
  std::cout << "Enter name for new list:" << std::endl;
  std::getline(std::cin, lists[index]);
  std::cout << "List has been duplicated!" << std::endl;
}

void delete_list()
{
  int index = read_index();
  memset(lists[index], 0, sizeof(List)); // 0x88
  if (lists[index]) {
    delete lists[index];
  }
  lists[index] = NULL;
  std::cout << "List has been deleted!" << std::endl;
}

int main()
{
  int choice;
  
  setup();
  welcome();

  while(1) {
    std::cin >> choice;
    switch(choice) {
    case 1:
      create_list();
      break;
    case 2:
      add_element();
      break;
    case 3:
      view_element();
      break;
    case 4:
      dup_list();
      break;
    case 5:
      remove_list();
      break;
    default:
      break;
    }
  }
  
  return 0;
}
