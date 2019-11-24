#!/usr/bin/python
# Example and exercise to build a alarm system
# First exercise
from gpiozero import MotionSensor, Buzzer
from lcd_i2c_lib import lcd as LCD
from keypad_mcp3008 import PinPad
import os
import time

# Konstanten
PIN_PIR = 23
PIN_BUZ = 21

# Globale Variablen
expected_pin = "1234"
is_alarm = False             # kein Alarm / Alarm ausgeloest
is_alarm_enabled = False     # Alarmanalge ein-/ausgeschaltet
alarm_aktive_delay = 5       # Verzoegerung bis Alarmanalge eingeschaltet

# +++ 1) +++ # Globale Instanzen
pin_pad = PinPad()           # Initialisierung der Key-Pad-Matrix
buz = Buzzer(PIN_BUZ)        # Initialisierung des Summers
lcd = LCD()                  # Initialisierung des Displays
pir = MotionSensor(PIN_PIR)  # Initialisierung des Bewegungssensors

# Callback Funktion zum Ausloesen des Alams
def callback_alarm(channel):
    global is_alarm
    # nur Alarm ausloesen, wenn Anlage aktiv und Alarm noch nicht ausgeloest
    if (not is_alarm) and is_alarm_enabled:
        print("A L A R M")
        # +++ 3) +++ Merke Alarm ausgeloest
        is_alarm = True
        # +++ 3) +++ Summer an
        buz.on()
        # +++ 3) +++ Erzeuge Bild und evtl. sende Bild (shell script ausfuehren)
        shell_stdout = os.popen('./take_picture.sh').read()
        print("Take picture: ", shell_stdout)
        # Erzeuge Bild (und sende Bild)
        lcd.lcd_clear()
        lcd.lcd_write_line("   A L A R M", 1)
        lcd.lcd_write_line("* > ausschalten", 2)

# Funktion zur ueberpruefung der Pin
#  - wenn Pin korrekt, Funktion gibt 'True' zurueck
#  - wenn abgebrochen, Funktion gibt 'False' zurueck
def verify_pin():
    # Anfangswerte
    pin_verified = False
    entered_pin = ""
    while True:  # Endlosschleife, warte auf erfolgreiche Pineingabe oder '*'
        lcd.lcd_write_line("Enter pin:      ", 2)
        # +++ 2) +++ Hole Pin von Pinpad
        entered_pin = pin_pad.get_pin(debug=True)  # Hole Pin von Pinpad, Abbruch der Eingabe mit '*' 
        if not entered_pin:                        # Pineingabe wurde abgebrochen
            print("Pineingabe abgebrochen")
            break
        # +++ 2) +++ Vergleiche Ist-Pin mit Soll-Pin
        if expected_pin == entered_pin:
            print("Pin ist korrekt") # Schreibe Kommentar auf die Konsole (nicht display)          
            pin_verified = True      # Pinvergleich ist erfolgreich
            break                    # dann Warteschleifen beenden
        else:
            lcd.lcd_write_line("Pin ist falsch!", 2)
            print("Pin ist falsch")
            time.sleep(2)
    print("Pinverifikation: ".format(str(pin_verified)))
    return(pin_verified)                           # Rueckgabe ob Pinvergleich erfolgreich war

# Funktion fuer ein Menue, um die Alarmanlage ein-/auszuschalten
def menu():
    global is_alarm_enabled
    # Show actual state of the alarmsystem
    lcd.lcd_clear()
    if is_alarm_enabled:
        lcd.lcd_write_line("  Alarm aktiv", 1)
    else:
        lcd.lcd_write_line("  Alarm aus", 1)
    lcd.lcd_write_line("* > Menue", 2)
    while True:  # Endlosschleife, warte auf Taste '*' gedrueckt
        if is_alarm:  # Beende diese Funktion
            break
        if pin_pad.is_key_pressed('*'):  # druecke '*', um das Menue zu zeigen
            break
    # Schreibe das Menue aufs Display
    lcd.lcd_clear()
    lcd.lcd_write_line("1 Alarm aus", 1)
    lcd.lcd_write_line("2 Alarm ein", 2)
    while True:  # Endlosschleife, warte auf erfolgreiche Menueeingabe oder Taste '*'
        if is_alarm:  # Beende diese Funktion
            break
        # +++ 2) +++ Beende die Schleife wenn Taste '*' gedrueckt wurde
        if pin_pad.is_key_pressed('*'):  # Taste '*' beendet das Menue
            break
        if pin_pad.is_key_pressed('1'):	 # druecke '1', um die Alarmanlage auszuschalten
            lcd.lcd_write_line("Alarmanlage aus", 1)
            if verify_pin():             # um auszuschalten ist eine Pin erforderlich
                lcd.lcd_clear()
                lcd.lcd_write_line("  Alarm aus", 1)
                # +++ 2) +++ Setze Alarmsystem auf aus/deaktiviert (False)
                is_alarm_enabled = False
                break
        if pin_pad.is_key_pressed('2'):  # druecke '2', um die Alarmanlage einzuschalten
            lcd.lcd_write_line("Alarmanlage ein", 1)
            if verify_pin():             # um einzuschalten ist eine Pin erforderlich
                lcd.lcd_clear()
                lcd.lcd_write_line("  Alarm aktiv", 1)
                # +++ 2) +++ Verzoegere die Aktivierung des Alarms
                #  (Zeit um das Umfeld des Sensors zu verlassen)
                time.sleep(alarm_aktive_delay)
                # +++ 2) +++ Setze Alarmsystem auf ein/aktiviert (True)
                is_alarm_enabled = True
                break

# Funktion zur Alarmgebung
def alarm():
    global is_alarm
    global is_alarm_enabled
    while True:  # Endlosschleife, warte auf erfolgreiche Pineingabe
        lcd.lcd_clear()
        lcd.lcd_write_line("   A L A R M", 1)
        lcd.lcd_write_line("* > ausschalten", 2)
        while True:  # Endlosschleife, warte auf Taste '*'
            # +++ 4) +++ Beende innere Schleife, wenn '*' gedrückt wurde,
            #  um mit der Eingabe des Pins fortzusetzen
            if pin_pad.is_key_pressed('*'):
                break
        # +++ 4) +++ Beende aeussere Schleife, wenn der eingebene Pin korrekt ist
        if verify_pin():
            break
    # Nach erfolgreicher Pineingabe...
    #  +++ 4) +++ setze alarm auf aus (False)
    is_alarm = False          # Alarm aus
    #  +++ 4) +++ setze alarm auf deaktiviert (False)
    is_alarm_enabled = False  # Alarmanlage aus
    buz.off()                 # Summer aus

# Hauptfunktion
try:
    # +++ 3) +++ Ausfuehren von 'callback_alarm' wenn Bewegung erkannt wurde
    pir.when_motion = callback_alarm

    # +++ 1) +++ Schreibe Projektnamen ins Display
    lcd.lcd_write_line("  Alarmanlage", 1)
    lcd.lcd_write_line("    - RPi -", 2)
    # +++ 1) +++ Zeige Display fuer ein paar Sekunden
    time.sleep(2)
    
    while True:  # Endlosschleife, Abbruch durch [Strg]+[c], Programmabbruch
        # Programm wartet auf Alarm oder Key-Pad-Eingabe
        if is_alarm:
            alarm()
        else:
            menu()
except KeyboardInterrupt:  # [Strg]+[c]
    pin_pad.close()
    print("Programm 'Alarm' beendet.")
