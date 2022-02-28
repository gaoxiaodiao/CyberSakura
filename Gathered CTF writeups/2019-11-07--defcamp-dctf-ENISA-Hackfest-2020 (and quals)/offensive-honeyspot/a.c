#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[], char* envp[])
{
int seed = time(NULL);
printf("seed=%lld\n", seed);
srand(seed);
for (int i = 0; i <900;i++)
{
printf("%d", rand() &3);
}
}
