import time 
import RPi.GPIO as GPIO 
import random 

def SequenceWobble(status, delay):
  for i in range(0, 6):
    GPIO.output(led_list[i], status)
    GPIO.output(led_list[len(led_list)-1-i], status)
    time.sleep(delay)
   
def SwitchAllLeds(status):
  for led_pin in led_list:
    GPIO.output(led_pin, status)

def BlinkAllLeds(delay):
  for led_pin in led_list:
    GPIO.output(led_pin, GPIO.LOW)
  time.sleep(delay)
  for led_pin in led_list:
    GPIO.output(led_pin, GPIO.HIGH)
  time.sleep(delay)

def SequenceUpDown(status, delay):
  for led_pin in led_list:
    GPIO.output(led_pin, status)
    time.sleep(delay)

def SequenceCircle(status, delay):
  GPIO.output(led_middle_list[0], status)
  time.sleep(delay)
  for led_pin in led_right_list:
    GPIO.output(led_pin, status)
    time.sleep(delay)
  GPIO.output(led_middle_list[len(led_middle_list)-1], status)
  time.sleep(delay)
  for led_pin in reversed(led_left_list):
    GPIO.output(led_pin, status)
    time.sleep(delay)

def BlinkMiddleLed(status, delay):
  for led_pin in led_middle_list:
    GPIO.output(led_pin, status)
  time.sleep(delay)
    
def SequenceCircleLeft(status, delay):
  GPIO.output(led_middle_list[0], status)
  time.sleep(delay)
  for led_pin in led_left_list:
    GPIO.output(led_pin, status)
    time.sleep(delay)
  GPIO.output(led_middle_list[len(led_middle_list)-1], status)
  time.sleep(delay)
  for led_pin in reversed(led_right_list):
    GPIO.output(led_pin, status)
    time.sleep(delay)

def SequenceDownUp(status,delay):
  for led_pin in reversed(led_list):
    GPIO.output(led_pin, status)
    time.sleep(delay)

def SwitchRandomLed(status,delay):
  GPIO.output(led_list[random.randrange(0 ,len(led_list)-1)], status)
  time.sleep(delay)
    
def BlinkRandomLed(delay):
  led_pin = led_list[random.randrange(0 , len(led_list))]
  GPIO.output(led_pin, GPIO.LOW)
  time.sleep(delay)
  GPIO.output(led_pin, GPIO.HIGH)
  time.sleep(delay)
    
#           1 2 3 4 5 6 7 8 9 10 11
#led_list = [3,5,7,11,13,15,12,16,18,22,24]
led_list = [19,21,23,11,13,15,12,16,18,22,24]
led_middle_list = [3, 11, 12, 16, 22]
led_left_list = [5, 13, 18]
led_right_list = [7, 15, 24] 
ledOn = GPIO.HIGH
ledOff = GPIO.LOW
 
GPIO.setwarnings(False)

# RPi.GPIO Layout verwenden (wie Pin-Nummern)
GPIO.setmode(GPIO.BOARD)

# Alle Pins auf Output setzen
for led_pin in led_list:
  print "Setup pin: ", led_pin
  GPIO.setup(led_pin, GPIO.OUT)
  delay=1
  print "Es werden ", len(led_list), "leds geschaltet!"
  i = 0
  while True:
    # LED an und aus
    SwitchAllLeds(ledOn)
    for i in range(0, 10):
      BlinkMiddleLed(ledOff, 0.3)
      BlinkMiddleLed(ledOn, 0.3)
    for i in range(0, 1):
      SwitchAllLeds(ledOn)
      SequenceWobble(ledOff, 0.3)
    for i in range(0, 3):
      SwitchAllLeds(ledOn)
    for i in range(0, 4):
      BlinkAllLeds(0.3)
    for i in range(0, 4):
      SwitchAllLeds(ledOn)
      SequenceUpDown(ledOff, 0.3)
    for i in range(0, 3):
      SwitchAllLeds(ledOn)
      SequenceCircle(ledOff, 0.3)
    for i in range(0, 3):
      SwitchAllLeds(ledOn)
      SequenceCircleLeft(ledOff, 0.3)
    for i in range(0, 4):
      SwitchAllLeds(ledOn)
      SequenceDownUp(ledOff, 0.3)
    for i in range(0, 5):
      SwitchAllLeds(ledOn)
      SwitchRandomLed(ledOff, 0.3)
    for i in range(0, 3):
      BlinkRandomLed(0.3)

GPIO.cleanup()
exit()
