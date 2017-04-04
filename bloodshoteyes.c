#include <stdio.h>
#include <stdlib.h>

void usage();

void main(int argc, char *argv[]) {

    int worktime, breaktime;
    // put input filtering and usage here
    worktime = atoi(argv[1]);
    breaktime = atoi(argv[2]);
    printf("[DEBUG] worktime: %d\n", worktime);
    printf("[DEBUG] breaktime: %d\n", breaktime);
    // сделать цвет полоски применяемым
}
