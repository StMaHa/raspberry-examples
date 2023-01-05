CC = gcc
CFLAGS = -Wall
LDFLAGS = -lpigpio
SRC = led_blink_pigpio.c
BIN = led_blink_pigpio

$(BIN): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $@ $(LDFLAGS)
	chmod 777 $(BIN)

clean:
	rm -f *.o $(BIN)
