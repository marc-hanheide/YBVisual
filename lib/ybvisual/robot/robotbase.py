#!/usr/bin/env python
import sys
import rospy
import actionlib
import geometry_msgs.msg
from geometry_msgs import *
from move_base_msgs.msg import *
from actionlib_msgs.msg import *
from nav_msgs.msg import Odometry
import time
from std_msgs.msg import String
import math


#
# Robotbase is used to send goals to the base
#
class RobotBase:
    #Initialise
    def __init__(self):
        #Log
        rospy.loginfo("Creating robot base controller");       
        #Publisher used to manually control the robot
        self.cmd_vel_publisher = rospy.Publisher('/move_base/cmd_vel',geometry_msgs.msg.Twist);
        #Subscribe to the move_base action server
        self.move_base_server = actionlib.SimpleActionClient('move_base',MoveBaseAction);
        #move base goal publisher
        #self.move_base_goal_publisher = rospy.Publisher('/move_base/goal',move_base_msgs.msg.MoveBaseActionGoal);                
        rospy.loginfo("Starting move_base action server..");
        #Wait unil the acton server is available
        self.move_base_server.wait_for_server(rospy.Duration(60));
        rospy.loginfo("Started move_base action server");
        #Linear velocity
        self.linear_velocity = 0.3
        #Angular velocity
        self.angular_velocity = 0.5        
        #Created!    
        rospy.loginfo("Created robot base");
        #Variables can be used to command robot by giving a string
        self.cmd_move_forwards = "FORWARDS"
        self.cmd_move_back = "BACK"
        self.cmd_move_left = "LEFT"
        self.cmd_move_right = "RIGHT"
        self.cmd_rotate_left = "LEFT"
        self.cmd_rotate_right = "RIGHT"
        
    #Process given cmdVel command
    def procCmdVel(self,twist):
        for i in range(30):
            self.cmd_vel_publisher.publish(twist)
    
    #Stop moving the base - cancel all goals
    def Stop(self):
        #Now stop the robot
        rospy.loginfo("Attempting to stop robot")
        self.procCmdVel(geometry_msgs.msg.Twist())        

    #Create a goal message
    def CreateGoal(self,x,y,z,w):
        #Create msg object
        g = MoveBaseGoal()
        g.target_pose.header.frame_id = "base_link";
        g.target_pose.header.stamp = rospy.Time.now()
        g.target_pose.pose.position.x = x; #Move in X axis by meters
        g.target_pose.pose.position.y = y; #Move in Y axis by meters 
        g.target_pose.pose.position.z = z; #Move in Z axis by meters
        g.target_pose.pose.orientation.w = w; #We need to specify an orientation > 0
        return g
    #Move base in direction
    def Move(self,lx,ly,az,amount):
        #Create the twist message
        twist = geometry_msgs.msg.Twist()
        twist.linear.x = lx
        twist.linear.y = ly
        twist.angular.z = az
        self.procCmdVel(twist)        
        #Robot is moving 1 m/s, so we should wait for specified given distance
        time.sleep(amount)
        #Stop the robot after waiting
        self.Stop()
    #Move specified distance - use time to calculate the distance
    def MoveDistance(self,lx,ly,dist):
        rospy.loginfo("Moving distance: " + str(dist) + "m")
        duration = dist / self.linear_velocity
        rospy.loginfo("The move should take: " + str(duration))
        start_time = time.time()
        twist = geometry_msgs.msg.Twist()
        if lx == 1:
            twist.linear.x = self.linear_velocity
        elif lx==-1:
            twist.linear.x = -self.linear_velocity
        else:
            #Do not set linear x
            twist.linear.x = 0
        if ly == 1:
            twist.linear.y = self.linear_velocity
        elif ly == -1:
            twist.linear.y = -self.linear_velocity
        else:
            #do not set linear y
            twist.linear.y = 0
        while ( (time.time() - start_time) < duration ):
            self.procCmdVel(twist)
        rospy.loginfo("Reached!")
        self.Stop()
    #Rotate specified distance (degrees given, converted to radians
    def RotateDistance(self,az,dist):
        _dist = math.radians(dist)
        rospy.loginfo("Rotating distance: " + str(dist) + "degrees" + " or " + str(_dist) + " radians")
        duration = _dist / self.angular_velocity
        rospy.loginfo("Rotation should take: " + str(duration))
        twist = geometry_msgs.msg.Twist()
        if az == 1:
            twist.angular.z = self.angular_velocity
        elif az == -1:
            twist.angular.z = -self.angular_velocity
        else:
            twist.angular.z = 0
        start_time = time.time()
        while( (time.time() - start_time) < duration):
            self.procCmdVel(twist)
        rospy.loginfo("Reached!")
        self.Stop()     
    def _Move(self,lx,ly,az):
        #Create the twist message
        twist = geometry_msgs.msg.Twist()
        twist.linear.x = lx
        twist.linear.y = ly
        twist.angular.z = az
        self.procCmdVel(twist)        

    #Move the base to a goal
    def MoveTo(self,x,y,z):
        #Create the goal 
        goal = self.CreateGoal(x,y,z,1.0);
        #Send the robot to the goal
        rospy.loginfo("Moving robot towards goal");
        self.move_base_server.send_goal(goal);
        #get result
        goalresult= self.move_base_server.wait_for_result(rospy.Duration(50));
        #stop when reached
        self.Stop();