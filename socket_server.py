#!/usr/bin/env python

import rospy
import socket

from unite_conference.msg import VRCommand, clash
from baxter_core_msgs.msg import HeadPanCommand

def main():
    print 'Starting the web proxy'
    rospy.init_node('unity_web_proxy')

    command_pub = rospy.Publisher('/robot/unity_command', VRCommand, queue_size=1, tcp_nodelay=True)
    cancel_pub = rospy.Publisher('/robot/unity_command_cancel', clash, queue_size=1, tcp_nodelay=True)
    start_pub = rospy.Publisher('/robot/unity_command_start', clash, queue_size=1, tcp_nodelay=True)
    end_pub = rospy.Publisher('/robot/unity_command_end', clash, queue_size=1, tcp_nodelay=True)
    head_pan = rospy.Publisher('/robot/head/command_head_pan', HeadPanCommand, queue_size=1, tcp_nodelay=True)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('10.42.1.254', 5007))
    print 'socket bound...'

    rospy.on_shutdown(cleanup)

    while not rospy.is_shutdown():
        msg, addr = sock.recvfrom(1024)
        if msg.startswith('baxter_pos'):
	    #print 'ignore baxter pos'
	    continue
     
        comm, limb, pos, rot = sanitize(msg)

        # print msg
     
        if comm == 'move_arm': 
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
        elif comm == 'clash':
            # command = VRCommand()
            # command.command = comm
            cancel_pub.publish(True)
        elif comm == 'start':
            print 'starting now...'
            start_pub.publish(True)
        elif comm == 'end':
            print 'ending now...'
            end_pub.publish(True)
        elif comm == 'enemy_face_angle':
            head_pan.publish(float(limb)*-1, 1, 0)
            # print limb
            # if limb > 1.5 or limb < -1.5:
            #     head_pan.publish(0, 1, 0)
    rospy.spin()

def sanitize(data):
    #print "sanitize",data
    if data == 'clash': return data, None, None, None
    elif data == 'start': return data, None, None, None
    elif data == 'end': return data, None, None, None
    elif data.startswith('enemy_face_angle'):
        data = data.rstrip(')').split('(')
        return data[0], data[1], None, None
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
