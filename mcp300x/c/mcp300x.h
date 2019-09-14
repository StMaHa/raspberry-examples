#ifndef MCP300X_H
#define MCP300X_H

#include <stdint.h>

#define SPI_MODE          SPI_MODE_0
#define SPI_CLOCK         1000000
#define SPI_DELAY         5
#define SPI_BITS_PER_WORD 8

// Functions
int adc_init();
int adc_read(int fd_adc, uint8_t channel);

#endif
