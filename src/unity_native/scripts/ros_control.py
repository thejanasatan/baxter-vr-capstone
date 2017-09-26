#!/usr/bin/env python

import rospy
import baxter_interface
from baxter_interface import (
  CHECK_VERSION,
  RobotEnable,
)

import sys

def main():
  print 'starting the ros control node...'
  rospy.init_node('unity_ros_control')

  def cleanup():
    print 'shutting down the ros control node...'

  rospy.on_shutdown(cleanup)

  rospy.spin()


if __name__ == '__main__':
  sys.exit(main())