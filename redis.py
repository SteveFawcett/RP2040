import socket


class Redis:

    def __init__(self , address , port=6379):
        self.sock = socket.socket()
        self.sock.connect( (address, port ))

    def keys(self, pattern='*'):
        cmd = f"*2\r\n$4\r\nKEYS\r\n${len(pattern)}\r\n{pattern}\r\n"
        self.sock.sendall(cmd.encode())
        data = self.sock.recv(4096)  # This may need to be larger for many keys.
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
