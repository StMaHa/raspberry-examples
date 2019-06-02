#include "mcp300x.h"
#include <stdio.h>
#include <unistd.h>


int main(int argc, char **argv) {
    int fd = adc_init("/dev/spidev0.0");

    while(1) {
        for(int i = 0;i < 8;i++) {
            printf("%04d  ", adc_read(fd, i));
        }
        printf("\n");
        sleep(1);
    }
    close(fd);
    return 0;
}
