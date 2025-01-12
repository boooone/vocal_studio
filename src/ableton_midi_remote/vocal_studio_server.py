import socket
import socketserver
import threading
import io
import json

from http.server import BaseHTTPRequestHandler, HTTPServer

from contextlib import redirect_stderr

from _Framework.ControlSurface import ControlSurface

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8899

class VocalStudioTCPServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass, vocal_studio_server, bind_and_activate=True):
        socketserver.TCPServer.__init__(self, server_address, MyTCPHandler, bind_and_activate)
        self._vocal_studio = vocal_studio_server
   
class MyTCPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Get the length of the JSON data in the request
            content_length = int(self.headers.get('Content-Length', 0))
            
            # Read the JSON data from the request body
            raw_data = self.rfile.read(content_length)
            json_data = json.loads(raw_data.decode('utf-8'))
            
            for command_json in json_data:
                for command_name, command_data in command_json.items():
                    self.handle_command(command_name, command_data)
            # Log the parsed JSON data
            self.ableton_log_message("Received JSON data:")
            self.ableton_log_message(json.dumps(json_data, indent=4))

            # Send a response
            self.ableton_log_message("Sending response...")
            self.send_response(200)
            self.ableton_log_message("Response sent")
            self.send_header('Content-Type', 'application/json')
            self.ableton_log_message("Header sent")
            self.end_headers()
            self.ableton_log_message("Headers ended")
            response = {"status": "success", "message": "JSON data received"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            self.ableton_log_message("Response sent:")
        except json.JSONDecodeError as e:
            # Handle invalid JSON data
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"status": "error", "message": f"Invalid JSON: {str(e)}"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        finally:
            self.request.close()
    def __handle(self):
        self.ableton_log_message("Connected, Recieving ...")
        self.data = self.request.recv(1024).strip()
        self.handle_command("stop")
        self.ableton_log_message("Received: " + str(self.data))
        self.request.sendall(bytes("HTTP/1.1 200 OK\n\n", 'utf-8'))
        self.request.close()
        self.ableton_log_message("Connection closed")

    def handle_command(self, command_name, command_data):
        with self.server._vocal_studio.component_guard():
            self._dispatch_command_component_guarded(command_name, command_data)

    def _dispatch_command_component_guarded(self, command_name, command_data,):
        if command_name == "/song/stop":
            self.server._vocal_studio.song().stop_playing()
        if command_name == "/song/start":
            self.server._vocal_studio.song().start_playing()
    
    def ableton_log_message(self, message):
        with self.server._vocal_studio.component_guard():
            self.server._vocal_studio.log_message(message)

class VocalStudioServer(ControlSurface):
    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)

        
        self._socket_thread_io = io.StringIO()
        self._socketserver = VocalStudioTCPServer((SERVER_HOST, SERVER_PORT), MyTCPHandler, self)
        self._socketserver_thread = threading.Thread(target=self.server_thread)
        self._socketserver_thread.start()
        with self.component_guard():
            self.log_message("VocalStudioServer initialized, bitch")
            # Get method names on c_instance
            methods = [method_name for method_name in dir(c_instance) if callable(getattr(c_instance, method_name))]
            self.log_message("Methods on c_instance: " + str(methods))
            
            # Get method names on song
            methods = [method_name for method_name in dir(self.song()) if callable(getattr(self.song(), method_name))]
            self.log_message("Methods on song: " + str(methods))

            self.song().start_playing()
            self.log_message("Socekt Server address " + hex(id(self._socketserver)))

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
    def server_thread(self):
        with self.component_guard():
            self.log_message("Socket Server address in thread is: " + hex(id(self._socketserver)))
        # with self._socket_thread_io as buffer, redirect_stderr(buffer):
        self._socketserver.serve_forever()

    def disconnect(self):
        with self.component_guard():
            self._socketserver.shutdown()
            self._socketserver_thread.join()
            self._socketserver.server_close()
        super(VocalStudioServer, self).disconnect()
