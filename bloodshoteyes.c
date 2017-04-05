#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

void main(int argc, char *argv[]) {

    if (argc !=3) { // finish input filtering part
        printf("Usage: %s <mins to work> <mins to rest>\n", argv[0]);
        exit(0);
    }
    
    int worktime, breaktime;
    worktime = atoi(argv[1]);
    breaktime = atoi(argv[2]);

    time_t rawtime;
    struct tm * timeinfo;

    time(&rawtime);
    timeinfo = localtime(&rawtime);
    printf("Starting at %s\n", asctime(timeinfo));

    while(1) {
        sleep(60*worktime);
        printf("Go get some rest now.\n");
        sleep(60*breaktime);
        printf("Ok, now back to work.\n");
    }
}
