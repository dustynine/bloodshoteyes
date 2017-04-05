#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void main(int argc, char *argv[]) {
    
    if (argc !=3) { // finish input filtering part
        printf("Usage: %s <mins to work> <mins to rest>\n", argv[0]);
        exit(0);
    }
    
    int worktime, breaktime;
    worktime = atoi(argv[1]);
    breaktime = atoi(argv[2]);

    time_t time_till = clock();
    printf("%ld", (long) time_till);
    // usleep() ???
}
