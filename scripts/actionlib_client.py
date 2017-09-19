import rospy
import baxter_interface
import actionlib
import sys

from rospy import rostime

from copy import copy

from control_msgs.msg import (
    FollowJointTrajectoryAction,
    FollowJointTrajectoryGoal,
)

from baxter_interface import (
    RobotEnable,
)

from trajectory_msgs.msg import (
    JointTrajectoryPoint,
)

from rospy import Duration

class BaxterNode():
  def __init__(self, limb, con_queue, can_queue):
    ns = 'robot/limb/' + limb + '/'
    
    self._limb = limb

    self.sprint('starting node....')
    rospy.init_node('rsdk_baxter_unity')
    
    robot = RobotEnable()
    robot.enable()

    rospy.on_shutdown(self.cleanup)

    self.control_queue = con_queue
    self.cancel_queue = can_queue

    self._limb_interface = baxter_interface.limb.Limb(limb)

    self._client = actionlib.SimpleActionClient(
        ns + "follow_joint_trajectory",
        FollowJointTrajectoryAction,
    )
    self._goal = FollowJointTrajectoryGoal()
    self._goal_time_tolerance = rostime.Time(0.1)
    self._goal.goal_time_tolerance = self._goal_time_tolerance
    server_up = self._client.wait_for_server(timeout=rostime.Duration(10.0))
    if not server_up:
      rospy.logerr("Timed out waiting for Joint Trajectory"
                    " Action Server to connect. Start the action server"
                    " before running example.")
      rospy.signal_shutdown("Timed out waiting for Action Server")
      sys.exit(1)
    self._clear_goal(limb)

  def _add_point(self, positions, time):
    try:
    	point = JointTrajectoryPoint()
    	point.positions = copy(positions)
    	point.time_from_start = rostime.Duration(time)
    	self.sprint('added')
	self._goal.trajectory.points.append(point)
	self.sprint('hello')
    except:
	return  

  def _run_goal(self):
    self.sprint('line 1 %s' % self._goal)
    self._goal.trajectory.header.stamp = rostime.Time.now()
    self._goal.trajectory.header.frame_id = 'base'
    self._client.send_goal(self._goal)

  def _cancel_goal(self):
    self._client.cancel_goal()

  def _wait_for_result(self, timeout=15.0):
    self._client.wait_for_result(timeout=rostime.Duration(timeout))
    self.sprint('waited - timedout')

  def _result(self):
    return self._client.get_result()

  def _clear_goal(self, limb):
    self._goal = FollowJointTrajectoryGoal()
    self._goal.goal_time_tolerance = self._goal_time_tolerance
    self._goal.trajectory.joint_names = [limb + '_' + joint for joint in \
      ['s0', 's1', 'e0', 'e1', 'w0', 'w1', 'w2']]

  def cleanup(self):
    self.control_queue = None
    self.cancel_goal = None
    self._cancel_goal()
    rospy.signal_shutdown('Shutting down....')
    sys.exit(0)

  def start(self):
    self.sprint('process started....')
    while True:
      self.consume_cancel()
      self.consume_control()

  def sprint(self, message):
    print('[rsdk_baxter_unity] %s' % message)

  def consume_control(self):
    try:
      message = self.control_queue.get_nowait()
      point = message['position']
      orientation = message['rotation']
      # self.sprint(point)
      # self.sprint(orientation)
      current_angles = [self._limb_interface.joint_angle(joint) for joint in self._limb_interface.joint_names()]
      self.sprint(current_angles)
      positions = {
        'left':  [-0.11, -0.62, -1.15, 1.32,  0.80, 1.27,  2.39],
        'right':  [0.11, -0.62,  1.15, 1.32, -0.80, 1.27, -2.39],
      }

      # self._clear_goal()
      self.sprint("I'm here")
      self._add_point(current_angles, 0.0)
      p1 = positions[self._limb]
      self._add_point(p1, 7.0)
      self._add_point([x * 0.75 for x in p1], 9.0)
      self._add_point([x * 1.25 for x in p1], 12.0)
      self._run_goal()
      self._wait_for_result(15.0)
    except:
      return

  def consume_cancel(self):
    try:
      self.cancel_queue.get_nowait()
      self._cancel_goal()
    except:
      return
