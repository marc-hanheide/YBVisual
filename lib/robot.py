#!/usr/bin/env python
import sys
import rospy
from lib.jsonparser import *
import moveit_commander
import moveit_msgs.msg
import actionlib
import geometry_msgs.msg
from geometry_msgs import *
import move_base_msgs.msg
from move_base_msgs.msg import *
from actionlib_msgs.msg import *
from std_msgs.msg import *


#
# Robotbase is used to send goals to the base
#
class RobotBase:
    #Initialise
    def __init__(self):
        rospy.loginfo("Creating robot base");       
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
        #Created!    
        rospy.loginfo("Created robot base");
    #Stop moving the base - cancel all goals
    def Stop(self):
        self.Move(0,0,0,0);
        self.move_base_server.cancel_goal();
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
    def Move(self,lx,ly,lz,az):
        #Create a twist message
        twist = geometry_msgs.msg.Twist()
        twist.linear.x = lx
        twist.linear.y = ly
        twist.linear.z = lz
        twist.angular.x = 0
        twist.angular.y = 0
        twist.angular.z = az
        #log event
        rospy.loginfo("Driving Youbot")
        
        #publish
        self.cmd_vel_publisher.publish(twist)
             
        
        
        #now publish
        #fo i in range(30):
           #self.cmd_vel_publisher.publish(twist)
           #rospy.sleep(0.1) # 30*0.1 = 3.0
    
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
    
    



#
# Primary Youbot class
#
class Youbot:
    #Initialise
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
        #robot base
        self.base = RobotBase();       
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
    def Drive(self,lx,ly,lz,az):
        #Create a twist message
        self.base.Move(lx,ly,lz,az);
    #Drive the robot to a goal
    def DriveTo(self,x,y,z):
        #Create appropriate ROS message
        self.base.MoveTo(x,y,z);
    #Stop the robot
    def Stop(self):
        #stop the base
        self.base.Stop();
#
# Robot controller
#
class RobotController:
    #Initialise
    def __init__(self):
        #Define the youbot object
        self.robot = Youbot();
        self.Processing = False;
    #Process incoming data
    def Process(self,data):
        #Create JSON object using given data
        #json_data = JSONObject(data);
        
        #Get the commands from the json data
        #commands = json.getData('commands');
        commands_json = JSONObject(data.getData('attribute'))
        commands = commands_json.getData('commands')
        #Cycle through, and manage the given commands
        for command in commands:
            #
            # We may get, and print command info 
            #
            _command = JSONObject(command);
            _type = _command.getData('type');
            _att = _command.getData('attribute');
            _val = _command.getData('value');
            print "Command Given"
            print "TYPE: "  + _type;
            print "ATTRIBUTE: " + _att;
            print "VALUE: " + _val;
       

            #
            # Now we need to check the given type, and use the data appropriately
            #
            if(_type == "APPDATA"):
                # -- Now process the application data, and save it to file
                xml_file = open(_data + ".xml","wb");
                xml_file.write(_data02);
                xml_file.close();
                print xml_file
            #Move type command
            if(_type == "MOVE"):
                    print "Move command";
                    #Get amount value
                    amount = float(_val);
                    print "Amount: " + str(amount);
                    if(_att == "FORWARDS"):
                        print "Move forward command";
                        #self.robot.Drive(1,0,0,0,0,0);
                        self.robot.DriveTo(amount,0,0);
                        #Process the data here - move the robot forward
                    if(_att == "BACK"):
                        print "Move backward command";
                        #self.robot.Drive(-1,0,0,0,0,0);
                        self.robot.DriveTo(-amount,0,0);
                        #Move the robot back
                    if(_att == "LEFT"):
                        print "Move left command";
                        #self.robot.Drive(0,1,0,0,0,0);
                        self.robot.DriveTo(0,amount,0);
                        #Move the robot left
                    if(_att == "RIGHT"):
                        print "Move right command";
                        #self.robot.Drive(0,-1,0,0,0,0);
                        self.robot.DriveTo(0,-amount,0);
                        #Move the robot right
            #Rotate type command
            if(_type == "ROTATE"):
                    if(_att == "RIGHT"):
                        #Rotate the robot right
                        print "Rotate right command";
                        self.robot.Drive(0,0,0,1);
                    if(_att == "LEFT"):
                        #Rotate the robot left
                        print "Rotate left command";
                        self.robot.Drive(0,0,0,-1);
            #halt type command
            if(_type == "HALT"):
                print "Halt command";
                self.robot.Stop();
            
            #Pause before starting next command
            rospy.sleep(0.2);
                
        #Stop the robot once execution has finished
        self.robot.Stop();
