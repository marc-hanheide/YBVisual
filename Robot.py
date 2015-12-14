#!/usr/bin/env python
import sys
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from geometry_msgs import *
import move_base_msgs.msg
from std_msgs.msg import *



class Youbot:
    #Init
    def __init__(self):
        rospy.loginfo("Initialising youbot")
        #Init moveit_commander
        moveit_commander.roscpp_initialize(sys.argv)
        #Init rospy
        rospy.init_node('youbot',anonymous=True)
        #Init robot object
        self.robot = moveit_commander.RobotCommander()
        #Init scene object
        self.scene = moveit_commander.PlanningSceneInterface()
        #Init move group object
        self.group = moveit_commander.MoveGroupCommander("arm_1")
        #Display trajectory publisher
        self.display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',moveit_msgs.msg.DisplayTrajectory)
        #move base cmd publisher
        self.move_base_cmdvel_publisher = rospy.Publisher('/move_base/cmd_vel',geometry_msgs.msg.Twist);
        #move base goal publisher
        self.move_base_goal_publisher = rospy.Publisher('/move_base/goal',move_base_msgs.msg.MoveBaseActionGoal);
        #Youbot has been initialised
        rospy.loginfo("Youbot initialised")      
        #Finally - print the initial state of the youbot        
        self.Print_State()
    #print the current robot state
    def Print_State(self):
        rospy.loginfo("Displaying current robot state")
        print self.robot.get_current_state()
        print " "
    #Drive the robot
    def Drive(self,lx,ly,lz,ax,ay,az):
        #Create a twist message
        twist = geometry_msgs.msg.Twist()
        twist.linear.x = lx
        twist.linear.y = ly
        twist.linear.z = lz
        twist.angular.x = ax
        twist.angular.y = ay
        twist.angular.z = az
        #log event
        rospy.loginfo("Driving Youbot")
        #now publish
        for i in range(30):
           self.move_base_cmdvel_publisher.publish(twist)
           rospy.sleep(0.1) # 30*0.1 = 3.0
    #Stop the robot
    def Stop(self):
        self.Drive(0,0,0,0,0,0);





class RobotController:
    #Initialise
    def __init__(self):
        rospy.loginfo("Creating robot controller")
        self.robot = Youbot()
        self.Processing = False;
    #Process incoming data
    def Process(self,data):
        #Set processing
        self.Processing = True;
        #we must split the string
        _data = str.split(data)
        print "DATA: " + _data;
		#Check for application data
		if(_data[0] == "APPDATA")
			#Then - found app data
			print "Found app data";
        #Check for a halt command
        if(_data[0] == "HALT"):
            #If halt - stop the robot
            self.robot.Stop()
        #Now check for a move command
        if(_data[0] == "MOVE"):
            if(_data[1] == "FORWARD"):
                self.robot.Drive(1,0,0,0,0,0);
            if(_data[1] == "BACK"):
                self.robot.Drive(-1,0,0,0,0,0);
            if(_data[1]=="LEFT"):
                self.robot.Drive(0,1,0,0,0,0);
            if(_data[1]=="RIGHT"):
                self.robot.Drive(0,-1,0,0,0,0);
        #Check for a rotate command
        if(_data[0] == "ROTATE"):
            if(_data[1] == "LEFT"):
                #rotate left
                self.robot.Drive(0,0,0,0,1,0);
            if(_data[1] == "RIGHT"):
                #rotate right
                print "Rotating right";
                self.robot.Drive(0,0,0,0,-1,0);
        print "Finished Processing";
        self.Processing = False;
    def isProcessing(self):
        return self.Processing;
                
            
        