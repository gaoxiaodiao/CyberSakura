//Makefile
//all:
//	gcc -Wl,-z,relro,-z,now ./kill_kirby.c -o kill_kirby -no-pie


/*************************************
//You kill kirby for your free??
**************************************/

#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<string.h>

#define MAXKIRBY 0x20
#define NORMALBUF 0x50
#define SMALLBUF 0x48


struct kirby{ //0:normal 1:small 2:large
  struct kirby *parent_kirby;
  struct kirby *child_kirby;
  long long bufsize;
  char *name;
};
static struct kirby kingkirby;
long long is_debug = 0;
long long is_exitable = 0;
long long kirby_num = 0;
int kirby_is_free = 0;
long long total_walk = 0;

void print_menu(void)
{
  printf("1:walk\n2:list\n3:kill kirby\n4:rename\n0:exit\n");
}

long long getint(void)
{
  long long num;
  if(fscanf(stdin,"%lld",&num)!=1){
    printf("BYE\n");
    exit(1);
  }
  getchar();
  return num;
}

void put_back(struct kirby *new_kirby){
  struct kirby *now = &kingkirby;
  while(1==1){
    if(now->child_kirby==NULL){
      now->child_kirby = new_kirby;
      new_kirby->parent_kirby = now;
      return;
    }
    now = now->child_kirby;
  }
  ++kirby_num;
}


struct kirby* get_ix_kirby(int ix)
{
  struct kirby *now = &kingkirby;
  for(int jx=0;ix!=jx;++jx,now=now->child_kirby){
    if(now==NULL) return NULL;
  }
  return now;
}

void delete_list(int ix)
{
  struct kirby *target = get_ix_kirby(ix);
  target->parent_kirby->child_kirby = target->child_kirby;
  if(target->child_kirby!=NULL){
    target->child_kirby->parent_kirby = target->parent_kirby;
  }
  free(target->name);
  free(target);
}

void inhale(int type){
  int inp;
  if(kirby_num==MAXKIRBY){
    printf("You can't inhale kirby more!\n");
    return;
  }

  struct kirby *new_kirby = malloc(sizeof(struct kirby));
  ++kirby_num;
  memset(new_kirby,0,sizeof(struct kirby));
  if(type==2){
    printf("How big is this BIG kirby?(0x50<=) > ");
    new_kirby->bufsize = getint();
  }else{
    new_kirby->bufsize = type==0?NORMALBUF:SMALLBUF;
  }
  new_kirby->name = malloc(new_kirby->bufsize);
  if(type==2 && new_kirby->bufsize<NORMALBUF)
    new_kirby->bufsize=1;
  printf("Name him! > ");
  if(new_kirby->bufsize!=1){
    if(read(0,new_kirby->name,NORMALBUF)<=0){
      printf("BYE\n");
      exit(1);
    }
  }else if(read(0,new_kirby->name,new_kirby->bufsize)<=0){
      printf("BYE\n");
      exit(1);
  }
  //new_kirby->name[new_kirby->bufsize-1] = NULL;
  
  put_back(new_kirby);
}

void kirby(int type){
  printf("What do you do?\n");
  printf("1:Inhale\n2:Kill\n3:Escape\n");
  while(1==1){
    printf("> ");
    switch(getint()){
      case 1:
        printf("You inhaled ");
        if(type==0) printf("kirby!\n");
        if(type==1) printf("smallkirby!\n");
        if(type==2) printf("BIG kirby!\n");
        inhale(type);
        return;
      case 2:
        printf("Kirby die.\n");
        return;
      case 3:
        printf("Kirby killed kingkirby.\n");
        exit(1);
      default:
        printf("Invalid input\n");
        continue;
    }
  }
}

void walk(void)
{
  ++total_walk;
  printf("walking in the sky");
  if(is_debug==1) sleep(1);
  printf(".");
  if(is_debug==1) sleep(1);
  printf(".");
  if(is_debug==1) sleep(1);
  printf(".");
  if(is_debug==1) sleep(1);
  
  if(total_walk%0xa==0){
    printf("you find BIG kirby!\n");
    kirby(2);
  }else if(total_walk%6==0){
    printf("you find smallkirby!\n");
    kirby(1);
  }else{
    printf("you find kirby!\n");
    kirby(0);
  }
  printf("\n");
}

void list(void){
  struct kirby *now_kirby = &kingkirby;

  for(int ix=0;;++ix){
    printf("%d: %s ",ix,now_kirby->name);
    if(now_kirby->parent_kirby!=NULL){
      printf("in %s",now_kirby->parent_kirby->name);
    }
    printf("\n");
    if(now_kirby->child_kirby==NULL){
      break;
    }
    now_kirby = now_kirby->child_kirby;
  }
  printf("\n\n");
}

void kill(void){
  int inp = 0;
  
  printf("You kill kirby for your free");
  sleep(1);
  printf(".");
  sleep(1);
  printf(".");
  sleep(1);
  printf(".");
  sleep(1);

  if(kirby_is_free==0){
    printf("No!!!\n\n");
    return;
  }else{
    list();
    printf("Which kirby do you want to kill?\n> ");
    while(1==1){
      if((inp = getint())<=0){
        printf("you can't\n");
        continue;
      }
      delete_list(inp);
      printf("you killed %d\n",inp);
      return;
    }
  }
  printf("\n\n");
}

void rename_kirby(void)
{
  int inp=0;
  struct kirby *target;

  list();
  printf("Which kirby do you wanna rename? > ");
  inp = getint();
  if(inp<=0 || kirby_num-1<inp){
    printf("Invalid\n");
    return;
  }
  target = get_ix_kirby(inp);
  printf("new name > ");
  if(target->bufsize!=1)
    read(0,target->name,NORMALBUF);
  else
    read(0,target->name,target->bufsize);
}

void main_loop(void)
{
  int inp = 0;
  
  while(1==1){
    print_menu();
    printf("> ");
    switch(getint()){
      case 1:
        walk();
        break;
      case 2:
        list();
        break;
      case 3:
        kill();
        break;
      case 4:
        rename_kirby();
        break;
      case 0:
        if(is_exitable==1){
          printf("See you!\n");
          return;
        }else{
          printf("No! I want you not to exit!!\n\n");
          break;
        }
      default:
        printf("Invalid input\n");
        continue;
    }
  }
  return;
}


int main(int argc,char *argv[])
{

  setvbuf(stdout,NULL,_IONBF,0);
  setvbuf(stdin,NULL,_IONBF,0);

  memset(&kingkirby,0,sizeof(struct kirby));
  kingkirby.bufsize = NORMALBUF;
  kingkirby.name = malloc(NORMALBUF);
  memcpy(kingkirby.name,"kingkirby",10);
  kirby_num = 1;

  main_loop();
  
  return 0;
}

