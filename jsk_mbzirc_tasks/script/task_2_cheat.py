#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import rospy
import math
from moveit_commander import MoveGroupCommander, conversions
from std_msgs.msg import Float64

__author__ = 'kei.okada@gmail.com (Kei Okada)'

def open_hand():
    msg = Float64()
    msg.data = 0.4
    rospy.loginfo("send %f"%msg.data)
    for i in range(10):
        pub.publish(msg)
        rospy.sleep(0.1)

def close_hand():
    msg = Float64()
    msg.data = -1.0
    for i in range(30):
        pub.publish(msg)
        rospy.sleep(0.1)

if __name__ == '__main__':
    rospy.init_node('task_2_cheat', anonymous=True)
    pub = rospy.Publisher("/r_gripper_controller/command", Float64, queue_size=1)

    # for for 1 sec
    while rospy.get_time() < 5 :
        rospy.sleep(0.01)
    rospy.loginfo("start program %f"%rospy.get_time())

    arm = MoveGroupCommander("ur5_arm")
    arm.set_planner_id('RRTConnectkConfigDefault')

    # open
    open_hand()
    # reach
    rospy.loginfo("reach")
    arm.set_pose_target([0.90, 0.16, 0.233, 0, 0, 0])
    arm.plan() and arm.go()
    arm.plan() and arm.go()
    # approach
    rospy.loginfo("approach")
    arm.set_pose_target([1.13, 0.16, 0.233, 0, 0, 0])
    arm.plan() and arm.go()
    # rotate
    for i in range(2):
        # close
        rospy.loginfo("close")
        close_hand()
        # rotate
        angles = arm.get_current_joint_values()
        import numpy
        start_angle = angles[5]
        print("current angles=", start_angle)
        for r in numpy.arange(start_angle, start_angle-3.14*2, -1.0):
            rospy.loginfo(angles)
            angles[5] = r
            arm.set_joint_value_target(angles)
            rospy.loginfo("rotate (%f)"%(r))
            arm.plan() and arm.go()
        # open
        rospy.loginfo("open")
        open_hand()
        # back
        angles[5] = start_angle
        arm.set_joint_value_target(angles)
        rospy.loginfo("rotate (%f)"%(r))
        arm.plan() and arm.go()
    
    rospy.loginfo("done")

