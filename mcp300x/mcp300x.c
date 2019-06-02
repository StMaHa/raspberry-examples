#include "mcp300x.h"
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <linux/spi/spidev.h>


/*
 * Initilise ADC
 */
int adc_init(char *device) {
    unsigned char spi_mode = SPI_MODE;
    unsigned char spi_bits = SPI_BITS_PER_WORD;
    unsigned long spi_clock = SPI_CLOCK;

    int fd_adc = open(device, O_RDWR);

    if (fd_adc <= 0) {
        perror("Can't connect to device");
        return -1;
    }
    if (ioctl(fd_adc, SPI_IOC_WR_MODE, &spi_mode) == -1) {
        perror("Can't set MODE");
        return -1;
    }
    if (ioctl(fd_adc, SPI_IOC_WR_BITS_PER_WORD, &spi_bits) == -1) {
        perror("Can't set number of BITS");
        return -1;
    }
    if (ioctl(fd_adc, SPI_IOC_WR_MAX_SPEED_HZ, &spi_clock) == -1) {
        perror("Can't set write CLOCK");
        return -1;
    }
    if (ioctl(fd_adc, SPI_IOC_RD_MAX_SPEED_HZ, &spi_clock) == -1) {
        perror("Can't set read CLOCK");
        return -1;
     }
     return fd_adc;
}

/*
 * Return control bits depending on mode (differential or single)
 */ 
uint8_t get_control_bits(uint8_t channel, bool is_diff) {
    if(is_diff)
        return (channel & 0x7) << 4;
    else
        return (0x8 | (channel & 0x7)) << 4;
}

/*
 *  Returns the ADC value for the given channel.
 */
int adc_read(int fd_adc, uint8_t channel) {
    uint8_t tx[] = {1, get_control_bits(channel, false), 0};
    uint8_t rx[3];

    struct spi_ioc_transfer spi_transfer = {
        .tx_buf = (unsigned long)tx,
        .rx_buf = (unsigned long)rx,
        .len = sizeof(tx) / sizeof(tx[0]),
        .delay_usecs = SPI_DELAY,
        .speed_hz = SPI_CLOCK,
        .bits_per_word = SPI_BITS_PER_WORD,
    };

    if (ioctl(fd_adc, SPI_IOC_MESSAGE(1), &spi_transfer) == 1) {
        perror("Can't read from ADC");
        abort();
    }
    return ((rx[1] << 8) & 0x300) | (rx[2] & 0xFF);
}
