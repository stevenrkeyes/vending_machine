import datetime
import serial
import serial.tools.list_ports
import threading
import time
from queue import Queue



def _find_port_with_name_in_descriptor(name):
    ports = serial.tools.list_ports.comports()
    ports_with_name = [port.device for port in ports if name in port.description]
    if len(ports_with_name) > 1:
        raise RuntimeError("Multiple " + name + " devices plugged in; unable to determine which to use")
    if len(ports_with_name) == 0:
        raise RuntimeError("No ports found with " + name + " in name.")
    return ports_with_name[0]


def find_arduino_port():
    return _find_port_with_name_in_descriptor("Arduino Uno")


def find_prolific_port():
    return _find_port_with_name_in_descriptor("Prolific PL2303GS")


# Interruptible version of read_until
def read_serial_until(port, terminator):
    buffer = b""
    while True:
        # Read one byte at a time so that it's not blocking at the I/O level, which is uninterruptible
        if port.in_waiting > 0:
            byte = port.read(1)
            buffer += byte
            if byte == terminator:
                line = buffer.decode('utf-8').strip()
                return line
        else:
            # Sleep briefly to avoid busy waiting
            time.sleep(0.05)


# Use a Queue because it is thread-safe
orders_received = Queue()


def read_from_keypad(serial_port):
    with serial.Serial(serial_port, baudrate=9600, timeout=1) as keypad_port:
        while True:
            # The keypad terminates its lines with '\r' (not '\n' or '\r\n')
            order = read_serial_until(keypad_port, b'\r')
            orders_received.put(order)


def read_from_buttons(serial_port):
    with serial.Serial(serial_port, baudrate=9600, timeout=1) as button_port:
        while True:
            order = read_serial_until(button_port, b'\n')
            orders_received.put(order)


if __name__ == "__main__":
    arduino_port = find_arduino_port()
    keypad_port = find_prolific_port()
    print(f"Reading from keypad on {keypad_port} and Arduino (buttons) on {arduino_port}.")
    print("Press Ctrl+C to stop.")
    print('', flush=True)
    
    keypad_thread = threading.Thread(target=read_from_keypad, args=(keypad_port,), daemon=True)
    keypad_thread.start()
    
    button_thread = threading.Thread(target=read_from_buttons, args=(arduino_port,), daemon=True)
    button_thread.start()
    
    while True:
        if not orders_received.empty():
            print(orders_received.get(), flush=True)
            time.sleep(0.05)
