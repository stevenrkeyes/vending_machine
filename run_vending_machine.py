import os
import serial
import threading
import time
from queue import Queue

from order import Order
from vending_machine_gui import VendingMachineGUI
from vending_machine_port_reading_utils import find_arduino_port, find_prolific_port, read_serial_until

# Use a Queue because it is thread-safe
orders_received = Queue()


def read_from_keypad(serial_port):
    with serial.Serial(serial_port, baudrate=9600, timeout=1) as keypad_port:
        while True:
            # The keypad terminates its lines with '\r' (not '\n' or '\r\n')
            requested_item = read_serial_until(keypad_port, b'\r')
            order = Order(requested_item)
            orders_received.put(order)


def read_from_buttons(serial_port, button_mapping):
    with serial.Serial(serial_port, baudrate=9600, timeout=1) as button_port:
        while True:
            button_number = read_serial_until(button_port, b'\n')
            requested_item = button_mapping[int(button_number)]
            order = Order(requested_item)
            orders_received.put(order)


def update_gui(gui):
    while True:
        if not orders_received.empty():
            new_order = orders_received.get()
            gui.add_new_order(str(new_order))

            # Log the order to a text file for nostalgia
            print(new_order, flush=True)
            log_file = open("log.txt", "a")
            log_file.writelines([str(new_order) + "\n"])
            log_file.close()

            time.sleep(0.02)


button_config_filepath = "button_config.txt"

if __name__ == "__main__":
    # Check for button label config and ask operator if they would like to update it
    if os.path.isfile(button_config_filepath):
        print("Existing button configuration found:")
        with open(button_config_filepath) as file:
            print(file.read())
        will_modify = input("Would you like to edit it? (y/n) ")
        if will_modify == "y":
            print("Exiting. Please edit " + button_config_filepath)
            time.sleep(1)
            exit()
    else:
        # Todo: These are probably in order from bottom to top lol. probably flip these here and in the arduino code
        #  to be top-to-bottom and also 1-indexed
        blank_config = '0. \n1. \n2. \n3. \n4. \n5. \n6. \n'
        with open(button_config_filepath, 'w') as file:
            file.write(blank_config)
        print("Button configuration not yet created. Blank template created. Please fill it out.")
        # Block for a second so that the user can read the message if it's being run as a batch script
        time.sleep(1)
        exit()

    # Load the button label config
    with open(button_config_filepath) as file:
        numbers_and_labels = [line.split(". ") for line in file.readlines()]
        button_mapping = {int(pair[0]): pair[1].strip() for pair in numbers_and_labels}

    # Connect to the Arduino (for buttons) and keypad
    arduino_port = find_arduino_port()
    keypad_port = find_prolific_port()
    print()
    print(f"Reading from keypad on {keypad_port} and Arduino (buttons) on {arduino_port}.")
    print("Press Ctrl+C to stop.")
    print('', flush=True)

    gui = VendingMachineGUI()

    keypad_thread = threading.Thread(target=read_from_keypad, args=(keypad_port,), daemon=True)
    keypad_thread.start()

    button_thread = threading.Thread(target=read_from_buttons, args=(arduino_port, button_mapping,), daemon=True)
    button_thread.start()

    update_gui_thread = threading.Thread(target=update_gui, args=(gui,), daemon=True)
    update_gui_thread.start()

    gui.run()
