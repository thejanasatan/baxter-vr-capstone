import socket
import subprocess
from subprocess import Popen, PIPE

UDP_IP = "10.234.2.49"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "received message:", data

    if (data == '1'):
    	print "received 1"
	    
	#p = Popen('/home/plebs/baxter-sim/init.sh',stdin=PIPE)   # set environment, start new shell
	p = Popen('./baxter.sh',shell=True,stdin=PIPE, stdout=PIPE, executable="/bin/sh")   # set environment, start new shell 
	#p = Popen("./init.sh",shell=True,stdin=PIPE, stdout=PIPE, executable="/bin/sh")   # set environment, start new shell
	    
        #p.communicate("rosrun baxter_tools enable_robot.py -e") # pass commands to the opened shell 
	p.communicate("./playbaxter-horizontal") # pass commands to the opened shell 
#	p.communicate("rosrun baxter_examples joint_position_file_playback.py -f /home/plebs/baxter-movements/baxter-recording-horizontal.csv") # pass commands to the opened shell
	#p.communicate("./vr-demo2.sh %s" % data) # pass commands to the opened shell 
    elif (data == '2'):
	print "received 2"

	#p = Popen('/home/plebs/baxter-sim/init.sh',stdin=PIPE)   # set environment, start new shell
	p = Popen('./baxter.sh',shell=True,stdin=PIPE, stdout=PIPE, executable="/bin/sh")   # set environment, start new shell 
	#p = Popen("./init.sh",shell=True,stdin=PIPE, stdout=PIPE, executable="/bin/sh")   # set environment, start new shell

	p.communicate("./playbaxter-diagonal") # pass commands to the opened shell 
#	p.communicate("rosrun baxter_examples joint_position_file_playback.py -f /home/plebs/baxter-movements/baxter-recording-diagonal.csv") # pass commands to the opened shell
    elif (data == '3'):
	print "received 3"

	#p = Popen('/home/plebs/baxter-sim/init.sh',stdin=PIPE)   # set environment, start new shell
	p = Popen('./baxter.sh',shell=True,stdin=PIPE, stdout=PIPE, executable="/bin/sh")   # set environment, start new shell 
	#p = Popen("./init.sh",shell=True,stdin=PIPE, stdout=PIPE, executable="/bin/sh")   # set environment, start new shell

	p.communicate("./playbaxter-vertical") # pass commands to the opened shell 
#	p.communicate("rosrun baxter_examples joint_position_file_playback.py -f /home/plebs/baxter-movements/baxter-recording-vertical.csv") # pass commands to the opened shell

