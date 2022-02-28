
/*************************************
//Ah... h,,,hello...?
//I am a bot of EEIC and tell them a...
//Sorry, I'm so shy. 
**************************************/

#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<string.h>

#define MAX_SCHEDULE 100
#define BUF_SIZE 0x200

char **schedules=NULL;
int num_schedule=0;

void introduce(void)
{
  printf("~~~~~~~~~~~~~~~~~___(((((((-_~__~~~~~~~~~~~~~~~~~~\n\
~~~~~~~~~~~~~~~~_(+uOOOOOOOOw&+-~~~~~~~~~~~~~~~~~~\n\
~~.~.~.~~~~~~~_(+wZOOwwOOOwwOOXO+_.~~~~~~~.~.~.~.~\n\
~~~~~~~~~~~~~~~_~<zwOv1OlvzzwOv<~_~~~~~~~~~~~~~~~~\n\
~.~~.~~~~~~~~~~~~~~<1wwOlzwZ<<~~~~~~~~~~~~~.~~.~~~\n\
~~~.~~.~~~~~~~~~~~~~~<+zwO<<~~~~~~~~~~~~~~.~~~~.~~\n\
~~~~~~~~~.~~~~~~~~~.(+dHgH0z~.~~~~~~~~~~~~~~~.~~~.\n\
~.~~~~~~~~~~~~~~~~~~_<OWHWC<_~~~~~~~~~~~~~~~~~~~~~\n\
~~~~~~~~~~~~~~~~~~~~_.(wuI< _~~~~~~~~~~~~~~~~~~~.~\n\
~~~~.~~~~~~_-------_--jXfk+-_-------__~~~~~.~~~~~~\n\
~~~~~~~~~(juwAAAAAAAAwXpbWkAAAAAAAAAA&+_~~~~~~~~~~\n\
~~~~~~._+zXkHHbbHppbbbppfppbppppHbbHHqkO<.~~~~~.~~\n\
~~~~~~~_jXWkpfppffpfffffpffpffpffppfpkW0>.~~~~~~~~\n\
~~~~~~._jXWkpfppfpfpfpfpffpfpffpfpffpkW0>.~~~~~~~.\n\
~~~~~~.-jXWkfpfpffpfpfpfffpffpffpppfpkW0>.~~~~~~~~\n\
~~~~~~.-+XWbffffffffffffffffffffffffpbW0>.~~~~~~~~\n\
~~~~~~.-+XWkfppfpffffffffpffffpffpffpbW0>.~~~~~~~.\n\
~~~.~~.-jXWbfffpfffpffpffffpffffpfpfpbW0>.~~~~~~~~\n\
~~~~~~~-jXWkffpffppfppfppfpfppfffpffpkW0>.~~~~~~~~\n\
~~~~~~~_jXWbppppfffffffpffpfffppfppfpkW0>.~~~~~~~.\n\
~~~~~~._jXWbfffpffppppffpffppfffpfpfpkW0>.~~~~~~~~\n\
~~~~~~~_+wWHWbbbbbpffffffpfffpbbWbbWWHKZ<.~~~~~~~~\n\
~~~~~~~~_<zUUUUUUWfWWpppppppWWXUUUUUUVC<~~~~~~~~~~\n\
~~~~~~~~~~~~<<<~(dHMMMMMMMMMMH0<~~<<<<~~~~~~~~~~~~\n\
~~~.~.~.~~..._-(dWMM@@@@@@@@MMNk+--.~.~.~~.~~~~~~~\n\
__((+++++zzzzwXHHMHH@HHHHHHH@HMHNkkwzzzz&&+++---__\n\
XXWWWkkkkbkkkkppWWbbHHHHHHkkkHWpppbbbbkkkkkbbWWkkk\n\
bpppfppffffffppfffffffffffffffffffpffffffffpfppppb\n\
ffpffffppfppffffpfppfppfpfpfpfpffpfpfpfpfpffpffffp\n\
pffpffffffffffffffffffffffffffffffffffffffffffpfpf\n\n\n");

  printf("Ah, h,hello...?\n");
  printf("M, my name is ... is ... EEICtan.\n");
  printf("Eh... I'm a bot of EEIC, ah... in Univ. of Tokyo...\n");
  printf("\n");
  printf("Sorry. I AM SO SHY...\n\n\n");
}

void printmenu(void)
{
  printf("Eh... what, what do you want ...?\n");
  printf("1: Add Schedule\n");
  printf("2: Remove Schedule\n");
  printf("3: List Schedule\n");
  printf("4: Edit Schedule\n");
  printf("0: Exit\n");
  printf("> ");
}

int getint(void)
{
  int num;
  if(fscanf(stdin,"%d",&num)!=1){
    printf("BYE\n");
    exit(1);
  }
  getchar();
  return num;
}

void _add(void){
  ++num_schedule;
  schedules[num_schedule-1] = malloc(BUF_SIZE);
  printf("Ah, i...input schedule...\n");
  printf(">");
  read(0,schedules[num_schedule-1],BUF_SIZE-1);
  schedules[num_schedule-1][BUF_SIZE-1] = '\0';
  printf("\n\n");
}

void _list(void)
{
  printf("Eh, %d schedules are set...\n",num_schedule);
  printf("1st schedule is:\n");
  if(schedules!=NULL){
    for(int ix=0;ix!=8;++ix){
      printf("%c",schedules[0][ix]);
    }
    printf(" ...\n");
  }
  printf("\nS, sorry. I can't say anymore.\nI AM SO SHY...\n\n");
}

void _remove(void)
{
  int inp;
  printf("\nEh, %d schedules are set...\n",num_schedule);
  printf("Please enter the index(zero origin) > ");
  
  inp = getint();
  if(0<=inp && inp<=num_schedule-1){
    free(schedules[inp]);
    printf("D, deleted...\n\n");
    return;
  }else{
    printf("invalid index\n\n");
    return;
  }
}

void _edit(void)
{
  int inp;
  printf("\nEh, %d schedules are set...\n",num_schedule);
  printf("Please enter the index(zero origin) > ");

  inp = getint();
  if(0<=inp && inp<=num_schedule-1){
    printf("I, input data...\n");
    printf(">");
    read(0,schedules[inp],BUF_SIZE-1);
    schedules[inp][BUF_SIZE-1] = '\0';
    printf("\n\n");
    return;
  }else{
    printf("invalid index\n\n");
    return;
  }

}

void mainloop(void)
{
  int inp;
  while(1==1){
    printmenu();
    inp = getint();
    switch(inp){
      case 1:
        _add();
        break;
      case 2:
        _remove();
        break;
      case 3:
        _list();
        break;
      case 4:
        _edit();
        break;
      case 0:
        printf("\n\nS, see you in EEIC...\n\n");
        exit(0);
      default:
        printf("invalid input\n\n");
        break;
    }
  }
}


int main(int argc,char *argv[])
{
  setvbuf(stdout,NULL,_IONBF,0);
  setvbuf(stdin,NULL,_IONBF,0);
  schedules = malloc(sizeof(char*)*MAX_SCHEDULE);
  
  introduce();
  mainloop();
  
  return 0;
}

