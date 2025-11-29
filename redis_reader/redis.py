import socket
import time
from machine import Pin,UART

BAUD_RATE = 9600

class Redis:

    def __init__(self):
        self.uart = UART(1, baudrate=BAUD_RATE, tx=Pin(20), rx=Pin(21))
        self.uart.init(bits=8, parity=None, stop=1)

    def ping(self):
        # Redis protocol: send "PING\r\n"
        self.uart.write(b"PING\r\n")
        self.receive()
                
    def keys(self, pattern='*'):
        cmd = f"*2\r\n$4\r\nKEYS\r\n${len(pattern)}\r\n{pattern}\r\n"
        self.uart.write( cmd.encode())
        return self.receive()

    def read(self, key, pattern='DATA'):
        command = f"{pattern}:{key}"
        cmd = f"*2\r\n$3\r\nGET\r\n${len(command)}\r\n{command}\r\n"
        self.uart.write(cmd.encode())
        return self.receive()[0]

    def write(self, key, value , pattern='DATA'):
        redis_key = f"{pattern}:{key}"
        cmd = f"*3\r\n$3\r\nSET\r\n${len(redis_key)}\r\n{redis_key}\r\n${len(str(value))}\r\n{value}\r\n"
        self.uart.write(cmd.encode())
        return self.receive( )

    def receive(self, size=4096 ):
        time.sleep(0.5)
        if self.uart.any():
            data = self.uart.read()
            return self._parse_resp(data)
        return None

    def _parse_resp(self, data):
        lines = data.decode().splitlines()
        keys = []
        for line in lines:
            if line.startswith('$') or line.startswith('*'):
                continue  # skip RESP length or array indicators
            keys.append(line)
        return keys

    def __del__(self):
        self.sock.close()
