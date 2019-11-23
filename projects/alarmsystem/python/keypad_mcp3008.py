from gpiozero import MCP3008
from time import sleep


# Class
class PinPad:
    # initialisation of class
    def __init__(self, pin_digit_count=4, max_voltage=3.3):
        self.pin_digit_count = pin_digit_count
        self.max_voltage = max_voltage
        self.keypad_adc_row_list = []
        self.invalid_pin_digits = ['A', 'B', 'C', 'D', '*', '#']
        self.keypad_matrix = [['1', '2', '3', 'A'],
                              ['4', '5', '6', 'B'],
                              ['7', '8', '9', 'C'],
                              ['*', '0', '#', 'D']]
        # setup MCP3008 instance for each pin pad row (left column 0.25 * VDD, right column 1 * VDD)
        for row in range(4):
            self.keypad_adc_row_list.append(MCP3008(max_voltage=self.max_voltage, channel=row))

    # close MCP3008 instances
    def close(self):
        for row in range(4):
            self.keypad_adc_row_list[row].close()

    # get state of key
    #  returns true if given key has been pressed, false otherwise
    def is_key_pressed(self, key, debug=False):
        key_state = False
        row = 0
        for row_digit_list in self.keypad_matrix:  # loop through rows
            if key in row_digit_list:
                column = row_digit_list.index(key)  # get column if key exists in pin pad row
                break
            row += 1  # increment for next row list,

        row_level = self.keypad_adc_row_list[row].value
        # if voltage level of row matches column
        if row_level > ((column + 1) * 0.2) and row_level < ((column + 2) * 0.2):
            if debug:
                print(key, row + 1, column + 1, row_level)
            key_state = True
            sleep(0.5)
        return key_state

    # get pressed key
    #  returns pressed key
    def get_key(self, debug=False):
        key = ""
        # loop through row at get voltage level as value of column
        for row in range(len(self.keypad_adc_row_list)):
            column = 0
            row_level = self.keypad_adc_row_list[row].value
            if row_level > 0.2:  # voltage devider at 0.25 * VDD
                column += 1
            if row_level > 0.4:  # voltage devider at 0.5 * VDD
                column += 1
            if row_level > 0.6:  # voltage devider at 0.75 * VDD
                column += 1
            if row_level > 0.8:  # voltage devider at 1 * VDD
                column += 1
            if column > 0:  # 0 means no key found. Array index starts at 0. To access array, decrement column.
                key = self.keypad_matrix[row][column - 1]  # get key from matrix
                if debug:
                    print(key, row_level)
                sleep(0.5)  # simple debouncing
        return key  # return pressed key

    # get pin
    #  returns entered pin
    def get_pin(self, debug=False):
        pin = ""
        digit_count = 0
        while digit_count < self.pin_digit_count:  # loop until all keys have been entered
            key = self.get_key(debug)  # get pressed key

            if key is '*':  # if * pressed, cancel pin input procedure
                pin = ""
                break

            if key in self.invalid_pin_digits:  # allow only numerical keys
                key = ""

            if key:  # if key pressed, add digit to pin string
                digit_count += 1
                pin = pin + key
        return pin  # return pin string

# main as example, will be ignored if imported as library
if __name__ == "__main__":
    expected_pin = "1234"
    entered_pin = ""
    try:
        pin_pad = PinPad()
        print("Enter * to continue...")
        while True:
            if pin_pad.is_key_pressed('*'):
                break
        while True:
            print("Enter pin:")
            entered_pin = pin_pad.get_pin(debug=True)
            print(entered_pin)
            if expected_pin == entered_pin:
                break
    except KeyboardInterrupt:
        pass
    pin_pad.close()
    print("Program exit.")
