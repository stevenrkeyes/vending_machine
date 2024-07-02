import serial
import serial.tools.list_ports
import time
import warnings


def _find_port_with_name_in_descriptor(name):
    ports = serial.tools.list_ports.comports()
    ports_with_name = [port.device for port in ports if name in port.description]
    if len(ports_with_name) > 1:
        raise RuntimeError("Multiple " + name + " devices plugged in; unable to determine which to use")
    if len(ports_with_name) == 0:
        raise RuntimeError("No ports found with " + name + " in name.")
    return ports_with_name[0]


def find_arduino_port():
    try:
        port = _find_port_with_name_in_descriptor("Arduino Uno")
    except RuntimeError:
        # Todo: maybe identify this port based on sending it a ping or something rather than relying on drivers
        #  to give it an expected name
        warnings.warn("Couldn't find Arduino port; are you missing Arduino drivers? Trying again with generic port name")
        port = _find_port_with_name_in_descriptor("USB Serial Device")
    return port


def find_prolific_port():
    return _find_port_with_name_in_descriptor("Prolific PL2303GS")


# Interruptable version of read_until
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
            time.sleep(0.02)
