#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

import math

class base():
    def __init__(self):
        
        #define location of landmark
        self.landmarks = []
        self.landmarks.append(("Cube", 0.31, -0.99))
        self.landmarks.append(("Dumpster", 0.11, -2.42))
        self.landmarks.append(("Cylinder", -1.14, -2.88))
        self.landmarks.append(("Barrier", -2.59, -0.83))
        self.landmarks.append(("Bookself", -0.09, 0.53))

        self.temp = raw_input("What is your goal?")
        self.goalInput = None
        self.velocity_publisher = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=10)
        self.sub = rospy.Subscriber('/odom', Odometry,self.callback)
        self.rate = rospy.Rate(10)
        self.x = 0
        self.y = 0
        self.orientation = 0
    def distance (self, x1, y1, x2, y2):
        xd = x1 -x2
        yd = y1 - y2
        return math.sqrt(xd*xd +yd*yd)
    def callback(self, data):        
        self.x = data.pose.pose.position.x
        self.y = data.pose.pose.position.y
        self.orientation = data.pose.pose.orientation.z
        rospy.loginfo("x: %f, y: %f", self.x, self.y)
        closest_name = None
        closest_distance = None
        for l_name, l_x, l_y in self.landmarks:
            dist = self.distance(self.x,self.y, l_x, l_y)
            if closest_distance is None or dist <closest_distance:
                closest_name = l_name
                closest_distance = dist
        rospy.loginfo('Closest object is %s', closest_name)


    def moveToGoal(self):
        for land, x, y in self.landmarks:
            if self.temp in land:
                self.goalInput = self.temp
        if self.goalInput is None:
            exit()
        #set movement to 0
        vel_msg = Twist()
        vel_msg.linear.x = 0
        vel_msg.linear.y = 0        
        vel_msg.linear.z = 0

        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = 0
        
        for l_name, l_x, l_y in self.landmarks:
            if l_name == self.goalInput:
                 goal_x = l_x
                 goal_y = l_y
        
        while self.distance(goal_x,goal_y,self.x,self.y) >= .5:
            vel_msg.linear.x = 1
            vel_msg.angular.z = (math.atan2(goal_y - self.y, goal_x - self.x) +self.orientation)
            self.velocity_publisher.publish(vel_msg)
            self.rate.sleep()
        vel_msg.linear.x = 0
        vel_msg.linear.y = 0        
        vel_msg.linear.z = 0

        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)
        rospy.spin()
    def main(self):
        self.moveToGoal()
        exit()
if __name__ == '__main__':
    rospy.init_node('location_monitor')
    newBase =base()
    newBase.main()
    