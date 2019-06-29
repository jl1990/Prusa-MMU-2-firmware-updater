import serial
import time
import os
from serial import Serial
import glob
import sys

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def reset_avr109(validPort):
    ser = serial.Serial()
    ser.port = validPort
    ser.baudrate = 1200
    ser.open()
    ser.setDTR(0)
    ser.close()
    time.sleep(1)

validSerialPorts = list(filter(lambda portName: "ACM" in portName, serial_ports()))
validPort = validSerialPorts[0]
reset_avr109(validPort)
os.system("avrdude -vv -p atmega32u4 -P " + validPort + " -c avr109 -b 57600 -D -U flash:w:MM-control-01.hex:i")