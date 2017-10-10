#!/usr/bin/env python

import rospy
import socket

from unity_ros_msgs.msg import VRCommand

def main():
  print 'Starting the web proxy'
  rospy.init_node('unity_web_proxy')

  command_pub = rospy.Publisher('/robot/unity_command', VRCommand, queue_size=1, tcp_nodelay=True)

  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.bind(('10.42.1.254', 5006))
  print 'socket bound...'

  rospy.on_shutdown(cleanup)

  while not rospy.is_shutdown():
    msg, addr = sock.recvfrom(1024)
    comm, limb, pos, rot = sanitize(msg)
    
    command = VRCommand()
    command.command = comm
    command.limb = limb
    command.pose.position.x = pos[0]
    command.pose.position.y = pos[1]
    command.pose.position.z = pos[2] 
    command.pose.orientation.x = rot[0]
    command.pose.orientation.y = rot[1]
    command.pose.orientation.z = rot[2]
    command.pose.orientation.w = rot[3]

    command_pub.publish(command)

  rospy.spin()

def sanitize(data):
  command, limb, pos, rot = data.split('|')
  posx, posy, posz = pos.replace('(', '').replace(')','').split(',')
  rotx, roty, rotz, rotw = rot.replace('(','').replace(')', '').split(',')
  position = (float(posx),float(posy), float(posz))
  rotation = (float(rotx), float(roty), float(rotz), float(rotw))

  return command, limb, position, rotation

def cleanup():
  print 'cleaning up...'
  command_pub = None

if __name__ == '__main__':
  try:
    main()
  except rospy.ROSInterruptException:
    pass
