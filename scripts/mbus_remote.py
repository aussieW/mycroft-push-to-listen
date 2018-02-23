
#! /usr/bin/env python
# python mbus.py localhost "mycroft.stop"

import sys
from websocket import create_connection
uri = 'ws://' + sys.argv[1] + ':8181/core'
ws = create_connection(uri)
print "Sending " + sys.argv[2] + " to " + uri + "..."
if len(sys.argv) >= 4:
    data = sys.argv[3]
else:
    data = "{}"

message = '{"type": "' + sys.argv[2] + '", "data": "'+ data +'"}'
result = ws.send(message)
print "Receiving..."
result =  ws.recv()
print "Received '%s'" % result
ws.close()