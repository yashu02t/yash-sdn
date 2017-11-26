
#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import threading
import os
import sys

HOST = '192.168.56.11'
PORT = 8080
ADDR = (HOST,PORT)

BUFSIZE = 2048
num_of_connections = 0
#HTTPRequestHandler class
class HClientRequestHandler(BaseHTTPRequestHandler):

    #handle GET command
    def do_GET(self):
        global num_of_connections
        if is_under_attack():
            self.send_error(503)
            return
        root_dir = '/home/ubuntu/http_attack/test/'
        root_dir += self.path
        try:
            if self.path.endswith('.html'):
            #if self.path.endswith('.html'):
                
                f = open(root_dir)

                #send code 200 response
                self.send_response(200)

                #send header
                self.send_header('Content-type','text-html')
                self.end_headers()


                #send file content to client
                self.wfile.write(f.read())
                f.close()
                num_of_connections += 1
                return

        except IOError:
            self.send_error(404, 'file not found')

def launch_server():
    web_server_address = ADDR
    server = HTTPServer(web_server_address, HClientRequestHandler)
    print('HTTP server is up and running...')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()

def is_under_attack():
    global num_of_connections
    if num_of_connections > 60:
        return True

def timer_func():
    global num_of_connections
    num_of_connections = 0

if __name__ == '__main__':
    timer = threading.Timer(2, timer_func)
    launch_server()
