"""from threading import Thread

import serial
import io

import http.server
import socketserver

PORT = 8080
HOST_ADDRESS = "localhost"
SERIAL_PATH = "COM12"

serial_data = "-1"
do_stop_serial_thread = False

class SerialMonitorThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.ser = serial.serial_for_url(SERIAL_PATH, timeout = 1)
        self.sio = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser))
    
    def run(self):
        while True:
            global do_stop_serial_thread
            if do_stop_serial_thread:
                break

            global serial_data
            serial_data = self.sio.readline().replace("\n", "")
            print("Serial data:", serial_data)

class request_handler(http.server.BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(http.server.HTTPStatus.OK)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        self.send_response(http.server.HTTPStatus.OK)

        self.send_header("Content-type", "application/json")
        self.send_header("Pragma", "no-cache")
        self.send_header("Access-Control-Allow-Origin", "*")

        self.end_headers()

        self.wfile.write(("{ \"data\": \"" + serial_data + "\"}").encode())

if __name__ == "__main__":
    
    serial = SerialMonitorThread()
    serial.start()

    with socketserver.TCPServer((HOST_ADDRESS, PORT), request_handler) as httpd:
        print("Serving at port", PORT)
        try:
            httpd.serve_forever()
        finally:
            do_stop_serial_thread = True """