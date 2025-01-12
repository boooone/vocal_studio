import socket

from _Framework.ControlSurface import ControlSurface

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8899

class VocalStudioServer(ControlSurface):
    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((SERVER_HOST, SERVER_PORT))
        self._socket.listen(1)
        with self.component_guard():
            self.log_message("VocalStudioServer initialized, bitch")
            self.song().start_playing()

#            while True:
#                conn, addr = self._socket.accept()
#
#               request = conn.recv(1024).decode()
#               self.log_message("Received: " + request)
#
#               response = "HTTP/1.1 200 OK\n\n"
#               conn.send(response)
#               conn.close()
#
        self._socket.close()
