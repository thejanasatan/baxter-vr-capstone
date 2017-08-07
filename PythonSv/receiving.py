import socket
import subprocess
from subprocess import Popen, PIPE

UDP_IP = "10.234.2.213"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "received message:", data

    if (data == 'Trigger'):
    	print "received input"
	    
	    p = Popen("./init.sh",stdin=PIPE)   # set environment, start new shell
	    
	    p.communicate("rosrun baxter_tools enable_robot.py -e") # pass commands to the opened shell 
