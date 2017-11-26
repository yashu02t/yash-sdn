##Client code for DDoS Project
import sys

from socket import *

HOST = '192.168.56.11'
PORT = 8080
ADDR = (HOST,PORT)
BUFSIZE = 2048

message='info.txt'

client = socket(AF_INET,SOCK_STREAM)
client.connect((ADDR))

client.send("GET /%s HTTP/1.1\r\n" % message)

data = client.recv(BUFSIZE)
data = data.rstrip()
print data

client.close()
