import socket


class Redis:

    def __init__(self , address , port=6379):
        self.sock = socket.socket()
        self.sock.connect( (address, port ))

    def keys(self, pattern='*'):
        cmd = f"*2\r\n$4\r\nKEYS\r\n${len(pattern)}\r\n{pattern}\r\n"
        self.sock.sendall(cmd.encode())
        return self.receive()

    def read(self, key, pattern='DATA'):
        command = f"{pattern}:{key}"
        cmd = f"*2\r\n$3\r\nGET\r\n${len(command)}\r\n{command}\r\n"
        self.sock.sendall(cmd.encode())
        return self.receive()[0]

    def write(self, key, value , pattern='DATA'):
        redis_key = f"{pattern}:{key}"
        cmd = f"*3\r\n$3\r\nSET\r\n${len(redis_key)}\r\n{redis_key}\r\n${len(str(value))}\r\n{value}\r\n"
        self.sock.sendall(cmd.encode())
        return self.receive( )

    def receive(self, size=4096 ):
        data = self.sock.recv( size )
        return self._parse_resp(data)

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

if __name__ == "__main__":
    r = Redis( "cache.local" )
    print( r.keys() )
    print( r.read( "PLANE ALTITUDE" )) 
    r.write( "PLANE ALTITUDE" , 8.99999 ) 
    print( r.read( "PLANE ALTITUDE" )) 
