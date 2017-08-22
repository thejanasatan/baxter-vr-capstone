import socket
import subprocess
from subprocess import Popen, PIPE
import os
UDP_IP = "10.234.2.251"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
	data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
	print "received message:", data

	dataPart = data.split(" ")

	if (dataPart[0] == 'Play'):
		print "received play request"

		#p = Popen('/home/plebs/baxter-sim/init.sh',stdin=PIPE, stdout=PIPE)   # set environment, start new shell 
		#p = Popen('/home/plebs/baxter-sim/vr-demo.sh',stdin=PIPE, stdout=PIPE)   # set environment, start new shell 
		# command = '/home/plebs/baxter-sim/baxter.sh'
		p = Popen('./baxter.sh',shell=True,stdin=PIPE, stdout=PIPE, executable="/bin/sh")   # set environment, start new shell 

		p.communicate("rosrun baxter_examples joint_position_file_playback.py -f /home/plebs/baxter-movements/" + dataPart[1]) # pass commands to the opened shell
		#print 'Should have run by now'
	elif (dataPart[0] == 'Record'):
		print "received record request"
		#p = Popen('/home/plebs/baxter-sim/recordbaxter', stdin=PIPE, stdout=PIPE) 
		# command = '/home/plebs/baxter-sim/baxter.sh'
		p = Popen('./baxter.sh' ,shell=True, stdin=PIPE, stdout=PIPE, executable='/bin/sh')
		p.communicate('rosrun baxter_examples joint_recorder.py -f /baxter-movements/' + dataPart[1]) 
