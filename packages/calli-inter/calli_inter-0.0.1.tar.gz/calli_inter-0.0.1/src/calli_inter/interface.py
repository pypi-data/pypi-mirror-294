import serial
import serial.tools.list_ports as list_ports
from time import *

PID_CALLIOPE_1 = 516
VID_CALLIOPE_1 = 3368

# TODO: Calliop 2, Calliop 3,

TIMEOUT = 0.1

BAUD = 115200

def find_comport():
    ser_port = serial.Serial(timeout=TIMEOUT)
    ser_port.baudrate = BAUD
    ports = list(list_ports.comports())
    for p in ports:
        try:        
            if (p.pid == PID_CALLIOPE_1) and (p.vid == VID_CALLIOPE_1):            
                ser_port.port = str(p.device)
                return ser_port
            
            # TODO: Calliope 2, Calliop 3,

        except AttributeError:
            continue

    return None

def readline(s):
    char = s.read()
    val = char
    while char != b'9':
        char = s. read()
        val = val + char
    return val
        

class Interface:
    def __init__(self, comport=False):
        if comport:
            self.s = serial.Serial(comport)
        else:
            self.s = find_comport()
            if not self.s:
                raise Exception("Calliope not found")
            self.s.open()
        
    def write(self, value):        
        if (value):
            self.s.write(b'1\n')
        else:
            self.s.write(b'0\n')
            
    def read(self):
        self.s.write(b't\n')
        value = readline(self.s)        
        if value[0] == 0x30:
            return 0
        else:
            return 1

    def close(self):
        self.s.close()