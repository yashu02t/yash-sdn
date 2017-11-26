
import time, os, sys, string, threading, math

from socket import *  #importing the socket library for network connections

class MyServer():
  def __init__(self, host, port):
    self.host = host
    self.port = port

    #Creating socket object
    self.sock = socket(AF_INET,SOCK_STREAM)

    #bind socket to address
    self.sock.bind((self.host, self.port))
    self.sock.listen(100)
    print 'Server up and running! Listening for incomming connections...'


  def acceptConnections(self):
    conn, addr = self.sock.accept() ## accept incoming connection
    data = conn.recv(1024)
    print "Message From " + addr[0] + " : " + data
    print 'Connected by ', addr
    print ">>>>>>>>>>>>>"

    command, file_name, httpv= data.split()   #strip HTTP request "GET /%s HTTP/1.1\r\n" to get filename
    datapath = "/home/ubuntu/tcp_attack/test/" + file_name
    fd=open(datapath)
    body = fd.read()
    fd.close()
    conn.send(body)
    conn.close()

##Setting up variables
HOST = '192.168.56.11'
PORT = 8080
ADDR = (HOST,PORT)
BUFSIZE = 2048

if __name__ == '__main__':
  server = MyServer(HOST, PORT)

  while True:
    server.acceptConnections()