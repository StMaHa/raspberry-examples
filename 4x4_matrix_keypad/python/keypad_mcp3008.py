from gpiozero import MCP3008
from time import sleep


class PinPad:

    def __init__(self):
        self.keypad_rows = []
        self.max_pin_digits = 4
        self.invalid_pin_digits = ['A', 'B', 'C', 'D', '*', '#']
        self.keypad = [['1', '2', '3', 'A'],
                       ['4', '5', '6', 'B'],
                       ['7', '8', '9', 'C'],
                       ['*', '0', '#', 'D']]
        # setup array of objects
        for row in range(4):
            self.keypad_rows.append(MCP3008(max_voltage=3.3, channel=row))


    def close(self):
        # close objects
        for row in range(4):
            self.keypad_rows[row].close()


    def get_key(self):
        key = ""
        # loop through row at get voltage level as value of column
        for row in range(len(self.keypad_rows)):
            column = 0
            row_value = self.keypad_rows[row].value
            if row_value > 0.2:  # 0.25
                column += 1
            if row_value > 0.4:  # 0.5
                column += 1
            if row_value > 0.6:  # 0.75
                column += 1
            if row_value > 0.8:  # 1
                column += 1
            if column > 0:
               key = self.keypad[row][column - 1]
               sleep(0.5)  # simple debouncing
        return key


    def get_pin(self):
        pin = ""
        digit_count = 0
        while digit_count < self.max_pin_digits:
            key = self.get_key()
            if key:
                print(key)

            if key is '*':
                pin = ""
                break

            if key in self.invalid_pin_digits:
                key = ""

            if key:
                digit_count += 1
                pin = pin + key
        return pin



if __name__ == "__main__":
    expected_pin = "1234"
    entered_pin = ""
    try:
        pin_pad = PinPad()

        while True:
            print("Enter pin:")
            entered_pin = pin_pad.get_pin()
            print(entered_pin)
            if expected_pin == entered_pin:
                break
    except KeyboardInterrupt:
        pass
    pin_pad.close()
    print("Program exit.")
