#include <stdio.h>
#include <time.h>

int main(int argc, char* argv[]) {
    int seed = time(0) + atoi(argv[1]);
    srand(seed);
    printf("%d\n", rand());
}
