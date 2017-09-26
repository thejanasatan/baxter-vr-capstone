#!/usr/bin/env python

import rospy
import baxter_interface
from baxter_interface import CHECK_VERSION

import sys
import socket
import argparse

def main():
  print 'starting web receiver...'
  rospy.init_node('unity_web_receiver')
  
  arg_fmt = argparse.ArgumentDefaultsHelpFormatter
  parser = argparse.ArgumentParser(formatter_class=arg_fmt)

  parser.add_argument(
    "-p", "--port", dest="port", default="5006", 
    help="Port that the Websocket server is listening on"
  )

  parser.add_argument(
    "-s", "--host", dest="host", default="10.42.0.1",
    help="IP that the Websocket server is listening on"
  )

  args = parser.parse_args(sys.argv[1:])

  def cleanup():
    print 'shutting down the web receiver'

  rospy.on_shutdown(cleanup)

  sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
  sock.bind((args.host, int(args.port)))
  
  print 'UDP Server listening on %s:%s' % (args.host, args.port)

  print 'registering the publisher'

  publisher = rospy.Publisher(
    'robot/unity_command',
    UnityCommand,
    latch=False,
    tcpnodelay=True,
  )

  if publisher == None:
    print 'publisher could not be registered successfully'

  while True:
    msg = sock.recv(1024)
    print msg

    publisher.publish(msg)

if __name__ == '__main__':
  sys.exit(main())