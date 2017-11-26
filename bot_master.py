
#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import time

MASTER_HOST = '192.168.60.120'
MASTER_PORT = 8081
ADDR = (MASTER_HOST, MASTER_PORT)


class BotClientRequestHandler(BaseHTTPRequestHandler):
   
    #handle GET command
    def do_GET(self):
        global num_bots
        root_dir = '/home/ubuntu/http_attack/test/'
        root_dir += self.path
        try:
            if self.path.endswith('.txt'):

                f = open(root_dir)

                self.send_response(200, "=====Bot connected to Bot Master======")

                self.send_header('Content-type','text-html')
                self.end_headers()

                self.wfile.write(f.read())
                f.close()
                return

        except IOError:
            self.send_error(404, 'file not found')

def launch_server():
    web_server_address = ADDR
    server = HTTPServer(web_server_address, BotClientRequestHandler)
    print('Bot Master is up and running...')
    server.serve_forever()

if __name__ == '__main__':
    launch_server()