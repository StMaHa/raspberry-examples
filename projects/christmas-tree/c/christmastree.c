#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>

#define	LED_ON	1
#define LED_OFF	0

//                       1 2 3  4  5  6  7  8  9 10 11
//         led_list[] = {3,5,7,11,13,15,12,16,18,22,24};
static int led_list[] = {8,9,7, 0, 2, 3, 1, 4, 5, 6,10};
static int led_middle_list[] = {8, 0, 1, 4, 6};
static int led_left_list[] = {9, 2, 5};
static int led_right_list[] = {7, 3, 10};

int SIZE_OF_INT = sizeof(int);

int rndgen(int min, int max) {
  srand ( time(NULL) );
  return (rand() % (1 + max - min));
}

void SequenceWobble(int status, int delay_time) {
  int i;
  for(i=0;i<=6;i++) { 
    digitalWrite(led_list[i], status);
    digitalWrite(led_list[sizeof(led_list)/SIZE_OF_INT-1-i], status);
    delay(delay_time);
  }
}

void SwitchAllLeds(int status) {
  int led_pin;
  for(led_pin=0;led_pin<sizeof(led_list)/SIZE_OF_INT;led_pin++) {
    digitalWrite(led_list[led_pin], status);
  }
}

void BlinkAllLeds(int delay_time) {
  int led_pin;
  for(led_pin=0;led_pin<sizeof(led_list)/SIZE_OF_INT;led_pin++) {
    digitalWrite(led_list[led_pin], LED_OFF);
  }
  delay(delay_time);
  for(led_pin=0;led_pin<sizeof(led_list)/SIZE_OF_INT;led_pin++) {
    digitalWrite(led_list[led_pin], LED_ON);
  }
  delay(delay_time);
}

void SequenceUpDown(int status, int delay_time) {
  int led_pin;
  for(led_pin=0;led_pin<sizeof(led_list)/SIZE_OF_INT;led_pin++) { 
    digitalWrite(led_list[led_pin], status);
    delay(delay_time);
  }
}

void SequenceCircle(int status, int delay_time) {
  int led_pin;
  digitalWrite(led_middle_list[0], status);
  delay(delay_time);
  for(led_pin=0;led_pin<sizeof(led_right_list)/SIZE_OF_INT;led_pin++) {
    digitalWrite(led_right_list[led_pin], status);
    delay(delay_time);
  }
  digitalWrite(led_middle_list[sizeof(led_middle_list)/SIZE_OF_INT-1], status);
  delay(delay_time);
  for(led_pin = sizeof(led_left_list)/SIZE_OF_INT-1; led_pin >= 0; led_pin--) {
    digitalWrite(led_left_list[led_pin], status);
    delay(delay_time);
  }
}

void SwitchMiddleLed(int status) {
  int led_pin;
  for(led_pin=0;led_pin<sizeof(led_middle_list)/SIZE_OF_INT;led_pin++) {
    digitalWrite(led_middle_list[led_pin], status);
  }
}

void SwitchSurroundLed(int status) {
  int led_pin;
  for(led_pin=0;led_pin<sizeof(led_right_list)/SIZE_OF_INT;led_pin++) {
    digitalWrite(led_right_list[led_pin], status);
  }
  for(led_pin=0;led_pin<sizeof(led_left_list)/SIZE_OF_INT;led_pin++) {
    digitalWrite(led_left_list[led_pin], status);
  }
}

void SequenceCircleLeft(int status, int delay_time) {
  int led_pin;
  digitalWrite(led_middle_list[0], status);
  delay(delay_time);
  for(led_pin = 0; led_pin < sizeof(led_left_list)/SIZE_OF_INT; led_pin++) {
    digitalWrite(led_left_list[led_pin], status);
    delay(delay_time);
  }
  digitalWrite(led_middle_list[sizeof(led_middle_list)/SIZE_OF_INT-1], status);
  delay(delay_time);
  for(led_pin = sizeof(led_right_list)/SIZE_OF_INT-1; led_pin >= 0; led_pin--) {
    digitalWrite(led_right_list[led_pin], status);
    delay(delay_time);
  }
}

void SequenceDownUp(int status, int delay_time) {
  int led_pin;
  for(led_pin = sizeof(led_list)/SIZE_OF_INT-1; led_pin >= 0; led_pin--) {
    digitalWrite(led_list[led_pin], status);
    delay(delay_time);
  }
}

void SwitchRandomLed(int status, int delay_time) {
  digitalWrite(led_list[rndgen(0 ,sizeof(led_list)/SIZE_OF_INT-1)], status);
  delay(delay_time);
}

void BlinkRandomLed(int delay_time) {
  int led_pin = led_list[rndgen(0 , sizeof(led_list)/SIZE_OF_INT-1)];
  digitalWrite(led_list[led_pin], LED_OFF);
  delay(delay_time);
  digitalWrite(led_list[led_pin], LED_ON);
  delay(delay_time);
}

void main(void) {
	int delay_time=1000;

	wiringPiSetup();

	// Alle Pins auf Output setzen
	int led_pin;
	for(led_pin=0;led_pin<sizeof(led_list)/SIZE_OF_INT;led_pin++) {
	  printf("Setup pin: %d\n", led_pin);
	  pinMode(led_pin, OUTPUT);
	}

	printf("Es werden %d leds geschaltet!\n", sizeof(led_list)/SIZE_OF_INT);

	while(1) {
	  int i;
          int a;
	  // LED an und aus
	  SwitchAllLeds(LED_ON);
	  int nWait = 300;
	  for(i=0;i<=10;i++) {
		SwitchMiddleLed(LED_ON);
		SwitchSurroundLed(LED_OFF);
		delay(nWait);
		SwitchMiddleLed(LED_OFF);
		SwitchSurroundLed(LED_ON);
		delay(nWait);
	  }
	  SwitchAllLeds(LED_ON);
	  for(i=0;i<=10;i++) {
		SequenceCircle(LED_OFF, 100);
		SequenceCircle(LED_ON, 100);
	  }
          SwitchAllLeds(LED_ON);
	  for(i=0;i<=10;i++) {
		SequenceUpDown(LED_OFF, 100);
		SequenceDownUp(LED_ON, 100);
	  }
	  for(i=0;i<=10;i++) {
		SwitchMiddleLed(LED_OFF);
		delay(200);
		SwitchMiddleLed(LED_ON);
	  	delay(200);
	  }
	  for(i=0;i<=1;i++) {
		SwitchAllLeds(LED_ON);
		SequenceWobble(LED_OFF, 300);
	  }
	  for(i=0;i<=3;i++) {
		SwitchAllLeds(LED_ON);
	  }
	  for(i=0;i<=4;i++) {
		BlinkAllLeds(300);
	  }
          SwitchAllLeds(LED_ON);
	  for(i=0;i<=5;i++) {
		SequenceCircleLeft(LED_OFF, 200);
		SequenceCircleLeft(LED_ON, 200);
	  }
	  SwitchAllLeds(LED_ON);
	  for(i=0;i<=8;i++) {
		SequenceDownUp(LED_OFF, 100);
		SequenceUpDown(LED_ON, 100);
	  }
	  for(i=0;i<=5;i++) {
		SwitchAllLeds(LED_ON);
		SwitchRandomLed(LED_OFF, 300);
	  }
	  for(i=0;i<=5;i++) {
		BlinkRandomLed(300);
	  }
  }
  return ;
}

