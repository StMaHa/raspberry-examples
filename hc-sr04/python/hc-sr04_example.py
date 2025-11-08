from gpiozero import InputDevice, OutputDevice
import time

 
# Constants of GPIO-Pins
GPIO_TRIGGER = 24
GPIO_ECHO = 23
 
# Get instances of GPIO-Pins
trigger_pin = OutputDevice(GPIO_TRIGGER)
echo_pin = InputDevice(GPIO_ECHO)


def get_distance():
    # normalize trigger signal
    trigger_pin.value = 0
    time.sleep(0.000001)

    # set trigger pin to HIGH
    trigger_pin.value = 1

    # trigger signal stays low for 10 micro seconds
    time.sleep(0.00001)

    # set trigger pin to LOW
    trigger_pin.value = 0

    # wait for echo signal goes high
    while echo_pin.value == 0:
        pass
    start_time = time.time()

    # wait for echo signal goes low
    while echo_pin.value == 1:
        pass
    stop_time = time.time()

    # calculate the elapsed time between the rising and falling edges of the echo signal
    time_elapsed = stop_time - start_time
    # calculate the distance by multiplying it by the speed of sound (343m/s)
    # devide by 2 to get only one way
    distance = (time_elapsed * 34300) / 2

    return distance


if __name__ == '__main__':
    try:
        print("Start measuring distance...")
        while True:
            distance = get_distance()
            print(f"Measured distance: {distance:.1f} cm")
            time.sleep(2)

        # Cancel program by pressing CTRL+C
    except KeyboardInterrupt:
        print("END")