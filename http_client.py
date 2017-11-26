##!/usr/bin/env python

import httplib
import sys
BUFFERSIZE = 2048
buffer = [BUFFERSIZE]

#get http server ip
#http_server = sys.argv[1]
server = '192.168.56.11:8080'
#create a connection
conn = httplib.HTTPConnection(server)
msg = 'info.html'

conn.request('GET', msg)
resp = conn.getresponse(2048)
print "Status %s %s" %(resp.status,resp.reason)

print resp.read()
    
conn.close()
