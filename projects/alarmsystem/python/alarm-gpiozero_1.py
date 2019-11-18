#!/usr/bin/python
# Example and exercise to build a alarm system
# First exercise
from gpiozero import MotionSensor, Buzzer
from lcd_i2c_lib import lcd as LCD
from keypad_mcp3008 import PinPad
import os
import time

expected_pin = "1234"

PIN_PIR = 23
PIN_BUZ = 21

is_alarm = False             # kein Alarm / Alarm ausgeloest
is_alarm_enabled = False     # Alarmanalge ein-/ausgeschaltet
alarm_aktive_delay = 5       # Verzoegerung bis Alarmanalge eingeschaltet

pin_pad = PinPad()           # Initialisierung der Key-Pad-Matrix
buz = Buzzer(PIN_BUZ)        # Initialisierung des Summers
lcd = LCD()                  # Initialisierung des Displays
pir = MotionSensor(PIN_PIR)  # Initialisierung des Bewegungssensors

# Callback Funktion zum Ausloesen des Alams
def callback_alarm(channel):
    global is_alarm
    if is_alarm_enabled:  # nur Alarm ausloesen, wenn Anlage aktiv
        print("A L A R M")
        is_alarm = True

# Funktion zur ueberpruefung der Pin
#  - wenn Pin korrekt, Funktion gibt 'True' zurück
#  - wenn abgebrochen, Funktion gibt 'False' zurück
def verify_pin():
    pin_verified = False
    entered_pin = ""
    while True:  # Endlosschleife, Abbruch durch erfolgreiche Pineingabe oder '*'
        lcd.lcd_write_line("Enter pin:      ", 2)
        entered_pin = pin_pad.get_pin(debug=True)  # Hole Pin von Pinpad
        if expected_pin == entered_pin:            # Vergleich Istpin mit Sollpin
            print("Pin ist korrekt")
            pin_verified = True                    # Pinvergelich ist erfolgreich
            break
        else:
            print("Pin ist falsch")
        if pin_pad.is_key_pressed('*'):            # Pineingabe wird abgebrochen
            print("Pineingabe abgebrochen")
            break
    print("Pinverifikation: ".format(str(pin_verified)))
    return(pin_verified)                           # Rueckgabe ob Pinvergleich erfolgreich war

# Funktion fuer ein Menue, um die Alarmanlage ein-/auszuschalten
def menu():
    global is_alarm_enabled
    lcd.lcd_clear()
    lcd.lcd_write_line("1 Alarm aus", 1)
    lcd.lcd_write_line("2 Alarm ein", 2)
    while True:  # Endlosschleife, Abbruch durch erfolgreiche Menueeingabe oder '*'
        if pin_pad.is_key_pressed('*'):  # druecke '*', um das Menue zu verlassen
            break
        if pin_pad.is_key_pressed('1'):	 # druecke '1', um die Alarmanlage auszuschalten
            lcd.lcd_write_line("Alarmanlage aus", 1)
            if verify_pin():             # um auszuschalten ist eine Pin erforderlich
                lcd.lcd_clear()
                lcd.lcd_write_line("  Alarm aus", 1)
                is_alarm_enabled = False
                break
        if pin_pad.is_key_pressed('2'):  # druecke '2', um die Alarmanlage einzuschalten
            lcd.lcd_write_line("Alarmanlage ein", 1)
            if verify_pin():             # um einzuschalten ist eine Pin erforderlich
                lcd.lcd_clear()
                lcd.lcd_write_line("  Alarm aktiv", 1)
                time.sleep(alarm_aktive_delay)
                is_alarm_enabled = True
                break
    lcd.lcd_write_line("* > Menue", 2)

# Funktion zur Alarmgebung
def alarm():
    global is_alarm
    global is_alarm_enabled
    buz.on()  # Summer an
    lcd.lcd_clear()
    lcd.lcd_write_line("   A L A R M", 1)
    lcd.lcd_write_line("* > ausschalten", 2)
    shell_stdout = os.popen('take_picture.sh').read()  # Erzeuge Bild (und sende Bild)
    print("Take picture: ", shell_stdout)
    while True:  # Endlosschleife, Abbruch durch erfolgreiche Pineingabe
        while True:  # Endlosschleife, Abbruch durch '*'
            if pin_pad.is_key_pressed('*'):
                break
        if verify_pin():
            break
    is_alarm = False          # Alarm aus
    is_alarm_enabled = False  # Alarmanlage aus
    buz.off()                 # Summer aus

# Hauptfunktion
try:
    pir.when_motion = callback_alarm
    lcd.lcd_write_line("Alarmanlage", 1)
    lcd.lcd_write_line("* > Menu", 2)
    while True:  # Endlosschleife, Abbruch durch [Strg]+[c], Programmabbruch
        # Programm wartet auf Alarm oder Key-Pad-Eingabe
        if is_alarm:
            alarm()
        if pin_pad.is_key_pressed('*'):
            menu()
except KeyboardInterrupt:
    pin_pad.close()
    print("Programm 'Alarm' beendet.")
